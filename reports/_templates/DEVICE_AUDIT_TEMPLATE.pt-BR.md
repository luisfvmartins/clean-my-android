# Auditoria de dispositivo Android — Fabricante Modelo

> **Modelo:** Substitua todos os `[campos]`. Remova instruções somente após registrar as informações necessárias. Não publique dumps privados brutos.

## 1. Resumo executivo
- **Fabricante / modelo / variante:** [identificação exata]
- **Codinome / placa / produto:** [valores ou Desconhecido]
- **Android / ROM / interface:** [versão, API, ROM]
- **Build / patch de segurança / região:** [valores ou Pendente]
- **Data da auditoria / operador:** [data / pseudônimo]
- **Status da auditoria:** [Nível 0–4; consulte o padrão]
- **Escopo:** [o que foi avaliado]
- **Fora do escopo:** [o que não foi avaliado]

## 2. Autorização e segurança
- Autorização do proprietário: [registrada explicitamente / pendente]
- Método de acesso e privilégios: [ADB, shell, status root]
- Modificações permitidas: [ações explicitamente delimitadas]
- Interrupção de emergência e reversão: [passos/evidências]
- Resumo de riscos e dependências: [resumo]

## 3. Metodologia e origem das evidências
| ID da evidência | Data/hora da coleta | Comando/ferramenta/fonte | Contexto aparelho/build | Caminho do arquivo | Sanitização |
|---|---|---|---|---|---|
| E-001 | [data/hora] | [comando] | [build] | [caminho] | [ações] |

Separe **fatos observados**, **interpretação técnica** e **hipóteses**.

## 4. Estado inicial
- Inventário de pacotes: [caminho]
- Contagem de ativos/desativados/desinstalados para usuário: [escopo e contagens]
- Permissões runtime/AppOps: [caminho ou Pendente]
- Métricas de armazenamento/RAM/bateria: [método, condições, resultados ou Não medido]
- Matriz de testes funcionais de baseline: [caminho]

## 5. Achados e avaliação por pacote
| Pacote | Evidência | Finalidade/confiança | Permissões/AppOps | Dependências | Risco | Recomendação | Reversão |
|---|---|---|---|---|---|---|---|
| [ID do pacote] | [E-ID] | [finalidade; confiança] | [observado] | [conhecidas/desconhecidas] | [nível] | [preservar/desativar/remover/testar] | [comando/passos] |

Não generalize uma recomendação para outro modelo/build.

## 6. Ações autorizadas e registro de alterações
| ID da ação | Pacote/componente | Ação proposta | Autorização do proprietário | Comando real | Resultado/hora | Reversão |
|---|---|---|---|---|---|---|
| C-001 | [ID] | [ação] | [registro] | [comando] | [resultado] | [passos] |

Registre como concluídas somente ações realmente executadas.

## 7. Estado final e comparação
| Métrica | Baseline | Final | Método/condições | Evidência | Interpretação/limitação |
|---|---:|---:|---|---|---|
| [métrica] | [valor] | [valor] | [método] | [E-ID] | [escopo] |

Não declare ganhos sem evidências medidas e comparáveis.

## 8. Testes funcionais
| Teste | Pré-condições | Passos | Esperado | Obtido | Resultado | Evidência |
|---|---|---|---|---|---|---|
| Chamadas/SMS/dados | [condições] | [passos] | [esperado] | [observado] | [Passou/Falhou/Não testado] | [E-ID] |

Liste testes não realizados e falhas.

## 9. Limitações, pendências e recuperação
- Evidências pendentes: [lista]
- Falhas/limitações conhecidas: [lista]
- Verificação de recuperação/reversão: [resultados]
- Monitoramento de longo prazo: [pendente/não realizado]

## 10. Revisão de privacidade
- [ ] IMEI, serial, MAC, IP privado, hostname e IDs de contas sanitizados
- [ ] Credenciais, tokens, chaves e segredos removidos
- [ ] Capturas de tela e anexos inspecionados
- [ ] Aplicativos pessoais e dados pessoais excluídos ou pseudonimizados
- [ ] Dados brutos privados mantidos fora do repositório público

## 11. Reprodutibilidade e revisão
- Scripts/ferramentas de coleta e versões: [valores]
- Escopo de reprodução: [aparelho/build exatos]
- Revisor/data: [valores]
- Status da auditoria e escopo aprovado: [Nível 0–4, escopo]
- Link do PR: [URL]

## 12. Referências
- [Documentação oficial do fabricante/Android]
- [Links de fontes relevantes, com data de acesso]
