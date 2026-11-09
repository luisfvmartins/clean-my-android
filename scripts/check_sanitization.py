#!/usr/bin/env python3
"""Verificador de sanitização de dados sensíveis e privacidade.

Inspeciona arquivos do repositório garantindo que nenhum dado identificável de
dispositivo, rede ou usuário (IMEI, MAC, IP privado IPv4/IPv6, e-mail, telefone,
credenciais, nomes de conta) seja publicado sem ofuscação.
"""
from __future__ import annotations

import argparse
import ipaddress
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
IPV6_CANDIDATE_RE = re.compile(r"(?<![a-zA-Z0-9_:])((?:[0-9a-fA-F]{1,4}:){2,7}[0-9a-fA-F]{1,4}|(?:[0-9a-fA-F]{1,4}:){1,7}:|:(?::[0-9a-fA-F]{1,4}){1,7}|fe80:[0-9a-fA-F:]+|fd[0-9a-fA-F]{2}:[0-9a-fA-F:]+|fc[0-9a-fA-F]{2}:[0-9a-fA-F:]+)(?![a-zA-Z0-9_:])")
ACCOUNT_RE = re.compile(r"Account\s*\{\s*name\s*=\s*([^,}]+)")
EMAIL_RE = re.compile(r"\b([A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,63})\b")

# Telefones brasileiros: celulares com 9 dígitos ou fixos com 8 dígitos (exigindo DDD formatado com parênteses ou separador)
PHONE_MOBILE_RE = re.compile(r"(?:\+55\s?)?(?:\([1-9]{2}\)\s?|[1-9]{2}\s?)9\d{4}[-\s]?\d{4}\b")
PHONE_LANDLINE_RE = re.compile(r"(?:\+55\s?)?(?:\([1-9]{2}\)\s*|[1-9]{2}\s+)[2-5]\d{3}[-\s]\d{4}\b")

SERIAL_PROP_RE = re.compile(r"\b(?:ro\.serialno|ro\.boot\.serialno)\s*[:=]\s*([a-zA-Z0-9]{6,})\b", re.IGNORECASE)
HOME_USER_RE = re.compile(r"/home/([a-zA-Z0-9_.-]+)/(?:Desktop|Downloads|Documents|Pictures|Videos|Android)")
CREDENTIAL_KEY_RE = re.compile(r"""\b(?:api[_-]?key|secret|password|passwd|auth[_-]?token|access[_-]?token)\s*[:=]\s*["']?([a-zA-Z0-9_\-\.]{12,})["']?""", re.IGNORECASE)
BEARER_RE = re.compile(r"\bBearer\s+([a-zA-Z0-9_\-\.]{20,})\b", re.IGNORECASE)

DUMMY_MACS = {
    "00:00:00:00:00:00",
    "02:00:00:00:00:00",
    "ff:ff:ff:ff:ff:ff",
    "FF:FF:FF:FF:FF:FF",
}

DUMMY_CREDENTIALS = {
    "sua_api_key",
    "your_api_key",
    "seu_token",
    "your_token",
    "seu_id",
    "your_id",
    "seu_perfil",
    "your_profile",
    "example_api_key",
    "redacted",
    "none",
    "dummy",
}

