# Auditorias de dispositivos Android

Este catálogo reúne auditorias técnicas enviadas pela comunidade e incorporadas ao **Clean My Android** por Pull Requests. Cada dispositivo possui uma documentação própria para que resultados, limitações e recomendações não sejam generalizados para outros modelos.

**Princípio:** uma auditoria publicada é um registro técnico, não uma autorização para executar os mesmos comandos em outro aparelho.

## Catálogo

| Fabricante / modelo | Identificação | Android / interface | Situação e escopo | Relatório |
|---|---|---|---|---|
| **Motorola Moto G54 5G** | `XT2343-1` · `cancunf` | Android 15 · Hello UI | Inventário técnico publicado; consulte o relatório para distinguir observações, histórico e pendências | [Auditoria completa](../docs/AUDITORIA_MOTO_G54_5G.md) |
| **Motorola Edge 60 Pro** | `XT2507-1` · `cybert` | Hello UI · versão canônica pendente de confirmação | Relatório publicado; validação funcional e coleta complementar pendentes | [Abrir relatório](motorola-edge-60-pro/README.md) |

### Como interpretar os status

- **Inventário publicado:** há dados coletados e documentação disponível; isso não significa que todas as alterações foram testadas.
- **Validação pendente:** existem dados ou procedimentos que ainda precisam de confirmação no aparelho.
- **Homologado para script:** só deve ser usado quando houver validação explícita do script, do modelo e da versão do sistema. A compatibilidade do script não é inferida a partir da existência de um relatório.

## Como adicionar um dispositivo

1. Leia o [guia de auditoria individual](../docs/USER_DEVICE_AUDIT.md).
2. Crie uma pasta exclusiva em `reports/`, usando fabricante, modelo e versão Android quando necessário para diferenciar variantes.
3. Registre identificação, inventário inicial, alterações autorizadas, inventário final, comparativo e limitações.
4. Inclua somente arquivos sanitizados e necessários para verificar as conclusões.
5. Adicione uma linha neste catálogo com os dados confirmados e o status correto.
6. Envie a contribuição por Pull Request para a branch `main`.

### Estrutura recomendada

A estrutura pode ser simplificada quando uma coleta não estiver disponível. Não crie arquivos vazios nem invente resultados para preencher o modelo.

```text
reports/<fabricante-modelo-android>/
├── README.md                  # Sumário e status da auditoria
├── auditoria.md               # Método, evidências, análise e limitações
├── inventario-antes.json      # Inventário anterior às alterações
├── inventario-depois.json     # Inventário posterior às alterações
├── comparativo.json           # Métricas antes/depois e condições de coleta
├── pacotes-desativados.txt    # Registro do estado final, se aplicável
├── permissoes-alteradas.json  # Alterações documentadas, se aplicável
└── evidencias/
    └── README.md              # Proveniência e sanitização das evidências
```

## Regras de qualidade e privacidade

1. **Evidência real:** não publique dados simulados, inferências como fatos ou métricas sem método de coleta.
2. **Antes e depois comparáveis:** informe data, condições e comandos utilizados. Uma medição isolada não comprova ganho causado pela alteração.
3. **Separação de estados:** diferencie pacote instalado, habilitado, desabilitado e desinstalado para um usuário. Um snapshot histórico não é uma lista de execução.
4. **Sem recomendações universais:** uma lista de pacotes de um modelo não deve ser aplicada a outro modelo, região ou firmware.
5. **Sanitização obrigatória:** remova IMEI, serial, MAC, IP público ou identificável, contas, e-mails, números de telefone, tokens, chaves, notificações e dados pessoais.
6. **Dados brutos privados:** mantenha dumps completos localmente ou em armazenamento privado; publique apenas os trechos estritamente necessários.
7. **Contribuição aditiva:** não apague, substitua ou reescreva auditorias de outros dispositivos. Atualizações devem ser feitas na pasta do mesmo aparelho e explicar o motivo da revisão.
8. **Validação transparente:** marque explicitamente testes não executados e resultados inconclusivos.

## Fluxo de integração

```text
Coleta local
    ↓
Análise e autorização do proprietário
    ↓
Sanitização e revisão do material
    ↓
Fork + branch exclusiva
    ↓
Pull Request para main
    ↓
Revisão técnica e de privacidade
    ↓
Merge: auditoria incorporada ao catálogo
```

A abertura de um Pull Request não garante aprovação ou merge. Contribuições podem receber pedidos de correção quando faltarem evidências, houver exposição de dados pessoais ou recomendações inseguras.

Consulte [CONTRIBUTING.md](../CONTRIBUTING.md) para o fluxo de envio e o [guia de auditoria](../docs/USER_DEVICE_AUDIT.md) para os detalhes técnicos.
