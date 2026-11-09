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

DEFAULT_PATTERN = re.compile(r"(?i)\b(?:" + "|".join(DEFAULT_TERMS) + r")\b")
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

    target_extensions = (".md", ".json", ".txt")
    for path in sorted(base_dir.rglob("*")):
        if ".git" in path.parts or ".pytest_cache" in path.parts or "__pycache__" in path.parts:
            continue
        if not path.is_file() or path.suffix not in target_extensions:
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

        for lno, line in enumerate(content.splitlines(), 1):
            checks += 1
            match = DEFAULT_PATTERN.search(line)
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
