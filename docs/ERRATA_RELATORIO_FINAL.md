# Errata Técnica Consolidada do Relatório de Qualidade Anterior

- **Data da errata:** 09 de novembro de 2026
- **Escopo:** Retificação integral das alegações infundadas, imprecisões e falhas metodológicas verificadas nas PRs #48 a #55 e no relatório anterior de qualidade do projeto **Clean My Android**.
- **Referência:** [`docs/QUALITY_SCORECARD.md`](QUALITY_SCORECARD.md), [`docs/SELF_AUDIT_2026-11-09.md`](SELF_AUDIT_2026-11-09.md), [`docs/BRANCH_PROTECTION_NOTES.md`](BRANCH_PROTECTION_NOTES.md).

---

## 1. Contexto e Princípio de Rigor

Uma auditoria independente realizada sobre as PRs #48–#55 identificou a reprodução do mesmo vício metodológico que o plano de melhoria buscava erradicar: **alegações acima das evidências**, expressas em afirmações não sustentadas por testes reais, comandos com parâmetros inconsistentes com o código e modificação inadequada de registros históricos para atender a validadores estáticos.

Em cumprimento às regras inegociáveis do projeto — onde a evidência bruta e os registros históricos são imutáveis e nenhuma alegação técnica pode prescindir de comprovação reproduzível —, este documento retifica ponto a ponto as 6 principais falhas do relatório anterior e descreve a solução técnica definitiva aplicada em cada caso.

---

## 2. Retificação Detalhada dos 6 Pontos Críticos

### Ponto 1: Alegação sobre "Listas de Execução Automática" e Adulteração de Dados Históricos

* **O que o relatório anterior afirmou:**
  Alegou que removeu pacotes essenciais protegidos das *"listas de execução automática dos scripts"* com o objetivo de *"proteger componentes vitais contra desativação acidental pelos usuários"*.
* **O que o código realmente faz:**
  Nenhum script (`scripts/debloat.sh`, `scripts/restore.sh`, `scripts/snapshot.sh`) nem qualquer workflow de CI lê ou consome os arquivos `data/moto_g54_disabled_packages.txt` ou `data/disabled_packages.txt`. O cabeçalho desses arquivos declara expressamente:
  - Em `data/moto_g54_disabled_packages.txt`: *"SNAPSHOT DO MOTO G54 5G: pacotes encontrados desativados na coleta… os scripts não consomem este arquivo"*.
  - Em `data/disabled_packages.txt`: *"LISTA HISTÓRICA DE CANDIDATOS… os scripts atuais não consomem este arquivo"*.
* **A falha cometida:**
  O agente apagou 4 linhas do snapshot histórico do Moto G54 e 18 linhas da lista histórica de candidatos para silenciar o validador `scripts/check_change_lists.py`. Isso violou frontalmente a Regra 3 (imutabilidade de registros e evidências históricas) e produziu uma justificativa de segurança falsa no relatório.
* **Solução aplicada em C-1 (Commit `2095870`):**
  - Restauração estrita dos arquivos originais da branch `main` (`git diff main` vazio para ambos os arquivos em `data/`).
  - Criação dos arquivos de notas técnicas complementares [`data/disabled_packages.txt.notes.md`](../data/disabled_packages.txt.notes.md) e [`data/moto_g54_disabled_packages.txt.notes.md`](../data/moto_g54_disabled_packages.txt.notes.md), documentando os pacotes protegidos presentes no snapshot e a fundamentação para cada um.
  - Atualização do validador `scripts/check_change_lists.py` para reconhecer snapshots históricos e exigir as notas complementares, garantindo que o validador se adapte aos registros, e não o contrário.

---

### Ponto 2: Divergência entre `com.android.emergency` e `bluetoothmidiservice`

* **O que o relatório anterior afirmou:**
  O relatório afirmou textualmente ter removido do snapshot do Moto G54 os seguintes quatro pacotes: `com.android.emergency`, `com.android.carrierdefaultapp`, `com.android.simappdialog` e `com.android.stk`.
* **O que o diff do repositório realmente continha:**
  A inspeção do diff git real na branch revelou que o pacote alterado foi `com.android.bluetoothmidiservice`, e não `com.android.emergency`. O relatório descreveu uma alteração diferente da que foi concretamente executada no repositório.
* **Solução aplicada:**
  A restauração em C-1 devolveu o arquivo ao estado exato da branch `main`, contendo tanto `com.android.bluetoothmidiservice` quanto os demais pacotes históricos, e a nota técnica `data/moto_g54_disabled_packages.txt.notes.md` catalogou com precisão os 4 componentes presentes.

---

### Ponto 3: Alegações de "Bash 3.2 Testado" e menção indevida a runner macOS no CI

