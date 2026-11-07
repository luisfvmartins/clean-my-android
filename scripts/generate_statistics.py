#!/usr/bin/env python3
"""Gera estatísticas do Clean My Android a partir do catálogo estruturado.

Não acessa dispositivos, não consulta a API do GitHub e não infere dados ausentes.
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data/device_catalog.json"
OUTPUT = ROOT / "docs/ESTATISTICAS.md"


def load_catalog() -> list[dict]:
    data = json.loads(SOURCE.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1 or not isinstance(data.get("devices"), list):
        raise ValueError("Catálogo: estrutura ou schema_version inválido")
    devices = data["devices"]
    seen: set[str] = set()
    for item in devices:
        required = ("id", "manufacturer", "model", "model_code", "android_version_status",
                    "audit_status", "component_count", "component_count_label",
                    "component_count_status", "report", "catalog")
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


def build_markdown(devices: list[dict]) -> str:
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
        report = f"[{d['audit_status']}]({d['report']})"
        count = f"{d['component_count']} — {d['component_count_label']}"
        lines.append(f"| {d['manufacturer']} {d['model']} | {d['model_code']} | {android} | {report} | {count} |")
    lines.extend([
        "",
        "## Como interpretar os números",
        "",
        "- **Contagens de componentes não são somadas.** Os relatórios usam escopos e estados diferentes: "
        "o Moto G54 registra componentes auditados; o Edge 60 Pro registra componentes mapeados no inventário inicial.",
        "- A contagem do Moto G54 é de 462 componentes na coleta local; a versão pública omite 29 aplicativos "
        "instalados pelo usuário e documenta 394 componentes de sistema/fabricante.",
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


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="falha se a página gerada estiver desatualizada")
    args = parser.parse_args()
    try:
        devices = load_catalog()
        expected = build_markdown(devices)
    except (OSError, UnicodeError, json.JSONDecodeError, ValueError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != expected:
            print("FALHA: docs/ESTATISTICAS.md está desatualizado. Execute o gerador.", file=sys.stderr)
            return 1
        print("OK: estatísticas correspondem ao catálogo estruturado.")
        return 0
    OUTPUT.write_text(expected, encoding="utf-8")
    print(f"OK: {OUTPUT.relative_to(ROOT)} atualizado com {len(devices)} dispositivos.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
