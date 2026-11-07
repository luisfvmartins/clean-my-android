# 📊 Relatórios Técnicos de Auditoria de Dispositivos (Device Audits)

Bem-vindo à base de conhecimento técnico e relatórios de auditoria forense do projeto [**Clean My Android**](https://github.com/luisfvmartins/clean-my-android).

Aqui são arquivados os relatórios completos de engenharia reversa, análise de pacotes, debloat, de-google, sandboxing de permissões e telemetria para cada dispositivo Android testado em laboratório.

---

## 📱 Dispositivos Homologados e Auditados

| Dispositivo Comercial | Código de Modelo | Codename | SoC / Plataforma | Android / UI | Status da Auditoria | Pasta do Relatório |
|---|---|---|---|---|---|---|
| **Motorola Edge 60 Pro** | `XT2507-1` | `cybert` | arm64-v8a | Android 17 (Hello UI) | **Concluída / Homologada** | [📂 `motorola-edge-60-pro/`](motorola-edge-60-pro/README.md) |
| **Motorola Moto G54 5G** | `XT2343-1` | `cancunf` | MediaTek Dimensity 7020 | Android 15 (Hello UI) | **Concluída / Homologada** | [📄 `AUDITORIA_MOTO_G54_5G.md`](../docs/AUDITORIA_MOTO_G54_5G.md) |

---

## 🎯 Padrão Documental para Novos Relatórios

Cada dispositivo auditado deve possuir uma pasta exclusiva em `reports/<fabricante-modelo>/` contendo a seguinte estrutura padronizada:

```text
reports/<fabricante-modelo>/
├── README.md                  # Sumário executivo, destaques técnicos e resultados
├── auditoria.md               # Relatório forense exaustivo em 10 seções técnicas
├── inventario-antes.json      # Todos os componentes mapeados pré-debloat em JSON válido
├── inventario-depois.json     # Comparativo de estado pós-debloat em JSON válido
├── pacotes-desativados.txt    # Lista nominal dos pacotes em estado disabled-user
├── pacotes-desinstalados.txt  # Lista de pacotes desinstalados e purgas físicas
├── permissoes-alteradas.json  # Revogações de permissões, AppOps e regras de firewall
├── comparativo.json          # Tabela de métricas quantitativas de desempenho
└── evidencias/
    └── README.md              # Proveniência, comandos ADB executados e sanitização
```

### Regras Mandatórias de Contribuição:
1. **Evidência Real:** Nunca gere relatórios baseados em suposições ou dados fictícios. Todo dado apresentado deve ter sido extraído via ADB (`dumpsys`, `pm`, `getprop`, `df`, `free`).
2. **Privacidade Absoluta (Zero PII):** Higienize previamente qualquer identificador pessoal ou de hardware (IMEI, MAC, Serial Number, contas de e-mail, tokens de API, números telefônicos e IPs reais).
3. **Estrutura Aditiva:** Contribuições de novos aparelhos nunca devem sobrescrever nem alterar relatórios de outros modelos existentes.
4. **Respeito ao Play Integrity:** O debloat deve comprovar a manutenção de serviços essenciais de segurança e compatibilidade com aplicativos bancários.

---

## 🧭 Navegação

- Para consultar o relatório detalhado do **Motorola Edge 60 Pro**, acesse [**`reports/motorola-edge-60-pro/README.md`**](motorola-edge-60-pro/README.md).
- Para instruções de execução assistida por IA, consulte [**`AI_INSTRUCTIONS.md`**](../AI_INSTRUCTIONS.md).
- Para a suite de scripts automatizados, veja a pasta [**`scripts/`**](../scripts/).
