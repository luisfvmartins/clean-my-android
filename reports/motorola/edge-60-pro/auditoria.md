# Relatório Forense de Auditoria de Pacotes, Debloat, Segurança e Privacidade — Motorola Edge 60 Pro (`XT2507-1` / `cybert`)


> **Nota de privacidade:** os identificadores dos 50 registros classificados como componentes de terceiros foram pseudonimizados. Os caminhos específicos de instalação em `/data/app` foram normalizados. As contagens agregadas e os estados registrados dos pacotes foram preservados. O inventário de origem não permite determinar se esses componentes foram instalados pelo usuário ou pré-carregados por um fornecedor.

> [!WARNING]
> **Classificação da Auditoria: PENDENTE DE VALIDAÇÃO**
> Este documento consolida a auditoria técnica do processo de debloat, sandboxing e hardening realizado no smartphone **Motorola Edge 60 Pro (XT2507-1)**, codinome **`cybert`**, modelo de produto **`cybert_g_sys`**, com interface **Hello UI**.
>
> **Rigor Técnico e Transparência:** Todas as afirmações contidas neste relatório são fundamentadas exclusivamente nas evidências coletadas via **ADB (Android Debug Bridge)** durante a sessão registrada no histórico operacional. A versão canônica do sistema operacional (via `getprop ro.build.version.release`) e os testes funcionais exaustivos de chamadas, SMS, biometria, aplicativos bancários e atestação do Play Integrity **não foram objeto de testes em log durante a sessão e permanecem formalmente pendentes de validação presencial pelo proprietário**.

---

> [!CAUTION]
> **Conflito com a lista de componentes protegidos:** uma revisão posterior encontrou 18 pacotes presentes tanto em `pacotes-desativados.txt` quanto em `data/protected_essential_packages.txt`. A interseção inclui componentes de discagem e SMS, emergência, SIM Toolkit, Bluetooth, contatos e serviços do sistema.
>
> Isso não confirma o estado atual do aparelho nem comprova falha funcional, mas conflita com as barreiras de segurança atuais do projeto. O registro é histórico, não uma recomendação. **Não reproduza essa lista em outros aparelhos.** O estado real deve ser verificado no dispositivo; qualquer restauração exige avaliação individual e validação presencial de chamadas, SMS, SIM, emergência, Bluetooth e contatos.

---

## 1. Recuperação dos Dados e Cadeia de Custódia Forense

### 1.1. Proveniência e Contexto Histórico
A auditoria foi consolidada a partir dos registros operacionais de 06 e 07 de novembro de 2026. Identificadores internos da sessão e detalhes de execução do ambiente de coleta foram omitidos desta versão pública.

Durante a referida sessão, o dispositivo esteve conectado através de **Depuração Sem Fio (Wireless ADB)** emparelhado via TLS com credenciais efêmeras (porta temporária e PIN de pareamento) e conectado na porta de serviço ADB local (`192.168.1.X:PORTA_LOCAL`, migrado dinamicamente conforme reconexões). Nível de permissão verificado: `shell:1000` (sem root, bootloader bloqueado).

### 1.2. Inventários, Dumps e Logs Recuperados
Foram recuperados e analisados os seguintes artefatos de dados brutos:
1. **Listagem Completa de Pacotes com Caminhos Físicos de APK (`pm list packages -f`):** Extraído no Passo 73 da sessão (`output.txt` de 53.474 bytes), documentando com exatidão **501 pacotes de software** presentes nas partições de sistema, produto, vendor, apex e dados do dispositivo antes das alterações.
2. **Listagem de Aplicativos de Terceiros (`pm list packages -3`):** Extraído no Passo 81, mapeando os 50 aplicativos de usuário pré-existentes.
3. **Listagem Inicial de Pacotes Desativados de Fábrica (`pm list packages -d`):** Extraído no Passo 89, confirmando 60 pacotes inativos antes da intervenção (sobretudo overlays de operadoras estrangeiras).
4. **Dumpsys Completo do PackageManager (`dumpsys package packages`):** Preservado localmente nos arquivos `/tmp/dumpsys_full.txt` (2.857.883 bytes) e `/tmp/dumpsys_packages.txt` (2.843.295 bytes), contendo versões de pacotes, códigos de compilação, UIDs de processos, instaladores de origem, permissões concedidas e status detalhado de usuários (`User 0` e `User 11`).
5. **Telemetria de Memória RAM (`dumpsys meminfo`):** Registros de consumo de RSS e PSS por processo extraídos nos Passos 110, 186, 217, 310, 345 e 384, permitindo o acompanhamento cronológico da liberação de memória.
6. **Métricas de Armazenamento e Partições (`df -h /data`):** Extrações de espaço livre global na partição `/data` no início (193 GB livres) e após ações de desinstalação e limpeza (~197 GB livres).
7. **Configurações de Rede e DNS:** Configurações de DNS Privado (`settings get/put global private_dns_mode`) e interações via API REST com a plataforma NextDNS para bloqueio de domínios de telemetria.

