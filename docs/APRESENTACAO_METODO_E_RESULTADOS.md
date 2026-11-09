# Clean My Android — Apresentação Técnica do Método e Resultados

> **Metodologia de auditoria cirúrgica, debloat consciente, validação por evidências e governança de privacidade para Android.**

---

## 1. Visão Geral e Filosofia do Projeto

O **Clean My Android** estabelece um novo padrão técnico para a análise, limpeza (*debloat*) e otimização de dispositivos Android. Diferente de scripts de debloat genéricos ("one-click debloat") que desativam listas cegas de pacotes e frequentemente causam *bootloops*, perda de notificações bancárias ou quebra de chamadas de emergência, o projeto adota os seguintes pilares fundamentais:

```mermaid
flowchart LR
    A["1. Inspeção Baseline<br>(pm list, dumpsys, appops)"] --> B["2. Análise Pacote por Pacote<br>(Origem, Dependências, Risco)"]
    B --> C["3. Autorização Explícita<br>(Proprietário do Hardware)"]
    C --> D["4. Intervenção Cirúrgica Reversível<br>(pm disable-user / uninstall -k)"]
    D --> E["5. Validação Funcional Pós-Debloat<br>(Telefonia, Bancos, Biometria)"]
    E --> F["6. Publicação Sanitizada e CI<br>(Zero PII, Catálogo Estruturado)"]
```

### Princípios Irrenunciáveis
1. **Nunca Presumir Segurança Universal:** Android varia radicalmente entre fabricantes (Motorola Hello UI, Samsung One UI, Xiaomi HyperOS), arquiteturas de chip (Qualcomm, MediaTek, Exynos) e versões de firmware. Nenhuma intervenção é universalmente segura.
2. **Evidência sobre Inferência:** Nenhum número, ganho de memória RAM, autonomia de bateria ou comportamento térmico é declarado sem um dump ADB comprobatório correspondente.
3. **Reversibilidade Estrita:** Todos os pacotes são neutralizados mantendo seus binários intactos nas partições de sistema (`/system`, `/product`, `/vendor`), permitindo reversão imediata via `pm enable` ou `cmd package install-existing`.
4. **Proteção de Dados Pessoais (Zero PII):** Identificadores exclusivos de hardware (IMEI, MAC address, número de série), credenciais, contas e endereços de rede local são rigorosamente sanitizados antes de qualquer publicação pública.

---

## 2. Níveis de Status e Homologação Técnica

