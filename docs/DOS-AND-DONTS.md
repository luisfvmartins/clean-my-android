# Contribution Do's and Don'ts

This guide establishes practical safeguards for Clean My Android contributions. Follow it alongside [CONTRIBUTING.md](../CONTRIBUTING.md), [AI_INSTRUCTIONS.md](../AI_INSTRUCTIONS.md), and the [device audit guide](USER_DEVICE_AUDIT.md).

## Do

- **Add knowledge cumulatively.** Add or revise the relevant device report without removing other devices' data or prior findings.
- **Identify the exact device and software.** Include manufacturer, model, Android version, build fingerprint or build identifier when safe, and audit date.
- **Separate evidence from interpretation.** Label observed state, user-provided details, inference, and recommendation distinctly.
- **Use read-only inspection first.** Inventory the device before proposing changes.
- **Get explicit authorization.** Explain each consequential action and obtain the owner's approval before disabling, uninstalling, changing settings, or executing other modifying commands.
- **Validate reversibility.** Document restoration paths and limitations for any proposed change.
- **Keep results reproducible.** Include relevant command, expected result, actual result, and test conditions without exposing sensitive output.
- **Compare like with like.** Record before/after states using equivalent conditions and note anything that prevents a fair comparison.
- **Update related indexes.** Keep report catalogs, summaries, and links consistent with the new contribution.
- **Review the final diff.** Confirm that only intended files changed and that documentation links resolve.
- **Use the repository's validation checks.** Run available tests and report failures or unavailable checks honestly.

## Don't

- **Don't delete, overwrite, or silently replace another device's report.**
- **Don't present a package list as a universal debloat list.** Package behavior varies by manufacturer, model, firmware, region, and user needs.
- **Don't claim a command was executed or a result was verified without evidence.**
- **Don't treat a package name, internet post, or AI inference alone as proof that removal is safe.**
- **Don't perform changes without the device owner's explicit authorization.**
- **Don't include sensitive identifiers or raw personal data.** This includes IMEI, serial numbers, MAC addresses, private IP addresses, hostnames, account names/IDs, notification contents, tokens, credentials, and unredacted logs.
- **Don't commit private device dumps, backups, or screenshots containing personal information.**
- **Don't leave debugging access enabled.** If ADB over network was enabled for an audit, document and verify that it is disabled afterward when appropriate.
- **Don't mix unrelated changes.** Keep a PR focused and avoid changing CI, scripts, catalogs, and device findings unrelated to its purpose.
- **Don't mark untested recommendations as confirmed or safe.**
- **Don't rely on automated secret scanning as a substitute for manual privacy review.**

## Before submitting

1. Read the PR checklist in [the pull request template](../.github/PULL_REQUEST_TEMPLATE.md).
2. Review the entire diff for scope, accuracy, and privacy.
3. Run the checks relevant to the files changed.
4. State what was tested, what was not tested, and any known limitations in the PR description.
