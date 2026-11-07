#!/usr/bin/env bash
# Clean My Android — reativação individual, com confirmação.
set -Eeuo pipefail

usage() {
  cat <<'EOF'
Uso:
  ./restore.sh PACOTE

Reativa somente um pacote por execução. Não há restauração em massa.
EOF
}
if ! command -v adb >/dev/null 2>&1; then
  echo "Erro: ADB não está instalado." >&2; exit 1
fi
if [[ ${#} -ne 1 || "$1" == "--help" || "$1" == "-h" ]]; then usage; exit 2; fi
PACKAGE="$1"
if [[ ! "$PACKAGE" =~ ^[A-Za-z0-9_]+(\.[A-Za-z0-9_]+)+$ ]]; then
  echo "Erro: nome de pacote inválido." >&2; exit 2
fi
mapfile -t DEVICES < <(adb devices | awk 'NR > 1 && $2 == "device" {print $1}')
if [[ ${#DEVICES[@]} -ne 1 ]]; then
  echo "Erro: conecte e autorize exatamente um dispositivo ADB. Detectados: ${#DEVICES[@]}." >&2
  adb devices -l; exit 1
fi
ADB=(adb -s "${DEVICES[0]}")
if ! "${ADB[@]}" shell pm path "$PACKAGE" 2>/dev/null | tr -d '\r' | grep -q '^package:'; then
  echo "Erro: pacote não encontrado: $PACKAGE" >&2; exit 3
fi
if ! "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  echo "$PACKAGE não consta como desativado para o usuário 0. Nenhuma alteração."; exit 0
fi
echo "Ação solicitada: reativar somente $PACKAGE."
read -r -p "Para confirmar, digite exatamente: REATIVAR $PACKAGE : " CONFIRM
if [[ "$CONFIRM" != "REATIVAR $PACKAGE" ]]; then
  echo "Cancelado. Nenhuma alteração realizada."; exit 0
fi
"${ADB[@]}" shell pm enable --user 0 "$PACKAGE"
if ! "${ADB[@]}" shell pm list packages -d --user 0 | tr -d '\r' | grep -Fxq "package:$PACKAGE"; then
  echo "Confirmado: $PACKAGE não está mais desativado para o usuário 0."
else
  echo "Não foi possível confirmar a reativação de $PACKAGE." >&2; exit 4
fi
