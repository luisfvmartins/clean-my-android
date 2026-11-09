# Motorola Edge 60 Fusion — Forensic Audit and Optimization (English Summary)

> **Translation note:** This is an English structured summary, not a line-by-line translation of the complete Portuguese audit. The Portuguese document remains the detailed source of record: [full audit in Portuguese](audit.md). Figures and findings below reproduce that report and have not been independently re-measured for this summary.

## Device and audit context

- **Model:** Motorola Edge 60 Fusion
- **Product / device identifiers:** `motorola_edge_60_fusion` / `scout_g_sysn`
- **Codename / board:** `scout` / `mt6878` (MediaTek Dimensity 7300)
- **Android:** 16 (API 36)
- **Build:** `W1VCS36H.14-20-19-9`
- **Security patch:** 2026-09-01
- **Software channel:** Brazilian retail (`retbr`)
- **Bootloader / privilege:** locked bootloader; no root
- **Audit dates:** November 7–8, 2026
- **Connection and collection:** authorized ADB session; read the source report for the complete command-level methodology.

## Scope and findings

The source audit cataloged 486 firmware packages and organized the review into six groups:

1. User-installed and third-party applications.
2. Commercial partners, carriers, advertising software, and financing components.
3. Motorola / Lenovo services and overlays.
4. Google / Google Mobile Services components.
5. MediaTek SoC, radio, telephony, and hardware abstraction layers.
6. Android core, AOSP, and base system components.

The investigation identified commercial app installers and advertising modules, OEM and SoC diagnostic services, Google location-history components, passive hotword-related components, and applications with precise-location permissions. These are findings about this specific firmware and collection; they are not a universal Android removal list.

## Reported post-audit state

According to the Portuguese source report:

- **486** packages were cataloged in the initial firmware inventory.
- **155** packages were classified as altered: 67 already disabled by the factory and 88 addressed through the documented ADB / AppOps / input-method actions.
- **343** packages were active for User 0 after the work, including 12 FOSS applications installed as alternatives.
- Available RAM was reported to increase from approximately **2,750 MB** to a range of **4,153–4,573 MB**.
- Background processes were reported to decrease from **66** to **39**.

These are session observations, not guaranteed performance gains. Battery life over a standardized 24-hour cycle and per-application storage savings were not measured in the source comparison.

## Safety and functional validation

The source describes a non-root process with the bootloader kept locked and critical platform components intentionally preserved. It reports functional checks for boot, navigation, calls, SMS, mobile data, Wi-Fi, Bluetooth, GPS, camera, biometrics, banking apps, and selected user-preserved applications.

The original report's test conditions and limitations must be consulted before relying on any result. Package behavior can change with firmware, region, carrier configuration, app updates, and user requirements.

## Related records

- [Full technical audit in Portuguese](audit.md)
- [Before/after comparison — English summary](comparison-report.en.md) · [Portuguese source](comparison-report.md)
- [Detailed change log — English summary](changes/change-log.en.md) · [Portuguese source](changes/change-log.md)
- [Device overview in English](README.en.md) · [Portuguese](README.md)

**Do not reuse the historical package actions on another device without a fresh, device-specific audit, evidence review, and explicit owner authorization.**
