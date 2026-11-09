# Sanitization and Privacy Protection Log

> This log documents all inspections, sanitization procedures, and privacy audits performed across reports, raw evidence, and inventories in the **Clean My Android** repository, in compliance with Non-Negotiable Rules (Section 1, Rule 3).

---

## 1. Sanitization Guidelines

No document published in the repository may expose data that allows identifying the hardware owner, personal accounts, credentials, or private network topology. Actively monitored categories include:

| Category | Pattern / Type | Required Action |
| :--- | :--- | :--- |
| **IMEI / IMSI** | 15 decimal digits with Luhn algorithm check | Total omission or replacement with dummy value |
| **MAC Address** | `XX:XX:XX:XX:XX:XX` | Replaced with `[REDACTED_MAC]` |
| **Serial Number** | `ro.serialno`, `ro.boot.serialno` | Total omission of hardware serial properties |
| **Account Identifiers** | User account structures | Removal of synced usernames and email addresses |
| **Private IP Addresses** | RFC 1918 subnets | Redaction of local routes and active socket endpoints |
| **Phone / Contacts** | Brazilian mobile and landline numbers | Total removal |
| **Image Metadata** | EXIF metadata in screenshots | Complete removal via lossless re-encoding |

---

## 2. Audit and False-Positive Investigation

### 2.1 Investigation of Numerical Patterns in `inventory.json` Files
* **Inspection Date:** 2026-11-08.
* **Context:** A regular expression search identified numerical quadruplet patterns across `inventory.json` files.
* **Technical Analysis:** All occurrences were individually investigated in their JSON context. It was technically confirmed that **none** represents a network IP address; all correspond to the software version field (`version_name`) of pre-installed system applications:
  * `reports/motorola/edge-60-fusion/before/inventory.json`: Line 5227 — Motorola Camera app version (MotCamera5).
  * `reports/motorola/edge-60-fusion/after/inventory.json`: Line 2487 — Motorola Camera app version (MotCamera5).
  * `reports/motorola/edge-60-pro/inventario-antes.json`: Line 4442 — Motorola Camera app version.
  * `reports/samsung/galaxy-a30s/before/inventory.json`: Lines 821, 1824, 4612, 5003 — Samsung system app versions (Gallery/Camera, Calendar, Weather, and Voice Recorder).
  * `reports/samsung/galaxy-a30s/after/inventory.json`: Lines 917, 2038, 5154, 5591 — Matching app versions.
* **Resolution:** Formally registered with individual technical justifications in [data/sanitization_allowlist.json](../data/sanitization_allowlist.json).

### 2.2 Visual Inspection and Metadata of Screenshots
* **Total Images:** 7 PNG files in `reports/samsung/galaxy-a30s/`.
* **EXIF Metadata Inspection:** All 7 images were processed to guarantee total stripping of any ancillary chunks or camera timestamps/geolocations.
* **Visual Content Inspection:**
  1. `before/screenshots/01_device_about.png`: Stock lock screen (12:58, Nov 8, 72% battery, "Chamadas de emergência", 3 generic system icons). **No personal data, accounts, or exposed identifiers.**
  2. `before/screenshots/02_storage.png`: Blank/black capture (display buffer asleep during ADB screencap). **Free of sensitive data.**
  3. `before/screenshots/03_battery.png`: Blank/black capture. **Free of sensitive data.**
  4. `before/screenshots/04_apps.png`: Blank/black capture. **Free of sensitive data.**
  5. `after/screenshots/02_storage.png`: Post-session lock screen (13:14, Nov 8, 71% battery, "Somente chamadas de emergência"). **No personal data, accounts, or exposed identifiers.**
  6. `after/screenshots/03_battery.png`: Blank/black capture. **Free of sensitive data.**
  7. `after/screenshots/04_apps.png`: Blank/black capture. **Free of sensitive data.**

---

## 3. Automated CI Validator

Automated sanitization verification is integrated into CI via the executable script [scripts/check_sanitization.py](../scripts/check_sanitization.py) and unit-tested in [tests/test_sanitization.py](../tests/test_sanitization.py).

Any newly added file containing valid IMEI numbers, exposed MAC addresses, user credentials, or unapproved private IPs fails the build immediately.
