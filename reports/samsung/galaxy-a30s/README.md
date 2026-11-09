# 📱 Samsung Galaxy A30s — Auditoria Técnica e Otimização Cirúrgica

[![Dispositivo: Samsung Galaxy A30s](https://img.shields.io/badge/Dispositivo-Samsung%20Galaxy%20A30s-002f6c?logo=samsung&logoColor=white)](comparison-report.md)
[![Codename: a30s](https://img.shields.io/badge/Codename-a30s-blue)](comparison-report.md)
[![Android: 11 (One UI 3.1)](https://img.shields.io/badge/Android-11%20(One%20UI%203.1)-green?logo=android&logoColor=white)](comparison-report.md)
[![Status: Auditoria Concluída](https://img.shields.io/badge/Auditoria-Conclu%C3%ADda-brightgreen)](comparison-report.md)
[![Clean My Android](https://img.shields.io/badge/Projeto-Clean%20My%20Android-green)](https://github.com/luisfvmartins/clean-my-android)

Este diretório contém a documentação técnica integral, inventários de pacotes antes e depois da intervenção, relatório comparativo de recursos e registro detalhado de alterações do smartphone **Samsung Galaxy A30s (SM-A307GT)**.

---

## 📌 Identificação Técnica Comprovada

| Parâmetro Técnico | Identificação Comprovada via ADB |
| :--- | :--- |
| **Fabricante / Marca** | Samsung (`samsung`) |
| **Modelo Comercial** | Samsung Galaxy A30s |
| **Código do Modelo** | `SM-A307GT` |
| **Produto / Codename** | `a30sdtvvj` / `a30s` |
| **Plataforma / Processador** | Samsung Exynos 7904 Octa-Core (`universal7904`) |
| **Arquitetura / ABI** | 64-bit `arm64-v8a` (`exynos7904`) |
| **Versão do Android** | Android 11 (API Level 30) |
| **Interface de Usuário** | One UI 3.1 (Samsung Experience Platform SEP `120100`) |
| **Compilação do Firmware (Build)** | `RP1A.200720.012.A307GTVJS5CWE2` |
| **Patch de Segurança** | 01/05/2023 (Patch final do ciclo de vida) |
| **Canal / Região CSC** | `ZTO` (Brasil - Varejo / Desbloqueado) |
| **Kernel do Linux** | `Linux 4.4.177-22825772 aarch64` |
| **Memória RAM Física** | 4 GB LPDDR4x (`Total RAM: 3.813.448 KB`) |
| **Armazenamento Interno** | 64 GB eMMC 5.1 (partição `/data` com 51 GB brutos) |
| **Estado do Bootloader** | Desbloqueado (`ro.boot.flash.locked: 0`, `ro.boot.verifiedbootstate: orange`) |
| **Privilégios de Execução** | Non-root (`uid=2000 shell`) |
| **Perfil de Usuário** | Usuário Primário (`User 0`) |

---

## 🎯 Escopo da Otimização Cirúrgica (Lotes 1 e 2)

O procedimento foi executado em modo não-root via **Android Debug Bridge (ADB)** com autorização explícita do proprietário:

1. **Diagnóstico e Inventário Exaustivo:** Todos os 392 pacotes do firmware foram catalogados e analisados em `before/inventory.json`.
2. **Remoção de Bloatware Comercial & Adware Oculto:** Desinstalação de parceiros comerciais (`com.odete.samsung` e loja `com.samsung.shop`) e desativação do dropper comercial **Digital Turbine Ignite** (`com.dti.samsung`).
3. **Erradicação da Telemetria Central:** Neutralização do **Samsung DiagMonAgent**, **IMS Logger**, **NetworkDiagnostic**, **Samsung Find My Mobile** e do **Google Location History 24/7**.
4. **Erradicação do Ecossistema Meta / Facebook:** Desativação de 4 componentes em segundo plano (`katana`, `system`, `appmanager`, `services`).
5. **Desbloqueio de Throttling Samsung (GOS):** Neutralização do *Game Optimizing Service* (`com.samsung.android.game.gos`) e satélites (`gamehome`, `gametools`), eliminando a limitação artificial de frequência de CPU/GPU do Exynos 7904.
6. **Alívio de Daemons Ociosos e Multimídia:** Desativação do *Dynamic Lock Screen*, *Story Service*, módulos de AR/Stickers (*AR Emoji*, *Live Stickers*, *Google ARCore*) e daemons de varredura (*Easy Setup BLE/Wi-Fi*, *AllShare* e *Spooler de Impressão*).
7. **Preservação de Subsistemas Vitais:** O teclado ativo (Samsung HoneyBoard), launcher (One UI Home), subsistema telefônico/RIL/IMS e Google Play Services/Store foram preservados sem modificação, mantendo a estabilidade operacional e compatibilidade bancária observadas nos testes.

---

## 📊 Síntese dos Resultados

- **Pacotes Catalogados no Firmware:** 392 pacotes (393 no `inventory.json` incluindo a biblioteca estática Trichrome)
- **Pacotes Habilitados Antes:** 391 pacotes
- **Pacotes Habilitados Depois:** 343 pacotes (**-48 pacotes no Usuário 0 / -12,3%**)
- **Pacotes Desativados:** 47 pacotes (1 de fábrica + 46 desativados cirurgicamente via disable-user)
- **Pacotes Comerciais Desinstalados (User 0):** 2 pacotes (`com.odete.samsung` e `com.samsung.shop`)
- **Total de Pacotes Neutralizados:** 48 pacotes
- **Estabilidade e Conectividade:** Subsistemas essenciais validados em sessão (Wi-Fi, Bluetooth, Telefonia, Biometria e Google Play Services).

---

## 📂 Estrutura de Documentos

- [`comparison-report.md`](comparison-report.md): Relatório comparativo detalhado de antes e depois.
- [`comparativo.json`](comparativo.json): Métricas estruturadas legíveis por máquina.
- [`before/`](before/): Diagnóstico inicial de linha de base (inventário, logs de memória, bateria, processos e permissões).
- [`changes/`](changes/): Registro de execução, comandos utilizados e métodos de reversão.
- [`after/`](after/): Diagnóstico final confirmatório pós-otimização.

## Documentos em inglês

- [Before/after comparison — English summary](comparison-report.en.md)
- [Change log — English summary](changes/change-log.en.md)

## Navegação

- [Voltar ao Catálogo Geral de Relatórios](../../README.pt-BR.md)
