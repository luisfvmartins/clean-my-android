# Guia de revisão de pull requests

Use esta lista de verificação ao revisar contribuições para o Clean My Android. A revisão deve preservar o conhecimento cumulativo e baseado em evidências sobre os dispositivos, priorizando a segurança do usuário e a privacidade.

## 1. Escopo e integridade do repositório

- [ ] O PR tem um objetivo claro e escopo bem delimitado.
- [ ] Novas descobertas sobre dispositivos estão no diretório correto de fabricante/modelo dentro de `reports/`.
- [ ] Relatórios existentes e descobertas de outros dispositivos foram preservados.
- [ ] O PR acrescenta conhecimento ou corrige claramente um erro documentado; não apaga o histórico silenciosamente.
- [ ] Índices, catálogos e links pertinentes foram atualizados de forma consistente.

## 2. Identificação do dispositivo e evidências

- [ ] Fabricante, modelo exato, versão do Android, contexto de software/compilação e data da auditoria estão registrados quando aplicável.
- [ ] Os métodos de coleta de dados e comandos relevantes estão identificados.
- [ ] Fatos observados estão diferenciados de suposições, interpretações e recomendações.
- [ ] Comparações antes/depois usam condições equivalentes ou explicam as diferenças.
- [ ] As afirmações são sustentadas por evidências incluídas no relatório ou por fontes claramente identificadas.
- [ ] Recomendações sobre pacotes/aplicativos são contextualizadas para o dispositivo e firmware, sem generalização para todos os aparelhos Android.
- [ ] Resultados ainda não testados ou incertos estão claramente identificados.

## 3. Segurança e autorização

- [ ] O relatório confirma a autorização do proprietário para ações que modificam o dispositivo.
- [ ] Riscos, impactos, dependências e opções de restauração são explicados para recomendações relevantes.
- [ ] Nenhuma recomendação é apresentada como universalmente segura sem evidências suficientes.
- [ ] A depuração ADB/rede ou outro acesso temporário é abordado nas observações de limpeza da auditoria, quando pertinente.

## 4. Privacidade e segurança da informação

- [ ] Nenhum identificador pessoal ou sensível do dispositivo foi exposto (IMEI, número de série, MAC, IP privado, nome de host ou identificadores de conta).
- [ ] Não há credenciais, tokens, chaves privadas, conteúdo de notificações ou logs pessoais sem anonimização.
- [ ] Capturas de tela, saídas de comandos e inventários foram verificados — não apenas o texto Markdown.
- [ ] Dumps e backups brutos foram excluídos, salvo quando necessários, justificados explicitamente e sanitizados.
- [ ] O autor revisou manualmente o diff; ferramentas automatizadas não foram consideradas suficientes.

## 5. Qualidade e validação

- [ ] A formatação Markdown e os links relativos estão corretos.
- [ ] JSON, scripts, listas de pacotes e dados gerados seguem as convenções do repositório.
- [ ] As verificações automatizadas pertinentes foram aprovadas ou suas falhas/limitações foram explicadas.
- [ ] A documentação e as contagens/estatísticas dos catálogos permanecem consistentes, quando aplicável.
- [ ] O modelo de PR foi preenchido e as dúvidas dos revisores foram resolvidas.

## Resultado da revisão

- **Aprovar** quando a contribuição for precisa, segura, revisada quanto à privacidade, cumulativa e validada na medida declarada.
- **Solicitar alterações** quando faltarem evidências, contexto de segurança, sanitização de privacidade ou consistência do repositório.
- **Comentar** quando um esclarecimento puder melhorar o relatório, mas não impedir sua aceitação.

Uma execução de CI aprovada não substitui a revisão humana da segurança específica do dispositivo, da qualidade das evidências ou da privacidade.
