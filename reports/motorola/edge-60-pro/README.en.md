# Motorola Edge 60 Pro — Audit Summary


> **Privacy note:** the 50 entries classified as third-party components have pseudonymized package identifiers. Installation-specific `/data/app` paths have been normalized. Aggregate inventory counts and recorded package states are preserved. The source inventory does not establish whether these components were user-installed or preloaded by a vendor.

**Model:** XT2507-1 · **Codename:** `cybert`  
**Interface:** Hello UI  
**Android version:** 17 (SDK 37, build `7a1c2-08c719` confirmed via `getprop`)  
**Status:** Level 3 — Integrity functional validation completed; voice/SMS subsystems pending

This folder contains the technical report, before/after package inventories, performance metrics, and a detailed history of debloating, sandboxing, and privacy-related actions performed on the **Motorola Edge 60 Pro (XT2507-1)**.

## Executive summary

The debloating and sandboxing session was performed through **Android Debug Bridge (ADB)** without root. Factory packages were mapped, selected services were disabled or restricted, permissions were changed, and secondary Android user profiles were addressed.

> **Validation status: Level 3 (Integrity Validation Approved).** Canonical Android version confirmation (Android 17 / API 37) and Play Integrity attestation validation have been completed following Play Store restoration. Telephony, SMS, and 24h battery testing remain under ongoing observation.

> [!CAUTION]
> **Conflict with the protected-components list and empirical resolution:** a post-audit review found 18 packages listed in both `pacotes-desativados.txt` and `data/protected_essential_packages.txt`. The overlap included `com.android.vending` (Google Play Store).
>
> **November 09, 2026 Resolution:** During real-world testing, disabling `com.android.vending` caused initialization failures in critical Brazilian government apps (**CNH Digital** and **GOV.BR**) due to Play Integrity API rejection. The package and associated verification modules were restored via ADB, successfully restoring both services. See the full [Play Integrity Case Study](case-study-play-integrity.en.md).

### Reported actions and observations

- **501 components** mapped in the initial firmware inventory.
- **244 packages disabled** for user 0 using `pm disable-user --user 0`.
- **9 packages uninstalled for user 0**, including third-party and system packages.
- System app updates were reverted for selected packages; an aggregate increase in free `/data` space was reported, but per-app gains were not measured.
- Selected firmware-protected services were restricted through AppOps and background network policy.
- Runtime permissions and Google Play Services AppOps were changed.
- Secondary Android user profiles were stopped or removed.
- RAM, storage, and temperature changes were reported in the source report; these measurements require careful interpretation and independent validation under comparable conditions.

## Important interpretation notes

The figures above reproduce claims recorded in the Portuguese source report. They are not independently re-measured by this English translation. Do not present them as guaranteed benefits or as results applicable to other devices.

The report includes historical operational details. Those details are **not an execution guide or authorization to repeat commands**. Some actions may affect data, essential features, or shared services.

## Files

- [Full technical audit (English summary)](auditoria.en.md) · [Original full report (Portuguese)](README.md)
- [Technical audit details (English summary)](auditoria.en.md) · [Original detailed audit (Portuguese)](auditoria.md)
- [Play Integrity Case Study (English)](case-study-play-integrity.en.md) · [Portuguese source](case-study-play-integrity.md)
- [Initial package inventory](inventario-antes.json)
- [Final package inventory](inventario-depois.json)
- [Disabled packages](pacotes-desativados.txt)
- [Packages uninstalled for user 0](pacotes-desinstalados.txt)
- [Permission and AppOps changes](permissoes-alteradas.json)
- [Metrics and test status](comparativo.json)
- [Evidence provenance and chain of custody (English)](evidencias/README.en.md) · [Portuguese source](evidencias/README.md)

## Safety and limitations

- Android 17 (SDK 37) confirmed via `getprop`.
- Play Integrity attestation verified and passing with government identity apps (CNH and GOV.BR). Telephony, SMS, and battery observation remain ongoing.
- The report does not approve a general-purpose debloat procedure for this model.
- Package state snapshots are historical records, not lists to execute.
- Do not repeat destructive or bulk commands from historical logs.
- Consult the source report and evidence documentation before drawing technical conclusions.

**A published report is not script homologation.** No procedure should be applied to another model or firmware based on this report.


## Historical summary

- [Historical report — English summary](historical-summary.en.md) · [Historical summary (Portuguese)](historical-summary.pt-BR.md)
