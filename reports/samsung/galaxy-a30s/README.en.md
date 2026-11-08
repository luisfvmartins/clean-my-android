# 📱 Samsung Galaxy A30s — Technical Audit and Surgical Optimization

[![Device: Samsung Galaxy A30s](https://img.shields.io/badge/Device-Samsung%20Galaxy%20A30s-002f6c?logo=samsung&logoColor=white)](comparison-report.md)
[![Codename: a30s](https://img.shields.io/badge/Codename-a30s-blue)](comparison-report.md)
[![Android: 11 (One UI 3.1)](https://img.shields.io/badge/Android-11%20(One%20UI%203.1)-green?logo=android&logoColor=white)](comparison-report.md)
[![Status: Completed Audit](https://img.shields.io/badge/Audit-Completed-brightgreen)](comparison-report.md)
[![Clean My Android](https://img.shields.io/badge/Project-Clean%20My%20Android-green)](https://github.com/luisfvmartins/clean-my-android)

This directory contains the complete technical documentation, baseline and post-optimization package inventories, resource comparison report, and detailed change log for the **Samsung Galaxy A30s (SM-A307GT)**.

---

## 📌 Technical Identification

| Technical Parameter | Verified ADB Identification |
| :--- | :--- |
| **Manufacturer / Brand** | Samsung (`samsung`) |
| **Commercial Model** | Samsung Galaxy A30s |
| **Model Code** | `SM-A307GT` |
| **Product / Codename** | `a30sdtvvj` / `a30s` |
| **Platform / Processor** | Samsung Exynos 7904 Octa-Core (`universal7904`) |
| **Architecture / ABI** | 64-bit `arm64-v8a` (`exynos7904`) |
| **Android Version** | Android 11 (API Level 30) |
| **User Interface** | One UI 3.1 (Samsung Experience Platform SEP `120100`) |
| **Firmware Build** | `RP1A.200720.012.A307GTVJS5CWE2` |
| **Security Patch** | May 1, 2023 (Final lifecycle security patch) |
| **CSC Region** | `ZTO` (Brazil - Retail / Unlocked) |
| **Linux Kernel** | `Linux 4.4.177-22825772 aarch64` |
| **Physical RAM** | 4 GB LPDDR4x (`Total RAM: 3,813,448 KB`) |
| **Internal Storage** | 64 GB eMMC 5.1 (`/data` partition with 51 GB raw) |
| **Bootloader State** | Unlocked (`ro.boot.flash.locked: 0`, `ro.boot.verifiedbootstate: orange`) |
| **Execution Privileges** | Non-root (`uid=2000 shell`) |
| **User Profile** | Primary User (`User 0`) |

---

## 🎯 Scope of the Surgical Optimization

The procedure was executed in non-root mode via **Android Debug Bridge (ADB)** with explicit user authorization:

1. **Exhaustive Package Inventory:** All 392 firmware packages were audited and categorized in `before/inventory.json`.
2. **Commercial Bloatware Removal:** Uninstalled for User 0 preloaded commercial partner apps (`com.odete.samsung` and `com.samsung.shop`).
3. **Meta / Facebook Background Eradication:** Disabled 4 persistent background components (`katana`, `system`, `appmanager`, `services`).
4. **Game Optimizing Service (GOS) Throttling Removal:** Disabled *Game Optimizing Service* (`com.samsung.android.game.gos`) and satellites (`gamehome`, `gametools`), eliminating artificial CPU/GPU thermal and clock throttling on the Exynos 7904.
5. **Silencing False Security Alerts & Telemetry:** Disabled *Security Log Agent* (`com.samsung.android.securitylogagent`), eradicating repetitive integrity warning notifications caused by the unlocked bootloader, as well as disabling *Samsung Rubin* and *Knox Analytics Uploader*.
6. **Preservation of Critical Subsystems:** Active keyboard (Samsung HoneyBoard), launcher (One UI Home), telephony/RIL/IMS stacks, and Google Play Services/Store were 100% preserved to guarantee everyday usability and banking compatibility.

---

## 📊 Summary of Results

- **Firmware Cataloged Packages:** 392 packages
- **Enabled Packages Before:** 391 packages
- **Enabled Packages After:** 371 packages (**-20 active background packages**)
- **Disabled Packages:** 20 packages (1 factory default + 19 surgically disabled)
- **Uninstalled Commercial Apps (User 0):** 2 packages (`com.odete.samsung` and `com.samsung.shop`)
- **System Stability & Connectivity:** 100% operational (Wi-Fi, Bluetooth, Telephony, Biometrics, and Google Play Services).

---

## 📂 Document Structure

- [`comparison-report.md`](comparison-report.md): Detailed technical before/after comparison report.
- [`comparativo.json`](comparativo.json): Machine-readable structured metrics.
- [`before/`](before/): Initial baseline diagnostics (package inventory, memory, battery, process, and permission logs).
- [`changes/`](changes/): Execution log, commands used, and reversal procedures.
- [`after/`](after/): Final confirmatory diagnostics post-optimization.
