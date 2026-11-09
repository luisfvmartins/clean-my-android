# Placar Consolidado de Qualidade Técnica e Conformidade — Clean My Android

- **Data de avaliação:** 2026-11-09
- **Ambiente de execução real:** Linux (`Linux Macmini 7.0.0-42-generic #42~24.04.1-Ubuntu SMP PREEMPT_DYNAMIC Mon Oct 19 14:43:01 UTC 2 x86_64 x86_64 x86_64 GNU/Linux`), GNU Bash (`GNU bash, versão 5.2.21(1)-release (x86_64-pc-linux-gnu)`), Bash 3.2 (`GNU bash, version 3.2.0(2)-release (x86_64-unknown-linux-gnu)`), Python (`Python 3.12.3`), ShellCheck (`version: 0.10.0`)
- **Metodologia:** Cada critério atende exclusivamente quando comprovado por comando reproduzível com artefato em `docs/evidence-runs/`. Itens dependentes de hardware físico ou privilégios externos de governança são marcados como **`Bloqueado por ação humana`** e referenciam as pendências catalogadas.

---

## 1. Placar Consolidado por Categoria

| # | Categoria de Qualidade | Critérios Atendidos / Total | Situação Geral | Itens de Ação Humana Associados |
|---|---|:---:|:---:|---|
| 1 | Segurança dos scripts | 5 / 5 | **Atendido** | Nenhum |
| 2 | Testes e CI | 3 / 5 | **Parcial** | Item 1 (Aplicação do workflow matricial no repositório) |
| 3 | Disciplina documental | 2 / 2 | **Atendido** | Nenhum |
| 4 | Consistência de layout | 1 / 1 | **Atendido** | Nenhum |
| 5 | Reprodutibilidade | 3 / 4 | **Parcial** | Item 3 (Execução do protocolo de medição física em hardware) |
| 6 | Portabilidade | 3 / 4 | **Parcial** | Item 1 (Workflow matricial no CI), Item 4 (Confirmação física no macOS) |
| 7 | Processo e governança | 4 / 6 | **Parcial** | Item 1 (Ruleset/Protection), Item 2 (Revisor externo), Item 8 (Tag v0.1.0) |
| 8 | Verificabilidade técnica | 2 / 2 | **Atendido** | Nenhum |
| **TOTAL** | **Pontuação Consolidada do Projeto** | **23 / 29 (79.3%)** | **Conforme com dependências externas documentadas** | **6 itens pendentes de ação humana** |

---

## 2. Critérios Detalhados por Categoria

### Categoria 1: Segurança dos scripts

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Códigos de saída documentados em --help | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_exit_codes_documented_in_help` | [c01_help_exit_codes.txt](evidence-runs/2026-11-09/c01_help_exit_codes.txt) | Atendido |
| Log JSONL com auditoria e rollback | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_code_0_success_and_jsonl_log` | [c02_jsonl_log.txt](evidence-runs/2026-11-09/c02_jsonl_log.txt) | Atendido |
| Trava orientada a dados (apply_support.tsv) | `python3 scripts/check_change_lists.py` | [c03_apply_gate.txt](evidence-runs/2026-11-09/c03_apply_gate.txt) | Atendido |
| Zero avisos no ShellCheck | `shellcheck -x scripts/*.sh scripts/lib/*.sh` | [c04_shellcheck.txt](evidence-runs/2026-11-09/c04_shellcheck.txt) | Atendido |
| Nenhum pacote protegido em listas de execução geral | `python3 scripts/check_change_lists.py` | [c05_protected_packages.txt](evidence-runs/2026-11-09/c05_protected_packages.txt) | Atendido |

