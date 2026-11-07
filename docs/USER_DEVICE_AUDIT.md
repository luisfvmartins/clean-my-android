# Auditoria individual do dispositivo Android

Este documento orienta cada colaborador do **Clean My Android** a preparar uma contribuição por Pull Request (PR), registrar o estado do aparelho antes das alterações, documentar cada intervenção e produzir um relatório comparativo depois da otimização.

O objetivo é criar um histórico técnico individual, verificável e reproduzível — não apenas uma lista de aplicativos removidos.

> **Princípio central:** nenhum resultado pode ser inventado. Toda métrica deve indicar método, condição de coleta e evidência. Quando não for possível medir, registrar como "Não mensurado" ou "Inconclusivo".

## 1. Fluxo recomendado

1. Criar um fork próprio do repositório (para colaboradores sem acesso de escrita) e preparar uma branch de contribuição.
2. Preparar uma pasta individual para o dispositivo.
3. Fazer o diagnóstico inicial, sem modificar o aparelho.
4. Salvar inventários, métricas, logs e capturas de tela.
5. Analisar os pacotes e apresentar um plano de alterações.
6. Obter autorização explícita antes de cada grupo de alterações.
7. Executar as mudanças de forma controlada e registrar os resultados.
8. Repetir as coletas iniciais nas mesmas condições.
9. Gerar o relatório comparativo.
10. Revisar e sanitizar os arquivos, enviar a branch ao fork e abrir um Pull Request para o repositório original.

## 2. Preparar seu fork e a contribuição

### Pelo GitHub

1. Acesse https://github.com/luisfvmartins/clean-my-android.
2. Entre na sua conta GitHub.
3. Clique em **Fork**.
4. Selecione sua conta como destino.
5. Mantenha o nome do repositório ou escolha outro.
6. Confirme a criação.

Seu fork ficará disponível em `https://github.com/SEU_USUARIO/clean-my-android`.

### Pelo GitHub CLI

Com o GitHub CLI instalado e autenticado:

```bash
gh auth login
gh repo fork luisfvmartins/clean-my-android --clone
cd clean-my-android
git remote add upstream https://github.com/luisfvmartins/clean-my-android.git
git remote -v
```

Confirme que `origin` aponta para seu fork e que `upstream` aponta para o repositório original:

### Privacidade

O repositório original é público. Não presuma que o fork será privado. Inventários e capturas podem revelar modelo, aplicativos pessoais, operadora, identificadores, notificações e hábitos de uso.

- Não publique IMEI, número de série, endereços MAC, tokens, credenciais, contas ou dados pessoais.
- Revise capturas de tela e logs antes de enviar.
- Mantenha os dados brutos localmente ou em repositório privado.
- Inclua no Pull Request somente relatórios e evidências sanitizados e necessários à revisão.
- O PR será enviado ao repositório original para análise; isso não significa que será aceito ou incorporado.

## 3. Estrutura de arquivos por dispositivo

Crie um diretório com nome descritivo, sem identificadores pessoais. Exemplo:

```text
reports/
└── motorola-edge-60-pro-android-16/
    ├── README.md
    ├── before/
    │   ├── device-info.txt
    │   ├── packages.txt
    │   ├── permissions.txt
    │   ├── appops.txt
    │   ├── users.txt
    │   ├── memory.txt
    │   ├── storage.txt
    │   ├── battery.txt
    │   ├── processes.txt
    │   ├── network.txt
    │   └── screenshots/
    ├── changes/
    │   ├── change-log.md
    │   ├── disabled-packages.txt
    │   ├── removed-packages.txt
    │   ├── permission-changes.txt
    │   └── appops-changes.txt
    ├── after/
    │   ├── device-info.txt
    │   ├── packages.txt
    │   ├── permissions.txt
    │   ├── appops.txt
    │   ├── users.txt
    │   ├── memory.txt
    │   ├── storage.txt
    │   ├── battery.txt
    │   ├── processes.txt
    │   ├── network.txt
    │   └── screenshots/
    └── comparison-report.md
```

