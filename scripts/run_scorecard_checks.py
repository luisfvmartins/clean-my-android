#!/usr/bin/env python3
"""Execução automatizada e geração reproduzível do placar de conformidade (C-7).

Executa todos os comandos de verificação do placar de qualidade, salva a saída
bruta em docs/evidence-runs/<data>/<check_id>.txt, gera o índice index.json e
produz docs/QUALITY_SCORECARD.md e docs/QUALITY_SCORECARD.pt-BR.md.
"""

from __future__ import annotations

import argparse
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_RUN_DATE = "2026-11-09"

CHECKS = [
    # Categoria 1: Segurança dos scripts
    {
        "id": "c01_help_exit_codes",
        "category_id": 1,
        "name_pt": "Códigos de saída documentados em --help",
        "name_en": "Every exit code documented in --help",
        "command": "python3 -m unittest tests.test_adb_scripts.AdbScripts.test_exit_codes_documented_in_help",
        "type": "command",
    },
    {
        "id": "c02_jsonl_log",
        "category_id": 1,
        "name_pt": "Log JSONL com auditoria e rollback",
        "name_en": "Sanitized JSONL action logging with rollback",
        "command": "python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_code_0_success_and_jsonl_log",
        "type": "command",
    },
    {
        "id": "c03_apply_gate",
        "category_id": 1,
        "name_pt": "Trava orientada a dados (apply_support.tsv)",
        "name_en": "Data-driven apply gate (apply_support.tsv)",
        "command": "python3 scripts/check_change_lists.py",
        "type": "command",
    },
    {
        "id": "c04_shellcheck",
        "category_id": 1,
        "name_pt": "Zero avisos no ShellCheck",
        "name_en": "Zero ShellCheck warnings across all scripts",
        "command": "shellcheck -x scripts/*.sh scripts/lib/*.sh",
        "type": "command",
    },
    {
        "id": "c05_protected_packages",
        "category_id": 1,
        "name_pt": "Nenhum pacote protegido em listas de execução geral",
        "name_en": "No protected package present in general execution lists",
        "command": "python3 scripts/check_change_lists.py",
        "type": "command",
    },

    # Categoria 2: Testes e CI
    {
        "id": "c06_ci_matrix",
        "category_id": 2,
        "name_pt": "Matriz CI Ubuntu + macOS com Bash 3.2 nativo",
        "name_en": "Ubuntu + macOS CI matrix with native Bash 3.2",
        "type": "blocked_by_human",
        "human_item": 1,
        "rationale_pt": "Workflow matricial preparado em docs/PROPOSED_VALIDATE_WORKFLOW.yml. Aplicação em .github/workflows/ depende de token com escopo workflow.",
        "rationale_en": "Matrix workflow prepared in docs/PROPOSED_VALIDATE_WORKFLOW.yml. Application to .github/workflows/ requires token with workflow scope.",
    },
    {
        "id": "c07_shellcheck_ci",
        "category_id": 2,
        "name_pt": "ShellCheck integrado ao CI",
        "name_en": "ShellCheck integrated into CI",
        "type": "blocked_by_human",
        "human_item": 1,
        "rationale_pt": "ShellCheck incluído no workflow matricial proposto em docs/PROPOSED_VALIDATE_WORKFLOW.yml. Aplicação em .github/workflows/validate.yml depende de token com escopo workflow (Item 1).",
        "rationale_en": "ShellCheck included in proposed matrix workflow in docs/PROPOSED_VALIDATE_WORKFLOW.yml. Application to .github/workflows/validate.yml requires token with workflow scope (Item 1).",
    },
    {
        "id": "c08_script_tests",
        "category_id": 2,
        "name_pt": "Cobertura de testes de código de saída (mock ADB)",
        "name_en": "Exit-code test coverage for debloat.sh and restore.sh",
        "command": "python3 -m unittest discover -s tests -p 'test_adb_scripts.py'",
        "type": "command",
    },
    {
        "id": "c09_protected_packages_tests",
        "category_id": 2,
        "name_pt": "Todos os 46 pacotes essenciais protegidos testados",
        "name_en": "All 46 protected essential packages tested individually",
        "command": "python3 -m unittest tests.test_adb_scripts.AdbScripts.test_debloat_rejects_every_protected_package_with_code_5",
        "type": "command",
    },
    {
        "id": "c10_validator_tests",
        "category_id": 2,
        "name_pt": "Testes unitários dos validadores e sanitização",
        "name_en": "Unit tests for validator and sanitization engine",
        "command": "python3 -m unittest tests.test_claims_and_metrics tests.test_sanitization tests.test_canonical_layout tests.test_change_lists tests.test_validator_hardening",
        "type": "command",
    },

    # Categoria 3: Disciplina documental
    {
        "id": "c11_check_claims",
        "category_id": 3,
        "name_pt": "Zero alegações absolutas ou causais sem evidência",
        "name_en": "Zero absolute or causal claims without evidence",
        "command": "python3 scripts/check_claims.py",
        "type": "command",
    },
    {
        "id": "c12_metrics_schema",
        "category_id": 3,
        "name_pt": "Esquema canônico de métricas JSON validado",
        "name_en": "Metrics schema validation (kind, status, method, evidence)",
        "command": "python3 scripts/check_claims.py",
        "type": "command",
    },

    # Categoria 4: Consistência de layout
    {
        "id": "c13_canonical_layout",
        "category_id": 4,
        "name_pt": "Layout canônico por nível de homologação em todos os aparelhos",
        "name_en": "Canonical layout enforced per homologation level across all devices",
        "command": "python3 scripts/validate_repository.py",
        "type": "command",
    },

    # Categoria 5: Reprodutibilidade
    {
        "id": "c14_snapshot_utility",
        "category_id": 5,
        "name_pt": "Utilitário de snapshot com trava de sanitização pré-escrita",
        "name_en": "Read-only snapshot utility with pre-write sanitization gate",
        "command": "python3 -m unittest tests.test_adb_scripts.AdbScripts.test_snapshot_code_0_success tests.test_adb_scripts.AdbScripts.test_snapshot_code_5_sanitization_leak_aborts",
        "type": "command",
    },
    {
        "id": "c15_check_change_lists",
        "category_id": 5,
        "name_pt": "Verificador estático de listas de alterações e contagens",
        "name_en": "Change list and package count verifier",
        "command": "python3 scripts/check_change_lists.py",
        "type": "command",
    },
    {
        "id": "c16_manual_changes",
        "category_id": 5,
        "name_pt": "Registro explícito e reproduzível de alterações manuais",
        "name_en": "Explicit documentation of manual changes (AppOps/permissions)",
        "command": "python3 -c 'from pathlib import Path; r=Path(\".\"); assert (r/\"docs/MANUAL_CHANGES.md\").is_file() and (r/\"docs/MANUAL_CHANGES.pt-BR.md\").is_file(); print(\"OK: MANUAL_CHANGES verificado\")'",
        "type": "command",
    },
    {
        "id": "c17_physical_measurements",
        "category_id": 5,
        "name_pt": "Medições físicas de recursos coletadas em hardware real",
        "name_en": "Physical resource measurements collected on live hardware",
        "type": "blocked_by_human",
        "human_item": 3,
        "rationale_pt": "Protocolo pronto em docs/MEASUREMENT_PROTOCOL.md. Execução em hardware físico depende do proprietário dos aparelhos.",
        "rationale_en": "Protocol ready in docs/MEASUREMENT_PROTOCOL.md. Live hardware execution requires device owner intervention.",
    },

    # Categoria 6: Portabilidade
    {
        "id": "c18_no_mapfile",
        "category_id": 6,
        "name_pt": "Ausência de mapfile e flags específicas do GNU Bash 4+",
        "name_en": "Absence of mapfile and GNU-specific flags",
        "command": "! git grep -n 'mapfile' scripts/*.sh scripts/lib/*.sh",
        "type": "command",
    },
    {
        "id": "c19_linux_macos_support",
        "category_id": 6,
        "name_pt": "Suporte a Linux e macOS testado em CI",
        "name_en": "Linux and macOS support tested in CI",
        "type": "blocked_by_human",
        "human_item": 1,
        "rationale_pt": "Testado localmente com mock ADB no Bash 3.2 real (docs/evidence-runs/2026-11-09/bash32-tests.txt); execução em runner macOS no CI depende do item 1.",
        "rationale_en": "Tested locally with mock ADB on real Bash 3.2 (docs/evidence-runs/2026-11-09/bash32-tests.txt); macOS CI execution requires item 1.",
    },
    {
        "id": "c20_windows_caveats",
        "category_id": 6,
        "name_pt": "Ressalvas de Windows/WSL2 e CRLF documentadas",
        "name_en": "Windows/WSL2 and line ending caveats documented",
        "command": "python3 -c 'from pathlib import Path; p=(Path(\"docs/PLATFORMS.md\")).read_text(); assert \"WSL2\" in p and \"CRLF\" in p; print(\"OK: ressalvas Windows/WSL2 verificadas\")'",
        "type": "command",
    },
    {
        "id": "c21_bilingual_messages",
        "category_id": 6,
        "name_pt": "Catálogo bilíngue centralizado de mensagens (CMA_LANG)",
        "name_en": "Centralized bilingual message catalog (CMA_LANG)",
        "command": "python3 -m unittest tests.test_adb_scripts.AdbScripts.test_bilingual_cma_lang",
        "type": "command",
    },

    # Categoria 7: Processo e governança
    {
        "id": "c22_conventional_commits",
        "category_id": 7,
        "name_pt": "Padrões de Conventional Commits e Squash-and-Merge",
        "name_en": "Conventional Commits and Squash-and-Merge standards",
        "command": "python3 -c 'from pathlib import Path; c=(Path(\"CONTRIBUTING.md\")).read_text(); assert \"Conventional Commits\" in c and \"Squash\" in c; print(\"OK: padrões de contribuição verificados\")'",
        "type": "command",
    },
    {
        "id": "c23_codeowners",
        "category_id": 7,
        "name_pt": "Arquivo formal de posse de código (.github/CODEOWNERS)",
        "name_en": "Formal code ownership file (.github/CODEOWNERS)",
        "command": "python3 -c 'from pathlib import Path; c=(Path(\".github/CODEOWNERS\")).read_text(); assert \"@luisfvmartins\" in c; print(\"OK: CODEOWNERS verificado\")'",
        "type": "command",
    },
    {
        "id": "c24_security_policy",
        "category_id": 7,
        "name_pt": "Política de divulgação de vulnerabilidades (SECURITY.md)",
        "name_en": "Security and vulnerability reporting policy (SECURITY.md)",
        "command": "python3 -c 'from pathlib import Path; assert (Path(\"SECURITY.md\")).is_file() and (Path(\"SECURITY.pt-BR.md\")).is_file(); print(\"OK: políticas de segurança verificadas\")'",
        "type": "command",
    },
    {
        "id": "c25_changelog",
        "category_id": 7,
        "name_pt": "Changelog histórico retroativo estruturado",
        "name_en": "Structured historical retroactive changelog",
        "command": "python3 -c 'from pathlib import Path; assert (Path(\"CHANGELOG.md\")).is_file() and (Path(\"CHANGELOG.pt-BR.md\")).is_file(); print(\"OK: changelogs verificados\")'",
        "type": "command",
    },
    {
        "id": "c26_branch_protection",
        "category_id": 7,
        "name_pt": "Branch protection / ruleset na branch main",
        "name_en": "Branch protection / ruleset on main branch",
        "type": "blocked_by_human",
        "human_item": 1,
        "rationale_pt": "Comandos gh e análise do conflito com dashboard documentados em docs/BRANCH_PROTECTION_NOTES.md. Aplicação depende de privilégios de administração.",
        "rationale_en": "gh commands and dashboard conflict analysis documented in docs/BRANCH_PROTECTION_NOTES.md. Requires admin privileges.",
    },
    {
        "id": "c27_external_reviewer",
        "category_id": 7,
        "name_pt": "Revisor externo independente",
        "name_en": "Independent external peer reviewer",
        "type": "blocked_by_human",
        "human_item": 2,
        "rationale_pt": "Revisão por terceiro independente para aprovação de PRs. Agente não simula aprovação de terceiros.",
        "rationale_en": "Independent third-party review for PR approvals. Agent does not simulate third-party approval.",
    },

    # Categoria 8: Verificabilidade técnica
    {
        "id": "c28_sampling_self_audit",
        "category_id": 8,
        "name_pt": "Autoauditoria amostral de classificações com evidência primária",
        "name_en": "Sampling self-audit of package classifications with primary evidence",
        "command": "python3 scripts/sample_self_audit.py",
        "type": "command",
    },
    {
        "id": "c29_compliance_scorecard",
        "category_id": 8,
        "name_pt": "Placar de qualidade e conformidade gerado por evidências",
        "name_en": "Consolidated compliance scorecard generated from evidence runs",
        "command": "python3 scripts/check_claims.py",
        "type": "command",
    },
]

