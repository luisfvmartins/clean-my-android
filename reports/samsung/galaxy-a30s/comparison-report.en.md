# Samsung Galaxy A30s — Before/After Comparison (English Summary)

> **Translation note:** This is an English structured summary, not a line-by-line translation. The [Portuguese comparison report](comparison-report.md) remains the detailed source. Figures below reproduce its records and have not been independently re-measured for this summary.

## Device context

- **Model:** Samsung Galaxy A30s (`SM-A307GT`)
- **Product / codename:** `a30sdtvvj` / `a30s`
- **Platform:** Exynos 7904
- **Android:** 11 (API 30), One UI 3.1
- **Build:** `RP1A.200720.012.A307GTVJS5CWE2`
- **Security patch:** 2023-05-01
- **Region:** Brazil retail / unlocked (`ZTO`)
- **Audit date:** November 8, 2026
- **Execution:** ADB shell, without root; bootloader reported unlocked.

## Main recorded changes

The audit was conducted in two batches and reports 48 packages addressed for User 0: 2 uninstalled for the user and 46 reversibly disabled. The changes included commercial preload apps, Digital Turbine Ignite, selected Samsung diagnostic and logging services, Google location-history components, four Meta background components, Game Optimizing Service and related game modules, and selected idle scanning, lock-screen, AR, and sticker components.

Critical components—including Samsung keyboard and launcher, telephony/RIL/IMS, Google Play Services, and Google Play Store—were intentionally preserved.

## Before/after metrics reported by the source

| Metric | Before | After |
|---|---:|---:|
| Firmware packages | 392 | 392 |
| Enabled packages for User 0 | 391 | 344 |
| Disabled packages | 1 factory-disabled | 47 |
| Uninstalled for User 0 | 0 | 2 |
| Free storage in `/data` | ~49 GB | ~49 GB |
| AP / battery temperature at rest | 25.6°C / 25.6°C | 25.5°C / 25.5°C |

The report states that 48 packages were addressed (46 disabled plus 2 uninstalled), while the enabled-package count decreased by 47 because the baseline included one factory-disabled package. These categories should not be conflated.

## Functional validation and limitations

The Portuguese report records no command failures, observed system force-closes, or immediate need for rollback during the session. It also states that a standardized 24–48-hour battery observation remains pending. These are session-specific observations, not a guarantee of long-term stability or battery improvement.

The original report contains operational detail and a historical private-network endpoint. That endpoint has been removed from the public Portuguese source in this update; network addresses are intentionally omitted from this English summary as well.

- [Detailed comparison report (Portuguese)](comparison-report.md)
- [Detailed change log (Portuguese)](changes/change-log.md) · [English change-log summary](changes/change-log.en.md)
- [Device overview (English)](README.en.md) · [Portuguese](README.md)

Do not reuse package actions on another Samsung model, firmware, region, or user profile without a new device-specific audit and explicit owner authorization.
