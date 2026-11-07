# Evidências e Cadeia de Custódia — Motorola Edge 60 Pro (`XT2507-1`)

Este diretório documenta as fontes de dados, comandos de extração forense e métodos de validação utilizados na auditoria técnica de debloat e otimização do **Motorola Edge 60 Pro**.

---

## 1. Origem e Proveniência dos Dados

Todos os registros e inventários apresentados nesta auditoria foram obtidos diretamente da execução real de comandos no dispositivo conectado via **Android Debug Bridge (ADB)** e camada **Shizuku**:

- **Sessão de Execução:** Histórico de auditoria forense registrado na base local do assistente técnico.
- **Identificador de Sessão Interna:** `2775a24c-1202-4911-836a-9f32885332b0` (365 invocações de ferramentas e 816 etapas analisadas).
- **Modo de Conexão:** Depuração Sem Fio (Wireless ADB) via pareamento TLS (porta efêmera + PIN de 6 dígitos) e conexão na porta TCP principal do dispositivo.
- **Nível de Privilégio:** `shell:1000` (usuário não-root).
- **Data da Auditoria:** 06 e 07 de novembro de 2026.

---

## 2. Comandos e Ferramentas ADB Empregadas

| Categoria | Comando Base | Finalidade |
|---|---|---|
| **Identificação** | `adb devices -l`<br>`adb shell getprop ro.product.model` | Validação do modelo (`motorola_edge_60_pro`), produto (`cybert_g_sys`) e codename (`cybert`). |
| **Inventário Inicial** | `adb shell pm list packages -f`<br>`adb shell pm list packages -3`<br>`adb shell pm list packages -d` | Extração dos 501 pacotes instalados com caminhos de APK, pacotes de terceiros e 60 pacotes desativados de fábrica. |
| **Inspeção de Pacotes** | `adb shell dumpsys package packages` | Extração de UIDs, flags de sistema, versões, instaladores de origem, permissões concedidas e status de usuários (User 0 / User 11). |
| **Telemetria de Memória** | `adb shell dumpsys meminfo` | Coleta de RSS/PSS por processo em múltiplas fases (inicial, pós-debloat básico, pós-degoogle e final). |
| **Armazenamento** | `adb shell df -h /data` | Mensuração do espaço livre recuperado com purga física de atualizações em `/data/app`. |
| **AppOps Sandboxing** | `adb shell cmd appops set --uid <UID> <OP> ignore` | Neutralização de GPS, Activity Recognition e Body Sensors no Google Play Services (`UID 10387`) e serviços `non-disable`. |
| **Bloqueio de Kernel** | `adb shell cmd netpolicy add restrict-background-blacklist <UID>` | Bloqueio de tráfego de rede em segundo plano no firewall/netpolicy do Android para bloatwares persistentes. |
| **Validação de Rede** | `adb shell ping -c 1 <host>` | Teste de resolução DNS e bloqueio de telemetria via NextDNS. |

---

## 3. Política Estrita de Privacidade e Sanitização

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
   - O dump completo de pacotes em formato bruto (`dumpsys_full.txt`, 2.857.883 bytes) e logs de execução com metadados detalhados permanecem armazenados exclusivamente de forma local no ambiente do operador técnico.

---

## 4. Arquivos Gerados e Verificação de Integridade

- `inventario-antes.json`: 501 pacotes mapeados com vendor, caminho APK, UID e função.
- `inventario-depois.json`: Comparativo de 501 pacotes com status final pós-debloat.
- `pacotes-desativados.txt`: Lista nominal dos 244 pacotes desativados.
- `pacotes-desinstalados.txt`: Registro dos 9 pacotes de usuário uninstalled e 10 purgas de atualização em `/data/app`.
- `permissoes-alteradas.json`: 14 revogações de permissão runtime, 6 AppOps ignorados no GMS e 7 bloatwares em quarentena de netpolicy.
- `comparativo.json`: Tabela consolidada de métricas de hardware e software.