A estrutura é uma referência. Não crie arquivos vazios para aparentar que uma coleta foi realizada. Registre limitações quando uma informação não estiver disponível.

## 4. Diagnóstico inicial — ANTES

Antes de qualquer alteração, identifique o dispositivo e registre o estado original.

### 4.1 Identificação

Coletar, quando disponível:

- Fabricante, modelo e codinome.
- Versão do Android, ROM/interface e compilação.
- Patch de segurança e versão do kernel.
- Arquitetura, processador e núcleos.
- RAM total e armazenamento total.
- Estado do bootloader e presença de root.
- Disponibilidade de ADB, Shizuku e Magisk.
- Usuários e perfis Android existentes.

Não incluir IMEI, número de série ou identificadores persistentes no relatório público.

### 4.2 Inventário de aplicativos e pacotes

Registrar:

- Pacotes de sistema e de usuário.
- Pacotes habilitados e desabilitados.
- Nome do pacote, nome legível e versão.
- UID quando necessário à análise.
- Caminho/origem de instalação, quando disponível.
- Permissões declaradas e concedidas, separadamente.
- AppOps relevantes.
- Serviços e componentes importantes.
- Execução em segundo plano e dependências conhecidas.

### 4.3 Recursos e desempenho

| Categoria | Dados a coletar |
|---|---|
| Hardware | Processador, núcleos, RAM e armazenamento |
| Sistema | Android, ROM, kernel e patch de segurança |
| Memória | RAM total, usada, disponível e pressão de memória, se disponível |
| Armazenamento | Total, ocupado e livre |
| Bateria | Nível, temperatura, estado e estatísticas disponíveis |
| Processos | Processos e serviços relevantes |
| Aplicativos | Quantidade por categoria e estado |
| Rede | DNS, conectividade e restrições configuradas |
| Privacidade | Permissões, AppOps e componentes com acesso sensível |
| Segurança | Root, bootloader e verificações de integridade disponíveis |

### 4.4 Condições de medição

Para permitir uma comparação justa, anote:

- Data e hora.
- Nível da bateria.
- Se estava carregando.
- Tela ligada ou desligada.
- Aplicativos abertos.
- Tempo desde a última reinicialização.
- Tipo de conexão de rede.
- Temperatura ambiente, se conhecida.
- Comando ou método usado para obter cada métrica.

RAM livre, temperatura e consumo de bateria variam com o uso. Uma única leitura não comprova melhoria sustentada.

## 5. Capturas de tela

Quando possível, registrar imagens equivalentes antes e depois:

- Informações do telefone e versão Android.
- Armazenamento.
- Memória.
- Bateria.
- Aplicativos instalados.
- Permissões e privacidade.
- Configurações de rede/DNS.
- Funcionalidades importantes do aparelho.

Salvar em `before/screenshots/` e `after/screenshots/`, mantendo nomes equivalentes para facilitar a comparação.

As capturas devem ser legíveis, mostrar contexto e não ser manipuladas para sugerir resultados. Oculte notificações, mensagens, contas, números, localização e qualquer dado pessoal antes de publicar.

Se a captura não puder ser obtida, registre a limitação.

## 6. Registro das alterações

Toda alteração deve ser documentada em `changes/change-log.md`, incluindo:

| Campo | O que registrar |
|---|---|
| Data/hora | Momento da alteração |
| Pacote | Nome exato |
| Aplicativo | Nome identificado |
| Estado anterior | Ativo, desativado ou indisponível |
| Ação | Desativação, remoção para usuário, permissão, AppOps etc. |
| Justificativa | Evidência e motivo técnico |
| Risco | Crítico, alto, médio, baixo ou informativo |
| Dependências | Componentes possivelmente afetados |
| Comando | Comando efetivamente executado |
| Resultado | Saída real do comando e validação |
| Reversão | Como restaurar |
| Evidência | Log ou captura relacionada |

Não classifique um pacote como dispensável apenas pelo nome ou fabricante.

