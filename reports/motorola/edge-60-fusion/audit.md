# Relatório Técnico de Auditoria Forense e Otimização — Motorola Edge 60 Fusion

**Dispositivo:** Motorola Edge 60 Fusion (`motorola_edge_60_fusion` / `scout_g_sysn`)  
**Nome de Código (Codename / Board):** `scout` / `mt6878` (MediaTek Dimensity 7300)  
**Versão do Android:** Android 16 (API Level 36 - VanillaIceCream)  
**ID da Build / Firmware:** `W1VCS36H.14-20-19-9`  
**Patch de Segurança:** 01/09/2026  
**Canal de Software:** Varejo Brasil (`retbr`) · Bootloader Bloqueado · Non-root  
**Data da Auditoria:** 07 e 08 de Novembro de 2026  

---

## 1. Contextualização e Escopo

O **Motorola Edge 60 Fusion** é um smartphone intermediário premium lançado com hardware baseado na plataforma MediaTek MT6878 (Dimensity 7300, arquitetura ARMv8.2-A / octa-core), 8 GB de memória RAM física LPDDR4X/LPDDR5 e 256 GB de armazenamento interno UFS. O sistema operacional de fábrica é o **Android 16** sob a camada de personalização **Hello UI** da Motorola.

### 1.1 Motivação da Auditoria
Embora a interface Hello UI apresente um design visual próximo ao Android Open Source Project (AOSP), o exame forense da imagem stock revelou uma densa malha de serviços em segundo plano:
1. **Adware e Droppers Comerciais Pré-carregados:** Inclusão de componentes de monetização de terceiros como Digital Turbine Ignite (`com.dti.motorola`) e ironSource AppCloud (`com.aura.oobe.motorola`), dotados de permissões privilegiadas para instalação silenciosa de aplicativos (`INSTALL_PACKAGES`).
2. **Frameworks de Publicidade e Telemetria da Meta:** Módulos pré-instalados em partições do sistema (`com.facebook.appmanager`, `com.facebook.services`, `com.facebook.system`) que burlam as políticas de economia de energia (modo Doze) e mantêm sincronização constante.
3. **Serviços Ociosos e Telemetria Diagnóstica OEM/SoC:** Módulos da Motorola e MediaTek (`motocare`, `bach.modemstats`, `motowifimetrics`, `apmonitor`, `appforecast`) executando diagnósticos ininterruptos e consumindo ciclos de CPU e RAM.
4. **Coleta Geográfica e Acústica Passiva Big Tech:** Serviços de linha do tempo contínua do Google Play Services (`gms.location.history`) e escuta acústica permanente em DSP RISCV (`hotwordenrollment.okgoogle` e `xgoogle`).
5. **Permissões Abusivas em Aplicativos de Comércio e Birôs:** Mais de 20 aplicativos de usuário possuíam permissão de rastreamento por satélite (`ACCESS_FINE_LOCATION`) concedida sem necessidade técnica real para suas tarefas essenciais.

### 1.2 Princípios e Limites Metodológicos
Esta auditoria foi executada sob autorização e acompanhamento do proprietário do dispositivo, adotando critérios rigorosos:
- **Zero Operações Destrutivas:** O debloat não utiliza root, não altera a partição de inicialização (`boot.img`), não desbloqueia o bootloader e preserva a integridade de verificação do **Play Integrity** (essencial para aplicativos bancários brasileiros).
- **Reversibilidade Integral:** Todas as desativações foram realizadas no nível do Usuário 0 (`pm disable-user --user 0`) ou via restrições pontuais de AppOps, permitindo restauração instantânea por comandos ADB espelhados.
- **Preservação de Dependências Vitais:** Pilhas de telefonia (RIL, IMS, VoLTE), System UI, SurfaceFlinger, launcher padrão (`com.motorola.launcher3`), biometria e aplicativos expressamente preservados pelo usuário (como **Gemini**, **Fruit Merge** e **Calendário Menstrual**) foram rigorosamente protegidos.

---

## 2. Metodologia de Coleta e Auditoria

A auditoria utilizou a ponte de comunicação oficial **Android Debug Bridge (ADB)** através de conexão autorizada e autenticada por chave RSA.

### 2.1 Ferramentas e Procedimentos de Inspeção
1. **Identificação Canônica de Hardware e Firmware:**
   ```bash
   adb shell getprop ro.product.manufacturer
   adb shell getprop ro.product.model
   adb shell getprop ro.product.name
   adb shell getprop ro.product.device
   adb shell getprop ro.build.version.release
   adb shell getprop ro.build.version.sdk
   adb shell getprop ro.build.display.id
   adb shell getprop ro.build.version.security_patch
   adb shell getprop ro.build.fingerprint
   adb shell uname -a
   ```
