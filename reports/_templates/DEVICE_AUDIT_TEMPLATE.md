# Android device audit — Manufacturer Model

> **Template:** Replace every `[placeholder]`. Delete instructions only after ensuring the required information is recorded. Do not publish raw private dumps.

## Canonical file layout required by repository

See [Audit status and homologation levels](../../docs/AUDIT_STATUS_AND_HOMOLOGATION.md) for required files per level:
- **Level 1:** `README.md`, `README.en.md`, `audit.md`, `audit.en.md`, `metrics.json`, `before/inventory.json`, `functional-tests.json`
- **Level 2:** Level 1 files + `comparison-report.md`, `comparison-report.en.md`, `after/inventory.json`, `changes/change-log.md`, `changes/change-log.en.md`, `changes/disabled-packages.txt`, `changes/removed-packages.txt`
- **Level 3:** Level 2 files + `functional-tests.json` with real executed test results
- **Level 4:** Level 3 files + homologated script with rollback and independent reviewer

## 1. Executive summary
- **Manufacturer / model / variant:** [exact identity]
- **Codename / board / product:** [values or Unknown]
- **Android / ROM / interface:** [version, API, ROM]
- **Build / security patch / region:** [values or Pending]
- **Audit date / operator:** [date / pseudonym]
- **Audit status:** [Level 0–4; see status standard]
- **Scope:** [what was assessed]
- **Out of scope:** [what was not assessed]

## 2. Authorization and safety
- Owner authorization: [explicitly recorded / pending]
- Access method and privileges: [ADB, shell, root status]
- Device modifications permitted: [explicitly scoped actions]
- Emergency stop and rollback path: [steps/evidence]
- Known risk and dependency summary: [summary]

## 3. Methodology and evidence provenance
| Evidence ID | Collection date/time | Command/tool/source | Device/build context | File path | Sanitization |
|---|---|---|---|---|---|
| E-001 | [date/time] | [command] | [build] | [path] | [actions] |

Separate **observed facts**, **technical interpretation**, and **hypotheses**.

## 4. Initial state
- Package inventory: [path]
- Enabled/disabled/uninstalled-for-user counts: [scope and counts]
- Runtime permissions/AppOps: [path or Pending]
- Storage/RAM/battery metrics: [method, conditions, results or Not measured]
- Baseline functional test matrix: [path]

## 5. Findings and package-level assessment
| Package | Evidence | Purpose/confidence | Permissions/AppOps | Dependencies | Risk | Recommendation | Reversal |
|---|---|---|---|---|---|---|---|
| [package ID] | [E-ID] | [purpose; confidence] | [observed] | [known/unknown] | [level] | [preserve/disable/remove/test] | [command/steps] |

Never generalize a package recommendation to another model/build.

## 6. Authorized actions and change log
| Action ID | Package/component | Proposed action | Owner authorization | Actual command | Result/time | Rollback |
|---|---|---|---|---|---|---|
| C-001 | [ID] | [action] | [record] | [command] | [result] | [steps] |

Only document actions actually performed as completed.

## 7. Final state and comparison
| Metric | Baseline | Final | Method/conditions | Evidence | Interpretation/limitation |
|---|---:|---:|---|---|---|
| [metric] | [value] | [value] | [method] | [E-ID] | [scope] |

Do not claim gains without comparable measured evidence.

## 8. Functional tests
| Test | Preconditions | Steps | Expected | Actual | Result | Evidence |
|---|---|---|---|---|---|---|
| Calls/SMS/data | [conditions] | [steps] | [expected] | [observed] | [Pass/Fail/Not tested] | [E-ID] |

List tests not performed and failures.

## 9. Limitations, unresolved issues, and recovery
- Pending evidence: [list]
- Known failures/limitations: [list]
- Recovery/rollback verification: [results]
- Long-term monitoring: [pending/not performed]

## 10. Privacy review
- [ ] IMEI, serial, MAC, private IP, hostname, account IDs sanitized
- [ ] Credentials, tokens, keys, and secrets removed
- [ ] Screenshots and attachments inspected
- [ ] User-installed apps and personal data excluded or pseudonymized
- [ ] Raw private data remains outside the public repository

## 11. Reproducibility and review
- Collection scripts/tools and versions: [values]
- Reproduction scope: [exact device/build only]
- Reviewer/date: [values]
- Audit status and approved scope: [Level 0–4, scope]
- PR link: [URL]

## 12. References
- [Official vendor/Android documentation]
- [Relevant source links, with access date]
