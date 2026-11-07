# Auditorias de dispositivos Android

Este diretório reúne auditorias colaborativas do [**Clean My Android**](https://github.com/luisfvmartins/clean-my-android). Cada entrada corresponde a um dispositivo e documenta seu estado antes/depois, alterações realizadas, testes, evidências e limitações.

## Como contribuir

1. Siga o [guia de auditoria individual](../docs/USER_DEVICE_AUDIT.md).
2. Crie uma pasta exclusiva para seu dispositivo neste diretório (`reports/<fabricante-modelo>/`).
3. Inclua somente relatórios e evidências estritamente sanitizados (sem PII ou identificadores de hardware).
4. Adicione abaixo uma entrada com link para sua auditoria.
5. Envie a contribuição por Pull Request para a branch `main`.

Após a aprovação e o merge, a auditoria passa a fazer parte deste catálogo no repositório principal. Cada contribuição deve ser aditiva: não apague nem sobrescreva auditorias de outros dispositivos ou colaboradores. Atualizações de uma auditoria existente devem corresponder ao mesmo dispositivo e explicar a revisão realizada.

---

## Dispositivos auditados

| Dispositivo Comercial | Código de Modelo | Codename | SoC / Plataforma | Android / UI | Status da Auditoria | Documentação |
|---|---|---|---|---|---|---|
| **Motorola Edge 60 Pro** | `XT2507-1` | `cybert` | arm64-v8a | Pendente de confirmação | **Pendente de validação** (Auditoria documental concluída; SO e testes funcionais pendentes) | [📂 `motorola-edge-60-pro/`](motorola-edge-60-pro/README.md) |
| **Motorola Moto G54 5G** | `XT2343-1` | `cancunf` | MediaTek Dimensity 7020 | Android 15 (Hello UI) | Concluída / Homologada | [📄 `AUDITORIA_MOTO_G54_5G.md`](../docs/AUDITORIA_MOTO_G54_5G.md) |

---

## Estrutura padrão para novos relatórios

Cada dispositivo auditado neste diretório deve seguir o padrão:

```text
reports/<fabricante-modelo>/
├── README.md                  # Sumário executivo, destaques técnicos e resultados
├── auditoria.md               # Relatório forense detalhado e reproduzível
├── inventario-antes.json      # Todos os pacotes mapeados pré-debloat em JSON válido
├── inventario-depois.json     # Comparativo de pacotes pós-debloat em JSON válido
├── pacotes-desativados.txt    # Lista nominal dos pacotes em estado disabled-user
├── pacotes-desinstalados.txt  # Lista de pacotes desinstalados para o usuário 0
├── permissoes-alteradas.json  # Revogações de permissões, AppOps e regras de rede
├── comparativo.json          # Tabela de métricas quantitativas de desempenho
└── evidencias/
    └── README.md              # Proveniência, comandos ADB executados e sanitização
```

### Regras Mandatórias de Contribuição:
1. **Evidência Real:** Nunca gere relatórios baseados em suposições ou dados fictícios. Todo dado apresentado deve ter sido extraído via ADB (`dumpsys`, `pm`, `getprop`, `df`, `free`). Informações sem comprovação devem ser explicitamente marcadas como "Pendente de validação".
2. **Privacidade Absoluta (Zero PII):** Higienize previamente qualquer identificador pessoal ou de hardware (IMEI, MAC, Serial Number, contas de e-mail, tokens de API, números telefônicos e IPs reais).
3. **Estrutura Aditiva:** Contribuições de novos aparelhos nunca devem sobrescrever nem alterar relatórios de outros modelos existentes.
4. **Respeito ao Play Integrity e Estabilidade:** O debloat deve prezar pela manutenção de serviços essenciais de segurança e compatibilidade do sistema operacional.
