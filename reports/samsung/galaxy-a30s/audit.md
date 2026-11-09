# Auditoria Técnica — Samsung Galaxy A30s (SM-A307GT)

**Fabricante:** Samsung Electronics  
**Modelo Comercial:** Galaxy A30s (`SM-A307GT`)  
**Plataforma / SoC:** Samsung Exynos 7904 (14nm Octa-core)  
**Sistema Operacional:** Android 11 · Samsung One UI 3.1  
**Status de Homologação:** Nível 3 (Validação funcional de subsistemas concluída; ressalva em impressão PDF)

---

## 1. Sumário Executivo e Metodologia

Esta auditoria técnica documenta a análise e otimização cirúrgica do smartphone **Samsung Galaxy A30s**. A inspeção inicial via Android Debug Bridge (ADB) identificou **392 pacotes catalogados** na partição de sistema de fábrica (`/system`, `/product`, `/apex` e stubs em `/data`).

O objetivo foi desativar pacotes de publicidade invasiva (Digital Turbine Ignite), agentes de diagnóstico em segundo plano e componentes desnecessários, preservando integralmente o subsistema telefônico RIL, biometria e a usabilidade do One UI.

---

## 2. Inventário Inicial e Lotes de Análise

O inventário inicial completo está registrado em [`before/packages.txt`](before/packages.txt) e [`before/inventory.json`](before/inventory.json).

As alterações foram conduzidas em dois lotes autorizados:
* **Lote 1 (Agentes Comerciais e Publicidade):** Desativação do *Digital Turbine Ignite* (`com.dti.samsung`), serviços de telemetria da Meta/Facebook (`com.facebook.katana`, `com.facebook.system`, `com.facebook.appmanager`, `com.facebook.services`), e Game Optimizing Service (`com.samsung.android.game.gos`).
* **Lote 2 (Diagnósticos e Recursos Não Utilizados):** Desativação de agentes de telemetria diagnóstica e métricas como *DiagMonAgent* (`com.sec.android.diagmonagent`), *IMS Logger* (`com.sec.imslogger`), e stubs comerciais de terceiros.

A lista completa das 46 desativações e 2 desinstalações para o Usuário 0 encontra-se em:
* [`changes/disabled-packages.txt`](changes/disabled-packages.txt)
* [`changes/removed-packages.txt`](changes/removed-packages.txt)

---

## 3. Avaliação de Riscos e Componentes Protegidos

Nenhum componente essencial de telefonia (`com.android.phone`, `com.android.server.telecom`), serviços de autenticação biométrica ou interface de usuário foi alterado. 

Conforme documentado em [`changes/appops-changes.txt`](changes/appops-changes.txt) e [`docs/MANUAL_CHANGES.md`](../../../docs/MANUAL_CHANGES.md), nenhum AppOps ou permissão de manifesto foi alterado isoladamente, evitando riscos de efeitos colaterais em pacotes com UIDs compartilhados.

---

## 4. Limitações e Regressão Identificada

* **Impressão / Salvar como PDF:** A desativação de `com.android.printspooler` causou a perda da funcionalidade nativa de salvar páginas como PDF. A limitação foi aceita pelo usuário e motivou a blindagem permanente desse pacote no arquivo de proteção global do projeto (`data/protected_essential_packages.txt`).
* **Telemetria residual:** A suspensão de daemons específicos limita o tráfego gerado por eles, mas não assegura a cessação de telemetria geral do ecossistema Google ou Samsung em nível de kernel ou serviços vitais (efeito geral: [não medido](comparison-report.md)).

---

## 5. Navegação e Arquivos Canônicos

* [Relatório Comparativo Antes/Depois](comparison-report.md)
* [Resumo do Dispositivo (README)](README.md)
* [Métricas Canônicas (JSON)](metrics.json)
* [Matriz de Testes Funcionais](functional-tests.json)
