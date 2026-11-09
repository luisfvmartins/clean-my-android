#!/usr/bin/env python3
"""Gera estatísticas e sincroniza as tabelas de dispositivos nos READMEs principais.

Não acessa dispositivos, não consulta a API do GitHub e não infere dados ausentes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/device_catalog.json"
OUTPUT_MD = ROOT / "docs/ESTATISTICAS.md"
OUTPUT_EN_MD = ROOT / "docs/ESTATISTICAS.en.md"
README_PT = ROOT / "README.pt-BR.md"
README_EN = ROOT / "README.md"

MARKER_BEGIN = "<!-- BEGIN_AUDITED_DEVICES -->"
MARKER_END = "<!-- END_AUDITED_DEVICES -->"


def load_catalog() -> list[dict]:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("devices"), list):
        raise ValueError("Catálogo: estrutura ou schema_version inválido")
    devices = data["devices"]
    seen: set[str] = set()
    for item in devices:
        required = (
            "id", "manufacturer", "model", "model_code", "android_version_status",
            "audit_status", "component_count", "component_count_label",
            "component_count_status", "report", "catalog"
        )
        missing = [key for key in required if key not in item]
        if missing:
            raise ValueError(f"Registro incompleto ({item.get('id', 'sem id')}): {', '.join(missing)}")
        if item["id"] in seen:
            raise ValueError(f"ID de dispositivo duplicado: {item['id']}")
        seen.add(item["id"])
        count = item["component_count"]
        if not isinstance(count, int) or count < 0:
            raise ValueError(f"Contagem inválida em {item['id']}")
        for key in ("report", "catalog"):
            if not (ROOT / item[key]).is_file():
                raise ValueError(f"Fonte inexistente para {item['id']}: {item[key]}")
        version = item.get("android_version")
        if version is not None and not isinstance(version, str):
            raise ValueError(f"Versão Android inválida em {item['id']}")
    return devices


def build_statistics_pt(devices: list[dict]) -> str:
    manufacturers = Counter(d["manufacturer"] for d in devices)
    versions = sorted({d["android_version"] for d in devices if d.get("android_version")})
    lines = [
        "# Estatísticas do projeto",
        "",
        "Indicadores calculados a partir do catálogo estruturado em "
        "[data/device_catalog.json](../data/device_catalog.json). "
        "Os números refletem somente informações documentadas e explicitamente classificadas.",
        "",
        "## Visão geral",
        "",
        f"- **Dispositivos catalogados:** {len(devices)}",
        f"- **Fabricantes representados:** {len(manufacturers)}",
        f"- **Versões Android confirmadas:** {len(versions)}"
        + (f" ({', '.join(versions)})" if versions else ""),
        f"- **Relatórios com contagem de componentes:** {sum(1 for d in devices if d.get('component_count') is not None)}",
        "",
        "## Dispositivos",
        "",
        "| Fabricante / modelo | Código | Android | Situação da auditoria | Componentes registrados |",
        "|---|---|---|---|---:|",
    ]
    for d in devices:
        version = d.get("android_version")
        android = f"Android {version}" if version else f"Não confirmado ({d['android_version_status']})"
        report_path = Path(__import__('os').path.relpath(ROOT / d['report'], OUTPUT_MD.parent)).as_posix()
        report = f"[{d['audit_status']}]({report_path})"
        count = f"{d['component_count']} — {d['component_count_label']}"
        lines.append(f"| {d['manufacturer']} {d['model']} | {d['model_code']} | {android} | {report} | {count} |")
    lines.extend([
        "",
        "## Como interpretar os números",
        "",
        "- **Contagens de componentes não são somadas.** Os relatórios usam escopos e estados diferentes: "
        "o Moto G54 registra componentes auditados; o Edge 60 Pro registra componentes mapeados no inventário inicial.",
        "- A contagem do Moto G54 é de 462 componentes na coleta local; a versão pública omite 29 aplicativos "
        "instalados pelo usuário e publica 433 componentes: 394 pacotes de sistema/fabricante e 39 módulos APEX.",
        "- A contagem do Edge 60 Pro (501) refere-se ao inventário inicial mapeado e não significa que todos "
        "os componentes tenham sido validados funcionalmente.",
        "- Versões Android pendentes não entram na contagem de versões confirmadas.",
        "- **Dispositivo catalogado**, **auditoria publicada**, **validação funcional** e **homologação de script** "
        "são estados diferentes. A presença nesta página não implica homologação.",
        "- Não são estimados ganhos de bateria, RAM, armazenamento, privacidade ou compatibilidade.",
        "",
        "## Atualização e validação",
        "",
        "Os dados são mantidos em data/device_catalog.json. Ao adicionar ou atualizar uma auditoria, "
        "revise esse arquivo com informações sustentadas pelos documentos do dispositivo e execute:",
        "",
        "    python scripts/generate_statistics.py",
        "    python scripts/generate_statistics.py --check",
        "",
        "A validação automatizada verifica se esta página corresponde ao catálogo. A geração não consulta "
        "a API do GitHub, não conta Pull Requests e não acessa nem modifica aparelhos.",
        "",
        "Consulte o [catálogo completo de auditorias](../reports/README.md).",
        "",
    ])
    return "\n".join(lines)


def build_statistics_en(devices: list[dict]) -> str:
    manufacturers = Counter(d["manufacturer"] for d in devices)
    versions = sorted({d["android_version"] for d in devices if d.get("android_version")})
    lines = [
        "# Project Statistics",
        "",
        "Metrics are calculated from the structured catalog in [data/device_catalog.json](../data/device_catalog.json). Counts reflect only documented and explicitly classified information.",
        "",
        "## Overview",
        "",
        f"- **Cataloged devices:** {len(devices)}",
        f"- **Represented manufacturers:** {len(manufacturers)}",
        f"- **Confirmed Android versions:** {len(versions)}"
        + (f" ({', '.join(versions)})" if versions else ""),
        f"- **Reports with component counts:** {sum(1 for d in devices if d.get('component_count') is not None)}",
        "",
        "## Devices",
        "",
        "| Manufacturer / model | Code | Android | Audit status | Recorded components |",
        "|---|---|---|---|---:|",
    ]
    for d in devices:
        version = d.get("android_version")
        android = f"Android {version}" if version else f"Not confirmed ({d['android_version_status']})"
        report_en_rel = d.get("report_en") or d["report"]
        report_path = Path(__import__('os').path.relpath(ROOT / report_en_rel, OUTPUT_EN_MD.parent)).as_posix()
        status_en = d.get("audit_status_en") or d["audit_status"]
        report = f"[{status_en}]({report_path})"
        label_en = d.get("component_count_label_en") or d["component_count_label"]
        count = f"{d['component_count']} — {label_en}"
        lines.append(f"| {d['manufacturer']} {d['model']} | {d['model_code']} | {android} | {report} | {count} |")
    lines.extend([
        "",
        "## How to interpret the numbers",
        "",
        "- **Component counts are not added together.** Reports use different scopes and states: Moto G54 records audited components; Edge 60 Pro records components mapped in the initial inventory.",
        "- The Moto G54 count is 462 components in the local collection; the public version omits 29 user-installed apps and publishes 433 components: 394 system/manufacturer package records and 39 APEX modules.",
        "- The Edge 60 Pro count (501) refers to the mapped initial inventory and does not mean every component has been functionally validated.",
        "- Pending Android versions are excluded from the confirmed-version count.",
        "- **Cataloged device**, **published audit**, **functional validation**, and **script approval** are different states. Listing a device here does not imply approval.",
        "- Battery, RAM, storage, privacy, or compatibility improvements are not estimated.",
        "",
        "## Updates and validation",
        "",
        "Data is maintained in `data/device_catalog.json`. When adding or updating an audit, revise that file using information supported by the device documentation and run:",
        "",
        "    python scripts/generate_statistics.py",
        "    python scripts/generate_statistics.py --check",
        "",
        "The automated validation verifies that this page, the Portuguese statistics, and root READMEs correspond to the structured catalog. Generation does not query the GitHub API, count Pull Requests, or access or modify devices.",
        "",
        "See the [complete audit catalog](../reports/README.md).",
        "",
    ])
    return "\n".join(lines)


def build_readme_table_pt(devices: list[dict]) -> str:
    lines = [
        "| Dispositivo | Documentação | Situação |",
        "|---|---|---|",
    ]
    for d in devices:
        name = f"{d['manufacturer']} {d['model']} ({d['model_code']})"
        docs = d.get("readme_links_pt") or f"[{d['audit_status']}]({d['report']})"
        status = d.get("readme_status_pt") or d["audit_status"]
        lines.append(f"| {name} | {docs} | {status} |")
    return "\n".join(lines)


def build_readme_table_en(devices: list[dict]) -> str:
    lines = [
        "| Device | Documentation | Status |",
        "|---|---|---|",
    ]
    for d in devices:
        name = f"{d['manufacturer']} {d['model']} ({d['model_code']})"
        docs = d.get("readme_links_en") or f"[{d.get('audit_status_en', d['audit_status'])}]({d.get('report_en', d['report'])})"
        status = d.get("readme_status_en") or d.get("audit_status_en") or d["audit_status"]
        lines.append(f"| {name} | {docs} | {status} |")
    return "\n".join(lines)


def update_readme_content(original: str, new_table: str, filename: str) -> str:
    pattern = re.compile(
        rf"({re.escape(MARKER_BEGIN)}\n).*?(\n{re.escape(MARKER_END)})",
        re.DOTALL
    )
    if not pattern.search(original):
        raise ValueError(f"Marcadores {MARKER_BEGIN} / {MARKER_END} não encontrados em {filename}")
    return pattern.sub(rf"\g<1>{new_table}\g<2>", original)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="falha se alguma página ou README estiver desatualizado")
    args = parser.parse_args()
    try:
        devices = load_catalog()
        expected_stat_pt = build_statistics_pt(devices)
        expected_stat_en = build_statistics_en(devices)
        table_pt = build_readme_table_pt(devices)
        table_en = build_readme_table_en(devices)

        current_readme_pt = README_PT.read_text(encoding="utf-8")
        current_readme_en = README_EN.read_text(encoding="utf-8")

        expected_readme_pt = update_readme_content(current_readme_pt, table_pt, "README.pt-BR.md")
        expected_readme_en = update_readme_content(current_readme_en, table_en, "README.md")
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1

    if args.check:
        errors = []
        if not OUTPUT_MD.is_file() or OUTPUT_MD.read_text(encoding="utf-8") != expected_stat_pt:
            errors.append("docs/ESTATISTICAS.md está desatualizado.")
        if not OUTPUT_EN_MD.is_file() or OUTPUT_EN_MD.read_text(encoding="utf-8") != expected_stat_en:
            errors.append("docs/ESTATISTICAS.en.md está desatualizado.")
        if current_readme_pt != expected_readme_pt:
            errors.append("README.pt-BR.md (tabela de dispositivos) está desatualizado.")
        if current_readme_en != expected_readme_en:
            errors.append("README.md (tabela de dispositivos) está desatualizado.")

        if errors:
            print("FALHA: Verificações de sincronização falharam:", file=sys.stderr)
            for err in errors:
                print(f" - {err}", file=sys.stderr)
            print("Execute 'python3 scripts/generate_statistics.py' para sincronizar.", file=sys.stderr)
            return 1

        print("OK: estatísticas e tabelas de dispositivos correspondem ao catálogo estruturado.")
        return 0

    OUTPUT_MD.write_text(expected_stat_pt, encoding="utf-8")
    OUTPUT_EN_MD.write_text(expected_stat_en, encoding="utf-8")
    README_PT.write_text(expected_readme_pt, encoding="utf-8")
    README_EN.write_text(expected_readme_en, encoding="utf-8")

    print(f"OK: ESTATISTICAS (.md/.en.md) e READMEs atualizados com {len(devices)} dispositivos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
