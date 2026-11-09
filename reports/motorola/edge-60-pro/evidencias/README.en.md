# Evidence and Chain of Custody — Motorola Edge 60 Pro (XT2507-1)

This directory documents the data sources, forensic extraction commands, validation methods, and technical limitations of the debloating and optimization audit for the **Motorola Edge 60 Pro**.

---

> [!CAUTION]
> **Conflict with protected component list:** a subsequent review identified 18 packages present in both `pacotes-desativados.txt` and `data/protected_essential_packages.txt`. The intersection includes dialer and SMS components, emergency services, SIM Toolkit, Bluetooth, contacts, and system services.
>
> **November 09, 2026 Update:** The conflict involving package `com.android.vending` (Google Play Store) and associated integrity modules resulted in an empirical execution failure in government applications (Play Integrity API). The components were reactivated via ADB, resolving the issue. See the [Play Integrity Case Study](../case-study-play-integrity.en.md).

---

## 1. Data origin and provenance

The inventories and records in this audit were collected by running commands on the connected device through **Android Debug Bridge (ADB)** and the **Shizuku** layer.

- **Initial Execution Session:** November 6–7, 2026.
- **Validation and Remediation Session:** November 09, 2026.
- **Connection Mode:** Wireless debugging (Wireless ADB) using TLS pairing (temporary port and six-digit pairing PIN), followed by a connection to the device's main ADB TCP port.
- **Privilege Level:** `shell:1000` (non-root user; bootloader locked).

---

## 2. ADB commands and tools used

| Category | Base command | Purpose |
|---|---|---|
| **Model identification** | `adb devices -l`<br>`adb shell getprop ro.product.model` | Validate model (`motorola_edge_60_pro`), product (`cybert_g_sys`), and codename (`cybert`). |
| **System identification** | `adb shell getprop ro.build.version.release`<br>`adb shell getprop ro.build.fingerprint` | Canonical confirmation of Android 17 (SDK 37) and build `7a1c2-08c719`. |
| **Initial inventory** | `adb shell pm list packages -f`<br>`adb shell pm list packages -3`<br>`adb shell pm list packages -d` | Collect 501 installed packages with APK paths, 50 third-party packages, and 60 factory-disabled packages. |
| **Package inspection** | `adb shell dumpsys package packages` | Collect UIDs, system flags, declared package versions, granted permissions, and user states (User 0 / User 11). |
| **Memory telemetry** | `adb shell dumpsys meminfo` | Collect per-process RSS/PSS across multiple stages (initial, after basic debloating, after de-Googling, and final). |
| **Storage** | `adb shell df -h /data` | Check free space on `/data` before and after uninstall and cache-cleanup operations. |
| **AppOps sandboxing** | `adb shell cmd appops set --uid <UID> <OP> ignore` | Restrict GPS, Activity Recognition, and Body Sensors for Google Play Services (`UID 10387`) and services protected against disabling. |
| **Kernel/network policy** | `adb shell cmd netpolicy add restrict-background-blacklist <UID>` | Restrict background data traffic through Android's network policy for persistent bloatware. |
| **Surgical restoration** | `adb shell pm enable --user 0 <package>` | Re-enable integrity components (`com.android.vending`, `com.google.android.verifier`). |
| **Network validation** | `adb shell ping -c 1 <host>` | Test DNS resolution and verify telemetry-domain blocking through NextDNS. |

---

## 3. Supplemental Collection and Validation Completed (11/09/2026)

On November 09, 2026, with the device reconnected via Wireless ADB, canonical system properties previously flagged as pending were retrieved directly from `getprop`:

```bash
# Canonical confirmation of Android version, SDK, and ROM build:
adb shell getprop ro.build.version.release       # Output: 17
adb shell getprop ro.build.version.sdk           # Output: 37
adb shell getprop ro.build.version.incremental   # Output: 7a1c2-08c719
adb shell getprop ro.build.fingerprint           # Output: motorola/cybert_g_sys/cybert:17/A171VVH.36-27/7a1c2-08c719:user/release-keys
adb shell getprop ro.soc.model                   # Output: MT6897 (Dimensity 8300)
```

### Functional Validation of Play Integrity API:
- **Documented Incident:** Sanitized screenshot of the error dialog in `br.gov.serpro.cnhe` and `br.gov.meugovbr` archived at `01-erro-play-integrity-cnh-gov.jpg`.
- **Procedure and Resolution:** Reactivation of integrity packages via ADB with real-time runtime confirmation. See full documentation in the [Play Integrity Case Study](../case-study-play-integrity.en.md).

---

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

---

## 5. Generated files and integrity checks

- `inventario-antes.json`: 501 cataloged packages with vendor, physical path, UID, and preliminary role.
- `inventario-depois.json`: 501 packages with final consolidated state.
- `pacotes-desativados.txt`: Historical names of packages recorded in the `disabled-user` state.
- `pacotes-desinstalados.txt`: Record of the 9 packages uninstalled for user 0 and notes about reverting updates in `/data/app`.
- `permissoes-alteradas.json`: 13 runtime permission revocations, 2 documented special-permission attempts, 6 GMS AppOps changes (`UID 10387`), and 7 packages placed under network-policy restrictions.
- `comparativo.json`: Consolidated quantitative performance metrics and functional-test status.
- `01-erro-play-integrity-cnh-gov.jpg`: Sanitized screenshot capturing the Play Integrity failure dialog in government apps.
- `case-study-play-integrity.en.md`: Technical forensic case study detailing the incident, remediation, and functional validation.

The Portuguese source is available as [README.md](README.md).
