#!/usr/bin/env python3
"""Valida a estrutura bilíngue e a presença de indicadores selecionados.

Verifica pares de arquivos, presença de códigos de dispositivos, igualdade dos
identificadores de pacotes extraídos de tabelas específicas e presença de
marcadores numéricos selecionados. Não avalia equivalência semântica, tradução
integral nem correspondência entre rótulos e valores de todas as métricas.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/device_catalog.json"

PACKAGE_COL_RE = re.compile(r"^`([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)`$")

# Pares mandatórios de arquivos bilíngues
MANDATORY_PAIRS: list[tuple[str, str]] = [
    # Documentos raiz
    ("README.pt-BR.md", "README.md"),
    ("CONTRIBUTING.pt-BR.md", "CONTRIBUTING.md"),
    ("AI_INSTRUCTIONS.pt-BR.md", "AI_INSTRUCTIONS.md"),
    ("reports/README.pt-BR.md", "reports/README.md"),
    # Guias em docs/
    ("docs/DOS-AND-DONTS.pt-BR.md", "docs/DOS-AND-DONTS.md"),
    ("docs/PR_REVIEW_GUIDE.pt-BR.md", "docs/PR_REVIEW_GUIDE.md"),
    ("docs/USER_DEVICE_AUDIT.pt-BR.md", "docs/USER_DEVICE_AUDIT.md"),
    ("docs/AUDIT_STATUS_AND_HOMOLOGATION.pt-BR.md", "docs/AUDIT_STATUS_AND_HOMOLOGATION.md"),
    ("docs/APRESENTACAO_METODO_E_RESULTADOS.md", "docs/APRESENTACAO_METODO_E_RESULTADOS.en.md"),
    ("docs/SANITIZATION_LOG.md", "docs/SANITIZATION_LOG.en.md"),
    ("docs/ESTATISTICAS.md", "docs/ESTATISTICAS.en.md"),
    ("docs/EVOLUCAO_CONTRIBUICOES.md", "docs/EVOLUCAO_CONTRIBUICOES.en.md"),
    # Dispositivos - READMEs de pasta
    ("reports/motorola/moto-g54-5g/README.md", "reports/motorola/moto-g54-5g/README.en.md"),
    ("reports/motorola/edge-60-pro/README.md", "reports/motorola/edge-60-pro/README.en.md"),
    ("reports/motorola/edge-60-fusion/README.md", "reports/motorola/edge-60-fusion/README.en.md"),
    ("reports/samsung/galaxy-a30s/README.md", "reports/samsung/galaxy-a30s/README.en.md"),
    # Dispositivos - Relatórios e resumos
    ("reports/motorola/edge-60-pro/auditoria.md", "reports/motorola/edge-60-pro/auditoria.en.md"),
    ("reports/motorola/edge-60-pro/historical-summary.pt-BR.md", "reports/motorola/edge-60-pro/historical-summary.en.md"),
    ("reports/samsung/galaxy-a30s/comparison-report.md", "reports/samsung/galaxy-a30s/comparison-report.en.md"),
    ("reports/samsung/galaxy-a30s/changes/change-log.md", "reports/samsung/galaxy-a30s/changes/change-log.en.md"),
    ("docs/AUDITORIA_MOTO_G54_5G.md", "docs/AUDITORIA_MOTO_G54_5G.en.md"),
    ("docs/auditorias/moto-g54/README.md", "docs/auditorias/moto-g54/README.en.md"),
]

# Adicionar lotes publicados do Moto G54 (Lotes 02 a 08)
for i in range(2, 9):
    matches = [
        p for p in (ROOT / "docs/auditorias/moto-g54").glob(f"lote-{i:02d}-*.md")
        if not p.name.endswith(".en.md")
    ]
    if matches:
        pt_file = matches[0]
        en_file = pt_file.with_name(pt_file.stem + ".en.md")
        MANDATORY_PAIRS.append((str(pt_file.relative_to(ROOT)), str(en_file.relative_to(ROOT))))


def check_bilingual_pairs(errors: list[str]) -> int:
    checks = 0
    for pt_rel, en_rel in MANDATORY_PAIRS:
        pt_path = ROOT / pt_rel
        en_path = ROOT / en_rel
        checks += 1
        if not pt_path.is_file():
            errors.append(f"Arquivo PT-BR ausente: {pt_rel}")
        checks += 1
        if not en_path.is_file():
            errors.append(f"Arquivo EN ausente: {en_rel}")
    return checks


def check_catalog_presence(errors: list[str]) -> int:
    checks = 0
    if not CATALOG.is_file():
        errors.append("data/device_catalog.json inexistente")
        return checks

    data = json.loads(CATALOG.read_text(encoding="utf-8"))
    devices = data.get("devices", [])

    reports_pt = (ROOT / "reports/README.pt-BR.md").read_text(encoding="utf-8")
    reports_en = (ROOT / "reports/README.md").read_text(encoding="utf-8")

    readme_pt = (ROOT / "README.pt-BR.md").read_text(encoding="utf-8")
    readme_en = (ROOT / "README.md").read_text(encoding="utf-8")

    for d in devices:
        model = d["model"]
        code = d["model_code"]
        checks += 4

        if code not in reports_pt:
            errors.append(f"Dispositivo {model} ({code}) não mencionado em reports/README.pt-BR.md")
        if code not in reports_en:
            errors.append(f"Dispositivo {model} ({code}) não mencionado em reports/README.md")
        if code not in readme_pt:
            errors.append(f"Dispositivo {model} ({code}) não mencionado em README.pt-BR.md")
        if code not in readme_en:
            errors.append(f"Dispositivo {model} ({code}) não mencionado em README.md")

    return checks


def extract_table_packages(path: Path) -> set[str]:
    packages = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|"):
            continue
        parts = [p.strip() for p in line.split("|")]
        if len(parts) > 3:
            match = PACKAGE_COL_RE.fullmatch(parts[3])
            if match:
                packages.add(match.group(1))
    return packages


def check_batch_package_parity(errors: list[str]) -> int:
    checks = 0
    for i in range(2, 9):
        matches = [
            p for p in (ROOT / "docs/auditorias/moto-g54").glob(f"lote-{i:02d}-*.md")
            if not p.name.endswith(".en.md")
        ]
        if not matches:
            continue
        pt_path = matches[0]
        en_path = pt_path.with_name(pt_path.stem + ".en.md")
        if not en_path.is_file():
            continue

        checks += 1
        pt_packages = extract_table_packages(pt_path)
        en_packages = extract_table_packages(en_path)

        diff_pt = pt_packages - en_packages
        diff_en = en_packages - pt_packages
        if diff_pt:
            errors.append(f"Lote {i:02d}: pacotes em PT-BR ausentes no EN: {', '.join(sorted(diff_pt))}")
        if diff_en:
            errors.append(f"Lote {i:02d}: pacotes em EN ausentes no PT-BR: {', '.join(sorted(diff_en))}")

    return checks


def check_galaxy_a30s_metric_presence(errors: list[str]) -> int:
    checks = 0
    pt_path = ROOT / "reports/samsung/galaxy-a30s/comparison-report.md"
    en_path = ROOT / "reports/samsung/galaxy-a30s/comparison-report.en.md"
    if not (pt_path.is_file() and en_path.is_file()):
        return checks

    pt_text = pt_path.read_text(encoding="utf-8")
    en_text = en_path.read_text(encoding="utf-8")

    # Verificar apenas a presença dos marcadores numéricos em ambos os arquivos; não compara seus rótulos ou contexto.
    for num in ("392", "391", "343", "47", "26.0°C", "25.3°C", "25.4°C", "24.8°C"):
        checks += 2
        if num not in pt_text:
            errors.append(f"Galaxy A30s PT-BR: métrica '{num}' ausente em comparison-report.md")
        if num not in en_text:
            errors.append(f"Galaxy A30s EN: métrica '{num}' ausente em comparison-report.en.md")

    return checks


def main() -> int:
    errors: list[str] = []
    total_checks = 0

    total_checks += check_bilingual_pairs(errors)
    total_checks += check_catalog_presence(errors)
    total_checks += check_batch_package_parity(errors)
    total_checks += check_galaxy_a30s_metric_presence(errors)

    if errors:
        print(f"FALHA: {len(errors)} erro(s) de validação estrutural bilíngue encontrados em {total_checks} verificações:", file=sys.stderr)
        for err in errors:
            print(f" - {err}", file=sys.stderr)
        return 1

    print(f"OK: {total_checks} verificações estruturais, de identificadores e de presença de indicadores aprovadas sem erros.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
