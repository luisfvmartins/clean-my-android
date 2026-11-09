# Códigos de Saída dos Scripts (Exit Codes)

Este documento descreve detalhadamente cada código de saída retornado pelos scripts utilitários do projeto **Clean My Android** (`debloat.sh`, `restore.sh` e `snapshot.sh`), especificando a causa do erro e a ação corretiva necessária.

---

## 1. `scripts/debloat.sh`

| Código | Significado | Condição de Disparo | Ação Recomendada |
|:---:|---|---|---|
| **0** | Sucesso / Sem alteração | Operação concluída com sucesso, modo somente leitura finalizado, `--help` exibido, cancelamento explícito pelo usuário ou pacote já desativado no Usuário 0. | Nenhuma ação necessária. |
| **1** | Falha de ambiente ADB | O binário `adb` não foi encontrado no `PATH`, ou o número de dispositivos conectados e autorizados é diferente de 1. | Instale o Android SDK Platform-Tools e garanta exatamente um dispositivo conectado e autorizado via `adb devices`. |
| **2** | Argumentos inválidos | Parâmetros incorretos passados na linha de comando ou sintaxe do nome do pacote incompatível com o padrão Android (ex.: `com.exemplo.app`). | Verifique os parâmetros com `./debloat.sh --help` e informe um nome canônico de pacote. |
| **3** | Bloqueio pelo Gate de Aplicação | O dispositivo conectado ou sua versão do Android não constam em `data/apply_support.tsv`. | A execução do `--apply` está restrita ao Moto G54 5G (Android 15) com homologação auditada. Em outros modelos, realize a auditoria em modo somente leitura. |
| **4** | Arquivo de configuração ausente | O arquivo de suporte `data/apply_support.tsv` ou a lista de pacotes essenciais `data/protected_essential_packages.txt` não foram localizados. | Execute o script a partir da raiz do repositório ou restaure os arquivos de configuração necessários. |
| **5** | Componente essencial protegido | O pacote solicitado consta em `data/protected_essential_packages.txt` como componente crítico do sistema operacional (ex.: telefonia, teclado, UI). | Intervenção bloqueada por segurança. O pacote não deve ser desativado para evitar instabilidade ou bootloop. |
| **6** | Pacote inexistente no aparelho | O pacote informado não foi encontrado pelo `pm path` no dispositivo alvo. | Verifique se o pacote está instalado com `adb shell pm list packages`. |
| **7** | Falha na verificação de estado | O comando de desativação foi executado, mas a verificação posterior com `pm list packages -d` não confirmou o estado desativado. | Inspecione logs do sistema (`logcat`) ou permissões de administração do dispositivo. |

---

## 2. `scripts/restore.sh`

| Código | Significado | Condição de Disparo | Ação Recomendada |
|:---:|---|---|---|
| **0** | Sucesso / Sem alteração | Pacote reativado com sucesso, `--help` exibido, cancelamento pelo usuário ou pacote já habilitado no Usuário 0. | Nenhuma ação necessária. |
| **1** | Falha de ambiente ADB | O binário `adb` não foi encontrado no `PATH`, ou o número de dispositivos conectados e autorizados é diferente de 1. | Conecte e autorize exatamente um dispositivo ADB. |
| **2** | Argumentos inválidos | Parâmetros ausentes/inválidos ou formato de pacote incorreto. | Use `./restore.sh PACOTE`. |
| **3** | Pacote inexistente no aparelho | O pacote não existe no firmware (`pm path` não localizou o APK). | Confirme se o nome do pacote está correto. |
| **4** | Falha na verificação de reativação | O comando `pm enable` foi executado, mas o pacote permaneceu listado como desativado. | Verifique permissões do ADB ou restrições impostas por perfil corporativo / MDM. |

---

## 3. `scripts/snapshot.sh`

| Código | Significado | Condição de Disparo | Ação Recomendada |
|:---:|---|---|---|
| **0** | Sucesso na captura e sanitização | Todas as evidências foram coletadas, estruturadas e aprovadas pelo validador de sanitização. | Evidências prontas para integração ao repositório. |
| **1** | Falha de ambiente ADB | Binário `adb` ausente ou número incorreto de dispositivos conectados. | Verifique a conexão com `adb devices`. |
| **2** | Argumentos inválidos | Parâmetros obrigatórios ausentes (`--label before\|after` ou `--out DIR`). | Consulte `./snapshot.sh --help` e informe rótulo e diretório de saída válidos. |
| **3** | Falha de comunicação ADB | Erro de comunicação ou timeout durante consultas de propriedades ou pacotes. | Reconecte o cabo USB e reinicie o servidor ADB (`adb kill-server`). |
| **4** | Falha na criação de diretório | Não foi possível criar o diretório de destino especificado em `--out`. | Verifique as permissões de escrita no sistema de arquivos. |
| **5** | Falha de sanitização pré-gravação | O validador detectou dados sensíveis (IMEI, endereços MAC, contas ou credenciais) nos arquivos temporários. | O script aborta a gravação para prevenir vazamento de dados privados. Inspecione e sanitize a saída antes de publicar. |
