#!/usr/bin/env bash
# ==============================================================================
# Clean My Android - Script de Restauração (Rollback)
# Autor: Luís Martins (@luisfvmartins)
# Repositório: https://github.com/luisfvmartins/clean-my-android
# ==============================================================================

set -e

if [ -z "$1" ]; then
    echo "Uso:"
    echo "  ./restore.sh <nome.do.pacote>        # Reativa ou reinstala um pacote específico"
    echo "  ./restore.sh --all                  # Reativa todos os pacotes da lista e restaura daemons persistentes"
    echo ""
    echo "Exemplo: ./restore.sh com.motorola.mobiledesktop"
    exit 1
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_LIST="$SCRIPT_DIR/../data/disabled_packages.txt"
PERSISTENT_LIST="$SCRIPT_DIR/../data/persistent_uninstall_packages.txt"

if [ "$1" == "--all" ]; then
    if [ ! -f "$PKG_LIST" ]; then
        echo "[-] Arquivo $PKG_LIST não encontrado!"
        exit 1
    fi
    echo "[!] Reativando todos os pacotes de disabled_packages.txt..."
    while IFS= read -r pkg || [ -n "$pkg" ]; do
        [ -z "$pkg" ] && continue
        [[ "$pkg" =~ ^#.* ]] && continue
        echo "Reativando: $pkg"
        adb shell pm enable "$pkg" 2>/dev/null || true
    done < "$PKG_LIST"

    if [ -f "$PERSISTENT_LIST" ]; then
        echo "[!] Reinstalando daemons persistentes para user 0..."
        while IFS= read -r pkg || [ -n "$pkg" ]; do
            [ -z "$pkg" ] && continue
            [[ "$pkg" =~ ^#.* ]] && continue
            echo "Reinstalando: $pkg"
            adb shell cmd package install-existing --user 0 "$pkg" 2>/dev/null || true
            adb shell pm enable "$pkg" 2>/dev/null || true
        done < "$PERSISTENT_LIST"
    fi
    echo "[+] Todos os pacotes foram restaurados."
else
    echo "Restaurando pacote: $1"
    adb shell cmd package install-existing --user 0 "$1" 2>/dev/null || true
    adb shell pm enable "$1"
    echo "[+] Pacote $1 restaurado com sucesso."
fi
