# 📱 Clean My Android

[![Android 14/15](https://img.shields.io/badge/Android-14%20%7C%2015-3DDC84?logo=android&logoColor=white)](https://android.com)
[![Root: NOT Required](https://img.shields.io/badge/Root-NOT%20Required-success)](https://developer.android.com)
[![Tools: ADB & Shizuku](https://img.shields.io/badge/Tools-ADB%20%7C%20Shizuku-blue)](https://developer.android.com)
[![Validated on Motorola](https://img.shields.io/badge/Tested%20on-Motorola%20Hello%20UI-001435?logo=motorola&logoColor=white)](https://motorola.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> Inspirado na filosofia do projeto [**CleanMyTV**](https://github.com/timothywei/CleanMyTV): **zero lixo visual, zero telemetria invasiva, zero anúncios de fábrica e desempenho máximo**, mantendo **100% da compatibilidade com aplicativos bancários e notificações push**, tudo sem root.

Testado e homologado no **Motorola Edge 60 Pro (`cybert_g_sys`) com Hello UI (Android 14/15)**, adaptável para qualquer smartphone Android moderno.

---

## 📑 Sumário

- [Por que este projeto existe?](#-por-que-este-projeto-existe)
- [Resultados Comprovados em Laboratório](#-resultados-comprovados-em-laboratório)
- [A Arquitetura de Defesa em 4 Camadas](#-a-arquitetura-de-defesa-em-4-camadas)
- [Início Rápido (Quick Start)](#-início-rápido-quick-start)
- [Passo a Passo Detalhado (Manual)](#-passo-a-passo-detalhado-manual)
  - [1. Conexão ADB (Cabo ou Wi-Fi)](#1-conexão-adb-cabo-ou-wi-fi)
  - [2. Adwares e Instaladores Fantasmas](#2-adwares-e-instaladores-fantasmas)
  - [3. Bloatwares de Operadoras Estrangeiras](#3-bloatwares-de-operadoras-estrangeiras)
  - [4. Purgar Atualizações em `/data/app` (+4 GB livres)](#4-purgar-atualizações-em-dataapp-4-gb-livres)
  - [5. De-Google Inteligente (Substituição por FOSS)](#5-de-google-inteligente-substituição-por-foss)
  - [6. Espiões de IA e Telemetria Oculta](#6-espiões-de-ia-e-telemetria-oculta)
  - [7. Sandboxing do Google Play Services](#7-sandboxing-do-google-play-services)
  - [8. Encerramento de Perfis Fantasmas](#8-encerramento-de-perfis-fantasmas)
  - [9. Auditoria de Permissões Abusivas (Sistema e Usuário)](#9-auditoria-de-permissões-abusivas-sistema-e-usuário)
  - [10. Paralisar Bloatwares Protegidos (`non-disable`)](#10-paralisar-bloatwares-protegidos-non-disable)
  - [11. Bloqueio de Telemetria no Nível de DNS (NextDNS API)](#11-bloqueio-de-telemetria-no-nível-de-dns-nextdns-api)
- [Ecossistema FOSS Recomendado](#-ecossistema-foss-recomendado)
- [Como Reverter Qualquer Alteração (Rollback)](#-como-reverter-qualquer-alteração-rollback)
- [Licença](#-licença)

---

## 🎯 Por que este projeto existe?

Aparelhos modernos saem de fábrica repletos de serviços desnecessários:
1. **Adwares e Bloatwares Ocultos:** Módulos como Glance, Taboola, InMobi e Digital Turbine vêm embutidos na ROM, baixando joguinhos silenciosamente, exibindo propagandas na tela de bloqueio e consumindo memória RAM e bateria.
2. **Telemetria Agressiva:** A fabricante e o Google monitoram continuamente localização, clipboard, dados de uso e atividade física.
3. **Bloatwares Travados de Fábrica (`non-disable`):** Pacotes como PayJoy Access e Amazon App Manager vêm marcados como imutáveis no firmware, impedindo a desativação comum via `pm disable`.
4. **O Mito do MicroG em ROM Stock:** Desinstalar o Google Play Services ou forçar o MicroG em uma ROM original bloqueia a verificação do **Play Integrity**, impedindo o funcionamento de aplicativos de banco brasileiros (*Caixa, FGTS, PicPay, Mercado Pago, Nubank*).

O **Clean My Android** resolve tudo isso: neutraliza o bloatware, isola o Google em uma jaula de leitura nula e mantém seus bancos e notificações push 100% operacionais.

---

## 📊 Resultados Comprovados em Laboratório

Métricas reais obtidas no Motorola Edge 60 Pro (12 GB RAM / 256 GB Armazenamento):

| Métrica | Antes do Clean My Android | Depois do Clean My Android | Ganho Real |
| :--- | :--- | :--- | :--- |
| **Pacotes Inúteis / Bloatware** | ~440 pacotes ativos | **244 pacotes congelados/removidos** | Sistema 100% limpo |
| **Memória RAM Livre** | ~4.5 GB livres | **~7.2 GB livres** | **+2.7 GB de RAM livre** |
| **Espaço de Armazenamento** | 193 GB livres | **197 GB a 200 GB livres** | **+4 GB a +7 GB recuperados** |
| **Anúncios no Sistema** | Ativos (Glance, Taboola, InMobi) | **ZERO anúncios** | Telas e launcher limpos |
| **Temperatura em Espera** | 37°C a 40°C | **33.0°C** | Aparelho frio e estável |
| **Apps de Banco (Caixa, Nubank, PicPay)** | Funcionais | **100% Funcionais** | Play Integrity intacto |
| **Privacidade** | Telemetria contínua | **Google Play Services enjaulado** | Zero acesso a GPS/Mic |

---

### 2. Motorola Moto G54 5G (`XT2343-1` / `cancunf` / Android 15)

A auditoria do Moto G54 está documentada em [`docs/AUDITORIA_MOTO_G54_5G.md`](docs/AUDITORIA_MOTO_G54_5G.md). O inventário público contém os componentes de sistema; aplicativos instalados pelo usuário e dados de rede foram omitidos por privacidade.

**Importante:** `data/moto_g54_disabled_packages.txt` é um registro do estado encontrado durante a coleta, não uma lista de recomendações nem uma lista para execução em lote. A presença de `FLAG_PERSISTENT` também não prova, isoladamente, que um pacote seja telemetria ou que possa ser removido.

## 🛡️ A Arquitetura de Defesa em 4 Camadas

```
+-------------------------------------------------------------------------+
| [Camada 1: Debloat em Massa]                                            |
| 244 pacotes inúteis congelados com "pm disable-user --user 0"           |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 2: Purgador de Armazenamento]                                   |
| Purgas físicas de APKs de atualização em /data/app (+4 GB livres)       |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 3: Sandboxing de Permissões & AppOps por UID]                   |
| - GPS, Sensores e Atividade Física do GMS forçados a retornar nulo/vazio|
| - Bloatwares "non-disable" (PayJoy, Amazon) paralisados via AppOps      |
+-------------------------------------------------------------------------+
                                    |
+-------------------------------------------------------------------------+
| [Camada 4: Blindagem de Rede & DNS]                                     |
| - Blacklist de rede em segundo plano no kernel Android (netpolicy)      |
| - NextDNS bloqueando +450.000 domínios e 51 hosts de telemetria na nuvem|
+-------------------------------------------------------------------------+
```

---

## ⚡ Início Rápido (Quick Start)

### Opção A: Auditoria e desativação individual via ADB
O script começa em modo somente leitura. Ele identifica o aparelho e mostra o estado atual, sem alterar configurações. Para desativar um único pacote no Moto G54, após auditoria e decisão consciente, use:

```bash
./scripts/debloat.sh --apply nome.do.pacote
```

O script exige confirmação digitada, aceita apenas um pacote por execução e bloqueia componentes essenciais. Não apaga dados, não desinstala pacotes, não altera AppOps e não remove perfis. Para outros modelos, use o script apenas para inspeção até existir uma lista específica validada.

### Opção B: Execução Assistida por IA (ChatGPT, Claude, Gemini, Antigravity)
1. Abra o arquivo [**`AI_INSTRUCTIONS.md`**](AI_INSTRUCTIONS.md).
2. Copie o prompt mestre e cole na sua IA de preferência com o celular conectado via ADB/Shizuku.
3. A IA fará o diagnóstico, classificará os pacotes e apresentará riscos e reversões. Nenhuma alteração deve ocorrer sem autorização explícita, pacote por pacote ou por grupo claramente delimitado.

---

## 📖 Passo a Passo Detalhado (Manual)

> **Regra de segurança:** os comandos abaixo são referências para análise, não uma sequência para execução em lote. Confirme modelo, pacote, dependências e função. Não use `pm clear`, remoção de perfis ou desinstalação de componentes persistentes como etapas automáticas.

### 1. Conexão ADB (Cabo ou Wi-Fi)

1. Ative as **Opções do desenvolvedor** tocando 7 vezes em *Configurar > Sobre o telefone > Número da versão*.
2. Em *Opções do desenvolvedor*, ative a **Depuração USB** (se usar cabo) ou **Depuração sem fio** (Wi-Fi).
3. Se usar Wi-Fi (Android 11+):
   ```bash
   adb pair 192.168.1.X:PORTA_POPUP CODIGO_PIN
   adb connect 192.168.1.X:PORTA_PRINCIPAL
   adb devices -l
   ```

---

### 2. Adwares e Instaladores Fantasmas
Elimina os serviços que instalam apps patrocinados e exibem propagandas:

```bash
# Digital Turbine (DT Ignite) - Instalador fantasma de patrocinados
adb shell pm disable-user --user 0 com.dti.motorola
adb shell pm disable-user --user 0 com.dti.amx

# IronSource Aura - Anúncios da operadora e recomendações
adb shell pm disable-user --user 0 com.aura.oobe.motorola
adb shell pm disable-user --user 0 com.aura.oobe.vodafone
adb shell pm disable-user --user 0 com.orange.aura.oobe
adb shell pm disable-user --user 0 com.ironsource.appcloud.oobe.hutchison

# Glance Lockscreen - Anúncios e vídeos na tela de bloqueio
adb shell pm disable-user --user 0 com.glance.lockscreenM

# Taboola MIP - Rede global de clickbait embutida na ROM
adb shell pm disable-user --user 0 com.taboola.mip

# InMobi Weather - Anúncios disfarçados de previsão do tempo
adb shell pm disable-user --user 0 com.inmobi.weather

# Meta / Facebook - Telemetria contínua
adb shell pm disable-user --user 0 com.facebook.appmanager
adb shell pm disable-user --user 0 com.facebook.services
adb shell pm disable-user --user 0 com.facebook.system

# Lojas parceiras desnecessárias
adb shell pm disable-user --user 0 com.motorola.brapps
adb shell pm disable-user --user 0 com.indus.appstore
```

---

### 3. Bloatwares de Operadoras Estrangeiras
Módulos inúteis residuais em aparelhos vendidos no Brasil:

```bash
adb shell pm disable-user --user 0 com.motorola.vzw.pco.extensions.pcoreceiver
adb shell pm disable-user --user 0 com.motorola.attvowifi
adb shell pm disable-user --user 0 com.mediatek.op12.ims
adb shell pm disable-user --user 0 com.oem.euiccpartnerapp
adb shell pm disable-user --user 0 com.google.android.wfcactivation
adb shell pm disable-user --user 0 com.android.carrierdefaultapp

# Fim definitivo dos pop-ups de horóscopo da operadora (SIM Toolkit)
adb shell pm disable-user --user 0 com.android.stk
adb shell pm disable-user --user 0 com.android.simappdialog
```

---

### 4. Armazenamento e atualizações de aplicativos

Não use `pm uninstall` como método genérico para liberar espaço em aplicativos de sistema. O comportamento depende do tipo de pacote, usuário e estado da atualização. Primeiro meça o armazenamento e identifique o caminho do APK; não remova atualizações nem dados automaticamente. O comando `pm clear` apaga os dados do aplicativo e não deve fazer parte de rotinas de debloat.

### 5. De-Google Inteligente (Substituição por FOSS)
Antes de desativar os apps abaixo, instale os substitutos recomendados via **F-Droid** ou **Aurora Store**:

```bash
# Navegador, Loja e Multimídia
adb shell pm disable-user --user 0 com.android.chrome
adb shell pm disable-user --user 0 com.android.vending
adb shell pm disable-user --user 0 com.google.android.youtube
adb shell pm disable-user --user 0 com.google.android.apps.youtube.music
adb shell pm disable-user --user 0 com.google.android.videos

# Comunicação e Contatos
adb shell pm disable-user --user 0 com.google.android.dialer
adb shell pm disable-user --user 0 com.google.android.apps.messaging
adb shell pm disable-user --user 0 com.google.android.contacts
adb shell pm disable-user --user 0 com.google.android.calendar
adb shell pm disable-user --user 0 com.google.android.gm
adb shell pm disable-user --user 0 com.google.android.apps.tachyon

# Utilitários e Busca
adb shell pm disable-user --user 0 com.google.android.googlequicksearchbox
adb shell pm disable-user --user 0 com.google.android.apps.maps
adb shell pm disable-user --user 0 com.google.android.apps.docs
adb shell pm disable-user --user 0 com.google.android.apps.photos
adb shell pm disable-user --user 0 com.google.android.apps.nbu.files
adb shell pm disable-user --user 0 com.google.android.calculator
adb shell pm disable-user --user 0 com.google.android.deskclock
```

#### Para o Teclado (Gboard):
Após instalar o **FUTO Keyboard** ou **HeliBoard**:
```bash
adb shell ime disable com.google.android.inputmethod.latin/com.android.inputmethod.latin.LatinIME
adb shell cmd appops set com.google.android.inputmethod.latin RUN_IN_BACKGROUND ignore
adb shell am force-stop com.google.android.inputmethod.latin
```

---

### 6. Espiões de IA e Telemetria Oculta
Serviços que monitoram tela, digitação e clipboard:

```bash
# Android System Intelligence
adb shell pm disable-user --user 0 com.google.android.as
adb shell pm disable-user --user 0 com.google.android.as.oss

# AI Core e Gemini
adb shell pm disable-user --user 0 com.google.android.aicore
adb shell pm disable-user --user 0 com.google.android.apps.bard

# Dados de Anúncios e Privacy Sandbox
adb shell pm disable-user --user 0 com.google.android.odad

# Linha do Tempo / Histórico de Localização Google
adb shell pm disable-user --user 0 com.google.android.gms.location.history

# Microfone sempre ouvindo ("Ok Google")
adb shell pm disable-user --user 0 com.android.hotwordenrollment.okgoogle
adb shell pm disable-user --user 0 com.android.hotwordenrollment.xgoogle
```

---

### 7. Sandboxing do Google Play Services
O Play Services é mantido **vivo exclusivamente para validar aplicativos de banco e entregar notificações push**, revogando todo o acesso a hardware e sensores:

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
# O Android protege Localização e Atividade Física contra o pm revoke comum.
# Para contornar e forçar o retorno de dados nulos/vazios sem quebrar os bancos:
GMS_UID=$(adb shell pm dump com.google.android.gms | grep -m 1 'userId=' | grep -oE '[0-9]+')
# AppOps por UID omitido: mapear todos os pacotes que compartilham o UID antes de qualquer alteração.
# AppOps por UID omitido: mapear todos os pacotes que compartilham o UID antes de qualquer alteração.
# AppOps por UID omitido: mapear todos os pacotes que compartilham o UID antes de qualquer alteração.
# AppOps por UID omitido: mapear todos os pacotes que compartilham o UID antes de qualquer alteração.
# AppOps por UID omitido: mapear todos os pacotes que compartilham o UID antes de qualquer alteração.
# AppOps por UID omitido: mapear todos os pacotes que compartilham o UID antes de qualquer alteração.
```

---

### 8. Inspeção de usuários e perfis Android

Use `adb shell pm list users` apenas para inventariar perfis. Não execute `am stop-user` ou `pm remove-user` automaticamente. Perfis de trabalho, usuários secundários e pastas seguras podem conter dados e funções legítimas; qualquer remoção exige identificação, backup e autorização específica.

### 9. Auditoria de Permissões Abusivas (Sistema e Usuário)

#### A. Aplicativos de Sistema (Motorola / Google / AOSP):
```bash
# Câmera Motorola (com.motorola.camera5) - Geotagging
# Evita gravar coordenadas de GPS (latitude/longitude) nos metadados EXIF das fotos
adb shell pm revoke --user 0 com.motorola.camera5 android.permission.ACCESS_COARSE_LOCATION

# Gerenciador Multi-SIM Motorola (com.motorola.msimsettings) - Acesso à Agenda
adb shell pm revoke --user 0 com.motorola.msimsettings android.permission.READ_CONTACTS

# Google Ext Services (com.google.android.ext.services) - Localização
adb shell pm revoke --user 0 com.google.android.ext.services android.permission.ACCESS_COARSE_LOCATION

# Companion Device Manager (com.android.companiondevicemanager) - Localização e Bluetooth
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_FINE_LOCATION
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_COARSE_LOCATION
adb shell pm revoke --user 0 com.android.companiondevicemanager android.permission.ACCESS_BACKGROUND_LOCATION
adb shell pm disable-user --user 0 com.android.companiondevicemanager

# eSIM Activation Google (com.google.android.euicc) - Câmera
adb shell pm revoke --user 0 com.google.android.euicc android.permission.CAMERA
```

#### B. Aplicativos de Usuário (Terceiros):
```bash
# Uber (com.ubercab) - Microfone Permanente
adb shell pm revoke --user 0 com.ubercab android.permission.RECORD_AUDIO

# 99 Táxi (com.taxis99) - Agenda de Contatos e Câmera
adb shell pm revoke --user 0 com.taxis99 android.permission.READ_CONTACTS
adb shell pm revoke --user 0 com.taxis99 android.permission.CAMERA

# Minha Unifique (com.minhaunifique.unifique) - Localização
adb shell pm revoke --user 0 com.minhaunifique.unifique android.permission.ACCESS_COARSE_LOCATION

# Navegador Brave (com.brave.browser) - Localização do SO
adb shell pm revoke --user 0 com.brave.browser android.permission.ACCESS_COARSE_LOCATION

# AJ Fans (br.com.ajfans) - Localização e Wake Locks do Salesforce
adb shell pm revoke --user 0 br.com.ajfans android.permission.ACCESS_COARSE_LOCATION
adb shell cmd appops set br.com.ajfans RUN_IN_BACKGROUND ignore
adb shell cmd appops set br.com.ajfans WAKE_LOCK ignore

# BariLife (br.org.app.barilife) - Varredura de Rede Wi-Fi Local (Android 15)
adb shell pm revoke --user 0 br.org.app.barilife android.permission.ACCESS_LOCAL_NETWORK
```

---

### 10. Pacotes protegidos e AppOps

Não tente contornar a proteção `non-disable` por UID ou aplicar AppOps em lote. Um UID pode ser compartilhado por vários pacotes e serviços. Registre o UID, mapeie todos os pacotes associados, identifique as dependências e avalie cada operação individualmente. Não altere AppOps sem autorização específica.

### 11. Bloqueio de Telemetria no Nível de DNS (NextDNS API)

Para fechar o cerco e garantir que nenhum módulo tente enviar dados para servidores remotos, integramos o **NextDNS**:

```bash
# 1. Configurar o DNS Privado no celular via ADB:
adb shell settings put global private_dns_mode hostname
adb shell settings put global private_dns_specifier "SEU_ID.dns.nextdns.io"

# 2. Ativar Listas de Bloqueio Recomendadas via API:
curl -s -X POST -H "X-Api-Key: SUA_API_KEY" -H "Content-Type: application/json" \
  -d '{"id":"oisd"}' https://api.nextdns.io/profiles/SEU_ID/privacy/blocklists

curl -s -X POST -H "X-Api-Key: SUA_API_KEY" -H "Content-Type: application/json" \
  -d '{"id":"easyprivacy"}' https://api.nextdns.io/profiles/SEU_ID/privacy/blocklists

# 3. Adicionar Domínios de Telemetria Motorola/Lenovo/PayJoy na Denylist:
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

## 📱 Ecossistema FOSS Recomendado

Substitutos de código aberto, sem anúncios e com foco estrito em privacidade:

| Função | App Recomendado | Onde Baixar | Observações |
| :--- | :--- | :--- | :--- |
| **Launcher** | **Lawnchair 14** ou **Neo Launcher** | F-Droid / GitHub | Visual Pixel moderno, Material You fluido. |
| **Teclado** | **FUTO Keyboard** ou **HeliBoard** | F-Droid / GitHub | Digitação por voz por IA 100% offline no celular. |
| **Telefone** | **Fossify Phone** | F-Droid | Gravação de chamadas local e bloqueio de SPAM. |
| **SMS** | **Fossify Messages** | F-Droid | Leve, limpo e com backup criptografado. |
| **Arquivos** | **Material Files** | F-Droid | **Integra com o Shizuku** para destravar `/Android/data`. |
| **Áudio / Equalizador**| **Wavelet** | Aurora Store | Conceda: `pm grant com.pittvandewitt.wavelet android.permission.DUMP`. |
| **Navegador** | **Brave Browser** ou **Mull** | F-Droid / Aurora | Bloqueio nativo de rastreadores e anúncios. |
| **Loja de Apps** | **Aurora Store** + **F-Droid** | F-Droid | Baixa apps da Google Play de forma anônima. |
| **Mapas & GPS** | **Organic Maps** | F-Droid | Mapas offline rápidos baseados em OpenStreetMap. |
| **Calculadora** | **OpenCalculator** | F-Droid | Histórico de cálculos sem internet. |
| **Relógio** | **Fossify Clock** | F-Droid | Alarmes e cronômetro limpos. |

---

## 🔄 Como Reverter Qualquer Alteração (Rollback)

Nenhuma alteração é destrutiva ou permanente. Se quiser reativar qualquer aplicativo:

```bash
# Reativação individual:
adb shell pm enable <nome_do_pacote>

# Exemplo:
adb shell pm enable com.google.android.projection.gearhead

# Ou use o script de restauração em massa:
./scripts/restore.sh --all
```

---


## 🧾 Auditoria individual e contribuições por Pull Request

Cada colaborador pode documentar seu próprio dispositivo com um relatório antes/depois. Para propor a inclusão desse material no projeto, o fluxo recomendado é **fork → branch → Pull Request (PR)**.

1. Crie seu [fork do Clean My Android](https://github.com/luisfvmartins/clean-my-android/fork) (necessário para colaboradores sem acesso de escrita).
2. Leia o [guia de auditoria individual](docs/USER_DEVICE_AUDIT.md).
3. Utilize o [prompt mestre para IA](AI_INSTRUCTIONS.md) para orientar a coleta, análise, otimização e geração do relatório.
4. Salve os resultados em `reports/SEU_DISPOSITIVO/` no seu fork ou mantenha os dados brutos localmente.
5. Revise e sanitize todos os arquivos e evidências.
6. Crie uma branch exclusiva, envie-a ao seu fork e abra um **Pull Request para `luisfvmartins/clean-my-android:main`**.
7. Aguarde a revisão do mantenedor; após o merge, a auditoria será incorporada à coleção oficial em `reports/`, somando-se às contribuições anteriores. O PR poderá ser aceito, receber pedidos de ajustes ou ser rejeitado.

**Privacidade:** forks de repositórios públicos também são públicos por padrão. Não publique IMEI, número de série, MAC, tokens, contas, notificações ou logs brutos. Mantenha evidências completas localmente ou em repositório privado. O Pull Request deve conter apenas material sanitizado e necessário à revisão. Cada contribuição deve acrescentar uma pasta de dispositivo e atualizar o [índice de auditorias](reports/README.md), sem sobrescrever relatórios de outros colaboradores.
## 📄 Licença

Distribuído sob a licença **MIT**. Veja [`LICENSE`](LICENSE) para mais informações.  
Desenvolvido com foco em liberdade, privacidade e engenharia reversa por [**Luís Martins**](https://github.com/luisfvmartins).
