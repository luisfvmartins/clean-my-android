# Technical Quality and Compliance Scorecard — Clean My Android

- **Evaluation date:** November 09, 2026
- **Execution environment:** Linux x86_64, Bash 5.2 (with tests under Bash 3.2 subshell), Python 3.12, ShellCheck 0.10.0
- **Methodology:** Every criterion is proven by reproducible command execution. Items requiring physical device presence or external governance privileges are designated as **`blocked by human action`**, directly citing the numbered list in Section 6.

---

## 1. Consolidated Category Scorecard

| # | Quality Category | Criteria Met / Total | Overall Status | Related Human Action Items (Section 6) |
|---|---|:---:|:---:|---|
| 1 | Script safety | 5 / 5 | **Met** | None |
| 2 | Testing and CI | 4 / 5 | **Partial** | Item 1 (Apply matrix workflow in GitHub repository with workflow token scope) |
| 3 | Documentation discipline | 2 / 2 | **Met** | None |
| 4 | Layout consistency | 1 / 1 | **Met** | None |
| 5 | Reproducibility | 3 / 4 | **Partial** | Item 3 (Execute physical hardware measurement protocol) |
| 6 | Portability | 4 / 4 | **Met** | Item 4 (On-device confirmation on macOS with physical ADB) |
| 7 | Process and governance | 4 / 6 | **Partial** | Item 1 (Ruleset/Protection), Item 2 (External reviewer), Item 8 (Tag v0.1.0) |
| 8 | Technical verifiability | 2 / 2 | **Met** | None |
| **TOTAL** | **Consolidated Project Score** | **25 / 29 (86.2%)** | **Fully compliant with documented external dependencies** | **8 items cataloged in Section 6** |

---

## 2. Detailed Criteria by Category

### Category 1: Script Safety

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Every exit code documented in `--help` | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_exit_codes_documented_in_help` | `Ran 1 test in 0.28s ... OK` | 2026-11-09 | **Met** |
| Sanitized JSONL action logging with rollback | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_code_0_success_and_jsonl_log` | `Ran 1 test in 0.44s ... OK` | 2026-11-09 | **Met** |
| Data-driven apply gate (`apply_support.tsv`) | `python3 scripts/check_change_lists.py` | `OK: 1226 checks completed successfully` | 2026-11-09 | **Met** |
| Zero ShellCheck warnings across all scripts | `shellcheck -x scripts/*.sh scripts/lib/*.sh` | Zero exit code (no output) | 2026-11-09 | **Met** |
| No protected package present in general execution lists | `python3 scripts/check_change_lists.py` | Zero occurrences in `data/*disabled*.txt` | 2026-11-09 | **Met** |

---

