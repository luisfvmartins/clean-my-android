#!/usr/bin/env bash
# ==============================================================================
# Motorola Edge 60 Pro (Hello UI / Android 14/15) - Debloat & Degoogle Script
# Autor: Luís Martins (@luisfvmartins)
# Repositório: https://github.com/luisfvmartins/motorola-edge-debloat-degoogle
# ==============================================================================

set -e

echo "=================================================================="
echo " Motorola Edge Series - Debloat & Degoogle Automático via ADB     "
echo "=================================================================="

# 1. Verifica conectividade ADB
if ! command -v adb &> /dev/null; then
    echo "[-] Erro: 'adb' não está instalado no seu computador."
    exit 1
fi

DEVICE_COUNT=$(adb devices | grep -v "List" | grep "device" | wc -l)
if [ "$DEVICE_COUNT" -eq 0 ]; then
    echo "[-] Nenhum dispositivo ADB conectado ou autorizado."
    echo "    Ative a Depuração USB/Wi-Fi nas Opções de Desenvolvedor e tente novamente."
    exit 1
fi

echo "[+] Dispositivo detectado:"
adb devices -l
echo ""

read -p "Deseja iniciar o processo completo de debloat e otimização? (s/N): " CONFIRM
if [[ "$CONFIRM" != "s" && "$CONFIRM" != "S" ]]; then
    echo "Operação cancelada pelo usuário."
    exit 0
fi

# 2. Desinstalação completa de Adwares / Jogos fantasmas de terceiros
echo ""
echo "=== [1/6] Removendo Adwares e Espiões em /data/app ==="
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

# 3. Liberação de espaço: Desinstalando atualizações de pacotes do sistema
echo ""
echo "=== [2/6] Purgando atualizações de sistema em /data/app (+4 GB livres) ==="
DATA_UPDATES=(
    "android.autoinstalls.config.motorola.layout"
    "com.android.chrome"
    "com.android.vending"
    "com.aura.oobe.vodafone"
    "com.dti.amx"
    "com.dti.motorola"
    "com.google.ambient.streaming"
    "com.google.android.aicore"
    "com.google.android.apps.bard"
    "com.google.android.apps.carrier.carrierwifi"
    "com.google.android.apps.docs"
    "com.google.android.apps.maps"
    "com.google.android.apps.messaging"
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
    "com.google.android.contacts"
    "com.google.android.deskclock"
    "com.google.android.dialer"
    "com.google.android.gm"
    "com.google.android.gms.supervision"
    "com.google.android.googlequicksearchbox"
    "com.google.android.marvin.talkback"
    "com.google.android.odad"
    "com.google.android.projection.gearhead"
    "com.google.android.tts"
    "com.google.android.verifier"
    "com.google.android.videos"
    "com.google.android.youtube"
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

# 4. Congelamento dos pacotes de sistema
echo ""
echo "=== [3/6] Congelando pacotes de sistema desnecessários (disabled-user) ==="
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PKG_LIST="$SCRIPT_DIR/../data/disabled_packages.txt"

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

# 5. Sandboxing do Google Play Services
echo ""
echo "=== [4/6] Aplicando Sandboxing no Google Play Services (com.google.android.gms) ==="
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
echo "[+] Permissões invasivas do Google Play Services revogadas."

# 6. Finalização de perfis fantasmas
echo ""
echo "=== [5/6] Limpeza de Perfis Fantasmas secundários ==="
adb shell am stop-user -f 11 2>/dev/null || true
adb shell pm remove-user 10 2>/dev/null || true
echo "[+] Perfis secundários limpos."

# 7. Otimizações de Áudio (Wavelet) e Teclado
echo ""
echo "=== [6/6] Ajustes Finais ==="
# Permissão especial para o Wavelet
if adb shell pm list packages | grep -q "com.pittvandewitt.wavelet"; then
    echo "[+] Concedendo permissão DUMP ao Wavelet..."
    adb shell pm grant com.pittvandewitt.wavelet android.permission.DUMP 2>/dev/null || true
fi

# Se FUTO Keyboard estiver instalado, desativa o Gboard das IMEs
if adb shell pm list packages | grep -q "org.futo.inputmethod.latin"; then
    echo "[+] FUTO Keyboard detectado. Desativando Gboard das entradas ativas..."
    adb shell ime disable com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME 2>/dev/null || true
    adb shell cmd appops set com.google.android.inputmethod.latin RUN_IN_BACKGROUND ignore 2>/dev/null || true
fi

# Se Lawnchair estiver instalado, define como Launcher padrão
if adb shell pm list packages | grep -q "app.lawnchair"; then
    echo "[+] Definindo Lawnchair como launcher padrão..."
    adb shell cmd role add-role-holder --user 0 android.app.role.HOME app.lawnchair.play 2>/dev/null || true
fi

echo ""
echo "=================================================================="
echo " [OK] Debloat e Otimização concluídos com sucesso!"
echo " Total de pacotes desativados no sistema: $(adb shell pm list packages -d --user 0 | wc -l)"
echo " Espaço livre em disco: $(adb shell df -h /data | tail -n 1 | awk '{print $4}')"
echo "=================================================================="
