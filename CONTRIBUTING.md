# Contributing to Clean My Android

Contributions are welcome, especially audits of new device models, documentation corrections, and security improvements to scripts.

The goal is to build a cumulative public knowledge base: **every approved Pull Request adds knowledge to the main repository without removing previous work.**

## Recommended way to use the project

For a device audit, we recommend using an AI assistant of your choice, such as ChatGPT, Claude, Gemini, Antigravity, Codex, or an equivalent tool. The project does not depend on a specific provider.

The simplest workflow is to clone this repository, open the folder in an agent with terminal/ADB access, and ask it to read [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) and the [individual device audit guide](docs/USER_DEVICE_AUDIT.md). The assistant can then guide data collection, analyze components, prepare a reviewable plan, document before/after states, and organize the contribution.

**Manual execution is still allowed** for people with technical Android and ADB knowledge. The AI recommendation does not remove user responsibility: no device change may happen without explicit authorization, and every contribution must be reviewed and sanitized before submission.

## Contribution types

| Contribution | Where to submit |
|---|---|
| Audit of a new device | New folder under `reports/` + catalog update |
| Addition to an existing audit | Same device folder, with revision and date clearly identified |
| Documentation correction | Corresponding file in `README.md`, `docs/`, or this guide |
| Script correction or improvement | `scripts/`, with justification and validation |
| New protected-components list | `data/`, with evidence and technical justification |

## 1. Prepare a fork and branch

Contributors without write access must create a GitHub fork and work on a dedicated branch.

With GitHub CLI:

```bash
gh auth login
gh repo fork luisfvmartins/clean-my-android --clone
cd clean-my-android
git remote add upstream https://github.com/luisfvmartins/clean-my-android.git
git remote -v
git switch -c audit/manufacturer-model-android
```

Confirm:
- `origin` points to your fork.
- `upstream` points to `luisfvmartins/clean-my-android`.
- Your working branch is not `main`.

## 2. Prepare an audit

Before making any device changes, follow the [individual device audit guide](docs/USER_DEVICE_AUDIT.md) and the [AI instructions](AI_INSTRUCTIONS.md).

A device contribution must:
- identify the exact manufacturer, model, codename, Android/ROM, and build when available;
- record the initial state before making changes;
- distinguish observed evidence, technical inference, and hypotheses;
- present a change plan and risks before execution;
- record only actions actually authorized and performed;
- repeat measurements afterward under comparable conditions;
- document functional tests, limitations, and rollback procedures.

Do not use another device's inventory as if it were yours. Do not apply package lists from another model.

## 3. Organize files

Create a dedicated folder following `reports/<manufacturer>/<model>/`, for example:

```text
reports/samsung/galaxy-model/
├── README.md
├── audit.md
├── inventory-before.json
├── inventory-after.json
├── comparison.json
└── evidence/
    └── README.md
```

The structure is flexible. Include only files that exist and are useful. Do not create empty files to imply complete data collection.

Update both catalog indexes, `reports/README.md` (English) and `reports/README.pt-BR.md` (Portuguese), with an entry for the device. Do not edit or reorganize other devices' entries unnecessarily.

## 4. Privacy before submission

The repository and Pull Requests are public. Review all files and images carefully.

Never publish:
- IMEI, MEID, serial number, account identifiers, or tokens;
- MAC addresses, public IP addresses, private hostnames, or details exposing your network;
- phone numbers, email addresses, contact names, or notifications;
- location data, synced accounts, or personal information;
- API keys, passwords, pairing codes, or ADB credentials.

Keep raw dumps locally. Share only sanitized data needed to support the conclusions. Deleting a file later does not guarantee that published information disappears from Git history.

## 5. Review and submit

```bash
git status --short
git diff --check
git diff
git add reports/YOUR-DEVICE reports/README.md reports/README.pt-BR.md
git commit -m "docs(audit): add <manufacturer-model> device report"
git push -u origin HEAD
gh pr create --repo luisfvmartins/clean-my-android --base main
```

Adapt paths and commit messages to the files actually changed. For documentation-only or script contributions, add the corresponding files to `git add`.

## 6. Review criteria

A Pull Request may be sent back for changes or rejected when it:
- does not clearly identify the device and system version;
- mixes observed data with assumptions;
- presents metrics without a method or collection conditions;
- omits risks, side effects, or recovery methods;
- recommends dangerous or universal changes;
- contains personal data, credentials, or identifiers;
- overwrites or removes another device's contribution;
- fails to update the catalog when adding an audit.

Opening a PR does not mean automatic approval. After review and merge, files become part of the official collection on the `main` branch.

## Useful links

- [Individual device audit guide](docs/USER_DEVICE_AUDIT.md)
- [Device catalog](reports/README.md)
- [AI assistant instructions](AI_INSTRUCTIONS.md)
- [GitHub repository](https://github.com/luisfvmartins/clean-my-android)
- [Portuguese contribution guide](CONTRIBUTING.md)

## 7. Automated validation

Pull Requests targeting `main` run the **Repository validation** workflow. It checks:

- syntax of all versioned JSON files;
- basic structure of `comparison.json` files (when they contain a `metrics` field);
- Bash syntax of scripts in `scripts/*.sh`, without executing them;
- format and duplicates in `data/protected_essential_packages.txt`;
- consistency of the generated `docs/ESTATISTICAS.md` with `data/device_catalog.json`.

Validation is static only: it does not connect through ADB, install dependencies on the device, or modify devices. A passing result does not replace technical review, privacy checks, or functional testing. Fix issues shown in GitHub Actions logs and update the same Pull Request.
