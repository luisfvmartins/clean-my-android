# Security Policy — Clean My Android

Device safety, user privacy, and operating system integrity are the core governing principles of the **Clean My Android** project.

This document defines the procedures for reporting technical vulnerabilities, dangerous instructions, or accidental personal data leaks.

---

## 1. Security Scope

We encourage responsible reporting for any of the following scenarios:

1. **Dangerous technical instructions or availability risks:**
   - Commands causing bootloops, permanent system freezes, or unrecoverable bricking without root.
   - Presence of essential system packages (telephony, SMS, emergency dialer, STK, biometrics, Play Store) in general execution lists (`data/*disabled*.txt`).
   - Destructive command parameters (such as `pm uninstall` without user safeguards or accidental critical data purges).
2. **Personal Identifiable Information (PII) leaks or residuals:**
   - Hardware identifiers (IMEI, MEID, device serial numbers).
   - Network hardware identifiers (Wi-Fi/Bluetooth MAC addresses, private local IP addresses in network dumps).
   - User account identifiers (cellular phone numbers, personal email addresses, personal account names).
3. **Automation script vulnerabilities:**
   - Safety gate bypasses (e.g. forced execution on unsupported devices or untested Android releases).
   - JSONL logging anomalies or missing/incorrect rollback commands.

---

## 2. Reporting a Vulnerability

> [!CAUTION]
> **DO NOT open a public Issue** to report personal data leaks or instructions capable of compromising production devices.

Please use one of the following secure channels:

1. **GitHub Private Vulnerability Reporting (Recommended):**
   - Navigate to the **Security** tab in the GitHub repository.
   - Click **Report a vulnerability** to open an encrypted private advisory directly with the maintainer.
2. **Direct Maintainer Contact:**
   - Contact the repository maintainer directly (`@luisfvmartins` on GitHub).

### What to include in your report:
- Clear description of the vulnerability or exposed artifact.
- File path within the repository (`path/to/file:line`).
- For dangerous commands: explanation of functional impact and corresponding rollback command.
- **Important:** If reporting exposed PII, identify the file and data category **without reproducing the sensitive value** in your communication.

---

## 3. Response Times and Remediation

- **Initial triage:** acknowledgment and assessment within **48 hours**.
- **Emergency sanitization:** immediate redaction/scrubbing in repository files accompanied by formal entry in `docs/SANITIZATION_LOG.md`.
- **Technical remediation:** patch implementation, test suite verification, and transparent disclosure.

---

## 4. Supported Versions

Security fixes are applied exclusively to the current canonical branch:

| Branch / Version | Security Fix Support |
|:---|:---:|
| `main` | :white_check_mark: Active |
| Feature / PR branches | :warning: Current review branch only |
