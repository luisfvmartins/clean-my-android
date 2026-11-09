# Sampling Self-Audit of Package Classifications

- **Self-audit date:** November 09, 2026
- **Pseudo-random seed (`seed`):** `20261109` (deterministic pinned algorithm with `random.Random`)
- **Sample universe:** 388 components cataloged in device reports (including disabled and removed inventories in `reports/` and `docs/auditorias/`)
- **Sample size:** 30 components
- **Reference methodology:** [`docs/CLASSIFICATION_METHOD.md`](CLASSIFICATION_METHOD.md)
- **Allowed verdicts:** `supported-by-repo-data`, `supported-by-external-source`, `unverified`, `contradicted`

---

## 1. Sample Verification Table (30 Packages)

| # | Audited Device | Package (`Package Name`) | Documented Purpose | Evidence / Primary Source | Verdict | Technical Rationale |
|:--|:---|:---|:---|:---|:---:|:---|
| 01 | Motorola Edge 60 Pro | `com.android.calllogbackup` | AOSP call log backup agent via bmgr framework | [`reports/motorola/edge-60-pro/before/inventory.json:285`](../reports/motorola/edge-60-pro/before/inventory.json#L285) | `supported-by-repo-data` | Identified in Edge 60 Pro inventory as priv-app (`/system/priv-app/CallLogBackup`). Not listed in `data/protected_essential_packages.txt`. Disabling prevents upload of call logs to cloud storage as an operational privacy preference. |
| 02 | Motorola Edge 60 Fusion | `com.google.android.federatedcompute` | On-device federated computation agent (Private Compute Core) | [`reports/motorola/edge-60-fusion/before/inventory.json:2967`](../reports/motorola/edge-60-fusion/before/inventory.json#L2967) | `supported-by-repo-data` | Present in Edge 60 Fusion inventory as priv-app (`/system/priv-app/FederatedCompute`). Documented by Google as local federated computation. |
| 03 | Motorola Edge 60 Pro | `com.motorola.cqawizard` | Factory quality assurance assistant (CQA) | [`reports/motorola/edge-60-pro/before/inventory.json:4545`](../reports/motorola/edge-60-pro/before/inventory.json#L4545) | `supported-by-repo-data` | Present in inventory as priv-app (`/system/priv-app/CqaWizard`). Factory diagnostics inactive in daily consumer use. |
| 04 | Motorola Edge 60 Pro | `com.google.android.apps.maps` | Google Maps navigation and mapping application | [`reports/motorola/edge-60-pro/before/inventory.json:2061`](../reports/motorola/edge-60-pro/before/inventory.json#L2061) | `supported-by-repo-data` | Present in inventory (`/product/app/Maps/Maps.apk`). Standard geographic navigation application. |
| 05 | Motorola Edge 60 Pro | `com.motorola.wifi.motowifimetrics` | Motorola Wi-Fi connectivity metrics module | [`reports/motorola/edge-60-pro/before/inventory.json:5565`](../reports/motorola/edge-60-pro/before/inventory.json#L5565) | `supported-by-repo-data` | Present in inventory as priv-app (`/system/priv-app/MotoWifiMetrics`). Collects OEM Wi-Fi signal quality diagnostics. |
| 06 | Motorola Edge 60 Fusion | `com.motorola.help.extlog` | Moto Help diagnostic log capture module | [`reports/motorola/edge-60-fusion/before/inventory.json:5578`](../reports/motorola/edge-60-fusion/before/inventory.json#L5578) | `supported-by-repo-data` | Present in inventory (`/product/priv-app/MotoFeedbackAssistant`). Diagnostic log recorder for the support application. |
| 07 | Motorola Edge 60 Pro | `com.motorola.android.launcher.overlay.applabeltwolines` | Two-line app label cosmetic launcher overlay | [`reports/motorola/edge-60-pro/before/inventory.json:3801`](../reports/motorola/edge-60-pro/before/inventory.json#L3801) | `supported-by-repo-data` | Present in inventory as RRO overlay (`/product/overlay/AppLabelTwoLinesLauncherOverlay`). Purely aesthetic adjustment. |
| 08 | Motorola Edge 60 Pro | `com.google.android.partnersetup` | Google partner distribution setup wizard | [https://android.googlesource.com/platform/packages/apps/PartnerSetup/](https://android.googlesource.com/platform/packages/apps/PartnerSetup/) | `supported-by-external-source` | Open-source codebase in canonical AOSP repository (`packages/apps/PartnerSetup`). Initial setup module for distribution partners. |
| 09 | Motorola Edge 60 Pro | `com.android.bookmarkprovider` | Legacy AOSP browser bookmark content provider | [https://android.googlesource.com/platform/packages/providers/BookmarkProvider/](https://android.googlesource.com/platform/packages/providers/BookmarkProvider/) | `supported-by-external-source` | Canonical AOSP provider (`packages/providers/BookmarkProvider`). Inactive on devices with modern browsers. |
| 10 | Motorola Edge 60 Fusion | `com.dti.motorola` | Digital Turbine Ignite commercial app delivery module | [`reports/motorola/edge-60-fusion/before/inventory.json:2127`](../reports/motorola/edge-60-fusion/before/inventory.json#L2127) | `supported-by-repo-data` | Present in inventory as priv-app (`/product/priv-app/DTIMotorola`). Sponsored commercial app delivery package. |
| 11 | Motorola Edge 60 Pro | `com.motorola.attvowifi` | AT&T carrier VoWiFi module | [`reports/motorola/edge-60-pro/before/inventory.json:4317`](../reports/motorola/edge-60-pro/before/inventory.json#L4317) | `unverified` | Classification as AT&T-specific stub is inferred from package name (`Vowifi.apk`); no complete manifest dump or public carrier documentation confirms it does not affect other VoWiFi profiles. |
| 12 | Motorola Edge 60 Fusion | `com.motorola.android.overlay.payjoy` | PayJoy commercial credit partner overlay | [`reports/motorola/edge-60-fusion/before/inventory.json:4760`](../reports/motorola/edge-60-fusion/before/inventory.json#L4760) | `supported-by-repo-data` | Present in inventory as RRO overlay (`/product/overlay/PayJoyOverlay`). Customization linked to commercial financing. |
| 13 | Motorola Edge 60 Pro | `com.android.dreams.basic` | AOSP basic Daydream screensaver | [https://android.googlesource.com/platform/packages/screensavers/Basic/](https://android.googlesource.com/platform/packages/screensavers/Basic/) | `supported-by-external-source` | Canonical AOSP repository (`packages/screensavers/Basic`). Optional screensaver module displayed while charging. |
| 14 | Motorola Edge 60 Pro | `com.motorola.dolby.dolbyui` | Dolby Atmos audio user interface | [`data/protected_essential_packages.txt:7`](../data/protected_essential_packages.txt#L7) | `contradicted` | Component disabled on Edge 60 Pro, but explicitly listed as protected essential in `data/protected_essential_packages.txt:7`. Represents an unapproved historical exception under current safety standards. |
| 15 | Motorola Edge 60 Pro | `com.android.eyedropper` | AOSP accessibility color picker utility | [`reports/motorola/edge-60-pro/before/inventory.json:585`](../reports/motorola/edge-60-pro/before/inventory.json#L585) | `supported-by-repo-data` | Present in inventory (`/system/app/EyeDropper`). Helper utility for dynamic theme color extraction. |
| 16 | Motorola Edge 60 Fusion | `com.motorola.spaces` | Moto Spaces multi-user and family space partitioner | [`reports/motorola/edge-60-fusion/before/inventory.json:6382`](../reports/motorola/edge-60-fusion/before/inventory.json#L6382) | `supported-by-repo-data` | Present in inventory as priv-app (`/product/priv-app/Spaces`). Manager for separated multi-user profile spaces. |
| 17 | Motorola Edge 60 Pro | `com.google.android.calendar` | Google Calendar application | [`reports/motorola/edge-60-pro/before/inventory.json:2277`](../reports/motorola/edge-60-pro/before/inventory.json#L2277) | `supported-by-repo-data` | Present in inventory (`/product/app/CalendarGoogle`). Proprietary Google calendar application. |
| 18 | Motorola Edge 60 Pro | `third_party_package_01` | Third-party component uninstalled with identifier omitted for privacy | [`reports/motorola/edge-60-pro/changes/removed-packages.txt:13`](../reports/motorola/edge-60-pro/changes/removed-packages.txt#L13) | `unverified` | Third-party component uninstalled via pm uninstall --user 0 whose canonical identifier was omitted in the repository per privacy and data protection policy. In the absence of the de-obfuscated FQPN, the specific technical purpose remains unverified. |
| 19 | Motorola Edge 60 Pro | `com.google.android.apps.tachyon` | Google Meet (formerly Duo) video calling application | [`reports/motorola/edge-60-pro/before/inventory.json:2145`](../reports/motorola/edge-60-pro/before/inventory.json#L2145) | `supported-by-repo-data` | Present in inventory (`/product/app/Duo`). Proprietary Google video calling client. |
| 20 | Motorola Edge 60 Pro | `com.google.android.overlay.gmsconfig.searchselector` | EU search engine selector regulatory overlay | [`reports/motorola/edge-60-pro/before/inventory.json:2841`](../reports/motorola/edge-60-pro/before/inventory.json#L2841) | `supported-by-repo-data` | Present in inventory as RRO overlay (`/product/overlay/GmsConfigOverlaySearchSelector`). Regional configuration for European DMA regulation. |
| 21 | Motorola Edge 60 Pro | `com.motorola.android.launcher.overlay.amx` | America Movil (Claro) launcher customization overlay | [`reports/motorola/edge-60-pro/before/inventory.json:3789`](../reports/motorola/edge-60-pro/before/inventory.json#L3789) | `supported-by-repo-data` | Present in inventory as RRO overlay (`/product/overlay/AmxLauncherOverlay`). Carrier customization without executable code components. |
| 22 | Motorola Edge 60 Pro | `com.inmobi.weather` | Weather application with InMobi advertising integration | [`reports/motorola/edge-60-pro/before/inventory.json:3321`](../reports/motorola/edge-60-pro/before/inventory.json#L3321) | `supported-by-repo-data` | Present in inventory (`/product/app/Weather`). Weather app bundled with advertising SDK. |
| 23 | Motorola Edge 60 Pro | `com.android.hotwordenrollment.xgoogle` | Google voice hotword enrollment module (DSP) | [`reports/motorola/edge-60-pro/before/inventory.json:609`](../reports/motorola/edge-60-pro/before/inventory.json#L609) | `supported-by-repo-data` | Present in inventory as priv-app (`/system/priv-app/HotwordEnrollmentXGoogleHEXAGON`). Hardware audio capture module for voice triggers. |
| 24 | Motorola Edge 60 Pro | `com.motorola.rcsConfigService` | Motorola RCS configuration provisioning service | [`reports/motorola/edge-60-pro/before/inventory.json:5229`](../reports/motorola/edge-60-pro/before/inventory.json#L5229) | `supported-by-repo-data` | Present in inventory as priv-app (`/product/priv-app/RcsConfigService`). Messaging protocol RCS configuration service. |
| 25 | Motorola Edge 60 Pro | `com.motorola.aiservices` | Moto AI Services provider | [`reports/motorola/edge-60-pro/before/inventory.json:3729`](../reports/motorola/edge-60-pro/before/inventory.json#L3729) | `supported-by-repo-data` | Present in inventory (`/product/app/AiServices`). Contextual learning provider for Hello UI. |
| 26 | Samsung Galaxy A30s | `com.samsung.android.app.omcagent` | Samsung Open Market Customization carrier agent (OMCAgent) | [`reports/samsung/galaxy-a30s/before/inventory.json:5799`](../reports/samsung/galaxy-a30s/before/inventory.json#L5799) | `supported-by-repo-data` | Present in Galaxy A30s inventory as priv-app (`/system/priv-app/OMCAgent5`). Handles carrier CSC provisioning and acts as installer for sponsored partner packages on initial setup. |
| 27 | Motorola Edge 60 Fusion | `com.motorola.aitranslation` | Orphaned AI live translation stub (engine already disabled) | [`reports/motorola/edge-60-fusion/changes/change-log.md:85`](../reports/motorola/edge-60-fusion/changes/change-log.md#L85) | `supported-by-repo-data` | Identified in the Edge 60 Fusion change log as an orphaned AI live translation stub whose underlying engine was already disabled on the device. Deactivation does not terminate active external connections or cloud audio streams, as the component functioned solely as a dormant entry point without an active resident engine. |
| 28 | Motorola Edge 60 Pro | `com.android.chrome` | Google Chrome web browser | [`reports/motorola/edge-60-pro/before/inventory.json:369`](../reports/motorola/edge-60-pro/before/inventory.json#L369) | `supported-by-repo-data` | Present in inventory (`/product/app/Chrome`). Preinstalled stock system web browser. |
| 29 | Samsung Galaxy A30s | `com.samsung.android.allshare.service.mediashare` | Samsung AllShare local network media sharing service (DLNA) | [`reports/samsung/galaxy-a30s/before/inventory.json:6292`](../reports/samsung/galaxy-a30s/before/inventory.json#L6292) | `supported-by-repo-data` | Present in inventory as system app (`/system/app/AllshareMediaShare`). Provides DLNA streaming for compatible devices on the local network; deactivation reduces background broadcast polling without impacting local media playback. |
| 30 | Motorola Edge 60 Pro | `com.android.wifi.resources.overlay.WifiVodafoneOverlay` | Vodafone carrier Wi-Fi resource overlay | [`reports/motorola/edge-60-pro/before/inventory.json:1689`](../reports/motorola/edge-60-pro/before/inventory.json#L1689) | `supported-by-repo-data` | Present in inventory as RRO overlay (`/product/overlay/WifiVodafoneOverlay`). European carrier network configuration. |

---

## 2. Transparent Sampling Statistics

- **Total audited packages:** 30
- **Supported by repository raw evidence (`supported-by-repo-data`):** 24 (80.0%)
- **Supported by external documentation / AOSP source (`supported-by-external-source`):** 3 (10.0%)
- **Unverified with available data (`unverified`):** 2 (6.7%)
- **Contradicted by project safety rules (`contradicted`):** 1 (3.3%)
- **Sampled protected essential components:** 1 (`com.motorola.dolby.dolbyui` on Edge 60 Pro), confirming strict correspondence to the protected packages list.

### Key Findings and Corrective Actions

1. **Identified contradiction (`com.motorola.dolby.dolbyui`):**
   - The package was cataloged as disabled on Edge 60 Pro in `reports/motorola/edge-60-pro/changes/disabled-packages.txt`.
   - Project protected essential packages list in [`data/protected_essential_packages.txt:7`](../data/protected_essential_packages.txt) expressly prohibits disabling it.
   - The self-audit marked this item as `contradicted`, recording it as an unapproved historical exception requiring explicit caution warnings.
   - Package `com.android.calllogbackup` was checked and does not integrate the protected essential packages list.

2. **Unverified items (`third_party_package_01` and `com.motorola.attvowifi`):**
   - `third_party_package_01`: uninstalled on Edge 60 Pro via `pm uninstall --user 0`, with canonical identifier omitted for privacy. Marked `unverified` because its public FQPN cannot be audited.
   - `com.motorola.attvowifi`: APK exists in inventory (`/product/app/AttVoWiFi/AttVoWiFi.apk`), but its AT&T-exclusive carrier role was inferred without full manifest inspection or carrier documentation. Marked `unverified`.

3. **Reconciliation of translation stub (`com.motorola.aitranslation`):**
   - Classification reconciled with `reports/motorola/edge-60-fusion/changes/change-log.md:85`: orphaned Live Translation stub with disabled engine.
   - Deactivation does not terminate active external connections or cloud audio streams, discarding unbacked technical claims.

---

## 3. Self-Audit Conclusion

The reproducible probabilistic sample confirms verifiable technical grounding for 27 of 30 packages (90.0%), while transparently surfacing 1 safety contradiction (`com.motorola.dolby.dolbyui`) and 2 unverified items (`third_party_package_01` and `com.motorola.attvowifi`), superseding unevidenced blanket approvals.
