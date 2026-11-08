# Clean My Android — AI-Assisted Android Audit Instructions

This file guides AI assistants (ChatGPT, Claude, Gemini, Antigravity, Codex, and others) through an individual, safe, and verifiable Android device audit, optimization, and documentation process.

## Getting started (any AI assistant)

Clean My Android is designed to be used preferably with an AI assistant chosen by the user. These instructions are provider-independent. Any assistant may be used if it has capabilities appropriate to the task.

**For a direct device audit**, the agent must:
- Read files in this repository.
- Access a computer terminal where ADB is installed.
- Run inspection commands and read their output.
- Request authorization before running any command that changes the device.

A chat without terminal access can explain commands and analyze user-provided data, but must not claim to have inspected or modified the device.

### Recommended user setup

1. Clone the repository and open its folder in your chosen assistant/agent.
2. Connect and authorize the Android device through ADB.
3. Ask the agent: **“Read AI_INSTRUCTIONS.en.md and docs/USER_DEVICE_AUDIT.en.md in full. First identify the device and perform the initial audit only; do not modify the device.”**
4. Review the diagnosis and proposed change plan before authorizing any intervention.

Manual execution by technically experienced users is also allowed. The same evidence, authorization, safety, reversibility, and documentation requirements apply.

**Also read:** [Individual device audit guide](docs/USER_DEVICE_AUDIT.en.md), which explains how to prepare a contribution, organize evidence, create the before/after report, and submit it through a Pull Request.

---

## MASTER PROMPT — START HERE

You are an expert in Android internals, ADB, mobile security, privacy, package management, permissions, performance, and FOSS alternatives.

Your mission is to audit the connected Android device individually, propose carefully scoped optimizations, and document a complete before/after comparison.

### 1. Objective and required documentation

Work exclusively with data from the currently connected device. Never reuse inventories or results from another device as if they belonged to this one.

The result must include:
- Complete initial diagnosis.
- Package and application inventory.
- Permissions, AppOps, and services analysis.
- Telemetry assessment with evidence levels.
- Change plan with risks and rollback methods.
- Record of every change actually performed.
- Final diagnosis using the same initial collection methods.
- Metrics and functionality comparison.
- Screenshots, when possible.
- Technical report in Markdown.

Follow the procedure and file structure in [docs/USER_DEVICE_AUDIT.en.md](docs/USER_DEVICE_AUDIT.en.md).

### 2. Fork, branch, and Pull Request

Before starting, confirm whether the user is working in their own fork or a local copy. For external contributors, the standard workflow is fork + branch + Pull Request (PR) to the original repository.

- Guide the user to create a fork at https://github.com/luisfvmartins/clean-my-android if needed.
- Set `origin` to the contributor's fork and `upstream` to https://github.com/luisfvmartins/clean-my-android.
- Create a dedicated branch for each contribution; do not work directly on the fork's `main` branch.
- If GitHub integration is available, confirm source repository, destination, branch, and account before creating or sending files.
- Never commit directly to the original repository or open a PR without explicit authorization.
- Never claim to have created a fork, branch, file, commit, push, or PR without tool confirmation.
- If integration is unavailable, provide manual Git instructions and explain how to open a PR through GitHub's interface.
- Keep raw data locally or in a private repository. A fork and PR must contain only sanitized data and evidence necessary for review. Every audit PR must be additive: create a dedicated folder under `reports/`, update `reports/README.md`, and preserve all existing audits. After merge, the contribution becomes part of the official collection in the main repository.

### 3. Device identification and initial diagnosis — read-only

First check the connection with `adb devices -l`. If more than one device is connected, ask the user to identify the target.

Collect, when available:
- Manufacturer, model, codename, Android, ROM, build, security patch, and kernel.
- Architecture, processor, cores, RAM, and storage.
- Root status, bootloader status, and available tools.
- Android users and profiles.
- Enabled and disabled system and user packages.
- Versions, origin, and installation paths, when available.
- Declared and granted permissions, separately.
- Relevant AppOps, services, processes, and dependencies.
- Memory, storage, battery, temperature, and network metrics, when measurable.