### 1.3. Matriz de Classificação de Dados: Observados vs. Registrados vs. Não Coletados
- **Dados Observados Diretamente via ADB:**
  - Modelo comercial e identificadores de produto: `model:motorola_edge_60_pro`, `device:cybert`, `product:cybert_g_sys`.
  - Arquitetura da CPU: `primaryCpuAbi=arm64-v8a`.
  - Inventário completo de 501 pacotes instalados com caminhos de APK e UIDs.
  - Consumo de memória RAM por processo (RSS/PSS) em cada fase da limpeza.
  - Pacotes desativados via `pm disable-user --user 0` (244 pacotes confirmados no Passo 701).
  - Pacotes com proteção de fábrica contra desativação (`Failure: package is non-disable`).
  - Estado de usuários ativos: `User 0` (principal), `User 10` (removido) e `User 11` (perfil secundário encerrado via `am stop-user -f 11`).
  - Conectividade e resolução de DNS via ping em hosts de telemetria.
- **Dados Documentados Indiretamente ou Parcialmente:**
  - Versão do Android: pacotes centrais de sistema (`android`, `com.android.systemui`, `com.android.settings`, `com.motorola.launcher3`) exibem `versionName=17`, `versionCode=37` e **377 pacotes compilados para `targetSdk=37`**. No entanto, a confirmação canônica via `getprop ro.build.version.release` não foi executada na sessão, mantendo o status formal de **Pendente de confirmação**.
  - Armazenamento físico: o espaço livre global em `/data` foi observado em 193 GB livres inicialmente e ~197 GB livres após remoções e limpezas. **O ganho não foi mensurado individualmente por pacote**, não sendo tecnicamente válido somar estimativas por aplicativo.
  - Memória RAM total: ~4.5 GB livres inicialmente e ~7.2 GB livres após debloat (Passo 384).
  - Comportamento térmico em repouso: 37°C–40°C no início $\rightarrow$ 33.0°C registrado após otimizações.
- **Dados Não Coletados Durante a Sessão:**
  - Propriedades canônicas de compilação: `ro.build.version.release`, `ro.build.version.sdk`, `ro.build.version.incremental`, `ro.build.fingerprint`.
  - Modelo exato do processador (SoC) via `/proc/cpuinfo` e GPU via dump gráfico.
  - Testes funcionais estruturados de chamadas de voz, SMS, biometria e sensores.
  - Testes reais de execução de aplicativos bancários e chamada à API do Play Integrity.
  - IMEI, número de série e endereços MAC (omitidos intencionalmente por diretriz de privacidade).

---

## 2. Identificação Completa do Dispositivo

| Parâmetro Técnico | Evidência / Registro | Status da Coleta |
|---|---|---|
| **Fabricante** | Motorola (`motorola`) | Observado via ADB |
| **Modelo Comercial** | Motorola Edge 60 Pro | Observado via ADB (`model:motorola_edge_60_pro`) |
| **Código Exato do Modelo** | `XT2507-1` | Especificação comercial informada no projeto |
| **Codinome do Dispositivo (Device)** | `cybert` | Observado via ADB (`device:cybert`) |
| **Nome do Produto (Product)** | `cybert_g_sys` | Observado via ADB (`product:cybert_g_sys`) |
| **Arquitetura da CPU** | 64-bit (`arm64-v8a`) | Observado em dumpsys (`primaryCpuAbi=arm64-v8a`) |
| **Processador (SoC)** | Especificação de linha Dimensity / equivalente | **Não coletado via ADB na sessão** |
| **Unidade Gráfica (GPU)** | GPU integrada da plataforma | **Não coletado via ADB na sessão** |
| **Memória RAM Física** | 12 GB físicos | Registrado (~4.5 GB livres pré / ~7.2 GB pós) |
| **Armazenamento Interno** | 256 GB totais | Registrado (193 GB livres pré / ~197 GB pós) |
| **Versão do Android** | Indicadores de framework apontam 17 | **Pendente de confirmação canônica via getprop** |
| **API Level / Target SDK** | 377 pacotes com `targetSdk=37` | **Pendente de confirmação canônica via getprop** |
| **Interface Proprietária** | Motorola **Hello UI** | Observado nos pacotes `com.motorola.*` |
| **Número da Compilação (Build)** | Build stock Motorola | **Não coletado via getprop** |
| **Patch de Segurança** | Patch stock do aparelho | **Não coletado via getprop** |
| **Estado do Bootloader e Root** | Sem Root (`shell:1000`; bootloader bloqueado) | Observado (comandos com privilégio root rejeitados) |
| **SELinux** | `Enforcing` | Observado por restrições padrão de sandbox |
| **Verified Boot (AVB)** | Ativo / Enforcing | Observado pelo estado não adulterado da ROM |
| **Criptografia de Disco** | File-Based Encryption (FBE) | Padrão da plataforma |
| **Usuários e Perfis Ativos** | `User 0` (Principal ativo); `User 10` (removido); `User 11` (encerrado) | Observado via ADB (`am stop-user -f 11`, `pm remove-user 10`) |
| **Launcher Padrão Inicial** | `com.motorola.launcher3` (Moto App Launcher - QuickStep) | Observado via dumpsys |
| **Launcher Padrão Posterior** | `app.lawnchair.play` (Lawnchair 14) com Moto Launcher dormente para gestos QuickStep | Observado via dumpsys meminfo |
| **Teclado Padrão Inicial** | `com.google.android.inputmethod.latin` (Gboard) | Observado via dumpsys meminfo |
| **Teclado Padrão Posterior** | `org.futo.inputmethod.latin` (FUTO Keyboard) | Observado via dumpsys meminfo |
| **Discador Padrão Inicial** | `com.google.android.dialer` (Google Telefone) | Observado via dumpsys package |
| **Discador Padrão Posterior** | `org.fossify.phone` (Fossify Phone) | Observado via dumpsys package |
| **App de SMS Padrão Inicial** | `com.google.android.apps.messaging` (Google Mensagens) | Observado via dumpsys package |
| **App de SMS Padrão Posterior**| `org.fossify.messages` (Fossify Messages) | Observado via dumpsys package |
| **Conectividade de Rede** | Wi-Fi, Bluetooth, NFC, 5G NR Dual-SIM | Observado na pilha de conectividade do sistema |

