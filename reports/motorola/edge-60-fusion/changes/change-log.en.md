# Motorola Edge 60 Fusion — Change Log (English Summary)

> **Translation note:** This is a structured English summary of the Portuguese operational log, not a line-by-line translation of all package rows and commands. The [Portuguese change log](change-log.md) is the detailed historical record. This file is descriptive documentation, not an execution guide or authorization to repeat any action.

## Scope

The source log records changes made through ADB on the Motorola Edge 60 Fusion (`scout` / `motorola_edge_60_fusion`), including the prior state, action, rationale, risk, known dependencies, restoration method, and available evidence.

The recorded work covers:

- Disabling or uninstalling selected commercial installers, advertising modules, and third-party preload components for Android User 0.
- Disabling selected Motorola / Lenovo diagnostic, telemetry, support, and promotional services.
- Disabling selected Google feedback, partner-setup, setup, and wellbeing components.
- Reviewing carrier-specific overlays and static stubs.
- Restricting selected permissions or AppOps where package-level disablement was not the recorded method.
- Replacing selected proprietary applications with FOSS alternatives.

## FOSS alternatives recorded

The source log records the following substitutions:

| Function | Previous application | Replacement |
|---|---|---|
| Keyboard | Gboard | FUTO Keyboard |
| Phone | Google Dialer | Fossify Phone |
| SMS | Google Messages | Fossify Messages |
| Contacts | Google Contacts | Fossify Contacts |
| Gallery | Google Photos | Fossify Gallery |
| File manager | Files by Google | Fossify File Manager |
| Calendar | Google Calendar | Fossify Calendar |
| Clock / alarm | Google Clock | Fossify Clock |

The source includes package-level commands and restoration commands for individual changes. Consult it only as historical evidence; do not copy commands without independently confirming the package, firmware, dependencies, impact, and reversibility on the target device.

## Safety notes

Package actions are firmware- and user-specific. A successful command does not by itself prove that every dependent feature remains functional. Any new intervention requires explicit device-owner authorization, a current backup where appropriate, read-only inspection first, and post-change functional validation.

- [Detailed package-by-package log (Portuguese)](change-log.md)
- [English technical audit summary](../audit.en.md)
- [Portuguese technical audit](../audit.md)
