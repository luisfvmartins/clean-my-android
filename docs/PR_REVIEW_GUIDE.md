# Pull Request Review Guide

Use this checklist when reviewing contributions to Clean My Android. The review should preserve the repository's cumulative, evidence-based device knowledge and prioritize user safety and privacy.

## 1. Scope and repository integrity

- [ ] The PR has a clear purpose and a focused scope.
- [ ] New device findings are placed in the appropriate manufacturer/model directory under `reports/`.
- [ ] Existing reports and findings for other devices remain intact.
- [ ] The PR adds knowledge or clearly corrects a documented error; it does not silently erase history.
- [ ] Relevant indexes, catalogs, and links are updated consistently.

## 2. Device identity and evidence

- [ ] Exact manufacturer, model, Android version, build/software context, and audit date are recorded where applicable.
- [ ] Data collection methods and relevant commands are identified.
- [ ] Observed facts are distinguished from assumptions, interpretations, and recommendations.
- [ ] Before/after comparisons use equivalent conditions or explain differences.
- [ ] Claims are supported by evidence included in the report or by clearly identified sources.
- [ ] Package/app recommendations are contextual to the device and firmware, not generalized to all Android devices.
- [ ] Results that remain untested or uncertain are clearly marked.

## 3. Safety and authorization

- [ ] The report confirms owner authorization for device-modifying actions.
- [ ] Risk, impact, dependencies, and restoration options are explained for consequential recommendations.
- [ ] No recommendation is framed as universally safe without adequate evidence.
- [ ] ADB/network debugging or other temporary access is addressed in the audit's cleanup notes where relevant.

## 4. Privacy and security

- [ ] No personal or device-sensitive identifiers are exposed (IMEI, serial, MAC, private IP, hostname, account identifiers).
- [ ] No credentials, tokens, private keys, notification contents, or unredacted personal logs are present.
- [ ] Screenshots, command output, and inventories have been checked—not just the Markdown text.
- [ ] Raw dumps and backups are excluded unless necessary, explicitly justified, and sanitized.
- [ ] The author has manually reviewed the diff; automated scanners are not treated as sufficient.

## 5. Quality and validation

- [ ] Markdown formatting and relative links are valid.
- [ ] JSON, scripts, package lists, and generated data conform to repository conventions.
- [ ] Relevant automated checks pass, or failures/limitations are explained.
- [ ] Documentation and catalog counts/statistics remain consistent when applicable.
- [ ] The PR template is completed and reviewer questions are resolved.

## Review outcome

- **Approve** when the contribution is accurate, safe, privacy-reviewed, additive, and validated to the extent claimed.
- **Request changes** when evidence, safety context, privacy sanitization, or repository consistency is insufficient.
- **Comment** when clarification would improve the report but does not block acceptance.

A passing CI run does not replace a human review of device-specific safety, evidence quality, or privacy.
