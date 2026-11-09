# Historical Report — Motorola Edge 60 Pro (XT2507-1)

> **Legacy-file note:** This English document summarizes the preserved Portuguese legacy report. The file remains in the repository for historical continuity; the canonical current documentation is organized under [the Edge 60 Pro report directory](README.en.md). Audit status remains **pending validation**. This is not an execution list or device certification.

## Device and validation status

- **Model:** Motorola Edge 60 Pro (`XT2507-1`)
- **Codename:** `cybert`
- **Interface:** Motorola Hello UI
- **Android version:** pending canonical confirmation through device properties
- **Execution mode:** ADB without root
- **Audit status:** pending in-person functional validation by the device owner

The source report states that the Android version and functional checks for voice calls, SMS, biometrics, banking applications, and Play Integrity still require direct confirmation. Its package history is retrospective evidence, not permission to repeat commands.

## Historical figures reported

The Portuguese legacy document records:

| Indicator | Before | Reported after state |
|---|---:|---:|
| Initial inventory | 501 components | 492 packages reported for User 0 |
| Disabled packages | 60 factory-disabled | 244 recorded as disabled |
| Uninstalled for User 0 | — | 9 |
| Available RAM | ~4.5 GB | ~7.2 GB |
| Free `/data` storage | ~193 GB | ~197 GB (aggregate partition change) |
| Idle temperature | 37–40°C | 33.0°C |
| Active secondary profiles | User 0 + User 11 | User 0 only |

These values are reproduced from a legacy record and have not been independently verified in this summary. The storage figure is aggregate, not a per-application measurement. Battery impact and banking / Play Integrity behavior remain pending validation.

## Critical safety warning

A later review found 18 package identifiers present both in the historical disabled-package list and the project's protected-essential-components list. The overlap includes telephony, SMS, emergency, SIM Toolkit, Bluetooth, contacts, and system-support components. This does not establish the device's current state or prove a functional failure, but it conflicts with current project safeguards.

**Do not reuse the historical disable list.** Any recovery or restoration must be assessed package by package on the actual device, followed by in-person validation of calls, SMS, SIM, emergency functions, Bluetooth, and contacts.

## Historical workflow summary

The source describes four layers: user-level package disablement, reverting selected system-app updates, permission / AppOps restrictions by UID, and background network policy with DNS filtering. The details are retained in the Portuguese legacy file and must be interpreted in light of the warning above.

- [Portuguese legacy historical report](comparison-report.md)
- [Current English report overview](README.en.md) · [Portuguese overview](README.md)
- [Current English technical audit summary](audit.en.md) · [Portuguese technical audit](audit.md)
