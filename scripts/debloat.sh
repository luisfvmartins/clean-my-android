#!/usr/bin/env bash
# ==============================================================================
# Clean My Android - Debloat, Degoogle & Extreme Optimization Script
# Homologado em:
#   - Motorola Edge 60 Pro (cybert_g_sys / Hello UI / Android 14 & 15)
#   - Motorola Moto G54 5G (XT2343-1 / cancunf_g_sysn / Android 15)
# Autor: Luís Martins (@luisfvmartins)
# Repositório: https://github.com/luisfvmartins/clean-my-android
# ==============================================================================

set -e

echo "=================================================================="
echo "          Clean My Android - Otimização & Debloat Automático      "
echo "=================================================================="

# 1. Verifica conectividade ADB
if ! command -v adb &> /dev/null; then
    echo "[-] Erro: 'adb' não está instalado no seu computador."
    exit 1
fi

DEVICE_COUNT=$(adb devices | grep -v "List" | grep -c "device" || true)
if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "[-] Nenhum dispositivo ADB conectado ou autorizado."
    echo "    Ative a Depuração USB/Wi-Fi nas Opções de Desenvolvedor e tente novamente."
    exit 1
fi

MODEL=$(adb shell getprop ro.product.model | tr -d '\r')
CODENAME=$(adb shell getprop ro.product.device | tr -d '\r')
ANDROID_VER=$(adb shell getprop ro.build.version.release | tr -d '\r')

echo "[+] Dispositivo detectado: $MODEL ($CODENAME) - Android $ANDROID_VER"
adb devices -l
echo ""

read -p "Deseja iniciar o processo completo de debloat, restauração de segurança e otimização? (s/N): " CONFIRM
if [[ "$CONFIRM" != "s" && "$CONFIRM" != "S" ]]; then
    echo "Operação cancelada pelo usuário."
    exit 0
fi

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROTECTED_LIST="$SCRIPT_DIR/../data/protected_essential_packages.txt"
PERSISTENT_LIST="$SCRIPT_DIR/../data/persistent_uninstall_packages.txt"
PKG_LIST="$SCRIPT_DIR/../data/disabled_packages.txt"

