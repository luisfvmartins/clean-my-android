# Protocolo Técnico de Medição de Recursos em Dispositivos Android

Este protocolo estabelece o método científico, rigoroso e reproduzível para coleta, mensuração e documentação de indicadores de desempenho de hardware e consumo de recursos (`kind: resource`) no projeto **Clean My Android**.

> [!IMPORTANT]
> **Regra de integridade:** Nenhuma métrica quantitativa de RAM, bateria, temperatura ou tempo de boot pode ser inferida ou preenchida em `metrics.json` sem a captura e arquivamento prévio da respectiva saída bruta (`raw dump`) no repositório. Métricas pendentes devem ser mantidas como `not_measured`.

---

## 1. Condições de Controle Experimental

Para garantir que a variação observada decorra estritamente das ações de debloat e não de variáveis espúrias do ambiente, todos os testes comparativos ("antes" e "depois") devem obedecer às mesmas condições de contorno:

| Parâmetro | Condição Controlada Obrigatória | Justificativa Técnica |
| :--- | :--- | :--- |
| **Temperatura ambiente** | 22°C a 25°C em repouso térmico | A temperatura ambiente afeta diretamente o *thermal throttling* do SoC e a perda de eficiência da bateria de lítio. |
| **Nível de carga inicial** | 100% de carga com cabo desconectado | Baterias de íon-lítio apresentam curvas de tensão não lineares em diferentes faixas de carga. |
| **Conectividade** | Wi-Fi fixo (mesma rede/banda 5 GHz) ou Modo Avião | Variações na intensidade de sinal celular (RSSI/RSRP) forçam o modem a aumentar a potência de transmissão, distorcendo o consumo. |
| **Brilho da tela** | Fixo em 50% (para testes de tela ativa) ou tela desligada (em repouso) | A tela OLED/IPS é o maior consumidor individual de energia de um smartphone. |
| **Período de assentamento** | Exatamente 5 minutos pós-boot | Evita capturar picos transitórios de inicialização de daemons e compilação JIT/ART. |
| **Número de repetições** | Mínimo de $N \ge 3$ medições por estado | Permite calcular média aritmética e desvio padrão, atestando significância estatística. |

---

## 2. Roteiro Passo a Passo de Coleta

### 2.1 Memória RAM Ociosa (`dumpsys meminfo`)

1. Reiniciar o smartphone a frio:
   ```bash
   adb reboot
   ```
2. Aguardar a conclusão da inicialização:
   ```bash
   adb wait-for-device
   adb shell 'while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 2; done'
   ```
3. Aguardar o repouso térmico e de inicialização de 5 minutos (300 segundos).
4. Executar 3 medições com intervalo de 60 segundos entre elas, salvando a saída bruta:
   ```bash
   # Medição 1
   adb shell dumpsys meminfo > evidence/raw-meminfo-run1.txt
   sleep 60
   # Medição 2
   adb shell dumpsys meminfo > evidence/raw-meminfo-run2.txt
   sleep 60
   # Medição 3
   adb shell dumpsys meminfo > evidence/raw-meminfo-run3.txt
   ```
5. Extrair os valores consolidados:
   - `Total RAM`
   - `Free RAM` (RAM livre física + buffers)
   - `Used RAM` (PSS total de processos residentes)
   - `Lost RAM`
6. Calcular a média das 3 coletas para compor os campos `before` e `after` de `metrics.json`.

---

### 2.2 Tempo de Inicialização do Sistema (Boot Time)

1. Registrar as marcas temporais do kernel e do init do Android:
   ```bash
   adb shell getprop ro.boottime.init
   adb shell getprop ro.boottime.init.cold_boot_done
   ```
2. Executar 3 ciclos completos de reinicialização a frio cronometrados a partir do evento de reinício até o sinalizador `sys.boot_completed=1`:
   ```bash
   date +%s%N
   adb reboot && adb wait-for-device shell 'while [ "$(getprop sys.boot_completed)" != "1" ]; do sleep 0.5; done'; date +%s%N
   ```
3. Salvar os registros e calcular a média aritmética do tempo total de boot em segundos.

---

### 2.3 Armazenamento da Partição de Dados (`df /data`)

1. Coletar a utilização em blocos e espaço disponível:
   ```bash
   adb shell df -k /data > evidence/raw-df-data.txt
   ```
2. Converter a variação para gigabytes (GB):
   $$\Delta \text{Livre} = \frac{\text{Available}_{\text{after}} - \text{Available}_{\text{before}}}{1024 \times 1024} \text{ GB}$$
3. Documentar expressamente que o valor reflete a variação agregada da partição `/data` (incluindo expurgo de atualizações em `/data/app` e caches), e que ganhos individuais por pacote não devem ser somados de forma independente.

---

### 2.4 Autonomia e Comportamento Térmico em Repouso [Protocolo de 24 Horas](MEASUREMENT_PROTOCOL.pt-BR.md)

1. Carregar o dispositivo até 100% e desconectar o carregador.
2. Limpar os contadores de bateria:
   ```bash
   adb shell dumpsys batterystats --reset
   ```
3. Coletar o estado inicial da bateria e temperatura:
   ```bash
   adb shell dumpsys battery > evidence/raw-battery-initial.txt
   ```
4. Manter o dispositivo em repouso com tela apagada durante **24 horas contínuas** [sob condições controladas](MEASUREMENT_PROTOCOL.pt-BR.md) controladas da Seção 1.
5. Decorridas exatamente 24 horas [conforme roteiro](MEASUREMENT_PROTOCOL.pt-BR.md), conectar via ADB e extrair a telemetria consolidada:
   ```bash
   adb shell dumpsys battery > evidence/raw-battery-final.txt
   adb shell dumpsys batterystats > evidence/raw-batterystats-24h.txt
   ```
6. Calcular a taxa horária de descarga em repouso:
   $$\text{Descarga Ociosa} = \frac{\text{Level}_{\text{initial}} - \text{Level}_{\text{final}}}{24} \text{ \%/hora}$$
7. Inspecionar o tempo em *Deep Sleep* e *Partial Wake Locks* para comprovar se daemons de telemetria desativados impediam o repouso profundo do processador.

---

## 3. Formatação Canônica em `metrics.json`

Após a conclusão dos testes com evidências salvas em `evidence/`, preencher o indicador em `metrics.json`:

```json
{
  "indicator": "Consumo de Bateria e Comportamento Térmico Contínuo",
  "kind": "resource",
  "status": "measured",
  "before": "Descarga de X%/h em repouso de 24h a 35°C",
  "after": "Descarga de Y%/h em repouso de 24h a 31°C",
  "variation": "Redução observada de Z%/h no consumo ocioso",
  "method": "dumpsys batterystats e dumpsys battery em repouso controlado de 24h",
  "evidence": [
    "reports/<fabricante>/<modelo>/evidence/raw-battery-initial.txt",
    "reports/<fabricante>/<modelo>/evidence/raw-battery-final.txt",
    "reports/<fabricante>/<modelo>/evidence/raw-batterystats-24h.txt"
  ],
  "limitations": "Medição em repouso de 24h em ambiente a 23°C; não reflete uso sob tela ativa contínua."
}
```
