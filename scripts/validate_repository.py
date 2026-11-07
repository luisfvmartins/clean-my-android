#!/usr/bin/env python3
"""Valida a estrutura básica do repositório sem acessar dispositivos Android."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
errors: list[str] = []
checks = 0


def fail(message: str) -> None:
    errors.append(message)


def validate_json_files() -> None:
    global checks
    files = sorted(ROOT.rglob("*.json"))
    for path in files:
        if ".git" in path.parts:
            continue
        checks += 1
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            fail(f"{path.relative_to(ROOT)}: JSON inválido ({exc})")
            continue

        if path.name == "comparativo.json":
            if not isinstance(data, dict):
                fail(f"{path.relative_to(ROOT)}: a raiz deve ser um objeto JSON")
                continue
            if "metrics" in data and not isinstance(data["metrics"], list):
                fail(f"{path.relative_to(ROOT)}: 'metrics' deve ser uma lista")
            for index, metric in enumerate(data.get("metrics", [])):
                if not isinstance(metric, dict):
                    fail(f"{path.relative_to(ROOT)}: metrics[{index}] deve ser um objeto")
                elif not str(metric.get("indicator", "")).strip():
                    fail(f"{path.relative_to(ROOT)}: metrics[{index}] não informa 'indicator'")


def validate_shell_scripts() -> None:
    global checks
    for path in sorted((ROOT / "scripts").glob("*.sh")):
        checks += 1
        result = subprocess.run(
            ["bash", "-n", str(path)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            detail = (result.stderr or result.stdout).strip()
            fail(f"{path.relative_to(ROOT)}: erro de sintaxe Bash: {detail}")


def validate_protected_packages() -> None:
    global checks
    path = ROOT / "data/protected_essential_packages.txt"
    if not path.exists():
        fail("data/protected_essential_packages.txt não encontrado")
        return

    seen: set[str] = set()
    pattern = re.compile(r"^[A-Za-z0-9_]+(?:\.[A-Za-z0-9_]+)+$")
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        value = raw.strip()
        if not value or value.startswith("#"):
            continue
        checks += 1
        if not pattern.fullmatch(value):
            fail(f"{path.relative_to(ROOT)}:{line_number}: nome de pacote inválido: {value}")
        if value in seen:
            fail(f"{path.relative_to(ROOT)}:{line_number}: pacote duplicado: {value}")
        seen.add(value)


def main() -> int:
    validate_json_files()
    validate_shell_scripts()
    validate_protected_packages()

    if errors:
        print(f"FALHA: {len(errors)} problema(s) encontrado(s) em {checks} verificações.")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"OK: {checks} verificações concluídas sem erros.")
    print("Nenhum dispositivo Android foi acessado ou modificado.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
