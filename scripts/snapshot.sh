#!/usr/bin/env bash
# Clean My Android — Coleta de snapshot técnico do dispositivo (somente leitura).
# Compatível com Bash 3.2+ (macOS / Linux) e com sanitização verificada.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LIB_MESSAGES="$SCRIPT_DIR/lib/messages.sh"
CHECK_SANITIZATION="$SCRIPT_DIR/check_sanitization.py"

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
  ./snapshot.sh --label <before|after> --out <DIR> [opções]

Opções:
  --label LABEL         Rótulo da coleta: 'before' (antes) ou 'after' (depois)
  --out DIR             Diretório de destino dos arquivos de evidência
  --with-permissions    Coleta dumpsys package (permissões concedidas e declaradas)
  --with-appops         Coleta permissões em nível de AppOps
  --help, -h            Exibe esta mensagem de ajuda

Códigos de saída (Exit Codes):
  0: Sucesso na coleta e validação de sanitização, ou exibição de ajuda
  1: ADB ausente ou número incorreto de dispositivos conectados (exatamente 1 exigido)
  2: Argumentos obrigatórios ausentes ou inválidos
  3: Falha na comunicação com o ADB
  4: Falha na criação do diretório de destino
  5: Falha na validação de sanitização dos dados coletados

O script é estritamente de leitura. Nenhum dado ou configuração do aparelho é alterado.
EOF
  else
    cat <<'EOF'
Usage:
  ./snapshot.sh --label <before|after> --out <DIR> [options]

Options:
  --label LABEL         Snapshot stage: 'before' or 'after'
  --out DIR             Target output directory for evidence files
  --with-permissions    Capture dumpsys package (granted and declared permissions)
  --with-appops         Capture AppOps status
  --help, -h            Show this help message

Exit Codes:
  0: Success in capture and sanitization verification, or help displayed
  1: ADB missing or incorrect number of connected devices (exactly 1 required)
  2: Missing or invalid required arguments
  3: ADB communication failure
  4: Output directory creation failure
  5: Sanitization check failure on captured data

This script is strictly read-only. No device data or configuration is modified.
EOF
  fi
}

LABEL=""
OUT_DIR=""
WITH_PERMS=0
WITH_APPOPS=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --help|-h)
      usage
      exit 0
      ;;
    --label)
      if [[ $# -lt 2 ]]; then cma_msg err_invalid_args >&2; usage >&2; exit 2; fi
      LABEL="$2"
      shift 2
      ;;
    --out)
      if [[ $# -lt 2 ]]; then cma_msg err_invalid_args >&2; usage >&2; exit 2; fi
      OUT_DIR="$2"
      shift 2
      ;;
    --with-permissions)
      WITH_PERMS=1
      shift
      ;;
    --with-appops)
      WITH_APPOPS=1
      shift
      ;;
    *)
      cma_msg err_invalid_args >&2
      usage >&2
      exit 2
      ;;
  esac
done

if [[ -z "$LABEL" || ( "$LABEL" != "before" && "$LABEL" != "after" ) ]]; then
  cma_msg err_invalid_args >&2
  usage >&2
  exit 2
fi

if [[ -z "$OUT_DIR" ]]; then
  cma_msg err_invalid_args >&2
  usage >&2
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

cma_msg snapshot_start "$LABEL"

TMP_DIR="$(mktemp -d 2>/dev/null || mktemp -d -t 'cma_snapshot')"
# shellcheck disable=SC2064
trap 'rm -rf "$TMP_DIR"' EXIT

# 1. Device Info (Propriedades seguras do sistema)
PROP_FILE="$TMP_DIR/device-info.txt"
PROPS=(
  "ro.product.model"
  "ro.product.device"
  "ro.build.product"
  "ro.build.version.release"
  "ro.build.version.sdk"
  "ro.build.version.security_patch"
  "ro.build.id"
  "ro.build.type"
)
for prop in "${PROPS[@]}"; do
  val="$("${ADB[@]}" shell getprop "$prop" 2>/dev/null | tr -d '\r')"
  printf "%s=%s\n" "$prop" "$val" >> "$PROP_FILE"
done

# 2. Listagens de Pacotes (User 0)
"${ADB[@]}" shell pm list packages -u --user 0 2>/dev/null | tr -d '\r' | sort > "$TMP_DIR/packages-all.txt" || true
"${ADB[@]}" shell pm list packages -e --user 0 2>/dev/null | tr -d '\r' | sort > "$TMP_DIR/packages-enabled.txt" || true
"${ADB[@]}" shell pm list packages -d --user 0 2>/dev/null | tr -d '\r' | sort > "$TMP_DIR/packages-disabled.txt" || true
"${ADB[@]}" shell pm list packages -3 --user 0 2>/dev/null | tr -d '\r' | sort > "$TMP_DIR/packages-third-party.txt" || true
"${ADB[@]}" shell pm list packages -s --user 0 2>/dev/null | tr -d '\r' | sort > "$TMP_DIR/packages-system.txt" || true

# 3. Resumos de Bateria, Memória e Armazenamento
"${ADB[@]}" shell dumpsys battery 2>/dev/null | tr -d '\r' > "$TMP_DIR/battery-summary.txt" || true
"${ADB[@]}" shell dumpsys meminfo 2>/dev/null | tr -d '\r' > "$TMP_DIR/meminfo-summary.txt" || true
"${ADB[@]}" shell df /data 2>/dev/null | tr -d '\r' > "$TMP_DIR/disk-usage.txt" || true

# 4. Opcionais
if [[ $WITH_PERMS -eq 1 ]]; then
  "${ADB[@]}" shell dumpsys package 2>/dev/null | tr -d '\r' > "$TMP_DIR/permissions.txt" || true
fi

if [[ $WITH_APPOPS -eq 1 ]]; then
  "${ADB[@]}" shell cmd appops get 2>/dev/null | tr -d '\r' > "$TMP_DIR/appops.txt" || true
fi

# 5. Sanitização pré-gravação
cma_msg snapshot_sanitizing

if command -v python3 >/dev/null 2>&1 && [[ -f "$CHECK_SANITIZATION" ]]; then
  if ! python3 "$CHECK_SANITIZATION" "$TMP_DIR" >/dev/null 2>&1; then
    cma_msg err_snapshot_sanitization "$TMP_DIR" >&2
    exit 5
  fi
fi

# 6. Gravação Final
mkdir -p "$OUT_DIR" || {
  cma_msg err_invalid_args >&2
  exit 4
}

cp -r "$TMP_DIR"/* "$OUT_DIR/"

cma_msg snapshot_success "$LABEL" "$OUT_DIR"
exit 0