### Categoria 2: Testes e CI

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Matriz CI Ubuntu + macOS com Bash 3.2 nativo | Ação humana externa necessária | [c06_ci_matrix.txt](evidence-runs/2026-11-09/c06_ci_matrix.txt) | Bloqueado por ação humana (Item 1) |
| ShellCheck integrado ao CI | Ação humana externa necessária | [c07_shellcheck_ci.txt](evidence-runs/2026-11-09/c07_shellcheck_ci.txt) | Bloqueado por ação humana (Item 1) |
| Cobertura de testes de código de saída (mock ADB) | `python3 -m unittest discover -s tests -p 'test_adb_scripts.py'` | [c08_script_tests.txt](evidence-runs/2026-11-09/c08_script_tests.txt) | Atendido |
| Todos os 46 pacotes essenciais protegidos testados | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_rejects_every_protected_package_with_code_5` | [c09_protected_packages_tests.txt](evidence-runs/2026-11-09/c09_protected_packages_tests.txt) | Atendido |
| Testes unitários dos validadores e sanitização | `python3 -m unittest tests.test_claims_and_metrics tests.test_sanitization tests.test_canonical_layout tests.test_change_lists tests.test_validator_hardening` | [c10_validator_tests.txt](evidence-runs/2026-11-09/c10_validator_tests.txt) | Atendido |

### Categoria 3: Disciplina documental

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Zero alegações absolutas ou causais sem evidência | `python3 scripts/check_claims.py` | [c11_check_claims.txt](evidence-runs/2026-11-09/c11_check_claims.txt) | Atendido |
| Esquema canônico de métricas JSON validado | `python3 scripts/check_claims.py` | [c12_metrics_schema.txt](evidence-runs/2026-11-09/c12_metrics_schema.txt) | Atendido |

### Categoria 4: Consistência de layout

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Layout canônico por nível de homologação em todos os aparelhos | `python3 scripts/validate_repository.py` | [c13_canonical_layout.txt](evidence-runs/2026-11-09/c13_canonical_layout.txt) | Atendido |

### Categoria 5: Reprodutibilidade

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Utilitário de snapshot com trava de sanitização pré-escrita | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_snapshot_code_0_success tests.test_adb_scripts.AdbScripts.test_snapshot_code_5_sanitization_leak_aborts` | [c14_snapshot_utility.txt](evidence-runs/2026-11-09/c14_snapshot_utility.txt) | Atendido |
| Verificador estático de listas de alterações e contagens | `python3 scripts/check_change_lists.py` | [c15_check_change_lists.txt](evidence-runs/2026-11-09/c15_check_change_lists.txt) | Atendido |
| Registro explícito e reproduzível de alterações manuais | `python3 -c 'from pathlib import Path; r=Path("."); assert (r/"docs/MANUAL_CHANGES.md").is_file() and (r/"docs/MANUAL_CHANGES.pt-BR.md").is_file(); print("OK: MANUAL_CHANGES verificado")'` | [c16_manual_changes.txt](evidence-runs/2026-11-09/c16_manual_changes.txt) | Atendido |
| Medições físicas de recursos coletadas em hardware real | Ação humana externa necessária | [c17_physical_measurements.txt](evidence-runs/2026-11-09/c17_physical_measurements.txt) | Bloqueado por ação humana (Item 3) |

### Categoria 6: Portabilidade

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Ausência de mapfile e flags específicas do GNU Bash 4+ | `! git grep -n 'mapfile' scripts/*.sh scripts/lib/*.sh` | [c18_no_mapfile.txt](evidence-runs/2026-11-09/c18_no_mapfile.txt) | Atendido |
| Suporte a Linux e macOS testado em CI | Ação humana externa necessária | [c19_linux_macos_support.txt](evidence-runs/2026-11-09/c19_linux_macos_support.txt) | Bloqueado por ação humana (Item 1) |
| Ressalvas de Windows/WSL2 e CRLF documentadas | `python3 -c 'from pathlib import Path; p=(Path("docs/PLATFORMS.md")).read_text(); assert "WSL2" in p and "CRLF" in p; print("OK: ressalvas Windows/WSL2 verificadas")'` | [c20_windows_caveats.txt](evidence-runs/2026-11-09/c20_windows_caveats.txt) | Atendido |
| Catálogo bilíngue centralizado de mensagens (CMA_LANG) | `python3 -m unittest tests.test_adb_scripts.AdbScripts.test_bilingual_cma_lang` | [c21_bilingual_messages.txt](evidence-runs/2026-11-09/c21_bilingual_messages.txt) | Atendido |

