# Registro de Sanitização e Proteção de Privacidade (Sanitization Log)

> Este registro documenta todas as inspeções, higienizações e auditorias de dados sensíveis realizadas nos relatórios, evidências e inventários do repositório **Clean My Android**, em conformidade com as Regras Inegociáveis (Seção 1, Regra 3).

---

## 1. Diretrizes de Sanitização

Nenhum arquivo publicado no repositório pode conter dados que permitam identificar o proprietário do hardware, suas contas pessoais, credenciais ou a topologia da sua rede privada. As categorias monitoradas ativamente incluem:

| Categoria | Padrão / Tipo | Ação Exigida |
| :--- | :--- | :--- |
| **IMEI / IMSI** | 15 dígitos decimais com validação Luhn | Omissão total ou substituição por valor genérico |
| **Endereço MAC** | `XX:XX:XX:XX:XX:XX` | Substituído por `[REDACTED_MAC]` |
| **Número de Série** | `ro.serialno`, `ro.boot.serialno` | Omissão total das propriedades de serial |
| **Identificadores de Conta** | Estruturas de contas de usuário | Remoção de nomes de usuários e e-mails sincronizados |
| **Endereços IP Privados** | Sub-redes RFC 1918 | Ofuscação de rotas e conexões ativas |
| **Telefone / Contatos** | Números móveis e fixos brasileiros | Remoção total |
| **Metadados de Imagem** | Metadados EXIF em capturas de tela | Remoção integral via reprocessamento sem perdas |

---

## 2. Auditoria e Investigação de Falsos Positivos

### 2.1 Investigação de Padrões Numéricos em Arquivos `inventory.json`
* **Data da Inspeção:** 08/11/2026.
* **Contexto:** Uma varredura por expressões regulares identificou ocorrências no formato de 4 blocos numéricos em arquivos `inventory.json`.
* **Análise Técnica:** Todas as ocorrências foram analisadas individualmente em seu contexto JSON. Foi confirmado tecnicamente que **nenhuma** representa um endereço IP de rede; todas são sequências do campo de versão (`version_name`) atribuídas a aplicativos de sistema pré-instalados:
  * `reports/motorola/edge-60-fusion/before/inventory.json`: Linha 5227 — Versão do aplicativo Motorola Camera (MotCamera5).
  * `reports/motorola/edge-60-fusion/after/inventory.json`: Linha 2487 — Versão do aplicativo Motorola Camera (MotCamera5).
  * `reports/motorola/edge-60-pro/inventario-antes.json`: Linha 4442 — Versão do aplicativo de câmera Motorola.
  * `reports/samsung/galaxy-a30s/before/inventory.json`: Linhas 821, 1824, 4612, 5003 — Versões de aplicativos Samsung (Câmera/Galeria, Calendário, Clima e Gravador de Voz).
  * `reports/samsung/galaxy-a30s/after/inventory.json`: Linhas 917, 2038, 5154, 5591 — Mesmas versões de aplicativos.
* **Resolução:** Cadastradas formalmente com justificativa técnica individual em [data/sanitization_allowlist.json](../data/sanitization_allowlist.json).

### 2.2 Inspeção Visual e Metadados das Capturas de Tela (*Screenshots*)
* **Total de Imagens:** 7 arquivos PNG em `reports/samsung/galaxy-a30s/`.
* **Inspeção de Metadados EXIF:** Todas as 7 imagens foram processadas sem perda de qualidade visual para garantir a eliminação de quaisquer chunks ancilares ou metadados de geolocalização e data original da câmera.
* **Inspeção de Conteúdo Visual:**
  1. `before/screenshots/01_device_about.png`: Tela de bloqueio padrão (12:58, 8 de novembro, bateria 72%, "Chamadas de emergência", 3 ícones genéricos de sistema). **Sem dados pessoais, contas ou números expostos.**
  2. `before/screenshots/02_storage.png`: Captura preta/vazia (buffer em repouso durante a captura ADB). **Livre de dados sensíveis.**
  3. `before/screenshots/03_battery.png`: Captura preta/vazia. **Livre de dados sensíveis.**
  4. `before/screenshots/04_apps.png`: Captura preta/vazia. **Livre de dados sensíveis.**
  5. `after/screenshots/02_storage.png`: Tela de bloqueio pós-sessão (13:14, 8 de novembro, bateria 71%, "Somente chamadas de emergência"). **Sem dados pessoais, contas ou números expostos.**
  6. `after/screenshots/03_battery.png`: Captura preta/vazia. **Livre de dados sensíveis.**
  7. `after/screenshots/04_apps.png`: Captura preta/vazia. **Livre de dados sensíveis.**

---

## 3. Validador Automatizado no CI

A checagem contínua de sanitização foi integrada ao processo de integração contínua (CI) através do script executável [scripts/check_sanitization.py](../scripts/check_sanitization.py) e validada em [tests/test_sanitization.py](../tests/test_sanitization.py).

Qualquer nova adição de arquivo ao repositório contendo números de IMEI, endereços MAC reais, credenciais ou IPs privados que não estejam documentados na allowlist resultará em falha imediata da esteira de validação.
