# Evidence and Chain of Custody — Motorola Edge 60 Pro (XT2507-1)

This directory documents the data sources, forensic extraction commands, validation methods, and technical limitations of the debloating and optimization audit for the **Motorola Edge 60 Pro**.

## 1. Data origin and provenance

The inventories and records in this audit were collected by running commands on the connected device through **Android Debug Bridge (ADB)** and the **Shizuku** layer.

- **Execution session:** Forensic audit history recorded in the technical assistant's local database.
- **Connection mode:** Wireless debugging (Wireless ADB) using TLS pairing (temporary port and six-digit pairing PIN), followed by a connection to the device's main ADB TCP port.
- **Privilege level:** `shell:1000` (non-root user; bootloader locked).
- **Audit dates:** November 6–7, 2026.

## 2. ADB commands and tools used

| Category | Base command | Purpose |
|---|---|---|
| **Model identification** | `adb devices -l`<br>`adb shell getprop ro.product.model` | Validate model (`motorola_edge_60_pro`), product (`cybert_g_sys`), and codename (`cybert`). |
| **Initial inventory** | `adb shell pm list packages -f`<br>`adb shell pm list packages -3`<br>`adb shell pm list packages -d` | Collect 501 installed packages with APK paths, 50 third-party packages, and 60 factory-disabled packages. |
| **Package inspection** | `adb shell dumpsys package packages` | Collect UIDs, system flags, declared package versions, granted permissions, and user states (User 0 / User 11). |
| **Memory telemetry** | `adb shell dumpsys meminfo` | Collect per-process RSS/PSS across multiple stages (initial, after basic debloating, after de-Googling, and final). |
| **Storage** | `adb shell df -h /data` | Check free space on `/data` before and after uninstall and cache-cleanup operations. |
| **AppOps sandboxing** | `adb shell cmd appops set --uid <UID> <OP> ignore` | Restrict GPS, Activity Recognition, and Body Sensors for Google Play Services (`UID 10387`) and services protected against disabling. |
| **Kernel/network policy** | `adb shell cmd netpolicy add restrict-background-blacklist <UID>` | Restrict background data traffic through Android's network policy for persistent bloatware. |
| **Network validation** | `adb shell ping -c 1 <host>` | Test DNS resolution and verify telemetry-domain blocking through NextDNS. |

## 3. Pending supplemental collection (device-owner actions)

Some canonical system properties were not collected through `getprop` during the debloating session. To close these gaps without assumptions or estimates, the device owner should run the following commands when convenient:

```bash
# Canonical Android version, SDK, and ROM build:
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.incremental
adb shell getprop ro.build.fingerprint

# Hardware details (SoC and GPU):
adb shell cat /proc/cpuinfo
adb shell dumpsys SurfaceFlinger | grep -i "GLES"

# Play Integrity attestation:
# Run a suitable Play Integrity API checker from the Play Store,
# or review device certification under Settings > Google > All services > Play Protect.
```

> [!NOTE]
> Until these commands are run and their outputs documented, the operating-system version remains **pending confirmation**, and functional tests remain **not collected during the session**.

## 4. Strict privacy and sanitization policy

In accordance with the **Clean My Android** project security and privacy guidelines, published evidence has been sanitized:

1. **Personal and hardware identifiers**
   - IMEI, MEID, and serial numbers were omitted.
   - Wi-Fi and Bluetooth MAC addresses were omitted.
   - Phone numbers and SIM identifiers (ICCID) were neither collected nor published.
2. **Accounts and credentials**
   - API tokens (including NextDNS profile keys) were replaced with neutral placeholders (`YOUR_API_KEY`, `YOUR_ID`).
   - Google accounts, email addresses, and synchronized credentials were omitted.
3. **Network and routing**
   - Dynamic local IP addresses were represented using the RFC 1918 convention (`192.168.1.X`) to protect the owner's network topology.
4. **Raw data storage**
   - The complete raw package dump (`dumpsys_full.txt`) and operational history files remain restricted to the technical operator's local environment to protect the device owner's data.

## 5. Generated files and integrity checks

- `inventario-antes.json`: 501 cataloged packages with vendor, physical path, UID, and preliminary role.
- `inventario-depois.json`: 501 packages with final state (248 preserved, 244 disabled, 9 uninstalled for user 0).
- `pacotes-desativados.txt`: Names of the 244 packages recorded in the `disabled-user` state.
- `pacotes-desinstalados.txt`: Record of the 9 packages uninstalled for user 0 and notes about reverting updates in `/data/app`.
- `permissoes-alteradas.json`: 13 runtime permission revocations, 2 documented special-permission attempts, 6 GMS AppOps changes (`UID 10387`), and 7 packages placed under network-policy restrictions.
- `metrics.json`: Consolidated quantitative performance metrics and functional-test status.

The Portuguese source is available as [README.md](README.md).
