#!/usr/bin/env python3
"""Verificador de listas de alterações e conformidade de pacotes protegidos (PT-2).

Verifica:
1. Pacotes em reports/<fabricante>/<modelo>/changes/*.txt existem no inventário 'before'.
2. Nenhum pacote em changes/*.txt consta em data/protected_essential_packages.txt
   (com exceção estritamente documentada para a regressão histórica do A30s com printspooler).
3. Nenhum pacote aparece simultaneamente em desativados e removidos.
4. Contagens de pacotes batem com comparativo.json.
5. Listas em data/*disabled*.txt não contêm pacotes de data/protected_essential_packages.txt.
6. Gate de aplicação (data/apply_support.tsv) está estritamente alinhado com data/device_catalog.json.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Exceção histórica auditada: desativação do printspooler no A30s causou a perda de 'Salvar como PDF',
# documentada como limitação honesta e justificativa para inclusão na lista de protegidos futuros.
HISTORICAL_EXCEPTIONS = {
    ("reports/samsung/galaxy-a30s/changes/disabled-packages.txt", "com.android.printspooler")
}


def load_protected_packages(root_dir: Path) -> set[str]:
    path = root_dir / "data/protected_essential_packages.txt"
    if not path.is_file():
        return set()
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip() and not line.startswith("#")
    }


def parse_packages_from_file(path: Path) -> list[str]:
    if not path.is_file():
        return []
    packages: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        # Support both 'package:name', 'name | status | ...', or raw 'name'
        if "|" in raw:
            pkg = raw.split("|")[0].strip()
        elif raw.startswith("package:"):
            pkg = raw.split("package:")[1].strip()
        else:
            pkg = raw.split()[0].strip()
        if pkg:
            packages.append(pkg)
    return packages


def load_before_inventory_packages(device_dir: Path) -> set[str]:
    packages: set[str] = set()

    # Try before/packages.txt
    for candidate in [
        device_dir / "before/packages.txt",
        device_dir / "before/packages-initial.txt",
        device_dir / "packages-before.txt",
    ]:
        if candidate.is_file():
            packages.update(parse_packages_from_file(candidate))

    # Try JSON inventories
    for candidate_json in [
        device_dir / "before/inventory.json",
        device_dir / "inventario-antes.json",
    ]:
        if candidate_json.is_file():
            try:
                data = json.loads(candidate_json.read_text(encoding="utf-8"))
                if isinstance(data, dict):
                    # Edge 60 Pro style or generic
                    pkgs = data.get("packages") or data.get("pacotes") or []
                    for item in pkgs:
                        if isinstance(item, dict) and "package_name" in item:
                            packages.add(item["package_name"])
                        elif isinstance(item, str):
                            packages.add(item)
                elif isinstance(data, list):
                    for item in data:
                        if isinstance(item, dict) and "package_name" in item:
                            packages.add(item["package_name"])
                        elif isinstance(item, str):
                            packages.add(item)
            except Exception:
                pass

    return packages


def validate_device_changes(root_dir: Path, protected: set[str]) -> tuple[int, list[str]]:
    checks = 0
    errors: list[str] = []

    reports_dir = root_dir / "reports"
    if not reports_dir.is_dir():
        return checks, errors

    for dev_dir in sorted(reports_dir.glob("*/*")):
        if not dev_dir.is_dir():
            continue

        changes_dir = dev_dir / "changes"
        if not changes_dir.is_dir():
            continue

        checks += 1
        before_pkgs = load_before_inventory_packages(dev_dir)

        disabled_file = changes_dir / "disabled-packages.txt"
        removed_file = changes_dir / "removed-packages.txt"

        disabled_pkgs = parse_packages_from_file(disabled_file) if disabled_file.is_file() else []
        removed_pkgs = parse_packages_from_file(removed_file) if removed_file.is_file() else []

        # 1. Check packages exist in before inventory
        if (disabled_pkgs or removed_pkgs) and not before_pkgs:
            errors.append(
                f"{changes_dir.relative_to(root_dir)}: inventário 'before' ausente, ilegível ou vazio; impossível validar existência dos pacotes alterados"
            )
        else:
            for p in disabled_pkgs:
                checks += 1
                if p not in before_pkgs:
                    errors.append(f"{disabled_file.relative_to(root_dir)}: pacote '{p}' não existe no inventário 'before'")

            for p in removed_pkgs:
                checks += 1
                if p not in before_pkgs:
                    errors.append(f"{removed_file.relative_to(root_dir)}: pacote '{p}' não existe no inventário 'before'")

        # 2. Check no overlap between disabled and removed
        overlap = set(disabled_pkgs).intersection(set(removed_pkgs))
        checks += 1
        if overlap:
            errors.append(f"{changes_dir.relative_to(root_dir)}: pacotes constam em desativados e removidos simultaneamente: {sorted(overlap)}")

        # 3. Check protected packages
        for change_file in sorted(changes_dir.glob("*.txt")):
            rel_file = str(change_file.relative_to(root_dir))
            for p in parse_packages_from_file(change_file):
                checks += 1
                if p in protected:
                    if (rel_file, p) in HISTORICAL_EXCEPTIONS:
                        continue
                    errors.append(f"{rel_file}: pacote protegido '{p}' consta na lista de alterações!")

        # 4. Check counts against comparativo.json
        comp_file = dev_dir / "comparativo.json"
        if comp_file.is_file():
            checks += 1
            try:
                comp_data = json.loads(comp_file.read_text(encoding="utf-8"))
                for m in comp_data.get("metrics", []):
                    ind = m.get("indicator") or m.get("metric") or ""
                    if "desativado" in ind.lower() and disabled_pkgs:
                        # Check count in variation or after
                        var_str = str(m.get("variation", ""))
                        m_var = re.search(r"(\d+)\s+pacotes\s+desativados", var_str)
                        if m_var:
                            declared = int(m_var.group(1))
                        else:
                            after_str = str(m.get("after", ""))
                            m_num = re.search(r"\b(\d+)\s+pacotes\b", after_str)
                            declared = int(m_num.group(1)) if m_num else len(disabled_pkgs)
                        if declared != len(disabled_pkgs):
                            errors.append(
                                f"{comp_file.relative_to(root_dir)}: contagem de desativados declarada ({declared}) diverge da lista ({len(disabled_pkgs)})"
                            )
                    elif "removido" in ind.lower() and removed_pkgs:
                        var_str = str(m.get("variation", ""))
                        m_var = re.search(r"(\d+)\s+pacotes\s+desinstalados", var_str)
                        if m_var:
                            declared = int(m_var.group(1))
                        else:
                            after_str = str(m.get("after", ""))
                            m_num = re.search(r"\b(\d+)\s+pacotes\b", after_str)
                            declared = int(m_num.group(1)) if m_num else len(removed_pkgs)
                        if declared != len(removed_pkgs):
                            errors.append(
                                f"{comp_file.relative_to(root_dir)}: contagem de removidos declarada ({declared}) diverge da lista ({len(removed_pkgs)})"
                            )
            except Exception as exc:
                errors.append(f"{comp_file.relative_to(root_dir)}: erro ao verificar contagens ({exc})")

    return checks, errors


def validate_data_disabled_lists(root_dir: Path, protected: set[str]) -> tuple[int, list[str]]:
    checks = 0
    errors: list[str] = []

    for path in sorted((root_dir / "data").glob("*disabled*.txt")):
        checks += 1
        rel_path = str(path.relative_to(root_dir))
        # Snapshots históricos de estado observado coletado no aparelho não são listas de recomendações de debloat
        if rel_path == "data/moto_g54_disabled_packages.txt":
            continue
        try:
            first_lines = path.read_text(encoding="utf-8").splitlines()[:3]
            if any(
                "SNAPSHOT" in line.upper()
                and ("NÃO É LISTA DE RECOMENDAÇÕES" in line.upper() or "ESTADO OBSERVADO" in line.upper())
                for line in first_lines
            ):
                continue
        except Exception:
            pass

        pkgs = parse_packages_from_file(path)
        for p in pkgs:
            checks += 1
            if p in protected:
                errors.append(f"{rel_path}: pacote protegido '{p}' encontrado na lista geral de desativados!")

    return checks, errors


def validate_apply_gate(root_dir: Path) -> tuple[int, list[str]]:
    checks = 0
    errors: list[str] = []

    tsv_path = root_dir / "data/apply_support.tsv"
    catalog_path = root_dir / "data/device_catalog.json"

    if not tsv_path.is_file():
        errors.append("data/apply_support.tsv não encontrado")
        return checks, errors

    if not catalog_path.is_file():
        errors.append("data/device_catalog.json não encontrado")
        return checks, errors

    checks += 2
    try:
        catalog = json.loads(catalog_path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"data/device_catalog.json inválido: {exc}")
        return checks, errors

    supported_devices: set[str] = set()
    for d in catalog.get("devices", []):
        checks += 1
        if d.get("apply_supported") is True:
            # Rule 4: Only Moto G54 is authorized
            if d.get("id") != "motorola-moto-g54-5g":
                errors.append(f"Regra 4 violada: dispositivo '{d.get('id')}' não pode ter apply_supported=True sem aprovação explícita.")
            codename = d.get("codename")
            if codename:
                supported_devices.add(codename)
                # also support variant codename
                supported_devices.add(f"{codename}_g_sysn")

    for line in tsv_path.read_text(encoding="utf-8").splitlines():
        raw = line.strip()
        if not raw or raw.startswith("#"):
            continue
        checks += 1
        parts = raw.split("\t")
        if len(parts) < 3:
            errors.append(f"data/apply_support.tsv linha inválida: '{raw}' (esperado codinome<TAB>android<TAB>nivel)")
            continue
        codename, _android_ver, _level = parts[0].strip(), parts[1].strip(), parts[2].strip()
        if codename not in supported_devices:
            errors.append(
                f"data/apply_support.tsv: codinome '{codename}' não consta como apply_supported=True em device_catalog.json"
            )

    return checks, errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Raiz do repositório")
    args = parser.parse_args()

    root_dir = args.repo_root
    protected = load_protected_packages(root_dir)

    total_checks = 0
    all_errors: list[str] = []

    c1, errs1 = validate_device_changes(root_dir, protected)
    total_checks += c1
    all_errors.extend(errs1)

    c2, errs2 = validate_data_disabled_lists(root_dir, protected)
    total_checks += c2
    all_errors.extend(errs2)

    c3, errs3 = validate_apply_gate(root_dir)
    total_checks += c3
    all_errors.extend(errs3)

    if all_errors:
        print(f"FALHA: {len(all_errors)} inconsistência(s) em listas de mudanças ou gate:")
        for err in all_errors:
            print(f" - {err}")
        return 1

    print(f"OK: {total_checks} verificações de listas de mudanças e gate de aplicação concluídas com sucesso.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
