# Motorola Edge 60 Fusion — Before/After Comparison (English Summary)

> **Translation note:** This is a structured English summary, not a line-by-line translation. The [Portuguese comparison report](comparison-report.md) is the detailed source. Values below are reproduced from it and have not been independently re-measured.

## Device context

Motorola Edge 60 Fusion · `scout_g_sysn` / `scout` · MediaTek MT6878 (Dimensity 7300) · Android 16 (API 36) · build `W1VCS36H.14-20-19-9` · security patch 2026-09-01 · audit dates November 7–8, 2026.

## Reported package and resource metrics

| Metric | Before | After / reported result |
|---|---:|---:|
| Cataloged packages | 486 | 343 active for User 0 |
| Active system packages | 424 | 291 |
| Third-party / user packages | 62 | 52 commercial + 12 FOSS apps |
| Factory-disabled packages | 67 | 67 (unchanged) |
| Packages addressed through ADB | 0 | 88 |
| Available RAM | ~2,750 MB | ~4,153–4,573 MB |
| Used PSS | ~3,800 MB | ~2,721–2,881 MB |
| Background processes | 66 | 39 |

The report reconciles 155 neutralized packages as 67 factory-disabled plus 88 addressed during the audit. The final User 0 count also includes 12 installed FOSS alternatives. Package totals refer to different states and categories; they should not be interpreted as a simple one-to-one uninstall count.

## Permissions and privacy surface

The source report documents permission restrictions on selected commercial apps, AppOps restrictions for selected firmware-protected components, and actions involving location-history and hotword-related services. These actions are specific to the recorded build and must not be generalized to other devices.

## Functional checks reported

The Portuguese report marks the following checks as approved: boot, launcher and navigation gestures, calls, SMS/MMS, 4G/5G, Wi-Fi/hotspot, Bluetooth/audio, GPS, camera/video, biometrics, Banco Inter and Nubank, Gemini/search, selected user-preserved apps, and the offline FUTO keyboard.

## Limitations

- A standardized 24-hour battery test was not performed.
- Per-application storage savings were not measured independently.
- Thermal improvement is described as an observation; controlled laboratory measurement remains pending.
- Results reflect the recorded session and are not guarantees for other firmware versions or users.

## Related records

- [Full technical audit (Portuguese)](audit.md) · [English audit summary](audit.en.md)
- [Detailed change log (Portuguese)](changes/change-log.md) · [English change-log summary](changes/change-log.en.md)
- [Device overview (English)](README.en.md) · [Portuguese](README.md)
