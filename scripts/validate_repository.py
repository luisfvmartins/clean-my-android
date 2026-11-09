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
            if parsed.scheme:
                if parsed.scheme.lower() == "file":
                    fail(
                        f"{markdown.relative_to(ROOT)}: link file:// não é portátil "
                        f"e não deve ser publicado: {destination}"
                    )
                continue
            if destination.startswith("//") or not parsed.path:
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
    """Valida evidências declaradas individualmente para cada dispositivo."""
    global checks
    catalog_path = ROOT / "data/device_catalog.json"
    if not catalog_path.exists():
        fail("data/device_catalog.json inexistente para validação de homologação")
        return

    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    devices = data.get("devices", [])

    def check_evidence_paths(device_id: str, evidence: dict, key: str) -> bool:
        global checks
        raw_paths = evidence.get(key)
        if isinstance(raw_paths, str):
            paths = [raw_paths]
        elif isinstance(raw_paths, list):
            paths = raw_paths
        else:
            paths = []

        checks += 1
        if not paths:
            fail(f"{device_id}: evidência obrigatória ausente no catálogo: evidence.{key}")
            return False

        valid = True
        for relative in paths:
            checks += 1
            if not isinstance(relative, str) or not relative.strip():
                fail(f"{device_id}: caminho inválido em evidence.{key}")
                valid = False
                continue
            candidate = (ROOT / relative).resolve()
            try:
                candidate.relative_to(ROOT.resolve())
            except ValueError:
                fail(f"{device_id}: evidência fora do repositório: {relative}")
                valid = False
                continue
            if not candidate.is_file() or candidate.stat().st_size == 0:
                fail(f"{device_id}: arquivo de evidência inexistente ou vazio: {relative}")
                valid = False
        return valid

    for device in devices:
        checks += 1
        device_id = device.get("id", "sem-id")
        level = device.get("homologation_level")
        if not isinstance(level, int) or isinstance(level, bool) or not 0 <= level <= 4:
            fail(f"{device_id}: nível de homologação inválido ({level}); esperado de 0 a 4.")
            continue

        evidence = device.get("evidence")
        if not isinstance(evidence, dict):
            evidence = {}

        if level >= 1:
            check_evidence_paths(device_id, evidence, "inventory")

        if level >= 2:
            check_evidence_paths(device_id, evidence, "audit")

        if level >= 3:
            check_evidence_paths(device_id, evidence, "functional_tests")

        if level == 4:
            check_evidence_paths(device_id, evidence, "script")
            check_evidence_paths(device_id, evidence, "rollback")
            script_version = device.get("script_version")
            script_sha256 = device.get("script_sha256")
            approved_scope = device.get("approved_scope")
            reviewer = device.get("reviewer")
            reviewed_at = device.get("reviewed_at")

            checks += 5
            if not isinstance(script_version, str) or not script_version.strip():
                fail(f"{device_id}: Nível 4 exige script_version.")
            if not isinstance(script_sha256, str) or not re.fullmatch(r"[a-fA-F0-9]{64}", script_sha256):
                fail(f"{device_id}: Nível 4 exige script_sha256 SHA-256 válido.")
            if not isinstance(approved_scope, list) or not approved_scope:
                fail(f"{device_id}: Nível 4 exige approved_scope explícito.")
            if not isinstance(reviewer, str) or not reviewer.strip():
                fail(f"{device_id}: Nível 4 exige reviewer identificado.")
            if not isinstance(reviewed_at, str) or not reviewed_at.strip():
                fail(f"{device_id}: Nível 4 exige reviewed_at.")


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
