# Boas práticas e práticas proibidas para contribuições

Este guia estabelece salvaguardas práticas para contribuições ao Clean My Android. Siga-o em conjunto com [CONTRIBUTING.pt-BR.md](../CONTRIBUTING.pt-BR.md), [AI_INSTRUCTIONS.pt-BR.md](../AI_INSTRUCTIONS.pt-BR.md) e o [guia de auditoria de dispositivos](USER_DEVICE_AUDIT.pt-BR.md).

## Faça

- **Acrescente conhecimento de forma cumulativa.** Adicione ou revise o relatório do dispositivo pertinente sem remover dados de outros aparelhos ou descobertas anteriores.
- **Identifique exatamente o dispositivo e o software.** Informe fabricante, modelo, versão do Android, fingerprint ou identificador da compilação quando seguro, e data da auditoria.
- **Separe evidências de interpretações.** Diferencie claramente estado observado, informações fornecidas pelo usuário, inferências e recomendações.
- **Comece por inspeções somente de leitura.** Faça o inventário do dispositivo antes de propor alterações.
- **Obtenha autorização explícita.** Explique cada ação relevante e obtenha a aprovação do proprietário antes de desativar, desinstalar, alterar configurações ou executar outros comandos que modifiquem o aparelho.
- **Verifique a possibilidade de reversão.** Documente os procedimentos e as limitações de restauração para cada alteração proposta.
- **Mantenha os resultados reproduzíveis.** Inclua comando relevante, resultado esperado, resultado obtido e condições do teste, sem expor dados sensíveis.
- **Compare condições equivalentes.** Registre estados antes/depois sob condições comparáveis e indique fatores que impeçam uma comparação justa.
- **Atualize os índices relacionados.** Mantenha catálogos, resumos e links dos relatórios consistentes com a nova contribuição.
- **Revise o diff final.** Confirme que somente os arquivos pretendidos foram alterados e que os links da documentação funcionam.
- **Execute as validações do repositório.** Rode os testes disponíveis e informe com transparência eventuais falhas ou verificações que não puderam ser executadas.

## Não faça

- **Não exclua, sobrescreva ou substitua silenciosamente o relatório de outro dispositivo.**
- **Não apresente uma lista de pacotes como uma lista universal de debloat.** O comportamento dos pacotes varia conforme fabricante, modelo, firmware, região e necessidades do usuário.
- **Não afirme que um comando foi executado ou que um resultado foi verificado sem evidências.**
- **Não considere o nome de um pacote, uma publicação na internet ou uma inferência de IA, isoladamente, como prova de que sua remoção é segura.**
- **Não faça alterações sem autorização explícita do proprietário do dispositivo.**
- **Não inclua identificadores sensíveis ou dados pessoais brutos.** Isso inclui IMEI, números de série, endereços MAC, IPs privados, nomes de host, nomes/IDs de contas, conteúdo de notificações, tokens, credenciais e logs sem anonimização.
- **Não envie dumps privados do dispositivo, backups ou capturas de tela que contenham informações pessoais.**
- **Não deixe o acesso de depuração habilitado.** Se a depuração ADB pela rede tiver sido ativada durante a auditoria, registre e verifique sua desativação ao final, quando aplicável.
- **Não misture alterações sem relação entre si.** Mantenha cada PR focado e evite modificar CI, scripts, catálogos e descobertas de dispositivos que não façam parte de seu objetivo.
- **Não marque recomendações não testadas como confirmadas ou seguras.**
- **Não dependa da varredura automatizada de segredos como substituta da revisão manual de privacidade.**

## Antes de enviar

1. Leia a lista de verificação do [modelo de pull request](../.github/pull_request_template.md).
2. Revise todo o diff quanto ao escopo, à precisão e à privacidade.
3. Execute as verificações pertinentes aos arquivos alterados.
4. Informe na descrição do PR o que foi testado, o que não foi testado e quaisquer limitações conhecidas.
