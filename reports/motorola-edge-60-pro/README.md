# 📱 Relatório Consolidado de Auditoria e Debloat — Motorola Edge 60 Pro (`XT2507-1`)

[![Dispositivo: Motorola Edge 60 Pro](https://img.shields.io/badge/Dispositivo-Motorola%20Edge%2060%20Pro-001435?logo=motorola&logoColor=white)](auditoria.md)
[![Codename: cybert](https://img.shields.io/badge/Codename-cybert-blue)](auditoria.md)
[![Android: 15 (API 35)](https://img.shields.io/badge/Android-15%20(API%2035)-3DDC84?logo=android&logoColor=white)](auditoria.md)
[![Status: Homologado](https://img.shields.io/badge/Auditoria-Homologada%20em%20Laborat%C3%B3rio-success)](auditoria.md)
[![Clean My Android](https://img.shields.io/badge/Projeto-Clean%20My%20Android-green)](https://github.com/luisfvmartins/clean-my-android)

Este diretório contém a documentação técnica integral, inventários de pacotes (antes e depois), métricas de desempenho e histórico detalhado das ações de debloat, sandboxing e privacidade executadas no smartphone **Motorola Edge 60 Pro (`XT2507-1`)**, codinome **`cybert`**, rodando a interface **Hello UI** sobre o **Android 15**.

---

## 📌 Sumário Executivo

O procedimento de debloat e hardening foi conduzido via **Android Debug Bridge (ADB)** sem a necessidade de root, garantindo **zero degradação funcional**, **100% de compatibilidade com aplicativos bancários brasileiros (Play Integrity intacto)** e **eliminação completa de adwares, telemetrias e instaladores silenciosos de fábrica**.

### Principais Destaques do Resultado:
- **501 componentes** mapeados no inventário inicial do firmware.
- **244 pacotes congelados** (`pm disable-user --user 0`) de forma reversível.
- **9 aplicativos desinstalados** para o usuário principal (incluindo adwares instalados silenciosamente via DT Ignite).
- **10 purgas físicas de APKs atualizados em `/data/app`**, liberando **mais de 4 GB** de armazenamento interno.
- **7 bloatwares com proteção de firmware (`non-disable`)** paralisados cirurgicamente via **AppOps por UID** e incluídos na blacklist de rede em segundo plano do kernel (`netpolicy`).
- **Sandboxing do Google Play Services (`com.google.android.gms`)**: 11 permissões runtime revogadas e 6 permissões `SYSTEM_FIXED` (Localização, Sensores Corporais e Reconhecimento de Atividade) neutralizadas via AppOps (`ignore`), transformando o GMS em um túnel mudo de atestação e push.
- **Perfis fantasmas encerrados**: Perfil `User 11` parado (`am stop-user -f 11`) e `User 10` removido, eliminando instâncias duplicadas do GMS da memória RAM (-269 MB RSS).
- **Ganho de Memória RAM:** De ~4.5 GB livres para **~7.2 GB livres** (**+2.7 GB de RAM disponível**, aumento de **58,7%**).
- **Temperatura Térmica em Espera:** Redução de **37°C–40°C** para **33.0°C**.

---

## 📊 Comparativo Resumido de Recursos

| Indicador | Antes do Debloat | Depois do Debloat | Variação Real |
|---|---|---|---|
| **Memória RAM Livre** | ~4.5 GB | **~7.2 GB** | **+2.7 GB livres** (+58,7%) |
| **Armazenamento Livre (`/data`)** | 193 GB livres | **197 GB a 200 GB** | **+4 GB a +7 GB recuperados** |
| **Total de Pacotes Registrados** | 501 pacotes | **492 pacotes** | -9 pacotes do usuário |
| **Aplicativos Habilitados** | 441 pacotes ativos | **257 pacotes ativos** | -184 pacotes ativos |
| **Aplicativos Desativados** | 60 pacotes | **244 pacotes** | +184 pacotes congelados |
| **Adwares em Execução na RAM** | Glance, Taboola, InMobi, DTI | **ZERO adwares** | 100% limpo |
| **Google QuickSearchBox em RAM** | 873 MB RSS | **0 MB (eliminado)** | -873 MB RSS |
| **Perfis Ativos em Background** | User 0 + User 11 | **Apenas User 0** | -269 MB RSS duplicado |
| **Temperatura em Espera** | 37°C a 40°C | **33.0°C** | Aparelho frio e estável |
| **Apps de Banco (Caixa, Nubank, PicPay)** | Funcionais | **100% Funcionais** | Play Integrity preservado |

---

## 🗂️ Estrutura de Arquivos deste Relatório

```text
reports/motorola-edge-60-pro/
├── README.md                  # Este documento (visão geral e sumário executivo)
├── auditoria.md               # Relatório técnico completo e exaustivo de auditoria
├── inventario-antes.json      # Inventário completo dos 501 componentes pré-debloat
├── inventario-depois.json     # Estado final dos 501 componentes pós-debloat
├── pacotes-desativados.txt    # Lista nominal dos 244 pacotes desativados
├── pacotes-desinstalados.txt  # Lista dos pacotes desinstalados e purgas físicas
├── permissoes-alteradas.json  # Detalhamento de revogações, AppOps e Netpolicy
├── comparativo.json          # Métricas técnicas de hardware e software em JSON
└── evidencias/
    └── README.md              # Proveniência, comandos ADB e cadeia de custódia
```

---

## 🛡️ Síntese da Arquitetura de Defesa Aplicada

```
+-------------------------------------------------------------------------+
| [Camada 1: Debloat em Massa]                                            |
| 244 pacotes congelados via "pm disable-user --user 0"                   |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 2: Purgador Físico de Armazenamento]                           |
| Remoção de APKs atualizados em /data/app (+4 GB livres recuperados)     |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 3: Sandboxing de Permissões & AppOps por UID]                   |
| GMS enjaulado (retorno nulo de GPS/sensores) + Quarentena de bloqueados |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 4: Blindagem de Rede & DNS]                                     |
| Netpolicy background blacklist + NextDNS sinkholing de telemetria       |
+-------------------------------------------------------------------------+
```

---

## 🔗 Navegação e Referências

- 📖 [**Relatório Completo de Auditoria Forense (`auditoria.md`)**](auditoria.md)
- 📋 [**Inventário Antes (`inventario-antes.json`)**](inventario-antes.json)
- 📋 [**Inventário Depois (`inventario-depois.json`)**](inventario-depois.json)
- ⚙️ [**Permissões e AppOps Alterados (`permissoes-alteradas.json`)**](permissoes-alteradas.json)
- 📊 [**Comparativo de Desempenho (`comparativo.json`)**](comparativo.json)
- 🔒 [**Cadeia de Custódia e Evidências (`evidencias/README.md`)**](evidencias/README.md)
- 🏠 [**Voltar ao Índice Geral de Relatórios (`reports/README.md`)**](../README.md)
