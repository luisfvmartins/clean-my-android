# Metodologia de Classificação de Componentes e Hierarquia de Evidências

Este documento estabelece a metodologia técnica padrão para identificação, classificação de risco, determinação de dependências e atribuição de níveis de confiança aos componentes de software documentados no projeto **Clean My Android**.

---

## 1. Princípio Fundamental

> [!IMPORTANT]
> **Conhecimento prévio ou memória de modelo de IA não constitui fonte nem evidência.**
> Qualquer alegação de finalidade, risco ou dependência sem sustentação direta em evidência de arquivo, código-fonte público ou saída bruta de comando ADB é compulsoriamente classificada com nível de confiança **`low` (baixa)** e marcada como **não verificada (`unverified`)** até confirmação forense.

---

## 2. Hierarquia Estrita de Fontes

Para garantir reprodutibilidade e afastar inferências sem base técnica, a determinação da finalidade de um pacote obedece à seguinte ordem hierárquica decrescente de autoridade:

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Código-fonte oficial AOSP (cs.android.com)               │
├─────────────────────────────────────────────────────────────┤
│ 2. Documentação oficial da fabricante ou do SoC             │
├─────────────────────────────────────────────────────────────┤
│ 3. Análise forense de manifesto e dumpsys package           │
├─────────────────────────────────────────────────────────────┤
│ 4. Comportamento operacional observado no dispositivo       │
├─────────────────────────────────────────────────────────────┤
│ 5. Fontes secundárias da comunidade (UAD, XDA, F-Droid)     │
└─────────────────────────────────────────────────────────────┘
```

### Nível 1: Código-fonte oficial do AOSP (`cs.android.com` / `android.googlesource.com`)
- **Autoridade máxima** para componentes da base Android, provedores essenciais (`providers.*`), módulos de telefonia, subsistemas de permissões e infraestrutura do sistema.
- Permite verificar diretamente a declaração de intents, receptores de broadcast protegidos (`protected-broadcast`), flags de inicialização e tratamento de exceções.

### Nível 2: Documentação oficial da fabricante (OEM) ou do SoC
- Manuais técnicos, portais de desenvolvedores da Motorola/Lenovo, Samsung Knox SDK, MediaTek Dimensity Software Architecture e Qualcomm Developer Network.
- Utilizada para componentes específicos da interface (Hello UI, One UI), drivers proprietários de câmera/áudio e daemons de integração de rádio (RIL/IMS).

### Nível 3: Análise forense de manifesto e inspeção técnica via ADB
- Extração de `dumpsys package <pacote>` e descompilação de `AndroidManifest.xml` (AXML).
- Permite verificar com certeza matemática:
  - **Identificador de Usuário Compartilhado (`sharedUserId`):** pacotes que rodam sob o mesmo UID compartilham permissões de sistema e podem quebrar se desativados em conjunto.
  - **Permissões de sistema (`protectionLevel: signature|privileged`):** revelam o escopo real de privilégios.
  - **Serviços vinculados (`Services/Providers`):** identifica clientes que consomem o componente via IPC (Binder).
  - **Flags de instalação:** `FLAG_SYSTEM`, `FLAG_UPDATED_SYSTEM_APP`, `FLAG_STOPPED`.

### Nível 4: Comportamento operacional observado no dispositivo
- Testes de execução sob condições controladas:
  - Telemetria de memória (`dumpsys meminfo <pacote>`).
  - Verificação de conexões ativas de rede (`dumpsys netstats` / `netpolicy`).
  - Resposta a tentativas de encerramento (`pm disable-user`, `am force-stop`).
  - Testes funcionais de estresse em chamadas de voz, envio/recebimento de SMS, autenticação biométrica e aplicativos bancários.

### Nível 5: Fontes secundárias da comunidade (UAD, XDA, F-Droid)
- Tratadas **exclusivamente como hipóteses de trabalho preliminares**, jamais como prova técnica definitiva.
- Listas de debloat comunitárias (como repositórios Universal Android Debloater ou discussões no XDA) frequentemente generalizam classificações entre versões de Android ou modelos regionais distintos, demandando verificação independente antes de qualquer ação.

---

## 3. Níveis de Confiança (`Confidence Levels`)

Cada pacote classificado no repositório recebe um atributo formal de confiança:

| Nível de Confiança | Requisitos Mínimos de Evidência | Status Permitido |
| :--- | :--- | :--- |
| **`high` (Alta)** | Sustentado por código AOSP (Nível 1) ou documentação oficial do fabricante (Nível 2), confirmado por manifesto/dumpsys (Nível 3) e teste funcional real (Nível 4). | Homologado para análise técnica e documentação. |
| **`medium` (Média)** | Sustentado por análise detalhada de manifesto e dumpsys (Nível 3) com comportamento operacional condizente (Nível 4), na ausência de documentação pública formal do fabricante. | Válido para relatório, com limitações registradas. |
| **`low` (Baixa)** | Baseado predominantemente em hipóteses da comunidade (Nível 5) ou inferência de nomenclatura sem evidência de manifesto extraída na sessão. | Compulsoriamente rotulado como `unverified` / pendente. |

---

## 4. Requisitos para Pacotes Efetivamente Alterados

Para cada componente desativado (`pm disable-user`) ou removido (`pm uninstall --user 0`) em qualquer aparelho, o relatório técnico correspondente deve obrigatoriamente registrar:

1. **Nome técnico canônico (`Package Name`):** identificador exato no formato FQPN (ex: `com.motorola.motocare`).
2. **Origem do componente:** AOSP stock, OEM (Motorola/Samsung), parceiro comercial patrocinado ou fornecedor de chipset (MediaTek/Qualcomm).
3. **Motivo técnico da intervenção:** telemetria redundante, publicidade, consumo indevido de recursos, ou ausência de utilidade pessoal.
4. **Dependências verificadas:** ausência de impacto em serviços essenciais do sistema e verificação de `sharedUserId`.
5. **Comando de reversão:** linha de comando exata para restabelecimento imediato (`pm enable` ou `cmd package install-existing`).
6. **Resultado funcional observado:** comportamento verificado no aparelho após a modificação (ex: "processo finalizado na RAM; integridade do sistema operacional preservada").

Caso qualquer um desses itens não tenha sido mensurado durante a coleta original, o campo deve ser formalmente preenchido como `not_measured` ou `pending`, sem qualquer suposição ou texto artificial.

---

## 5. Procedimento de Autoauditoria por Amostragem

Periodicamente, o projeto executa auditorias por amostragem probabilística:
1. **Semente pseudoaleatória documentada (`seed`):** seleção reproduzível de pacotes do catálogo geral.
2. **Reverificação contra fontes primárias:** cada pacote sorteado é reexaminado contra AOSP, documentação do fabricante e inventário de manifesto.
3. **Emissão de relatório de veredicto:** publicação de documento com a classificação original, fonte primária consultada, veredicto (*Concordo*, *Discordo* ou *Evidência Insuficiente*) e ação corretiva implementada em caso de discordância.
