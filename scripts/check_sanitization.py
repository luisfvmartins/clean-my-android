#!/usr/bin/env python3
"""Verificador de sanitização de dados sensíveis e privacidade.

Inspeciona arquivos do repositório garantindo que nenhum dado identificável de
dispositivo, rede ou usuário (IMEI, MAC, IP privado, e-mail, telefone, credenciais,
nomes de conta) seja publicado sem ofuscação.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ALLOWLIST_PATH = ROOT / "data/sanitization_allowlist.json"

# Padrões de detecção de dados sensíveis
MAC_RE = re.compile(r"(?<![a-zA-Z0-9_])([0-9a-fA-F]{2}(?::[0-9a-fA-F]{2}){5})(?![a-zA-Z0-9_])")
IMEI_RE = re.compile(r"\b(\d{15})\b")
PRIVATE_IPV4_RE = re.compile(r"\b((?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3}|192\.168\.\d{1,3}\.\d{1,3}))\b")
ACCOUNT_RE = re.compile(r"Account\s*\{\s*name\s*=\s*([^,}]+)")
EMAIL_RE = re.compile(r"\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,7})\b")
PHONE_BR_RE = re.compile(r"(?:\+55\s?)?(?:\([1-9]{2}\)\s?|[1-9]{2}\s?)9\d{4}[-\s]?\d{4}\b")
SERIAL_PROP_RE = re.compile(r"\b(?:ro\.serialno|ro\.boot\.serialno)\s*[:=]\s*([a-zA-Z0-9]{6,})\b", re.IGNORECASE)
HOME_USER_RE = re.compile(r"/home/([a-zA-Z0-9_.-]+)/(?:Desktop|Downloads|Documents|Pictures|Videos|Android)")

DUMMY_MACS = {
    "00:00:00:00:00:00",
    "02:00:00:00:00:00",
    "ff:ff:ff:ff:ff:ff",
    "FF:FF:FF:FF:FF:FF",
}


def is_luhn_valid(num_str: str) -> bool:
    """Valida se uma sequência numérica satisfaz o algoritmo de Luhn (usado em IMEIs)."""
    if not num_str.isdigit() or len(num_str) != 15:
        return False
    digits = [int(c) for c in num_str]
    checksum = 0
    for i, d in enumerate(reversed(digits)):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        checksum += d
    return checksum % 10 == 0


def load_allowlist() -> set[tuple[str, str]]:
    """Carrega tuplas (caminho_relativo, valor) permitidas da allowlist."""
    if not ALLOWLIST_PATH.is_file():
        return set()
    try:
        data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
        entries = data.get("allowlist", [])
        return {(e["path"], str(e["value"])) for e in entries if "path" in e and "value" in e}
    except Exception as exc:
        print(f"AVISO: Não foi possível ler allowlist: {exc}", file=sys.stderr)
        return set()


def check_file(path: Path, allowlist: set[tuple[str, str]]) -> list[str]:
    """Inspeciona um arquivo de texto e retorna lista de violações encontradas."""
    violations: list[str] = []
    try:
        rel_path = path.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = str(path)

    # Ignorar a própria allowlist
    if path.resolve() == ALLOWLIST_PATH.resolve():
        return violations

    # Ignorar extensões binárias
    if path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp", ".zip", ".apk", ".apex", ".pyc"}:
        return violations

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return violations

    lines = content.splitlines()
    for lno, line in enumerate(lines, 1):
        # 1. MAC Address
        for mac in MAC_RE.findall(line):
            if mac in DUMMY_MACS:
                continue
            if (rel_path, mac) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Endereço MAC exposto: {mac}")

        # 2. IMEI com validação de Luhn
        for imei in IMEI_RE.findall(line):
            if is_luhn_valid(imei):
                if (rel_path, imei) in allowlist:
                    continue
                violations.append(f"{rel_path}:{lno}: IMEI válido detectado: {imei}")

        # 3. IPv4 Privado
        for ip in PRIVATE_IPV4_RE.findall(line):
            if (rel_path, ip) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Endereço IP privado detectado: {ip}")

        # 4. Nome de Conta pessoal
        for acc in ACCOUNT_RE.findall(line):
            acc_clean = acc.strip()
            if (rel_path, acc_clean) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Identificador de conta exposto: Account{{name={acc_clean}}}")

        # 5. E-mails (exclui pacotes APEX com formato package@version.apex e exemplos)
        for email in EMAIL_RE.findall(line):
            if email.endswith(".apex") or email.endswith(("@example.com", "@android.com", "@users.noreply.github.com")):
                continue
            if (rel_path, email) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Endereço de e-mail detectado: {email}")

        # 6. Número de Telefone Brasileiro
        for phone in PHONE_BR_RE.findall(line):
            if (rel_path, phone) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Possível número de telefone exposto: {phone}")

        # 7. Serial de Hardware
        for serial in SERIAL_PROP_RE.findall(line):
            if serial.lower() in {"unknown", "none", "redacted"}:
                continue
            if (rel_path, serial) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Número de série de hardware exposto: {serial}")

        # 8. Caminho de usuário local pessoal
        for user in HOME_USER_RE.findall(line):
            if user in {"runner", "ubuntu", "user"}:
                continue
            violations.append(f"{rel_path}:{lno}: Caminho com usuário local pessoal exposto: /home/{user}/...")

    return violations


def scan_directories(dirs: list[Path]) -> list[str]:
    allowlist = load_allowlist()
    all_violations: list[str] = []

    for base_dir in dirs:
        if not base_dir.exists():
            continue
        for p in sorted(base_dir.rglob("*")):
            if p.is_file():
                violations = check_file(p, allowlist)
                all_violations.extend(violations)

    return all_violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Diretórios ou arquivos a verificar (padrão: reports, data, docs)")
    args = parser.parse_args()

    targets = [ROOT / p for p in args.paths] if args.paths else [ROOT / "reports", ROOT / "data", ROOT / "docs"]
    violations = scan_directories(targets)

    if violations:
        print(f"FALHA: {len(violations)} problema(s) de sanitização encontrado(s):", file=sys.stderr)
        for v in violations:
            print(f" - {v}", file=sys.stderr)
        return 1

    print("OK: Verificação de sanitização concluída sem violações de privacidade.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
