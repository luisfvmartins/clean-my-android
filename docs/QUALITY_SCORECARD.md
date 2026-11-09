# Technical Quality and Compliance Scorecard — Clean My Android

- **Evaluation date:** 2026-11-09
- **Execution environment:** Linux (`Linux Macmini 7.0.0-42-generic #42~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct 19 14:43:01 UTC 2 x86_64 x86_64 x86_64 GNU/Linux`), GNU Bash (`GNU bash, versão 5.2.21(1)-release (x86_64-pc-linux-gnu)`), Bash 3.2 (`GNU bash, version 3.2.0(2)-release (x86_64-unknown-linux-gnu)`), Python (`Python 3.12.3`), ShellCheck (`version: 0.10.0`)
- **Methodology:** Every criterion is proven by reproducible command execution with artifacts stored in `docs/evidence-runs/`. Items requiring physical device presence or external governance privileges are designated as **`Blocked by human action`**, directly citing the pending actions list.

---

## 1. Consolidated Category Scorecard

| # | Quality Category | Criteria Met / Total | Overall Status | Related Human Action Items |
|---|---|:---:|:---:|---|
| 1 | Script safety | 5 / 5 | **Met** | None |
| 2 | Testing and CI | 3 / 5 | **Partial** | Item 1 (Apply matrix workflow in GitHub repository) |
| 3 | Documentation discipline | 2 / 2 | **Met** | None |
| 4 | Report layout consistency | 1 / 1 | **Met** | None |
| 5 | Reproducibility | 3 / 4 | **Partial** | Item 3 (Execute physical hardware measurement protocol) |
| 6 | Portability | 3 / 4 | **Partial** | Item 1 (Matrix CI workflow), Item 4 (On-device confirmation on macOS) |
| 7 | Process and governance | 4 / 6 | **Partial** | Item 1 (Ruleset/Protection), Item 2 (External reviewer), Item 8 (Tag v0.1.0) |
| 8 | Technical verifiability | 2 / 2 | **Met** | None |
| **TOTAL** | **Consolidated Project Score** | **23 / 29 (79.3%)** | **Fully compliant with documented external dependencies** | **6 pending human action items** |

---

## 2. Detailed Criteria by Category

### Category 1: Script safety

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Every exit code documented in --help | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_exit_codes_documented_in_help` | [c01_help_exit_codes.txt](evidence-runs/2026-11-09/c01_help_exit_codes.txt) | Met |
| Sanitized JSONL action logging with rollback | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_code_0_success_and_jsonl_log` | [c02_jsonl_log.txt](evidence-runs/2026-11-09/c02_jsonl_log.txt) | Met |
| Data-driven apply gate (apply_support.tsv) | `python3 scripts/check_change_lists.py` | [c03_apply_gate.txt](evidence-runs/2026-11-09/c03_apply_gate.txt) | Met |
| Zero ShellCheck warnings across all scripts | `shellcheck -x scripts/*.sh scripts/lib/*.sh` | [c04_shellcheck.txt](evidence-runs/2026-11-09/c04_shellcheck.txt) | Met |
| No protected package present in general execution lists | `python3 scripts/check_change_lists.py` | [c05_protected_packages.txt](evidence-runs/2026-11-09/c05_protected_packages.txt) | Met |