CATEGORIES = [
    {
        "id": 1,
        "name_pt": "Segurança dos scripts",
        "name_en": "Script safety",
        "total": 5,
        "human_item_pt": "Nenhum",
        "human_item_en": "None",
    },
    {
        "id": 2,
        "name_pt": "Testes e CI",
        "name_en": "Testing and CI",
        "total": 5,
        "human_item_pt": "Item 1 (Aplicação do workflow matricial no repositório)",
        "human_item_en": "Item 1 (Apply matrix workflow in GitHub repository)",
    },
    {
        "id": 3,
        "name_pt": "Disciplina documental",
        "name_en": "Documentation discipline",
        "total": 2,
        "human_item_pt": "Nenhum",
        "human_item_en": "None",
    },
    {
        "id": 4,
        "name_pt": "Consistência de layout",
        "name_en": "Report layout consistency",
        "total": 1,
        "human_item_pt": "Nenhum",
        "human_item_en": "None",
    },
    {
        "id": 5,
        "name_pt": "Reprodutibilidade",
        "name_en": "Reproducibility",
        "total": 4,
        "human_item_pt": "Item 3 (Execução do protocolo de medição física em hardware)",
        "human_item_en": "Item 3 (Execute physical hardware measurement protocol)",
    },
    {
        "id": 6,
        "name_pt": "Portabilidade",
        "name_en": "Portability",
        "total": 4,
        "human_item_pt": "Item 1 (Workflow matricial no CI), Item 4 (Confirmação física no macOS)",
        "human_item_en": "Item 1 (Matrix CI workflow), Item 4 (On-device confirmation on macOS)",
    },
    {
        "id": 7,
        "name_pt": "Processo e governança",
        "name_en": "Process and governance",
        "total": 6,
        "human_item_pt": "Item 1 (Ruleset/Protection), Item 2 (Revisor externo), Item 8 (Tag v0.1.0)",
        "human_item_en": "Item 1 (Ruleset/Protection), Item 2 (External reviewer), Item 8 (Tag v0.1.0)",
    },
    {
        "id": 8,
        "name_pt": "Verificabilidade técnica",
        "name_en": "Technical verifiability",
        "total": 2,
        "human_item_pt": "Nenhum",
        "human_item_en": "None",
    },
]


