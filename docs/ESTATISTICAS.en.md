# Project Statistics

Metrics are calculated from the structured catalog in [data/device_catalog.json](../data/device_catalog.json). Counts reflect only documented and explicitly classified information.

## Overview

- **Cataloged devices:** 2
- **Represented manufacturers:** 1
- **Confirmed Android versions:** 1 (15)
- **Reports with component counts:** 2

## Devices

| Manufacturer / model | Code | Android | Audit status | Recorded components |
|---|---|---|---|---:|
| Motorola Moto G54 5G | XT2343-1 | Android 15 | [Technical inventory published](../reports/motorola/moto-g54-5g/README.en.md) | 462 — components audited in the local inventory |
| Motorola Edge 60 Pro | XT2507-1 | Not confirmed (pending confirmation) | [Report published; functional validation pending](../reports/motorola/edge-60-pro/README.en.md) | 501 — components mapped in the initial inventory |

## How to interpret the numbers

- **Component counts are not added together.** Reports use different scopes and states: Moto G54 records audited components; Edge 60 Pro records components mapped in the initial inventory.
- The Moto G54 count is 462 components in the local collection; the public version omits 29 user-installed apps and documents 394 system/manufacturer components.
- The Edge 60 Pro count (501) refers to the mapped initial inventory and does not mean every component has been functionally validated.
- Pending Android versions are excluded from the confirmed-version count.
- **Cataloged device**, **published audit**, **functional validation**, and **script approval** are different states. Listing a device here does not imply approval.
- Battery, RAM, storage, privacy, or compatibility improvements are not estimated.

## Updates and validation

Data is maintained in `data/device_catalog.json`. When adding or updating an audit, revise that file using information supported by the device documentation and run:

    python scripts/generate_statistics.py
    python scripts/generate_statistics.py --check

Automated validation checks whether this page matches the catalog. Generation does not query the GitHub API, count Pull Requests, or access or modify devices.

See the [complete audit catalog](../reports/README.en.md).
