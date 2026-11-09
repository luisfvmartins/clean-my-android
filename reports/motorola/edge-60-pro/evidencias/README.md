# Evidências e Cadeia de Custódia — Motorola Edge 60 Pro (`XT2507-1`)

Este diretório documenta as fontes de dados, comandos de extração forense, métodos de validação e limitações técnicas da auditoria de debloat e otimização do **Motorola Edge 60 Pro**.

---

> [!CAUTION]
> **Conflito com a lista de componentes protegidos:** uma revisão posterior encontrou 18 pacotes presentes tanto em `pacotes-desativados.txt` quanto em `data/protected_essential_packages.txt`. A interseção inclui componentes de discagem e SMS, emergência, SIM Toolkit, Bluetooth, contatos e serviços do sistema.
>
> Isso não confirma o estado atual do aparelho nem comprova falha funcional, mas conflita com as barreiras de segurança atuais do projeto. O registro é histórico, não uma recomendação. **Não reproduza essa lista em outros aparelhos.** O estado real deve ser verificado no dispositivo; qualquer restauração exige avaliação individual e validação presencial de chamadas, SMS, SIM, emergência, Bluetooth e contatos.

---

## 1. Origem e Proveniência dos Dados

Todos os registros e inventários apresentados nesta auditoria foram obtidos a partir da execução de comandos no dispositivo conectado via **Android Debug Bridge (ADB)** e camada **Shizuku**:

- **Sessão de Execução:** Histórico de auditoria forense registrado na base local do assistente técnico.
- **Modo de Conexão:** Depuração Sem Fio (Wireless ADB) via pareamento TLS (porta efêmera + PIN de 6 dígitos) e conexão na porta TCP principal do dispositivo.
- **Nível de Privilégio:** `shell:1000` (usuário não-root; bootloader bloqueado).
- **Data da Auditoria:** 06 e 07 de novembro de 2026.

---

## 2. Comandos e Ferramentas ADB Empregadas

| Categoria | Comando Base | Finalidade |
|---|---|---|
| **Identificação do Modelo** | `adb devices -l`<br>`adb shell getprop ro.product.model` | Validação do modelo (`motorola_edge_60_pro`), produto (`cybert_g_sys`) e codename (`cybert`). |
| **Inventário Inicial** | `adb shell pm list packages -f`<br>`adb shell pm list packages -3`<br>`adb shell pm list packages -d` | Extração dos 501 pacotes instalados com caminhos de APK, 50 pacotes de terceiros e 60 pacotes desativados de fábrica. |
| **Inspeção de Pacotes** | `adb shell dumpsys package packages` | Extração de UIDs, flags de sistema, versões declaradas de pacotes, permissões concedidas e status de usuários (User 0 / User 11). |
| **Telemetria de Memória** | `adb shell dumpsys meminfo` | Coleta de RSS/PSS por processo em múltiplas fases (inicial, pós-debloat básico, pós-degoogle e final). |
| **Armazenamento** | `adb shell df -h /data` | Verificação do espaço livre global em `/data` antes e depois das operações de desinstalação e limpeza de cache. |
| **AppOps Sandboxing** | `adb shell cmd appops set --uid <UID> <OP> ignore` | Restrição de GPS, Activity Recognition e Body Sensors no Google Play Services (`UID 10387`) e serviços protegidos contra disable. |
| **Bloqueio no Kernel** | `adb shell cmd netpolicy add restrict-background-blacklist <UID>` | Bloqueio de tráfego de dados em segundo plano no firewall/netpolicy do Android para bloatwares persistentes. |
| **Validação de Rede** | `adb shell ping -c 1 <host>` | Teste de resolução DNS e verificação de bloqueio de domínios de telemetria via NextDNS. |

---

## 3. Coleta Complementar Pendente (Ações Recomendadas para o Proprietário)

Durante a sessão operacional de debloat, determinados parâmetros canônicos do sistema não foram extraídos via `getprop`. Para sanar essas pendências sem inferências ou estimativas, os seguintes comandos devem ser executados pelo proprietário em uma oportunidade futura:

```bash
# Confirmação canônica da versão do Android, SDK e compilação da ROM:
adb shell getprop ro.build.version.release
adb shell getprop ro.build.version.sdk
adb shell getprop ro.build.version.incremental
adb shell getprop ro.build.fingerprint

# Detalhamento de hardware (SoC e GPU):
adb shell cat /proc/cpuinfo
adb shell dumpsys SurfaceFlinger | grep -i "GLES"

# Validação do Play Integrity (atestação):
# Executar verificação via aplicativo Play Integrity API Checker (Play Store)
# ou consultar status de certificação em Configurações > Google > Todos os serviços > Play Protect
```

> [!NOTE]
> Enquanto os comandos acima não forem executados e suas saídas documentadas, a versão do sistema operacional permanecerá classificada como **Pendente de confirmação** e os testes funcionais como **Não coletados na sessão**.

---

## 4. Política Estrita de Privacidade e Sanitização

Conforme as diretrizes de segurança e privacidade do projeto **Clean My Android**, todas as evidências publicadas neste repositório passaram por higienização prévia:

1. **Identificadores Pessoais e de Hardware:**
   - Números de IMEI, MEID e Serial Number foram omitidos.
   - Endereços MAC de Wi-Fi e Bluetooth foram omitidos.
   - Números de telefone e identificadores de chip (ICCID) não foram coletados nem publicados.
2. **Contas e Credenciais:**
   - Tokens de API (incluindo chaves de perfil do NextDNS) foram substituídos por marcações neutras (`SUA_API_KEY`, `SEU_ID`).
   - Contas Google, e-mails e credenciais sincronizadas foram omitidas.
3. **Rede e Roteamento:**
   - Endereços IP locais dinâmicos da rede doméstica foram documentados apenas com a convenção padrão RFC 1918 (`192.168.1.X`), preservando a privacidade da topologia de rede do usuário.
4. **Armazenamento de Dados Brutos:**
   - O dump completo de pacotes em formato bruto (`dumpsys_full.txt`) e os arquivos de histórico operacional permanecem restritos ao ambiente local do operador técnico para proteção de dados do proprietário.

---

## 5. Arquivos Gerados e Verificação de Integridade

- `inventario-antes.json`: 501 pacotes catalogados com fornecedor, caminho físico, UID e função preliminar.
- `inventario-depois.json`: 501 pacotes com estado final (248 preservados, 244 desativados, 9 desinstalados para usuário 0).
- `pacotes-desativados.txt`: Lista nominal dos 244 pacotes em estado `disabled-user`.
- `pacotes-desinstalados.txt`: Registro dos 9 pacotes desinstalados para o usuário 0 e notas sobre reversão de atualizações em `/data/app`.
- `permissoes-alteradas.json`: 13 permissões runtime revogadas, 2 tentativas de permissão especial documentadas, 6 AppOps no GMS (`UID 10387`) e 7 pacotes em quarentena de netpolicy.
- `comparativo.json`: Tabela consolidada de métricas quantitativas de desempenho e status de testes.