# 2. Etapa 0: Auto-cura e proteção de pacotes essenciais do sistema (Play Integrity / Dolby / Settings Search)
echo ""
echo "=== [1/9] Protegendo e Restaurando Componentes Críticos do Sistema ==="
if [ -f "$PROTECTED_LIST" ]; then
    while IFS= read -r pkg || [ -n "$pkg" ]; do
        [ -z "$pkg" ] && continue
        [[ "$pkg" =~ ^#.* ]] && continue
        echo "Garantindo estado ativo (enabled): $pkg"
        adb shell pm enable "$pkg" 2>/dev/null || true
    done < "$PROTECTED_LIST"
fi

# 3. Etapa 1: Erradicar Daemons de Telemetria "Zumbis" (FLAG_PERSISTENT) que ignoram pm disable-user
echo ""
echo "=== [2/9] Erradicando Daemons de Telemetria FLAG_PERSISTENT (Zumbis em RAM) ==="
if [ -f "$PERSISTENT_LIST" ]; then
    while IFS= read -r pkg || [ -n "$pkg" ]; do
        [ -z "$pkg" ] && continue
        [[ "$pkg" =~ ^#.* ]] && continue
        echo "Removendo daemon persistente para user 0: $pkg"
        adb shell pm uninstall --user 0 "$pkg" 2>/dev/null || true
    done < "$PERSISTENT_LIST"
fi

# 4. Desinstalação de Adwares pré-instalados em /data/app
echo ""
echo "=== [3/9] Removendo Adwares e Espiões Pré-Instalados em /data/app ==="
THIRD_PARTY_BLOAT=(
    "com.google.android.safetycore"
    "com.google.android.contactkeys"
    "com.google.android.apps.subscriptions.red"
    "com.google.android.apps.walletnfcrel"
    "com.google.android.apps.adm"
    "com.google.android.apps.kids.familylink"
    "com.oakever.tiletrip"
    "com.puzzlegames.puzzlebrickslegend"
    "wool.match.color.sort.jam.puzzle"
    "all.documentreader.filereader.office.viewer"
    "ringtonesforandroidphonefree.ringtones.ringtonessongs.ringtonesapp"
)

for pkg in "${THIRD_PARTY_BLOAT[@]}"; do
    echo "Removendo $pkg..."
    adb shell pm uninstall "$pkg" 2>/dev/null || adb shell pm uninstall --user 0 "$pkg" 2>/dev/null || true
done

# 5. Liberação de espaço: Desinstalando atualizações de pacotes do sistema desnecessários
echo ""
echo "=== [4/9] Purgando atualizações de bloatware de sistema em /data/app ==="
DATA_UPDATES=(
    "android.autoinstalls.config.motorola.layout"
    "com.aura.oobe.vodafone"
    "com.dti.amx"
    "com.dti.motorola"
    "com.google.ambient.streaming"
    "com.google.android.aicore"
    "com.google.android.apps.bard"
    "com.google.android.apps.carrier.carrierwifi"
    "com.google.android.apps.docs"
    "com.google.android.apps.maps"
    "com.google.android.apps.nbu.files"
    "com.google.android.apps.photos"
    "com.google.android.apps.restore"
    "com.google.android.apps.safetyhub"
    "com.google.android.apps.tachyon"
    "com.google.android.apps.wellbeing"
    "com.google.android.apps.youtube.music"
    "com.google.android.as"
    "com.google.android.as.oss"
    "com.google.android.calculator"
    "com.google.android.calendar"
    "com.google.android.deskclock"
    "com.google.android.gm"
    "com.google.android.gms.supervision"
    "com.google.android.googlequicksearchbox"
    "com.google.android.marvin.talkback"
    "com.google.android.odad"
    "com.google.android.projection.gearhead"
    "com.google.android.tts"
    "com.google.android.verifier"
    "com.google.android.videos"
    "com.google.ar.core"
    "com.inmobi.weather"
    "com.motorola.account"
    "com.motorola.livewallpaper3"
    "com.motorola.mobiledesktop"
    "com.motorola.securityhub"
    "com.motorola.smartfeed"
    "com.motorola.touchshare"
)

for pkg in "${DATA_UPDATES[@]}"; do
    adb shell pm uninstall "$pkg" 2>/dev/null || true
done

# 6. Congelamento e limpeza dos pacotes de sistema (disabled-user)
echo ""
echo "=== [5/9] Congelando e Limpando Pacotes de Bloatware/Telemetria (disabled-user) ==="
if [ -f "$PKG_LIST" ]; then
    while IFS= read -r pkg || [ -n "$pkg" ]; do
        [ -z "$pkg" ] && continue
        [[ "$pkg" =~ ^#.* ]] && continue
        echo "Congelando: $pkg"
        adb shell pm clear "$pkg" 2>/dev/null || true
        adb shell pm disable-user --user 0 "$pkg" 2>/dev/null || true
        adb shell am force-stop "$pkg" 2>/dev/null || true
    done < "$PKG_LIST"
else
    echo "[-] Arquivo $PKG_LIST não encontrado!"
fi

# 7. Sandboxing do Google Play Services
echo ""
echo "=== [6/9] Aplicando Sandboxing no Google Play Services (com.google.android.gms) ==="
PERMS=(
    "android.permission.ACCESS_FINE_LOCATION"
    "android.permission.ACCESS_COARSE_LOCATION"
    "android.permission.ACCESS_BACKGROUND_LOCATION"
    "android.permission.CAMERA"
    "android.permission.RECORD_AUDIO"
    "android.permission.READ_CONTACTS"
    "android.permission.WRITE_CONTACTS"
    "android.permission.READ_CALENDAR"
    "android.permission.WRITE_CALENDAR"
    "android.permission.READ_CALL_LOG"
    "android.permission.WRITE_CALL_LOG"
    "android.permission.READ_SMS"
    "android.permission.RECEIVE_SMS"
    "android.permission.SEND_SMS"
    "android.permission.ACTIVITY_RECOGNITION"
    "android.permission.BODY_SENSORS"
)

for perm in "${PERMS[@]}"; do
    adb shell pm revoke com.google.android.gms "$perm" 2>/dev/null || true
done

GMS_UID=$(adb shell pm dump com.google.android.gms 2>/dev/null | grep -m 1 'userId=' | grep -oE '[0-9]+' || true)
if [ -n "$GMS_UID" ]; then
    echo "[+] Neutralizando rastreamento SYSTEM_FIXED no UID $GMS_UID do Play Services via AppOps..."
    adb shell cmd appops set --uid "$GMS_UID" FINE_LOCATION ignore 2>/dev/null || true
    adb shell cmd appops set --uid "$GMS_UID" COARSE_LOCATION ignore 2>/dev/null || true
    adb shell cmd appops set --uid "$GMS_UID" MONITOR_LOCATION ignore 2>/dev/null || true
    adb shell cmd appops set --uid "$GMS_UID" MONITOR_HIGH_POWER_LOCATION ignore 2>/dev/null || true
    adb shell cmd appops set --uid "$GMS_UID" ACTIVITY_RECOGNITION ignore 2>/dev/null || true
    adb shell cmd appops set --uid "$GMS_UID" BODY_SENSORS ignore 2>/dev/null || true
fi
echo "[+] Google Play Services isolado e neutralizado com sucesso."

# 8. Revogação de Permissões Abusivas em Apps de Sistema e de Usuário (Edge 60 Pro + Moto G54 5G)
echo ""
echo "=== [7/9] Revogando Permissões Abusivas e Bloqueando Clipboard/Sensores ==="

# Apps do Sistema (Motorola Camera 3 [Moto G54] & Camera 5 [Edge 60 Pro], Multi-SIM, Play Store, Chrome, YouTube)
echo "[+] Revogando permissões invasivas em apps de sistema..."
adb shell pm revoke --user 0 com.motorola.camera3 android.permission.ACCESS_FINE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 com.motorola.camera3 android.permission.ACCESS_COARSE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 com.motorola.camera5 android.permission.ACCESS_COARSE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 com.motorola.msimsettings android.permission.READ_CONTACTS 2>/dev/null || true
adb shell pm revoke --user 0 com.google.android.ext.services android.permission.ACCESS_COARSE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 com.google.android.euicc android.permission.CAMERA 2>/dev/null || true
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_FINE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_COARSE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_BACKGROUND_LOCATION 2>/dev/null || true

for p in READ_SMS RECEIVE_SMS SEND_SMS RECORD_AUDIO; do
    adb shell pm revoke com.android.vending "android.permission.$p" 2>/dev/null || true
done

for p in READ_CONTACTS RECORD_AUDIO CAMERA ACCESS_FINE_LOCATION; do
    adb shell pm revoke com.android.chrome "android.permission.$p" 2>/dev/null || true
done

for p in CAMERA RECORD_AUDIO READ_MEDIA_IMAGES READ_MEDIA_VIDEO; do
    adb shell pm revoke com.google.android.youtube "android.permission.$p" 2>/dev/null || true
done

# Apps de Usuário (Terceiros - Edge 60 Pro & Moto G54 5G)
echo "[+] Revogando permissões invasivas e leitura de Clipboard em apps de terceiros..."
for p in READ_CALL_LOG SEND_SMS ANSWER_PHONE_CALLS ACCESS_FINE_LOCATION ACCESS_COARSE_LOCATION; do
    adb shell pm revoke com.whatsapp "android.permission.$p" 2>/dev/null || true
done

adb shell cmd appops set --uid com.openai.chatgpt READ_CLIPBOARD ignore 2>/dev/null || true
adb shell cmd appops set --uid com.openai.chatgpt FINE_LOCATION ignore 2>/dev/null || true
adb shell cmd appops set --uid com.openai.chatgpt COARSE_LOCATION ignore 2>/dev/null || true
adb shell cmd appops set --uid com.openai.chatgpt MONITOR_LOCATION ignore 2>/dev/null || true
adb shell cmd appops set --uid com.openai.chatgpt MONITOR_HIGH_POWER_LOCATION ignore 2>/dev/null || true
adb shell pm revoke com.openai.chatgpt android.permission.CAMERA 2>/dev/null || true

adb shell cmd appops set com.lemon.lvoverseas READ_CLIPBOARD ignore 2>/dev/null || true
for p in CAMERA RECORD_AUDIO READ_MEDIA_IMAGES READ_MEDIA_VIDEO READ_MEDIA_AUDIO; do
    adb shell pm revoke com.lemon.lvoverseas "android.permission.$p" 2>/dev/null || true
done

adb shell pm revoke --user 0 com.digidust.elokence.akinator.freemium android.permission.RECORD_AUDIO 2>/dev/null || true
adb shell pm revoke --user 0 com.spotify.music android.permission.RECORD_AUDIO 2>/dev/null || true
adb shell pm revoke --user 0 com.pinterest android.permission.CAMERA 2>/dev/null || true
adb shell pm revoke --user 0 com.roblox.client android.permission.CAMERA 2>/dev/null || true
adb shell pm revoke --user 0 com.ubercab android.permission.RECORD_AUDIO 2>/dev/null || true
adb shell pm revoke --user 0 com.taxis99 android.permission.READ_CONTACTS 2>/dev/null || true
adb shell pm revoke --user 0 com.taxis99 android.permission.CAMERA 2>/dev/null || true
adb shell pm revoke --user 0 com.minhaunifique.unifique android.permission.ACCESS_COARSE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 com.brave.browser android.permission.ACCESS_COARSE_LOCATION 2>/dev/null || true
adb shell pm revoke --user 0 br.com.ajfans android.permission.ACCESS_COARSE_LOCATION 2>/dev/null || true
adb shell cmd appops set br.com.ajfans RUN_IN_BACKGROUND ignore 2>/dev/null || true
adb shell cmd appops set br.com.ajfans WAKE_LOCK ignore 2>/dev/null || true
adb shell pm revoke --user 0 br.org.app.barilife android.permission.ACCESS_LOCAL_NETWORK 2>/dev/null || true

# 9. Lockdown de Bloatwares Protegidos (isNonDisablePackage)
echo ""
echo "=== [8/9] Paralisando Bloatwares com Proteção 'non-disable' via AppOps, Standby Bucket & NetPolicy ==="
NON_DISABLE_PKGS=(
    "com.payjoy.access"
    "com.amazon.appmanager"
    "com.motorola.ccc.devicemanagement"
    "com.motorola.paks.notification"
    "com.motorola.installer"
    "com.google.android.sdksandbox"
)

for pkg in "${NON_DISABLE_PKGS[@]}"; do
    adb shell pm clear "$pkg" 2>/dev/null || true
    adb shell am set-standby-bucket "$pkg" restricted 2>/dev/null || true
    UID=$(adb shell dumpsys package "$pkg" 2>/dev/null | grep -m 1 'appId=' | grep -oE '[0-9]+' || true)
    if [ -n "$UID" ]; then
        echo "Paralisando UID $UID ($pkg)..."
        for op in RUN_IN_BACKGROUND RUN_ANY_IN_BACKGROUND WAKE_LOCK START_FOREGROUND GET_USAGE_STATS REQUEST_INSTALL_PACKAGES POST_NOTIFICATION COARSE_LOCATION FINE_LOCATION; do
            adb shell cmd appops set --uid "$pkg" "$op" ignore 2>/dev/null || adb shell cmd appops set --uid "$UID" "$op" ignore 2>/dev/null || true
        done
        adb shell cmd netpolicy add restrict-background-blacklist "$UID" 2>/dev/null || true
    fi
done

# 10. Limpeza de Perfis Fantasmas, Caches e Ajustes Finais
echo ""
echo "=== [9/9] Limpeza de Perfis Fantasmas, Caches e Ajustes Finais ==="
adb shell am stop-user -f 11 2>/dev/null || true
adb shell pm remove-user 10 2>/dev/null || true
adb shell pm trim-caches 999999999999 2>/dev/null || true

if adb shell pm list packages | grep -q "com.pittvandewitt.wavelet"; then
    echo "[+] Concedendo permissão DUMP ao Wavelet..."
    adb shell pm grant com.pittvandewitt.wavelet android.permission.DUMP 2>/dev/null || true
fi

if adb shell pm list packages | grep -qE "org.futo.inputmethod.latin|helium314.keyboard"; then
    echo "[+] Teclado FOSS detectado. Desativando Gboard das entradas ativas..."
    adb shell ime disable com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME 2>/dev/null || true
    adb shell cmd appops set com.google.android.inputmethod.latin RUN_IN_BACKGROUND ignore 2>/dev/null || true
fi

if adb shell pm list packages | grep -q "app.lawnchair"; then
    echo "[+] Definindo Lawnchair como launcher padrão..."
    adb shell cmd role add-role-holder --user 0 android.app.role.HOME app.lawnchair.play 2>/dev/null || true
fi

echo ""
echo "=================================================================="
echo " [OK] Debloat e Otimização concluídos com sucesso!"
echo " Dispositivo: $MODEL ($CODENAME)"
echo " Total de pacotes desativados no sistema: $(adb shell pm list packages -d --user 0 | wc -l)"
echo " Espaço livre em disco: $(adb shell df -h /data | tail -n 1 | awk '{print $4}')"
echo " Dica: Reinicie o aparelho ('adb reboot') para encerrar os processos persistentes."
echo "=================================================================="