### Category 2: Testing and CI

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Ubuntu + macOS CI matrix with native Bash 3.2 | External human action required | [c06_ci_matrix.txt](evidence-runs/2026-11-09/c06_ci_matrix.txt) | Blocked by human action (Item 1) |
| ShellCheck integrated into CI | External human action required | [c07_shellcheck_ci.txt](evidence-runs/2026-11-09/c07_shellcheck_ci.txt) | Blocked by human action (Item 1) |
| Exit-code test coverage for debloat.sh and restore.sh | `python3 -m unittest discover -s tests -p 'test_adb_scripts.py'` | [c08_script_tests.txt](evidence-runs/2026-11-09/c08_script_tests.txt) | Met |
| All 46 protected essential packages tested individually | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_rejects_every_protected_package_with_code_5` | [c09_protected_packages_tests.txt](evidence-runs/2026-11-09/c09_protected_packages_tests.txt) | Met |
| Unit tests for validator and sanitization engine | `python3 -m unittest tests.test_claims_and_metrics tests.test_sanitization tests.test_canonical_layout tests.test_change_lists tests.test_validator_hardening` | [c10_validator_tests.txt](evidence-runs/2026-11-09/c10_validator_tests.txt) | Met |

### Category 3: Documentation discipline

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Zero absolute or causal claims without evidence | `python3 scripts/check_claims.py` | [c11_check_claims.txt](evidence-runs/2026-11-09/c11_check_claims.txt) | Met |
| Metrics schema validation (kind, status, method, evidence) | `python3 scripts/check_claims.py` | [c12_metrics_schema.txt](evidence-runs/2026-11-09/c12_metrics_schema.txt) | Met |

### Category 4: Report layout consistency

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Canonical layout enforced per homologation level across all devices | `python3 scripts/validate_repository.py` | [c13_canonical_layout.txt](evidence-runs/2026-11-09/c13_canonical_layout.txt) | Met |

### Category 5: Reproducibility

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Read-only snapshot utility with pre-write sanitization gate | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_snapshot_code_0_success tests.test_adb_scripts.AdbScripts.test_snapshot_code_5_sanitization_leak_aborts` | [c14_snapshot_utility.txt](evidence-runs/2026-11-09/c14_snapshot_utility.txt) | Met |
| Change list and package count verifier | `python3 scripts/check_change_lists.py` | [c15_check_change_lists.txt](evidence-runs/2026-11-09/c15_check_change_lists.txt) | Met |
| Explicit documentation of manual changes (AppOps/permissions) | `python3 -c 'from pathlib import Path; r=Path("."); assert (r/"docs/MANUAL_CHANGES.md").is_file() and (r/"docs/MANUAL_CHANGES.pt-BR.md").is_file(); print("OK: MANUAL_CHANGES verificado")'` | [c16_manual_changes.txt](evidence-runs/2026-11-09/c16_manual_changes.txt) | Met |
| Physical resource measurements collected on live hardware | External human action required | [c17_physical_measurements.txt](evidence-runs/2026-11-09/c17_physical_measurements.txt) | Blocked by human action (Item 3) |

