# Technical Audit — Motorola Moto G54 5G (XT2343-1)

**Manufacturer:** Motorola Mobility (Lenovo)  
**Commercial Model:** Moto G54 5G (`XT2343-1`)  
**Codename / Hardware:** `cancunf` · MediaTek Dimensity 7020 (MT6855)  
**Operating System:** Android 15 · Motorola Hello UI  
**Homologation Level:** Level 1 (Inventory documented)

---

## 1. Executive Summary and Scope

This technical audit presents the structured inventory and architectural assessment of **462 components** present on the factory firmware of the **Motorola Moto G54 5G** smartphone running Android 15.

The public repository version omits 29 user-installed third-party apps and documents in full **433 components**:
* 394 system packages, Motorola customizations, carrier packages, and Google GMS services.
* 39 containerized Project Mainline modules (APEX).

---

## 2. Canonical Inventory by Analysis Batches

To ensure thorough technical review, components were classified into 7 documented batches:

1. **Google Ecosystem and GMS Services:** [`docs/auditorias/moto-g54/lote-02-ecossistema-google.en.md`](../../../docs/auditorias/moto-g54/lote-02-ecossistema-google.en.md)
2. **Motorola/Lenovo Components and Customizations:** [`docs/auditorias/moto-g54/lote-03-motorola-lenovo.en.md`](../../../docs/auditorias/moto-g54/lote-03-motorola-lenovo.en.md)
3. **Commercial Partners and Carriers:** [`docs/auditorias/moto-g54/lote-04-parceiros-comerciais-e-hardware.en.md`](../../../docs/auditorias/moto-g54/lote-04-parceiros-comerciais-e-hardware.en.md)
4. **Base AOSP System and Framework:** [`docs/auditorias/moto-g54/lote-05-sistema-base-aosp.en.md`](../../../docs/auditorias/moto-g54/lote-05-sistema-base-aosp.en.md)
5. **AOSP, Google, and MediaTek Overlays:** [`docs/auditorias/moto-g54/lote-06-overlays-aosp-google-mediatek.en.md`](../../../docs/auditorias/moto-g54/lote-06-overlays-aosp-google-mediatek.en.md)
6. **Motorola Overlays and Carrier / eSIM:** [`docs/auditorias/moto-g54/lote-07-overlays-motorola-operadoras-esim.en.md`](../../../docs/auditorias/moto-g54/lote-07-overlays-motorola-operadoras-esim.en.md)
7. **Containerized Project Mainline APEX Modules:** [`docs/auditorias/moto-g54/lote-08-modulos-project-mainline-apex.en.md`](../../../docs/auditorias/moto-g54/lote-08-modulos-project-mainline-apex.en.md)

The structured consolidated inventory is located in [`before/inventory.json`](before/inventory.json) and [`data/inventory_moto_g54.json`](../../../data/inventory_moto_g54.json).

---

## 3. Limitations and Homologation Level

* **Level 1 Homologation:** Publication of this inventory documents firmware baseline and provenance. Batch debloat procedures are not homologated in this report.
* **Script Safety:** Executing debloat operations via `./debloat.sh --apply` requires preflight validation against `data/apply_support.tsv` and `data/protected_essential_packages.txt`.

---

## 4. Navigation

* [Device README](README.en.md)
* [Detailed Audit Report (Methodology & Conclusions)](../../../docs/AUDITORIA_MOTO_G54_5G.en.md)
* [Canonical Metrics (JSON)](metrics.json)
* [Functional Tests Matrix](functional-tests.json)
