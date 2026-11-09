# Matriz de Compatibilidade e Suporte de Plataformas

Este documento detalha o suporte e os requisitos de ambiente operacional para execução dos scripts utilitários do **Clean My Android** (`debloat.sh`, `restore.sh` e `snapshot.sh`).

---

## 1. Ambientes Suportados

| Sistema Operacional | Shell / Runtime | Status de Teste | Suporte Oficial | Notas de Portabilidade |
|---|---|:---:|:---:|---|
| **Linux (Ubuntu, Debian, Fedora, Arch, etc.)** | GNU Bash 4.x / 5.x | Testado em CI e local | **Suportado** | Execução padrão com suporte nativo a pipes e ferramentas POSIX. |
| **macOS (Sonoma, Sequoia, etc.)** | Apple `/bin/bash` 3.2.57 | Testado em CI (`macos-latest`) | **Suportado** | Compatível com Bash 3.2. Sem dependência de `mapfile`, `declare -A` ou flags exclusivas GNU. |
| **Windows 10 / 11 (WSL2)** | Bash no Ubuntu/Debian via WSL2 | Testado pela comunidade | **Recomendado para Windows** | Requer encaminhamento da porta ADB do host Windows para o WSL2 (`usbipd-win` ou ADB server compartilhado). |
| **Windows 10 / 11 (Git Bash / MSYS2)** | Bash emulado no Windows | **Não testado em hardware físico** | Experimental / Comunitário | Requer atenção à conversão automática de caminhos de arquivos e quebras de linha CRLF. |
| **Windows (PowerShell / CMD nativo)** | N/A | **Não suportado** | Não suportado | Os scripts utilizam sintaxe Bash e chamadas POSIX. Não há script `.bat` ou `.ps1` nativo. |

---

## 2. Requisitos de Ferramentas e Dependências

Para executar os scripts utilitários em qualquer plataforma suportada:
1. **Bash 3.2 ou superior:** Presente nativamente em sistemas Linux e macOS.
2. **Android SDK Platform-Tools (`adb`):** O binário `adb` deve estar devidamente instalado e acessível através da variável de ambiente `PATH`.
3. **Python 3.10 ou superior:** Necessário para validação de integridade do repositório (`validate_repository.py`) e sanitização de evidências. Não é exigido para a execução dos scripts de alteração no aparelho pelo usuário.

---

## 3. Seleção de Idioma (`CMA_LANG`)

Os scripts suportam internacionalização nativa (Português do Brasil e Inglês).
* Por padrão, o idioma é inferido a partir das variáveis de ambiente do sistema (`LANG` ou `LC_ALL`).
* É possível forçar o idioma definindo a variável `CMA_LANG`:
  ```bash
  # Forçar saída em inglês:
  CMA_LANG=en ./scripts/debloat.sh

  # Forçar saída em português:
  CMA_LANG=pt ./scripts/debloat.sh
  ```