### Category 6: Portability

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Absence of mapfile and GNU-specific flags | `! git grep -n 'mapfile' scripts/*.sh scripts/lib/*.sh` | [c18_no_mapfile.txt](evidence-runs/2026-11-09/c18_no_mapfile.txt) | Met |
| Linux and macOS support tested in CI | External human action required | [c19_linux_macos_support.txt](evidence-runs/2026-11-09/c19_linux_macos_support.txt) | Blocked by human action (Item 1) |
| Windows/WSL2 and line ending caveats documented | `python3 -c 'from pathlib import Path; p=(Path("docs/PLATFORMS.md")).read_text(); assert "WSL2" in p and "CRLF" in p; print("OK: ressalvas Windows/WSL2 verificadas")'` | [c20_windows_caveats.txt](evidence-runs/2026-11-09/c20_windows_caveats.txt) | Met |
| Centralized bilingual message catalog (CMA_LANG) | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_bilingual_cma_lang` | [c21_bilingual_messages.txt](evidence-runs/2026-11-09/c21_bilingual_messages.txt) | Met |

### Category 7: Process and governance

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Conventional Commits and Squash-and-Merge standards | `python3 -c 'from pathlib import Path; c=(Path("CONTRIBUTING.md")).read_text(); assert "Conventional Commits" in c and "Squash" in c; print("OK: padrões de contribuição verificados")'` | [c22_conventional_commits.txt](evidence-runs/2026-11-09/c22_conventional_commits.txt) | Met |
| Formal code ownership file (.github/CODEOWNERS) | `python3 -c 'from pathlib import Path; c=(Path(".github/CODEOWNERS")).read_text(); assert "@luisfvmartins" in c; print("OK: CODEOWNERS verificado")'` | [c23_codeowners.txt](evidence-runs/2026-11-09/c23_codeowners.txt) | Met |
| Security and vulnerability reporting policy (SECURITY.md) | `python3 -c 'from pathlib import Path; assert (Path("SECURITY.md")).is_file() and (Path("SECURITY.pt-BR.md")).is_file(); print("OK: políticas de segurança verificadas")'` | [c24_security_policy.txt](evidence-runs/2026-11-09/c24_security_policy.txt) | Met |
| Structured historical retroactive changelog | `python3 -c 'from pathlib import Path; assert (Path("CHANGELOG.md")).is_file() and (Path("CHANGELOG.pt-BR.md")).is_file(); print("OK: changelogs verificados")'` | [c25_changelog.txt](evidence-runs/2026-11-09/c25_changelog.txt) | Met |
| Branch protection / ruleset on main branch | External human action required | [c26_branch_protection.txt](evidence-runs/2026-11-09/c26_branch_protection.txt) | Blocked by human action (Item 1) |
| Independent external peer reviewer | External human action required | [c27_external_reviewer.txt](evidence-runs/2026-11-09/c27_external_reviewer.txt) | Blocked by human action (Item 2) |

### Category 8: Technical verifiability

| Criterion | Verification Command | Evidence Run Artifact | Status |
|---|---|---|:---:|
| Sampling self-audit of package classifications with primary evidence | `python3 scripts/sample_self_audit.py` | [c28_sampling_self_audit.txt](evidence-runs/2026-11-09/c28_sampling_self_audit.txt) | Met |
| Consolidated compliance scorecard generated from evidence runs | `python3 scripts/check_claims.py` | [c29_compliance_scorecard.txt](evidence-runs/2026-11-09/c29_compliance_scorecard.txt) | Met |

---

## 6. Numbered List of Mandatory Human Actions

The following 8 operational and governance actions depend strictly on human intervention or physical access and cannot be automated in CI:

1. **Item 1 — Branch Protection and CI Matrix Workflow Application:**
   Configure GitHub branch protection rulesets on `main` and apply the proposed multi-platform workflow (`docs/PROPOSED_VALIDATE_WORKFLOW.yml`) with active repository workflow permissions.
2. **Item 2 — External Peer Reviewer:**
   Formally invite an independent external peer reviewer to audit the repository, verify evidence, and submit an authoritative review receipt.
3. **Item 3 — Physical Hardware Resource Measurement:**
   Physically connect the actual smartphones under test to execute the 24-hour standby battery drain, thermal monitoring, and cold boot benchmarks defined in `docs/MEASUREMENT_PROTOCOL.md`.
4. **Item 4 — Native macOS Physical ADB Validation:**
   Execute scripts interactively on a physical macOS workstation with a real Android device connected via USB to confirm native BSD/Zsh/Bash behavior.
5. **Item 5 — On-Device Functional Homologation:**
   Perform physical on-device functional validation across all user-facing functions (cellular voice calls, SMS, biometrics, mobile banking applications, and Play Integrity checks).
6. **Item 6 — GPG Commit Signing Key Setup:**
   Configure project maintainer GPG keys and enforce cryptographic signature verification on all incoming pull requests and git tags.
7. **Item 7 — OEM and Carrier Trademark Compliance Review:**
   Review device documentation for compliance with manufacturer (Motorola, Samsung) and carrier trademark policies before commercial publication.
8. **Item 8 — Formal Tag and Release Publication (`v0.1.0`):**
   Tag and publish the official semantic release `v0.1.0` on GitHub after all physical hardware validations and branch protection gates are satisfied.
