# Record of Manual Interventions (AppOps and Permissions)

This document records the policy of the **Clean My Android** project regarding runtime permission modifications (`pm revoke`) and application operations (`cmd appops`).

---

## 1. Intentional Absence of Automation

The **Clean My Android** project **does not provide automated scripts** for batch alteration of permissions or AppOps.

This technical decision is rooted in fundamental Android stability and security principles:
1. **Shared UID Risks (`sharedUserId`):** Changing AppOps directly on a UID can unexpectedly corrupt or disable other essential system packages sharing the same security identity.
2. **Foreground Dependencies:** Arbitrary background permission revocations can cause abrupt crashes (*Force Close / ANR*) when an app is launched interactively by the user.
3. **Policy Persistence:** Many AppOps configurations do not survive OS reboots or OTA firmware updates with the same reliability as package-level state flags.

---

## 2. Samsung Galaxy A30s

In the audit of the **Samsung Galaxy A30s (SM-A307GT)**, as documented in canonical files:
* [`reports/samsung/galaxy-a30s/changes/appops-changes.txt`](../reports/samsung/galaxy-a30s/changes/appops-changes.txt): **No individual AppOps were modified.**
* [`reports/samsung/galaxy-a30s/changes/permission-changes.txt`](../reports/samsung/galaxy-a30s/changes/permission-changes.txt): **No manifest-level permissions were modified individually.**

All approved interventions on the Galaxy A30s were strictly limited to disabling (`pm disable-user --user 0`) 46 packages and user-level removal (`pm uninstall -k --user 0`) of 2 factory packages.

---

## 3. Motorola Edge 60 Pro and Edge 60 Fusion

For Motorola Edge devices where surgical revocations of telemetry permissions or AppOps sandboxing were performed:
* All interventions were executed **exclusively manually**, package by package, by the reviewing auditor.
* The exact executed commands, revoked permissions, and technical justifications are recorded in [`reports/motorola/edge-60-pro/changes/permission-changes.json`](../reports/motorola/edge-60-pro/changes/permission-changes.json) and in the Edge 60 Fusion change log ([`reports/motorola/edge-60-fusion/changes/change-log.md`](../reports/motorola/edge-60-fusion/changes/change-log.md)).
* No automated tool in the repository (`debloat.sh` or otherwise) executes or will execute these commands automatically.
