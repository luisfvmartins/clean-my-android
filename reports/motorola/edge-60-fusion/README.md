# 📱 Motorola Edge 60 Fusion — Auditoria Técnica e Debloat

[![Dispositivo: Motorola Edge 60 Fusion](https://img.shields.io/badge/Dispositivo-Motorola%20Edge%2060%20Fusion-001435?logo=motorola&logoColor=white)](audit.md)
[![Codename: scout](https://img.shields.io/badge/Codename-scout-blue)](audit.md)
[![Android: 16 (API 36)](https://img.shields.io/badge/Android-16%20(API%2036)-green?logo=android&logoColor=white)](audit.md)
[![Status: Auditoria Concluída](https://img.shields.io/badge/Auditoria-Conclu%C3%ADda-brightgreen)](audit.md)
[![Clean My Android](https://img.shields.io/badge/Projeto-Clean%20My%20Android-green)](https://github.com/luisfvmartins/clean-my-android)

Este diretório contém a documentação técnica integral, inventários de pacotes antes e depois da intervenção, relatório comparativo de recursos e registro detalhado de alterações do **Motorola Edge 60 Fusion**.

---

## 📌 Identificação Técnica Comprovada

| Parâmetro Técnico | Identificação Comprovada via ADB |
| :--- | :--- |
| **Fabricante / Marca** | Motorola (`motorola`) |
| **Modelo Comercial** | Motorola Edge 60 Fusion |
| **Código do Produto / Modelo** | `motorola_edge_60_fusion` / `scout_g_sysn` |
| **Nome de Código (Codename / Board)** | `scout` / `mt6878` (MediaTek Dimensity 7300) |
| **Versão do Android** | Android 16 (API Level 36 - VanillaIceCream) |
| **Compilação do Firmware (Build ID)** | `W1VCS36H.14-20-19-9` |
| **Patch de Segurança** | 01/09/2026 |
| **Fingerprint da ROM** | `motorola/scout_g_sysn/scout:16/W1VCS36H.14-20-19-9/6e076a-c9e5e6:user/release-keys` |
| **Kernel do Linux** | `Linux 6.1.145-android14-11-g9b69cc399ae1-ab14819715 aarch64` |
| **Memória RAM Física** | 8 GB (`Total RAM: 7.594.168 KB`) |
| **Armazenamento Interno** | 256 GB UFS |
| **Canal de Software / Região** | Varejo Brasil (`retbr`) · Bootloader Bloqueado · Non-root |
| **Perfil de Usuário** | Usuário Primário (`User 0`) |

---

## 🎯 Escopo da Auditoria

O procedimento foi realizado sem privilégios de root, utilizando estritamente a interface **Android Debug Bridge (ADB)** com autorização expressa do proprietário:

1. **Mapeamento Exaustivo:** Todos os 486 pacotes presentes na ROM de fábrica foram catalogados e classificados tecnicamente.
2. **Neutralização de Rastreamento e Telemetria:** Desativação de daemons diagnósticos OEM da Motorola, telemetria SoC da MediaTek, histórico contínuo de localização 24/7 do Google e escuta passiva de microfone em hardware DSP RISCV ("Ok Google" / "Hey Google").
3. **Eliminação de Adware e Droppers Comerciais:** Desinstalação para o Usuário 0 de módulos com permissões abusivas de instalação de apps em background (`Digital Turbine Ignite`, `ironSource AppCloud`, `Meta Preloads`).
4. **Sandboxing de Permissões Críticas:** Revogação de permissão de satélite (`ACCESS_FINE_LOCATION`) em 19 aplicativos comerciais, delivery e birôs de crédito.
5. **Migração para Alternativas FOSS:** Substituição transparente do teclado proprietário (Gboard), discador, SMS, contatos, agenda, calculadora e gerenciador de arquivos por aplicativos livres sem conexão à internet.
6. **Preservação de Componentes Críticos e Escolhas do Usuário:** Proteção total do System UI, Motorola Launcher3 (gestos QuickStep), drivers de câmera, e aplicativos expressamente solicitados: **Gemini** (com preservação do app Google hospedeiro), **Fruit Merge**, **Calendário Menstrual** e **bancos** (Banco Inter e Nubank com Play Integrity 100% operacional).

---

## 📊 Síntese dos Resultados

- **Pacotes Catalogados no Firmware:** 486 pacotes
- **Pacotes Neutralizados:** 155 pacotes (67 desativados de fábrica + 88 neutralizados via ADB)
- **Pacotes Ativos no Usuário 0:** 343 pacotes (incluindo 12 novos aplicativos FOSS)
- **Memória RAM Livre:** Aumento de ~2.750 MB para **~4.153 MB a 4.573 MB livres** (**+1,40 GB a +1,82 GB de RAM disponível**, ganho de **+50.9% a +66.3%**)
- **Processos Residentes em Background:** Redução de 66 para 39 processos ativos (-27 daemons eliminados da RAM)
- **Status Funcional:** Testado e aprovado em chamadas, SMS, biometria, Wi-Fi, 4G/5G, câmera, Pix e bancos.

---

## 🗂️ Estrutura da Documentação

A documentação deste dispositivo está organizada nos seguintes arquivos:

- [📄 Relatório Técnico Completo (`audit.md`)](audit.md): Contexto, metodologia, análise detalhada dos 6 lotes de componentes, etapas de execução e conclusões.
- [📊 Relatório Comparativo Antes/Depois (`comparison-report.md`)](comparison-report.md): Indicadores técnicos, comparativo de RAM, permissões e testes funcionais.
- [📝 Registro Detalhado de Alterações (`changes/change-log.md`)](changes/change-log.md): Tabela detalhada de cada pacote modificado, justificativa, risco e método de reversão.
- [📋 Inventário Inicial — 486 Pacotes (`before/packages-initial.txt`)](before/packages-initial.txt): Relação dos pacotes antes do debloat.
- [📋 Inventário Final — 343 pacotes ativos / 344 listados (`after/packages-final.txt`)](after/packages-final.txt): Relação dos pacotes ativos pós-otimização (inclui registro de sistema inerte do Gboard).
- [🗄️ Dados Estruturados em JSON](comparativo.json): Métricas estruturadas validadas pelo repositório.

---

## 🧭 Navegação no Repositório

- [Catálogo Geral de Auditorias](../../README.pt-BR.md)
- [Estatísticas do Projeto](../../../docs/ESTATISTICAS.md)
- [Guia de Auditoria Individual](../../../docs/USER_DEVICE_AUDIT.pt-BR.md)


## Versões em inglês

- [Technical audit — English summary](audit.en.md)
- [Before/after comparison — English summary](comparison-report.en.md)
- [Change log — English summary](changes/change-log.en.md)