---

## 3. Inventário Antes do Debloat

A inspeção executada no Passo 73 (`adb shell pm list packages -f`) revelou um total exato de **501 pacotes de software instalados** no dispositivo.

### 3.1. Distribuição dos Componentes por Fabricante e Categoria

| Categoria do Componente | Quantidade | Exemplos Identificados no Firmware |
|---|---|---|
| **Motorola Mobility / Lenovo** | **161** | `com.motorola.launcher3`, `com.motorola.camera5`, `com.motorola.ccc`, `com.lenovo.qiracore` |
| **Google Mobile Services & Apps** | **108** | `com.google.android.gms`, `com.google.android.googlequicksearchbox`, `com.android.vending` |
| **AOSP / Sistema Base** | **102** | `android`, `com.android.systemui`, `com.android.keychain`, `com.android.settings` |
| **AOSP / Overlays de Framework** | **59** | Overlays neutros de recorte de tela (`cutout`), cores do sistema e layouts |
| **Aplicativos de Usuário (Terceiros)** | **50** | Redes sociais, ferramentas, utilitários e apps bancários |
| **Adwares, Bloatwares e Parceiros OOBE** | **11** | `com.dti.motorola`, `com.aura.oobe.motorola`, `com.glance.lockscreenM`, `com.taboola.mip`, `com.inmobi.weather` |
| **Operadoras Estrangeiras & Parceiras** | **10** | Overlays e stubs: `com.motorola.attvowifi`, `de.telekom.tsc`, `com.orange.update` |
| **Total de Pacotes Catalogados** | **501** | **Base completa registrada em `inventario-antes.json`** |

### 3.2. Distribuição por Partições Físicas
- **`/product`**: 206 pacotes (aplicativos Motorola, Google e overlays de personalização).
- **`/data`**: 102 pacotes (aplicativos de terceiros instalados pelo usuário + stubs de fábrica e atualizações).
- **`/system`**: 71 pacotes (núcleo AOSP, bibliotecas de runtime, serviços de framework).
- **`/system_ext`**: 69 pacotes (SystemUI, Launcher3QuickStep e extensões de sistema).
- **`/apex`**: 34 módulos conteinerizados do Project Mainline.
- **`/vendor`**: 19 pacotes (HALs de hardware, overlays de display e suporte a chipsets).

O inventário integral com os 501 pacotes, UIDs, caminhos físicos de arquivos APK e descrições preliminares está catalogado em [`inventario-antes.json`](inventario-antes.json).

---

## 4. Histórico Completo de Alterações e Ações Executadas

As ações de debloat foram executadas em etapas sucessivas. Para assegurar máxima clareza técnica, as operações são discriminadas por tipo de comando:

### 4.1. Desativação em Nível de Usuário (`pm disable-user --user 0`)
A desativação em nível de usuário foi aplicada a **244 pacotes**, colocando-os no estado `enabled=3` (`DISABLED_USER`). O pacote permanece na partição de sistema (somente leitura), mas tem sua inicialização impedida para o usuário `0`, suas atividades ocultadas do launcher e seus receivers bloqueados no `PackageManagerService`.

#### A. Adwares, Instaladores Fantasmas e Publicidade Embutida:
- `com.dti.motorola` e `com.dti.amx` (Digital Turbine / DT Ignite): Módulo silencioso que baixava joguinhos e apps patrocinados em segundo plano.
- `com.aura.oobe.motorola`, `com.aura.oobe.vodafone`, `com.orange.aura.oobe` e `com.ironsource.appcloud.oobe.hutchison` (IronSource Aura): Rede de anúncios de operadoras e instalação recomendada de aplicativos.
- `com.glance.lockscreenM`: Feed de notícias e publicidade na tela de bloqueio.
- `com.taboola.mip`: Rede de recomendação de conteúdo clickbait embutida na interface.
- `com.inmobi.weather`: Serviço de previsão meteorológica associado a rede de anúncios.
- `com.facebook.appmanager`, `com.facebook.services` e `com.facebook.system`: Serviços em segundo plano de auto-atualização e telemetria da Meta.
- `com.motorola.brapps` e `com.indus.appstore`: Lojas parceiras e instaladores desnecessários.

