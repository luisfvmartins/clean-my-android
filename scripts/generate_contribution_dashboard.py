#!/usr/bin/env python3
"""Gera painel de evolução das contribuições via API REST do GitHub."""
from __future__ import annotations
import json, os, sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "data/device_catalog.json"
OUTPUT = ROOT / "docs/EVOLUCAO_CONTRIBUICOES.md"
REPOSITORY = os.environ.get("GITHUB_REPOSITORY", "luisfvmartins/clean-my-android")
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")

def github_json(url: str):
    headers = {"Accept": "application/vnd.github+json", "X-GitHub-Api-Version": "2022-11-28", "User-Agent": "clean-my-android-contribution-dashboard"}
    if TOKEN:
        headers["Authorization"] = f"Bearer {TOKEN}"
    try:
        with urlopen(Request(url, headers=headers), timeout=30) as response:
            return json.loads(response.read().decode("utf-8")), response.headers.get("Link")
    except (HTTPError, URLError, TimeoutError) as exc:
        raise RuntimeError(f"Falha ao consultar API GitHub: {exc}") from exc

def merged_pull_requests() -> list[dict]:
    url = f"https://api.github.com/repos/{REPOSITORY}/pulls?state=closed&per_page=100&sort=updated&direction=desc"
    merged = []
    while url:
        payload, link_header = github_json(url)
        if not isinstance(payload, list):
            raise RuntimeError("Resposta inesperada da API de Pull Requests.")
        merged.extend(item for item in payload if item.get("merged_at"))
        url = None
        if link_header:
            for link in link_header.split(","):
                if 'rel="next"' in link:
                    url = link[link.find("<") + 1:link.find(">")]
                    break
    return merged

def generate(pulls: list[dict]) -> str:
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    devices = catalog.get("devices", [])
    years = Counter()
    authors = set()
    for pull in pulls:
        merged_at = datetime.fromisoformat(pull["merged_at"].replace("Z", "+00:00"))
        years[str(merged_at.year)] += 1
        author = (pull.get("user") or {}).get("login")
        if author:
            authors.add(author)
    updated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# Evolução das contribuições", "",
        "Painel calculado com dados da API REST do GitHub. A contagem considera Pull Requests "
        "fechadas com campo merged_at preenchido; PRs rejeitadas ou fechadas sem merge não entram.", "",
        f"**Atualizado em:** {updated}  ",
        f"**Repositório:** [{REPOSITORY}](https://github.com/{REPOSITORY})", "",
        "## Indicadores", "",
        f"- **Pull Requests incorporadas:** {len(pulls)}",
        f"- **Autores distintos com PR incorporada:** {len(authors)}",
        f"- **Dispositivos catalogados:** {len(devices)}",
        f"- **Fabricantes representados:** {len({d.get('manufacturer') for d in devices if d.get('manufacturer')})}", "",
        "## Pull Requests incorporadas por ano", "",
        "| Ano de incorporação | Pull Requests |", "|---:|---:|",
    ]
    for year in sorted(years):
        lines.append(f"| {year} | {years[year]} |")
    if not years:
        lines.append("| Ainda sem merges | 0 |")
    lines.extend([
        "", "## Escopo e limitações", "",
        "- Autores distintos são contados pelo login GitHub associado ao autor da PR incorporada. "
        "Isso não equivale a pessoas verificadas ou membros ativos atuais.",
        "- Uma PR representa uma contribuição integrada, mas pode conter vários arquivos ou dispositivos.",
        "- Dispositivos e fabricantes vêm de data/device_catalog.json; atividade de PR vem da API GitHub.",
        "- O painel não mede qualidade, linhas úteis, testes em aparelho ou homologação.",
        "- Os dados refletem o repositório no momento da atualização.", "",
        "## Atualização", "",
        "O workflow Atualizar painel de contribuições executa diariamente e também pode ser iniciado "
        "manualmente pela aba Actions. Usa GITHUB_TOKEN fornecido pelo GitHub Actions; nenhum token "
        "pessoal é armazenado no repositório.", "",
        "Consulte também as [estatísticas do projeto](ESTATISTICAS.md) e o [catálogo de auditorias](../reports/README.md).", ""
    ])
    return "\n".join(lines)

def main() -> int:
    try:
        content = generate(merged_pull_requests())
    except (OSError, UnicodeError, json.JSONDecodeError, RuntimeError) as exc:
        print(f"ERRO: {exc}", file=sys.stderr)
        return 1
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"OK: painel gerado em {OUTPUT.relative_to(ROOT)}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