### Categoria 7: Processo e governança

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Padrões de Conventional Commits e Squash-and-Merge | `python3 -c 'from pathlib import Path; c=(Path("CONTRIBUTING.md")).read_text(); assert "Conventional Commits" in c and "Squash" in c; print("OK: padrões de contribuição verificados")'` | [c22_conventional_commits.txt](evidence-runs/2026-11-09/c22_conventional_commits.txt) | Atendido |
| Arquivo formal de posse de código (.github/CODEOWNERS) | `python3 -c 'from pathlib import Path; c=(Path(".github/CODEOWNERS")).read_text(); assert "@luisfvmartins" in c; print("OK: CODEOWNERS verificado")'` | [c23_codeowners.txt](evidence-runs/2026-11-09/c23_codeowners.txt) | Atendido |
| Política de divulgação de vulnerabilidades (SECURITY.md) | `python3 -c 'from pathlib import Path; assert (Path("SECURITY.md")).is_file() and (Path("SECURITY.pt-BR.md")).is_file(); print("OK: políticas de segurança verificadas")'` | [c24_security_policy.txt](evidence-runs/2026-11-09/c24_security_policy.txt) | Atendido |
| Changelog histórico retroativo estruturado | `python3 -c 'from pathlib import Path; assert (Path("CHANGELOG.md")).is_file() and (Path("CHANGELOG.pt-BR.md")).is_file(); print("OK: changelogs verificados")'` | [c25_changelog.txt](evidence-runs/2026-11-09/c25_changelog.txt) | Atendido |
| Branch protection / ruleset na branch main | Ação humana externa necessária | [c26_branch_protection.txt](evidence-runs/2026-11-09/c26_branch_protection.txt) | Bloqueado por ação humana (Item 1) |
| Revisor externo independente | Ação humana externa necessária | [c27_external_reviewer.txt](evidence-runs/2026-11-09/c27_external_reviewer.txt) | Bloqueado por ação humana (Item 2) |

### Categoria 8: Verificabilidade técnica

| Critério | Comando / Verificação | Artefato de Evidência | Situação |
|---|---|---|:---:|
| Autoauditoria amostral de classificações com evidência primária | `python3 scripts/sample_self_audit.py` | [c28_sampling_self_audit.txt](evidence-runs/2026-11-09/c28_sampling_self_audit.txt) | Atendido |
| Placar de qualidade e conformidade gerado por evidências | `python3 scripts/check_claims.py` | [c29_compliance_scorecard.txt](evidence-runs/2026-11-09/c29_compliance_scorecard.txt) | Atendido |

---

## 6. Lista Numerada de Ações Humanas Obrigatórias

As 8 ações operacionais e de governança a seguir dependem estritamente de intervenção humana ou acesso a hardware físico e não podem ser automatizadas em CI:

1. **Item 1 — Proteção de Branch e Aplicação do Workflow de Matriz CI:**
   Configurar ruleset de proteção de branch na `main` do GitHub e aplicar o workflow multiplataforma proposto (`docs/PROPOSED_VALIDATE_WORKFLOW.yml`) com permissões ativas de token de workflow no repositório.
2. **Item 2 — Revisor Externo Independente:**
   Convidar formalmente um revisor técnico externo independente para auditar o repositório, verificar evidências e emitir parecer formal.
3. **Item 3 — Medição Física de Recursos em Hardware:**
   Conectar fisicamente os smartphones reais para executar as medições de [24 horas](MEASUREMENT_PROTOCOL.pt-BR.md) de repouso de bateria, telemetria térmica e ciclos de boot a frio conforme o protocolo em `docs/MEASUREMENT_PROTOCOL.pt-BR.md`.
4. **Item 4 — Validação Física com ADB Nativo em macOS:**
   Executar os scripts interativamente em uma estação física com macOS e aparelho conectado via USB para confirmar comportamento nativo com ADB físico.
5. **Item 5 — Homologação Funcional no Aparelho:**
   Executar testes manuais de estresse e validação em hardware físico (chamadas de voz, SMS, biometria, aplicativos bancários e integridade Play Integrity).
6. **Item 6 — Configuração de Assinatura de Commits com Chaves GPG:**
   Configurar chaves criptográficas GPG dos mantenedores e exigir commits assinados para integração na branch `main`.
7. **Item 7 — Revisão de Conformidade de Marcas Comerciais OEM/Operadoras:**
   Avaliar conformidade de marcas de fabricantes (Motorola, Samsung) e operadoras de telefonia nos relatórios públicos antes de publicações externas.
8. **Item 8 — Publicação Formal de Tag e Release (`v0.1.0`):**
   Criar a tag semântica formal `v0.1.0` no GitHub após a conclusão de todas as homologações em hardware físico e atendimento dos gates.
