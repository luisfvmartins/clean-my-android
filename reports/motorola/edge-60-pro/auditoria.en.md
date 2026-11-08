# Motorola Edge 60 Pro — Technical Audit (English Summary)


> **Privacy note:** the 50 entries classified as third-party components have pseudonymized package identifiers. Installation-specific `/data/app` paths have been normalized. Aggregate inventory counts and recorded package states are preserved. The source inventory does not establish whether these components were user-installed or preloaded by a vendor.

**Model:** XT2507-1 · **Codename:** `cybert` · **Product:** `cybert_g_sys`  
**Interface:** Motorola Hello UI  
**Audit status:** **Pending validation**  
**Privilege level:** ADB shell (`shell:1000`), no root; bootloader locked.

> [!WARNING]
> This English document is a structured summary of the Portuguese technical audit, not a line-by-line translation of every operational detail. The Portuguese source remains authoritative for the complete historical record. All figures below are reproduced from that source and have not been independently re-measured by this translation.

> [!CAUTION]
> **Conflict with the protected-components list:** a post-audit review found 18 packages listed in both `pacotes-desativados.txt` and `data/protected_essential_packages.txt`. The overlap includes dialer and SMS, emergency, SIM Toolkit, Bluetooth, contacts, and system-support components.
>
> This does not confirm the device's current state or prove a functional failure, but it conflicts with the project's current safety guardrails. This is a historical record, not a recommendation. **Do not reuse this disable list on other devices.** The actual state must be checked on-device; any restoration requires individual assessment and in-person validation of calls, SMS, SIM, emergency, Bluetooth, and contacts.

---

## 1. Evidence and provenance

The audit consolidates operational records from November 6–7, 2026. Internal session identifiers and collection-environment details were omitted from the public report.

The device was connected using Wireless ADB with TLS pairing. The session used the non-root `shell:1000` privilege level.

Artifacts reviewed included:
- `pm list packages -f`: initial inventory of 501 software packages.
- `pm list packages -3`: 50 pre-existing third-party applications.
- `pm list packages -d`: 60 packages disabled by the factory image before intervention.
- `dumpsys package packages`: package versions, build codes, process UIDs, installers, permissions, and user states.
- `dumpsys meminfo`: per-process RSS/PSS observations across several stages.
- `df -h /data`: free storage before and after operations.
- Private DNS settings and NextDNS API interactions for domain blocking.

Raw dumps and operational history remain private.

## 2. Evidence classification

**Directly observed through ADB**
- Product identifiers: `model:motorola_edge_60_pro`, `device:cybert`, `product:cybert_g_sys`.
- CPU ABI: `arm64-v8a`.
- Initial inventory of 501 packages, including APK paths and UIDs.
- Per-process memory measurements across the cleanup stages.
- 244 packages disabled through `pm disable-user --user 0` (recorded at session step 701).
- Packages protected against disabling, returning `Failure: package is non-disable`.
- User states: User 0 active, User 10 removed, and User 11 stopped with `am stop-user -f 11`.
- DNS connectivity and resolution tests using ping.

**Partially or indirectly documented**
- Framework packages reported `versionName=17`, `versionCode=37`, and 377 packages with `targetSdk=37`. The canonical Android version was not confirmed using `getprop ro.build.version.release`.
- Free space on `/data` was reported as 193 GB initially and approximately 197 GB after operations. Per-application gains were not measured.
- Available RAM was reported as approximately 4.5 GB before and 7.2 GB after the session.
- Idle temperature was reported as 37–40°C initially and 33.0°C afterward.

**Not collected during the session**
- Canonical build properties: `ro.build.version.release`, `ro.build.version.sdk`, `ro.build.version.incremental`, and `ro.build.fingerprint`.
- Exact SoC from `/proc/cpuinfo` and GPU details from a graphics dump.
- Structured tests for voice calls, SMS, biometrics, and sensors.
- Real banking-app execution tests and a Play Integrity API result.
- IMEI, serial number, and MAC addresses (intentionally omitted for privacy).

## 3. Device identification

