# 🚀 Motorola Edge - Guia Definitivo de Debloat, Degoogle e Otimização Extrema

[![Android 14/15](https://img.shields.io/badge/Android-14%20%7C%2015-3DDC84?logo=android&logoColor=white)](https://android.com)
[![Motorola Hello UI](https://img.shields.io/badge/Motorola-Hello%20UI%20%2F%20My%20UX-001435?logo=motorola&logoColor=white)](https://motorola.com)
[![ADB & Shizuku](https://img.shields.io/badge/Tool-ADB%20%7C%20Shizuku-blue)](https://developer.android.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Guia minucioso, testado em laboratório no **Motorola Edge 60 Pro** executando o **Hello UI (Android 14/15)**, projetado para remover adwares silenciosos, eliminar telemetrias pesadas, aplicar **De-Google inteligente** (preservando bancos e notificações push) e liberar gigabytes de RAM e armazenamento interno sem root.

---

## 📊 Resultados Obtidos Neste Procedimento

| Métrica | Antes | Depois | Ganho Real |
| :--- | :--- | :--- | :--- |
| **Pacotes Inúteis / Bloatware** | ~440 pacotes ativos | **241 pacotes congelados/removidos** | Sistema 100% enxuto |
| **Memória RAM Livre** | ~4.5 GB livres | **~7.2 GB livres** | **+2.7 GB de RAM livre** |
| **Espaço de Armazenamento** | 193 GB livres | **197 GB livres** | **+4 GB recuperados** em `/data` |
| **Anúncios no Sistema** | Ativos (Glance, Taboola, InMobi) | **ZERO anúncios** | Telas e launcher limpos |
| **Apps de Banco (Caixa, Nubank, PicPay)** | Funcionais | **100% Funcionais** | Integridade preservada |
| **Privacidade** | Telemetria contínua | **Google Play Services enjaulado** | Zero acesso a GPS/Mic |

---

## ⚠️ A Filosofia do "De-Google Inteligente" (Sandboxed GMS)

Muitos tutoriais na internet orientam a desinstalar completamente o `com.google.android.gms` (Google Play Services) ou tentar forçar o **microG** na ROM original. 

### Por que isso é um erro no Android moderno?
1. **Quebra dos Apps de Banco Brasileiros:** Apps como *Caixa, FGTS Trabalhador, PicPay, Mercado Pago, Nubank* utilizam a verificação **Play Integrity API**. Se você remover o Play Services ou colocar o microG em uma ROM com bootloader bloqueado, **seus bancos não abrirão**.
2. **Conflito de Assinatura:** ROMs originais da Motorola não suportam *Signature Spoofing*, impedindo a instalação limpa do microG como serviço de sistema.

### A Nossa Solução (O Google Enjaulado):
Em vez de quebrar o aparelho, nós:
*   Substituímos todos os **apps visíveis da Google** por alternativas de código aberto (**FOSS**).
*   Desativamos os módulos espiões (**Android System Intelligence, Ad Data, Gemini, Telemetria de IA**).
*   Mantemos o **Play Services ativo exclusivamente como túnel mudo para notificações push e integridade bancária**, revogando **todas** as permissões invasivas (Localização, Microfone, Câmera, Contatos, SMS e Sensores corporais).

---

## 🛠️ Pré-requisitos e Conexão ADB

### 1. Ativar Depuração USB ou Sem Fio no Aparelho
1. Vá em **Configurar > Sobre o telefone**.
2. Toque 7 vezes seguidas em **Número da versão** até virar desenvolvedor.
3. Volte em **Sistema > Opções do desenvolvedor**.
4. Ative **Depuração USB** (se usar cabo) ou **Depuração sem fio** (se usar Wi-Fi).

### 2. Pareamento Sem Fio (Android 11+)
Se for conectar via Wi-Fi sem cabo:
```bash
# 1. No celular, toque em "Parear dispositivo com código de pareamento"
# 2. No PC, execute o comando com a porta temporária e o PIN de 6 dígitos:
adb pair 192.168.1.X:PORTA_DO_POPUP CODIGO_PIN

# 3. Feche o pop-up e conecte na porta principal que aparece na tela de Depuração Sem Fio:
adb connect 192.168.1.X:PORTA_PRINCIPAL
adb devices
```

---

## 🚀 Passo a Passo Detalhado da Limpeza

### Etapa 1: Eliminar Adwares Invasivos e Instaladores Fantasmas
O ecossistema de operadoras e fabricantes pré-carrega verdadeiros spywares que instalam joguinhos e propagandas em segundo plano:

```bash
# Digital Turbine (DT Ignite) - Instalador fantasma de propagandas
adb shell pm clear com.dti.motorola && adb shell pm disable-user --user 0 com.dti.motorola
adb shell pm clear com.dti.amx && adb shell pm disable-user --user 0 com.dti.amx

# IronSource Aura - Anúncios da operadora e recomendações
adb shell pm clear com.aura.oobe.motorola && adb shell pm disable-user --user 0 com.aura.oobe.motorola
adb shell pm clear com.aura.oobe.vodafone && adb shell pm disable-user --user 0 com.aura.oobe.vodafone
adb shell pm clear com.orange.aura.oobe && adb shell pm disable-user --user 0 com.orange.aura.oobe
adb shell pm clear com.ironsource.appcloud.oobe.hutchison && adb shell pm disable-user --user 0 com.ironsource.appcloud.oobe.hutchison

# Glance Lockscreen - Anúncios e vídeos na tela de bloqueio
adb shell pm clear com.glance.lockscreenM && adb shell pm disable-user --user 0 com.glance.lockscreenM

# Taboola MIP - Rede global de clickbait incorporada ao sistema
adb shell pm clear com.taboola.mip && adb shell pm disable-user --user 0 com.taboola.mip

# InMobi Weather - Anúncios disfarçados de previsão do tempo (gastava 210MB RAM)
adb shell pm clear com.inmobi.weather && adb shell pm disable-user --user 0 com.inmobi.weather

# Meta / Facebook - Rastreamento e telemetria contínua em segundo plano
adb shell pm clear com.facebook.appmanager && adb shell pm disable-user --user 0 com.facebook.appmanager
adb shell pm clear com.facebook.services && adb shell pm disable-user --user 0 com.facebook.services
adb shell pm clear com.facebook.system && adb shell pm disable-user --user 0 com.facebook.system

# Lojas parceiras desnecessárias
adb shell pm clear com.motorola.brapps && adb shell pm disable-user --user 0 com.motorola.brapps
adb shell pm clear com.indus.appstore && adb shell pm disable-user --user 0 com.indus.appstore
adb shell pm clear com.amazon.appmanager && adb shell pm disable-user --user 0 com.amazon.appmanager
adb shell pm suspend de.telekom.tsc
```

---

### Etapa 2: Desativar Telemetria Pesada da Motorola
Alguns assistentes da Lenovo/Motorola rodam silenciosamente e chegam a drenar **quase 1 GB de RAM**:

```bash
# Lenovo Qira AI - Consumia sozinho ~400 MB de RAM
adb shell pm clear com.lenovo.qira && adb shell pm disable-user --user 0 com.lenovo.qira
adb shell pm clear com.lenovo.qiracore && adb shell pm disable-user --user 0 com.lenovo.qiracore

# Moto SmartFeed - Tela de notícias e anúncios no launcher (~330 MB de RAM)
adb shell pm clear com.motorola.smartfeed && adb shell pm disable-user --user 0 com.motorola.smartfeed

# Telemetrias de uso, bateria e logs da Motorola
adb shell pm clear com.motorola.motocare && adb shell pm disable-user --user 0 com.motorola.motocare
adb shell pm clear com.motorola.help.extlog && adb shell pm disable-user --user 0 com.motorola.help.extlog
adb shell pm clear com.motorola.bug2go && adb shell pm disable-user --user 0 com.motorola.bug2go
adb shell pm clear com.motorola.lifetimedata && adb shell pm disable-user --user 0 com.motorola.lifetimedata
adb shell pm clear com.motorola.bach.modemstats && adb shell pm disable-user --user 0 com.motorola.bach.modemstats
adb shell pm clear com.motorola.wifi.motowifimetrics && adb shell pm disable-user --user 0 com.motorola.wifi.motowifimetrics
adb shell pm clear com.motorola.android.nativedropboxagent && adb shell pm disable-user --user 0 com.motorola.android.nativedropboxagent
adb shell pm clear com.motorola.appforecast && adb shell pm disable-user --user 0 com.motorola.appforecast
adb shell pm clear com.motorola.nfwlocationattribution && adb shell pm disable-user --user 0 com.motorola.nfwlocationattribution
adb shell pm clear com.motorola.ccc.notification && adb shell pm disable-user --user 0 com.motorola.ccc.notification
```

---

### Etapa 3: Desativar Módulos Inúteis de Operadoras Estrangeiras e Fábrica
ROMs globais contêm resíduos de operadoras americanas e asiáticas que não têm utilidade no Brasil:

```bash
# Verizon, AT&T, Vodafone e operadoras asiáticas
adb shell pm clear com.motorola.vzw.pco.extensions.pcoreceiver && adb shell pm disable-user --user 0 com.motorola.vzw.pco.extensions.pcoreceiver
adb shell pm clear com.motorola.attvowifi && adb shell pm disable-user --user 0 com.motorola.attvowifi
adb shell pm clear com.mediatek.op12.ims && adb shell pm disable-user --user 0 com.mediatek.op12.ims
adb shell pm clear com.oem.euiccpartnerapp && adb shell pm disable-user --user 0 com.oem.euiccpartnerapp

# SIM Toolkit (Fim definitivo dos pop-ups intrusivos de horóscopo da operadora)
adb shell pm clear com.android.stk && adb shell pm disable-user --user 0 com.android.stk
adb shell pm clear com.android.simappdialog && adb shell pm disable-user --user 0 com.android.simappdialog

# Testes de linha de montagem e homolação da fábrica
adb shell pm clear com.motorola.motocit && adb shell pm disable-user --user 0 com.motorola.motocit
adb shell pm clear com.android.cts.ctsshim && adb shell pm disable-user --user 0 com.android.cts.ctsshim
adb shell pm clear com.android.cts.priv.ctsshim && adb shell pm disable-user --user 0 com.android.cts.priv.ctsshim

# Bloqueio de atualizações automáticas que reinstalam bloatware
adb shell pm suspend com.motorola.ccc.ota
```

---

### Etapa 4: De-Google - Remoção de Aplicativos do Usuário
Antes de desativar os apps abaixo, instale os substitutos recomendados via **F-Droid** ou **Aurora Store**:

```bash
# Navegador, Loja e Multimídia
adb shell pm clear com.android.chrome && adb shell pm disable-user --user 0 com.android.chrome
adb shell pm clear com.android.vending && adb shell pm disable-user --user 0 com.android.vending
adb shell pm clear com.google.android.youtube && adb shell pm disable-user --user 0 com.google.android.youtube
adb shell pm clear com.google.android.apps.youtube.music && adb shell pm disable-user --user 0 com.google.android.apps.youtube.music
adb shell pm clear com.google.android.videos && adb shell pm disable-user --user 0 com.google.android.videos

# Comunicação, Chamadas e Calendário
adb shell pm clear com.google.android.dialer && adb shell pm disable-user --user 0 com.google.android.dialer
adb shell pm clear com.google.android.apps.messaging && adb shell pm disable-user --user 0 com.google.android.apps.messaging
adb shell pm clear com.google.android.contacts && adb shell pm disable-user --user 0 com.google.android.contacts
adb shell pm clear com.google.android.calendar && adb shell pm disable-user --user 0 com.google.android.calendar
adb shell pm clear com.google.android.gm && adb shell pm disable-user --user 0 com.google.android.gm
adb shell pm clear com.google.android.apps.tachyon && adb shell pm disable-user --user 0 com.google.android.apps.tachyon

# Utilitários e Barra de Pesquisa fixa
adb shell pm clear com.google.android.googlequicksearchbox && adb shell pm disable-user --user 0 com.google.android.googlequicksearchbox
adb shell pm clear com.google.android.apps.maps && adb shell pm disable-user --user 0 com.google.android.apps.maps
adb shell pm clear com.google.android.apps.docs && adb shell pm disable-user --user 0 com.google.android.apps.docs
adb shell pm clear com.google.android.apps.photos && adb shell pm disable-user --user 0 com.google.android.apps.photos
adb shell pm clear com.google.android.apps.nbu.files && adb shell pm disable-user --user 0 com.google.android.apps.nbu.files
adb shell pm clear com.google.android.calculator && adb shell pm disable-user --user 0 com.google.android.calculator
adb shell pm clear com.google.android.deskclock && adb shell pm disable-user --user 0 com.google.android.deskclock
```

#### Para o Teclado (Gboard):
O Android protege o Gboard contra o comando `disable-user` caso não haja outro teclado ativo. Após instalar o **FUTO Keyboard** ou **HeliBoard**:
```bash
adb shell ime disable com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME
adb shell cmd appops set com.google.android.inputmethod.latin RUN_IN_BACKGROUND ignore
adb shell cmd appops set com.google.android.inputmethod.latin RECORD_AUDIO ignore
adb shell am force-stop com.google.android.inputmethod.latin
```

---

### Etapa 5: Eliminar Espiões de IA e Telemetria Oculta da Google
Estes serviços ficam em segundo plano monitorando sua tela e lendo a área de transferência:

```bash
# Android System Intelligence (Lia clipboard e textos de tela)
adb shell pm clear com.google.android.as && adb shell pm disable-user --user 0 com.google.android.as
adb shell pm clear com.google.android.as.oss && adb shell pm disable-user --user 0 com.google.android.as.oss

# IA Core e Gemini
adb shell pm clear com.google.android.aicore && adb shell pm disable-user --user 0 com.google.android.aicore
adb shell pm clear com.google.android.apps.bard && adb shell pm disable-user --user 0 com.google.android.apps.bard

# Dados de Anúncios e Privacy Sandbox
adb shell pm clear com.google.android.odad && adb shell pm disable-user --user 0 com.google.android.odad
adb shell pm suspend com.google.android.sdksandbox

# Linha do Tempo / Histórico de Localização Google
adb shell pm clear com.google.android.gms.location.history && adb shell pm disable-user --user 0 com.google.android.gms.location.history

# Microfone sempre em espera para "Ok Google"
adb shell pm clear com.android.hotwordenrollment.okgoogle && adb shell pm disable-user --user 0 com.android.hotwordenrollment.okgoogle
adb shell pm clear com.android.hotwordenrollment.xgoogle && adb shell pm disable-user --user 0 com.android.hotwordenrollment.xgoogle

# Upload silencioso do seu registro de ligações para a nuvem
adb shell pm clear com.android.calllogbackup && adb shell pm disable-user --user 0 com.android.calllogbackup
adb shell pm clear com.android.wallpaperbackup && adb shell pm disable-user --user 0 com.android.wallpaperbackup
adb shell pm clear com.android.sharedstoragebackup && adb shell pm disable-user --user 0 com.android.sharedstoragebackup

# Desinstalação completa de pacotes em /data/app
adb shell pm uninstall com.google.android.safetycore
adb shell pm uninstall com.google.android.contactkeys
```

---

### Etapa 6: Enjaular o Google Play Services (Sandboxing de Permissões)
Com este bloco de comandos, o Play Services perde qualquer permissão de espionar sua vida, mas continua vivo apenas para validar seus bancos e entregar notificações push:

```bash
# 1. Revogação de permissões padrão via PM
adb shell pm revoke com.google.android.gms android.permission.CAMERA
adb shell pm revoke com.google.android.gms android.permission.RECORD_AUDIO
adb shell pm revoke com.google.android.gms android.permission.READ_CONTACTS
adb shell pm revoke com.google.android.gms android.permission.WRITE_CONTACTS
adb shell pm revoke com.google.android.gms android.permission.READ_CALENDAR
adb shell pm revoke com.google.android.gms android.permission.WRITE_CALENDAR
adb shell pm revoke com.google.android.gms android.permission.READ_CALL_LOG
adb shell pm revoke com.google.android.gms android.permission.WRITE_CALL_LOG
adb shell pm revoke com.google.android.gms android.permission.READ_SMS
adb shell pm revoke com.google.android.gms android.permission.RECEIVE_SMS
adb shell pm revoke com.google.android.gms android.permission.SEND_SMS

# 2. Neutralização de permissões "SYSTEM_FIXED" via AppOps (UID do GMS)
# O Android impede pm revoke em Localização e Atividade Física marcando como SYSTEM_FIXED.
# Para contornar e forçar o envio de dados vazios/nulos sem quebrar os bancos:
GMS_UID=$(adb shell pm dump com.google.android.gms | grep -m 1 'userId=' | grep -oE '[0-9]+')
adb shell cmd appops set --uid $GMS_UID FINE_LOCATION ignore
adb shell cmd appops set --uid $GMS_UID COARSE_LOCATION ignore
adb shell cmd appops set --uid $GMS_UID MONITOR_LOCATION ignore
adb shell cmd appops set --uid $GMS_UID MONITOR_HIGH_POWER_LOCATION ignore
adb shell cmd appops set --uid $GMS_UID ACTIVITY_RECOGNITION ignore
adb shell cmd appops set --uid $GMS_UID BODY_SENSORS ignore
```

---

### Etapa 7: Encerrar Perfis Fantasmas Secundários (+420 MB de RAM)
Mesmo desativando a Pasta Segura no seu perfil principal, o Android mantém os perfis secundários rodando um segundo Play Services duplicado em segundo plano:

```bash
# Lista os perfis ativos
adb shell pm list users

# Encerra e remove os perfis fantasmas
adb shell am stop-user -f 11
adb shell pm remove-user 10
```

---

### Etapa 8: Auditoria de Permissões Abusivas (Sistema e Usuário) e Bloatwares "Non-Disable"

Mesmo após o debloat tradicional, diversos aplicativos que continuam no aparelho possuem permissões desproporcionais que violam a privacidade ou gastam bateria. Dividimos a limpeza cirúrgica em duas categorias:

#### 1. Permissões Abusivas em Aplicativos de Sistema (Motorola, Google e AOSP):
Módulos nativos do sistema que vêm de fábrica com acessos invasivos pré-concedidos:

```bash
# Câmera Motorola (com.motorola.camera5) - Geotagging
# Por que revogar: Evita gravar coordenadas de GPS (latitude/longitude) nos metadados EXIF das fotos.
adb shell pm revoke --user 0 com.motorola.camera5 android.permission.ACCESS_COARSE_LOCATION

# Gerenciador Multi-SIM Motorola (com.motorola.msimsettings) - Acesso à Agenda
# Por que revogar: O alternador de chips da Motorola não precisa ler sua agenda inteira de contatos.
adb shell pm revoke --user 0 com.motorola.msimsettings android.permission.READ_CONTACTS

# Google Ext Services (com.google.android.ext.services) - Localização
# Por que revogar: Serviço de sistema do Google com rastreamento contínuo de localização em segundo plano.
adb shell pm revoke --user 0 com.google.android.ext.services android.permission.ACCESS_COARSE_LOCATION

# Gerenciador de Dispositivos Companion (com.android.companiondevicemanager) - Localização e Bluetooth
# Por que revogar: Varre Bluetooth e mantém rastreamento de GPS em tempo real e em segundo plano.
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_FINE_LOCATION
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_COARSE_LOCATION
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_BACKGROUND_LOCATION
adb shell pm disable-user --user 0 com.android.companiondevicemanager

# eSIM Activation Google (com.google.android.euicc) - Câmera
# Por que revogar: Usada apenas uma vez para ler o QR Code da operadora, mas mantinha acesso perpétuo.
adb shell pm revoke --user 0 com.google.android.euicc android.permission.CAMERA
```

#### 2. Permissões Abusivas em Aplicativos de Usuário (Terceiros):
Aplicativos instalados pelo usuário que solicitam acessos que não fazem sentido para seu funcionamento básico:

```bash
# Uber (com.ubercab) - Microfone Permanente
# Por que revogar: Impede que o app de transporte tenha acesso contínuo ao seu microfone 24/7.
adb shell pm revoke --user 0 com.ubercab android.permission.RECORD_AUDIO

# 99 Táxi (com.taxis99) - Agenda de Contatos e Câmera
# Por que revogar: A 99 não precisa ler todos os seus contatos nem acessar a câmera para chamar um carro.
adb shell pm revoke --user 0 com.taxis99 android.permission.READ_CONTACTS
adb shell pm revoke --user 0 com.taxis99 android.permission.CAMERA

# Minha Unifique (com.minhaunifique.unifique) - Localização
# Por que revogar: Aplicativo de consulta de fatura/banda larga não precisa das suas coordenadas GPS.
adb shell pm revoke --user 0 com.minhaunifique.unifique android.permission.ACCESS_COARSE_LOCATION

# Navegador Brave (com.brave.browser) - Localização do SO
# Por que revogar: Evita vazamento global de GPS; o navegador deve solicitar apenas nos sites necessários.
adb shell pm revoke --user 0 com.brave.browser android.permission.ACCESS_COARSE_LOCATION

# AJ Fans (br.com.ajfans) - Localização e Wake Locks
# Por que revogar: Contém o SDK Salesforce Marketing Cloud, que acordava a CPU para enviar telemetria.
adb shell pm revoke --user 0 br.com.ajfans android.permission.ACCESS_COARSE_LOCATION
adb shell cmd appops set br.com.ajfans RUN_IN_BACKGROUND ignore
adb shell cmd appops set br.com.ajfans WAKE_LOCK ignore

# BariLife (br.org.app.barilife) - Varredura de Rede Wi-Fi Local (Android 15)
# Por que revogar: Impede o app de escanear outros computadores e TVs na mesma rede doméstica.
adb shell pm revoke --user 0 br.org.app.barilife android.permission.ACCESS_LOCAL_NETWORK
```

#### 3. Paralisar Bloatwares Protegidos como "Non-Disable":
Fabricantes e operadoras protegem certos rastreadores contra o comando `pm disable` (`Failure: package is non-disable`). Paralisamos esses apps impedindo que executem em segundo plano, acordem a CPU ou acessem a rede:

```bash
NON_DISABLE_PKGS=(
    "com.payjoy.access"                  # Rastreamento/trava de financiamento
    "com.amazon.appmanager"              # Instalador da Amazon
    "com.motorola.ccc.devicemanagement"  # Telemetria 3C com GPS
    "com.motorola.paks.notification"     # Notificações de operadora/crédito
    "com.motorola.installer"             # Instalador silencioso em segundo plano
    "com.google.android.sdksandbox"      # Privacy Sandbox Google AdServices
    "com.motorola.ccc.ota"               # Daemon de atualizações OTA da Motorola
)

for pkg in "${NON_DISABLE_PKGS[@]}"; do
    UID=$(adb shell dumpsys package "$pkg" | grep -m 1 'appId=' | grep -oE '[0-9]+')
    if [ -n "$UID" ]; then
        adb shell cmd appops set --uid "$UID" RUN_IN_BACKGROUND ignore
        adb shell cmd appops set --uid "$UID" RUN_ANY_IN_BACKGROUND ignore
        adb shell cmd appops set --uid "$UID" WAKE_LOCK ignore
        adb shell cmd appops set --uid "$UID" START_FOREGROUND ignore
        adb shell cmd appops set --uid "$UID" COARSE_LOCATION ignore
        adb shell cmd appops set --uid "$UID" FINE_LOCATION ignore
        adb shell cmd netpolicy add restrict-background-blacklist "$UID"
    fi
done
```

---

### Etapa 9: Bloqueio de Telemetria no Nível de DNS (NextDNS API)

Mesmo com os bloatwares congelados e permissões revogadas, alguns módulos de sistema podem tentar resolver domínios na internet. Para neutralizar isso de forma definitiva antes que os pacotes saiam do aparelho, integramos o **NextDNS**:

```bash
# 1. Configurar o DNS Privado diretamente no celular via ADB:
adb shell settings put global private_dns_mode hostname
adb shell settings put global private_dns_specifier "SEU_ID.dns.nextdns.io"

# 2. Ativar Listas de Bloqueio Recomendadas via API:
# OISD, HaGeZi Multi PRO, EasyPrivacy e Fanboy Annoyances
curl -X POST -H "X-Api-Key: SUA_API_KEY" -H "Content-Type: application/json" \
  -d '{"id":"oisd"}' https://api.nextdns.io/profiles/SEU_ID/privacy/blocklists

curl -X POST -H "X-Api-Key: SUA_API_KEY" -H "Content-Type: application/json" \
  -d '{"id":"easyprivacy"}' https://api.nextdns.io/profiles/SEU_ID/privacy/blocklists

# 3. Adicionar Domínios de Telemetria Motorola/Lenovo/Adwares na Denylist via API:
# Bloqueia checkin.motorola.com, telemetry.motorola.com, payjoy.com, inmobi.com, glance.in, etc.
TELEMETRY_DOMAINS=(
    "telemetry.motorola.com"
    "checkin.motorola.com"
    "blur.motorola.com"
    "blur.com"
    "payjoy.com"
    "lenovomm.com"
    "digitalturbine.com"
    "inmobi.com"
    "glance.in"
    "taboola.com"
    "ironsrc.com"
    "google-analytics.com"
    "crashlytics.com"
)

for domain in "${TELEMETRY_DOMAINS[@]}"; do
    curl -s -X POST -H "X-Api-Key: SUA_API_KEY" -H "Content-Type: application/json" \
      -d "{\"id\":\"$domain\",\"active\":true}" https://api.nextdns.io/profiles/SEU_ID/denylist
done
```

---

### Etapa 8: Purgar Atualizações em `/data/app` (+4 GB de Armazenamento Livres)
Quando um app de sistema é atualizado pela Play Store, a atualização fica gravada em `/data/app/`. Ao desativar o app, a atualização continua ocupando espaço valioso.

Ao executar `pm uninstall` no pacote do sistema, o Android **apaga a atualização física de 400 MB da memória interna** e volta ao stub de fábrica congelado:

```bash
# Exemplo para alguns pacotes pesados:
adb shell pm uninstall com.android.chrome
adb shell pm uninstall com.google.android.googlequicksearchbox
adb shell pm uninstall com.google.android.youtube
adb shell pm uninstall com.google.android.apps.photos
adb shell pm uninstall com.google.android.apps.maps
adb shell pm uninstall com.google.android.gm
adb shell pm uninstall com.motorola.smartfeed
adb shell pm uninstall com.motorola.mobiledesktop

# (O script debloat.sh faz isso automaticamente em todos os 48 pacotes!)
```

---

## 📱 Ecossistema de Substituição Recomendado (FOSS)

Todos os aplicativos abaixo são gratuitos, de código aberto, sem anúncios e com foco estrito em privacidade:

| Função | App Recomendado | Onde Baixar | Observações |
| :--- | :--- | :--- | :--- |
| **Launcher** | **Lawnchair 14** ou **Neo Launcher** | F-Droid / GitHub | Visual Pixel moderno, Material You fluido. |
| **Teclado** | **FUTO Keyboard** ou **HeliBoard** | F-Droid / GitHub | Digitação por voz por IA 100% offline no celular. |
| **Telefone** | **Fossify Phone** | F-Droid | Gravação de chamadas local e bloqueio de SPAM. |
| **SMS** | **Fossify Messages** | F-Droid | Leve, limpo e com backup criptografado. |
| **Arquivos** | **Material Files** | F-Droid | **Integra com o Shizuku** para destravar `/Android/data`. |
| **Áudio / Dolby**| **Wavelet** | Aurora Store | Ative com `pm grant com.pittvandewitt.wavelet android.permission.DUMP`. |
| **Navegador** | **Brave Browser** ou **Mull** | F-Droid / Aurora | Bloqueio nativo de rastreadores e anúncios. |
| **Loja de Apps** | **Aurora Store** + **F-Droid** | F-Droid | Baixa apps da Google Play de forma anônima. |
| **Mapas** | **Organic Maps** | F-Droid | Mapas offline rápidos baseados em OpenStreetMap. |
| **Calculadora** | **OpenCalculator** | F-Droid | Histórico completo de cálculos e design limpo. |
| **Relógio** | **Fossify Clock** | F-Droid | Alarmes e cronômetro sem rastreadores. |

---

## ⚡ Como Usar Este Repositório com Sua IA Favorita

Se você usa **ChatGPT, Claude, Gemini, Antigravity, Cursor ou Aider**, você não precisa digitar nenhum comando manualmente:

1. Abra o arquivo [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).
2. Copie o prompt completo.
3. Cole na sua IA com o celular conectado ao computador via ADB.
4. A IA fará a varredura do seu aparelho, listará os pacotes e executará a limpeza com total segurança!

---

## 🔄 Como Reverter Qualquer Aplicativo

Se no futuro você quiser reativar algum app específico (exemplo: Android Auto ou Ready For):

```bash
# Reativação individual:
adb shell pm enable <nome_do_pacote>

# Exemplo:
adb shell pm enable com.google.android.projection.gearhead

# Ou use o script de restauração:
./scripts/restore.sh com.motorola.mobiledesktop
```

---

## 📄 Licença
Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.
Desenvolvido e mantido por [Luís Martins](https://github.com/luisfvmartins).
