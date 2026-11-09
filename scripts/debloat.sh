#!/usr/bin/env bash
# Clean My Android — inspeção e desativação individual, com confirmação.
# Compatível com Bash 3.2+ (macOS / Linux) e estritamente auditado.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_MESSAGES="$SCRIPT_DIR/lib/messages.sh"
PROTECTED_LIST="$SCRIPT_DIR/../data/protected_essential_packages.txt"
APPLY_SUPPORT_FILE="$SCRIPT_DIR/../data/apply_support.tsv"

if [[ -f "$LIB_MESSAGES" ]]; then
  # shellcheck source=scripts/lib/messages.sh
  source "$LIB_MESSAGES"
else
  cma_msg() { printf "%s\n" "$1"; }
  get_cma_lang() { echo "en"; }
fi

usage() {
  local lang
  lang="$(get_cma_lang)"
  if [[ "$lang" == "pt" ]]; then
    cat <<'EOF'
Uso:
  ./debloat.sh [--log-dir DIR]                 # somente leitura: identifica o aparelho e lista pacotes desativados
  ./debloat.sh [--log-dir DIR] --apply PACOTE  # desativa um único pacote após confirmação

Opções:
  --log-dir DIR   Diretório de logs JSONL (padrão: ./.cma-logs/)
  --help, -h      Exibe esta mensagem de ajuda

Códigos de saída (Exit Codes):
  0: Sucesso, somente leitura, ajuda exibida, cancelado pelo usuário ou pacote já desativado
  1: ADB ausente ou número incorreto de dispositivos conectados (exatamente 1 exigido)
  2: Argumentos inválidos ou sintaxe de nome de pacote inválida
  3: Aparelho ou versão do Android não suportados pelo gate de aplicação (data/apply_support.tsv)
  4: Arquivo de configuração ausente (data/apply_support.tsv ou data/protected_essential_packages.txt)
  5: Pacote bloqueado por pertencer à lista de componentes protegidos
  6: Pacote não encontrado no dispositivo
  7: Falha na confirmação do estado final do pacote

A aplicação de mudanças está limitada ao Moto G54 5G (Android 15).
O script nunca limpa dados, desinstala pacotes, altera AppOps ou remove perfis.
EOF
  else
    cat <<'EOF'
Usage:
  ./debloat.sh [--log-dir DIR]                 # read-only: identify device and list disabled packages
  ./debloat.sh [--log-dir DIR] --apply PACKAGE # disable a single package after explicit confirmation

Options:
  --log-dir DIR   JSONL log directory (default: ./.cma-logs/)
  --help, -h      Show this help message

Exit Codes:
  0: Success, read-only mode, help displayed, cancelled by user, or package already disabled
  1: ADB missing or incorrect number of connected devices (exactly 1 required)
  2: Invalid arguments or invalid package name syntax
  3: Device or Android version not supported by apply gate (data/apply_support.tsv)
  4: Missing configuration file (data/apply_support.tsv or data/protected_essential_packages.txt)
  5: Package blocked: listed in protected essential components list
  6: Package not found on device
  7: Verification failure: package final disabled state could not be confirmed

Applying changes is strictly limited to Moto G54 5G (Android 15).
This script never clears data, uninstalls packages, alters AppOps, or removes user profiles.
EOF
  fi
}

