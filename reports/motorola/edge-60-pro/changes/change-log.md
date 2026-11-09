# Histórico de Alterações — Motorola Edge 60 Pro (`XT2507-1`)

Este documento consolida o registro técnico de todas as alterações executadas durante a sessão de auditoria e debloat no **Motorola Edge 60 Pro**.

---

## 1. Pacotes Desativados para o Usuário 0 (`pm disable-user --user 0`)

Foram desativados **244 pacotes**, discriminados integralmente em [`disabled-packages.txt`](disabled-packages.txt).
* **Adwares, Bloatwares e Parceiros OOBE:** 11 componentes (Digital Turbine, IronSource Aura, Glance, Taboola, InMobi).
* **Telemetria de Fabricante e Operadoras Estrangeiras:** Overlays e stubs de operadoras internacionais (AT&T, Telekom, Orange) e daemons de marketing Motorola.
* **Componentes Google Opcionais:** Desativação seletiva de bloatwares pré-instalados preservando a integridade do sistema operacional.

---

## 2. Pacotes Desinstalados para o Usuário 0 (`pm uninstall -k --user 0`)

Foram removidos para o Usuário 0 **9 pacotes**, listados em [`removed-packages.txt`](removed-packages.txt):
* 2 aplicativos de terceiros purgados de `/data/app` (adwares instalados previamente via DT Ignite).
* 7 stubs de sistema desinstalados em nível de usuário.

---

## 3. Revogação Cirúrgica de Permissões e AppOps

As revogações de permissões em tempo de execução e configurações de AppOps foram realizadas manualmente e estão registradas em [`permission-changes.json`](permission-changes.json):
* 13 permissões sensíveis de localização, microfone e contatos revogadas para pacotes não essenciais.
* Sandboxing de AppOps aplicado a UIDs específicos. Conforme [`docs/MANUAL_CHANGES.md`](../../../../docs/MANUAL_CHANGES.md), não há automação para essas etapas.
