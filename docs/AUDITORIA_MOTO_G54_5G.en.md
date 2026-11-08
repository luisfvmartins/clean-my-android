# Motorola Moto G54 5G — Technical Audit (English Summary)

**Device:** XT2343-1 · cancunf · Android 15 · Hello UI  
**Collection scope:** 462 components recorded locally (423 APK/static-library/RRO overlay packages and 39 APEX modules).  
**Public inventory:** 394 system/manufacturer components. The 29 user-installed applications and their details are intentionally omitted.  
**Collection mode:** The audit collection described here was read-only. Earlier operations are retrospective history, not instructions or authorization to repeat them.

> [!IMPORTANT]
> This is an English structured summary, not a line-by-line translation of every package entry. The Portuguese report and seven batch files remain the detailed source records. No new device measurements or validation were performed for this English document.

## 1. Executive summary

The inspection found a device with a substantial history of prior ADB debloating. A previous script had disabled 162 packages (130 system apps/services and 32 RRO overlays) through ADB; another 10 applications had been disabled through Android Settings.

Previously disabled advertising and partner packages included Meta services, InMobi Glance, Taboola, Digital Turbine, ironSource Aura, PayJoy, Amazon AppManager, Motorola Analytics, MotoCare, Bug2Go, and Android advertising/personalization modules.

The audit also identified disabled components that the source report considers essential or functionally important:

- **com.android.rkpdapp:** Remote Key Provisioning for KeyMint/StrongBox hardware attestation. The report warns that cached-key expiration could affect Play Integrity and dependent applications. This is a risk assessment, not evidence that a failure has already occurred.
- **com.android.companiondevicemanager:** AOSP companion-device service associated with Passkeys/FIDO2 flows and device pairing.
- **com.android.settings.intelligence:** Local Settings search indexer; the report says it does not declare INTERNET.
- **com.dolby.daxservice and com.motorola.dolby.dolbyui:** Dolby audio processing and user interface. The report observed the persistent service still running despite its disabled-user state, while audio features were reported degraded.
- **com.android.printspooler:** Android printing and Save as PDF.
- **com.android.providers.contactkeys:** Android 15 local E2EE contact-key provider.
- **com.android.providers.userdictionary:** Local personal dictionary.
- **com.motorola.nfwlocationattribution:** Privacy Dashboard attribution for low-level location access.

Persistent services reportedly remained active while their packages were marked disabled:

- **com.motorola.android.nativedropboxagent:** Reported running as PID 30253, UID 1007, using approximately 4.2 MB PSS and associated with native crash reporting.
- **com.motorola.bach.modemstats:** Four services remained registered with ActivityManager: ModemStatsService, LinkLatencyService, SmartNotificationService, and ModemFilterService.

Enabled manufacturer services requiring individual review included:

- **com.motorola.ccc.devicemanagement:** Three services were recorded, including BlurServiceMother and CheckinService. The report lists privileged permissions such as READ_LOGS, READ_DROPBOX_DATA, READ_NOTIFICATIONS, PACKAGE_USAGE_STATS, READ_PRIVILEGED_PHONE_STATE, and INTERNET.
- **com.motorola.installer:** Moto Installer, enabled with INSTALL_PACKAGES, READ_PRIVILEGED_PHONE_STATE, QUERY_ALL_PACKAGES, and INTERNET.
- **com.bluetooth.aptxmode:** The source identifies MotoBtMetricsService running with FLAG_PERSISTENT and permissions associated with Motorola Checkin. The public report does not provide packet-level proof of data transmission.
- **com.motorola.paks.notification:** Enabled Direct Boot notification trigger associated in the source with PAKS.
- **com.motorola.IncrementalUpdater:** Enabled 3c_ota service with READ_LOGS and READ_PRIVILEGED_PHONE_STATE.

**Interpretation caution:** A permission, active service, persistent flag, or network connection does not by itself prove improper data collection or establish that disabling a package is safe. Validate each finding independently.

## 2. Device identification

| Parameter | Recorded value |
|---|---|
| Manufacturer | Motorola |
| Commercial model | moto g54 5G / XT2343-1 |
| Device / board codename | cancunf |
| Product | cancunf_g_sysn |
| Distribution channel | retbr (Brazil retail) |
| SoC | MediaTek Dimensity 7020 (MT6855), arm64-v8a, 8 cores |
| Android version | Android 15, API level 35 |
| Build | V1TDS35H.83-20-5-8-2-1-3 |
| Security patch | 2026-09-01 |
| ROM | Official Motorola stock ROM, user build, release-keys |
| Root / bootloader | Not rooted; bootloader locked; Verified Boot green; dm-verity enforcing; SELinux enforcing |
| Encryption | File-Based Encryption (FBE), encrypted |
| Android users | One user, User 0 |
| Connectivity | LTE/5G reported active |
| Default launcher | com.motorola.launcher3 (Moto App Launcher / QuickStep) |
| Default keyboard | Gboard; Google Voice Typing enabled |
| Default dialer / SMS | Google Phone / Google Messages |
| Default browser / gallery | Chrome / Google Photos |
| RAM | 8 GB |
| Internal storage | 231 GB total; approximately 198 GB used and 32 GB free at collection time |

