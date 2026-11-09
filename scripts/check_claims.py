#!/usr/bin/env python3
"""Validador de alegações técnicas e esquema canônico de métricas (PT-1).

Verifica:
1. Termos absolutistas ou causais sem qualificação (não medido/pendente/hipótese/evidência).
2. Conformidade de exceções com data/claims_allowlist.json (com categoria A/B e justificativa obrigatória).
3. Esquema canônico de métricas em comparativo.json e metrics.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DEFAULT_TERMS = [
    r"erradic\w*",
    r"elimin\w*",
    r"interrupção completa",
    r"neutraliz\w*",
    r"bloqueio total",
    r"24 horas",
    r"24/7",
    r"rastreamento",
    r"coleta de IMEI",
    r"espionagem",
    r"spyware",
    r"adware",
    r"eradicat\w*",
    r"completely",
    r"stops tracking",
]

ENGLISH_TERMS = [
    r"privacy gain",
    r"verified",
    r"confirmed",
    r"highly recommended",
    r"telemetry",
    r"servers",
    r"tracking",
    r"dropper",
    r"harvest",
    r"exfiltrat",
]

DEFAULT_PATTERN = re.compile(r"(?i)\b(?:" + "|".join(DEFAULT_TERMS) + r")\b")
DOCS_PATTERN = re.compile(r"(?i)\b(?:" + "|".join(DEFAULT_TERMS + english_terms) + r")\b" if 'english_terms' in locals() else r"(?i)\b(?:" + "|".join(DEFAULT_TERMS + ENGLISH_TERMS) + r")\b")
QUALIFIER_PATTERN = re.compile(
    r"(?i)(?:não medid[ao]s?|not measured|pendente|pending|hipótese|hypothesis|\[.*?\]\(.*?\))"
)

FORBIDDEN_COUNT_EFFECTS = [
    r"efeito sobre rastreamento",
    r"efeito sobre privacidade",
    r"economia de bateria",
    r"economia de ram",
    r"eliminação de telemetria",
    r"tracking elimination",
    r"battery saving",
    r"privacy guarantee",
]
COUNT_EFFECTS_PATTERN = re.compile(r"(?i)(?:" + "|".join(FORBIDDEN_COUNT_EFFECTS) + r")")


def load_allowlist(allowlist_path: Path) -> tuple[list[dict], list[str]]:
    """Carrega e valida entradas da allowlist. Retorna (entradas_validas, erros)."""
    if not allowlist_path.is_file():
        return [], []
    try:
        data = json.loads(allowlist_path.read_text(encoding="utf-8"))
        entries = data.get("entries", [])
    except Exception as exc:
        return [], [f"{allowlist_path}: erro ao decodificar JSON ({exc})"]

    valid_entries: list[dict] = []
    errors: list[str] = []
    for idx, entry in enumerate(entries):
        path = entry.get("path")
        term = entry.get("term")
        cat = entry.get("category")
        rat = entry.get("rationale")

        if not path or not term:
            errors.append(f"{allowlist_path}: entry[{idx}] ausente de 'path' ou 'term'")
            continue

        if cat not in ("A", "B"):
            errors.append(
                f"{allowlist_path}: entry[{idx}] ('{term}' em {path}) categoria inválida: {cat!r} (esperado 'A' ou 'B')"
            )
            continue

        if not isinstance(rat, str) or not rat.strip():
            errors.append(
                f"{allowlist_path}: entry[{idx}] ('{term}' em {path}) justificativa/rationale ausente ou vazia"
            )
            continue

        valid_entries.append(entry)

    return valid_entries, errors


def is_allowlisted(
    rel_path: str, line_no: int, term: str, line_text: str, allowlist_entries: list[dict]
) -> bool:
    for entry in allowlist_entries:
        if entry.get("path") != rel_path:
            continue
        # Categoria A ou B e justificativa preenchida são obrigatórias para honrar a exceção
        if entry.get("category") not in ("A", "B") or not str(entry.get("rationale", "")).strip():
            continue
        entry_term = entry.get("term", "")
        if entry_term.lower() not in term.lower() and term.lower() not in entry_term.lower():
            continue
        # Match line number or snippet
        if entry.get("line") == line_no:
            return True
        snippet = entry.get("snippet", "")
        if snippet and snippet in line_text:
            return True
    return False


def validate_claims(
    base_dir: Path, allowlist_path: Path
) -> tuple[int, list[str]]:
    errors: list[str] = []
    checks = 0
    allowlist, allowlist_errors = load_allowlist(allowlist_path)
    errors.extend(allowlist_errors)

    target_extensions = (".md",)
    for path in sorted(base_dir.rglob("*.md")):
        if ".git" in path.parts or ".pytest_cache" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file():
            continue
        rel = str(path.relative_to(base_dir))
        if rel in ("data/sanitization_allowlist.json", "data/claims_allowlist.json"):
            continue
        if not (
            rel.startswith(("reports/", "docs/", "data/"))
            or rel.startswith("README")
            or rel.startswith("CONTRIBUTING")
        ):
            continue

        try:
            content = path.read_text(encoding="utf-8")
        except Exception as exc:
            errors.append(f"{rel}: erro de leitura ({exc})")
            continue

        pat = DOCS_PATTERN if rel.startswith("docs/") else DEFAULT_PATTERN
        for lno, line in enumerate(content.splitlines(), 1):
            checks += 1
            line_no_code = re.sub(r"`[^`]*`", "", line)
            line_clean = re.sub(r"\b[a-zA-Z0-9_-]+(?:\.[a-zA-Z0-9_-]+)+\b", "", line_no_code)
            match = pat.search(line_clean)
            if match:
                term = match.group(0)
                if QUALIFIER_PATTERN.search(line):
                    continue
                if is_allowlisted(rel, lno, term, line.strip(), allowlist):
                    continue
                errors.append(
                    f"{rel}:{lno}: termo não qualificado '{term}' sem evidência ou marcador na linha: {line.strip()[:100]}"
                )

    return checks, errors


def validate_metrics_json(
    base_dir: Path
) -> tuple[int, list[str]]:
    errors: list[str] = []
    checks = 0

    metric_files = list(base_dir.rglob("comparativo.json")) + list(base_dir.rglob("metrics.json"))
    for path in sorted(metric_files):
        if ".git" in path.parts or ".pytest_cache" in path.parts or "__pycache__" in path.parts:
            continue
        rel = str(path.relative_to(base_dir))
        checks += 1
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"{rel}: JSON inválido ({exc})")
            continue

        if not isinstance(data, dict):
            errors.append(f"{rel}: raiz deve ser um objeto JSON")
            continue

        metrics = data.get("metrics")
        if not isinstance(metrics, list):
            errors.append(f"{rel}: campo 'metrics' deve ser uma lista")
            continue

        for idx, m in enumerate(metrics):
            checks += 1
            if not isinstance(m, dict):
                errors.append(f"{rel}: metric[{idx}] deve ser um objeto JSON")
                continue

            ind = m.get("indicator") or m.get("metric")
            if not ind or not isinstance(ind, str) or not ind.strip():
                errors.append(f"{rel}: metric[{idx}] ausente de identificador ('indicator' ou 'metric')")

            kind = m.get("kind")
            if kind not in ("count", "resource", "behavior"):
                errors.append(f"{rel}: metric[{idx}] '{ind}' possui kind inválido: {kind} (esperado count|resource|behavior)")

            status = m.get("status")
            if status not in ("measured", "not_measured", "pending"):
                errors.append(f"{rel}: metric[{idx}] '{ind}' possui status inválido: {status} (esperado measured|not_measured|pending)")

            method = m.get("method")
            evidence = m.get("evidence")
            limitations = m.get("limitations")

            if not isinstance(limitations, str):
                errors.append(f"{rel}: metric[{idx}] '{ind}' campo 'limitations' deve ser string")

            if status == "measured":
                if not isinstance(method, str) or not method.strip():
                    errors.append(f"{rel}: metric[{idx}] '{ind}' com status=measured exige 'method' preenchido")
                if not isinstance(evidence, list) or len(evidence) == 0:
                    errors.append(f"{rel}: metric[{idx}] '{ind}' com status=measured exige lista 'evidence' não vazia")
                else:
                    for ev_rel in evidence:
                        ev_path = (base_dir / ev_rel).resolve()
                        try:
                            ev_path.relative_to(base_dir.resolve())
                        except ValueError:
                            errors.append(f"{rel}: metric[{idx}] '{ind}' evidência fora do repositório: {ev_rel}")
                            continue
                        if not ev_path.is_file():
                            errors.append(f"{rel}: metric[{idx}] '{ind}' arquivo de evidência inexistente: {ev_rel}")

            if kind == "count":
                fields_to_check = [
                    str(ind),
                    str(m.get("description", "")),
                    str(m.get("variation", "")),
                    str(m.get("before", "")),
                    str(m.get("after", "")),
                    str(m.get("limitations", "")),
                ]
                desc = " ".join(fields_to_check).lower()
                m_effect = COUNT_EFFECTS_PATTERN.search(desc)
                if m_effect:
                    errors.append(
                        f"{rel}: metric[{idx}] '{ind}' métrica do tipo 'count' não pode alegar efeito em nenhum campo: {m_effect.group(0)}"
                    )

    return checks, errors


def get_active_ci_os_list(root_dir: Path) -> set[str]:
    """Extrai os sistemas operacionais configurados em workflows ativos (.github/workflows/)."""
    ci_os: set[str] = set()
    wf_dir = root_dir / ".github/workflows"
    if not wf_dir.is_dir():
        return ci_os

    for p in wf_dir.glob("*.y*ml"):
        try:
            content = p.read_text(encoding="utf-8")
            for m in re.finditer(r"runs-on:\s*([a-zA-Z0-9_\-\.]+)", content):
                ci_os.add(m.group(1).strip().lower())
            m_matrix = re.search(r"os:\s*\[([^\]]+)\]", content)
            if m_matrix:
                for item in m_matrix.group(1).split(","):
                    val = item.strip().strip("'\"").lower()
                    if val:
                        ci_os.add(val)
        except Exception:
            pass
    return ci_os


def validate_ci_platform_claims(root_dir: Path) -> tuple[int, list[str]]:
    """Valida que qualquer menção a 'Tested in CI' reflete SOs configurados em workflows ativos."""
    checks = 0
    errors: list[str] = []
    active_os = get_active_ci_os_list(root_dir)

    ci_claim_pattern = re.compile(
        r"(?i)\b(?:tested in ci|testado no ci|testado em ci)\s*(?:\(([^)]+)\)|(?:on|em|no|[-—:])\s*([a-zA-Z0-9_\-\.]+))"
    )

    docs_to_check = (
        list(root_dir.glob("docs/**/*.md"))
        + list(root_dir.glob("reports/**/*.md"))
        + list(root_dir.glob("README*.md"))
    )
    for p in docs_to_check:
        if ".git" in p.parts:
            continue
        rel = str(p.relative_to(root_dir))
        try:
            content = p.read_text(encoding="utf-8")
        except Exception:
            continue

        for lno, line in enumerate(content.splitlines(), 1):
            checks += 1
            for m in ci_claim_pattern.finditer(line):
                claimed_os_str = m.group(1) or m.group(2) or ""
                claimed_os_str = claimed_os_str.strip()
                for os_token in re.split(r"[,/ ]+", claimed_os_str):
                    os_token = os_token.strip().lower()
                    if not os_token or os_token in {"supported", "suportado", "tested", "testado"}:
                        continue
                    if os_token not in active_os:
                        errors.append(
                            f"{rel}:{lno}: SO '{os_token}' citado em 'Tested in CI' não está presente em workflows ativos de .github/workflows/ (ativos: {sorted(active_os)})"
                        )
    return checks, errors


def validate_scorecard_evidence_references(root_dir: Path) -> tuple[int, list[str]]:
    """Valida que linhas com status 'Met'/'Atendido' em QUALITY_SCORECARD*.md referenciam artefato existente em docs/evidence-runs/**."""
    checks = 0
    errors: list[str] = []

    scorecard_files = list(root_dir.glob("docs/QUALITY_SCORECARD*.md"))
    for p in scorecard_files:
        rel = str(p.relative_to(root_dir))
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        for lno, line in enumerate(lines, 1):
            if not line.strip().startswith("|"):
                continue
            # Look for status cell: | Met | or | Atendido |
            if re.search(r"\|\s*(?:`?(?:Met|Atendido)`?)\s*\|", line):
                checks += 1
                art_match = re.search(r"\[.*?\]\(((?:docs/)?evidence-runs/[^)]+)\)", line)
                if not art_match:
                    errors.append(
                        f"{rel}:{lno}: linha com status 'Met'/'Atendido' não referencia artefato em docs/evidence-runs/**"
                    )
                else:
                    art_rel = art_match.group(1)
                    if not art_rel.startswith("docs/"):
                        art_path = root_dir / "docs" / art_rel
                    else:
                        art_path = root_dir / art_rel
                    if not art_path.is_file():
                        errors.append(
                            f"{rel}:{lno}: artefato de evidência referenciado '{art_rel}' não existe no repositório"
                        )

    return checks, errors


def validate_self_audit_rigor(root_dir: Path) -> tuple[int, list[str]]:
    """Valida rigor metodológico em SELF_AUDIT*.md: proíbe 'Agree' e fontes genéricas sem caminho/URL."""
    checks = 0
    errors: list[str] = []

    self_audit_files = list(root_dir.glob("docs/SELF_AUDIT*.md"))
    for p in self_audit_files:
        rel = str(p.relative_to(root_dir))
        try:
            lines = p.read_text(encoding="utf-8").splitlines()
        except Exception:
            continue

        for lno, line in enumerate(lines, 1):
            if not line.strip().startswith("|"):
                continue
            if "---" in line or "| #" in line or "| Package" in line or "| Pacote" in line:
                continue

            checks += 1
            if re.search(r"\bAgree\b", line):
                errors.append(
                    f"{rel}:{lno}: veredito 'Agree' não é permitido (use vereditos rastreáveis: supported-by-repo-data, supported-by-external-source, unverified, contradicted)"
                )

            cells = [c.strip() for c in line.split("|")]
            if len(cells) >= 6:
                source_cell = ""
                for c in cells[3:]:
                    if any(
                        kw in c.lower()
                        for kw in [
                            "http://",
                            "https://",
                            "reports/",
                            "docs/",
                            "data/",
                            "firmware",
                            "dumpsys",
                            "gapps",
                            "play",
                            "aosp",
                        ]
                    ):
                        source_cell = c
                        break
                if source_cell:
                    has_link = bool(
                        re.search(r"\[.*?\]\((https?://[^)]+|[a-zA-Z0-9_\-\./]+)\)", source_cell)
                    )
                    has_url = bool(re.search(r"https?://", source_cell))
                    has_repo_path = any(
                        (root_dir / part.strip("`(),[] ")).exists()
                        for part in source_cell.split()
                        if "/" in part
                    )
                    if not (has_link or has_url or has_repo_path):
                        errors.append(
                            f"{rel}:{lno}: fonte genérica '{source_cell}' sem caminho de arquivo existente nem URL válida"
                        )

    return checks, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Raiz do repositório")
    args = parser.parse_args()

    base_dir = args.repo_root
    allowlist_path = base_dir / "data/claims_allowlist.json"

    total_checks = 0
    all_errors: list[str] = []

    c1, errs1 = validate_claims(base_dir, allowlist_path)
    total_checks += c1
    all_errors.extend(errs1)

    c2, errs2 = validate_metrics_json(base_dir)
    total_checks += c2
    all_errors.extend(errs2)

    if all_errors:
        print(f"FALHA: {len(all_errors)} violação(ões) de alegações/métricas:")
        for err in all_errors:
            print(f" - {err}")
        return 1

    print(f"OK: {total_checks} verificações de alegações e métricas concluídas com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
