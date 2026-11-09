# Notas de Configuração: Branch Protection, Checks do CI e Automação do Dashboard (C-3)

Este documento orienta o proprietário do repositório (`@luisfvmartins`) sobre a configuração segura de proteção da branch `main`, a correlação correta dos checks do GitHub Actions e a resolução do conflito com o workflow do painel de contribuições.

---

## 1. Ordem Obrigatória de Aplicação

> **AVISO CRÍTICO:** O check `CI result` **não existe** no repositório até que o workflow de matriz seja aplicado. Se o comando de proteção for executado antes, **nenhuma PR poderá ser mergeada** (o check ficará eternamente pendente).

A ordem estrita de execução deve ser:
1. **Passo 1 (Aplicação do CI):** Copiar o conteúdo de `docs/PROPOSED_VALIDATE_WORKFLOW.yml` para `.github/workflows/validate.yml` e fazer o commit/push na branch com um Personal Access Token (PAT) que possua o escopo `workflow`.
2. **Passo 2 (Verificação da PR):** Observar a execução do GitHub Actions em uma PR aberta e confirmar que o job agregador com `name: CI result` foi executado e reportou `success` (verde).
3. **Passo 3 (Aplicação da Proteção):** Apenas após a confirmação visual do check `CI result` no GitHub, executar o comando de proteção abaixo.

---

## 2. Comando Corrigido de Proteção de Branch

O comando abaixo configura a proteção padrão da branch `main` exigindo PR, aprovações, histórico linear e o contexto exato e estável gerado pelo job agregador `CI result`:

```bash
gh api \
  --method PUT \
  -H "Accept: application/vnd.github+json" \
  /repos/luisfvmartins/clean-my-android/branches/main/protection \
  --input - << 'EOF'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "CI result"
    ]
  },
  "enforce_admins": false,
  "required_pull_request_reviews": {
    "dismiss_stale_reviews": true,
    "require_code_owner_reviews": true,
    "required_approving_review_count": 1
  },
  "restrictions": null,
  "required_linear_history": true,
  "allow_force_pushes": false,
  "allow_deletions": false
}
EOF
```

---

## 3. Conflito entre Proteção da `main` e Push do Dashboard [Decisão]

O workflow ativo `.github/workflows/contribution-dashboard.yml` executa diariamente e após pushes na `main`, atualizando `docs/EVOLUCAO_CONTRIBUICOES*.md` e fazendo:
```bash
git commit -m "chore: update contribution dashboard"
git push
```
Ao aplicar a proteção da `main` (que exige Pull Request obrigatório para qualquer commit), a tentativa de `git push` direto pelo bot `github-actions[bot]` será **rejeitada pelo GitHub com erro HTTP 403 (Protected branch hook declined)**.

### Opções para decisão do proprietário:

#### Opção A: Migrar para GitHub Rulesets com Bypass para o App Actions
- **Como funciona:** Em vez de Branch Protection clássica, cria-se um **Repository Ruleset** para a branch `main`. No ruleset, adiciona-se uma exceção de *Bypass List* para o "GitHub Actions" (ou "GitHub Apps").
- **Prós:** Mantém o push direto inalterado; não polui a aba de Pull Requests com PRs automatizadas diárias.
- **Contras:** Exige configuração via interface web do GitHub (`Settings > Rules > Rulesets`) ou API beta de rulesets.

#### Opção B (Recomendada): Workflow do Dashboard abre Pull Request automatizada
- **Como funciona:** O workflow do dashboard deixa de fazer `git push` direto na `main`. Ele gera o commit em uma branch separada (ex: `automation/update-dashboard`) e abre uma Pull Request via `gh pr create` (com permissão `pull-requests: write`). A PR passa pelo validador do CI e é mergeada pelo mantenedor ou com auto-merge.
- **Prós:** Respeita 100% a disciplina de "nenhum commit entra na main sem passar por PR e CI". Totalmente compatível com Branch Protection clássica.
- **Contras:** Gera PRs periódicas que precisam de merge.
- **Arquivo pronto fornecido:** `docs/PROPOSED_DASHBOARD_WORKFLOW.yml`.

#### Opção C: Publicar o Dashboard em Branch Dedicada
- **Como funciona:** Os arquivos `docs/EVOLUCAO_CONTRIBUICOES*.md` ou o HTML correspondente são publicados em uma branch desprotegida (ex: `dashboard` ou `gh-pages`).
- **Prós:** Zero impacto na branch `main`; sem conflito de branch protection.
- **Contras:** Os arquivos de evolução deixam de residir no diretório `docs/` da branch principal.

**Recomendação técnica:** Adotar a **Opção B** (ou a **Opção A** se Luís preferir não receber PRs automáticas de dashboard).
