# Audit status and homologation levels

This standard separates the publication of evidence from functional validation and script compatibility. A report, a successful test, and a homologated script are not interchangeable.

## Status levels

| Level | Label | Minimum evidence | Permitted claim |
|---|---|---|---|
| 0 | **Unassessed** | Device identity or evidence is insufficient to assess the audit | No compatibility or safety claim |
| 1 | **Inventory documented** | Identified manufacturer/model/build; collected and documented package inventory with provenance | Inventory was documented for this device/build |
| 2 | **Audit reviewed** | Package-level rationale, risks, dependencies, protected components, privacy sanitization, and reviewer checklist completed | Findings were reviewed; no functional approval implied |
| 3 | **Functional validation completed** | Explicit test matrix, test environment, outcomes, and limitations recorded on the exact device/build | Only the listed functions were tested successfully |
| 4 | **Script homologated** | Exact script/version, exact supported model/build scope, preflight and rollback checks, functional tests, reviewer approval, and reproducible evidence | Script is approved only for the explicitly listed scope |

## Rules

- Use the lowest level fully supported by evidence; do not infer higher status.
- Status applies to an exact manufacturer, model, variant, firmware/build, Android version, script version, and scope. Changes can invalidate approval.
- Homologation is **not** inferred from a report being published, packages being disabled, a device booting, or an unrelated device passing tests.
- A test not performed is **Not tested**; missing evidence is **Pending**; a failure is **Failed**. Do not convert these to “passed”.
- No broad labels such as “safe”, “approved for Android”, or “works on Samsung/Motorola” without bounded evidence.
- Any device-modifying action requires the owner’s explicit authorization. The status framework does not grant authorization.
- Include this record in each report:

| Field | Value |
|---|---|
| Audit status level | Level 0–4 |
| Device/model/variant | Exact value |
| Android/build/security patch | Exact value or Pending |
| Script name/version/hash | Exact value or Not applicable |
| Functional test matrix | Link or Not tested |
| Rollback/recovery evidence | Link or Pending |
| Reviewer/date | Name or pseudonym / date |
| Approved scope and exclusions | Explicit list |

## Translations

Portuguese version: [Níveis de status e homologação](AUDIT_STATUS_AND_HOMOLOGATION.pt-BR.md).
