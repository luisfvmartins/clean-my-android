#!/usr/bin/env bash
# Clean My Android — inspeção e desativação individual, com confirmação.
set -Eeuo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTECTED_LIST="$SCRIPT_DIR/../data/protected_essential_packages.txt"

usage() {
  cat <<'EOF'
Uso:
  ./debloat.sh                 # somente leitura: identifica o aparelho e lista pacotes desativados
  ./debloat.sh --apply PACOTE  # desativa um único pacote após confirmação

A aplicação de mudanças está limitada ao Moto G54 5G (Android 15).
O script nunca limpa dados, desinstala pacotes, altera AppOps ou remove perfis.
EOF
}

if ! command -v adb >/dev/null 2>&1; then
  echo "Erro: ADB não está instalado." >&2
  exit 1
fi

mapfile -t DEVICES < <(adb devices | awk 'NR > 1 && $2 == "device" {print $1}')
if [[ ${#DEVICES[@]} -ne 1 ]]; then
  echo "Erro: conecte e autorize exatamente um dispositivo ADB. Detectados: ${#DEVICES[@]}." >&2
  adb devices -l
  exit 1
fi

ADB=(adb -s "${DEVICES[0]}")
MODEL="$("${ADB[@]}" shell getprop ro.product.model | tr -d '\r')"
DEVICE="$("${ADB[@]}" shell getprop ro.product.device | tr -d '\r')"
PRODUCT="$("${ADB[@]}" shell getprop ro.build.product | tr -d '\r')"
ANDROID_VER="$("${ADB[@]}" shell getprop ro.build.version.release | tr -d '\r')"

echo "Dispositivo: $MODEL | device=$DEVICE | product=$PRODUCT | Android=$ANDROID_VER"
echo

if [[ ${1:-} == "--help" || ${1:-} == "-h" ]]; then usage; exit 0; fi
if [[ ${1:-} != "--apply" ]]; then
  echo "Modo somente leitura. Nenhuma alteração foi realizada."
  echo "Pacotes atualmente desativados para o usuário 0:"
  "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | sort
  echo
  usage
  exit 0
fi

if [[ ${#} -ne 2 ]]; then usage >&2; exit 2; fi
PACKAGE="$2"
if [[ ! "$PACKAGE" =~ ^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$ ]]; then
  echo "Erro: nome de pacote inválido." >&2; exit 2
fi

if [[ "$ANDROID_VER" != "15" || ! ( "$DEVICE" =~ ^cancunf(_g_sysn)?$ || "$PRODUCT" =~ ^cancunf(_g_sysn)?$ ) ]]; then
  echo "Erro: aplicação bloqueada. A validação disponível é específica do Moto G54 5G com Android 15." >&2; exit 3
fi
if [[ ! -f "$PROTECTED_LIST" ]]; then
  echo "Erro: lista de proteção não encontrada: $PROTECTED_LIST" >&2; exit 4
fi
if grep -Fxq "$PACKAGE" "$PROTECTED_LIST"; then
  echo "Bloqueado: $PACKAGE está na lista de componentes protegidos." >&2; exit 5
fi
if ! "${ADB[@]}" shell pm path "$PACKAGE" 2>/dev/null | tr -d '\r' | grep -q '^package:'; then
  echo "Erro: pacote não encontrado no dispositivo: $PACKAGE" >&2; exit 6
fi
if "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  echo "$PACKAGE já está desativado para o usuário 0. Nenhuma alteração."; exit 0
fi

echo "Ação solicitada: desativar somente $PACKAGE para o usuário 0."
echo "Isso pode afetar funções que dependam do pacote. Nenhum dado será apagado."
read -r -p "Para confirmar, digite exatamente: DESATIVAR $PACKAGE : " CONFIRM
if [[ "$CONFIRM" != "DESATIVAR $PACKAGE" ]]; then
  echo "Cancelado. Nenhuma alteração realizada."; exit 0
fi
"${ADB[@]}" shell pm disable-user --user 0 "$PACKAGE"
if "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  echo "Confirmado: $PACKAGE está desativado para o usuário 0."
else
  echo "Não foi possível confirmar o estado final de $PACKAGE." >&2; exit 7
fi