| Parameter | Recorded value | Collection status |
|---|---|---|
| Manufacturer | Motorola | Observed through ADB |
| Commercial model | Motorola Edge 60 Pro | Observed through ADB |
| Model code | `XT2507-1` | Commercial specification recorded in the project |
| Device codename | `cybert` | Observed through ADB |
| Product | `cybert_g_sys` | Observed through ADB |
| CPU architecture | 64-bit (`arm64-v8a`) | Observed in dumpsys |
| SoC / GPU | Dimensity-class platform / integrated GPU | Not collected through ADB in this session |
| Physical RAM | 12 GB | Reported; approximately 4.5 GB free before / 7.2 GB after |
| Internal storage | 256 GB | Reported; 193 GB free before / approximately 197 GB after |
| Android version | Framework indicators point to version 17 | Canonical confirmation pending |
| API level / target SDK | 377 packages with `targetSdk=37` | Canonical confirmation pending |
| Interface | Motorola Hello UI | Inferred from Motorola packages |
| Build / security patch | Stock Motorola build | Not collected through `getprop` |
| Root / bootloader | No root; locked bootloader | Observed through rejected root-level commands |
| SELinux | Enforcing | Observed through standard sandbox restrictions |
| Verified Boot | Active / enforcing | Inferred from the unmodified ROM state |
| Storage encryption | File-Based Encryption (FBE) | Platform default |
| Users | User 0 active; User 10 removed; User 11 stopped | Observed through ADB |
| Initial launcher | `com.motorola.launcher3` (Moto App Launcher / QuickStep) | Observed through dumpsys |
| Later launcher | `app.lawnchair.play` (Lawnchair 14); Moto Launcher retained for QuickStep gestures | Observed through dumpsys meminfo |
| Initial keyboard | Gboard (`com.google.android.inputmethod.latin`) | Observed through dumpsys meminfo |
| Later keyboard | FUTO Keyboard (`org.futo.inputmethod.latin`) | Observed through dumpsys meminfo |
| Initial dialer / SMS | Google Phone and Google Messages | Observed through package data |
| Later dialer / SMS | Fossify Phone and Fossify Messages | Observed through package data |
| Connectivity | Wi-Fi, Bluetooth, NFC, dual-SIM 5G NR | Observed in the system connectivity stack |

## 4. Initial package inventory

The initial inspection (`adb shell pm list packages -f`, session step 73) reported **501 installed software packages**.

| Component category | Count | Examples |
|---|---:|---|
| Motorola Mobility / Lenovo | 161 | `com.motorola.launcher3`, `com.motorola.camera5`, `com.motorola.ccc`, `com.lenovo.qiracore` |
| Google Mobile Services and apps | 108 | `com.google.android.gms`, `com.google.android.googlequicksearchbox`, `com.android.vending` |
| AOSP / base system | 102 | `android`, `com.android.systemui`, `com.android.keychain`, `com.android.settings` |
| AOSP framework overlays | 59 | Cutout, system color, and layout overlays |
| Third-party user applications | 50 | Social, utility, and banking apps |
| Adware, bloatware, and OOBE partners | 11 | Digital Turbine, Aura, Glance, Taboola, InMobi |
| Foreign carriers and partners | 10 | Carrier overlays and stubs |
| **Total** | **501** | Recorded in `inventario-antes.json` |

Reported partition distribution:
- `/product`: 206 packages.
- `/data`: 102 packages.
- `/system`: 71 packages.
- `/system_ext`: 69 packages.
- `/apex`: 34 Project Mainline modules.
- `/vendor`: 19 packages.

See [the initial inventory](inventario-antes.json) for package-level records.

## 5. Recorded changes

### 5.1 User-level disabling

A total of **244 packages** were disabled for User 0 using `pm disable-user --user 0`, placing them in the `enabled=3` (`DISABLED_USER`) state. This does not physically remove the APK from read-only system partitions.

The source report groups the disabled packages into:
- Commercial adware, sponsored installers, and embedded advertising (Digital Turbine, IronSource Aura, Glance, Taboola, InMobi, Meta services, and partner stores).
- Motorola/Lenovo diagnostics and telemetry (Customer Care Central notifications, MotoCare, external logs, Bug2Go, lifecycle/modem statistics, Smart Feed, Qira, Smart Connect/Ready For, and gesture services).
- De-Googling changes requested by the device owner, including replacement of Chrome, Google Phone, and Google Messages with Brave and Fossify alternatives; other Google apps and services were disabled.

The full list is in [pacotes-desativados.txt](pacotes-desativados.txt). These historical records are not a reusable package-removal recipe.

### 5.2 Uninstallation for User 0