The original report includes additional build properties, fingerprint, carrier/network details, and memory measurements. Network identifiers and sensitive values were omitted from this public summary.

## 3. Inventory statistics

| Metric | Count | Notes |
|---|---:|---|
| Total audited components | 462 | 423 APK/static-library packages + 39 APEX modules |
| System components | 394 | 267 functional system packages + 127 RRO overlays |
| User-installed applications | 29 | Excluded from public package-level inventory |
| Enabled packages | 203 | 131 system/user packages + 72 active RRO overlays |
| Disabled packages | 220 | 162 disabled through ADB, 10 through Settings, 47 by Motorola regional script, and 1 disabled-until-used |
| Active APEX modules | 39 | 37 AOSP/Google Mainline + 2 Motorola modules |
| Shared UID groups | 7 | System, phone, Bluetooth, NFC, Network Stack, Motorola CCS, and Google shared identities |

### Risk classification recorded by the source

- Critical: 10 packages
- High: 38 packages
- Medium: 54 packages
- Low: 112 packages
- Informational: 248 components

Per-application storage, cache, and usage measurements were omitted to protect the owner's privacy.

## 4. Detailed inventory batches

The individual analysis is divided into seven documents. Original numbering is preserved:

| Batch | Scope | Items | Detailed document |
|---|---|---:|---|
| 2 | Google ecosystem, GMS, Mainline APKs, proprietary services | 30–111 (82) | [Batch 2 — Portuguese source](auditorias/moto-g54/lote-02-ecossistema-google.md) |
| 3 | Motorola and Lenovo | 112–199 (88) | [Batch 3 — Portuguese source](auditorias/moto-g54/lote-03-motorola-lenovo.md) |
| 4 | Commercial partners, carriers, hardware | 200–224 (25) | [Batch 4 — Portuguese source](auditorias/moto-g54/lote-04-parceiros-comerciais-e-hardware.md) |
| 5 | Android AOSP base system | 225–296 (72) | [Batch 5 — Portuguese source](auditorias/moto-g54/lote-05-sistema-base-aosp.md) |
| 6 | AOSP, Google Mainline, MediaTek RRO overlays | 297–358 (62) | [Batch 6 — Portuguese source](auditorias/moto-g54/lote-06-overlays-aosp-google-mediatek.md) |
| 7 | Motorola overlays, regional carriers, eUICC/eSIM | 359–423 (65) | [Batch 7 — Portuguese source](auditorias/moto-g54/lote-07-overlays-motorola-operadoras-esim.md) |
| 8 | Project Mainline and APEX system modules | 424–462 (39) | [Batch 8 — Portuguese source](auditorias/moto-g54/lote-08-modulos-project-mainline-apex.md) |

Batch 1 contained the 29 user-installed applications. Their names, package names, versions, permissions, sizes, and usage data remain excluded from the public repository.

## 5. Packages highlighted for individual review

| Package(s) | Partner / function | Recorded state |
|---|---|---|
| com.facebook.appmanager, com.facebook.services, com.facebook.system | Meta services | Disabled |
| com.dti.motorola | Digital Turbine Ignite | Disabled |
| com.dti.amx | Claro / América Móvil | Disabled |
| com.aura.oobe.motorola | ironSource Aura / Unity | Disabled |
| com.glance.lockscreenM | InMobi Glance | Disabled |
| com.taboola.mip | Taboola News/Ads | Disabled |
| com.payjoy.access | PayJoy | Disabled |
| com.amazon.appmanager | Amazon AppManager | Disabled |
| com.claroColombia.contenedor, com.orange.aura.oobe, com.orange.update, de.telekom.tsc | Foreign carrier stubs | Disabled |
| com.motorola.ccc.devicemanagement | Motorola device management / Checkin | Enabled |
| com.motorola.installer | Moto Installer | Enabled |
| com.bluetooth.aptxmode | Motorola Bluetooth metrics service | Enabled |
| com.motorola.android.nativedropboxagent | Native crash reporting agent | Disabled state, process reported running |
| com.motorola.bach.modemstats | Modem statistics services | Disabled state, services reported registered |
| com.motorola.paks.notification | PAKS notification trigger | Enabled |
| com.motorola.IncrementalUpdater | Motorola incremental updater | Enabled |

These are observations and interpretations from one device collection. They are not a universal package-removal list.

## 6. Essential components and compatibility

The source report identifies the following groups as requiring preservation and functional validation:

