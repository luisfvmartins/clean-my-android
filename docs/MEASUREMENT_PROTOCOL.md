# Technical Protocol for Resource Measurement on Android Devices

This protocol establishes the scientific, rigorous, and reproducible method for collecting, measuring, and documenting hardware performance and resource consumption indicators (`kind: resource`) in the **Clean My Android** project.

> [!IMPORTANT]
> **Integrity Rule:** No quantitative metric for RAM, battery, temperature, or boot time may be inferred or entered into `metrics.json` without capturing and archiving the corresponding raw command dump in private storage, with sanitized evidence committed to the repository. Full raw dumps containing hardware serials or unredacted system logs must be retained privately, while sanitized outputs are published. Pending metrics must remain marked as `not_measured`.

---

## 1. Experimental Control Conditions

To significantly reduce environmental variation and confounding factors across runs (acknowledging that unmeasured background operating system tasks preclude absolute causal attribution), all comparative tests ("before" and "after") must follow identical baseline conditions:

| Parameter | Mandatory Controlled Condition | Technical Rationale |
| :--- | :--- | :--- |
| **Ambient temperature** | 22°C to 25°C in thermal equilibrium | Ambient temperature directly affects SoC thermal throttling and lithium battery chemical efficiency. |
| **Initial charge level** | 100% full charge with cable disconnected | Lithium-ion batteries exhibit non-linear discharge voltage curves across different charge stages. |
| **Connectivity** | Fixed Wi-Fi (same network / 5 GHz band) or Airplane Mode | Fluctuations in cellular signal strength (RSSI/RSRP) force the baseband modem to alter transmission power, skewing power draw. |
| **Display brightness** | Fixed at 50% (for active screen tests) or display off (for idle tests) | The OLED/IPS display panel is the largest single energy consumer on a mobile device. |
| **Settling period** | Exactly 5 minutes post-boot | Prevents capturing transient initialization spikes from system daemons and ART/JIT compilation. |
| **Sample repetitions** | Minimum $N \ge 3$ measurements per state | Enables calculating arithmetic mean and standard deviation, confirming statistical validity. |

---

## 2. Step-by-Step Collection Procedure

### 2.1 Idle RAM Footprint (`dumpsys meminfo`)

1. Cold reboot the smartphone:
   ```bash
   adb reboot
   ```
2. Wait for boot completion:
   ```bash
   adb wait-for-device
   adb shell 'while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done'
   ```
3. Allow the device to settle in thermal idle for 5 minutes (300 seconds).
4. Run 3 measurements separated by 60-second intervals, saving the raw output:
   ```bash
   # Measurement 1
   adb shell dumpsys meminfo > evidence/raw-meminfo-run1.txt
   sleep 60
   # Measurement 2
   adb shell dumpsys meminfo > evidence/raw-meminfo-run2.txt
   sleep 60
   # Measurement 3
   adb shell dumpsys meminfo > evidence/raw-meminfo-run3.txt
   ```
5. Extract consolidated metrics:
   - `Total RAM`
   - `Free RAM` (physical free RAM + kernel buffers)
   - `Used RAM` (total PSS of resident processes)
   - `Lost RAM`
6. Calculate the average across the 3 runs to populate the `before` and `after` fields in `metrics.json`.

---

### 2.2 System Boot Time

1. Record kernel and Android init timestamps:
   ```bash
   adb shell getprop ro.boottime.init
   adb shell getprop ro.boottime.init.cold_boot_done
   ```
2. Perform 3 cold reboot cycles timed from reboot initiation until the `sys.boot_completed=1` signal:
   ```bash
   START_MS=$(python3 -c 'import time; print(int(time.time() * 1000))')
   adb reboot && adb wait-for-device shell 'while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 0.5; done'
   END_MS=$(python3 -c 'import time; print(int(time.time() * 1000))')
   python3 -c "print(f'Boot time: {($END_MS - $START_MS) / 1000.0:.2f} s')"
   ```
3. Archive raw console timestamps and calculate the mean total boot duration in seconds across the 3 runs.

---

### 2.3 User Data Partition Storage (`df /data`)

1. Collect block allocation and free space:
   ```bash
   # Before intervention
   adb shell df -k /data > evidence/raw-df-before.txt
   # After intervention
   adb shell df -k /data > evidence/raw-df-after.txt
   ```
2. Compute the variation in gigabytes (GB):
   $$\Delta \text{Free} = \frac{\text{Available}_{\text{after}} - \text{Available}_{\text{before}}}{1024 \times 1024} \text{ GB}$$
3. Document clearly that this figure represents aggregate partition change across `/data` (including update rollbacks in `/data/app` and cache clearing), and individual package gains cannot be independently summed.

---

### 2.4 Standby Power Consumption and Thermal Behavior (24-Hour Idle Test)

1. Charge the device to 100% and disconnect the power source.
2. Reset battery usage statistics:
   ```bash
   adb shell dumpsys batterystats --reset
   ```
3. Capture initial battery level and temperature:
   ```bash
   adb shell dumpsys battery > evidence/raw-battery-initial.txt
   ```
   > [!NOTE]
   > AOSP `BatteryService` reports battery temperature in tenths of a degree Celsius ($0.1^\circ\text{C}$). For instance, a raw output of `temperature: 310` corresponds to $31.0^\circ\text{C}$ ($310 / 10 = 31.0$). When entering temperature values in documentation or JSON metrics, divide by 10 to record true degrees Celsius.

4. Place the device in screen-off standby for **24 continuous hours** under the controlled conditions in Section 1.
5. Repeat the 24-hour test for **at least 3 separate intervals** ($N \ge 3$) per state to compute arithmetic mean and sample standard deviation across runs.
6. After each 24-hour interval, reconnect via ADB and pull telemetry dumps:
   ```bash
   adb shell dumpsys battery > evidence/raw-battery-final-run1.txt
   adb shell dumpsys batterystats > evidence/raw-batterystats-24h-run1.txt
   ```
7. Compute the hourly idle discharge rate:
   $$\text{Standby Drain} = \frac{\text{Level}_{\text{initial}} - \text{Level}_{\text{final}}}{24} \text{ \%/hour}$$
8. Inspect Deep Sleep duration vs Partial Wake Locks to verify whether disabled background services were preventing kernel sleep states.

---

## 3. Canonical Formatting in `metrics.json`

Once testing is complete and raw outputs are saved in `evidence/`, populate the indicator in `metrics.json`:

```json
{
  "metrics": [
    {
      "indicator": "Consumo de Bateria e Comportamento Térmico Contínuo",
      "kind": "resource",
      "status": "measured",
      "before": "X%/h idle drain over 24h at 35°C",
      "after": "Y%/h idle drain over 24h at 31°C",
      "variation": "Observed reduction of Z%/h in standby drain",
      "method": "dumpsys batterystats and dumpsys battery in 24h controlled standby",
      "evidence": [
        "reports/<manufacturer>/<model>/evidence/raw-battery-initial.txt",
        "reports/<manufacturer>/<model>/evidence/raw-battery-final.txt",
        "reports/<manufacturer>/<model>/evidence/raw-batterystats-24h.txt"
      ],
      "limitations": "24h idle standby measurement in 23°C environment across 3 runs; does not reflect active screen usage."
    }
  ]
}
```
