# Changelog — Clean My Android

Todas as alterações notáveis neste projeto são documentadas neste arquivo.

O formato é baseado no [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/) e este repositório adota o [Versionamento Semântico](https://semver.org/lang/pt-BR/).

---

## [Unreleased]

### Adicionado
- **PT-7 (Processo e Governança):** Criação de `SECURITY(.pt-BR).md`, `.github/CODEOWNERS`, `CHANGELOG(.pt-BR).md` retroativo baseado em PRs #1–#47, e template de issue `request_audit_review.yml`. Padronização de Conventional Commits e Squash and Merge em `CONTRIBUTING(.pt-BR).md`.
- **PT-6 (Verificabilidade das Classificações):** Criação de `docs/CLASSIFICATION_METHOD(.pt-BR).md` com hierarquia estrita de 5 níveis de fontes (AOSP, fabricante, manifesto/dumpsys, comportamento em teste e comunidade secundária) e níveis de confiança (`high`, `medium`, `low`). Publicação de autoauditoria com amostragem probabilística de 30 pacotes em `docs/SELF_AUDIT_2026-11-09(.pt-BR).md` com semente reproduzível `20261109` em `scripts/sample_self_audit.py`.
- **PT-5 (Layout Canônico de Relatórios):** Padronização uniforme de diretórios em `reports/` com `audit(.en).md`, `comparison-report(.en).md`, `metrics.json`, `functional-tests.json`, `before/`, `after/`, `changes/` e `evidence/`. Validação automatizada por nível de homologação em `scripts/validate_repository.py` com testes em `tests/test_canonical_layout.py`.
- **PT-3 (Testes, CI e Portabilidade):** Expansão da suíte para 44 testes em `tests/test_adb_scripts.py` cobrindo 100% dos códigos de saída e testando todos os 44 pacotes protegidos. Configuração do Dependabot semanal para GitHub Actions em `.github/dependabot.yml`. Documentação de compatibilidade e restrições de plataformas em `docs/PLATFORMS(.pt-BR).md`.
- **PT-2 (Segurança de Scripts, Log e Snapshot):** Eliminação de `mapfile` em favor de laço compatível com Bash 3.2. Catálogo bilíngue centralizado (`scripts/lib/messages.sh` com `CMA_LANG`). Logging de ações em JSONL sanitizado com rollback. Gate dirigido por dados (`data/apply_support.tsv`). Ferramenta de snapshot somente-leitura com sanitização pré-gravação (`scripts/snapshot.sh`). Verificador de listas de alterações (`scripts/check_change_lists.py`). Remoção de pacotes protegidos de listas gerais em `data/`.
- **PT-1 (Alegações e Métricas com Status):** Validador automatizado de alegações absolutistas (`scripts/check_claims.py`) com allowlist qualificada (`data/claims_allowlist.json`). Esquema canônico rigoroso para `metrics.json` exigindo `kind`, `status`, `method` e `evidence`.
- **PT-4 (Sanitização Verificável):** Verificador automatizado de dados sensíveis (`scripts/check_sanitization.py`) cobrindo IMEI com algoritmo de Luhn, MEID, endereços MAC, números de telefone celular e IPs privados em contexto não documentado. Registro de auditoria em `docs/SANITIZATION_LOG.md`.

---

## [0.1.0] — 2026-11-08

Versão inicial de consolidação pública das auditorias técnicas forenses de dispositivos e automação preliminar de debloat.

### Resumo do histórico consolidado (Pull Requests #1 a #47)

#### Dispositivos e Relatórios Técnicos
- **Motorola Moto G54 5G (`cancunf` · XT2343-1):** Mapeamento integral dos 462 componentes de fábrica em 7 lotes técnicos detalhados e script com suporte a aplicação segura (PRs #1, #15, #16, #17, #19, #20, #21, #22, #23, #24, #29).
- **Motorola Edge 60 Pro (`cybert` · XT2507-1):** Auditoria técnica forense retrospectiva de 501 componentes de fábrica, conciliação de contagens pós-debloat, documentação de conflito com lista de pacotes protegidos e isolamento de identificadores de terceiros (PRs #2, #25, #30, #31, #32).
- **Motorola Edge 60 Fusion (`scout` · XT2503-1):** Auditoria técnica completa de 486 componentes no Android 16 (API 36), desativação de 87 bloatwares, restrição via AppOps de 5 componentes non-disable e substituição funcional validada por suíte FOSS com RoleManager (PR #33).
- **Samsung Galaxy A30s (`a30s` · SM-A307GT):** Auditoria técnica e debloat em dois lotes cobrindo 48 componentes alterados, mitigação de perda de PDF printing (printspooler) e sandboxing de telemetria OEM (PRs #35, #36).

#### Estrutura, Internacionalização e Documentação
- Reorganização da hierarquia de diretórios por fabricante e modelo em `reports/<fabricante>/<modelo>/` (PRs #9, #12).
- Internacionalização completa em inglês (EN) e português brasileiro (PT-BR) de todos os READMEs e lotes de auditoria (PRs #13, #14, #27, #40).
- Guia para assistentes de IA (`AI_INSTRUCTIONS`) e instruções de contribuição (`CONTRIBUTING`) (PRs #11, #25, #27, #34, #39).
- Estabelecimento do framework de status e níveis de homologação técnica de 0 a 4 (`docs/AUDIT_STATUS_AND_HOMOLOGATION`) e templates padronizados (PR #38).
- Auditoria semântica e alinhamento de terminologias e claims (PRs #41, #43, #44).

#### Qualidade, Validação e CI
- Criação e expansão do validador contínuo `scripts/validate_repository.py` validando JSONs, links locais de Markdown, sintaxe shell e integridade de pacotes protegidos (PRs #10, #28, #45, #46).
- Implementação inicial de framework de testes automatizados com mock de comandos ADB em `tests/test_adb_scripts.py` sem dependência de aparelho físico (PR #47).
- Fixação de ações e workflows de CI por commit SHA seguro com permissões mínimas (PR #46).