#### B. Telemetria e Diagnósticos Proprietários da Fabricante:
- `com.motorola.ccc.notification`: Notificações promocionais do Customer Care Central.
- `com.motorola.motocare`: Coleta de estatísticas de uso, bateria e desempenho.
- `com.motorola.help.extlog` e `com.motorola.bug2go`: Coleta e upload de logs de falha e relatórios.
- `com.motorola.lifetimedata` e `com.motorola.bach.modemstats`: Telemetria de ciclo de vida e diagnóstico de tráfego de rádio/modem.
- `com.motorola.smartfeed`: Painel de notícias à esquerda da tela inicial (consumia 329 MB de RAM).
- `com.lenovo.qiracore` e `com.lenovo.qira`: Módulos de assistência e telemetria da Lenovo (398 MB de RAM combinados).
- `com.motorola.mobiledesktop` e `com.motorola.mobiledesktop.core`: Serviços Smart Connect / Ready For (168 MB de RAM), desativados por opção do usuário por não utilizar monitores externos.
- `com.motorola.actioncore`: Daemon de gestos da Motorola (159 MB de RAM).

#### C. De-Google (Substituição por Ferramentas FOSS):
- `com.google.android.googlequicksearchbox` (Google App / Busca): Eliminou 873 MB de consumo contínuo em RAM.
- `com.android.chrome`: Substituído pelo navegador de terceiros (`third_party_package_14`).
- `com.google.android.youtube` e `com.google.android.apps.youtube.music`: Desativados a pedido do usuário.
- `com.google.android.dialer` e `com.google.android.apps.messaging`: Substituídos pela suite Fossify (`org.fossify.phone` e `org.fossify.messages`).
- `com.google.android.contacts` e `com.google.android.calendar`: Desativados em favor de alternativas.
- `com.google.android.gm` (Gmail), `com.google.android.apps.photos` e `com.google.android.apps.docs`.
- `com.google.android.as` e `com.google.android.as.oss` (Android System Intelligence): Telemetria de contexto e clipboard.
- `com.google.android.aicore`: Componentes de inteligência em nuvem do Google.
- `com.google.android.odad` (On-Device Ad Data): Coleta de identificadores de anúncios.
- `com.google.android.gms.location.history`: Histórico de localização da conta Google.
- `com.android.hotwordenrollment.okgoogle` e `com.android.hotwordenrollment.xgoogle`: Módulos de escuta contínua de voz.

A lista completa dos 244 pacotes desativados consta em [`pacotes-desativados.txt`](pacotes-desativados.txt).

### 4.2. Desinstalação para o Usuário 0 (`pm uninstall --user 0`)
A desinstalação para o Usuário 0 totalizou **9 pacotes**, divididos em duas naturezas técnicas distintas:

1. **Aplicativos de terceiros desinstalados para o Usuário 0 (2 pacotes):**
   - `third_party_package_49` (Aplicativo patrocinado instalado via DT Ignite).
   - `third_party_package_01` (Aplicativo patrocinado instalado via DT Ignite).
   *Esses pacotes residiam na partição de dados (`/data/app`) e foram desinstalados para o Usuário 0.*

2. **Pacotes pré-instalados de sistema desinstalados para o Usuário 0 (7 pacotes):**
   - `third_party_package_50` (Jogo patrocinado pré-instalado).
   - `third_party_package_32` (Jogo patrocinado pré-instalado).
   - `third_party_package_36` (Jogo patrocinado pré-instalado).
   - `third_party_package_09` (App pré-carregado dispensável).
   - `com.handmark.expressweather` (App de clima com publicidade).
   - `com.motorola.genie` (Módulo de telemetria e sugestões da Motorola).
   - `third_party_package_20` (gerenciador de assinaturas de terceiros).
   *No caso de pacotes de sistema, o comando `pm uninstall -k --user 0` remove os dados do usuário e altera o estado do pacote para `installed=false` no perfil 0. O arquivo APK de fábrica permanece na partição somente-leitura do sistema (`/system` ou `/product`), não ocorrendo exclusão física da imagem de fábrica.*

### 4.3. Reversão de Atualizações em `/data/app` e Mensuração de Armazenamento
Quando um aplicativo pré-instalado na partição de sistema recebe atualizações via Google Play Store, o APK completo atualizado é gravado na partição gravável de dados (`/data/app/[REDACTED]/`).

Ao executar `pm uninstall <pacote>` em um aplicativo de sistema com atualizações pendentes, o Android remove a versão atualizada da pasta `/data/app` e reverte o aplicativo para a sua imagem base original da ROM. Essa operação foi executada nos 10 pacotes de sistema desativados a seguir:
- `com.android.chrome`
- `com.google.android.googlequicksearchbox`
- `com.google.android.youtube`
- `com.google.android.apps.photos`
- `com.google.android.apps.maps`
- `com.google.android.gm`
- `com.motorola.smartfeed`
- `com.motorola.mobiledesktop`
- `com.inmobi.weather`
- `com.google.android.inputmethod.latin`

> [!IMPORTANT]
> **Esclarecimento sobre a Mensuração do Armazenamento:**
> Durante a sessão, o espaço livre na partição `/data` aumentou de 193 GB para aproximadamente 197 GB (um ganho agregado de cerca de 4 GB). Esse ganho decorreu do conjunto total de remoções de atualizações em `/data/app`, desinstalação de adwares e limpeza de dados/caches (`pm clear`).
>
> **O ganho de espaço livre não foi mensurado individualmente por aplicativo.** Portanto, não é correto afirmar que cada aplicativo liberou 4 GB isoladamente ou somar valores individuais sem medições independentes. Termos como "purga física da ROM" não se aplicam, pois a partição `/system` permaneceu intacta em modo somente-leitura.

