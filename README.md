<div align="center">

# Clean My Android

**Technical Android audits, careful debloating, and privacy documentation for Android devices.**

[![Android](https://img.shields.io/badge/Android-audited%20devices-3DDC84?logo=android&logoColor=white)](reports/README.md)
[![ADB](https://img.shields.io/badge/ADB-required-3C78A8)](https://developer.android.com/tools/adb)
[![Root](https://img.shields.io/badge/Root-not%20required-2E8B57)](docs/USER_DEVICE_AUDIT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Validation](https://github.com/luisfvmartins/clean-my-android/actions/workflows/validate.yml/badge.svg?branch=main)](https://github.com/luisfvmartins/clean-my-android/actions/workflows/validate.yml)

[Get started](#get-started-ai-assistant-recommended) · [How it works](#how-it-works) · [Audited devices](reports/README.md) · [Statistics](docs/ESTATISTICAS.en.md) · [Contribution progress](docs/EVOLUCAO_CONTRIBUICOES.en.md) · [Contributing](CONTRIBUTING.md) · [Security](#security-first)

[Português (Brasil)](README.pt-BR.md)

</div>

---

## The project

**Clean My Android** is an open-source project to investigate what is present on an Android device, understand the purpose of its components, and document changes carefully and verifiably.

The goal goes beyond disabling preinstalled apps. Each audit aims to record the device state **before and after**, explain what changed, provide supporting evidence, measure results when possible, and clearly state testing limitations.

The project follows the collaborative approach of [CleanYourTV](https://github.com/Gathin23/cleanyourtv): model-specific knowledge, reproducible documentation, and contributions incorporated into the main repository through Pull Requests.

> **Important:** Android devices are not interchangeable. Manufacturer, model, region, firmware, Android version, and user configuration all affect package behavior. A recommendation must never be treated as universal.

## Get started: AI assistant recommended

**Clean My Android is designed to be used preferably with the help of an AI assistant of the user's choice.** The AI guides the investigation, interprets device-specific data, explains risks, organizes evidence, and prepares the report. You remain in control: no device changes may be made without your explicit authorization.

You are not tied to a provider. You may use ChatGPT, Claude, Gemini, Antigravity, Codex, or another assistant capable of working with the project files. To run commands and collect data directly, choose an agent with access to your computer's terminal and ADB. A chat without device access can still guide the analysis, but it cannot inspect the device directly.

### Recommended workflow

1. **Prepare the environment:** install ADB, enable USB or wireless debugging, and authorize the computer on the device.
2. **Open the project in your assistant:** clone the repository and open its folder in your AI agent.
3. **Load the instructions:** ask the assistant to read [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) and follow [the individual device audit guide](docs/USER_DEVICE_AUDIT.md).
4. **Inspect first:** the AI identifies the device and collects the initial state without making changes.
5. **Review the plan:** examine package analysis, risks, proposed commands, and rollback methods.
6. **Authorize deliberately:** changes may only happen after your explicit approval, in controlled steps.
7. **Compare and document:** the AI repeats data collection, records tests and limitations, and prepares the before/after report.
8. **Contribute:** review and sanitize the files and, if you choose, submit the audit through a Pull Request.

### Requirements

- Linux, macOS, or Windows with Android Debug Bridge (ADB) installed.
- USB or wireless debugging enabled on the device.
- Computer authorized by Android.
- A connected device identified as the target.
- An assistant with access to the project folder and terminal/ADB for direct automation.

### Which assistant should you use?

Use the assistant you prefer. The project does not require a subscription, model, or specific service. To perform the audit directly, the agent must be able to read repository files and access the terminal where ADB is available. Review the permissions granted to the agent and do not enable unnecessary access.

### Manual execution (advanced alternative)

Users experienced with Android, ADB, permissions, services, and package management may follow the procedure manually without AI. The same safety and documentation workflow applies; only the person performing the analysis and organizing the results changes.

Clone the project:

~~~bash
git clone https://github.com/luisfvmartins/clean-my-android.git
cd clean-my-android
~~~

Run an initial inspection:

~~~bash
adb devices -l
./scripts/debloat.sh
~~~

The default mode identifies the device and lists packages disabled for the primary user. **It makes no changes.**

### Changes: only when explicitly supported

The script's apply mode is restricted to the **Motorola Moto G54 5G running Android 15**, requires typed confirmation, and acts on one package per execution:

~~~bash
./scripts/debloat.sh --apply package.name
~~~

Do not use this command on another model or Android version. The protected-components list is an additional safeguard, not a guarantee that every package outside it is safe to disable.

To re-enable an individually disabled package:

~~~bash
./scripts/restore.sh package.name
~~~

Before making any change, read the [individual device audit guide](docs/USER_DEVICE_AUDIT.md) and follow its safety rules. Manual execution does not remove the need for evidence, authorization, reversibility, and testing.

## How it works

The recommended workflow is divided into independent stages. Diagnosis and data collection come before any change.

| Stage | Goal | Expected result |
|---|---|---|
| **1. Identification** | Record model, codename, Android, firmware, and environment | Verifiable device identification |
| **2. Initial state** | Collect packages, permissions, AppOps, and available metrics | “Before” inventory |
| **3. Analysis** | Investigate purpose, dependencies, evidence, and risks | Technical classification per component |
| **4. Plan** | Present proposed changes and rollback methods | Reviewable plan for the device owner |
| **5. Authorized changes** | Perform only approved and compatible actions | Record of changes actually made |
| **6. Final state** | Repeat data collection under comparable conditions | “After” inventory |
| **7. Comparison** | Compare data, tests, and limitations | Technical before/after report |
| **8. Publication** | Sanitize and submit the contribution through a Pull Request | New audit in the public catalog |

AI is the recommended working method, not an authority over the device. It must analyze evidence, explain risks, and wait for explicit authorization before changing the device. [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) provides provider-independent guidance.

## Audited devices

Audits are device-specific and have different validation levels. Consult the [device catalog](reports/README.md) for each report's scope, files, and outstanding items.

| Device | Documentation | Status |
|---|---|---|
| Motorola Moto G54 5G (XT2343-1) | [Technical audit (English summary)](docs/AUDITORIA_MOTO_G54_5G.en.md) · [Full report (Portuguese)](docs/AUDITORIA_MOTO_G54_5G.md) | Inventory published; see report for scope and limitations |
| Motorola Edge 60 Pro (XT2507-1) | [Audit summary (English)](reports/motorola/edge-60-pro/README.en.md) · [Full technical audit (English)](reports/motorola/edge-60-pro/auditoria.en.md) | Functional validation and confirmation of some data pending |

**A device appearing in the catalog does not mean every procedure has been approved for it.** Script compatibility is indicated separately and must not be inferred from the existence of a report.

## What each audit should document

- **Identification:** manufacturer, model, codename, Android/ROM version, and build.
- **Inventory:** system and user packages, state, version, and origin when available.
- **Permissions and AppOps:** what is declared, granted, or effectively configured.
- **Component analysis:** known purpose, evidence, dependencies, and change risk.
- **Changes:** commands executed, authorization, outcome, and rollback method.
- **Comparison:** before/after metrics collected under equivalent conditions.
- **Functional tests:** telephony, connectivity, camera, biometrics, notifications, banking apps, and other relevant features, when applicable.
- **Limitations:** data not collected, tests not performed, and inconclusive findings.

Results without evidence must be marked **not measured**, **not collected**, or **pending validation**. Do not turn estimates into proven results.

## Automated validation

Pull Requests to `main` run automated integrity checks for JSON, Bash syntax, and the protected-components list. These checks are static: they do not access or modify devices. A passing workflow does not replace technical review, privacy review, or functional testing.

See the [validation workflow](.github/workflows/validate.yml) and [validator](scripts/validate_repository.py).

## Security first

This project prioritizes reversibility, transparency, and device-owner control.

- Inspection is different from modification: the default script mode is read-only.
- The available apply operation is individual, requires confirmation, and is device/version restricted.
- Current scripts do not support batch uninstall, data wiping, or automatic profile removal.
- Do not disable critical Android, telephony, connectivity, encryption, package installation, or security components.
- Do not conclude that an app is spyware solely because it has internet access, belongs to the manufacturer, or includes an analytics SDK.
- AppOps applied by UID may affect multiple packages sharing that UID; do not apply rules without mapping the relationships and effects.
- Do not publish raw inventories, identifiers, tokens, accounts, notifications, or personal data.

**There is no universal guarantee of better battery life, RAM use, storage, privacy, or banking compatibility.** These effects depend on the device and must be measured. Changes may cause feature loss; keep a recovery path available.

Also read [docs/USER_DEVICE_AUDIT.md](docs/USER_DEVICE_AUDIT.md) and [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

## Repository structure

```text
.
├── AI_INSTRUCTIONS.md       # AI-assisted audit instructions (English)
├── AI_INSTRUCTIONS.pt-BR.md # AI-assisted audit instructions (Portuguese)
├── data/                    # Inventories and protection lists
├── docs/                    # Guides and technical audits
├── reports/                 # Device-specific reports
└── scripts/                 # Inspection, disabling, and restoration
```

## How to contribute

Each device must have its own folder under `reports/`. A contribution must preserve existing reports and add its documentation to the catalog.

1. Read [CONTRIBUTING.md](CONTRIBUTING.md) and [docs/USER_DEVICE_AUDIT.md](docs/USER_DEVICE_AUDIT.md).
2. Fork the repository and create a dedicated branch for your contribution.
3. Collect and sanitize data from your own device.
4. Include the report, inventories, and required evidence.
5. Update the device index in `reports/README.md` (and its English counterpart).
6. Open a Pull Request against `main`.

Every approved and merged Pull Request expands the public knowledge base. Do not alter or replace another device's audit to add your own.

## Language coverage\n\nThe main project guides, AI instructions, contribution guide, and device catalog are available in English. Some detailed historical audit reports and raw component inventories remain in Portuguese; their package identifiers and collected evidence are preserved unchanged. English summaries are provided where practical.\n\n## Documentation and links

- [Audit catalog (English)](reports/README.md)
- [Individual device audit guide (English)](docs/USER_DEVICE_AUDIT.md)
- [AI instructions (English)](AI_INSTRUCTIONS.md)
- [Contributing and Pull Requests (English)](CONTRIBUTING.md)
- [README em português](README.pt-BR.md)
- [Source code](https://github.com/luisfvmartins/clean-my-android)
- [MIT License](LICENSE)

---

<div align="center">

**Real audits. Verifiable evidence. Deliberate changes.**

</div>
