<div align="center">

# Clean My Android

**Auditoria técnica, debloat criterioso e documentação de privacidade para dispositivos Android.**

[![Android](https://img.shields.io/badge/Android-dispositivos%20auditados-3DDC84?logo=android&logoColor=white)](reports/README.md)
[![ADB](https://img.shields.io/badge/ADB-required-3C78A8)](https://developer.android.com/tools/adb)
[![Root](https://img.shields.io/badge/Root-n%C3%A3o%20necess%C3%A1rio-2E8B57)](docs/USER_DEVICE_AUDIT.md)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

[Começar](#começar) · [Como funciona](#como-funciona) · [Dispositivos auditados](reports/README.md) · [Contribuir](CONTRIBUTING.md) · [Segurança](#segurança-em-primeiro-lugar)

</div>

---

## O projeto

O **Clean My Android** é um projeto de código aberto para investigar o que existe em um dispositivo Android, entender a função de seus componentes e documentar alterações de forma cuidadosa e verificável.

A proposta vai além de desativar aplicativos pré-instalados. Cada auditoria procura registrar o estado do aparelho **antes e depois**, explicar o que foi alterado, apresentar evidências, medir resultados quando possível e deixar claras as limitações dos testes.

O projeto segue a inspiração colaborativa do [CleanYourTV](https://github.com/Gathin23/cleanyourtv): conhecimento específico por modelo, documentação reproduzível e contribuições incorporadas ao repositório principal por Pull Requests.

> **Importante:** Android não é igual em todos os aparelhos. Fabricante, modelo, região, firmware, versão do Android e configuração do usuário mudam o comportamento dos pacotes. Uma recomendação nunca deve ser tratada como universal.

## Começar

O primeiro contato com o projeto deve ser uma **inspeção sem alterações**.

### Requisitos

- Linux, macOS ou Windows com Android Debug Bridge (ADB) instalado.
- Depuração USB ou sem fio habilitada no aparelho.
- Computador autorizado pelo Android.
- Exatamente um dispositivo conectado e autorizado para executar o script.

### 1. Obter o projeto

```bash
git clone https://github.com/luisfvmartins/clean-my-android.git
cd clean-my-android
```

### 2. Inspecionar o dispositivo

```bash
adb devices -l
./scripts/debloat.sh
```

O modo padrão identifica o aparelho e lista os pacotes desativados para o usuário principal. **Não realiza alterações.**

### 3. Alterações: somente quando houver suporte explícito

O modo de aplicação do script está restrito ao **Motorola Moto G54 5G com Android 15**, exige confirmação digitada e atua sobre um pacote por execução:

```bash
./scripts/debloat.sh --apply nome.do.pacote
```

Não use esse comando em outro modelo ou versão do Android. A lista de componentes protegidos é uma barreira adicional, não uma garantia de que todo pacote fora dela seja seguro para desativação.

Para reativar individualmente um pacote que foi desativado:

```bash
./scripts/restore.sh nome.do.pacote
```

Leia o [guia de auditoria individual](docs/USER_DEVICE_AUDIT.md) antes de executar qualquer alteração ou preparar uma contribuição.

## Como funciona

O fluxo recomendado é dividido em etapas independentes. Diagnóstico e coleta vêm antes de qualquer mudança.

| Etapa | Objetivo | Resultado esperado |
|---|---|---|
| **1. Identificação** | Registrar modelo, codinome, Android, firmware e ambiente | Identificação verificável do dispositivo |
| **2. Estado inicial** | Coletar pacotes, permissões, AppOps e métricas disponíveis | Inventário "antes" |
| **3. Análise** | Investigar função, dependências, evidências e riscos | Classificação técnica por componente |
| **4. Plano** | Apresentar alterações propostas e formas de reversão | Plano revisável pelo proprietário |
| **5. Aplicação autorizada** | Executar somente ações aprovadas e compatíveis | Registro das alterações realizadas |
| **6. Estado final** | Repetir as coletas em condições comparáveis | Inventário "depois" |
| **7. Comparação** | Confrontar dados, testes e limitações | Relatório técnico antes/depois |
| **8. Publicação** | Sanitizar e enviar a contribuição por Pull Request | Nova auditoria no catálogo público |

O [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) contém instruções para assistentes de IA. A IA deve analisar evidências, explicar riscos e aguardar autorização explícita antes de modificar o dispositivo.

## Dispositivos auditados

As auditorias são específicas por aparelho e possuem diferentes níveis de validação. Consulte o [catálogo de dispositivos](reports/README.md) para conhecer o escopo, os arquivos e as pendências de cada relatório.

| Dispositivo | Documentação | Situação |
|---|---|---|
| Motorola Moto G54 5G (XT2343-1) | [Auditoria técnica](docs/AUDITORIA_MOTO_G54_5G.md) | Inventário publicado; consulte o relatório para escopo e limitações |
| Motorola Edge 60 Pro (XT2507-1) | [Relatório e evidências](reports/motorola-edge-60-pro/) | Validação funcional e confirmação de alguns dados pendentes |

**A presença de um aparelho no catálogo não significa que todos os procedimentos estejam homologados para ele.** A compatibilidade de scripts é indicada separadamente e não deve ser inferida a partir de um relatório.

## O que cada auditoria deve documentar

- **Identificação:** fabricante, modelo, codinome, versão do Android/ROM e compilação.
- **Inventário:** pacotes do sistema e do usuário, estado, versão e origem quando disponíveis.
- **Permissões e AppOps:** o que está declarado, concedido ou efetivamente configurado.
- **Análise de componentes:** função conhecida, evidência, dependências e risco de alteração.
- **Alterações:** comandos executados, autorização, resultado e método de reversão.
- **Comparativo:** métricas antes/depois coletadas em condições equivalentes.
- **Testes funcionais:** telefonia, conectividade, câmera, biometria, notificações, bancos e outros recursos relevantes, quando aplicável.
- **Limitações:** dados não coletados, testes não realizados e conclusões inconclusivas.

Resultados sem evidência devem ser identificados como **não mensurados**, **não coletados** ou **pendentes de validação**. Não transforme estimativas em resultados comprovados.

## Segurança em primeiro lugar

Este projeto prioriza reversibilidade, transparência e controle do proprietário do aparelho.

- Inspecionar é diferente de alterar: o modo padrão dos scripts é somente leitura.
- A aplicação disponível no script é individual, exige confirmação e possui restrição de dispositivo/versão.
- Não há desinstalação em lote, limpeza de dados ou remoção automática de perfis nos scripts atuais.
- Não desative componentes críticos de Android, telefonia, conectividade, criptografia, instalação de pacotes ou segurança.
- Não conclua que um aplicativo é espião apenas por ter acesso à internet, pertencer ao fabricante ou possuir SDK analítico.
- AppOps por UID pode afetar vários pacotes que compartilham o mesmo UID; não aplique regras sem mapear os vínculos e os efeitos.
- Não publique inventários brutos, identificadores, tokens, contas, notificações ou dados pessoais.

**Não existe garantia universal de ganho de bateria, RAM, armazenamento, privacidade ou compatibilidade bancária.** Esses efeitos dependem do aparelho e precisam ser medidos. Alterações podem causar perda de funções; mantenha uma forma de recuperação disponível.

Consulte também [docs/USER_DEVICE_AUDIT.md](docs/USER_DEVICE_AUDIT.md) e [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md).

## Estrutura do repositório

```text
.
├── AI_INSTRUCTIONS.md       # Instruções para auditoria assistida por IA
├── data/                    # Inventários e listas de proteção
├── docs/                    # Guias e auditorias técnicas
├── reports/                 # Relatórios por dispositivo
└── scripts/                 # Inspeção, desativação e restauração
```

## Como contribuir

Cada dispositivo deve ter sua própria pasta em `reports/`. A contribuição deve preservar os relatórios existentes e acrescentar documentação ao catálogo.

1. Leia [CONTRIBUTING.md](CONTRIBUTING.md) e [docs/USER_DEVICE_AUDIT.md](docs/USER_DEVICE_AUDIT.md).
2. Faça um fork e crie uma branch exclusiva para sua contribuição.
3. Colete e sanitize os dados do seu próprio aparelho.
4. Inclua o relatório, inventários e evidências necessários.
5. Atualize o índice de dispositivos em `reports/README.md`.
6. Abra um Pull Request para a branch `main`.

Cada Pull Request aprovado e integrado amplia a base pública de conhecimento. Não altere nem substitua a auditoria de outro dispositivo para incluir a sua.

## Documentação e links

- [Catálogo de auditorias](reports/README.md)
- [Guia de auditoria individual](docs/USER_DEVICE_AUDIT.md)
- [Instruções para IA](AI_INSTRUCTIONS.md)
- [Contribuição e Pull Requests](CONTRIBUTING.md)
- [Código-fonte](https://github.com/luisfvmartins/clean-my-android)
- [Licença MIT](LICENSE)

---

<div align="center">

**Auditorias reais. Evidências verificáveis. Alterações conscientes.**

</div>