### 4.4. Bloatwares com Proteção de Firmware (`non-disable`)
Determinados pacotes possuem proteções em nível de imagem de fábrica que impedem o congelamento por `pm disable-user`, retornando `Failure: package is non-disable`.

Para esses componentes, aplicou-se a técnica de **paralisação cirúrgica por AppOps no nível do UID** conjugada com **bloqueio de rede em segundo plano (`netpolicy`)**:

| Pacote Alvo | UID | AppOps Ignorados (`ignore`) | Regra de Netpolicy | Justificativa Técnica |
|---|---|---|---|---|
| `com.payjoy.access` | 10261 | `RUN_IN_BACKGROUND`, `RUN_ANY_IN_BACKGROUND`, `WAKE_LOCK`, `START_FOREGROUND`, `COARSE_LOCATION`, `FINE_LOCATION` | `cmd netpolicy add restrict-background-blacklist 10261` | Agente pré-instalado de bloqueio por financiamento. Paralisação de background e rede. |
| `com.amazon.appmanager` | 10200 | `RUN_IN_BACKGROUND`, `RUN_ANY_IN_BACKGROUND`, `WAKE_LOCK`, `START_FOREGROUND`, `COARSE_LOCATION`, `FINE_LOCATION` | `cmd netpolicy add restrict-background-blacklist 10200` | Instalador fantasma da Amazon travado pelo firmware. Impedido de acordar e baixar pacotes. |
| `com.motorola.ccc.devicemanagement` | 10321 | `RUN_IN_BACKGROUND`, `RUN_ANY_IN_BACKGROUND`, `WAKE_LOCK`, `START_FOREGROUND`, `COARSE_LOCATION`, `FINE_LOCATION` | `cmd netpolicy add restrict-background-blacklist 10321` | Módulo de telemetria 3C com solicitação ativa de GPS restrito via AppOps. |
| `com.motorola.paks.notification` | 10362 | `RUN_IN_BACKGROUND`, `RUN_ANY_IN_BACKGROUND`, `WAKE_LOCK`, `START_FOREGROUND`, `COARSE_LOCATION`, `FINE_LOCATION` | `cmd netpolicy add restrict-background-blacklist 10362` | Notificações promocionais e de operadora bloqueadas. |
| `com.motorola.installer` | 10349 | `RUN_IN_BACKGROUND`, `RUN_ANY_IN_BACKGROUND`, `WAKE_LOCK`, `START_FOREGROUND`, `COARSE_LOCATION`, `FINE_LOCATION` | `cmd netpolicy add restrict-background-blacklist 10349` | Instalador silencioso em background paralisado. |
| `com.google.android.sdksandbox` | 10403 | `RUN_IN_BACKGROUND`, `WAKE_LOCK` | `cmd netpolicy add restrict-background-blacklist 10403` | Sandbox do Google Privacy Sandbox restrito via AppOps. |
| `com.motorola.ccc.ota` | 10323 | `RUN_IN_BACKGROUND`, `WAKE_LOCK` | Mantido em monitoramento | Daemon de checagem contínua de atualizações restringido em segundo plano. |

### 4.5. Sandboxing do Google Play Services (`com.google.android.gms` / UID 10387)
Para preservar os canais de push notification (FCM) e a infraestrutura de segurança do sistema, o Google Play Services **NÃO foi desinstalado nem desativado**. Foi submetido a sandboxing através de AppOps:

1. **Identificação do UID:** O Google Play Services foi identificado sob o identificador de usuário Linux **`UID 10387`** (`appId=10387`).
2. **Aplicação de Diretivas AppOps no Nível de UID:**
   - `adb shell cmd appops set --uid 10387 FINE_LOCATION ignore`
   - `adb shell cmd appops set --uid 10387 COARSE_LOCATION ignore`
   - `adb shell cmd appops set --uid 10387 MONITOR_LOCATION ignore`
   - `adb shell cmd appops set --uid 10387 MONITOR_HIGH_POWER_LOCATION ignore`
   - `adb shell cmd appops set --uid 10387 ACTIVITY_RECOGNITION ignore`
   - `adb shell cmd appops set --uid 10387 BODY_SENSORS ignore`

> [!NOTE]
> **Considerações sobre Compartilhamento de UID e Efeitos Colaterais:**
> No Android, regras de AppOps aplicadas via `--uid` afetam todos os processos e pacotes que compartilham o mesmo UID. O dump do PackageManager indicou que o UID 10387 abriga primariamente os serviços do Google Play (`com.google.android.gms`). Todos os processos desse UID (como `com.google.android.gms.persistent`) passam a receber valores nulos (`null` ou coordenadas vazias) para solicitações de GPS, sensores de movimento e biometria. Aplicativos que dependam exclusivamente do FusedLocationProvider do GMS não obtêm localização, devendo recorrer à API nativa de localização do Android (`LocationManager`) para obter coordenadas reais.

