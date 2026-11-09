#!/usr/bin/env bash
# Clean My Android — Catálogo unificado de mensagens bilíngues (PT-BR / EN).
# Compatível com Bash 3.2+ e POSIX (sem uso de declare -A).

get_cma_lang() {
  local val="${CMA_LANG:-${LANG:-${LC_ALL:-en}}}"
  case "$val" in
    pt*|PT*) echo "pt" ;;
    *) echo "en" ;;
  esac
}

cma_msg() {
  local lang
  lang="$(get_cma_lang)"
  local key="$1"
  shift

  if [[ "$lang" == "pt" ]]; then
    case "$key" in
      err_no_adb)
        printf "Erro: ADB não está instalado.\n"
        ;;
      err_device_count)
        printf "Erro: conecte e autorize exatamente um dispositivo ADB. Detectados: %s.\n" "$@"
        ;;
      device_info)
        printf "Dispositivo: %s | device=%s | product=%s | Android=%s\n" "$@"
        ;;
      read_only_mode)
        printf "Modo somente leitura. Nenhuma alteração foi realizada.\n"
        ;;
      disabled_packages_header)
        printf "Pacotes atualmente desativados para o usuário 0:\n"
        ;;
      err_invalid_args)
        printf "Erro: argumentos inválidos.\n"
        ;;
      err_invalid_package)
        printf "Erro: nome de pacote inválido: %s\n" "$@"
        ;;
      err_device_gate)
        printf "Erro: aplicação bloqueada. Dispositivo ou versão do Android não suportados pelo gate de aplicação (%s / Android %s).\n" "$@"
        ;;
      err_missing_support)
        printf "Erro: arquivo de gate de aplicação não encontrado: %s\n" "$@"
        ;;
      err_missing_protection)
        printf "Erro: lista de proteção não encontrada: %s\n" "$@"
        ;;
      err_protected_package)
        printf "Bloqueado: %s está na lista de componentes protegidos.\n" "$@"
        ;;
      err_package_not_found)
        printf "Erro: pacote não encontrado no dispositivo: %s\n" "$@"
        ;;
      info_already_disabled)
        printf "%s já está desativado para o usuário 0. Nenhuma alteração.\n" "$@"
        ;;
      prompt_debloat_warning)
        printf "Ação solicitada: desativar somente %s para o usuário 0.\nIsso pode afetar funções que dependam do pacote. Nenhum dado será apagado.\n" "$@"
        ;;
      prompt_debloat_confirm)
        printf "Para confirmar, digite exatamente: DESATIVAR %s : " "$@"
        ;;
      prompt_restore_warning)
        printf "Ação solicitada: reativar somente %s.\n" "$@"
        ;;
      prompt_restore_confirm)
        printf "Para confirmar, digite exatamente: REATIVAR %s : " "$@"
        ;;
      action_cancelled)
        printf "Cancelado. Nenhuma alteração realizada.\n"
        ;;
      debloat_success)
        printf "Confirmado: %s está desativado para o usuário 0.\n" "$@"
        ;;
      err_debloat_failed)
        printf "Não foi possível confirmar o estado final de %s.\n" "$@"
        ;;
      info_not_disabled)
        printf "%s não consta como desativado para o usuário 0. Nenhuma alteração.\n" "$@"
        ;;
      restore_success)
        printf "Confirmado: %s não está mais desativado para o usuário 0.\n" "$@"
        ;;
      err_restore_failed)
        printf "Não foi possível confirmar a reativação de %s.\n" "$@"
        ;;
      snapshot_start)
        printf "Iniciando snapshot '%s' do dispositivo...\n" "$@"
        ;;
      snapshot_sanitizing)
        printf "Sanitizando dados coletados antes da gravação final...\n"
        ;;
      snapshot_success)
        printf "Snapshot '%s' gerado e verificado com sucesso em: %s\n" "$@"
        ;;
      err_snapshot_sanitization)
        printf "Erro: falha na validação de sanitização do snapshot em: %s\n" "$@"
        ;;
      *)
        printf "%s\n" "$key"
        ;;
    esac
  else
    case "$key" in
      err_no_adb)
        printf "Error: ADB is not installed.\n"
        ;;
      err_device_count)
        printf "Error: connect and authorize exactly one ADB device. Detected: %s.\n" "$@"
        ;;
      device_info)
        printf "Device: %s | device=%s | product=%s | Android=%s\n" "$@"
        ;;
      read_only_mode)
        printf "Read-only mode. No changes were made.\n"
        ;;
      disabled_packages_header)
        printf "Packages currently disabled for user 0:\n"
        ;;
      err_invalid_args)
        printf "Error: invalid arguments.\n"
        ;;
      err_invalid_package)
        printf "Error: invalid package name: %s\n" "$@"
        ;;
      err_device_gate)
        printf "Error: apply blocked. Device or Android version not supported by apply gate (%s / Android %s).\n" "$@"
        ;;
      err_missing_support)
        printf "Error: apply support file not found: %s\n" "$@"
        ;;
      err_missing_protection)
        printf "Error: protection list not found: %s\n" "$@"
        ;;
      err_protected_package)
        printf "Blocked: %s is in the protected components list.\n" "$@"
        ;;
      err_package_not_found)
        printf "Error: package not found on device: %s\n" "$@"
        ;;
      info_already_disabled)
        printf "%s is already disabled for user 0. No changes.\n" "$@"
        ;;
      prompt_debloat_warning)
        printf "Requested action: disable only %s for user 0.\nThis may affect functions depending on the package. No data will be erased.\n" "$@"
        ;;
      prompt_debloat_confirm)
        printf "To confirm, type exactly: DISABLE %s : " "$@"
        ;;
      prompt_restore_warning)
        printf "Requested action: re-enable only %s.\n" "$@"
        ;;
      prompt_restore_confirm)
        printf "To confirm, type exactly: REENABLE %s : " "$@"
        ;;
      action_cancelled)
        printf "Cancelled. No changes made.\n"
        ;;
      debloat_success)
        printf "Confirmed: %s is disabled for user 0.\n" "$@"
        ;;
      err_debloat_failed)
        printf "Could not confirm final state of %s.\n" "$@"
        ;;
      info_not_disabled)
        printf "%s is not disabled for user 0. No changes.\n" "$@"
        ;;
      restore_success)
        printf "Confirmed: %s is no longer disabled for user 0.\n" "$@"
        ;;
      err_restore_failed)
        printf "Could not confirm re-enabling of %s.\n" "$@"
        ;;
      snapshot_start)
        printf "Starting device snapshot '%s'...\n" "$@"
        ;;
      snapshot_sanitizing)
        printf "Sanitizing collected data before final write...\n"
        ;;
      snapshot_success)
        printf "Snapshot '%s' successfully generated and verified in: %s\n" "$@"
        ;;
      err_snapshot_sanitization)
        printf "Error: snapshot sanitization check failed in: %s\n" "$@"
        ;;
      *)
        printf "%s\n" "$key"
        ;;
    esac
  fi
}
