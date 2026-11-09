# Motorola Edge 60 Pro — Audit Summary

> [!CAUTION]
> **CRITICAL WARNING — DISABLED ESSENTIAL COMPONENTS AND PENDING VALIDATION**
>
> This device has **18 essential packages disabled** in `changes/disabled-packages.txt` that conflict with current project safety rules (`data/protected_essential_packages.txt`), including:
> - **Dialer & Telephony:** `com.android.dialer`, `com.google.android.dialer`
> - **Messaging / SMS:** `com.google.android.apps.messaging`
> - **Contacts:** `com.android.contacts`, `com.android.providers.contactkeys`
> - **Google Play Store:** `com.android.vending`
> - **Emergency Services:** `com.android.emergency`, `com.motorola.nfwlocationattribution`
> - **SIM Card & Carrier:** `com.android.stk`, `com.android.simappdialog`, `com.android.carrierdefaultapp`
>
> Functional validation of the device is currently **pending** (Homologation Level 2).
> To check current role holders without altering device state, run these **read-only** commands:
> ```bash
> adb shell cmd role get-role-holders android.app.role.DIALER
> adb shell cmd role get-role-holders android.app.role.SMS
> adb shell pm list packages -d --user 0
> ```
> Individual re-enablement of any component is performed via `./scripts/restore.sh <package>`, at the sole discretion of the device owner.

> **Privacy note:** the 50 entries classified as third-party components have pseudonymized package identifiers. Installation-specific `/data/app` paths have been normalized. Aggregate inventory counts and recorded package states are preserved. The source inventory does not establish whether these components were user-installed or preloaded by a vendor.

**Model:** XT2507-1 · **Codename:** `cybert`  
**Interface:** Hello UI  
**Android version:** pending canonical confirmation  
**Status:** Pending validation

This folder contains the technical report, before/after package inventories, performance metrics, and a detailed history of debloating, sandboxing, and privacy-related actions performed on the **Motorola Edge 60 Pro (XT2507-1)**.

## Executive summary

The debloating and sandboxing session was performed through **Android Debug Bridge (ADB)** without root. Factory packages were mapped, selected services were disabled or restricted, permissions were changed, and secondary Android user profiles were addressed.

> **Validation status: Pending.** This report reflects evidence collected during the ADB session. Canonical Android version confirmation through `getprop ro.build.version.release` and functional tests for voice calls, SMS, biometrics, banking applications, and Play Integrity remain pending in-person validation by the device owner.

> [!CAUTION]
> **Conflict with the protected-components list:** a post-audit review found 18 packages listed in both `changes/disabled-packages.txt` and `data/protected_essential_packages.txt`. The overlap includes dialer and SMS, emergency, SIM Toolkit, Bluetooth, contacts, and system-support components. This does not confirm the device's current state or prove a functional failure, but it conflicts with the project's current safety guardrails. This is a historical record, not a recommendation. **Do not reuse this disable list on other devices.** The actual state must be checked on-device; any restoration requires individual assessment and in-person validation of calls, SMS, SIM, emergency, Bluetooth, and contacts.

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

- [Full technical audit (English summary)](audit.en.md) · [Original full report (Portuguese)](README.md)
- [Technical audit details (English summary)](audit.en.md) · [Original detailed audit (Portuguese)](audit.md)
- [Initial package inventory](before/inventory.json)
- [Final package inventory](after/inventory.json)
- [Disabled packages](changes/disabled-packages.txt)
- [Packages uninstalled for user 0](changes/removed-packages.txt)
- [Permission and AppOps changes](changes/permission-changes.json)
- [Metrics and test status](metrics.json)
- [Evidence provenance and pending collection (English)](evidence/README.en.md) · [Portuguese source](evidence/README.md)

## Safety and limitations

- The Android version remains pending canonical confirmation.
- Functional testing remains pending for key features, including telephony, SMS, biometrics, banking apps, and Play Integrity.
- The report does not approve a general-purpose debloat procedure for this model.
- Package state snapshots are historical records, not lists to execute.
- Do not repeat destructive or bulk commands from historical logs.
- Consult the source report and evidence documentation before drawing technical conclusions.

**A published report is not script homologation.** No procedure should be applied to another model or firmware based on this report.


## Historical summary

- [Historical report — English summary](comparison-report.en.md) · [Historical summary (Portuguese)](comparison-report.md)
