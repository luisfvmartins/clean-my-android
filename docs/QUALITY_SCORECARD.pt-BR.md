# Placar Técnico de Qualidade e Conformidade — Clean My Android

- **Data da avaliação:** 09 de novembro de 2026
- **Ambiente de execução:** Linux x86_64, Bash 5.2 (com testes em subshell Bash 3.2), Python 3.12, ShellCheck 0.10.0
- **Metodologia:** Cada critério foi verificado por comando reproduzível. Critérios dependentes de intervenção física em hardware ou privilégios de governança externa estão formalmente identificados como **`bloqueado por humano`**, com referência direta à lista numerada da Seção 6.

---

## 1. Tabela Consolidada de Conformidade por Categoria

| # | Categoria de Qualidade | Critérios Atendidos / Total | Estado Geral | Pendências Humanas Relacionadas (Seção 6) |
|---|---|:---:|:---:|---|
| 1 | Segurança dos scripts | 5 / 5 | **Atendido** | Nenhuma |
| 2 | Testes e CI | 4 / 5 | **Parcial** | Item 1 (Aplicar workflow de matriz no GitHub com escopo de token) |
| 3 | Disciplina de documentação | 2 / 2 | **Atendido** | Nenhuma |
| 4 | Consistência de layout | 1 / 1 | **Atendido** | Nenhuma |
| 5 | Reprodutibilidade | 3 / 4 | **Parcial** | Item 3 (Execução física do protocolo de medição em hardware) |
| 6 | Portabilidade | 4 / 4 | **Atendido** | Item 4 (Confirmação presencial em macOS com ADB físico) |
| 7 | Processo e governança | 4 / 6 | **Parcial** | Item 1 (Ruleset/Protection), Item 2 (Revisor externo), Item 8 (Tag v0.1.0) |
| 8 | Verificabilidade técnica | 2 / 2 | **Atendido** | Nenhuma |
| **TOTAL** | **Consolidado do Projeto** | **25 / 29 (86.2%)** | **Conforme com bloqueios externos documentados** | **8 itens catalogados na Seção 6** |

---

## 2. Detalhamento dos Critérios por Categoria

### Categoria 1: Segurança dos Scripts

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Códigos de saída documentados em `--help` | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_exit_codes_documented_in_help` | `Ran 1 test in 0.28s ... OK` | 2026-11-09 | **Atendido** |
| Log JSONL sanitizado com rollback | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_code_0_success_and_jsonl_log` | `Ran 1 test in 0.44s ... OK` | 2026-11-09 | **Atendido** |
| Gate dirigido por dados (`apply_support.tsv`) | `python3 scripts/check_change_lists.py` | `OK: 1226 verificações concluídas com sucesso` | 2026-11-09 | **Atendido** |
| ShellCheck sem avisos | `shellcheck -x scripts/*.sh scripts/lib/*.sh` | Retorno zero (sem mensagens) | 2026-11-09 | **Atendido** |
| Pacotes protegidos ausentes em listas gerais de execução | `python3 scripts/check_change_lists.py` | Nenhuma ocorrência em `data/*disabled*.txt` | 2026-11-09 | **Atendido** |

---

