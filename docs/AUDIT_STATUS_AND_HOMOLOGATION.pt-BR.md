# Níveis de status e homologação de auditoria

Este padrão separa a publicação de evidências da validação funcional e da compatibilidade de scripts. Relatório publicado, teste bem-sucedido e script homologado não são equivalentes.

## Níveis de status

| Nível | Rótulo | Evidência mínima | Afirmação permitida |
|---|---|---|---|
| 0 | **Não avaliado** | Identificação do aparelho ou evidências insuficientes para avaliar a auditoria | Nenhuma afirmação de compatibilidade ou segurança |
| 1 | **Inventário documentado** | Fabricante/modelo/build identificados; inventário coletado e documentado com origem dos dados | Inventário documentado para este aparelho/build |
| 2 | **Auditoria revisada** | Justificativas por pacote, riscos, dependências, componentes protegidos, sanitização e checklist de revisão concluídos | Achados revisados; não implica aprovação funcional |
| 3 | **Validação funcional concluída** | Matriz explícita de testes, ambiente, resultados e limitações registrados no aparelho/build exatos | Somente as funções listadas foram testadas com sucesso |
| 4 | **Script homologado** | Script/versão exatos, escopo de modelos/builds, verificações prévias e reversão, testes funcionais, aprovação revisora e evidências reproduzíveis | Script aprovado somente para o escopo explicitamente indicado |

## Regras

- Use o nível mais baixo totalmente sustentado por evidências; não infira níveis superiores.
- O status vale para fabricante, modelo, variante, firmware/build, Android, versão do script e escopo exatos. Alterações podem invalidar a aprovação.
- Homologação **não** é inferida pela publicação de relatório, pacotes desativados, aparelho iniciando ou outro modelo passando nos testes.
- Teste não executado é **Não testado**; evidência ausente é **Pendente**; falha é **Falhou**. Não converta esses estados em “aprovado”.
- Evite rótulos amplos como “seguro”, “aprovado para Android” ou “funciona em Samsung/Motorola” sem evidência delimitada.
- Toda ação que modifica o aparelho exige autorização explícita do proprietário. O framework de status não concede autorização.
- Inclua este registro em cada relatório:

| Campo | Valor |
|---|---|
| Nível de status da auditoria | Nível 0–4 |
| Aparelho/modelo/variante | Valor exato |
| Android/build/patch de segurança | Valor exato ou Pendente |
| Nome/versão/hash do script | Valor exato ou Não aplicável |
| Matriz de testes funcionais | Link ou Não testado |
| Evidência de reversão/recuperação | Link ou Pendente |
| Revisor/data | Nome ou pseudônimo / data |
| Escopo aprovado e exclusões | Lista explícita |

## Traduções

Versão em inglês: [Audit status and homologation levels](AUDIT_STATUS_AND_HOMOLOGATION.md).
