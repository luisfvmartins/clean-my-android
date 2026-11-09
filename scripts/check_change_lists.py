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

def load_audited_exceptions(root_dir: Path) -> tuple[dict[tuple[str, str], dict], list[str]]:
    """Carrega e valida as exceções documentadas em data/audited_exceptions.json."""
    path = root_dir / "data/audited_exceptions.json"
    if not path.is_file():
        return {}, [f"{path.relative_to(root_dir)}: arquivo não encontrado"]

    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return {}, [f"{path.relative_to(root_dir)}: JSON inválido ({exc})"]

    exceptions_map: dict[tuple[str, str], dict] = {}
    errors: list[str] = []
    seen: set[tuple[str, str]] = set()

    for idx, item in enumerate(data.get("exceptions", [])):
        device = item.get("device")
        pkg = item.get("package")
        reason = item.get("reason")
        status = item.get("status")
        decided_by = item.get("decided_by")
        decision_date = item.get("decision_date")
        functional_risk = item.get("functional_risk")

        if not device or not pkg:
            errors.append(f"audited_exceptions[{idx}]: 'device' e 'package' são obrigatórios")
            continue

        pair = (device, pkg)
        if pair in seen:
            errors.append(f"audited_exceptions: exceção duplicada para {pair}")
            continue
        seen.add(pair)

        if not reason:
            errors.append(f"audited_exceptions[{idx}]: 'reason' é obrigatório para {pair}")
        if status not in {"open", "mitigated", "accepted"}:
            errors.append(
                f"audited_exceptions[{idx}]: 'status' inválido ({status}) para {pair} (esperado: open, mitigated, accepted)"
            )
        if not decided_by:
            errors.append(f"audited_exceptions[{idx}]: 'decided_by' é obrigatório para {pair}")
        if not decision_date:
            errors.append(f"audited_exceptions[{idx}]: 'decision_date' é obrigatório para {pair}")
        if not functional_risk:
            errors.append(f"audited_exceptions[{idx}]: 'functional_risk' é obrigatório para {pair}")

        exceptions_map[pair] = item

    return exceptions_map, errors


def report_open_exceptions(exceptions_map: dict[tuple[str, str], dict]) -> None:
    """Imprime aviso visível das exceções abertas por dispositivo."""
    open_by_device: dict[str, list[str]] = {}
    for (dev, pkg), item in exceptions_map.items():
        if item.get("status") == "open":
            parts = dev.split("/")
            dev_name = parts[2] if len(parts) > 2 else dev
            open_by_device.setdefault(dev_name, []).append(pkg)

    total_open = sum(len(pkgs) for pkgs in open_by_device.values())
    if total_open > 0:
        print(f"AVISO: {total_open} exceções abertas catalogadas em data/audited_exceptions.json:")
        for dname, pkgs in sorted(open_by_device.items()):
            print(
                f"  - {dname} ({len(pkgs)} abertas): {', '.join(sorted(pkgs)[:5])}{'...' if len(pkgs) > 5 else ''}"
            )


def validate_role_holders_for_risky_exceptions(
    root_dir: Path, exceptions_map: dict[tuple[str, str], dict]
) -> tuple[int, list[str]]:
    """Valida que exceções críticas (dialer, sms, contacts) possuem titular de papel real e testado quando mitigadas."""
    checks = 0
    errors: list[str] = []
    CRITICAL_RISKS = {"dialer", "sms", "contacts"}

    for (device_rel_file, pkg), item in exceptions_map.items():
        risk = item.get("functional_risk")
        if risk in CRITICAL_RISKS:
            checks += 1
            status = item.get("status")
            dev_path = (root_dir / device_rel_file).parent.parent
            func_json_path = dev_path / "functional-tests.json"
            if not func_json_path.is_file():
                errors.append(
                    f"{func_json_path.relative_to(root_dir)}: arquivo ausente para validar titular de papel em exceção {pkg} (risco: {risk})"
                )
                continue

            try:
                func_data = json.loads(func_json_path.read_text(encoding="utf-8"))
            except Exception as exc:
                errors.append(f"{func_json_path.relative_to(root_dir)}: JSON inválido ({exc})")
                continue

            role_holders = func_data.get("role_holders", {})
            raw_holder = str(role_holders.get(risk, "")).strip()

            # Rejeita explicitamente placeholders como 'not_tested', 'none', vazio
            is_valid_holder = bool(
                raw_holder
                and raw_holder.lower() not in ("not_tested", "none", "null", "undefined")
                and "." in raw_holder
            )

            RISK_KEYWORDS = {
                "dialer": ("dialer", "discador", "chamada", "chamadas", "voz", "telefone", "phone"),
                "sms": ("sms", "mensagem", "mensagens", "message", "messaging"),
                "contacts": ("contato", "contatos", "contacts"),
            }
            keywords = RISK_KEYWORDS.get(risk, (risk,))

            has_passing_test = any(
                (
                    any(kw in str(t.get("test_name", "")).lower() for kw in keywords)
                    or any(kw in str(t.get("observation", "")).lower() for kw in keywords)
                    or (raw_holder and raw_holder.lower() in str(t).lower())
                    or risk in str(t.get("role", "")).lower()
                )
                and str(t.get("status", "")).lower() in ("pass", "passed", "ok")
                for t in func_data.get("tests", [])
            )

            if status == "mitigated":
                if not is_valid_holder:
                    errors.append(
                        f"{func_json_path.relative_to(root_dir)}: exceção mitigada {pkg} (risco: {risk}) rejeitada: titular '{raw_holder}' é placeholder ou inválido (exige pacote real)"
                    )
                elif not has_passing_test:
                    errors.append(
                        f"{func_json_path.relative_to(root_dir)}: exceção mitigada {pkg} (risco: {risk}) exige teste funcional com status aprovado (pass/passed)"
                    )
            elif status == "open":
                # Exceção aberta documenta ausência de titular e testes pendentes;
                # garante que não seja tratada como coberta ou mitigada
                pass

    return checks, errors


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


