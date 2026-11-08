# Evidence and Data Provenance — Motorola Edge 60 Pro (XT2507-1)

This directory documents data sources, forensic extraction commands, validation methods, and technical limitations of the Motorola Edge 60 Pro debloating and optimization audit.

## 1. Data origin and provenance

The inventories and records in this audit were collected by running commands on the connected device through **Android Debug Bridge (ADB)** and the **Shizuku** layer.

- **Execution session:** forensic audit history recorded in the technical assistant's local database.
- **Connection mode:** Wireless debugging through TLS pairing (temporary port and six-digit PIN), followed by connection to the device's main TCP port.
- **Privilege level:** `shell:1000` (non-root user; locked bootloader).
- **Audit dates:** November 6–7, 2026.

## 2. ADB commands and tools

| Category | Base command | Purpose |
|---|---|---|
| Model identification | `adb devices -l`; `adb shell getprop ro.product.model` | Validate model (`motorola_edge_60_pro`), product (`cybert_g_sys`), and codename (`cybert`). |
| Initial inventory | `adb shell pm list packages -f`; `adb shell pm list packages -3`; `adb shell pm list packages -d` | Collect installed packages, APK paths, third-party packages, and factory-disabled packages. |
| Package inspection | `adb shell dumpsys package packages` | Collect UIDs, system flags, package versions, granted permissions, and user states. |
| Memory telemetry | `adb shell dumpsys meminfo` | Collect per-process RSS/PSS at multiple stages. |
| Storage | `adb shell df -h /data` | Check free space on `/data` before and after uninstall/cache operations. |
| AppOps sandboxing | `adb shell cmd appops set --uid <UID> <OP> ignore` | Change selected location, activity-recognition, and body-sensor operations. |
| Kernel/network policy | `adb shell cmd netpolicy add restrict-background-blacklist <UID>` | Restrict background data for selected UIDs. |
| Network validation | `adb shell ping -c 1 <host>` | Test DNS resolution and domain blocking through NextDNS. |

## 3. Pending supplemental collection

Some canonical system properties were not collected through `getprop` during the debloating session. To avoid assumptions, the device owner should run these commands later:

```bash
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.incremental
adb shell getprop ro.build.fingerprint
adb shell cat /proc/cpuinfo
adb shell dumpsys SurfaceFlinger | grep -i "GLES"
```

Play Integrity should be checked separately with a suitable checker application or the relevant device certification settings.

Until the commands and outputs are recorded, the operating system version remains **pending confirmation** and functional tests remain **not collected during the session**.

## 4. Privacy and sanitization

The public evidence is intended to omit:
- IMEI, MEID, serial numbers, and Wi-Fi/Bluetooth MAC addresses.
- Phone numbers and SIM identifiers.
- API tokens, NextDNS profile keys, Google accounts, email addresses, and credentials.
- Exact local network details that could expose the owner's network topology.
- Raw package dumps and operational history that remain in the operator's local environment.

Review every file before publication. Do not assume that replacing a few identifiers makes a complete raw dump safe to publish.

## 5. Generated files

- `inventario-antes.json`: initial package inventory.
- `inventario-depois.json`: final package states.
- `pacotes-desativados.txt`: packages recorded as disabled for user 0.
- `pacotes-desinstalados.txt`: packages uninstalled for user 0 and update rollback notes.
- `permissoes-alteradas.json`: runtime permission, AppOps, and network-policy changes.
- `comparativo.json`: quantitative metrics and functional test status.

The original Portuguese evidence README remains available as [README.md](README.md).