2. **Mapeamento Exaustivo de Pacotes:**
   - Pacotes totais: `adb shell pm list packages -f`
   - Pacotes do sistema: `adb shell pm list packages -s -f`
   - Pacotes de usuário/terceiros: `adb shell pm list packages -3 -f`
   - Pacotes desativados de fábrica: `adb shell pm list packages -d`
3. **Análise Forense de Permissões e Componentes:**
   - Inspeção de manifesto e permissões concedidas: `adb shell dumpsys package <package_name>`
   - Detecção de processos ativos e consumo de memória: `adb shell dumpsys meminfo <package_name>` e `dumpsys meminfo` agregado.
   - Verificação de daemons em execução no kernel: `adb shell ps -A`
4. **Classificação em 6 Lotes Temáticos:**
   - **Lote 1:** Aplicativos de Usuário e Terceiros (62 pacotes)
   - **Lote 2:** Bloatware de Parceiros, Operadoras, Adware e Financiamento (49 pacotes)
   - **Lote 3:** Ecossistema Motorola / Lenovo OEM (130 pacotes)
   - **Lote 4:** Ecossistema Google / GMS & Framework (104 pacotes)
   - **Lote 5:** MediaTek SoC, RIL, Telefonia, IMS e Hardware HALs (18 pacotes)
   - **Lote 6:** Android Core, AOSP, Framework e Sistema Base (123 pacotes)

---

## 3. Estado Inicial do Dispositivo (Linha de Base Pré-Debloat)

| Item de Diagnóstico | Estado Inicial Verificado |
| :--- | :--- |
| **Total de Pacotes Instalados** | **486 pacotes** |
| **Pacotes de Sistema** | 424 pacotes |
| **Pacotes de Terceiros / Usuário** | 62 pacotes |
| **Pacotes Desativados de Fábrica** | 67 pacotes (overlays inativos de operadoras internacionais e stubs de varejo) |
| **Processos Ativos em RAM em Repouso** | 66 processos em segundo plano |
| **Memória RAM Usada (Used PSS)** | ~3.800 MB PSS |
| **Memória RAM Livre** | ~2.750 MB livres (2.750.000 KB) de 7.594.168 KB totais |
| **Perfil de Usuário Ativo** | `User 0` (Usuário Primário) |
| **Segurança & Permissões** | Mais de 20 apps comerciais com rastreamento GPS contínuo ativo |
| **Teclado / Discador / SMS Padrão** | Gboard (`latin`), Google Dialer e Google Messages proprietários |

---

## 4. Análise de Componentes por Lotes

### 4.1 Lote 1 — Aplicativos de Usuário e Terceiros (62 Pacotes)
- **Serviços Bancários e Governamentais (Críticos - Preservação Obrigatória):**
  - Banco Inter (`br.com.intermedium`), Nubank (`com.nu.production`), Cartões CAIXA (`br.gov.caixa.cartoes`), Mercado Pago (`com.mercadopago.wallet`).
  - Gov.br (`br.gov.meugovbr`), e-Título (`br.jus.tse.eleitoral.etitulo`), CDT Trânsito (`br.gov.serpro.cnhe`).
  - *Decisão Técnica:* Preservados operacionais sem modificação, mantendo a conformidade observada com autenticação bancária, biometria facial e diretrizes regulatórias.
- **Redes Sociais e Mensageiros (Alto Risco de Privacidade):**
  - Facebook (`com.facebook.katana`), Instagram (`com.instagram.android`), TikTok (`com.zhiliaoapp.musically`), Threads (`com.instagram.barcelona`), WhatsApp (`com.whatsapp`).
  - *Decisão Técnica:* Threads desinstalado (encerra daemon persistente `InappFbnsService`). Facebook, Instagram, TikTok e WhatsApp mantidos funcionais, porém com revogação estrita de `ACCESS_FINE_LOCATION`, `ACCESS_COARSE_LOCATION`, `READ_CONTACTS` e `READ_PHONE_STATE`.
- **Comércio e Delivery:**
  - iFood, Burger King, McDonald's, Mercado Livre, Booking, Primeira Mesa, Food To Save, Jequiti.
  - *Decisão Técnica:* Revogada a permissão de GPS por satélite (`ACCESS_FINE_LOCATION`). Os aplicativos continuam funcionando perfeitamente utilizando o endereço cadastrado pelo usuário.
