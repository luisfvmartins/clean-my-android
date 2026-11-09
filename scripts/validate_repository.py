#!/usr/bin/env python3
"""Valida a estrutura básica do repositório sem acessar dispositivos Android."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path
from urllib.parse import unquote, urlsplit

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


def validate_statistics() -> None:
    global checks
    checks += 1
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/generate_statistics.py"), "--check"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        fail(f"estatísticas desatualizadas ou inválidas: {detail}")



REFERENCE_DEFINITION_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|(?:\\.|[^\s])+)")

def unescape_markdown_destination(destination: str) -> str:
    """Unescape Markdown punctuation in a link destination."""
    return re.sub(r"\\([\\() ])", r"\1", destination)


def markdown_destinations(content: str):
    """Yield inline-link and reference-definition destinations outside code blocks."""
    visible_lines: list[str] = []
    fence_char: str | None = None
    fence_length = 0
    in_indented_code = False
    previous_blank = True

    for line in content.splitlines():
        fence = re.match(r"^ {0,3}(\x60{3,}|~{3,})", line)
        if fence:
            marker = fence.group(1)
            if fence_char is None:
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = None
                fence_length = 0
            continue
        if fence_char is not None:
            continue

        if not line.strip():
            visible_lines.append("")
            previous_blank = True
            if in_indented_code:
                continue
            continue

        indented = line.startswith("    ") or line.startswith("\t")
        if indented and (previous_blank or in_indented_code):
            in_indented_code = True
            previous_blank = False
            continue

        in_indented_code = False
        previous_blank = False
        visible_lines.append(line)

    text = "\n".join(visible_lines)
    text = re.sub(r"(?<!\\)\x60+[^\\n]*?(?<!\\)\x60+", "", text)

    # Parse inline links while respecting balanced and escaped parentheses.
    for match in re.finditer(r"\]\(\s*", text):
        index = match.end()
        if index >= len(text):
            continue

        if text[index] == "<":
            start = index + 1
            index = start
            escaped = False
            while index < len(text):
                char = text[index]
                if escaped:
                    escaped = False
                elif char == "\\":
                    escaped = True
                elif char == ">":
                    break
                index += 1
            if index < len(text) and text[index] == ">":
                destination = text[start:index]
                if destination:
                    yield unescape_markdown_destination(destination)
            continue

        start = index
        depth = 0
        escaped = False
        while index < len(text):
            char = text[index]
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == "(":
                depth += 1
            elif char == ")":
                if depth == 0:
                    break
                depth -= 1
            elif char.isspace() and depth == 0:
                break
            index += 1

        destination = text[start:index]
        if destination:
            yield unescape_markdown_destination(destination)

    # Reference-style link definitions.
    for line in visible_lines:
        match = REFERENCE_DEFINITION_RE.match(line)
        if match:
            destination = match.group(1)
            if destination.startswith("<") and destination.endswith(">"):
                destination = destination[1:-1]
            yield unescape_markdown_destination(destination)


def validate_markdown_links() -> None:
    """Check that local Markdown links point to files or directories in the repository."""
    global checks
    for markdown in sorted(ROOT.rglob("*.md")):
        if ".git" in markdown.parts:
            continue
        try:
            content = markdown.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            fail(f"{markdown.relative_to(ROOT)}: não foi possível ler Markdown ({exc})")
            continue

        for destination in markdown_destinations(content):
            parsed = urlsplit(destination)
            if parsed.scheme or destination.startswith("//") or not parsed.path:
                continue

            target = unquote(parsed.path)
            candidate = ROOT / target.lstrip("/") if target.startswith("/") else markdown.parent / target
            checks += 1
            try:
                resolved = candidate.resolve()
                resolved.relative_to(ROOT.resolve())
            except (OSError, ValueError):
                fail(
                    f"{markdown.relative_to(ROOT)}: link local fora do repositório "
                    f"ou inválido: {destination}"
                )
                continue

            if not resolved.exists():
                fail(
                    f"{markdown.relative_to(ROOT)}: destino de link inexistente: "
                    f"{destination}"
                )



def validate_bilingual_parity() -> None:
    global checks
    checks += 1
    result = subprocess.run(
        [sys.executable, str(ROOT / "scripts/validate_bilingual_parity.py")],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = (result.stderr or result.stdout).strip()
        fail(f"paridade bilíngue violada: {detail}")


def validate_homologation_levels_and_evidence() -> None:
    global checks
    catalog_path = ROOT / "data/device_catalog.json"
    if not catalog_path.exists():
        fail("data/device_catalog.json inexistente para validação de homologação")
        return

    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    devices = data.get("devices", [])

    for d in devices:
        checks += 1
        dev_id = d.get("id", "sem-id")
        level = d.get("homologation_level")
        if level is None or not isinstance(level, int) or level < 0 or level > 4:
            fail(f"{dev_id}: nível de homologação inválido ({level}). Deve ser 0 a 4.")
            continue

        report_dir = (ROOT / d["report"]).parent

        # Nível 1: Exige inventário documentado
        if level >= 1:
            checks += 1
            has_inventory = (
                (report_dir / "before/packages.txt").exists()
                or (report_dir / "packages.txt").exists()
                or (report_dir / "before/inventory.json").exists()
                or (ROOT / "docs/auditorias/moto-g54/lote-02-ecossistema-google.md").exists()
            )
            if not has_inventory:
                fail(f"{dev_id}: Nível {level} exige inventário documentado (packages.txt/inventory.json)")

        # Nível 2: Exige justificativa e registro de auditoria/modificações
        if level >= 2:
            checks += 1
            has_audit = (
                (report_dir / "audit.md").exists()
                or (report_dir / "auditoria.md").exists()
                or (report_dir / "comparison-report.md").exists()
                or (report_dir / "README.md").exists()
            )
            if not has_audit:
                fail(f"{dev_id}: Nível {level} exige documento de auditoria/análise")

        # Nível 3: Exige matriz de testes funcionais ou comparativo estruturado
        if level >= 3:
            checks += 1
            has_validation = (
                (report_dir / "comparativo.json").exists()
                or (report_dir / "comparison-report.md").exists()
            )
            if not has_validation:
                fail(f"{dev_id}: Nível {level} exige comparativo.json ou comparison-report.md com testes funcionais")

        # Nível 4: Script homologado - atualmente nenhum dispositivo reivindica
        if level == 4:
            fail(f"{dev_id}: Nível 4 (Script homologado) requer teste comunitário multi-dispositivo formal")


def main() -> int:
    validate_json_files()
    validate_shell_scripts()
    validate_protected_packages()
    validate_statistics()
    validate_markdown_links()
    validate_bilingual_parity()
    validate_homologation_levels_and_evidence()

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
