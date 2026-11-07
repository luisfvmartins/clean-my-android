#!/usr/bin/env bash
# ==============================================================================
# Script de Restauração para Motorola Edge Debloat
# ==============================================================================

set -e

if [ -z "$1" ]; then
    echo "Uso:"
    echo "  ./restore.sh <nome.do.pacote>        # Reativa um pacote específico"
    echo "  ./restore.sh --all                  # Reativa todos os pacotes da lista"
    echo ""
    echo "Exemplo: ./restore.sh com.motorola.mobiledesktop"
    exit 1
fi

if [ "$1" == "--all" ]; then
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    PKG_LIST="$SCRIPT_DIR/../data/disabled_packages.txt"
    if [ ! -f "$PKG_LIST" ]; then
        echo "[-] Arquivo $PKG_LIST não encontrado!"
        exit 1
    fi
    echo "[!] Reativando todos os pacotes..."
    while IFS= read -r pkg || [ -n "$pkg" ]; do
        [ -z "$pkg" ] && continue
        echo "Reativando: $pkg"
        adb shell pm enable "$pkg" 2>/dev/null || true
    done < "$PKG_LIST"
    echo "[+] Todos os pacotes foram reativados."
else
    echo "Reativando pacote: $1"
    adb shell pm enable "$1"
    echo "[+] Pacote $1 reativado com sucesso."
fi
