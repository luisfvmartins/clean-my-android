# Changelog — Clean My Android

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [Unreleased]

### Added
- **PT-7 (Process and Governance):** Creation of `SECURITY(.pt-BR).md`, `.github/CODEOWNERS`, retroactive `CHANGELOG(.pt-BR).md` derived strictly from PRs #1–#47, and `request_audit_review.yml` issue template. Enforcement of Conventional Commits and Squash and Merge in `CONTRIBUTING(.pt-BR).md`.
- **PT-6 (Verifiable Classifications):** Creation of `docs/CLASSIFICATION_METHOD(.pt-BR).md` establishing a 5-tier evidence hierarchy (AOSP, OEM/SoC, manifest/dumpsys, on-device testing, secondary community) and confidence levels (`high`, `medium`, `low`). Published 30-package sampling self-audit in `docs/SELF_AUDIT_2026-11-09(.pt-BR).md` using reproducible seed `20261109` in `scripts/sample_self_audit.py`.
- **PT-5 (Canonical Report Layout):** Established uniform directory layout under `reports/` with `audit(.en).md`, `comparison-report(.en).md`, `metrics.json`, `functional-tests.json`, `before/`, `after/`, `changes/`, and `evidence/`. Automated homologation level enforcement in `scripts/validate_repository.py` backed by `tests/test_canonical_layout.py`.
- **PT-3 (Testing, CI, and Portability):** Expanded test suite to 44 tests in `tests/test_adb_scripts.py` covering 100% of exit codes and individually validating all 44 protected essential packages. Weekly GitHub Actions updates configured via `.github/dependabot.yml`. Platform compatibility and limitations documented in `docs/PLATFORMS(.pt-BR).md`.
- **PT-2 (Script Safety, Logging, and Snapshot):** Replaced `mapfile` with Bash 3.2-compatible loop. Centralized bilingual message catalog (`scripts/lib/messages.sh` with `CMA_LANG`). Sanitized JSONL action logging with rollback commands. Data-driven apply gate (`data/apply_support.tsv`). Read-only device snapshot utility with pre-write sanitization gate (`scripts/snapshot.sh`). Change list verifier (`scripts/check_change_lists.py`). Removed protected packages from general lists in `data/`.
- **PT-1 (Claims and Metrics with Status):** Automated validator for absolute and causal claims (`scripts/check_claims.py`) backed by qualified allowlist (`data/claims_allowlist.json`). Strict canonical schema for `metrics.json` requiring `kind`, `status`, `method`, and `evidence`.
- **PT-4 (Verifiable Sanitization):** Automated sensitive data scanner (`scripts/check_sanitization.py`) checking IMEI via Luhn algorithm, MEID, MAC addresses, phone numbers, and undocumented private IP addresses. Audit trail documented in `docs/SANITIZATION_LOG.md`.

---

## [0.1.0] — 2026-11-08

Initial public consolidation release of forensic Android device audits and safety-first debloat automation.

### Summary of merged Pull Requests (#1 to #47)

#### Device Reports and Forensic Audits
- **Motorola Moto G54 5G (`cancunf` · XT2343-1):** Comprehensive mapping of 462 factory components across 7 detailed batch reports, and safe execution script support (PRs #1, #15, #16, #17, #19, #20, #21, #22, #23, #24, #29).
- **Motorola Edge 60 Pro (`cybert` · XT2507-1):** Retrospective forensic audit of 501 factory components, post-debloat count reconciliation, conflict documentation with protected component list, and redaction of third-party identifiers (PRs #2, #25, #30, #31, #32).
- **Motorola Edge 60 Fusion (`scout` · XT2503-1):** Comprehensive technical audit of 486 components on Android 16 (API 36), deactivation of 87 bloatwares, AppOps sandboxing for 5 non-disable system components, and validated functional migration to FOSS suite with RoleManager (PR #33).
- **Samsung Galaxy A30s (`a30s` · SM-A307GT):** Technical audit and debloat in two batches covering 48 modified components, mitigation of PDF printing loss (printspooler), and OEM telemetry sandboxing (PRs #35, #36).

#### Directory Structure, Localization, and Documentation
- Reorganized report directory hierarchy by manufacturer and model under `reports/<manufacturer>/<model>/` (PRs #9, #12).
- Complete English (EN) and Brazilian Portuguese (PT-BR) localization of all READMEs and audit batches (PRs #13, #14, #27, #40).
- Guidance for AI assistants (`AI_INSTRUCTIONS`) and contribution standards (`CONTRIBUTING`) (PRs #11, #25, #27, #34, #39).
- Established status framework and technical homologation levels 0 to 4 (`docs/AUDIT_STATUS_AND_HOMOLOGATION`) with standardized templates (PR #38).
- Semantic audit aligning technical terminology and claims across all documentation (PRs #41, #43, #44).

#### Quality Assurance, Validation, and CI
- Created and expanded repository validator `scripts/validate_repository.py` enforcing JSON syntax, local Markdown links, shell syntax, and protected package integrity (PRs #10, #28, #45, #46).
- Implemented initial mocked ADB testing framework in `tests/test_adb_scripts.py` verifying device scripts without requiring physical hardware (PR #47).
- Pinned GitHub Actions workflows by immutable commit SHA with minimal permissions (PR #46).