LOG_DIR="./.cma-logs"
APPLY_MODE=0
PACKAGE=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --log-dir)
      if [[ $# -lt 2 ]]; then
        cma_msg err_invalid_args >&2
        usage >&2
        exit 2
      fi
      LOG_DIR="$2"
      shift 2
      ;;
    --apply)
      APPLY_MODE=1
      if [[ $# -lt 2 ]]; then
        cma_msg err_invalid_args >&2
        usage >&2
        exit 2
      fi
      PACKAGE="$2"
      shift 2
      ;;
    *)
      cma_msg err_invalid_args >&2
      usage >&2
      exit 2
      ;;
  esac
done

if ! command -v adb >/dev/null 2>&1; then
  cma_msg err_no_adb >&2
  exit 1
fi

DEVICES=()
while IFS= read -r dev; do
  [[ -n "$dev" ]] && DEVICES+=("$dev")
done < <(adb devices | awk 'NR > 1 && $2 == "device" {print $1}')

if [[ ${#DEVICES[@]} -ne 1 ]]; then
  cma_msg err_device_count "${#DEVICES[@]}" >&2
  adb devices -l
  exit 1
fi

ADB=(adb -s "${DEVICES[0]}")
MODEL="$("${ADB[@]}" shell getprop ro.product.model | tr -d '\r')"
DEVICE="$("${ADB[@]}" shell getprop ro.product.device | tr -d '\r')"
PRODUCT="$("${ADB[@]}" shell getprop ro.build.product | tr -d '\r')"
ANDROID_VER="$("${ADB[@]}" shell getprop ro.build.version.release | tr -d '\r')"

cma_msg device_info "$MODEL" "$DEVICE" "$PRODUCT" "$ANDROID_VER"
echo

if [[ $APPLY_MODE -eq 0 ]]; then
  cma_msg read_only_mode
  cma_msg disabled_packages_header
  "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | sort
  echo
  usage
  exit 0
fi

if [[ ! "$PACKAGE" =~ ^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$ ]]; then
  cma_msg err_invalid_package "$PACKAGE" >&2
  exit 2
fi

if [[ ! -f "$APPLY_SUPPORT_FILE" ]]; then
  cma_msg err_missing_support "$APPLY_SUPPORT_FILE" >&2
  exit 4
fi

DEVICE_CATALOG_FILE="${CMA_DEVICE_CATALOG_FILE:-$SCRIPT_DIR/../data/device_catalog.json}"

DEV_LEVEL=0
if [[ -f "$DEVICE_CATALOG_FILE" ]]; then
  if command -v python3 >/dev/null 2>&1; then
    DEV_LEVEL=$(python3 -c '
import json, sys
try:
    with open(sys.argv[1], encoding="utf-8") as f:
        data = json.load(f)
    dev = sys.argv[2]
    prod = sys.argv[3]
    for d in data.get("devices", []):
        if d.get("codename") in (dev, prod) or d.get("model_code") in (dev, prod):
            print(d.get("homologation_level", 0))
            sys.exit(0)
except Exception:
    pass
print(0)
' "$DEVICE_CATALOG_FILE" "$DEVICE" "$PRODUCT" 2>/dev/null || echo 0)
  fi
fi

GATE_MATCH=0
while IFS=$'\t' read -r tsv_coden tsv_and tsv_lvl || [[ -n "$tsv_coden" ]]; do
  # Ignore empty lines and comments
  [[ -z "$tsv_coden" || "$tsv_coden" =~ ^# ]] && continue
  if [[ ("$DEVICE" == "$tsv_coden" || "$PRODUCT" == "$tsv_coden") && "$ANDROID_VER" == "$tsv_and" ]]; then
    tsv_lvl_clean="${tsv_lvl:-1}"
    if [[ "$DEV_LEVEL" -ge "$tsv_lvl_clean" ]]; then
      GATE_MATCH=1
      break
    fi
  fi
done < "$APPLY_SUPPORT_FILE"

if [[ $GATE_MATCH -ne 1 ]]; then
  cma_msg err_device_gate "$DEVICE" "$ANDROID_VER" >&2
  exit 3
fi

if [[ ! -f "$PROTECTED_LIST" ]]; then
  cma_msg err_missing_protection "$PROTECTED_LIST" >&2
  exit 4
fi

if grep -Fxq "$PACKAGE" "$PROTECTED_LIST"; then
  cma_msg err_protected_package "$PACKAGE" >&2
  exit 5
fi

if ! "${ADB[@]}" shell pm path "$PACKAGE" 2>/dev/null | tr -d '\r' | grep -q '^package:'; then
  cma_msg err_package_not_found "$PACKAGE" >&2
  exit 6
fi

if "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  cma_msg info_already_disabled "$PACKAGE"
  exit 0
fi

cma_msg prompt_debloat_warning "$PACKAGE"
cma_msg prompt_debloat_confirm "$PACKAGE"
read -r CONFIRM

EXPECTED_CONFIRM="DESATIVAR $PACKAGE"
EXPECTED_CONFIRM_EN="DISABLE $PACKAGE"
if [[ "$CONFIRM" != "$EXPECTED_CONFIRM" && "$CONFIRM" != "$EXPECTED_CONFIRM_EN" ]]; then
  cma_msg action_cancelled
  exit 0
fi

# Pré-validação do armazenamento e permissões de log antes de alterar o dispositivo
if ! mkdir -p "$LOG_DIR" 2>/dev/null; then
  echo "Erro: falha ao criar ou acessar diretório de log: $LOG_DIR" >&2
  exit 4
fi
if ! touch "$LOG_DIR/actions.jsonl" 2>/dev/null; then
  echo "Erro: sem permissão de escrita no arquivo de log: $LOG_DIR/actions.jsonl" >&2
  exit 4
fi

CMD_OUT="$("${ADB[@]}" shell pm disable-user --user 0 "$PACKAGE" 2>&1 | tr -d '\r')"
if "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  cma_msg debloat_success "$PACKAGE"

  # JSONL Logging
  mkdir -p "$LOG_DIR"
  TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  # Sanitized JSON logging without hardware identifiers
  cat >> "$LOG_DIR/actions.jsonl" <<EOF
{"timestamp_utc":"$TIMESTAMP","action":"disable","model":"$MODEL","codename":"$DEVICE","android_version":"$ANDROID_VER","package":"$PACKAGE","command":"pm disable-user --user 0 $PACKAGE","output":"$CMD_OUT","verified_state":"disabled","rollback_command":"pm enable --user 0 $PACKAGE"}
EOF
else
  cma_msg err_debloat_failed "$PACKAGE" >&2
  exit 7
fi