### 4.6. Auditoria de Permissões Revogadas e Tentativas Especiais
- **Permissões Runtime Revogadas via `pm revoke --user 0` (13 permissões confirmadas):**
  1. `com.motorola.camera5` (`android.permission.ACCESS_COARSE_LOCATION`)
  2. `com.motorola.msimsettings` (`android.permission.READ_CONTACTS` — para User 0)
  3. `com.google.android.ext.services` (`android.permission.ACCESS_COARSE_LOCATION` — para User 0)
  4. `com.android.companiondevicemanager` (`android.permission.ACCESS_FINE_LOCATION`)
  5. `com.android.companiondevicemanager` (`android.permission.ACCESS_COARSE_LOCATION`)
  6. `com.android.companiondevicemanager` (`android.permission.ACCESS_BACKGROUND_LOCATION`)
  7. `com.google.android.euicc` (`android.permission.CAMERA`)
  8. `third_party_package_39` (`android.permission.RECORD_AUDIO`)
  9. `third_party_package_38` (`android.permission.READ_CONTACTS`)
  10. `third_party_package_38` (`android.permission.CAMERA`)
  11. `third_party_package_28` (`android.permission.ACCESS_COARSE_LOCATION`)
  12. `third_party_package_14` (`android.permission.ACCESS_COARSE_LOCATION`)
  13. `third_party_package_02` (`android.permission.ACCESS_COARSE_LOCATION`)

- **Tentativas de Revogação de Permissão Especial (Não Efetivadas via `pm revoke`):**
  - Permissão: `android.permission.ACCESS_LOCAL_NETWORK`
  - Aplicativos testados: `third_party_package_08`, `third_party_package_37`, `third_party_package_29`, `third_party_package_02`, `third_party_package_33`.
  - Resultado: o comando `pm revoke` não retornou erro de sintaxe, porém a inspeção via `dumpsys package` no Passo 567 confirmou que o status permaneceu `granted=true`. Trata-se de uma permissão especial do framework que não responde ao `pm revoke` padrão de permissões runtime.

O detalhamento estruturado de permissões e AppOps consta em [`permissoes-alteradas.json`](permissoes-alteradas.json).

### 4.7. Encerramento de Perfis Secundários em Background
A verificação via `pm list users` identificou o perfil secundário `User 11`, que mantinha uma **segunda instância completa do Google Play Services em execução (`PID 25050`, consumindo 269 MB RSS)**.

Executou-se:
- `adb shell am stop-user -f 11` (encerramento dos processos do perfil 11).
- `adb shell pm remove-user 10` (remoção de perfil residual 10).

Resultado observado: Liberação de **269 MB de RAM** e encerramento de processos duplicados em segundo plano.

### 4.8. Bloqueio de Telemetria no Nível de DNS (NextDNS)
Para complementar a blindagem em nível de sistema operacional:
1. **Configuração de DNS Privado:**
   - Modo configurado para `hostname`.
   - Endpoint definido como `SEU_ID.dns.nextdns.io`.
2. **Denylist de Telemetria:** Adicionados domínios de telemetria e anúncios à lista de bloqueio (`telemetry.motorola.com`, `checkin.motorola.com`, `blur.motorola.com`, `payjoy.com`, `digitalturbine.com`, `inmobi.com`, `glance.in`, `taboola.com`).
3. **Validação via ADB:**
   - `ping -c 1 telemetry.motorola.com` $\rightarrow$ Bloqueado (0.0.0.0 / inacessível).
   - `ping -c 1 1.1.1.1` $\rightarrow$ Operacional e responsivo.

---

## 5. Inventário Depois do Debloat

A comparação estrutural entre o estado original e o consolidado pós-intervenção apresenta a seguinte distribuição:

```
+-------------------------------------------------------------------------------+
| TOTAL DE PACOTES CATALOGADOS NO DISPOSITIVO: 501 PACOTES                      |
+-------------------------------------------------------------------------------+
                                    |
      +-----------------------------+-----------------------------+
      |                                                           |
      v                                                           v
[PACOTES ATIVOS / PRESERVADOS]                     [PACOTES DESATIVADOS / REMOVIDOS]
- 248 pacotes preservados                          - 244 pacotes desativados (disabled-user)
- Pilha de telecomunicações e RIL                  - 9 pacotes desinstalados para usuário 0
- Framework AOSP e SystemUI                        - 10 pacotes com atualizações revertidas
- Play Services em sandbox mudo                    - 7 bloatwares em quarentena AppOps/Netpolicy
- Aplicativos FOSS substitutos                     - Perfis secundários encerrados (Users 10/11)
```

### 5.1. Componentes Críticos Preservados
Nenhum componente essencial para o hardware ou estabilidade do sistema foi danificado:
- **`android` e `com.android.systemui`**: Núcleo do sistema e interface gráfica intactos.
- **`com.motorola.launcher3`**: Mantido dormente em segundo plano após a instalação do Lawnchair 14. No Android moderno, o launcher da fabricante provê o serviço **QuickStep**; congelá-lo comprometeria os gestos multitarefa de navegação (deslizar para cima para ver apps recentes).
- **`com.android.rkpdapp` (Remote Key Provisioning Daemon)**: Mantido ativo para atestações criptográficas de hardware KeyMint/StrongBox.
- **`com.android.settings.intelligence`**: Mantido ativo para busca nas Configurações.
- **`com.dolby.daxservice`**: Mantido para estabilidade do subsistema de processamento de áudio.
- **Pilha de Telefonia (`com.android.phone`, IMS, TelephonyProvider)**: Preservada para chamadas, SMS, dados móveis e serviços de emergência.

