# Change Log — Motorola Edge 60 Pro (`XT2507-1`)

This document consolidates the technical record of all modifications executed during the audit and debloat session on the **Motorola Edge 60 Pro**.

---

## 1. Packages Disabled for User 0 (`pm disable-user --user 0`)

A total of **244 packages** were disabled, listed in [`disabled-packages.txt`](disabled-packages.txt):
* **Commercial Promoters, Bloatware, and OOBE Partners:** 11 components (Digital Turbine, IronSource Aura, Glance, Taboola, InMobi).
* **OEM Telemetry & Foreign Carrier Stubs:** International carrier overlays (AT&T, Telekom, Orange) and Motorola marketing daemons.
* **Optional Google Components:** Selective deactivation of pre-installed apps while preserving core system stability.

---

## 2. Packages Uninstalled for User 0 (`pm uninstall -k --user 0`)

A total of **9 packages** were uninstalled for User 0, documented in [`removed-packages.txt`](removed-packages.txt):
* 2 third-party apps purged from `/data/app` (adwares installed via DT Ignite).
* 7 system stubs uninstalled at user level.

---

## 3. Surgical Permission Revocation and AppOps

Runtime permission revocations and AppOps sandboxing were performed manually and are documented in [`permission-changes.json`](permission-changes.json):
* 13 sensitive runtime permissions (location, microphone, contacts) revoked from non-essential packages.
* AppOps sandboxing applied to specific UIDs. As documented in [`docs/MANUAL_CHANGES.md`](../../../../docs/MANUAL_CHANGES.md), these steps are strictly manual without script automation.
