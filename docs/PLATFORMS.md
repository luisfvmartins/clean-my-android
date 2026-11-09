# Platform Support and Compatibility Matrix

This document details operating system compatibility and runtime requirements for the **Clean My Android** utility scripts (`debloat.sh`, `restore.sh`, and `snapshot.sh`).

---

## 1. Supported Environments

| Operating System | Shell / Runtime | Testing Status | Official Support | Portability Notes |
|---|---|:---:|:---:|---|
| **Linux (Ubuntu, Debian, Fedora, Arch, etc.)** | GNU Bash 4.x / 5.x | Tested in CI and locally | **Supported** | Standard execution with native POSIX and pipeline support. |
| **macOS (Sonoma, Sequoia, etc.)** | Apple `/bin/bash` 3.2.57 | Tested in CI (`macos-latest`) | **Supported** | Full Bash 3.2 compatibility. No dependencies on `mapfile`, `declare -A`, or GNU-only flags. |
| **Windows 10 / 11 (WSL2)** | Bash in Ubuntu/Debian via WSL2 | Community tested | **Recommended for Windows** | Requires forwarding ADB device from Windows host to WSL2 (`usbipd-win` or shared ADB server). |
| **Windows 10 / 11 (Git Bash / MSYS2)** | Emulated Bash on Windows | **Not tested on physical hardware** | Experimental / Community | Watch out for path mangling and CRLF line terminator conversions. |
| **Windows (Native PowerShell / CMD)** | N/A | **Unsupported** | Unsupported | Scripts rely on Bash syntax and POSIX primitives. No `.bat` or `.ps1` scripts provided. |

---

## 2. Prerequisites and Tooling

To run the utility scripts on any supported platform:
1. **Bash 3.2 or newer:** Present natively on modern Linux and macOS installations.
2. **Android SDK Platform-Tools (`adb`):** The `adb` binary must be installed and accessible in the system `PATH`.
3. **Python 3.10 or newer:** Required for repository validation (`validate_repository.py`) and evidence sanitization. Not required for end-user on-device debloat execution.

---

## 3. Language Selection (`CMA_LANG`)

The scripts include native internationalization support (Brazilian Portuguese and English).
* By default, language is inferred from system environment variables (`LANG` or `LC_ALL`), with English fallback.
* You can explicitly select the language using the `CMA_LANG` variable:
  ```bash
  # Force English output:
  CMA_LANG=en ./scripts/debloat.sh

  # Force Brazilian Portuguese output:
  CMA_LANG=pt ./scripts/debloat.sh
  ```
