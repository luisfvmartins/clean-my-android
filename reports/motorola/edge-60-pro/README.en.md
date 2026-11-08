# Motorola Edge 60 Pro — Audit Summary

**Model:** XT2507-1 · **Codename:** `cybert`  
**Interface:** Hello UI  
**Android version:** pending canonical confirmation  
<badge>Pending validation</badge>

This folder contains the technical report, before/after package inventories, performance metrics, and a detailed history of debloating, sandboxing, and privacy-related actions performed on the **Motorola Edge 60 Pro (XT2507-1)**.

## Executive summary

The debloating and sandboxing session was performed through **Android Debug Bridge (ADB)** without root. Factory packages were mapped, selected services were disabled or restricted, permissions were changed, and secondary Android user profiles were addressed.

> **Validation status: Pending.** This report reflects evidence collected during the ADB session. Canonical Android version confirmation through `getprop ro.build.version.release` and functional tests for voice calls, SMS, biometrics, banking applications, and Play Integrity remain pending in-person validation by the device owner.

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

- [Full technical audit (Portuguese)](README.md)
- [Technical audit details](auditoria.md)
- [Initial package inventory](inventario-antes.json)
- [Final package inventory](inventario-depois.json)
- [Disabled packages](pacotes-desativados.txt)
- [Packages uninstalled for user 0](pacotes-desinstalados.txt)
- [Permission and AppOps changes](permissoes-alteradas.json)
- [Metrics and test status](comparativo.json)
- [Evidence provenance and pending collection (Portuguese)](evidencias/README.md)

## Safety and limitations

- The Android version remains pending canonical confirmation.
- Functional testing remains pending for key features, including telephony, SMS, biometrics, banking apps, and Play Integrity.
- The report does not approve a general-purpose debloat procedure for this model.
- Package state snapshots are historical records, not lists to execute.
- Do not repeat destructive or bulk commands from historical logs.
- Consult the source report and evidence documentation before drawing technical conclusions.

**A published report is not script homologation.** No procedure should be applied to another model or firmware based on this report.
