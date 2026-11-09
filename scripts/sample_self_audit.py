#!/usr/bin/env python3
"""Script de amostragem reproduzível para autoauditoria de classificações (PT-6).

Usa a semente fixa 20261109 para selecionar 30 pacotes aleatórios entre os
componentes catalogados nos relatórios do repositório.
"""

from __future__ import annotations

import argparse
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SEED = 20261109
SAMPLE_SIZE = 30


def collect_catalog_packages(root_dir: Path) -> list[tuple[str, str, str]]:
    items: list[tuple[str, str, str]] = []

    # Moto G54 batches
    for p in sorted((root_dir / "docs/auditorias/moto-g54").glob("lote-*.md")):
        if p.name.endswith(".en.md"):
            continue
        rel = str(p.relative_to(root_dir))
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.startswith("### `") and line.endswith("`"):
                pkg = line.strip("# `")
                items.append(("Motorola Moto G54 5G", rel, pkg))

    # Galaxy A30s
    a30s_file = root_dir / "reports/samsung/galaxy-a30s/changes/disabled-packages.txt"
    if a30s_file.is_file():
        rel = str(a30s_file.relative_to(root_dir))
        for line in a30s_file.read_text(encoding="utf-8").splitlines():
            pkg = line.split("#")[0].strip()
            if pkg:
                items.append(("Samsung Galaxy A30s", rel, pkg))

    # Edge 60 Fusion
    fusion_file = root_dir / "reports/motorola/edge-60-fusion/changes/disabled-packages.txt"
    if fusion_file.is_file():
        rel = str(fusion_file.relative_to(root_dir))
        for line in fusion_file.read_text(encoding="utf-8").splitlines():
            pkg = line.split("#")[0].strip()
            if pkg:
                items.append(("Motorola Edge 60 Fusion", rel, pkg))

    # Edge 60 Pro
    pro_file = root_dir / "reports/motorola/edge-60-pro/changes/disabled-packages.txt"
    if pro_file.is_file():
        rel = str(pro_file.relative_to(root_dir))
        for line in pro_file.read_text(encoding="utf-8").splitlines():
            pkg = line.split("#")[0].strip()
            if pkg:
                items.append(("Motorola Edge 60 Pro", rel, pkg))

    return sorted(list(set(items)))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED, help="Semente pseudoaleatória (padrão: 20261109)")
    parser.add_argument("--size", type=int, default=SAMPLE_SIZE, help="Tamanho da amostra (padrão: 30)")
    parser.add_argument("--repo-root", type=Path, default=ROOT, help="Raiz do repositório")
    args = parser.parse_args()

    items = collect_catalog_packages(args.repo_root)
    rng = random.Random(args.seed)
    sample = rng.sample(items, min(args.size, len(items)))

    print(f"Universo amostral: {len(items)} componentes únicos")
    print(f"Semente utilizada: {args.seed}")
    print(f"Amostra selecionada ({len(sample)} pacotes):")
    for idx, (dev, src, pkg) in enumerate(sample, 1):
        print(f" {idx:02d}. [{dev}] {pkg} (fonte: {src})")

    return 0


if __name__ == "__main__":
    main()
