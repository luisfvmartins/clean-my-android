# Individual Android Device Audit

This guide helps every **Clean My Android** contributor prepare a Pull Request (PR), record the device state before changes, document each intervention, and produce a comparative report after optimization.

The goal is to build a cumulative public collection of technical audits that are verifiable and reproducible. Every approved Pull Request adds a new audit to the main repository without replacing existing reports.

> **Core principle:** never invent results. Every metric must state its method, collection conditions, and supporting evidence. If it cannot be measured, mark it as “Not measured” or “Inconclusive”.

## How to use this guide: AI recommended, manual execution allowed

The recommended approach is to work with an AI assistant of your choice. Clean My Android does not depend on ChatGPT, Claude, Gemini, Antigravity, or any specific provider. Choose a tool that can read the repository and, if you want direct data collection, access the computer terminal where ADB is installed.

1. Clone the repository and open its folder in your AI assistant/agent.
2. Ask it to read [AI_INSTRUCTIONS.en.md](../AI_INSTRUCTIONS.en.md) and this guide in full before starting.
3. Confirm ADB recognizes the correct device and the computer is authorized.
4. Request the initial audit in read-only mode.
5. Review findings and the change plan. The AI must explain evidence, uncertainty, risks, and rollback options.
6. Explicitly authorize each change stage. Do not give blanket permission to modify everything.
7. Follow testing, final data collection, and report preparation.
8. Review and sanitize files before publication.

**AI assists with investigation and documentation; the device owner remains responsible for authorization.** An assistant without terminal/ADB access may guide the process, but must not claim to have inspected or modified the device.

Manual execution is also allowed for users experienced with Android and ADB. Follow the same stages, evidence standards, safety rules, reversibility requirements, and documentation practices.

## 1. Recommended workflow

1. Create your own repository fork (for contributors without write access) and prepare a contribution branch.
2. Prepare a dedicated folder for the device.
3. Run the initial diagnosis without modifying the device.
4. Save inventories, metrics, logs, and screenshots.
5. Analyze packages and present a change plan.
6. Obtain explicit authorization before each group of changes.
7. Apply changes in a controlled manner and record the results.
8. Repeat initial data collection under the same conditions.
9. Generate the comparison report.
10. Review and sanitize files, push the branch to your fork, and open a Pull Request to the original repository.

## 2. Prepare your fork and contribution

### Using GitHub

1. Visit https://github.com/luisfvmartins/clean-my-android.
2. Sign in to your GitHub account.
3. Click **Fork**.
4. Select your account as the destination.
5. Keep the repository name or choose another.
6. Confirm creation.

Your fork will be available at `https://github.com/YOUR_USERNAME/clean-my-android`.

### Using GitHub CLI

With GitHub CLI installed and authenticated:

```bash
gh auth login
gh repo fork luisfvmartins/clean-my-android --clone
cd clean-my-android
git remote add upstream https://github.com/luisfvmartins/clean-my-android.git
git remote -v
```

Confirm that `origin` points to your fork and `upstream` points to the original repository.

### Privacy

The original repository is public. Do not assume your fork is private. Inventories and screenshots may reveal the model, personal apps, carrier, identifiers, notifications, and usage habits.

- Never publish IMEI, serial number, MAC addresses, tokens, credentials, accounts, or personal data.
- Review screenshots and logs before submission.
- Keep raw data locally or in a private repository.
- Include only sanitized reports and evidence necessary for review in the Pull Request.
- The PR will be submitted to the original repository for review; this does not mean it will automatically be accepted or merged.

## 3. Cumulative report structure in the main repository

The original repository maintains a collection of audits under `reports/`. Each device must have its own directory using `reports/<manufacturer>/<model>/`, following the catalog convention. Examples:

```text
reports/
├── README.md
├── motorola/
│   ├── edge-60-pro/
│   │   └── ... sanitized report and evidence ...
│   └── moto-g54-5g/
│       └── ... sanitized report and evidence ...
└── samsung/
    └── galaxy-s20-fe/
        └── ... sanitized report and evidence ...
```

**Contribution rule:** each PR must add a new device folder, or update only that same device's folder when making an identified revision. Do not replace, delete, or modify other contributors' reports. Every approved PR should expand the collection of documented devices in the main branch.

`reports/README.md` is the collection index. When adding an audit, include a link to the new report with manufacturer/model, Android/ROM version, and audit date. Do not add unverified details.

## 4. Device folder structure

Create the directory under the manufacturer's folder, using a descriptive model identifier without personal data. Example:

```text
reports/
└── motorola/
    └── edge-60-pro/
        ├── README.md
        ├── before/
        │   ├── device-info.txt
        │   ├── packages.txt
        │   ├── permissions.txt
        │   ├── appops.txt
        │   ├── users.txt
        │   ├── memory.txt
        │   ├── storage.txt
        │   ├── battery.txt
        │   ├── processes.txt
        │   ├── network.txt
        │   └── screenshots/
        ├── changes/
        │   ├── change-log.md
        │   ├── disabled-packages.txt
        │   ├── removed-packages.txt
        │   ├── permission-changes.txt
        │   └── appops-changes.txt
        ├── after/
        │   ├── device-info.txt
        │   ├── packages.txt
        │   ├── permissions.txt
        │   ├── appops.txt
        │   ├── users.txt
        │   ├── memory.txt
        │   ├── storage.txt
        │   ├── battery.txt
        │   ├── processes.txt
        │   ├── network.txt
        │   └── screenshots/
        └── comparison-report.md
```

This structure is a reference. Do not create empty files to imply that data collection occurred. Document limitations when information is unavailable.