- **Jogos Comerciais e Adware:**
  - Word Solitaire (`com.hitappsgames.wordsolitaire`): Identificados 5 SDKs de publicidade integrados (LevelPlay, AppMetrica, AppLovin, Vungle, Facebook Ads). Neutralizado.
  - Fruit Merge (`com.melon.drop.fruit.merge.master`): Expressamente preservado por solicitação direta do usuário.
  - Calendário Menstrual (`com.popularapp.periodcalendar`): Expressamente preservado por solicitação direta do usuário.

### 4.2 Lote 2 — Bloatware de Parceiros, Operadoras e Financiamento (49 Pacotes)
- **Droppers Comerciais e Adware OEM:**
  - Digital Turbine Ignite (`com.dti.motorola`): Dropper ativo em RAM (PID 12589) com permissão `INSTALL_PACKAGES`. Desinstalado no Usuário 0.
  - ironSource AppCloud (`com.aura.oobe.motorola`): Dropper de primeiro boot. Desinstalado no Usuário 0.
  - Meta Preloads (`com.facebook.appmanager`, `com.facebook.services`, `com.facebook.system`): Sincronizadores e instaladores da Meta na partição `/system`. Desinstalados no Usuário 0.
- **Stubs de Financiamento e Cobrança:**
  - PAKS Finance (`com.motorola.paks`): Desativado de fábrica.
  - PAKS Notification (`com.motorola.paks.notification`): Bloqueado via AppOps (`RUN_IN_BACKGROUND=ignore`, `POST_NOTIFICATION=ignore`, `WAKE_LOCK=ignore`).
  - PayJoy Access (`com.payjoy.access`): Desativado de fábrica.
- **Resíduos de Operadoras Estrangeiras:**
  - Desativados stubs da AT&T, Verizon, Sprint, T-Mobile, Claro Colômbia e Vodafone europeia, completamente inertes e inúteis no Brasil.

### 4.3 Lote 3 — Ecossistema Motorola / Lenovo OEM (130 Pacotes)
- **Telemetria Diagnóstica:**
  - `motocare`, `bach.modemstats`, `motowifimetrics`, `bug2go`, `help.extlog`, `appforecast`: Desativados no Usuário 0. Elimina envio contínuo de logs para servidores da fabricante.
- **Inteligência Artificial Proprietária da Motorola:**
  - `com.motorola.aicore`, `com.motorola.aiservices`, `com.motorola.createwithai`: Serviços com conexões ativas para a nuvem Vertex AI e MS Speech. Desativados no Usuário 0.
- **Serviços Ociosos:**
  - `com.motorola.mobiledesktop.core` (Ready For), `com.motorola.timeweatherwidget` (polling AccuWeather), `contacts.preloadcontacts`, `lifetimedata`, `livewallpaper3`, `iotservice`: Desativados, liberando mais de 250 MB de RAM.
- **Componentes Essenciais Preservados:**
  - `com.motorola.launcher3` (QuickStep e gestos de navegação preservados).
  - Moto Camera nativa e drivers de sensor fotográfico preservados.
  - Subsistemas de tela, áudio e carregamento rápido TurboPower preservados.

### 4.4 Lote 4 — Ecossistema Google / GMS & Framework (104 Pacotes)
- **Serviços Secundários e Bloatware Google:**
  - `com.google.android.apps.chromecast.app` (Google Home), `projection.gearhead` (Android Auto), `apps.magazines` (Google Notícias), `apps.tachyon` (Google Meet), `apps.subscriptions.red` (Google One), `apps.turbo` (Device Health Services), `feedback`, `partnersetup`, `setupwizard`, `apps.wellbeing`: Desativados.
- **Rastreamento Passivo:**
  - `com.google.android.gms.location.history`: Histórico de localização 24/7 desativado.
  - `com.android.hotwordenrollment.okgoogle` e `xgoogle`: Escuta passiva acústica de microfone desativada.
  - `com.google.android.adservices.api` e `ondevicepersonalization.services`: Privacy Sandbox desativada/bloqueada.
- **Preservação Estratégica do Gemini e do Google App:**
  - `com.google.android.apps.bard` (Gemini): **Preservado sem alteração**.
  - `com.google.android.googlequicksearchbox` (Google App): **Preservado sem alteração**, pois a análise arquitetural de dependências do APK do Gemini comprovou que a interface e o motor do Bard/Gemini residem internamente no pacote hospedeiro da Google.
- **Preservação do GMS Core e Play Store:**
  - `com.google.android.gms` e `com.android.vending`: Mantidos ativos e íntegros, assegurando validação de licenças, push notifications via FCM e integridade do Play Protect.

