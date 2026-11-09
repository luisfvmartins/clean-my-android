# Project Statistics

Metrics are calculated from the structured catalog in [data/device_catalog.json](../data/device_catalog.json). Counts reflect only documented and explicitly classified information.

## Overview

- **Cataloged devices:** 4
- **Represented manufacturers:** 2
- **Confirmed Android versions:** 3 (11, 15, 16)
- **Reports with component counts:** 4

## Devices

| Manufacturer / model | Code | Android | Audit status | Recorded components |
|---|---|---|---|---:|
| Motorola Moto G54 5G | XT2343-1 | Android 15 | [Technical inventory published](../reports/motorola/moto-g54-5g/README.en.md) | 462 — components audited in the local inventory |
| Motorola Edge 60 Pro | XT2507-1 | Not confirmed (pending confirmation) | [Report published; functional validation pending](../reports/motorola/edge-60-pro/README.en.md) | 501 — components mapped in the initial inventory |
| Motorola Edge 60 Fusion | scout_g_sysn | Android 16 | [Audit and debloat completed](../reports/motorola/edge-60-fusion/README.en.md) | 486 — packages mapped in the initial inventory |
| Samsung Galaxy A30s | SM-A307GT | Android 11 | [Audit and surgical optimization completed](../reports/samsung/galaxy-a30s/README.en.md) | 392 — packages cataloged in factory firmware |

## How to interpret the numbers

- **Component counts are not added together.** Reports use different scopes and states: Moto G54 records audited components; Edge 60 Pro records components mapped in the initial inventory.
- The Moto G54 count is 462 components in the local collection; the public version omits 29 user-installed apps and publishes 433 components: 394 system/manufacturer package records and 39 APEX modules.
- The Edge 60 Pro count (501) refers to the mapped initial inventory and does not mean every component has been functionally validated.
- Pending Android versions are excluded from the confirmed-version count.
- **Cataloged device**, **published audit**, **functional validation**, and **script approval** are different states. Listing a device here does not imply approval.
- Battery, RAM, storage, privacy, or compatibility improvements are not estimated.

## Updates and validation

Data is maintained in `data/device_catalog.json`. When adding or updating an audit, revise that file using information supported by the device documentation and run:

    python scripts/generate_statistics.py
    python scripts/generate_statistics.py --check

The current generator writes and validates `docs/ESTATISTICAS.md` (Portuguese). This English companion is maintained as a manual translation and is not currently checked by `--check`; update it when the catalog or Portuguese statistics change. Generation does not query the GitHub API, count Pull Requests, or access or modify devices.

See the [complete audit catalog](../reports/README.md).
