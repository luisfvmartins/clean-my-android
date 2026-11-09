# 📱 Relatório Consolidado de Auditoria e Debloat — Motorola Edge 60 Pro (`XT2507-1`)


> **Nota de privacidade:** os identificadores dos 50 registros classificados como componentes de terceiros foram pseudonimizados. Os caminhos específicos de instalação em `/data/app` foram normalizados. As contagens agregadas e os estados registrados dos pacotes foram preservados. O inventário de origem não permite determinar se esses componentes foram instalados pelo usuário ou pré-carregados por um fornecedor.

[![Dispositivo: Motorola Edge 60 Pro](https://img.shields.io/badge/Dispositivo-Motorola%20Edge%2060%20Pro-001435?logo=motorola&logoColor=white)](auditoria.md)
[![Codename: cybert](https://img.shields.io/badge/Codename-cybert-blue)](auditoria.md)
[![Android: 17](https://img.shields.io/badge/Android-17%20(SDK%2037)-green?logo=android&logoColor=white)](auditoria.md)
[![Status: Nível 3 (Validação Funcional)](https://img.shields.io/badge/Homologa%C3%A7%C3%A3o-N%C3%ADvel%203-brightgreen)](case-study-play-integrity.md)
[![Clean My Android](https://img.shields.io/badge/Projeto-Clean%20My%20Android-green)](https://github.com/luisfvmartins/clean-my-android)

Este diretório contém a documentação técnica integral, inventários de pacotes (antes e depois), métricas de desempenho e histórico detalhado das ações de debloat, sandboxing e privacidade executadas no smartphone **Motorola Edge 60 Pro (`XT2507-1`)**, codinome **`cybert`**, rodando a interface **Hello UI** sobre o **Android 17** (API Level 37, compilação `7a1c2-08c719` confirmada via `getprop`).

---

## 📌 Sumário Executivo

> [!CAUTION]
> **Conflito com a lista de componentes protegidos e resolução empírica:** uma revisão posterior encontrou 18 pacotes presentes tanto em `pacotes-desativados.txt` quanto em `data/protected_essential_packages.txt`. A interseção incluía `com.android.vending` (Google Play Store).
>
> **Resolução em 09/11/2026:** Em validação funcional de uso real, a desativação de `com.android.vending` causou a falha de inicialização dos aplicativos governamentais **CNH Digital** e **GOV.BR** (Play Integrity API). O pacote foi reativado via ADB juntamente com os módulos de integridade associados, restabelecendo a operação plena de ambos os serviços. O histórico detalhado e evidências constam no [Estudo de Caso de Play Integrity](case-study-play-integrity.md).

O procedimento de debloat e sandboxing foi conduzido via **Android Debug Bridge (ADB)** sem root. Foram mapeados todos os pacotes de fábrica, desativados daemons de rastreamento e telemetria, neutralizados instaladores patrocinados e isolados serviços protegidos por firmware.

> [!NOTE]
> **Status da Auditoria: Nível 3 (Validação Funcional de Integridade Aprovada)**
> A versão canônica do sistema foi confirmada como **Android 17** (SDK 37). A validação de atestação do Play Integrity foi homologada com sucesso após a reativação da Play Store. Testes exaustivos de voz, SMS e consumo de bateria em 24h permanecem catalogados para acompanhamento contínuo.

### Principais Destaques do Procedimento:
- **501 componentes** mapeados no inventário inicial do firmware.
- **244 pacotes desativados** (`pm disable-user --user 0`) de forma reversível.
- **9 pacotes desinstalados para o Usuário 0**: 2 aplicativos de terceiros purgados integralmente e 7 pacotes de sistema marcados como `installed=false`.
- **Reversão de atualizações em `/data/app`** para 10 pacotes de sistema desativados, contribuindo para um aumento agregado de **~4 GB de espaço livre em `/data`** (de 193 GB para ~197 GB; ganho por aplicativo não mensurado individualmente).
- **7 bloatwares com proteção de firmware (`non-disable`)** paralisados cirurgicamente via **AppOps por UID** e incluídos na blacklist de rede em segundo plano do kernel (`netpolicy`).
- **Sandboxing do Google Play Services (`com.google.android.gms` / UID 10387)**: 6 operações protegidas (Localização Precisa/Aproximada, Monitoramento Contínuo, Sensores Corporais e Reconhecimento de Atividade) configuradas para retorno nulo via AppOps (`ignore`), afetando os processos vinculados ao UID 10387.
- **13 permissões runtime revogadas** via `pm revoke --user 0` e 2 tentativas de revogação de permissão especial documentadas.
- **Perfis secundários encerrados**: Perfil fantasma `User 11` parado (`am stop-user -f 11`) e `User 10` removido, eliminando a duplicação de processos do GMS na memória RAM (-269 MB RSS).
- **Memória RAM Livre:** De ~4.5 GB livres para **~7.2 GB livres** (**+2.7 GB de RAM disponível**, aumento de **58,7%** registrado no Passo 384).
- **Comportamento Térmico em Repouso:** Redução de **37°C–40°C** para **33.0°C**.

---

## 📊 Comparativo Resumido de Recursos

| Indicador | Antes do Debloat | Depois do Debloat | Variação Observada |
|---|---|---|---|
| **Memória RAM Livre** | ~4.5 GB | **~7.2 GB** | **+2.7 GB livres** (+58,7%) |
| **Armazenamento Livre (`/data`)** | 193 GB livres | **~197 GB livres** | **~4 GB recuperados** (ganho agregado da partição; não mensurado por app) |
| **Total de Pacotes do Usuário** | 501 pacotes | **492 pacotes** | -9 pacotes desinstalados para o Usuário 0 |
| **Aplicativos Habilitados** | 441 pacotes ativos | **248 pacotes preservados/ativos** | -193 pacotes ativos (184 desativados + 9 desinstalados para o Usuário 0) |
| **Aplicativos Desativados** | 60 pacotes de fábrica | **244 pacotes** | +184 pacotes desativados via ADB |
| **Adwares Monitorados em RAM** | Glance, Taboola, InMobi ativos (~750 MB RSS) | **Processos finalizados** | Daemons paralisados na sessão |
| **Google QuickSearchBox em RAM** | 873 MB RSS | **0 MB** | Processo eliminado da memória RAM |
| **Perfis Ativos em Background** | User 0 + User 11 | **Apenas User 0 ativo** | -269 MB RSS de instâncias duplicadas |
| **Temperatura em Repouso** | 37°C a 40°C | **33.0°C** | Dispositivo frio e estável |
| **Play Integrity / Apps de Banco** | Não coletado na sessão inicial | **Validado com sucesso (09/11/2026)** | CNH e GOV.BR operando após reativação da Play Store |

> **Nota de reconciliação:** um resumo operacional anterior registrava 257 pacotes habilitados. Esse valor não coincide com os 248 pacotes classificados como preservados/ativos no inventário final. Como a saída bruta do comando não está publicada para conferência, 257 não é tratado como valor confirmado; o comparativo utiliza a classificação do inventário estruturado.

---

## 🗂️ Estrutura de Arquivos deste Relatório

```text
reports/motorola/edge-60-pro/
├── README.md                  # Este documento (visão geral e sumário executivo)
├── auditoria.md               # Relatório técnico completo, reproduzível e auditado
├── case-study-play-integrity.md  # Estudo de caso: incidente, reversão e validação da Play Store
├── inventario-antes.json      # Inventário completo dos 501 componentes pré-debloat
├── inventario-depois.json     # Estado consolidado dos 501 componentes pós-debloat
├── pacotes-desativados.txt    # Lista nominal histórica dos 244 pacotes desativados
├── pacotes-desinstalados.txt  # Lista dos 9 pacotes desinstalados e notas de atualização
├── permissoes-alteradas.json  # Detalhamento de revogações, AppOps e Netpolicy
├── comparativo.json          # Métricas técnicas de desempenho e status de testes em JSON
└── evidencias/
    ├── README.md              # Proveniência, comandos ADB e cadeia de custódia
    └── 01-erro-play-integrity-cnh-gov.jpg  # Registro fotográfico do erro de integridade
```

---

## 🛡️ Síntese da Estrutura de Otimização Aplicada

```
+-------------------------------------------------------------------------+
| [Camada 1: Desativação em Nível de Usuário]                             |
| 244 pacotes colocados em disabled-user via "pm disable-user --user 0"   |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 2: Remoção de Atualizações de Sistema em /data/app]             |
| Reversão de 10 pacotes à imagem de fábrica (~4 GB livres agregados)     |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 3: Sandboxing de Permissões & AppOps por UID]                   |
| GMS (UID 10387) com retorno nulo de GPS/sensores + Quarentena de travados |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 4: Blindagem de Rede & DNS]                                     |
| Netpolicy blacklist de background por UID + NextDNS sinkholing          |
+-------------------------------------------------------------------------+
```

---

## 🔗 Navegação e Referências

- 📖 [**Relatório Completo de Auditoria Forense (`auditoria.md`)**](auditoria.md)
- 🔍 [**Estudo de Caso e Validação de Play Integrity (`case-study-play-integrity.md`)**](case-study-play-integrity.md)
- 📋 [**Inventário Antes (`inventario-antes.json`)**](inventario-antes.json)
- 📋 [**Inventário Depois (`inventario-depois.json`)**](inventario-depois.json)
- ⚙️ [**Permissões e AppOps Alterados (`permissoes-alteradas.json`)**](permissoes-alteradas.json)
- 📊 [**Comparativo de Desempenho (`comparativo.json`)**](comparativo.json)
- 🔒 [**Evidências e Coleta Complementar (`evidencias/README.md`)**](evidencias/README.md)
- 🏠 [**Voltar ao Catálogo Geral de Relatórios (`reports/README.md`)**](../../README.pt-BR.md)


## Resumo histórico

- [Resumo histórico (Português)](historical-summary.pt-BR.md)
- [Historical report — English summary](historical-summary.en.md)