### 4.5 Lote 5 — MediaTek SoC, RIL, Telefonia e Hardware HALs (18 Pacotes)
- `com.mediatek.apmonitor`: Monitor de desempenho do SoC desativado.
- `com.mediatek.op12.ims`: Módulo IMS exclusivo da operadora americana Verizon Wireless desativado.
- **Preservados Obrigatoriamente:** Pilha IMS AOSP/MediaTek para Claro, Vivo e TIM, RIL de modem celular, drivers de rádio 4G/5G, Bluetooth e Wi-Fi HAL.

### 4.6 Lote 6 — Android Core, AOSP e Sistema Base (123 Pacotes)
- Preservados todos os componentes críticos: `android` (framework-res), `com.android.systemui`, `com.android.providers.media`, `com.android.providers.telephony`, `com.android.providers.settings`, `com.android.keychain`, `com.android.permissioncontroller`.
- Desativados stubs obsoletos: `com.motorola.appdirectedsmsproxy`, `com.motorola.android.provisioning`, `com.motorola.enterprise.service`.

---

## 5. Procedimentos Realizados (Etapas 1 a 14)

A execução ocorreu em 14 etapas progressivas com verificação de estabilidade e memória entre cada bloco:

1. **Etapa 1:** Neutralização de adwares críticos (`dti.motorola`, `aura.oobe.motorola`, `paks.notification`).
2. **Etapa 2:** Desativação da infraestrutura pré-carregada da Meta (`facebook.appmanager`, `services`, `system`).
3. **Etapa 3:** Desativação de telemetria diagnóstica da Motorola (`smartfeed`, `appforecast`, `motocare`, `nativedropboxagent`, `dimo`, `enterprise.adapter.service`).
4. **Etapa 4:** Revogação de permissões abusivas de localização, contatos e identificação em redes sociais (Facebook, Instagram, TikTok, WhatsApp).
5. **Etapa 5:** Hardening inicial da Google (`setupwizard`, `feedback`, `partnersetup`, `wellbeing`, AppOps em `adservices.api`).
6. **Etapa 6:** Telemetria de baixo nível da Motorola, MediaTek e operadoras (17 pacotes, incluindo `motowifimetrics`, `modemstats`, `aicore`, `aiservices`, `apmonitor`).
7. **Etapa 7:** Desativação de serviços ociosos da Google (9 pacotes, incluindo Google Home, Android Auto, Google One, Google Meet), com preservação expressa do Gemini e do Google App hospedeiro.
8. **Etapa 8:** Remoção de jogos comerciais de publicidade (Word Solitaire) e threads da Meta, preservando Fruit Merge e Calendário Menstrual.
9. **Etapa 9:** Revogação de permissão de satélite (`ACCESS_FINE_LOCATION`) em 8 aplicativos de compras e delivery (iFood, Burger King, McDonald's, Booking, etc.).
10. **Etapa 10:** Otimização avançada de daemons da Motorola (Ready For / Desktop Core, widget de clima com polling AccuWeather, IoT service, etc.).
11. **Etapa 11:** Desativação de bloatwares da Google com permissões amplas (`ambient.streaming`, Google TV, YouTube Music, ARCore).
12. **Etapa 12:** Revogação de satélite (`ACCESS_FINE_LOCATION`) em aplicativos financeiros e birôs de crédito (Serasa, Jeitto, Boa Vista, Koin, Cartões CAIXA, Mercado Livre e Mercado Pago).
13. **Etapa 13:** Migração e neutralização de duplicidades proprietárias substituídas por suíte FOSS:
    - Gboard substituído por FUTO Keyboard (`ime disable` + AppOps).
    - Google Dialer e Mensagens substituídos por Fossify Phone (`ROLE_DIALER`) e Fossify Messages (`ROLE_SMS`).
    - Files, Agenda, Relógio, Calculadora, Contatos e Gravador de Voz substituídos por equivalentes FOSS.
14. **Etapa 14:** Expurgo final de resíduos de subsistema (Histórico de Localização da Google 24/7, módulos de escuta em hardware DSP RISCV "Ok Google" / "Hey Google", personalização federada da Privacy Sandbox e 5 overlays de operadoras norte-americanas).

---

## 6. Estado Final do Dispositivo (Pós-Debloat)

| Indicador de Estado | Estado Final Verificado | Variação Líquida |
| :--- | :--- | :--- |
| **Total de Pacotes Ativos no Usuário 0** | **343 pacotes** | -143 pacotes líquidos (155 neutralizados, +12 FOSS) |
| **Pacotes de Sistema Ativos** | 291 pacotes | -133 pacotes de sistema desativados/bloqueados |
| **Pacotes de Usuário / Terceiros Ativos** | 52 comerciais + 12 FOSS (64 pacotes) | Eliminação de adwares e substituição por FOSS |
| **Memória RAM Livre em Repouso** | **~4.153 MB a 4.573 MB livres** | **+1,40 GB a +1,82 GB de RAM disponível (+50.9% a +66.3%)** |
| **Memória RAM Usada (Used PSS)** | ~2.721 MB a 2.881 MB PSS | Queda sustentada de ~1 GB de processos residentes |
| **Processos em Segundo Plano** | 39 processos ativos | -27 daemons eliminados da memória |
| **Segurança e Privacidade Acústica** | Escuta passiva DSP e histórico 24/7 desativados | Eliminação de escuta acústica permanente |
| **Digitação de Textos** | Teclado FUTO Keyboard com operação local offline | Zero dados de digitação enviados para a nuvem |

---

## 7. Testes Disponíveis e Validação Funcional

Após a conclusão das intervenções, foram executadas validações empíricas no smartphone:
1. **Estabilidade de Boot:** Reinicialização a frio bem-sucedida; tempo de inicialização reduzido em relação à imagem stock; zero falhas de serviços essenciais.
2. **Interface e Gestos:** O `com.motorola.launcher3` opera com total fluidez na navegação por gestos do Android 16, transição de aplicativos e tela inicial.
3. **Telefonia e Mensagens:** Chamadas de voz de entrada e saída testadas e homologadas via Fossify Phone. Envio e recepção de SMS testados via Fossify Messages.
4. **Conectividade:** Conexão 4G/5G, Wi-Fi 2.4/5 GHz e Bluetooth com fones de ouvido operando estavelmente.
5. **Aplicativos Bancários:** Banco Inter e Nubank testados em ambiente real:
   - Login biométrico por impressão digital concluído com sucesso.
   - Consulta de extratos e emissão de Pix operacionais.
   - Nenhuma notificação de "dispositivo modificado" ou falha de integridade.
6. **Gemini & Pesquisa:** O atalho e a interface do Gemini continuam respondendo instantaneamente ao toque, aproveitando o app Google mantido íntegro.
7. **Aplicativos Preservados:** Fruit Merge e Calendário Menstrual continuam intactos e com seus dados preservados.

---

## 8. Limitações e Pendências

1. **Protocolo RCS no Fossify Messages:** O chat RCS não funciona no mensageiro FOSS, pois depende dos servidores fechados da Google. O aplicativo opera via SMS/MMS convencionais.
2. **Acionamento por Voz ("Ok Google"):** Com a desativação da escuta passiva no DSP RISCV, o assistente não desperta à distância por voz; o uso ocorre exclusivamente por toque.
3. **Medição de Bateria em Ciclo Padronizado de 24h:** A melhoria na autonomia energética é uma inferência lógica decorrente do encerramento de 27 processos em segundo plano e do fim do polling de GPS, mas não foi mensurada em ciclo controlado de 24h em laboratório. Marcado como **não medido**.
4. **Descompressão de Armazenamento por Pacote:** O ganho na partição `/data` foi observado de forma agregada; o ganho de bytes individual de cada APK não foi medido isoladamente. Marcado como **ganho agregado não decomposto**.

---

## 9. Conclusões Técnicas

A auditoria e o debloat realizados no **Motorola Edge 60 Fusion** demonstraram que é viável converter um smartphone comercial recente (Android 16 / Hello UI) em uma estação de trabalho móvel com alto grau de privacidade, performance e segurança, sem necessidade de root e sem comprometer a estabilidade do sistema operacional.

Os principais resultados técnicos consolidados incluem:
- **Redução substancial da superfície de ataque e vigilância:** Eliminação de 155 componentes desnecessários e revogação de permissões invasivas em 21 aplicativos.
- **Aumento sustentado de memória RAM disponível:** Liberação de até **1,82 GB de RAM física**, garantindo que aplicativos pesados permaneçam em cache sem engasgos.
- **Migração bem-sucedida para o ecossistema FOSS:** Substituição transparente de teclado, discador, SMS, contatos, agenda, relógio e galeria por alternativas de código aberto auditáveis e sem acesso à internet.
- **Preservação rigorosa de utilidade diária:** Aplicativos bancários, Pix, documentos oficiais e aplicativos pessoais do proprietário continuam funcionando com total integridade.