IGNORED_DIRS = {
    ".git",
    "__pycache__",
    ".cma-logs",
    "tests",
    ".venv",
    "node_modules",
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


def load_allowlist() -> tuple[set[tuple[str, str]], bool]:
    """Carrega tuplas (caminho_relativo, valor) permitidas da allowlist. Retorna (allowlist, ok)."""
    if not ALLOWLIST_PATH.is_file():
        return set(), True
    try:
        data = json.loads(ALLOWLIST_PATH.read_text(encoding="utf-8"))
        entries = data.get("allowlist", [])
        return {(e["path"], str(e["value"])) for e in entries if "path" in e and "value" in e}, True
    except Exception as exc:
        print(f"ERRO: Falha ao carregar allowlist: {exc}", file=sys.stderr)
        return set(), False


def check_image_metadata(path: Path) -> list[str]:
    """Inspeciona imagens procurando por metadados ancilares ou EXIF."""
    violations: list[str] = []
    try:
        rel_path = path.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = str(path)

    try:
        data = path.read_bytes()
    except Exception as exc:
        violations.append(f"{rel_path}: Falha segura ao ler imagem: {exc}")
        return violations

    suffix = path.suffix.lower()
    if suffix == ".png":
        # PNG: verificar chunks ancilares como eXIf, tEXt, zTXt, iTXt
        idx = 8
        while idx < len(data) - 8:
            try:
                length = int.from_bytes(data[idx:idx+4], "big")
                chunk_type = data[idx+4:idx+8].decode("latin1", errors="replace")
                if chunk_type in {"eXIf", "tEXt", "zTXt", "iTXt"}:
                    violations.append(f"{rel_path}: Metadados ancilares/EXIF detectados na imagem PNG ({chunk_type}) [REDACTED]")
                    break
                idx += 12 + length
            except Exception:
                break
    elif suffix in {".jpg", ".jpeg"}:
        # JPEG: verificar marcador APP1 com cabeçalho Exif (\xff\xe1 ... Exif\x00\x00)
        if b"\xff\xe1" in data and b"Exif\x00\x00" in data:
            violations.append(f"{rel_path}: Metadados EXIF detectados na imagem JPEG [REDACTED]")

    return violations


def check_file(path: Path, allowlist: set[tuple[str, str]]) -> list[str]:
    """Inspeciona um arquivo e retorna lista de violações encontradas sem vazar dados brutos."""
    violations: list[str] = []
    try:
        rel_path = path.relative_to(ROOT).as_posix()
    except ValueError:
        rel_path = str(path)

    # Ignorar a própria allowlist e este script verificador
    try:
        if path.resolve() in {ALLOWLIST_PATH.resolve(), Path(__file__).resolve()}:
            return violations
    except Exception:
        pass

    suffix = path.suffix.lower()

    # Se for imagem, inspecionar metadados
    if suffix in {".png", ".jpg", ".jpeg"}:
        if (rel_path, "*") in allowlist:
            return violations
        return check_image_metadata(path)

    # Ignorar outros binários não-texto
    if suffix in {".webp", ".zip", ".apk", ".apex", ".pyc"}:
        return violations

    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return violations
    except Exception as exc:
        violations.append(f"{rel_path}: Falha segura ao ler arquivo de texto: {exc}")
        return violations

    lines = content.splitlines()
    for lno, line in enumerate(lines, 1):
        # 1. MAC Address
        for mac in MAC_RE.findall(line):
            if mac in DUMMY_MACS:
                continue
            if (rel_path, mac) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Endereço MAC exposto [REDACTED]")

        # 2. IMEI com validação de Luhn
        for imei in IMEI_RE.findall(line):
            if is_luhn_valid(imei):
                if (rel_path, imei) in allowlist:
                    continue
                violations.append(f"{rel_path}:{lno}: IMEI válido detectado [REDACTED]")

        # 3. IPv4 Privado
        for ip in PRIVATE_IPV4_RE.findall(line):
            if (rel_path, ip) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Endereço IP privado IPv4 detectado [REDACTED]")

        # 4. IPv6 Privado (ULA fc00::/7 ou link-local fe80::/10)
        for cand in IPV6_CANDIDATE_RE.findall(line):
            try:
                parsed_ip = ipaddress.ip_address(cand)
                if parsed_ip.version == 6 and (parsed_ip.is_private or parsed_ip.is_link_local):
                    if (rel_path, cand) in allowlist:
                        continue
                    violations.append(f"{rel_path}:{lno}: Endereço IPv6 privado detectado [REDACTED]")
            except ValueError:
                continue

        # 5. Nome de Conta pessoal
        for acc in ACCOUNT_RE.findall(line):
            acc_clean = acc.strip()
            if (rel_path, acc_clean) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Identificador de conta pessoal exposto [REDACTED]")

        # 6. E-mails
        for email in EMAIL_RE.findall(line):
            # Excluir pacotes APEX e exemplos
            if email.endswith(".apex") or email.endswith(("@example.com", "@android.com", "@users.noreply.github.com")):
                continue
            # Excluir declarações de serviços Android HAL/HIDL (ex: wifi@2.0-service, drm@1.3-service.clearkey)
            domain_part = email.split("@", 1)[1] if "@" in email else ""
            if re.match(r"^[0-9]+\.[0-9]+-service", domain_part) or domain_part.endswith((".service", ".clearkey")):
                continue
            if (rel_path, email) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Endereço de e-mail pessoal detectado [REDACTED]")

        # 7. Número de Telefone Brasileiro (fixo ou móvel)
        for phone in PHONE_MOBILE_RE.findall(line):
            if (rel_path, phone) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Possível número de telefone celular exposto [REDACTED]")

        for phone in PHONE_LANDLINE_RE.findall(line):
            if (rel_path, phone) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Possível número de telefone fixo exposto [REDACTED]")

        # 8. Serial de Hardware
        for serial in SERIAL_PROP_RE.findall(line):
            if serial.lower() in {"unknown", "none", "redacted"}:
                continue
            if (rel_path, serial) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Número de série de hardware exposto [REDACTED]")

        # 9. Caminho de usuário local pessoal
        for user in HOME_USER_RE.findall(line):
            if user in {"runner", "ubuntu", "user"}:
                continue
            violations.append(f"{rel_path}:{lno}: Caminho com usuário local pessoal exposto [REDACTED]")

        # 10. Credenciais, senhas e tokens de acesso
        for key_val in CREDENTIAL_KEY_RE.findall(line):
            if key_val.lower() in DUMMY_CREDENTIALS:
                continue
            if (rel_path, key_val) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Credencial ou token em chave sensível exposto [REDACTED]")

        for token in BEARER_RE.findall(line):
            if token.lower() in DUMMY_CREDENTIALS:
                continue
            if (rel_path, token) in allowlist:
                continue
            violations.append(f"{rel_path}:{lno}: Token Bearer detectado [REDACTED]")

    return violations


def scan_target(target: Path, allowlist: set[tuple[str, str]]) -> list[str]:
    """Inspeciona um alvo que pode ser arquivo ou diretório."""
    violations: list[str] = []
    if not target.exists():
        return violations

    if target.is_file():
        return check_file(target, allowlist)

    for p in sorted(target.rglob("*")):
        if any(ignored in p.parts for ignored in IGNORED_DIRS):
            continue
        if p.is_file():
            violations.extend(check_file(p, allowlist))

    return violations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("paths", nargs="*", help="Diretórios ou arquivos a verificar (padrão: repositório completo)")
    args = parser.parse_args()

    allowlist, ok = load_allowlist()
    if not ok:
        print("FALHA: Não foi possível carregar a allowlist de sanitização de forma segura.", file=sys.stderr)
        return 1

    all_violations: list[str] = []
    if args.paths:
        for p in args.paths:
            target = (ROOT / p).resolve() if not Path(p).is_absolute() else Path(p)
            all_violations.extend(scan_target(target, allowlist))
    else:
        # Default: escanear repositório completo, excetuando diretórios ignorados
        for item in sorted(ROOT.iterdir()):
            if item.name in IGNORED_DIRS:
                continue
            all_violations.extend(scan_target(item, allowlist))

    if all_violations:
        print(f"FALHA: {len(all_violations)} problema(s) de sanitização encontrado(s):", file=sys.stderr)
        for v in all_violations:
            print(f" - {v}", file=sys.stderr)
        return 1

    print("OK: Verificação de sanitização concluída sem violações de privacidade.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