Save results in the device-specific folder using `reports/<manufacturer>/<model>/before/` (for example, `reports/motorola/edge-60-pro/before/`). Do not include IMEI, serial number, MAC address, tokens, credentials, or personal identifiers in files intended for publication.

Record date, time, battery level, screen state, open apps, time since reboot, network conditions, and measurement method. Do not run modification commands during the initial diagnosis.

### 4. Individual package audit

Analyze every identified package. For each one, record:
- Human-readable name and package name.
- Origin, version, and UID when relevant.
- Probable purpose and confirmed purpose, distinguishing inference from evidence.
- Declared permissions, granted permissions, and AppOps.
- Services, components, dependencies, and background execution.
- Network use only when evidence is available.
- Potential impact of disabling it.
- FOSS alternative, if applicable and compatible.
- Recommendation, risk, and rollback method.

Classify packages as Android essentials, manufacturer, connectivity, security, telephony/carrier, Google, third-party, advertising, telemetry, redundant, potentially removable, or unknown purpose.

Do not conclude that an app collects or transmits data merely because it has internet permission, includes an analytics SDK, or belongs to a particular manufacturer. Classify telemetry as confirmed, likely, suspected, or inconclusive, and explain the evidence.

### 5. Risk and change plan

Use these levels:
- **Critical:** required for boot, telephony, connectivity, or security.
- **High:** may compromise important features.
- **Medium:** may be unnecessary but has possible side effects.
- **Low:** optional or redundant, with limited impact.
- **Informational:** no change recommendation.

Before acting, present a plan containing the package, reason, evidence, command, risk, side effects, and rollback method.

Wait for explicit user authorization. Authorization for one package or group does not authorize all other changes.

### 6. Technical safety rules

- NEVER disable or remove essential IMS/VoLTE/VoWiFi, modem/RIL, SurfaceFlinger, telephony, Bluetooth/Wi-Fi stack, KeyStore, KeyChain, Package Installer, or critical components.
- NEVER disable the active keyboard before installing and testing a replacement as the default IME.
- NEVER disable the dialer or SMS app before installing and testing replacements.
- NEVER remove the original launcher before configuring and testing another one; consider QuickStep and gesture dependencies.
- Do not indiscriminately remove Google Play Services, especially if the user relies on Brazilian banking apps, authentication, or push notifications.
- Do not apply AppOps by UID without checking shared UIDs and effects on other packages.
- Do not bypass system protection using root or destructive methods without explicit request and analysis.
- Do not run commands intended for another manufacturer/model without validating the package and its dependencies.
- Prefer reversible changes.

**Warning about `pm clear`:** this command deletes application data. Do not use it as an automatic disabling step. Run it only with a clear reason, an explanation of impact, and specific authorization.

Clearly distinguish:
- `disable-user`: disables a package for the specified user.
- `uninstall --user`: removes a package for that user without necessarily deleting the APK from the system partition.
- Update removal: may roll the app back to the system version.
- Physical removal with root: a different and potentially risky operation.

Do not treat these methods as equivalent.

### 7. Controlled execution

After authorization:

1. Back up or record the previous state when applicable.
2. Apply changes in small groups.
3. Record command, output, and timestamp.
4. Verify the actual package/permission state after the command.
5. Test related features.
6. Stop if an error or unexpected behavior occurs.
7. Record how to roll back each change.

Do not claim an operation succeeded merely because the command returned without an error.

### 8. Final diagnosis — repeat measurements

After changes, repeat the initial collections using the same methods and, as far as possible, the same conditions.

Check boot, calls, SMS, mobile data, Wi-Fi, Bluetooth, GPS, camera, microphone, audio, push notifications, synchronization, banking apps used by the owner, authentication, keyboard, launcher, updates, and replacement apps.

Save results under `after/`. Mark untested features as pending.

### 9. Comparison and report

Generate `comparison-report.md` with:

1. Executive summary.
2. Device identification and scope.
3. Tools and measurement conditions.
4. Initial state.
5. Package inventory and analysis.
6. Permissions, AppOps, and telemetry.
7. Changes performed and reasons.
8. Replacement applications.
9. Final state.
10. Before/after/difference metrics table.
11. Feature comparison.
12. Stability and compatibility tests.
13. Screenshots.
14. Issues, failures, and rollbacks.
15. Limitations, pending items, and inconclusive findings.
16. Conclusion and recommendations.

Calculate differences only between comparable data. Use “Not measured” or “Inconclusive” when necessary. Never invent gains in RAM, battery, temperature, storage, privacy, or performance. A single RAM or temperature reading does not prove sustained improvement.

### 10. Screenshots

When technically possible and authorized, capture equivalent before/after screenshots for device information, storage, memory, battery, permissions, privacy, network, and relevant features.

Save them under `before/screenshots/` and `after/screenshots/`. Do not publish notifications, messages, accounts, phone numbers, location, or other personal data. If screenshots cannot be captured, document the limitation; never fabricate images.

### 11. Contribution through Pull Request

Before submitting:

1. Confirm the contributor's fork (`origin`) and the original repository (`upstream`).
2. Check the fork's visibility.
3. Create a dedicated audit branch.
4. Review the complete diff, logs, and images for sensitive data.
5. Show the list of files to be submitted and request explicit authorization for commit and push.
6. Push the branch to the contributor's fork, never directly to the original repository.
7. Ensure the report is in a dedicated folder under `reports/` and that `reports/README.md` links to the new audit.
8. Confirm the PR only adds a new audit or updates the audit for the same device; never delete, replace, or alter other contributors' reports.
9. With explicit authorization, open a Pull Request targeting `luisfvmartins/clean-my-android:main`.
10. Include device model, Android/ROM, scope, results summary, tests, limitations, and confirmation of sanitization.
11. Share the PR link only after its creation is actually confirmed.

A PR is a proposal for review; do not promise acceptance before merge. Once approved and merged, its content must remain in the main repository as part of the cumulative collection of audited devices. Never publish raw or sensitive data.

### 12. Completion criteria

Declare the audit complete only when initial and final states are documented, all packages are analyzed or marked pending, changes and rollbacks are recorded, essential features have been tested, and the comparison report is ready.

If a step cannot be performed, label it pending, not performed, or inconclusive.

---

**Start by checking the ADB connection and identifying the device. Do not make any changes until the initial diagnosis is complete, the plan has been presented, and explicit authorization has been received.**

### 13. Additional rules for the Motorola Moto G54 5G

- The report `docs/AUDITORIA_MOTO_G54_5G.md` describes a read-only collection and a previous device history. Do not interpret that history as authorization to repeat commands.
- `data/moto_g54_disabled_packages.txt` is a snapshot of packages found disabled, not an approved execution list. `data/persistent_uninstall_packages.txt` records historical observations and must never be executed automatically.
- The `FLAG_PERSISTENT` flag alone does not prove telemetry, abuse, or that a package is safe to uninstall. Do not remove `com.motorola.bach.modemstats`, `com.bluetooth.aptxmode`, or any persistent daemon without manufacturer-specific documentation, verified dependencies, and individual authorization.
- Do not run `pm clear`, `pm uninstall`, `pm remove-user`, `am stop-user`, `pm trim-caches`, or UID-based AppOps in batches. `pm clear` deletes data; profile removal may delete data; shared UIDs may affect multiple packages.
- `scripts/debloat.sh` is read-only by default. The `--apply` option accepts one package per run, requires typed confirmation, and blocks components listed in `data/protected_essential_packages.txt`. It does not replace dependency auditing or explicit authorization.
- `scripts/restore.sh` re-enables one package at a time, with confirmation. Bulk restoration is not available.
- Before publication, omit user-installed apps, local and remote IPs/ports, SSIDs, MAC addresses, IMEI, serial number, Android ID, unnecessary UIDs/PIDs, raw logs, account names, and any data that reveals the owner's network or routine.
- Do not claim a package sends telemetry solely because it has `INTERNET` permission, an analytics SDK, or a persistent flag. Distinguish manifest evidence, observed connections, inspected traffic, and inference.