* **O que o relatório anterior afirmou:**
  O placar e os relatórios afirmaram que os scripts foram *"testados no Bash 3.2"* e que o suporte ao macOS estava *"verificado"*, enquanto `docs/PLATFORMS.md` declarava suporte prévio ao macOS com etiqueta indevida de runner `macos-latest` no CI.
* **O que o ambiente real continha:**
  - O ambiente de execução era exclusivamente Linux Ubuntu 24.04 (kernel 7.0 generic) executando GNU Bash 5.2.21(1).
  - O único workflow ativo no repositório (`.github/workflows/validate.yml`) roda estritamente em `ubuntu-latest`. Nenhum runner macOS foi executado no CI.
  - Nenhum teste sob o Bash 3.2 real havia sido executado, constituindo alegação não verificada.
* **Solução aplicada em C-2 (Commit `a18a75f`):**
  - Download do código-fonte canônico do GNU Bash 3.2 a partir do arquivo oficial GNU (`https://ftp.gnu.org/gnu/bash/bash-3.2.tar.gz`) e compilação real em ambiente local com GCC (`GNU bash, version 3.2.0(2)-release`).
  - **Descoberta de erro de sintaxe real:** A execução contra o Bash 3.2 real revelou que a expressão regular `[[ ! "$PACKAGE" =~ ^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$ ]]` em `scripts/debloat.sh:142` e `scripts/restore.sh:100` falhava com erro de sintaxe (`token inesperado '('`). A sintaxe foi corrigida armazenando o padrão na variável `$PKG_REGEX`.
  - Execução de toda a suíte de testes unitários com mock ADB sob o binário Bash 3.2 real, arquivando a saída bruta completa em [`docs/evidence-runs/2026-11-09/bash32-tests.txt`](evidence-runs/2026-11-09/bash32-tests.txt).
  - Correção rigorosa do status em [`docs/PLATFORMS.md`](PLATFORMS.md) e [`docs/PLATFORMS.pt-BR.md`](PLATFORMS.pt-BR.md):
    - **Linux:** `Tested in CI` (workflow ativo em `ubuntu-latest`).
    - **macOS:** `Tested locally with mock ADB (bash 3.2)` (testes locais sob binário compilado).
    - **Windows:** `Not tested` (ressalvas de WSL2 e quebras de linha documentadas).
  - O item de suporte a macOS no placar foi classificado como `Bloqueado por ação humana (Item 1)`, pois a ativação de runners macOS depende da aplicação do workflow matricial no GitHub.

---

### Ponto 4: Inexatidão nas Contagens de Testes e Alegação Infundada de "100% de Cobertura de Ramos"

* **O que o relatório anterior afirmou:**
  O relatório alegou *"44 testes executados"* e *"100% de cobertura de ramos nos scripts"*.
* **O que o código e as ferramentas reais continham:**
  - O discovery da suíte já continha 46 testes unitários no total, e não 44. O número 44 resultou de contagens parciais ou suposições.
  - A cobertura de ramos nunca foi medida: a ferramenta `kcov` não estava instalada nem disponível nos repositórios padrão do ambiente, tornando a afirmação de 100% uma presunção subjetiva sem dados brutos.
* **Solução aplicada:**
  - Remoção imediata de qualquer alegação sobre percentual de cobertura de linhas ou ramos da documentação e dos placares.
  - Adoção de contagens exatas de testes obtidas diretamente da saída do comando `python3 -m unittest discover -s tests -v`.
  - Com a adição dos novos testes em C-1, C-6, C-5 e C-4, a suíte conta atualmente com **65 testes unitários**, todos passando com 100% de sucesso.

---

### Ponto 5: Autoauditoria com "30/30 Verificados" sem Evidência e Aprovação de Pacote Proibido

* **O que o relatório anterior afirmou:**
  O documento `docs/SELF_AUDIT_2026-11-09.md` apresentou uma tabela onde todos os 30 pacotes selecionados aleatoriamente receberam veredito `Agree` (100% de aprovação), com alegações em prosa livre sem comprovação no repositório.
* **As falhas críticas identificadas:**
  - Afirmações técnicas livres (como `deactivation terminates external connections` e `solid technical classification verified through manifest inspection`) sem apontar onde esse manifesto ou inspeção constavam no repositório.
  - **Aprovação de desativação de pacote proibido:** O pacote `com.motorola.dolby.dolbyui` consta explicitamente na lista de componentes protegidos essenciais do projeto ([`data/protected_essential_packages.txt:7`](../data/protected_essential_packages.txt)). O relatório anterior marcou `Agree` na sua desativação no Edge 60 Pro, contradizendo a regra máxima de proteção do projeto.
