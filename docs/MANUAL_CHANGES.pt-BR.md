# Registro de Intervenções Manuais (AppOps e Permissões)

Este documento registra a política do projeto **Clean My Android** referente a permissões em nível de runtime (`pm revoke`) e operações de modo de aplicação (`cmd appops`).

---

## 1. Ausência Intencional de Automação

O projeto **Clean My Android** **não fornece nem disponibiliza scripts automatizados** para modificação em lote de permissões ou AppOps. 

Essa decisão técnica decorre de princípios fundamentais de segurança e estabilidade do Android:
1. **Riscos de Privilégios Compartilhados (`sharedUserId`):** Alterar AppOps diretamente em um UID pode corromper ou bloquear inesperadamente outros pacotes essenciais do sistema que compartilham a mesma identidade de segurança.
2. **Dependências em Primeiro Plano:** Revogações arbitrárias de permissões em segundo plano podem causar encerramento forçado (*Force Close / ANR*) de aplicativos no momento em que o usuário os aciona interativamente.
3. **Persistência de Políticas:** Muitas regras de AppOps não sobrevivem a reinicializações de sistema ou atualizações OTA da mesma forma que desativações explícitas de pacotes.

---

## 2. Samsung Galaxy A30s

Na auditoria do **Samsung Galaxy A30s (SM-A307GT)**, conforme registrado nos arquivos canônicos:
* [`reports/samsung/galaxy-a30s/changes/appops-changes.txt`](../reports/samsung/galaxy-a30s/changes/appops-changes.txt): **Nenhum AppOps individual foi alterado.**
* [`reports/samsung/galaxy-a30s/changes/permission-changes.txt`](../reports/samsung/galaxy-a30s/changes/permission-changes.txt): **Nenhuma permissão em nível de manifesto foi alterada individualmente.**

Todas as intervenções aprovadas e realizadas no A30s limitaram-se estritamente à desativação (`pm disable-user --user 0`) de 46 pacotes e à desinstalação para o Usuário 0 (`pm uninstall -k --user 0`) de 2 pacotes de fábrica.

---

## 3. Motorola Edge 60 Pro e Edge 60 Fusion

Para os dispositivos da linha Motorola Edge onde foram realizadas revogações cirúrgicas de permissões de telemetria ou restrições de AppOps:
* Todas as intervenções foram executadas **exclusivamente de forma manual**, pacote por pacote, pelo auditor responsável.
* Os comandos exatos executados, as permissões revogadas e suas respectivas justificativas técnicas encontram-se documentados em [`reports/motorola/edge-60-pro/changes/permission-changes.json`](../reports/motorola/edge-60-pro/changes/permission-changes.json) e no histórico de mudanças do Edge 60 Fusion ([`reports/motorola/edge-60-fusion/changes/change-log.md`](../reports/motorola/edge-60-fusion/changes/change-log.md)).
* Nenhuma ferramenta automatizada do repositório (`debloat.sh` ou similar) executa ou executará tais comandos automaticamente.
