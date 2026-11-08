# Motorola Moto G54 5G — Technical Inventory

**Device:** Motorola Moto G54 5G · XT2343-1 · `cancunf`  
**System:** Android 15 · Hello UI  
**Main report:** [English audit summary](../../AUDITORIA_MOTO_G54_5G.en.md) · [Full report (Portuguese)](../../AUDITORIA_MOTO_G54_5G.md)

This folder contains the device's component inventory, split into batches for easier reading and review. The content was extracted from the original report without reclassifying packages or changing recommendations.

## Component inventory

| Batch | Scope | Items | File |
|---|---|---:|---|
| 2 | Google, GMS, Mainline APKs, and proprietary services | 30–111 (82) | [Batch 2](lote-02-ecossistema-google.md) |
| 3 | Motorola and Lenovo | 112–199 (88) | [Batch 3](lote-03-motorola-lenovo.md) |
| 4 | Commercial partners, carriers, and hardware | 200–224 (25) | [Batch 4](lote-04-parceiros-comerciais-e-hardware.md) |
| 5 | Android AOSP base system | 225–296 (72) | [Batch 5](lote-05-sistema-base-aosp.md) |
| 6 | AOSP, Google Mainline, and MediaTek RRO overlays | 297–358 (62) | [Batch 6](lote-06-overlays-aosp-google-mediatek.md) |
| 7 | Motorola overlays, regional carriers, and eUICC/eSIM | 359–423 (65) | [Batch 7](lote-07-overlays-motorola-operadoras-esim.md) |
| 8 | Project Mainline modules and APEX system modules | 424–462 (39) | [Batch 8](lote-08-modulos-project-mainline-apex.md) |

**Batch 1:** the 29 user-installed applications were intentionally omitted from the public version to protect the device owner's privacy.

## How to interpret this inventory

- The split is editorial and preserves the original inventory numbering.
- The audit describes one specific collection; do not generalize its conclusions to another device, region, or firmware.
- A risk classification is not authorization to disable or remove packages.
- See the main report for methodology, limitations, operational history, rollback, and recommendations.
- A published inventory does not mean a debloating script has been approved for this device.

The detailed batch files remain in Portuguese for now. The English audit summary links to all seven source batches. Package names, identifiers, commands, and technical evidence are preserved in their original form. Batch translations will be submitted separately to keep each review manageable.