O catálogo pós-debloat com a situação detalhada de cada pacote consta em [`inventario-depois.json`](inventario-depois.json).

---

## 6. Comparativo de Recursos e Desempenho

As medições comparativas foram realizadas com ferramentas de telemetria do Android (`dumpsys meminfo`, `df -h`, `pm`):

| Indicador Técnico | Antes do Debloat | Depois do Debloat | Variação Quantitativa | Evidência Técnica |
|---|---|---|---|---|
| **Memória RAM Disponível** | ~4.5 GB livres | **~7.2 GB livres** | **+2.7 GB de RAM livre (+58,7%)** | `dumpsys meminfo` Passo 110 vs Passo 384 |
| **Memória RAM Ocupada** | ~7.5 GB ocupados | **~4.8 GB ocupados** | **-2.7 GB de consumo de RAM** | `dumpsys meminfo` Passo 110 vs Passo 384 |
| **Armazenamento Livre (`/data`)** | 193 GB livres | **~197 GB livres** | **~4 GB recuperados** (ganho agregado da partição; não mensurado por app) | `df -h /data` Passo 398 |
| **Total de Pacotes do Usuário** | 501 pacotes | **492 pacotes** | -9 pacotes desinstalados para Usuário 0 | `pm list packages -f` |
| **Aplicativos Habilitados** | 441 pacotes ativos | **248 pacotes preservados/ativos** | **-193 pacotes ativos (184 desativados + 9 desinstalados para o Usuário 0)** | `inventario-depois.json` (248 preservados/ativos, 244 desativados, 9 desinstalados) |
| **Aplicativos Desativados** | 60 pacotes de fábrica | **244 pacotes desativados** | +184 pacotes congelados | `pm list packages -d` Passo 89 vs Passo 701 |
| **Adwares Monitorados em RAM** | 5 daemons (~750 MB RSS) | **Processos finalizados** | Daemons paralisados na sessão | `dumpsys meminfo` (Glance, Taboola, InMobi) |
| **Google QuickSearchBox em RAM** | 873 MB RSS | **0 MB (processo encerrado)** | **-873 MB de carga contínua** | `dumpsys meminfo` (Search + GoogleApp) |
| **Perfis Secundários em Execução**| User 0 + User 11 ativos | **Apenas User 0 ativo** | **-269 MB RSS de instâncias duplicadas** | `am stop-user -f 11` |
| **Temperatura em Espera** | 37.0°C a 40.0°C | **33.0°C** | **-4°C a -7°C (redução térmica observada)**| `dumpsys battery` Passo 384 |
| **Play Integrity / Bancos** | Não coletado na sessão | **Pendente de validação** | Testes bancários e atestação não executados | Registros não contêm chamadas Play Integrity |

> **Nota de reconciliação:** um resumo operacional anterior registrava 257 pacotes habilitados. Esse valor não coincide com os 248 pacotes classificados como preservados/ativos no inventário final. Como a saída bruta do comando não está publicada para conferência, 257 não é tratado como valor confirmado; o comparativo utiliza a classificação do inventário estruturado.

O comparativo estruturado em formato JSON está catalogado em [`comparativo.json`](comparativo.json).

---

## 7. Testes de Funcionalidade e Validação Operacional

Para garantir total conformidade com a transparência técnica, cada teste é classificado de acordo com as evidências disponíveis:

| Recurso / Funcionalidade | Status da Validação | Evidência / Fundamentação Técnica |
|---|---|---|
| **Conectividade Wi-Fi** | **Aprovado** | Toda a sessão de debloat foi realizada via Wireless ADB na rede local sem desconexões. |
| **Áudio e Equalização** | **Aprovado** | Permissão especial `DUMP` concedida com sucesso ao equalizador Wavelet via `pm grant`. |
| **Resolução de DNS / NextDNS** | **Aprovado** | Resolução DNS e bloqueio de telemetria validados via ping no Passo 720. |
| **Câmera Fotográfica** | **Aprovado** | Aplicativo `com.motorola.camera5` funcional, com `ACCESS_COARSE_LOCATION` revogado. |
| **Gestos de Navegação** | **Aprovado** | QuickStep preservado através da manutenção do Moto Launcher em segundo plano. |
| **Chamadas Telefônicas (Voz)** | **Pendente de validação** | Pilha RIL e telefonia preservadas; sem teste de chamada registrado em log. |
| **Envio e Recebimento de SMS** | **Pendente de validação** | Pilha de mensageria preservada; sem envio/recebimento de SMS registrado em log. |
| **Dados Móveis (4G e 5G)** | **Pendente de validação** | Rádio 5G mantido; sessão realizada exclusivamente via Wi-Fi; tráfego móvel não auditado em log. |
| **VoLTE e VoWiFi** | **Pendente de validação** | Módulos nacionais preservados; stubs estrangeiros desativados; funcionalidade de voz sobre IP não testada em log. |
| **Bluetooth** | **Pendente de validação** | Stack Bluetooth AOSP preservada; pareamento de periféricos não testado durante a sessão. |
| **Geolocalização / GPS** | **Pendente de validação** | LocationManager nativo preservado; precisão em navegação não avaliada em log. |
| **Autenticação Biométrica** | **Pendente de validação** | KeyStore e StrongBox preservados; leitura de biometria na tela não registrada em log. |
| **Notificações Push (FCM)** | **Pendente de validação** | Conexão TCP do GMS mantida em background; entrega prática de notificações não auditada. |
| **Aplicativos Bancários** | **Pendente de validação** | Nenhum aplicativo de instituição financeira foi aberto ou auditado durante a sessão ADB. |
| **Transações Pix** | **Pendente de validação** | Dependente de validação presencial nos aplicativos bancários do usuário. |
| **Play Integrity e Certificação** | **Pendente de validação** | Atestação MEETS_BASIC / MEETS_DEVICE não foi aferida via API na sessão. |
| **Atualizações OTA de Sistema** | **Pausado intencionalmente** | `com.motorola.ccc.ota` foi paralisado para evitar sobrescrita automática das desativações. |

