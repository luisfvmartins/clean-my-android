# Auditoria Técnica — Motorola Moto G54 5G (XT2343-1)

**Fabricante:** Motorola Mobility (Lenovo)  
**Modelo Comercial:** Moto G54 5G (`XT2343-1`)  
**Codinome / Hardware:** `cancunf` · MediaTek Dimensity 7020 (MT6855)  
**Sistema Operacional:** Android 15 · Motorola Hello UI  
**Status de Homologação:** Nível 1 (Inventário documentado)

---

## 1. Sumário Executivo e Escopo

Esta auditoria técnica apresenta o inventário estruturado e a análise arquitetural de **462 componentes** presentes no firmware de fábrica do smartphone **Motorola Moto G54 5G** executando o Android 15.

A versão pública do repositório omite 29 aplicativos de uso estritamente pessoal instalados pelo usuário e documenta integralmente **433 componentes** do sistema:
* 394 pacotes de sistema, serviços da Motorola, operadoras e ecossistema Google.
* 39 módulos conteinerizados do Project Mainline (APEX).

---

## 2. Inventário Canônico por Lotes de Análise

Para viabilizar uma revisão técnica rigorosa e detalhada, os componentes foram categorizados em 7 lotes documentais:

1. **Ecossistema Google e Serviços GMS:** [`docs/auditorias/moto-g54/lote-02-ecossistema-google.md`](../../../docs/auditorias/moto-g54/lote-02-ecossistema-google.md)
2. **Componentes e Customizações Motorola/Lenovo:** [`docs/auditorias/moto-g54/lote-03-motorola-lenovo.md`](../../../docs/auditorias/moto-g54/lote-03-motorola-lenovo.md)
3. **Parceiros Comerciais e Operadoras:** [`docs/auditorias/moto-g54/lote-04-parceiros-comerciais-e-hardware.md`](../../../docs/auditorias/moto-g54/lote-04-parceiros-comerciais-e-hardware.md)
4. **Sistema Base AOSP e Framework:** [`docs/auditorias/moto-g54/lote-05-sistema-base-aosp.md`](../../../docs/auditorias/moto-g54/lote-05-sistema-base-aosp.md)
5. **Overlays AOSP, Google e MediaTek:** [`docs/auditorias/moto-g54/lote-06-overlays-aosp-google-mediatek.md`](../../../docs/auditorias/moto-g54/lote-06-overlays-aosp-google-mediatek.md)
6. **Overlays Motorola e Operadoras / eSIM:** [`docs/auditorias/moto-g54/lote-07-overlays-motorola-operadoras-esim.md`](../../../docs/auditorias/moto-g54/lote-07-overlays-motorola-operadoras-esim.md)
7. **Módulos Conteinerizados Project Mainline (APEX):** [`docs/auditorias/moto-g54/lote-08-modulos-project-mainline-apex.md`](../../../docs/auditorias/moto-g54/lote-08-modulos-project-mainline-apex.md)

O inventário estruturado consolidado encontra-se em [`before/inventory.json`](before/inventory.json) e [`data/inventory_moto_g54.json`](../../../data/inventory_moto_g54.json).

---

## 3. Limitações e Status de Homologação

* **Nível 1 de Homologação:** A publicação do inventário documenta o estado do firmware e a proveniência dos pacotes. Procedimentos de debloat em lote não foram homologados para este modelo no escopo deste relatório.
* **Segurança dos Scripts:** A execução de desativações via script (`debloat.sh --apply`) neste modelo exige validação prévia contra o gate de aplicação (`data/apply_support.tsv`) e a lista de pacotes protegidos (`data/protected_essential_packages.txt`).

---

## 4. Navegação

* [README do Aparelho](README.md)
* [Relatório Detalhado de Metodologia e Conclusões](../../../docs/AUDITORIA_MOTO_G54_5G.md)
* [Métricas Canônicas (JSON)](metrics.json)
* [Matriz de Testes Funcionais](functional-tests.json)