## 5. Initial diagnosis — BEFORE

Before making any changes, identify the device and record its original state.

### 5.1 Identification

Collect, when available:

- Manufacturer, model, and codename.
- Android version, ROM/interface, and build.
- Security patch and kernel version.
- Architecture, processor, and cores.
- Total RAM and storage.
- Bootloader state and root status.
- Availability of ADB, Shizuku, and Magisk.
- Existing Android users and profiles.

Do not include IMEI, serial number, or persistent identifiers in the public report.

### 5.2 Application and package inventory

Record:

- System and user packages.
- Enabled and disabled packages.
- Package name, display name, and version.
- UID when relevant to the analysis.
- Installation path/origin, when available.
- Declared and granted permissions, separately.
- Relevant AppOps.
- Important services and components.
- Background execution and known dependencies.

### 5.3 Resources and performance

| Category | Data to collect |
|---|---|
| Hardware | Processor, cores, RAM, and storage |
| System | Android, ROM, kernel, and security patch |
| Memory | Total, used, available RAM, and memory pressure, if available |
| Storage | Total, used, and free space |
| Battery | Level, temperature, state, and available statistics |
| Processes | Relevant processes and services |
| Applications | Count by category and state |
| Network | DNS, connectivity, and configured restrictions |
| Privacy | Permissions, AppOps, and components with sensitive access |
| Security | Root, bootloader, and available integrity checks |

### 5.4 Measurement conditions

For a fair comparison, record:

- Date and time.
- Battery level.
- Whether the device was charging.
- Screen on/off state.
- Open applications.
- Time since last reboot.
- Network connection type.
- Ambient temperature, if known.
- Command or method used for each metric.

Free RAM, temperature, and battery consumption vary with usage. A single reading does not prove sustained improvement.

## 6. Screenshots

When possible, capture equivalent before/after images of:

- Phone information and Android version.
- Storage.
- Memory.
- Battery.
- Installed applications.
- Permissions and privacy.
- Network/DNS settings.
- Important device features.

Save them under `before/screenshots/` and `after/screenshots/`, using equivalent names to make comparison easier.

Screenshots must be legible, show context, and must not be manipulated to suggest results. Hide notifications, messages, accounts, phone numbers, location, and any personal data before publication.

If a screenshot cannot be captured, document the limitation.

## 7. Change log

Every change must be documented in `changes/change-log.md`, including:

| Field | What to record |
|---|---|
| Date/time | When the change occurred |
| Package | Exact package name |
| Application | Identified application |
| Previous state | Enabled, disabled, or unavailable |
| Action | Disable, uninstall for user, permission, AppOps, etc. |
| Reason | Evidence and technical justification |
| Risk | Critical, high, medium, low, or informational |
| Dependencies | Components that may be affected |
| Command | Command actually executed |
| Result | Actual command output and validation |
| Rollback | How to restore |
| Evidence | Related log or screenshot |

Do not classify a package as unnecessary based only on its name or manufacturer.

## 8. Final diagnosis — AFTER

After changes, repeat the initial data collection using the same methods and, as far as possible, the same conditions.

Check:

- Android boot and stability.
- Calls, SMS, and mobile data.
- Wi-Fi, Bluetooth, and GPS.
- Cameras, microphone, and audio.
- Push notifications and synchronization.
- Banking and authentication apps used by the owner.
- Keyboard and launcher.
- System updates.
- Replacement applications.
- Memory, storage, battery, and temperature.

Record untested features as pending.

## 9. Before/after comparison

Create `comparison-report.md` with:

1. Executive summary.
2. Device identification.
3. Audit scope.
4. Collection methods and conditions.
5. Initial state.
6. Changes performed.
7. Final state.
8. Metrics comparison.
9. Feature comparison.
10. Stability and compatibility tests.
11. Problems and rollback actions.
12. Limitations and pending items.
13. Conclusion.

Use a table such as:

| Metric | Before | After | Difference | Method / notes |
|---|---:|---:|---:|---|
| Free storage | | | | |
| RAM available | | | | |
| Battery temperature | | | | |
| Enabled packages | | | | |
| Disabled packages | | | | |
| Boot time | | | | |

Only compare measurements collected with equivalent methods and conditions. Mark unavailable data as “Not measured” or “Inconclusive”. Never invent improvements.

## 10. Review and Pull Request

Before submission:

1. Review the full diff.
2. Check JSON syntax and file paths.
3. Remove personal identifiers, credentials, and raw dumps.
4. Ensure the report describes only the identified device.
5. Preserve existing reports.
6. Update the device catalog.
7. Run the repository validation workflow.
8. Push the branch to your fork.
9. Open a Pull Request against `main`.

A Pull Request is a proposal, not an automatic approval. The maintainers may request corrections or reject unsupported, unsafe, or privacy-sensitive content.

## 11. Safety and interpretation

- Do not execute package lists copied from another device.
- Do not treat an inventory as an approved removal list.
- Do not infer telemetry solely from internet permission, analytics SDKs, or package ownership.
- Do not apply AppOps by UID without checking shared UID relationships.
- Do not use `pm clear` as a routine optimization step; it deletes app data.
- Do not perform bulk changes without individual analysis and authorization.
- Keep a recovery path available.
- Separate observed evidence, technical inference, and hypotheses.
- Clearly label unperformed tests and unresolved questions.

The scripts in this repository are read-only by default. Their limited apply functionality is not universal and must not be assumed compatible with other models or Android versions.

---

**A device report documents one specific configuration. It is not a universal debloating recipe.**
