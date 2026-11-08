# Evolução das contribuições

Painel calculado com dados da API REST do GitHub. A contagem considera Pull Requests fechadas com campo merged_at preenchido; PRs rejeitadas ou fechadas sem merge não entram.

**Atualizado em:** 2026-11-08 23:03 UTC  
**Repositório:** [luisfvmartins/clean-my-android](https://github.com/luisfvmartins/clean-my-android)

## Indicadores

- **Pull Requests incorporadas:** 38
- **Autores distintos com PR incorporada:** 1
- **Dispositivos catalogados:** 3
- **Fabricantes representados:** 1

## Pull Requests incorporadas por ano

| Ano de incorporação | Pull Requests |
|---:|---:|
| 2026 | 38 |

## Escopo e limitações

- Autores distintos são contados pelo login GitHub associado ao autor da PR incorporada. Isso não equivale a pessoas verificadas ou membros ativos atuais.
- Uma PR representa uma contribuição integrada, mas pode conter vários arquivos ou dispositivos.
- Dispositivos e fabricantes vêm de data/device_catalog.json; atividade de PR vem da API GitHub.
- O painel não mede qualidade, linhas úteis, testes em aparelho ou homologação.
- Os dados refletem o repositório no momento da atualização.

## Atualização

O workflow Atualizar painel de contribuições gera as versões em português e inglês a partir da mesma resposta da API do GitHub. Executa após atualizações na branch main, diariamente e também pode ser iniciado manualmente pela aba Actions. Usa GITHUB_TOKEN fornecido pelo GitHub Actions; nenhum token pessoal é armazenado no repositório.

Consulte também as [estatísticas do projeto](ESTATISTICAS.md) e o [catálogo de auditorias](../reports/README.md).