The report records **9 packages uninstalled for User 0**:
- Two third-party applications located under `/data/app`, reported as DT Ignite-installed adware.
- Seven preinstalled packages, including sponsored games, Airbnb, ExpressWeather, Motorola Genie, and the YouTube Music subscription manager.

For system packages, `pm uninstall -k --user 0` changes the package state for that user; it does not physically delete the factory APK from `/system` or `/product`.

### 5.3 Reverting application updates and storage measurement

Updates stored under `/data/app` were reverted for ten selected system packages. The report records free space increasing from 193 GB to approximately 197 GB after the combined set of update removals, adware uninstalls, and data/cache clearing.

**The approximately 4 GB gain was measured only as an aggregate partition change, not per application.** It must not be attributed to each package individually. The read-only `/system` image was not physically purged.

### 5.4 Firmware-protected packages and AppOps

For packages returning `Failure: package is non-disable`, the session applied selected AppOps restrictions by UID and Android background network restrictions through `netpolicy`. The source report lists PayJoy, Amazon AppManager, Motorola device management, PAKS notifications, Moto Installer, Google SDK Sandbox, and Motorola OTA among the affected services.

UID-level AppOps may affect every package sharing that UID. The recorded settings must not be copied to another device or reapplied without checking UID membership, dependencies, and side effects.

### 5.5 Google Play Services restrictions

Google Play Services (`com.google.android.gms`, UID 10387) was not uninstalled or disabled. The report records AppOps set to `ignore` for:
- `FINE_LOCATION`
- `COARSE_LOCATION`
- `MONITOR_LOCATION`
- `MONITOR_HIGH_POWER_LOCATION`
- `ACTIVITY_RECOGNITION`
- `BODY_SENSORS`

Because these settings were applied at UID level, they may affect all processes/packages sharing UID 10387. Apps relying exclusively on the GMS Fused Location Provider may be affected.

### 5.6 Permission changes

The source report records 13 runtime permission revocations, involving Motorola Camera, Motorola SIM settings, Google external services, Companion Device Manager, Google eUICC, Uber, 99, Minha Unifique, Brave, and another user app.

It also records attempts to revoke `android.permission.ACCESS_LOCAL_NETWORK` from five applications. A later `dumpsys package` inspection still showed `granted=true`; the standard `pm revoke` command did not revoke this special permission.

See [permissoes-alteradas.json](permissoes-alteradas.json) for the structured record.

### 5.7 Secondary user profiles

The session identified User 11 running a second Google Play Services instance (PID 25050, reported at 269 MB RSS). The recorded commands were:
- `adb shell am stop-user -f 11`
- `adb shell pm remove-user 10`

The report attributes 269 MB of RAM release and removal of duplicate background processes to these operations. Profile removal can delete profile data and must never be treated as a routine cleanup step.

### 5.8 DNS-level blocking through NextDNS

The report records Private DNS configured in `hostname` mode with a redacted NextDNS endpoint. A denylist included Motorola telemetry, Check-in, Blur, PayJoy, Digital Turbine, InMobi, Glance, and Taboola domains.

The session tested:
- `ping -c 1 telemetry.motorola.com`: reported blocked / unreachable.
- `ping -c 1 1.1.1.1`: reported operational.

A ping result alone does not prove that all telemetry is blocked or that an application has no alternate endpoints.

## 6. Final package state and preserved components

The report records:
- 248 packages preserved.
- 244 packages disabled for User 0.
- 9 packages uninstalled for User 0.
- 10 system-app updates reverted.
- 7 firmware-protected bloatware packages restricted through AppOps/network policy.
- Secondary user profiles stopped or removed.

Components specifically identified as preserved include:
- `android` and `com.android.systemui`.
- `com.motorola.launcher3`, retained for QuickStep navigation gestures after Lawnchair installation.
- `com.android.rkpdapp`, for KeyMint/StrongBox hardware attestation.
- `com.android.settings.intelligence`, for Settings search.
- `com.dolby.daxservice`, for audio processing.
- Core telephony, IMS, and TelephonyProvider components.

The detailed final state is recorded in [inventario-depois.json](inventario-depois.json).

## 7. Before/after metrics reported by the source