## 7. Diagnóstico final — DEPOIS

Após as alterações, repita as coletas do diagnóstico inicial com os mesmos métodos e, tanto quanto possível, nas mesmas condições.

Verifique:

- Inicialização e estabilidade do Android.
- Chamadas, SMS e dados móveis.
- Wi-Fi, Bluetooth e GPS.
- Câmeras, microfone e áudio.
- Notificações push e sincronização.
- Aplicativos bancários e de autenticação usados pelo proprietário.
- Teclado e launcher.
- Atualizações do sistema.
- Aplicativos substitutos.
- Memória, armazenamento, bateria e temperatura.

Um aplicativo continuar instalado não prova que sua função está operacional. Teste o recurso real.

## 8. Comparativo antes e depois

O relatório deve comparar os dados coletados, sem preencher lacunas com estimativas.

| Indicador | Antes | Depois | Diferença |
|---|---:|---:|---:|
| Pacotes habilitados | Medir | Medir | Calcular |
| Pacotes desabilitados | Medir | Medir | Calcular |
| Aplicativos de usuário | Medir | Medir | Calcular |
| RAM disponível | Medir | Medir | Calcular |
| Armazenamento livre | Medir | Medir | Calcular |
| Temperatura em repouso | Medir | Medir | Calcular |
| Permissões concedidas | Medir | Medir | Calcular |
| Serviços em segundo plano | Medir | Medir | Calcular |

Além das métricas, comparar:

- Pacotes removidos ou desativados.
- Aplicativos substituídos por alternativas FOSS.
- Permissões revogadas.
- AppOps modificados.
- Serviços neutralizados.
- Recursos preservados.
- Funcionalidades prejudicadas ou indisponíveis.
- Problemas encontrados e corrigidos.
- Melhorias comprovadas e resultados inconclusivos.

Não confundir remoção de pacote para o usuário atual com remoção física da partição do sistema. Diferencie desativação, desinstalação para usuário, remoção de atualização e remoção com root.

## 9. Modelo de relatório final

O arquivo `comparison-report.md` deverá conter:

1. Resumo executivo.
2. Identificação técnica do aparelho.
3. Objetivo e escopo.
4. Ferramentas utilizadas.
5. Condições de medição.
6. Estado inicial.
7. Inventário de aplicativos.
8. Análise de permissões e AppOps.
9. Análise de telemetria e limitações de evidência.
10. Alterações realizadas.
11. Aplicativos substituídos.
12. Estado final.
13. Tabela comparativa de métricas.
14. Comparação de funcionalidades.
15. Testes de compatibilidade e estabilidade.
16. Capturas de tela.
17. Problemas encontrados e reversões.
18. Limitações e itens não mensurados.
19. Conclusão técnica e recomendações.

A conclusão deve responder: o que mudou, o que foi preservado, o que deixou de funcionar, quais melhorias foram medidas, quais resultados são inconclusivos e como reverter alterações.

## 10. Instruções para a IA

A IA utilizada pelo usuário deverá:

1. Confirmar que o usuário está trabalhando em um fork próprio ou cópia local e identificar o repositório original como `upstream`.
2. Identificar o dispositivo conectado e criar uma pasta individual para a auditoria.
3. Fazer todas as coletas iniciais antes de modificar qualquer coisa.
4. Analisar cada pacote individualmente, incluindo função, origem, permissões, AppOps, dependências e risco.
5. Distinguir telemetria confirmada, provável, suspeita e inconclusiva. A presença de uma permissão ou SDK, isoladamente, não comprova envio de dados.
6. Apresentar um plano com pacote, justificativa, comando, risco, efeitos colaterais e reversão.
7. Aguardar autorização explícita antes de executar cada grupo de alterações.
8. Executar em pequenos grupos, registrar comandos e saídas e validar os resultados.
9. Repetir as coletas iniciais depois das alterações.
10. Produzir o relatório comparativo e organizar evidências.
11. Sanitizar os arquivos, criar uma branch própria, enviar a branch ao fork e preparar um Pull Request direcionado ao repositório original.
12. Nunca abrir PR nem publicar arquivos sem autorização explícita; nunca afirmar que criou um fork, capturou uma tela, mediu uma métrica ou publicou um arquivo sem confirmação real.

