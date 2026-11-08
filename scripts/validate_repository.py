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



MARKDOWN_LINK_RE = re.compile(
    r"!?\[[^\]]*\]\(\s*(<[^>]+>|(?:\\.|[^)\s])+)"
    r"(?:\s+(?:\"[^\"]*\"|'[^']*'|\([^)]*\)))?\s*\)"
)
REFERENCE_DEFINITION_RE = re.compile(r"^\s{0,3}\[[^\]]+\]:\s*(<[^>]+>|\S+)")

def markdown_destinations(content: str):
    """Yield inline-link and reference-definition destinations outside code blocks."""
    visible_lines: list[str] = []
    fence_char: str | None = None
    fence_length = 0

    for line in content.splitlines():
        match = re.match(r"^\s{0,3}(\x60{3,}|~{3,})", line)
        if match:
            marker = match.group(1)
            if fence_char is None:
                fence_char = marker[0]
                fence_length = len(marker)
            elif marker[0] == fence_char and len(marker) >= fence_length:
                fence_char = None
                fence_length = 0
            continue
        if fence_char is None:
            visible_lines.append(line)

    text = "\n".join(visible_lines)
    text = re.sub(r"\x60+[^\x60]*\x60+", "", text)

    for match in MARKDOWN_LINK_RE.finditer(text):
        destination = match.group(1)
        yield destination[1:-1] if destination.startswith("<") and destination.endswith(">") else destination

    for line in visible_lines:
        match = REFERENCE_DEFINITION_RE.match(line)
        if match:
            destination = match.group(1)
            yield destination[1:-1] if destination.startswith("<") and destination.endswith(">") else destination


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



def main() -> int:
    validate_json_files()
    validate_shell_scripts()
    validate_protected_packages()
    validate_statistics()
    validate_markdown_links()

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
