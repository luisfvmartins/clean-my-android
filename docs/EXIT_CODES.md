# Script Exit Codes

This document details every exit code returned by the **Clean My Android** utility scripts (`debloat.sh`, `restore.sh`, and `snapshot.sh`), specifying the root cause and the required corrective action.

---

## 1. `scripts/debloat.sh`

| Code | Meaning | Trigger Condition | Recommended Action |
|:---:|---|---|---|
| **0** | Success / No change | Operation completed successfully, read-only mode finished, `--help` displayed, user cancelled confirmation, or package already disabled for User 0. | No action required. |
| **1** | ADB Environment failure | The `adb` binary was not found in `PATH`, or the number of authorized connected devices is not exactly 1. | Install Android SDK Platform-Tools and verify connection using `adb devices`. |
| **2** | Invalid arguments | Incorrect command-line syntax or invalid package name formatting (e.g. must follow `com.example.app`). | Check usage with `./debloat.sh --help` and provide a valid canonical package name. |
| **3** | Blocked by Apply Gate | Connected device or Android version is not present in `data/apply_support.tsv`. | `--apply` execution is restricted to Moto G54 5G (Android 15) with audited homologation. For other models, use read-only mode. |
| **4** | Missing configuration file | Apply support file `data/apply_support.tsv` or protected packages list `data/protected_essential_packages.txt` was not found. | Run the script from repository root or restore required configuration files. |
| **5** | Protected essential component | The specified package is listed in `data/protected_essential_packages.txt` as a critical OS component (e.g., telephony, keyboard, system UI). | Intervention blocked for safety. Package must remain active to prevent system instability or boot loops. |
| **6** | Package not found on device | The specified package was not found via `pm path` on the target device. | Verify installed packages using `adb shell pm list packages`. |
| **7** | State verification failure | Disable command executed, but post-execution verification (`pm list packages -d`) did not confirm the disabled state. | Inspect system logs (`logcat`) or check device administrator restrictions. |

---

## 2. `scripts/restore.sh`

| Code | Meaning | Trigger Condition | Recommended Action |
|:---:|---|---|---|
| **0** | Success / No change | Package successfully re-enabled, `--help` displayed, user cancelled confirmation, or package already enabled for User 0. | No action required. |
| **1** | ADB Environment failure | The `adb` binary was not found in `PATH`, or the number of authorized connected devices is not exactly 1. | Connect and authorize exactly one ADB device. |
| **2** | Invalid arguments | Missing or invalid parameters, or incorrect package format. | Use `./restore.sh PACKAGE`. |
| **3** | Package not found on device | The package does not exist on device firmware (`pm path` returned no APK). | Confirm the package name is correct. |
| **4** | Re-enabling verification failure | `pm enable` command was issued, but package remained listed as disabled. | Check ADB permissions or restrictions imposed by work profile / MDM. |

---

## 3. `scripts/snapshot.sh`

| Code | Meaning | Trigger Condition | Recommended Action |
|:---:|---|---|---|
| **0** | Capture and sanitization success | All evidence files collected, structured, and approved by the sanitization validator. | Evidence ready for repository integration. |
| **1** | ADB Environment failure | The `adb` binary was not found in `PATH`, or device count is not exactly 1. | Check connection with `adb devices`. |
| **2** | Invalid arguments | Missing required arguments (`--label before\|after` or `--out DIR`). | Refer to `./snapshot.sh --help` and provide valid label and output path. |
| **3** | ADB communication failure | Device communication error or timeout during property/package queries. | Reconnect USB cable and restart ADB server (`adb kill-server`). |
| **4** | Output directory creation failure | Could not create target output directory specified by `--out`. | Check filesystem write permissions. |
| **5** | Pre-write sanitization failure | Sanitization validator detected sensitive telemetry (IMEI, MAC addresses, accounts, or credentials) in staging files. | The script aborts write to prevent leaking private data. Inspect and sanitize evidence before publishing. |