| Metric | Before | After | Reported difference | Evidence reference |
|---|---:|---:|---:|---|
| Available RAM | ~4.5 GB | ~7.2 GB | +2.7 GB (+58.7%) | `dumpsys meminfo`, steps 110 and 384 |
| RAM in use | ~7.5 GB | ~4.8 GB | -2.7 GB | Same measurements |
| Free `/data` storage | 193 GB | ~197 GB | ~4 GB aggregate | `df -h /data`, step 398 |
| Installed package count | 501 | 492 | -9 for User 0 | `pm list packages -f` |
| Enabled / preserved packages | 441 | 248 | -193 (184 disabled + 9 uninstalled for user 0) | `inventario-depois.json` (248 preserved/active, 244 disabled, 9 uninstalled) |
| Disabled packages | 60 factory-disabled | 244 | +184 | `pm list packages -d`, steps 89 and 701 |
| Google QuickSearchBox RAM | 873 MB RSS | 0 MB reported | -873 MB | `dumpsys meminfo` |
| Secondary profile processes | User 0 + User 11 | User 0 only | -269 MB RSS | `am stop-user -f 11` |
| Idle temperature | 37–40°C | 33.0°C | -4 to -7°C observed | `dumpsys battery`, step 384 |

> **Reconciliation note:** an earlier operational summary recorded 257 enabled packages. This does not match the 248 packages classified as preserved/active in the final inventory. Because the raw command output is not publicly available for review, 257 is not treated as confirmed; the comparison uses the structured inventory classification.

These are historical measurements from the source report, not independently replicated tests. Memory and temperature vary with workload, uptime, ambient conditions, and measurement timing. They do not establish sustained performance or battery-life gains.

See [comparativo.json](comparativo.json) for the structured comparison.

## 8. Functional validation status

| Feature | Status | Evidence / limitation |
|---|---|---|
| Wi-Fi | Passed during session | Wireless ADB remained connected without recorded disconnects |
| Audio / equalization | Passed during session | Wavelet received the special `DUMP` permission through `pm grant` |
| DNS / NextDNS | Passed for the recorded checks | DNS resolution and a telemetry-domain ping test were recorded |
| Camera | Passed during session | Motorola Camera opened; coarse location permission was revoked |
| Navigation gestures | Passed during session | Moto Launcher / QuickStep was retained |
| Voice calls | Pending | No call test logged |
| SMS send/receive | Pending | No SMS test logged |
| 4G/5G mobile data | Pending | Session used Wi-Fi; mobile data was not logged as tested |
| VoLTE / VoWiFi | Pending | Not functionally tested |
| Bluetooth | Pending | Peripheral pairing not tested |
| GPS / navigation accuracy | Pending | No navigation-accuracy test logged |
| Biometrics | Pending | No biometric unlock test logged |
| Push notifications (FCM) | Pending | Practical delivery not audited |
| Banking applications / Pix | Pending | No banking app was opened or tested |
| Play Integrity / certification | Pending | No API attestation result collected |
| System OTA updates | Intentionally paused | `com.motorola.ccc.ota` was paused in the recorded session |

## 9. Security and privacy interpretation

The source report describes disabling selected sponsored installers and ad-supported services, restricting background activity for firmware-protected packages, applying UID-level AppOps restrictions to Google Play Services, and revoking selected runtime permissions.

These observations must be interpreted carefully:
- A permission, SDK, persistent flag, or installed package does not by itself prove data exfiltration.
- DNS blocking tests do not establish that every telemetry endpoint is blocked.
- UID-level AppOps can affect unrelated packages sharing the same UID.
- Disabling or restricting components can break functionality.
- Historical actions are not recommendations for other devices or firmware.

## 10. Limitations and follow-up collection

The device owner should collect the following properties to confirm the Android version and build:

```bash
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.incremental
adb shell getprop ro.build.fingerprint
adb shell cat /proc/cpuinfo
adb shell dumpsys SurfaceFlinger | grep -i "GLES"
```

Play Integrity should be checked separately with an appropriate checker and documented result. Voice calls, SMS, mobile data, VoLTE/VoWiFi, Bluetooth, GPS, biometrics, push notifications, banking apps, and Pix must be tested by the device owner before the audit status can be changed.

The source report recommends rerunning debloating scripts after OTA updates. **Do not interpret that historical recommendation as blanket authorization to rerun a script.** Any post-update action requires a fresh inventory, compatibility review, a device-specific plan, and explicit authorization.

## 11. Final status

**Audit classification: PENDING VALIDATION.**