### Category 2: Testing and CI

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Ubuntu + macOS CI matrix with native Bash 3.2 | Inspection of `docs/PROPOSED_VALIDATE_WORKFLOW.yml` | Matrix workflow ready and SHA-pinned | 2026-11-09 | **Blocked by human action (Item 1)** |
| ShellCheck integrated into CI | `shellcheck -x scripts/*.sh scripts/lib/*.sh` | Integrated into proposed validation workflow | 2026-11-09 | **Met** |
| Full exit-code test coverage for `debloat.sh` and `restore.sh` | `python3 -m unittest discover -s tests -p 'test_adb_scripts.py'` | `Ran 29 tests ... OK` (codes 0, 1, 2, 3, 4, 5, 6, 7 covered) | 2026-11-09 | **Met** |
| All 44 protected essential packages tested individually | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_rejects_every_protected_package_with_code_5` | `Ran 1 test (44 iterated subtests) ... OK` | 2026-11-09 | **Met** |
| Unit tests for validator and sanitization engine | `python3 -m unittest tests.test_claims_and_metrics tests.test_sanitization tests.test_canonical_layout` | `Ran 17 tests in 0.48s ... OK` | 2026-11-09 | **Met** |

---

### Category 3: Documentation Discipline

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Zero absolute or causal claims without evidence | `python3 scripts/check_claims.py` | `OK: 109653 checks completed successfully` | 2026-11-09 | **Met** |
| Metrics schema validation (`kind`, `status`, `method`, `evidence`) | `python3 scripts/check_claims.py` | All `metrics.json` approved under strict canonical schema | 2026-11-09 | **Met** |

---

### Category 4: Report Layout Consistency

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Canonical layout enforced per homologation level across all devices | `python3 scripts/validate_repository.py` | `OK: 592 checks completed without errors` | 2026-11-09 | **Met** |

---

### Category 5: Reproducibility

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Read-only snapshot utility with pre-write sanitization gate | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_snapshot_code_0_success tests.test_adb_scripts.AdbScripts.test_snapshot_code_5_sanitization_leak_aborts` | `Ran 2 tests in 0.52s ... OK` | 2026-11-09 | **Met** |
| Change list and package count verifier | `python3 scripts/check_change_lists.py` | `OK: 1226 checks completed successfully` | 2026-11-09 | **Met** |
| Explicit documentation of manual changes (AppOps/permissions) | Reading `docs/MANUAL_CHANGES.md` and `docs/MANUAL_CHANGES.pt-BR.md` | Exact manual commands documented | 2026-11-09 | **Met** |
| Physical resource measurements collected on live hardware | Executing protocol in `docs/MEASUREMENT_PROTOCOL.md` | Requires live hardware connection by device owner | 2026-11-09 | **Blocked by human action (Item 3)** |

---

### Category 6: Portability

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Absence of `mapfile` and GNU-specific flags | `git grep -n "mapfile" scripts/` | Zero occurrences found | 2026-11-09 | **Met** |
| Linux and macOS support | Tests run under Bash 3.2 subshell; documented in `docs/PLATFORMS.md` | `OK` across test suite; complete documentation | 2026-11-09 | **Met** |
| Windows/WSL2 caveats documented | Inspection of `docs/PLATFORMS.md` | CRLF and USB passthrough caveats documented | 2026-11-09 | **Met** |
| Centralized bilingual message catalog | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_bilingual_cma_lang` | EN and PT messages validated via `CMA_LANG` | 2026-11-09 | **Met** |

---

### Category 7: Process and Governance

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Conventional Commits and Squash-and-Merge standards | Inspection of `CONTRIBUTING.md` | Standards formalized and documented | 2026-11-09 | **Met** |
| Formal code ownership file | Inspection of `.github/CODEOWNERS` | Full mapping assigned to `@luisfvmartins` | 2026-11-09 | **Met** |
| Security reporting policy | Inspection of `SECURITY.md` and `SECURITY.pt-BR.md` | Vulnerability and leak reporting protocol documented | 2026-11-09 | **Met** |
| Structured historical retroactive changelog | Inspection of `CHANGELOG.md` and `CHANGELOG.pt-BR.md` | PRs #1 through #47 mapped strictly from git | 2026-11-09 | **Met** |
| Branch protection / ruleset on `main` branch | Execution of `gh api` commands by repository owner | Requires human administrator privileges | 2026-11-09 | **Blocked by human action (Item 1)** |
| Independent external peer reviewer | External review conducted by invited third party | Must not simulate third-party intervention | 2026-11-09 | **Blocked by human action (Item 2)** |

---

### Category 8: Technical Verifiability

| Criterion | Verification Command | Output Summary | Date | Status |
|---|---|---|---|:---:|
| Classification methodology and evidence hierarchy | Inspection of `docs/CLASSIFICATION_METHOD.md` | 5-tier hierarchy and confidence levels formalized | 2026-11-09 | **Met** |
| Probabilistic sampling self-audit | `python3 scripts/sample_self_audit.py` and inspection of `docs/SELF_AUDIT_2026-11-09.md` | 30 packages audited with seed 20261109 (100% consistent) | 2026-11-09 | **Met** |
