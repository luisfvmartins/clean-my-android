# Component Classification Methodology and Evidence Hierarchy

This document defines the standard technical methodology for identifying packages, assessing risks, mapping dependencies, and assigning confidence levels to software components documented in the **Clean My Android** project.

---

## 1. Fundamental Principle

> [!IMPORTANT]
> **Prior model knowledge or AI training memory is not an evidence source.**
> Any claim regarding component purpose, risk, or dependencies lacking direct backing from repository evidence, public source code, or raw ADB command output is strictly classified with a **`low` confidence level** and explicitly flagged as **`unverified`** pending forensic confirmation.

---

## 2. Strict Evidence Hierarchy

To guarantee reproducibility and prevent speculative claims, package purpose determination adheres to the following descending hierarchy of authoritative sources:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Official AOSP Source Code (cs.android.com)               │
├─────────────────────────────────────────────────────────────┤
│ 2. Official OEM or SoC Documentation                        │
├─────────────────────────────────────────────────────────────┤
│ 3. Forensic Package Manifest and dumpsys Analysis           │
├─────────────────────────────────────────────────────────────┤
│ 4. Operational Behavior Observed on Device                  │
├─────────────────────────────────────────────────────────────┤
│ 5. Secondary Community Sources (UAD, XDA, F-Droid)          │
└─────────────────────────────────────────────────────────────┘
```

### Level 1: Official AOSP Source Code (`cs.android.com` / `android.googlesource.com`)
- **Highest authority** for Android base components, essential providers (`providers.*`), telephony modules, permission subsystems, and core system infrastructure.
- Directly confirms intent filters, protected broadcasts (`protected-broadcast`), boot flags, and exception handling.

### Level 2: Official OEM or SoC Documentation
- Technical manuals, Motorola/Lenovo developer portals, Samsung Knox SDK guides, MediaTek Dimensity Software Architecture documentation, and Qualcomm Developer Network references.
- Used for manufacturer-specific interface components (Hello UI, One UI), proprietary camera/audio HALs, and cellular radio integration daemons (RIL/IMS).

### Level 3: Forensic Manifest and Technical ADB Inspection
- Data extracted via `dumpsys package <package>` and decoded `AndroidManifest.xml` (AXML).
- Establishes mathematical certainty for:
  - **Shared User ID (`sharedUserId`):** packages sharing a UID run under identical system security contexts and cannot be isolated carelessly.
  - **System permissions (`protectionLevel: signature|privileged`):** reveals genuine runtime and signature privilege scope.
  - **Bound services (`Services/Providers`):** identifies client components consuming services via IPC (Binder).
  - **Installation flags:** `FLAG_SYSTEM`, `FLAG_UPDATED_SYSTEM_APP`, `FLAG_STOPPED`.

### Level 4: Operational Behavior Observed on Device
- Verification tests under controlled execution environments:
  - Memory footprint telemetry (`dumpsys meminfo <package>`).
  - Active network connections and sockets (`dumpsys netstats` / `netpolicy`).
  - System response to termination commands (`pm disable-user`, `am force-stop`).
  - Functional stress tests covering voice calls, SMS sending/receipt, biometric authentication, and banking applications.

### Level 5: Secondary Community Sources (UAD, XDA, F-Droid)
- Treated **exclusively as preliminary working hypotheses**, never as definitive technical proof.
- Community debloat lists (e.g. Universal Android Debloater repositories or XDA forum threads) frequently generalize package behavior across divergent Android versions or regional variants, demanding independent verification before any action.

---

## 3. Confidence Levels

Every classified package in this repository is assigned a formal confidence attribute:

| Confidence Level | Minimum Evidence Requirements | Permitted Claim |
| :--- | :--- | :--- |
| **`high`** | Verified via AOSP code (Level 1) or official OEM documentation (Level 2), corroborated by manifest/dumpsys data (Level 3) and live functional tests (Level 4). | Homologated for technical analysis and documentation. |
| **`medium`** | Supported by forensic manifest and dumpsys data (Level 3) with consistent operational behavior (Level 4), in the absence of formal public OEM documentation. | Valid for audit reports with documented limitations. |
| **`low`** | Predominantly based on community hypotheses (Level 5) or naming inference without extracted manifest evidence from the session. | Compulsorily flagged as `unverified` / pending. |

---

## 4. Requirements for Altered Packages

For every component disabled (`pm disable-user`) or removed (`pm uninstall --user 0`) on any documented device, the corresponding technical report must record:

1. **Canonical package identifier (`Package Name`):** exact FQPN format (e.g. `com.motorola.motocare`).
2. **Component origin:** stock AOSP, OEM (Motorola/Samsung), sponsored commercial partner, or chipset vendor (MediaTek/Qualcomm).
3. **Technical justification:** redundant telemetry, advertising, unnecessary resource consumption, or lack of personal utility.
4. **Verified dependencies:** absence of impact on essential system services and confirmation of `sharedUserId`.
5. **Rollback command:** exact command for immediate re-enablement (`pm enable` or `cmd package install-existing`).
6. **Observed functional outcome:** behavior confirmed on the device after intervention (e.g. "resident RAM process terminated; operating system integrity preserved").

If any of these attributes were not measured during the original collection session, the field must be formally designated as `not_measured` or `pending`, avoiding invented explanations.

---

## 5. Sampling Self-Audit Procedure

The project periodically executes probabilistic sampling audits:
1. **Documented pseudo-random seed (`seed`):** reproducible selection of packages from the catalog.
2. **Re-verification against primary sources:** each sampled package is re-evaluated against AOSP code, OEM specifications, and manifest dumps.
3. **Verdict report publication:** issuance of a report recording original classification, primary source consulted, verdict (*Agree*, *Disagree*, or *Insufficient Evidence*), and corrective action taken where discrepancies are found.
