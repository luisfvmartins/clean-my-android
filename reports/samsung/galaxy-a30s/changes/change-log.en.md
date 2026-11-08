# Samsung Galaxy A30s — Change Log (English Summary)

> **Translation note:** This is a structured English summary of the Portuguese operational log, not a line-by-line translation of every row. The [Portuguese change log](change-log.md) is the detailed historical record. This summary is not an execution guide.

## Scope

The source log records two batches of ADB changes on a Samsung Galaxy A30s (`SM-A307GT`), running Android 11 / One UI 3.1 on an Exynos 7904 platform. The session was performed without root.

The log records 48 package actions for User 0:

- 2 commercial applications uninstalled for User 0.
- 46 packages disabled using reversible package-manager state changes.
- Categories include commercial preload apps, Meta background components, Samsung diagnostic and analytics services, Google feedback and location-history components, game-related services, and selected convenience or multimedia modules.

For each recorded action, the Portuguese source includes the package name, command, command output, verified state, and restoration command.

## Important preserved components

The source audit states that the Samsung keyboard (HoneyBoard), One UI Home launcher, telephony/RIL/IMS stack, Google Play Services, and Google Play Store were preserved.

## Validation notes

The source log reports successful command execution for the listed changes. A successful package-manager response is not, by itself, proof of complete functional validation. The accompanying comparison report documents the observed checks and pending long-term battery testing.

- [Detailed package-by-package change log (Portuguese)](change-log.md)
- [English comparison summary](../comparison-report.en.md) · [Portuguese comparison](../comparison-report.md)
- [Device overview (English)](../README.en.md) · [Portuguese](../README.md)

Do not copy these historical commands to another Samsung device without fresh package identification, dependency analysis, explicit owner authorization, and post-change testing.