The package reconciliation and action history are documented from ADB evidence. However, canonical Android build properties and functional logs for calls, biometrics, and banking apps were not collected during the session. The audit must remain pending until the device owner completes the missing in-person tests.

## Source files

- [Original full technical report (Portuguese)](auditoria.md)
- [Evidence provenance and collection guide (English)](evidencias/README.en.md)
- [Initial inventory](inventario-antes.json)
- [Final inventory](inventario-depois.json)
- [Disabled packages](pacotes-desativados.txt)
- [Uninstalled packages](pacotes-desinstalados.txt)
- [Permission and AppOps changes](permissoes-alteradas.json)
- [Before/after comparison](comparativo.json)

**This report is not a script approval or a universal debloating procedure.**
 Memory and temperature vary with workload, uptime, ambient conditions, and measurement timing. They do not establish sustained performance or battery-life gains.

See [comparativo.json](comparativo.json) for the structured comparison.

## 8. Functional validation status

| Feature | Status | Evidence / limitation |
|---|---|---|
| Wi-Fi | Passed during session | Wireless ADB remained connected without recorded disconnects |
| Audio / equalization | Passed during session | Wavelet received the special `DUMP` permission through `pm grant` |
| DNS / NextDNS | Passed for the recorded checks | DNS resolution and a telemetry-domain ping test were recorded |
| Camera | Passed during session | Motorola Camera opened; coarse location permission was revoked |
| Navigation gestures | Passed during session | Moto Launcher / QuickStep was retained |
| Voice calls | Pending | No call test logged |
| SMS send/receive | Pending | No SMS test logged |
| 4G/5G mobile data | Pending | Session used Wi-Fi; mobile data was not logged as tested |
| VoLTE / VoWiFi | Pending | Not functionally tested |
| Bluetooth | Pending | Peripheral pairing not tested |
| GPS / navigation accuracy | Pending | No navigation-accuracy test logged |
| Biometrics | Pending | No biometric unlock test logged |
| Push notifications (FCM) | Pending | Practical delivery not audited |
| Banking applications / Pix | Pending | No banking app was opened or tested |
| Play Integrity / certification | Pending | No API attestation result collected |
| System OTA updates | Intentionally paused | `com.motorola.ccc.ota` was paused in the recorded session |

## 9. Security and privacy interpretation

The source report describes disabling selected sponsored installers and ad-supported services, restricting background activity for firmware-protected packages, applying UID-level AppOps restrictions to Google Play Services, and revoking selected runtime permissions.

These observations must be interpreted carefully:
- A permission, SDK, persistent flag, or installed package does not by itself prove data exfiltration.
- DNS blocking tests do not establish that every telemetry endpoint is blocked.
- UID-level AppOps can affect unrelated packages sharing the same UID.
- Disabling or restricting components can break functionality.
- Historical actions are not recommendations for other devices or firmware.

## 10. Limitations and follow-up collection

The device owner should collect the following properties to confirm the Android version and build:

```bash
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.incremental
adb shell getprop ro.build.fingerprint
adb shell cat /proc/cpuinfo
adb shell dumpsys SurfaceFlinger | grep -i "GLES"
```

Play Integrity should be checked separately with an appropriate checker and documented result. Voice calls, SMS, mobile data, VoLTE/VoWiFi, Bluetooth, GPS, biometrics, push notifications, banking apps, and Pix must be tested by the device owner before the audit status can be changed.

The source report recommends rerunning debloating scripts after OTA updates. **Do not interpret that historical recommendation as blanket authorization to rerun a script.** Any post-update action requires a fresh inventory, compatibility review, a device-specific plan, and explicit authorization.

## 11. Final status

**Audit classification: PENDING VALIDATION.**

The package reconciliation and action history are documented from ADB evidence. However, canonical Android build properties and functional logs for calls, biometrics, and banking apps were not collected during the session. The audit must remain pending until the device owner completes the missing in-person tests.

## Source files

- [Original full technical report (Portuguese)](auditoria.md)
- [Evidence provenance and collection guide (English)](evidencias/README.en.md)
- [Initial inventory](inventario-antes.json)
- [Final inventory](inventario-depois.json)
- [Disabled packages](pacotes-desativados.txt)
- [Uninstalled packages](pacotes-desinstalados.txt)
- [Permission and AppOps changes](permissoes-alteradas.json)
- [Before/after comparison](comparativo.json)

**This report is not a script approval or a universal debloating procedure.**
