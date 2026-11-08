# Android Device Audits

This catalog lists technical audits submitted by the community and incorporated into **Clean My Android** through Pull Requests. Each device has its own documentation so results, limitations, and recommendations are not generalized to other models.

**Principle:** a published audit is a technical record, not authorization to run the same commands on another device. See the [project statistics](../docs/ESTATISTICAS.en.md), generated from the structured catalog.

## Catalog

| Manufacturer / model | Identification | Android / interface | Status and scope | Report |
|---|---|---|---|---|
| **Motorola Moto G54 5G** | `XT2343-1` · `cancunf` | Android 15 · Hello UI | Technical inventory published; main report and seven inventory batch files | [Device folder](motorola/moto-g54-5g/README.en.md) · [Main report (Portuguese)](../docs/AUDITORIA_MOTO_G54_5G.md) · [Batch inventory index (English)](../docs/auditorias/moto-g54/README.en.md) |
| **Motorola Edge 60 Pro** | `XT2507-1` · `cybert` | Hello UI · canonical version pending confirmation | Report published; functional validation and supplemental data collection pending | [English summary](motorola/edge-60-pro/README.en.md) · [Full report (Portuguese)](motorola/edge-60-pro/README.md) |

### Understanding audit statuses

- **Inventory published:** collected data and documentation are available; this does not mean every change has been tested.
- **Validation pending:** some data or procedures still require confirmation on the device.
- **Script approved:** use this status only when the script, model, and system version have been explicitly validated. Script compatibility is not inferred from the existence of a report.

## How to add a device

1. Read the [individual device audit guide](../docs/USER_DEVICE_AUDIT.en.md).
2. Create a dedicated folder under `reports/`, using manufacturer and model; include Android version when needed to distinguish variants.
3. Record identification, initial inventory, authorized changes, final inventory, comparison, and limitations.
4. Include only sanitized files needed to verify the conclusions.
5. Add an entry to this catalog with confirmed data and the correct status.
6. Submit the contribution through a Pull Request to the `main` branch.

### Recommended structure

The structure may be simplified when data collection is unavailable. Do not create empty files or invent results to fill the template.

```text
reports/<manufacturer>/<model>/
├── README.md                  # Summary and audit status
├── audit.md                   # Method, evidence, analysis, and limitations
├── inventory-before.json      # Inventory before changes
├── inventory-after.json       # Inventory after changes
├── comparison.json            # Before/after metrics and collection conditions
├── disabled-packages.txt      # Final state record, if applicable
├── changed-permissions.json   # Documented changes, if applicable
└── evidence/
    └── README.md              # Evidence provenance and sanitization
```

## Quality and privacy rules

1. **Real evidence:** do not publish simulated data, inferences presented as facts, or metrics without a collection method.
2. **Comparable before/after:** report dates, conditions, and commands. A single measurement does not prove an improvement caused by a change.
3. **Separate states:** distinguish installed, enabled, disabled, and uninstalled-for-user packages. A historical snapshot is not an execution list.
4. **No universal recommendations:** a package list from one model must not be applied to another model, region, or firmware.
5. **Mandatory sanitization:** remove IMEI, serial, MAC, public or identifying IP addresses, accounts, email addresses, phone numbers, tokens, keys, notifications, and personal data.
6. **Keep raw data private:** retain complete dumps locally or in private storage; publish only strictly necessary excerpts.
7. **Additive contributions:** do not delete, replace, or rewrite audits for other devices. Updates must be made in the same device folder and explain the reason for revision.
8. **Transparent validation:** explicitly mark tests not performed and inconclusive results.

## Integration workflow

```text
Local data collection
    ↓
Analysis and owner authorization
    ↓
Sanitization and review
    ↓
Fork + dedicated branch
    ↓
Pull Request to main
    ↓
Technical and privacy review
    ↓
Merge: audit added to the catalog
```

Opening a Pull Request does not guarantee approval or merge. Contributions may receive revision requests when evidence is missing, personal data is exposed, or recommendations are unsafe.

See [CONTRIBUTING.en.md](../CONTRIBUTING.en.md) for submission instructions and the [audit guide](../docs/USER_DEVICE_AUDIT.en.md) for technical details.