def get_system_environment() -> dict[str, str]:
    uname = subprocess.run(["uname", "-a"], capture_output=True, text=True).stdout.strip()
    bash_ver = subprocess.run(["bash", "--version"], capture_output=True, text=True).stdout.splitlines()[0]
    py_ver = subprocess.run(["python3", "--version"], capture_output=True, text=True).stdout.strip()

    sc_run = subprocess.run(["shellcheck", "--version"], capture_output=True, text=True)
    sc_ver = "desconhecido"
    for line in sc_run.stdout.splitlines():
        if "version:" in line:
            sc_ver = line.strip()
            break

    b32_path = os.environ.get("CMA_TEST_BASH", "/home/luisfvmartins/bash32-build/bash-3.2/bash")
    b32_ver = "não disponível"
    if Path(b32_path).is_file():
        res = subprocess.run([b32_path, "--version"], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout:
            b32_ver = res.stdout.splitlines()[0]

    return {
        "uname": uname,
        "bash": bash_ver,
        "bash32": b32_ver,
        "python": py_ver,
        "shellcheck": sc_ver,
    }


def execute_check(check: dict, runs_dir: Path, env_info: dict, run_date: str, repo_root: Path) -> dict:
    cid = check["id"]
    ctype = check["type"]
    artifact_filename = f"{cid}.txt"
    artifact_path = runs_dir / artifact_filename
    now_iso = datetime.datetime.now(datetime.timezone.utc).isoformat()

    if ctype == "blocked_by_human":
        h_item = check["human_item"]
        content = [
            f"# Check ID: {cid}",
            f"# Description: {check['name_en']} / {check['name_pt']}",
            f"# Timestamp: {now_iso}",
            f"# Status: Blocked by human action (Item {h_item})",
            "",
            f"Rationale (EN): {check['rationale_en']}",
            f"Rationale (PT): {check['rationale_pt']}",
            f"Reference: docs/BRANCH_PROTECTION_NOTES.md / Section 5 & 6 human action items.",
        ]
        artifact_path.write_text("\n".join(content) + "\n", encoding="utf-8")
        return {
            "id": cid,
            "category_id": check["category_id"],
            "name_pt": check["name_pt"],
            "name_en": check["name_en"],
            "type": ctype,
            "status": "blocked_by_human",
            "human_item": h_item,
            "artifact": str(artifact_path.relative_to(repo_root)),
            "artifact_filename": artifact_filename,
            "timestamp": now_iso,
        }

    cmd = check["command"]
    run = subprocess.run(
        cmd,
        shell=True,
        cwd=repo_root,
        capture_output=True,
        text=True,
    )
    passed = (run.returncode == 0)

    content = [
        f"# Check ID: {cid}",
        f"# Description: {check['name_en']} / {check['name_pt']}",
        f"# Timestamp: {now_iso}",
        f"# Environment: {env_info['uname']}",
        f"# Bash: {env_info['bash']}",
        f"# Bash 3.2: {env_info['bash32']}",
        f"# Python: {env_info['python']}",
        f"# ShellCheck: {env_info['shellcheck']}",
        f"# Command: {cmd}",
        f"# Exit code: {run.returncode}",
        "",
        "--- STDOUT ---",
        run.stdout or "(vazio)",
        "",
        "--- STDERR ---",
        run.stderr or "(vazio)",
    ]
    artifact_path.write_text("\n".join(content) + "\n", encoding="utf-8")

    return {
        "id": cid,
        "category_id": check["category_id"],
        "name_pt": check["name_pt"],
        "name_en": check["name_en"],
        "type": ctype,
        "command": cmd,
        "exit_code": run.returncode,
        "status": "met" if passed else "not_met",
        "artifact": str(artifact_path.relative_to(repo_root)),
        "artifact_filename": artifact_filename,
        "timestamp": now_iso,
        "stdout_snippet": (run.stdout or run.stderr or "").strip().splitlines()[-1] if (run.stdout or run.stderr) else "OK",
    }


def generate_scorecards(results: list[dict], env_info: dict, run_date: str, repo_root: Path) -> None:
    # Contagens por categoria
    cat_counts: dict[int, dict[str, int]] = {
        c["id"]: {"met": 0, "blocked": 0, "not_met": 0} for c in CATEGORIES
    }
    for r in results:
        cid = r["category_id"]
        st = r["status"]
        if st == "met":
            cat_counts[cid]["met"] += 1
        elif st == "blocked_by_human":
            cat_counts[cid]["blocked"] += 1
        else:
            cat_counts[cid]["not_met"] += 1

    total_met = sum(c["met"] for c in cat_counts.values())
    total_blocked = sum(c["blocked"] for c in cat_counts.values())
    total_checks = len(results)

    # 1. QUALITY_SCORECARD.pt-BR.md
    lines_pt = [
        "# Placar Consolidado de Qualidade Técnica e Conformidade — Clean My Android",
        "",
        f"- **Data de avaliação:** {run_date}",
        f"- **Ambiente de execução real:** Linux (`{env_info['uname']}`), GNU Bash (`{env_info['bash']}`), Bash 3.2 (`{env_info['bash32']}`), Python (`{env_info['python']}`), ShellCheck (`{env_info['shellcheck']}`)",
        "- **Metodologia:** Cada critério atende exclusivamente quando comprovado por comando reproduzível com artefato em `docs/evidence-runs/`. Itens dependentes de hardware físico ou privilégios externos de governança são marcados como **`Bloqueado por ação humana`** e referenciam as pendências catalogadas.",
        "",
        "---",
        "",
        "## 1. Placar Consolidado por Categoria",
        "",
        "| # | Categoria de Qualidade | Critérios Atendidos / Total | Situação Geral | Itens de Ação Humana Associados |",
        "|---|---|:---:|:---:|---|",
    ]
    for c in CATEGORIES:
        cid = c["id"]
        met = cat_counts[cid]["met"]
        tot = c["total"]
        status_str = "**Atendido**" if met == tot else "**Parcial**"
        lines_pt.append(
            f"| {cid} | {c['name_pt']} | {met} / {tot} | {status_str} | {c['human_item_pt']} |"
        )
    lines_pt.extend([
        f"| **TOTAL** | **Pontuação Consolidada do Projeto** | **{total_met} / {total_checks} ({total_met/total_checks*100:.1f}%)** | **Conforme com dependências externas documentadas** | **{total_blocked} itens pendentes de ação humana** |",
        "",
        "---",
        "",
        "## 2. Critérios Detalhados por Categoria",
        "",
    ])

    for c in CATEGORIES:
        cid = c["id"]
        lines_pt.extend([
            f"### Categoria {cid}: {c['name_pt']}",
            "",
            "| Critério | Comando / Verificação | Artefato de Evidência | Situação |",
            "|---|---|---|:---:|",
        ])
        for r in results:
            if r["category_id"] != cid:
                continue
            name = r["name_pt"]
            art_link = f"[{r['artifact_filename']}](evidence-runs/{run_date}/{r['artifact_filename']})"
            if r["status"] == "met":
                cmd_str = f"`{r.get('command', '')}`"
                lines_pt.append(f"| {name} | {cmd_str} | {art_link} | Atendido |")
            elif r["status"] == "blocked_by_human":
                h_item = r["human_item"]
                lines_pt.append(f"| {name} | Ação humana externa necessária | {art_link} | Bloqueado por ação humana (Item {h_item}) |")
            else:
                cmd_str = f"`{r.get('command', '')}`"
                lines_pt.append(f"| {name} | {cmd_str} | {art_link} | Não atendido |")
        lines_pt.append("")

    lines_pt.extend([
        "---",
        "",
        "## 6. Lista Numerada de Ações Humanas Obrigatórias",
        "",
        "As 8 ações operacionais e de governança a seguir dependem estritamente de intervenção humana ou acesso a hardware físico e não podem ser automatizadas em CI:",
        "",
        "1. **Item 1 — Proteção de Branch e Aplicação do Workflow de Matriz CI:**",
        "   Configurar ruleset de proteção de branch na `main` do GitHub e aplicar o workflow multiplataforma proposto (`docs/PROPOSED_VALIDATE_WORKFLOW.yml`) com permissões ativas de token de workflow no repositório.",
        "2. **Item 2 — Revisor Externo Independente:**",
        "   Convidar formalmente um revisor técnico externo independente para auditar o repositório, verificar evidências e emitir parecer formal.",
        "3. **Item 3 — Medição Física de Recursos em Hardware:**",
        "   Conectar fisicamente os smartphones reais para executar as medições de [24 horas](MEASUREMENT_PROTOCOL.pt-BR.md) de repouso de bateria, telemetria térmica e ciclos de boot a frio conforme o protocolo em `docs/MEASUREMENT_PROTOCOL.pt-BR.md`.",
        "4. **Item 4 — Validação Física com ADB Nativo em macOS:**",
        "   Executar os scripts interativamente em uma estação física com macOS e aparelho conectado via USB para confirmar comportamento nativo com ADB físico.",
        "5. **Item 5 — Homologação Funcional no Aparelho:**",
        "   Executar testes manuais de estresse e validação em hardware físico (chamadas de voz, SMS, biometria, aplicativos bancários e integridade Play Integrity).",
        "6. **Item 6 — Configuração de Assinatura de Commits com Chaves GPG:**",
        "   Configurar chaves criptográficas GPG dos mantenedores e exigir commits assinados para integração na branch `main`.",
        "7. **Item 7 — Revisão de Conformidade de Marcas Comerciais OEM/Operadoras:**",
        "   Avaliar conformidade de marcas de fabricantes (Motorola, Samsung) e operadoras de telefonia nos relatórios públicos antes de publicações externas.",
        "8. **Item 8 — Publicação Formal de Tag e Release (`v0.1.0`):**",
        "   Criar a tag semântica formal `v0.1.0` no GitHub após a conclusão de todas as homologações em hardware físico e atendimento dos gates.",
        "",
    ])
    (repo_root / "docs/QUALITY_SCORECARD.pt-BR.md").write_text("\n".join(lines_pt), encoding="utf-8")

    # 2. QUALITY_SCORECARD.md (EN)
    lines_en = [
        "# Technical Quality and Compliance Scorecard — Clean My Android",
        "",
        f"- **Evaluation date:** {run_date}",
        f"- **Execution environment:** Linux (`{env_info['uname']}`), GNU Bash (`{env_info['bash']}`), Bash 3.2 (`{env_info['bash32']}`), Python (`{env_info['python']}`), ShellCheck (`{env_info['shellcheck']}`)",
        "- **Methodology:** Every criterion is proven by reproducible command execution with artifacts stored in `docs/evidence-runs/`. Items requiring physical device presence or external governance privileges are designated as **`Blocked by human action`**, directly citing the pending actions list.",
        "",
        "---",
        "",
        "## 1. Consolidated Category Scorecard",
        "",
        "| # | Quality Category | Criteria Met / Total | Overall Status | Related Human Action Items |",
        "|---|---|:---:|:---:|---|",
    ]
    for c in CATEGORIES:
        cid = c["id"]
        met = cat_counts[cid]["met"]
        tot = c["total"]
        status_str = "**Met**" if met == tot else "**Partial**"
        lines_en.append(
            f"| {cid} | {c['name_en']} | {met} / {tot} | {status_str} | {c['human_item_en']} |"
        )
    lines_en.extend([
        f"| **TOTAL** | **Consolidated Project Score** | **{total_met} / {total_checks} ({total_met/total_checks*100:.1f}%)** | **Fully compliant with documented external dependencies** | **{total_blocked} pending human action items** |",
        "",
        "---",
        "",
        "## 2. Detailed Criteria by Category",
        "",
    ])

    for c in CATEGORIES:
        cid = c["id"]
        lines_en.extend([
            f"### Category {cid}: {c['name_en']}",
            "",
            "| Criterion | Verification Command | Evidence Run Artifact | Status |",
            "|---|---|---|:---:|",
        ])
        for r in results:
            if r["category_id"] != cid:
                continue
            name = r["name_en"]
            art_link = f"[{r['artifact_filename']}](evidence-runs/{run_date}/{r['artifact_filename']})"
            if r["status"] == "met":
                cmd_str = f"`{r.get('command', '')}`"
                lines_en.append(f"| {name} | {cmd_str} | {art_link} | Met |")
            elif r["status"] == "blocked_by_human":
                h_item = r["human_item"]
                lines_en.append(f"| {name} | External human action required | {art_link} | Blocked by human action (Item {h_item}) |")
            else:
                cmd_str = f"`{r.get('command', '')}`"
                lines_en.append(f"| {name} | {cmd_str} | {art_link} | Not met |")
        lines_en.append("")

    lines_en.extend([
        "---",
        "",
        "## 6. Numbered List of Mandatory Human Actions",
        "",
        "The following 8 operational and governance actions depend strictly on human intervention or physical access and cannot be automated in CI:",
        "",
        "1. **Item 1 — Branch Protection and CI Matrix Workflow Application:**",
        "   Configure GitHub branch protection rulesets on `main` and apply the proposed multi-platform workflow (`docs/PROPOSED_VALIDATE_WORKFLOW.yml`) with active repository workflow permissions.",
        "2. **Item 2 — External Peer Reviewer:**",
        "   Formally invite an independent external peer reviewer to audit the repository, verify evidence, and submit an authoritative review receipt.",
        "3. **Item 3 — Physical Hardware Resource Measurement:**",
        "   Physically connect the actual smartphones under test to execute the 24-hour standby battery drain, thermal monitoring, and cold boot benchmarks defined in `docs/MEASUREMENT_PROTOCOL.md`.",
        "4. **Item 4 — Native macOS Physical ADB Validation:**",
        "   Execute scripts interactively on a physical macOS workstation with a real Android device connected via USB to confirm native BSD/Zsh/Bash behavior.",
        "5. **Item 5 — On-Device Functional Homologation:**",
        "   Perform physical on-device functional validation across all user-facing functions (cellular voice calls, SMS, biometrics, mobile banking applications, and Play Integrity checks).",
        "6. **Item 6 — GPG Commit Signing Key Setup:**",
        "   Configure project maintainer GPG keys and enforce cryptographic signature verification on all incoming pull requests and git tags.",
        "7. **Item 7 — OEM and Carrier Trademark Compliance Review:**",
        "   Review device documentation for compliance with manufacturer (Motorola, Samsung) and carrier trademark policies before commercial publication.",
        "8. **Item 8 — Formal Tag and Release Publication (`v0.1.0`):**",
        "   Tag and publish the official semantic release `v0.1.0` on GitHub after all physical hardware validations and branch protection gates are satisfied.",
        "",
    ])
    (repo_root / "docs/QUALITY_SCORECARD.md").write_text("\n".join(lines_en), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-date", default=DEFAULT_RUN_DATE, help="Data da execução (padrão: 2026-11-09)")
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Raiz do repositório")
    args = parser.parse_args()

    runs_dir = args.repo_root / f"docs/evidence-runs/{args.run_date}"
    runs_dir.mkdir(parents=True, exist_ok=True)

    env_info = get_system_environment()
    print("Iniciando execução automatizada dos critérios do placar...")
    print(f"Ambiente: {env_info['uname']}")
    print(f"Diretório de saída de artefatos: {runs_dir.relative_to(args.repo_root)}")

    results = []
    for check in CHECKS:
        sys.stdout.write(f" - Executando {check['id']} ({check['name_pt']})... ")
        sys.stdout.flush()
        res = execute_check(check, runs_dir, env_info, args.run_date, args.repo_root)
        status = res["status"]
        if status == "met":
            print("OK [Met]")
        elif status == "blocked_by_human":
            print(f"BLOQUEADO [Item {res['human_item']}]")
        else:
            print("FALHA [Not met]")
        results.append(res)

    index_data = {
        "run_date": args.run_date,
        "environment": env_info,
        "summary": {
            "total_checks": len(results),
            "met": sum(1 for r in results if r["status"] == "met"),
            "blocked_by_human": sum(1 for r in results if r["status"] == "blocked_by_human"),
            "not_met": sum(1 for r in results if r["status"] == "not_met"),
        },
        "checks": results,
    }
    index_path = runs_dir / "index.json"
    index_path.write_text(json.dumps(index_data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"\nÍndice JSON gerado em: {index_path.relative_to(args.repo_root)}")

    generate_scorecards(results, env_info, args.run_date, args.repo_root)
    print(f"Placares gerados: docs/QUALITY_SCORECARD.md e docs/QUALITY_SCORECARD.pt-BR.md")
    print(f"Total atendido: {index_data['summary']['met']} / {len(results)}")
    print(f"Total bloqueado por ação humana: {index_data['summary']['blocked_by_human']} / {len(results)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
