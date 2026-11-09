#!/usr/bin/env bash
# Clean My Android — reativação individual, com confirmação.
# Compatível com Bash 3.2+ (macOS / Linux) e estritamente auditado.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_MESSAGES="$SCRIPT_DIR/lib/messages.sh"

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
  ./restore.sh [--log-dir DIR] PACOTE

Opções:
  --log-dir DIR   Diretório de logs JSONL (padrão: ./.cma-logs/)
  --help, -h      Exibe esta mensagem de ajuda

Códigos de saída (Exit Codes):
  0: Sucesso, ajuda exibida, cancelado pelo usuário ou pacote já habilitado
  1: ADB ausente ou número incorreto de dispositivos conectados (exatamente 1 exigido)
  2: Argumentos inválidos ou sintaxe de nome de pacote inválida
  3: Pacote não encontrado no dispositivo
  4: Falha na confirmação da reativação do pacote

Reativa somente um pacote por execução. Não há restauração em massa.
EOF
  else
    cat <<'EOF'
Usage:
  ./restore.sh [--log-dir DIR] PACKAGE

Options:
  --log-dir DIR   JSONL log directory (default: ./.cma-logs/)
  --help, -h      Show this help message

Exit Codes:
  0: Success, help displayed, cancelled by user, or package already enabled
  1: ADB missing or incorrect number of connected devices (exactly 1 required)
  2: Invalid arguments or invalid package name syntax
  3: Package not found on device
  4: Verification failure: package reactivation could not be confirmed

Re-enables only one package per execution. There is no bulk restoration.
EOF
  fi
}

LOG_DIR="./.cma-logs"
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
    -*)
      cma_msg err_invalid_args >&2
      usage >&2
      exit 2
      ;;
    *)
      if [[ -n "$PACKAGE" ]]; then
        cma_msg err_invalid_args >&2
        usage >&2
        exit 2
      fi
      PACKAGE="$1"
      shift
      ;;
  esac
done

if [[ -z "$PACKAGE" ]]; then
  cma_msg err_invalid_args >&2
  usage >&2
  exit 2
fi

if [[ ! "$PACKAGE" =~ ^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$ ]]; then
  cma_msg err_invalid_package "$PACKAGE" >&2
  exit 2
fi

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
ANDROID_VER="$("${ADB[@]}" shell getprop ro.build.version.release | tr -d '\r')"

if ! "${ADB[@]}" shell pm path "$PACKAGE" 2>/dev/null | tr -d '\r' | grep -q '^package:'; then
  cma_msg err_package_not_found "$PACKAGE" >&2
  exit 3
fi

if ! "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  cma_msg info_not_disabled "$PACKAGE"
  exit 0
fi

cma_msg prompt_restore_warning "$PACKAGE"
cma_msg prompt_restore_confirm "$PACKAGE"
read -r CONFIRM

EXPECTED_CONFIRM="REATIVAR $PACKAGE"
EXPECTED_CONFIRM_EN="REENABLE $PACKAGE"
if [[ "$CONFIRM" != "$EXPECTED_CONFIRM" && "$CONFIRM" != "$EXPECTED_CONFIRM_EN" ]]; then
  cma_msg action_cancelled
  exit 0
fi

CMD_OUT="$("${ADB[@]}" shell pm enable --user 0 "$PACKAGE" 2>&1 | tr -d '\r')"
if ! "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  cma_msg restore_success "$PACKAGE"

  # JSONL Logging
  mkdir -p "$LOG_DIR"
  TIMESTAMP="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
  cat >> "$LOG_DIR/actions.jsonl" <<EOF
{"timestamp_utc":"$TIMESTAMP","action":"restore","model":"$MODEL","codename":"$DEVICE","android_version":"$ANDROID_VER","package":"$PACKAGE","command":"pm enable --user 0 $PACKAGE","output":"$CMD_OUT","verified_state":"enabled","rollback_command":"pm disable-user --user 0 $PACKAGE"}
EOF
else
  cma_msg err_restore_failed "$PACKAGE" >&2
  exit 4
fi