- **Android core and UI:** android, com.android.systemui, com.android.settings, Settings providers, shell, external storage, DocumentsUI, PermissionController, and Package Installer.
- **Security and cryptography:** com.android.keychain, com.trustonic.teeservice, com.android.rkpdapp, com.google.android.conscrypt, and com.android.se.
- **Telephony and networking:** com.android.phone, Telecom, telephony providers, MMS service, MediaTek IMS/telephony services, Network Stack, tethering, and captive portal login.
- **Local connectivity:** com.android.bluetooth and com.android.nfc.
- **Launcher integration:** com.motorola.launcher3 is retained in the source report because of its QuickStep / Recents integration.
- **Google-dependent functions:** Google Play services, Google Services Framework, and Play Store may be required by apps relying on Play Integrity, FIDO2, or Firebase Cloud Messaging. Test each banking, government, and messaging application on the actual device.

Nine components were reported as accidentally disabled in the earlier cleanup: com.android.rkpdapp, com.android.companiondevicemanager, com.android.settings.intelligence, com.dolby.daxservice, com.motorola.dolby.dolbyui, com.android.printspooler, com.android.providers.contactkeys, com.android.providers.userdictionary, and com.motorola.nfwlocationattribution.

## 7. Network, permissions, and privacy

The local collection observed DNS-over-TLS, push-notification services, and HTTPS connections to platform services. Public network identifiers and IP/port details were omitted.

An INTERNET permission or active connection does not establish improper collection. Telemetry attribution requires correlation among process, destination, domain, connection time, and ideally traffic inspection.

Do not apply AppOps by UID without mapping every package that shares that UID. UID-level restrictions may affect unrelated system components.

## 8. Safe validation and rollback

1. Confirm model, codename, Android version, build, and active user.
2. Validate telephony/RIL/IMS, KeyMint/KeyStore, Passkeys, audio, Bluetooth, Wi-Fi, launcher, and package installer.
3. Gather evidence for suspect packages; do not infer telemetry solely from permissions or flags.
4. Propose one change at a time, including rationale, risk, functional test, and rollback command.
5. Do not use pm clear, bulk cache clearing, or profile/user removal as routine cleanup.
6. Do not uninstall persistent services based only on FLAG_PERSISTENT.
7. After any authorized change, test calls, SMS, mobile data, Wi-Fi, Bluetooth, notifications, banking apps, authentication, keyboard, and launcher.
8. To re-enable a confirmed disabled package, the source documents pm enable --user 0 package.name. This does not recover data deleted by pm clear or restore packages removed for a user.

## 9. Compatibility and privacy-hardening notes

- **Banking, Pix, and government apps:** The source report identifies Google Play services, Google Services Framework, Play Store, Trustonic TEE, and Remote Key Provisioning as potentially relevant dependencies. Verify actual application behavior and Play Integrity results; do not assume a specific verdict.
- **ADB debugging:** Some banking applications may check whether ADB debugging is enabled. Turn off USB/Wireless debugging when it is not needed.
- **Keyboard:** The source records Gboard disabled with no replacement selected as the default input method. Install and test a replacement keyboard or re-enable Gboard if on-screen typing is unavailable.
- **Gallery:** Google Photos was recorded as disabled. Fossify Gallery is mentioned as an offline alternative; test it before relying on it.
- **Advertising ID:** Review Android's Advertising ID controls and delete/reset the identifier if desired.
- **Private DNS:** A filtered DNS provider or local DNS/firewall tool may block some known tracker domains. Filtering cannot guarantee that every SDK endpoint is blocked.
- **Wi-Fi/Bluetooth scanning:** Review location scanning settings. Disabling scanning may affect location accuracy and nearby-device features.

## 10. Historical operations — retrospective record only

> [!WARNING]
> The following describes earlier events in the Portuguese source. It is not an execution guide, was not revalidated for this translation, and must not be repeated as a batch.

The source report records that, after user authorization:
- Nine essential components were re-enabled.
- Selected runtime permissions were revoked from third-party apps and selected Google apps; third-party app identities were omitted from the public report.
- pm clear was run on a number of Google and Motorola packages. Repeating this can erase application data.
- Some packages rejected disabling with Failure: package is non-disable. The historical session then applied standby, AppOps, and network restrictions by UID. Such restrictions can affect every package sharing the UID.
- Three persistent services were reportedly uninstalled for User 0: com.motorola.android.nativedropboxagent, com.motorola.bach.modemstats, and com.bluetooth.aptxmode. This is a historical record, not a recommendation to repeat the action.
- A post-reboot check reportedly found no matching processes for those services and recorded com.android.rkpdapp and com.dolby.daxservice running again.

Historical storage and ZRAM changes are not independently reproduced in this English summary.

---

## Limitations and status

This document summarizes one device and one historical collection. It does not establish compatibility of any debloating script, authorize package changes, or provide a universal debloating procedure. Package-level details remain in the Portuguese batch documents until those files are translated separately.

**The Portuguese report remains the detailed source record.**
