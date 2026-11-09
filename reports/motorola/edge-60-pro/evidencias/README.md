# Evidências e Cadeia de Custódia — Motorola Edge 60 Pro (`XT2507-1`)

Este diretório documenta as fontes de dados, comandos de extração forense, métodos de validação e limitações técnicas da auditoria de debloat e otimização do **Motorola Edge 60 Pro**.

---

> [!CAUTION]
> **Conflito com a lista de componentes protegidos:** uma revisão posterior encontrou 18 pacotes presentes tanto em `pacotes-desativados.txt` quanto em `data/protected_essential_packages.txt`. A interseção inclui componentes de discagem e SMS, emergência, SIM Toolkit, Bluetooth, contatos e serviços do sistema.
>
> **Atualização de 09/11/2026:** O conflito relativo ao pacote `com.android.vending` (Google Play Store) e módulos de integridade associados resultou em falha empírica na execução de aplicativos governamentais (Play Integrity API). Os componentes foram reativados via ADB, sanando a incompatibilidade. Consulte o [Estudo de Caso de Play Integrity](../case-study-play-integrity.md).

---

## 1. Origem e Proveniência dos Dados

Todos os registros e inventários apresentados nesta auditoria foram obtidos a partir da execução de comandos no dispositivo conectado via **Android Debug Bridge (ADB)** e camada **Shizuku**:

- **Sessão de Execução Inicial:** 06 e 07 de novembro de 2026.
- **Sessão de Validação e Remediação:** 09 de novembro de 2026.
- **Modo de Conexão:** Depuração Sem Fio (Wireless ADB) via pareamento TLS (porta efêmera + PIN de 6 dígitos) e conexão na porta TCP principal do dispositivo.
- **Nível de Privilégio:** `shell:1000` (usuário não-root; bootloader bloqueado).

---

## 2. Comandos e Ferramentas ADB Empregadas

| Categoria | Comando Base | Finalidade |
|---|---|---|
| **Identificação do Modelo** | `adb devices -l`<br>`adb shell getprop ro.product.model` | Validação do modelo (`motorola_edge_60_pro`), produto (`cybert_g_sys`) e codename (`cybert`). |
| **Identificação do Sistema** | `adb shell getprop ro.build.version.release`<br>`adb shell getprop ro.build.fingerprint` | Confirmação canônica do Android 17 (SDK 37) e compilação `7a1c2-08c719`. |
| **Inventário Inicial** | `adb shell pm list packages -f`<br>`adb shell pm list packages -3`<br>`adb shell pm list packages -d` | Extração dos 501 pacotes instalados com caminhos de APK, 50 pacotes de terceiros e 60 pacotes desativados de fábrica. |
| **Inspeção de Pacotes** | `adb shell dumpsys package packages` | Extração de UIDs, flags de sistema, versões declaradas de pacotes, permissões concedidas e status de usuários (User 0 / User 11). |
| **Telemetria de Memória** | `adb shell dumpsys meminfo` | Coleta de RSS/PSS por processo em múltiplas fases (inicial, pós-debloat básico, pós-degoogle e final). |
| **Armazenamento** | `adb shell df -h /data` | Verificação do espaço livre global em `/data` antes e depois das operações de desinstalação e limpeza de cache. |
| **AppOps Sandboxing** | `adb shell cmd appops set --uid <UID> <OP> ignore` | Neutralização de GPS, Activity Recognition e Body Sensors no Google Play Services (`UID 10387`) e serviços protegidos contra disable. |
| **Bloqueio no Kernel** | `adb shell cmd netpolicy add restrict-background-blacklist <UID>` | Bloqueio de tráfego de dados em segundo plano no firewall/netpolicy do Android para bloatwares persistentes. |
| **Restauração Cirúrgica** | `adb shell pm enable --user 0 <pacote>` | Reativação pontual de componentes de integridade (`com.android.vending`, `com.google.android.verifier`). |
| **Validação de Rede** | `adb shell ping -c 1 <host>` | Teste de resolução DNS e verificação de bloqueio de domínios de telemetria via NextDNS. |

---

## 3. Coleta Complementar e Validação Concluídas (09/11/2026)

Em 09 de novembro de 2026, com o dispositivo reconectado via Wireless ADB, foram sanadas as pendências canônicas de identificação:

```bash
# Confirmação canônica da versão do Android, SDK e compilação da ROM:
adb shell getprop ro.build.version.release       # Retorno: 17
adb shell getprop ro.build.version.sdk           # Retorno: 37
adb shell getprop ro.build.version.incremental   # Retorno: 7a1c2-08c719
adb shell getprop ro.build.fingerprint           # Retorno: motorola/cybert_g_sys/cybert:17/A171VVH.36-27/7a1c2-08c719:user/release-keys
adb shell getprop ro.soc.model                   # Retorno: MT6897 (Dimensity 8300)
```

### Validação Funcional de Integridade (Play Integrity API):
- **Incidente documentado:** Captura de tela do erro nos apps `br.gov.serpro.cnhe` e `br.gov.meugovbr` arquivada em `01-erro-play-integrity-cnh-gov.jpg`.
- **Procedimento e resolução:** Reativação dos pacotes de integridade via ADB com confirmação de funcionamento em tempo real. Consulte a documentação completa no [Estudo de Caso de Play Integrity](../case-study-play-integrity.md).

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
- `inventario-depois.json`: 501 pacotes com estado consolidado pós-debloat.
- `pacotes-desativados.txt`: Lista nominal histórica dos pacotes desativados.
- `pacotes-desinstalados.txt`: Registro dos 9 pacotes desinstalados para o usuário 0 e notas sobre reversão de atualizações em `/data/app`.
- `permissoes-alteradas.json`: 13 permissões runtime revogadas, 2 tentativas de permissão especial documentadas, 6 AppOps no GMS (`UID 10387`) e 7 pacotes em quarentena de netpolicy.
- `comparativo.json`: Tabela consolidada de métricas quantitativas de desempenho e status de testes.
- `01-erro-play-integrity-cnh-gov.jpg`: Captura de tela sanitizada evidenciando a falha de integridade em apps governamentais.
- `case-study-play-integrity.md`: Estudo de caso técnico forense detalhando o incidente, a reversão e a validação funcional.