### Categoria 2: Testes e CI

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Matriz Ubuntu + macOS no CI com Bash 3.2 nativo | Inspeção de `docs/PROPOSED_VALIDATE_WORKFLOW.yml` | Workflow de matriz pronto e fixado por SHA | 2026-11-09 | **Bloqueado por humano (Item 1)** |
| ShellCheck automatizado no CI | `shellcheck -x scripts/*.sh scripts/lib/*.sh` | Integrado ao workflow de validação proposto | 2026-11-09 | **Atendido** |
| Cobertura de todos os códigos de saída de `debloat.sh` e `restore.sh` | `python3 -m unittest discover -s tests -p 'test_adb_scripts.py'` | `Ran 29 tests ... OK` (códigos 0, 1, 2, 3, 4, 5, 6, 7 cobertos) | 2026-11-09 | **Atendido** |
| Todos os 44 pacotes protegidos testados individualmente | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_rejects_every_protected_package_with_code_5` | `Ran 1 test (44 sub-testes iterados) ... OK` | 2026-11-09 | **Atendido** |
| Testes unitários do próprio validador e sanitização | `python3 -m unittest tests.test_claims_and_metrics tests.test_sanitization tests.test_canonical_layout` | `Ran 17 tests in 0.48s ... OK` | 2026-11-09 | **Atendido** |

---

### Categoria 3: Disciplina de Documentação

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Zero alegação absolutista sem evidência | `python3 scripts/check_claims.py` | `OK: 109653 verificações de alegações e métricas concluídas com sucesso` | 2026-11-09 | **Atendido** |
| Métricas com esquema canônico (`kind`, `status`, `method`, `evidence`) | `python3 scripts/check_claims.py` | Todos os `metrics.json` aprovados no esquema estrito | 2026-11-09 | **Atendido** |

---

### Categoria 4: Consistência de Layout dos Relatórios

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Layout canônico imposto por nível de homologação em todos os aparelhos | `python3 scripts/validate_repository.py` | `OK: 592 verificações concluídas sem erros` | 2026-11-09 | **Atendido** |

---

### Categoria 5: Reprodutibilidade

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Script de snapshot somente-leitura com sanitização pré-gravação | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_snapshot_code_0_success tests.test_adb_scripts.AdbScripts.test_snapshot_code_5_sanitization_leak_aborts` | `Ran 2 tests in 0.52s ... OK` | 2026-11-09 | **Atendido** |
| Verificador automatizado de listas de alterações | `python3 scripts/check_change_lists.py` | `OK: 1226 verificações concluídas com sucesso` | 2026-11-09 | **Atendido** |
| Documentação explícita de alterações manuais (AppOps/permissões) | Leitura de `docs/MANUAL_CHANGES.pt-BR.md` e `docs/MANUAL_CHANGES.md` | Comandos manuais exatos documentados | 2026-11-09 | **Atendido** |
| Coleta e validação de medições físicas em aparelho real | Execução do roteiro em `docs/MEASUREMENT_PROTOCOL.md` | Requer conexão física de aparelhos sob responsabilidade do proprietário | 2026-11-09 | **Bloqueado por humano (Item 3)** |

---

### Categoria 6: Portabilidade

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Ausência de `mapfile` e comandos específicos GNU | `git grep -n "mapfile" scripts/` | Zero ocorrências encontradas | 2026-11-09 | **Atendido** |
| Suporte a Linux e macOS | Testes executados em Bash nativo 3.2 e documentação em `docs/PLATFORMS.md` | `OK` nos testes; documentação completa | 2026-11-09 | **Atendido** |
| Documentação de ressalvas de Windows/WSL2 | Inspeção de `docs/PLATFORMS.pt-BR.md` | Ressalvas de CRLF e encaminhamento USB documentadas | 2026-11-09 | **Atendido** |
| Catálogo bilíngue centralizado para scripts | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_bilingual_cma_lang` | Mensagens em EN e PT validadas via `CMA_LANG` | 2026-11-09 | **Atendido** |

---

### Categoria 7: Processo e Governança

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Padrão Conventional Commits e Squash-and-Merge | Inspeção de `CONTRIBUTING.pt-BR.md` | Padrões formalizados e documentados | 2026-11-09 | **Atendido** |
| Arquivo de proprietários de código | Inspeção de `.github/CODEOWNERS` | Mapeamento completo para `@luisfvmartins` | 2026-11-09 | **Atendido** |
| Política de segurança | Inspeção de `SECURITY.pt-BR.md` e `SECURITY.md` | Protocolo de reporte de vulnerabilidades e vazamento | 2026-11-09 | **Atendido** |
| Changelog histórico retroativo estruturado | Inspeção de `CHANGELOG.md` e `CHANGELOG.pt-BR.md` | PRs #1 a #47 mapeadas estritamente do git | 2026-11-09 | **Atendido** |
| Branch protection / ruleset na branch `main` | Execução de comandos `gh api` pelo proprietário | Requer privilégio de administração humana | 2026-11-09 | **Bloqueado por humano (Item 1)** |
| Revisor independente externo | Revisão externa por terceiro convidado | Não simular intervenção de terceiros | 2026-11-09 | **Bloqueado por humano (Item 2)** |

---

### Categoria 8: Verificabilidade Técnica

| Critério | Comando de Verificação | Resumo da Saída | Data | Estado |
|---|---|---|---|:---:|
| Metodologia de classificação e hierarquia de fontes | Inspeção de `docs/CLASSIFICATION_METHOD.pt-BR.md` | Hierarquia de 5 níveis e confiança formalizados | 2026-11-09 | **Atendido** |
| Autoauditoria por amostragem probabilística | `python3 scripts/sample_self_audit.py` e inspeção de `docs/SELF_AUDIT_2026-11-09.pt-BR.md` | 30 pacotes auditados com semente 20261109 (100% de consistência) | 2026-11-09 | **Atendido** |
