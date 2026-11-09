# Política de Segurança — Clean My Android

A segurança dos dispositivos, a privacidade dos usuários e a integridade do sistema operacional são as diretrizes fundamentais do projeto **Clean My Android**.

Este documento define os procedimentos para reporte de vulnerabilidades, instruções técnicas perigosas ou vazamento acidental de dados pessoais.

---

## 1. Escopo de Segurança

Encorajamos o reporte responsável para qualquer um dos seguintes cenários:

1. **Instrução técnica perigosa ou risco de indisponibilidade:**
   - Comandos que causem *bootloop*, travamento permanente do sistema ou quebra irreversível sem root.
   - Presença de pacotes essenciais do sistema (telefonia, SMS, chamadas de emergência, STK, biometria, Play Store) em listas gerais de desativação (`data/*disabled*.txt`).
   - Comandos com parâmetros destrutivos (como `pm uninstall` sem salvaguardas ou exclusão de dados essenciais).
2. **Vazamento ou resíduo de dados pessoais (PII):**
   - Presença de identificadores de hardware (IMEI, MEID, número de série).
   - Identificadores de rede física (endereço MAC de Wi-Fi/Bluetooth, IP privado em contexto de rede).
   - Identificadores de usuário (número de telefone celular, conta de e-mail, nomes de contas pessoais).
3. **Falhas em scripts de automação:**
   - Evasão de gates de segurança (ex: execução forçada em aparelhos ou versões não suportadas).
   - Falhas no log JSONL ou comandos incorretos de reversão/recuperação.

---

## 2. Como Reportar com Responsabilidade

> [!CAUTION]
> **NÃO abra uma Issue pública** para reportar vazamento de dados pessoais ou instruções que possam comprometer dispositivos de usuários em produção.

Utilize os seguintes canais seguros:

1. **GitHub Private Vulnerability Reporting (Recomendado):**
   - Acesse a aba **Security** do repositório no GitHub.
   - Clique em **Report a vulnerability** para abrir um canal de discussão criptografado e privado diretamente com o mantenedor.
2. **Contato Direto com o Mantenedor:**
   - Entre em contato diretamente com o proprietário do repositório (`@luisfvmartins` via GitHub).

### O que incluir no reporte:
- Descrição clara da vulnerabilidade ou do dado exposto.
- Caminho do arquivo afetado no repositório (`caminho/do/arquivo:linha`).
- Em caso de instrução técnica perigosa: explicação do impacto funcional e comando de mitigação/reversão.
- **Importante:** Em caso de dado pessoal exposto, indique o arquivo e a categoria do dado, **sem reproduzir o valor sensível** na mensagem.

---

## 3. Prazos e Resposta

- **Triagem inicial:** resposta e confirmação de recebimento em até **48 horas**.
- **Ação emergencial de sanitização:** remoção ou mascaramento imediato do dado no repositório e registro formal em `docs/SANITIZATION_LOG.md`.
- **Correção técnica:** elaboração de patch, validação via suíte de testes e publicação transparente da correção.

---

## 4. Versões Suportadas

Correções de segurança são aplicadas estritamente na branch canônica atual:

| Branch / Versão | Suporte a Correções de Segurança |
|:---|:---:|
| `main` | :white_check_mark: Ativo |
| Branches de desenvolvimento | :warning: Conforme PR ativa |