Para evitar que a simples publicação de um relatório seja interpretada como uma homologação definitiva de procedimentos, o projeto adota uma taxonomia formal em 5 níveis (conforme [docs/AUDIT_STATUS_AND_HOMOLOGATION.md](file:///home/luisfvmartins/clean-my-android/docs/AUDIT_STATUS_AND_HOMOLOGATION.md)):

| Nível | Classificação | Evidência Exigida | Declaração Permitida |
| :---: | :--- | :--- | :--- |
| **0** | **Não Avaliado** | Dados insuficientes para validar o modelo ou compilação | Nenhuma alegação de segurança ou compatibilidade |
| **1** | **Inventário Documentado** | Identificação completa do hardware/firmware e inventário bruto de pacotes com proveniência | Inventário documentado para o dispositivo/build específico |
| **2** | **Auditoria Revisada** | Justificativa técnica pacote por pacote, dependências, riscos, checagem contra lista protegida e sanitização de PII | Análise técnica revisada; sem aprovação funcional implícita |
| **3** | **Validação Funcional Concluída** | Matriz de testes funcionais, ambiente de medição antes/depois e limitações registradas no aparelho físico | Apenas as funções e subsistemas listados foram testados com sucesso |
| **4** | **Script Homologado** | Script específico com hash/versão, pré-checagens, rollback, testes funcionais repetíveis e aprovação comunitária | Script aprovado estritamente para o escopo e modelo declarados |

---

## 3. Dispositivos Auditados e Resultados Consolidados

O repositório documenta atualmente **4 dispositivos** de **2 fabricantes**, abrangendo **3 plataformas de processamento** e **3 versões principais do Android**:

| Dispositivo | Código / Codinome | Plataforma (SoC) | Android / UI | Nível de Homologação | Pacotes Firmware | Neutralizados | Habilitados Pós-Debloat |
| :--- | :--- | :--- | :--- | :---: | :---: | :---: | :---: |
| **Motorola Moto G54 5G** | `XT2343-1` · `cancunf` | MediaTek Dimensity 7020 | Android 15 · Hello UI | **Nível 1** (Inventário estruturado) | 462 locais | Inventário público: 433 | 394 sistema + 39 APEX |
| **Motorola Edge 60 Pro** | `XT2507-1` · `cybert` | Snapdragon 8 Gen 3/4 | Android 16 (Dev) · Hello UI | **Nível 2** (Auditoria revisada) | 501 mapeados | 253 neutralizados (60 fábrica + 184 ADB + 9 desinstalados) | 248 preservados |
| **Motorola Edge 60 Fusion** | `scout_g_sysn` · `scout` | Snapdragon 7s Gen 2/3 | Android 16 · Hello UI | **Nível 3** (Validação funcional) | 486 catalogados | 155 neutralizados (67 fábrica + 88 ADB) | 343 ativos (331 stock + 12 FOSS) |
| **Samsung Galaxy A30s** | `SM-A307GT` · `a30s` | Exynos 7904 | Android 11 · One UI 3.1 | **Nível 3** (Validação funcional) | 392 catalogados | 48 neutralizados (46 ADB + 2 desinstalados) | 343 habilitados (-12,3%) |

---

## 4. Destaques Técnicos por Plataforma

### 4.1 Samsung Galaxy A30s (Exynos 7904 · One UI 3.1)
* **Neutralização de Adware Silencioso:** Desativação do agente *Digital Turbine Ignite* (`com.dti.samsung`), bloqueando downloads silenciosos de aplicativos de parceiros em segundo plano.
* **Remoção de Throttling Artificial:** Desativação cirúrgica do *Game Optimizing Service (GOS)* (`com.samsung.android.game.gos`), restaurando o comportamento térmico nativo da CPU/GPU sem intervenção no kernel.
* **Eliminação de Telemetria Contínua:** Suspensão do *DiagMonAgent* (`com.sec.android.diagmonagent`) e do *IMS Logger* (`com.sec.imslogger`).
* **Estabilidade e Limitações Honestas:** Subsistemas vitais de telefonia, biometria e interface One UI preservados; ressalva documentada sobre a perda da função "Salvar como PDF" decorrente da desativação do spooler de impressão nativo.

### 4.2 Motorola Edge 60 Fusion (Qualcomm Snapdragon · Hello UI)
* **Substituição Consciente por Alternativas FOSS:** 12 aplicativos proprietários da Google/Motorola (Discador, Mensagens, Calendário, Calculadora, Contatos) foram substituídos por versões de código aberto sem rastreadores da suíte Fossify, FUTO e OpenCalc.
* **Preservação de Dependências Críticas:** Descoberta arquitetural de que o aplicativo Gemini (`com.google.android.apps.bard`) depende internamente do motor hospedeiro no Google App (`com.google.android.googlequicksearchbox`), levando à sua preservação deliberada para evitar quebras.
* **Validação Bancária:** Testes com aplicativos Banco Inter e Nubank atestando conformidade com a Google Play Integrity API após o debloat.

### 4.3 Motorola Edge 60 Pro (Flagship Qualcomm · Hello UI)
* **Mapeamento de Framework Avançado:** Inventário detalhado de 501 componentes. Identificação transparente de 18 pacotes que conflitam com a lista protegida básica, documentados com justificativa técnica individual e scripts de reversão.

### 4.4 Motorola Moto G54 5G (MediaTek Dimensity 7020)
* **Inventário Modular em Lotes:** 433 componentes públicos categorizados e documentados em 7 lotes técnicos especializados (Ecossistema Google, Serviços Motorola, Parceiros Comerciais, AOSP, Overlays e Módulos APEX Mainline).

---

## 5. Garantia de Qualidade e Governança Automatizada

O repositório é sustentado por uma esteira de automação contínua (CI) que impede regressões documentais ou técnicas:

```text
Scripts de Automação e Qualidade:
├── scripts/generate_statistics.py    # Sincroniza métricas e tabelas de dispositivos nos READMEs principais
├── scripts/validate_bilingual_parity.py # Assegura paridade e equivalência de pacotes/números entre PT-BR e EN
├── scripts/validate_repository.py     # Executa 440+ verificações de integridade de links, JSONs e níveis de homologação
├── data/device_catalog.json          # Fonte única da verdade estruturada para todos os dispositivos integrados
└── data/protected_essential_packages.txt # Lista protegida contra desativação de componentes vitais do sistema
```

* **Sincronização Automática:** Qualquer novo dispositivo adicionado a `data/device_catalog.json` é automaticamente refletido nos READMEs em português e inglês e nas páginas de estatísticas ao executar `generate_statistics.py`.
* **CI Bloqueante:** Pull Requests são rejeitados caso links locais estejam quebrados, dados numéricos divirjam entre as traduções ou relatórios de homologação não possuam as evidências exigidas.