### Classificação de risco

- **Crítico:** necessário à inicialização, telefonia, conectividade ou segurança.
- **Alto:** pode comprometer funções importantes ou aplicativos essenciais.
- **Médio:** dispensável em algumas configurações, mas com efeitos colaterais possíveis.
- **Baixo:** opcional ou redundante, com impacto limitado.
- **Informativo:** sem recomendação de alteração.

### Segurança obrigatória

- Não modificar o aparelho sem autorização.
- Não apagar dados sem autorização específica.
- Preservar IMS/VoLTE/VoWiFi, modem/RIL, telefonia, Wi-Fi, Bluetooth, KeyStore, KeyChain, Package Installer e componentes essenciais.
- Não desativar o teclado ativo antes de instalar e testar outro.
- Não desativar discador/SMS antes de testar substitutos.
- Não remover o launcher original antes de testar outro e considerar dependências de gestos/QuickStep.
- Não remover Google Play Services indiscriminadamente, especialmente quando o usuário depende de bancos brasileiros e notificações push.
- Não aplicar AppOps por UID sem verificar se outros pacotes compartilham o UID.
- Não usar `pm clear` como etapa automática: ele apaga dados do aplicativo. Exigir justificativa e autorização específica.
- Não executar comandos de outro modelo sem validar pacote, ROM e dependências.
- Preferir ações reversíveis e documentar o rollback.
- Não prometer compatibilidade sem testes reais.

### Critério de conclusão

A auditoria só estará concluída quando o estado inicial estiver registrado, os pacotes estiverem analisados ou marcados como pendentes, as alterações estiverem documentadas, o estado final tiver sido coletado, as funções essenciais tiverem sido testadas e o relatório comparativo estiver produzido.

## 11. Enviar sua contribuição por Pull Request

O relatório individual deve ficar em uma pasta própria, por exemplo `reports/SEU_DISPOSITIVO/`. Para contribuir com o projeto original, siga este fluxo:

1. Atualize a branch principal do fork com o repositório original.
2. Crie uma branch exclusiva para a auditoria.
3. Adicione somente os arquivos sanitizados do relatório.
4. Revise o diff completo e confirme que não há identificadores, credenciais, notificações ou dados pessoais.
5. Envie a branch para o seu fork.
6. Abra um Pull Request do seu fork para `luisfvmartins/clean-my-android:main`.
7. Descreva o modelo, versão Android/ROM, escopo da auditoria, principais resultados, testes realizados e limitações.
8. Aguarde a revisão. Atenda aos pedidos de alteração, se houver.

Exemplo de comandos Git:

```bash
git remote -v
git fetch upstream
git switch main
git merge upstream/main
git switch -c docs/auditoria-SEU-DISPOSITIVO
git add reports/SEU_DISPOSITIVO/
git diff --cached
git commit -m "docs: add audit for SEU_DISPOSITIVO"
git push -u origin docs/auditoria-SEU_DISPOSITIVO
```

Depois, no GitHub, use **Compare & pull request** e confirme:
- **Base repository:** `luisfvmartins/clean-my-android`
- **Base:** `main`
- **Head repository:** seu fork
- **Compare:** sua branch de auditoria

Se não tiver Git configurado, abra o PR pela interface do GitHub após enviar os arquivos pela interface web. Não faça commit diretamente na branch principal do repositório original.

O Pull Request é uma proposta de contribuição, não uma publicação automática na versão principal. O mantenedor revisará o conteúdo e poderá aceitar, solicitar ajustes ou rejeitar a contribuição.
---

**O objetivo não é produzir os maiores números de otimização. É construir um histórico técnico confiável, verificável e reproduzível de cada dispositivo.**
