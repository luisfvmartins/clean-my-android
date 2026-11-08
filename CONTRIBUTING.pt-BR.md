# Contribuindo com o Clean My Android

Contribuições são bem-vindas, especialmente auditorias de novos modelos, correções de documentação e melhorias de segurança nos scripts.

O objetivo é construir uma base pública e cumulativa: **cada Pull Request aprovado acrescenta conhecimento ao repositório principal sem apagar o trabalho anterior.**

## Forma recomendada de utilização

Para realizar uma auditoria de dispositivo, recomendamos utilizar um assistente de IA de sua escolha, como ChatGPT, Claude, Gemini, Antigravity, Codex ou equivalente. Não há dependência de um fornecedor específico.

O fluxo mais simples é clonar este repositório, abrir a pasta em um agente com acesso ao terminal/ADB e solicitar que leia [AI_INSTRUCTIONS.md](AI_INSTRUCTIONS.md) e o [guia de auditoria individual](docs/USER_DEVICE_AUDIT.md). Assim, o assistente pode conduzir as coletas, analisar os componentes, preparar um plano revisável, documentar o antes/depois e organizar a contribuição.

**A execução manual continua permitida** para quem possui conhecimento técnico de Android e ADB. A recomendação de IA não elimina a responsabilidade do usuário: nenhuma alteração no aparelho pode ocorrer sem autorização explícita, e toda contribuição deve ser revisada e sanitizada antes do envio.

## Tipos de contribuição

| Contribuição | Onde enviar |
|---|---|
| Auditoria de um novo aparelho | Nova pasta em `reports/` + atualização do índice |
| Complemento de uma auditoria existente | Pasta do mesmo aparelho, com revisão e data identificadas |
| Correção de documentação | Arquivo correspondente em `README.md`, `docs/` ou neste guia |
| Correção ou melhoria de script | `scripts/`, acompanhada de justificativa e validação |
| Nova lista de componentes protegidos | `data/`, com evidências e justificativa técnica |

## 1. Preparar fork e branch

Colaboradores sem acesso de escrita devem criar um fork pelo GitHub e trabalhar em uma branch exclusiva.

Com GitHub CLI:

```bash
gh auth login
gh repo fork luisfvmartins/clean-my-android --clone
cd clean-my-android
git remote add upstream https://github.com/luisfvmartins/clean-my-android.git
git remote -v
git switch -c audit/fabricante-modelo-android
```

Confirme:
- `origin` aponta para seu fork.
- `upstream` aponta para `luisfvmartins/clean-my-android`.
- A branch de trabalho não é `main`.

## 2. Preparar uma auditoria

Antes de qualquer alteração no aparelho, siga o [guia de auditoria individual](docs/USER_DEVICE_AUDIT.md) e as [instruções para IA](AI_INSTRUCTIONS.md).

Uma contribuição de dispositivo deve:
- identificar exatamente fabricante, modelo, codinome, Android/ROM e compilação quando disponíveis;
- registrar o estado inicial antes de alterar qualquer coisa;
- separar evidência observada, inferência técnica e hipótese;
- apresentar plano de alteração e riscos antes da execução;
- registrar apenas ações realmente autorizadas e executadas;
- repetir as medições depois, em condições comparáveis;
- documentar testes funcionais, limitações e reversões.

Não use inventário de outro aparelho como se fosse do seu. Não aplique listas de pacotes de outro modelo.

## 3. Organizar os arquivos

Crie uma pasta exclusiva seguindo a hierarquia `reports/<fabricante>/<modelo>/`, por exemplo:

```text
reports/samsung/galaxy-model/
├── README.md
├── auditoria.md
├── inventario-antes.json
├── inventario-depois.json
├── comparativo.json
└── evidencias/
    └── README.md
```

A estrutura é flexível. Inclua somente arquivos que existam e sejam úteis. Não crie arquivos vazios para aparentar uma coleta completa.

Atualize `reports/README.md` com uma linha para o aparelho. Não edite ou reorganize entradas de outros dispositivos sem necessidade.

## 4. Privacidade antes do envio

O repositório e os Pull Requests são públicos. Faça uma revisão completa dos arquivos e imagens.

Nunca publique:
- IMEI, MEID, número de série, identificadores de conta ou tokens;
- endereços MAC, IP público, hostname privado ou detalhes que exponham sua rede;
- números de telefone, e-mails, nomes de contatos ou notificações;
- dados de localização, contas sincronizadas ou informações pessoais;
- chaves de API, senhas, códigos de pareamento ou credenciais ADB.

Mantenha dumps brutos localmente. Compartilhe apenas os dados sanitizados necessários para sustentar as conclusões. A remoção posterior de um arquivo não garante que uma informação publicada deixe de estar acessível no histórico Git.

## 5. Revisar e enviar

```bash
git status --short
git diff --check
git diff
git add reports/SEU-DISPOSITIVO reports/README.md
git commit -m "docs(audit): add <fabricante-modelo> device report"
git push -u origin HEAD
gh pr create --repo luisfvmartins/clean-my-android --base main
```

Adapte o caminho e a mensagem de commit aos arquivos realmente alterados. Para contribuições apenas documentais ou de scripts, adicione os arquivos correspondentes ao `git add`.

## 6. Critérios de revisão

Um Pull Request pode ser solicitado para ajustes ou recusado quando:
- não identifica claramente o aparelho e a versão do sistema;
- mistura dados observados com suposições;
- apresenta métricas sem método ou condições de coleta;
- omite riscos, efeitos colaterais ou formas de recuperação;
- recomenda alterações perigosas ou universais;
- contém dados pessoais, credenciais ou identificadores;
- sobrescreve ou remove a contribuição de outro dispositivo;
- não atualiza o catálogo quando adiciona uma auditoria.

A abertura do PR não representa aprovação automática. Após a revisão e o merge, os arquivos passam a integrar a coleção oficial na branch `main`.

## Links úteis

- [Guia de auditoria individual](docs/USER_DEVICE_AUDIT.md)
- [Catálogo de dispositivos](reports/README.md)
- [Instruções para assistentes de IA](AI_INSTRUCTIONS.md)
- [Repositório no GitHub](https://github.com/luisfvmartins/clean-my-android)

## 7. Validação automática

Pull Requests direcionados à `main` executam o workflow **Validação do repositório**. Ele verifica:

- sintaxe de todos os arquivos JSON versionados;
- estrutura básica dos arquivos `comparativo.json` (quando possuem o campo `metrics`);
- sintaxe Bash dos scripts em `scripts/*.sh`, sem executá-los;
- formato e duplicidade dos pacotes em `data/protected_essential_packages.txt`.

A validação é somente estática: não conecta via ADB, não instala dependências no aparelho e não altera dispositivos. Um resultado aprovado não substitui revisão técnica, checagem de privacidade nem testes funcionais. Corrija as falhas indicadas no log do GitHub Actions e atualize o mesmo Pull Request.