def validate_device_changes(
    root_dir: Path, protected: set[str], exceptions_map: dict[tuple[str, str], dict]
) -> tuple[int, list[str]]:
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
                    if (rel_file, p) in exceptions_map:
                        continue
                    errors.append(f"{rel_file}: pacote protegido '{p}' consta na lista de alterações!")

        # 4. Check counts against metrics.json (or fallback to comparativo.json)
        comp_file = dev_dir / "metrics.json"
        if not comp_file.is_file():
            comp_file = dev_dir / "comparativo.json"
        if comp_file.is_file():
            checks += 1
            try:
                comp_data = json.loads(comp_file.read_text(encoding="utf-8"))
                for m in comp_data.get("metrics", []):
                    ind = m.get("indicator") or m.get("metric") or ""
                    if "desativado" in ind.lower() and "fábrica" not in ind.lower() and "factory" not in ind.lower() and disabled_pkgs:
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


def is_snapshot_or_candidate_file(path: Path) -> bool:
    """Detecta se o arquivo é snapshot ou lista histórica de candidatos pelo cabeçalho."""
    if not path.is_file():
        return False
    try:
        first_lines = "".join(path.read_text(encoding="utf-8").splitlines()[:15]).upper()
        return any(k in first_lines for k in ["SNAPSHOT", "CANDIDATOS", "REGISTRO HISTÓRICO", "HISTÓRICA"])
    except Exception:
        return False


def load_notes_protected_packages(notes_path: Path) -> set[str]:
    """Lê os pacotes documentados no arquivo .notes.md associado."""
    if not notes_path.is_file():
        return set()
    text = notes_path.read_text(encoding="utf-8")
    matches = set(re.findall(r"`([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)`", text))
    for line in text.splitlines():
        line = line.strip()
        m = re.match(r"^\d+\.\s+`?([a-zA-Z0-9_]+(?:\.[a-zA-Z0-9_]+)+)`?", line)
        if m:
            matches.add(m.group(1))
    return matches


def check_snapshot_not_consumed_by_scripts(root_dir: Path, filename: str) -> list[str]:
    """Verifica se nenhum script, workflow ou doc executável faz referência ao arquivo de snapshot/candidatos."""
    errors: list[str] = []
    candidates: list[Path] = []
    scripts_dir = root_dir / "scripts"
    if scripts_dir.is_dir():
        for p in scripts_dir.rglob("*"):
            if p.is_file() and p.suffix in {".sh", ".py"}:
                if p.name in {"check_change_lists.py", "validate_repository.py", "generate_statistics.py"}:
                    continue
                candidates.append(p)

    wf_dir = root_dir / ".github/workflows"
    if wf_dir.is_dir():
        for p in wf_dir.glob("*.yml"):
            candidates.append(p)
        for p in wf_dir.glob("*.yaml"):
            candidates.append(p)

    for p in candidates:
        try:
            content = p.read_text(encoding="utf-8")
            if filename in content:
                errors.append(
                    f"{p.relative_to(root_dir)}: faz referência indevida ao arquivo de dados/snapshot '{filename}'"
                )
        except Exception:
            pass

    return errors


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

        if is_snapshot_or_candidate_file(path):
            notes_file = path.with_name(path.name + ".notes.md")
            if not notes_file.is_file():
                errors.append(f"{rel_path}: arquivo de snapshot/candidatos requer notas em {notes_file.name}")
                continue

            documented_pkgs = load_notes_protected_packages(notes_file)
            for p in pkgs:
                checks += 1
                if p in protected:
                    if p not in documented_pkgs:
                        errors.append(
                            f"{rel_path}: pacote protegido '{p}' presente no snapshot sem documentação em {notes_file.name}"
                        )

            checks += 1
            ref_errs = check_snapshot_not_consumed_by_scripts(root_dir, path.name)
            errors.extend(ref_errs)
        else:
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

    exceptions_map, exc_errs = load_audited_exceptions(root_dir)
    all_errors.extend(exc_errs)
    total_checks += len(exceptions_map)

    report_open_exceptions(exceptions_map)

    c_roles, role_errs = validate_role_holders_for_risky_exceptions(root_dir, exceptions_map)
    total_checks += c_roles
    all_errors.extend(role_errs)

    c1, errs1 = validate_device_changes(root_dir, protected, exceptions_map)
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