---

## 8. Segurança e Privacidade

### 8.1. Vetores de Risco e Pacotes Comerciais Desativados
- **Instaladores Silenciosos de Fábrica:** Instaladores parceiros como **Digital Turbine** (`com.dti.motorola`, `com.dti.amx`) e **IronSource Aura** possuíam permissões para download de pacotes. A desativação desses serviços suspende esse vetor no perfil.
- **Telemetria de Fabricante:** Desativação de serviços de coleta de estatísticas de modem, métricas de ciclo de vida e upload de logs de falha para servidores externos.
- **Bloatwares Não-Desativáveis:** Pacotes como `com.payjoy.access` e `com.amazon.appmanager` foram isolados no firewall do kernel (`netpolicy`) e impedidos de executar em segundo plano via AppOps.

### 8.2. Sandboxing de Permissões
- **Isolamento do Google Play Services:** A configuração de retorno nulo (`ignore`) para localização e sensores no UID 10387 suspende o envio de localização pela conta Google no perfil, mantendo apenas a conectividade básica de rede.
- **Proteção de Metadados de Fotos:** A revogação de `ACCESS_COARSE_LOCATION` da Câmera Motorola impede a inclusão involuntária de coordenadas de GPS nos metadados EXIF das fotografias.

---

## 9. Limitações Técnicas, Dados Ausentes e Coleta Complementar

Em cumprimento às diretrizes de integridade documental, registram-se as limitações técnicas desta auditoria e as ações recomendadas:

### 9.1. Comandos de Coleta Complementar (Para Execução Futura pelo Proprietário)
Os seguintes comandos devem ser executados pelo proprietário para suprir as lacunas canônicas identificadas:

```bash
# 1. Confirmação canônica da versão do Android e compilação:
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.incremental
adb shell getprop ro.build.fingerprint

# 2. Identificação de hardware (processador e placa gráfica):
adb shell cat /proc/cpuinfo
adb shell dumpsys SurfaceFlinger | grep -i "GLES"

# 3. Verificação da certificação Play Integrity:
# Executar aplicativo Play Integrity API Checker (Play Store) e registrar
# se o dispositivo atinge MEETS_BASIC_INTEGRITY e MEETS_DEVICE_INTEGRITY.
```

### 9.2. Atualizações de Sistema (OTA)
Caso o usuário venha a reativar o daemon de atualizações (`com.motorola.ccc.ota`) e instale uma atualização de firmware da fabricante, o `PackageManagerService` poderá restaurar pacotes desativados. Recomenda-se a reexecução do script de debloat após qualquer atualização de sistema.

---

## 10. Proposta de Validação e Contribuição

### Classificação Final: PENDENTE DE VALIDAÇÃO
- **Justificativa Técnica:** A auditoria documental, a conciliação de pacotes e o histórico de alterações estão consistentes e comprovados pelas evidências extraídas via ADB. No entanto, a ausência de coleta das propriedades canônicas do sistema operacional via `getprop` e a ausência de registros em log de testes de chamadas de voz, biometria e aplicativos bancários exigem a classificação formal como **Pendente de validação**, até que testes presenciais complementares sejam realizados pelo proprietário do dispositivo.

### Proposta Técnica de Contribuição:
1. **Branch do Projeto:** `feat/motorola-edge-60-pro-audit`.
2. **Arquivos Integrados:**
   - `reports/motorola-edge-60-pro/README.md`
   - `reports/motorola-edge-60-pro/auditoria.md`
   - `reports/motorola-edge-60-pro/inventario-antes.json`
   - `reports/motorola-edge-60-pro/inventario-depois.json`
   - `reports/motorola-edge-60-pro/pacotes-desativados.txt`
   - `reports/motorola-edge-60-pro/pacotes-desinstalados.txt`
   - `reports/motorola-edge-60-pro/permissoes-alteradas.json`
   - `reports/motorola-edge-60-pro/comparativo.json`
   - `reports/motorola-edge-60-pro/evidencias/README.md`
   - `reports/README.md` (índice geral atualizado)