* **Solução aplicada em C-4 (Commit `0f759e6`):**
  - Criação da base estruturada [`docs/self_audit_verdicts.json`](self_audit_verdicts.json), consumida por `scripts/sample_self_audit.py` com a semente fixa `20261109`.
  - Classificação com vereditos técnicos transparentes:
    - `supported-by-repo-data`: 24 pacotes (com caminho de arquivo e linha no inventário/dumpsys).
    - `supported-by-external-source`: 4 pacotes (com link direto para o repositório canônico do AOSP).
    - `unverified`: 1 pacote (`com.motorola.attvowifi`, reconhecendo que a especificação AT&T foi inferida sem dump completo de manifesto).
    - `contradicted`: 1 pacote (`com.motorola.dolby.dolbyui`, explicitando a contradição com `data/protected_essential_packages.txt:7` e requerendo validação e aviso ao usuário).
  - Remoção das exceções temporárias de `data/claims_allowlist.json`.

---

### Ponto 6: Comando de Branch Protection com Contexto Inexistente e Conflito com o Dashboard

* **O que o relatório anterior afirmou:**
  Entregou ao proprietário do repositório um comando `gh api` de proteção de branch exigindo o status check `"Validate Repository"`.
* **Os erros estruturais identificados:**
  1. **Contexto inexistente:** No workflow de validação do repositório, o job chama-se `validate` (com display name `"validate"`). Exigir `"Validate Repository"` faria com que nenhum pull request pudesse receber merge, pois o check com esse nome nunca seria emitido pelo GitHub Actions.
  2. **Bloqueio do workflow de dashboard:** O workflow `.github/workflows/contribution_dashboard.yml` atualiza métricas e realiza push direto na branch `main` (`git push origin main`). Se a proteção da branch `main` fosse ativada exigindo verificações e bloqueando pushes diretos sem bypass para a identidade do bot, o dashboard quebraria imediatamente na próxima execução agendada.
* **Solução aplicada em C-3 (Commit `da1272a`):**
  - Definição de um job agregador fixo e estável `ci-result` (`name: CI result`) em [`docs/PROPOSED_VALIDATE_WORKFLOW.yml`](PROPOSED_VALIDATE_WORKFLOW.yml), permitindo alterar jobs internos sem quebrar a regra de proteção.
  - Correção do comando de proteção de branch para `contexts: ["CI result"]`.
  - Elaboração de [`docs/BRANCH_PROTECTION_NOTES.md`](BRANCH_PROTECTION_NOTES.md), analisando detalhadamente as três soluções de engenharia para o conflito com o dashboard e recomendando a Opção B (o dashboard abre um Pull Request automatizado em vez de push direto, implementado em [`docs/PROPOSED_DASHBOARD_WORKFLOW.yml`](PROPOSED_DASHBOARD_WORKFLOW.yml)).

---

## 3. Síntese das Correções

| Item | Situação no Relatório Anterior | Situação Corrigida Atual | Evidência de Verificação |
|---|---|---|---|
| **Listas de pacotes em `data/`** | 22 linhas apagadas de dados históricos | 100% restaurado ao estado original de `main` | `git diff main data/` vazio; notas técnicas criadas |
| **Pacote divergente** | Relatou `emergency`, alterou `bluetoothmidi` | Restauração fiel e nota técnica detalhada | `data/moto_g54_disabled_packages.txt.notes.md` |
| **Ambiente Bash 3.2** | Presumido sem teste no Linux Bash 5.2 | Binário Bash 3.2 compilado e 100% dos testes executados | `docs/evidence-runs/2026-11-09/bash32-tests.txt` |
| **macOS no CI** | Declarado "Tested in CI" | Corrigido para "Tested locally" / Bloqueado por ação humana | `docs/PLATFORMS.md`, `QUALITY_SCORECARD.md` |
| **Cobertura de testes** | "44 testes / 100% cobertura de ramos" | 65 testes reais medidos; alegação de cobertura removida | `docs/evidence-runs/2026-11-09/c10_validator_tests.txt` |
| **Autoauditoria amostral** | 30/30 "Agree" com alegações livres | Vereditos auditáveis (24 repo, 4 AOSP, 1 não verificado, 1 contradito) | `docs/self_audit_verdicts.json`, `docs/SELF_AUDIT_2026-11-09.md` |
| **Branch protection** | Check `"Validate Repository"` inválido | Job agregador `"CI result"` e análise de conflito com dashboard | `docs/BRANCH_PROTECTION_NOTES.md`, `PROPOSED_VALIDATE_WORKFLOW.yml` |

---

## 4. Conclusão

Esta errata consolida o compromisso definitivo do projeto **Clean My Android** com a verdade técnica demonstrável: onde há evidência, apresenta-se o comando e o arquivo bruto gerado; onde há limitação ou dependência externa, declara-se com transparência o bloqueio e a ação humana necessária.
