# Package-by-package audit — Clean My Android

## Exhaustive coverage
Build a master inventory of every detected package name, including components not visible in the launcher: AOSP/system, OEM, Google, carrier, preloaded/user-installed third-party, modules/APEX, overlays, services, and headless components. One individual row per package; grouping only in summaries. Reconcile total inventoried = analyzed + pending. Do not omit packages because they appear uninteresting. Never fabricate fields: mark unknown, not collected, or inconclusive. Never reuse evidence across models, variants, builds, ROMs, or Android users.

## Required per-package inspection
Record when available: package name, label, version/versionCode, UID/shared UID; state per user/profile; install source/path/partition, separating observation from inference; declared components (activities/services/receivers/providers/jobs/intent filters); manifest, runtime-granted, and special permissions separately; AppOps, mode and package/UID scope; persistent services, startup, jobs, alarms, background execution; direct/indirect dependencies (framework, APEX, overlays, OEM APIs, telephony, IMS, GMS/FCM/Play Integrity, biometrics, camera, audio, location, launcher/QuickStep); sensitive access and rationale; network/telemetry evidence; relation to owner-used apps/functions; sanitized commands/sources/evidence.

INTERNET permission, analytics SDK, manufacturer name, DNS-listed domain, or privacy policy do not prove actual transmission. Do not access private app content or intercept protected traffic without authorization and scope.

## Mandatory matrix — one row per package name
Required fields: package name; label/version/UID; manufacturer/source and evidence; category; individual function and confidence; state per user; permissions (manifest/runtime/special); AppOps (operation, mode, scope, shared UID); components/services; dependencies and confidence; sensitive data/rationale; telemetry (confirmed/likely/suspected/inconclusive/not observed in scope), method and limits; FOSS alternative/package name/compatibility/migration or N/A rationale; recommendation; rationale; risk; functional impact; preconditions; model/build-specific command; validation; rollback; confidence; evidence IDs, sources, URLs. Mark N/A or unknown explicitly, never leave fields blank.

## Decision categories
- KEEP — essential/protected: boot, framework, System UI, Package Manager/Installer, KeyStore/KeyChain, SELinux, modem/RIL, IMS/VoLTE/VoWiFi, calls/SMS/emergency, Wi-Fi/Bluetooth, audio, camera, biometrics, updates, launcher/QuickStep, active keyboard.
- KEEP — owner-used/requested functions, including banking/authentication and dependencies.
- REVIEW PERMISSIONS — sensitive access without confirmed need; assess impact before revocation.
- MONITOR / INSUFFICIENT EVIDENCE — unclear function/dependency/activity.
- REVERSIBLE RESTRICTION CANDIDATE — only after dispensability/dependencies confirmed, with plan and tests.
- UNINSTALL-FOR-USER CANDIDATE — last resort, individual authorization, backup/rollback and testing.
“Bloatware” is not sufficient evidence or rationale.

## Telemetry evidence levels
Confirmed: traffic/data directly observed and validly attributed, method described. Likely: corroborating indicators but insufficient direct proof. Suspected: limited indicator. Inconclusive: ambiguous/insufficient. Not observed in scope: not found during collection, not a claim it never occurs. Cite reliable Android/AOSP, official OEM, source-code, or manifest sources with title, URL, access date; separate observation, documentation, and hypothesis.

## Required files
1. package-audit.csv/tsv: complete matrix, one row per package.
2. package-audit.md: detailed alphabetical individual analysis, no omissions.
3. package-summary.md: counts by category/state/recommendation/risk and coverage.
4. change-plan.md: proposal only, with preconditions, commands, impact, tests, rollback.
5. Sanitized evidence/source register.
6. Before/after report after authorized execution, distinguishing proposed from performed actions.

If context/technical limits prevent complete coverage, state the limit, enumerate pending packages, and continue in batches. Never claim full coverage without reconciliation. Initial audit is read-only; wait for explicit authorization before any action. Approval for one package/group does not authorize others.

## Manufacturer scope and cross-OEM contamination prevention

The audit prompt and matrix are generic. Identify manufacturer/model/variant/Android/ROM/build from evidence before any OEM research. This device's ADB inventory is the primary source. Consult OEM-specific packages and documentation only for the identified manufacturer; Samsung references must not guide Motorola audits, nor Motorola guide Samsung, and so on. Never treat a reference package as installed or removable without confirming it in the inventory. Keep OEM lists in separate references labeled by model/build. Unknown packages remain pending/inconclusive. AOSP components must also be validated on the actual build.

