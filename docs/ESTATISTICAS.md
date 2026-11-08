# Estatísticas do projeto

Indicadores calculados a partir do catálogo estruturado em [data/device_catalog.json](../data/device_catalog.json). Os números refletem somente informações documentadas e explicitamente classificadas.

## Visão geral

- **Dispositivos catalogados:** 4
- **Fabricantes representados:** 2
- **Versões Android confirmadas:** 3 (11, 15, 16)
- **Relatórios com contagem de componentes:** 4

## Dispositivos

| Fabricante / modelo | Código | Android | Situação da auditoria | Componentes registrados |
|---|---|---|---|---:|
| Motorola Moto G54 5G | XT2343-1 | Android 15 | [Inventário técnico publicado](../reports/motorola/moto-g54-5g/README.md) | 462 — componentes auditados no inventário local |
| Motorola Edge 60 Pro | XT2507-1 | Não confirmado (pendente de confirmação) | [Relatório publicado; validação funcional pendente](../reports/motorola/edge-60-pro/README.md) | 501 — componentes mapeados no inventário inicial |
| Motorola Edge 60 Fusion | scout_g_sysn | Android 16 | [Auditoria e debloat concluídos](../reports/motorola/edge-60-fusion/README.md) | 486 — pacotes mapeados no inventário inicial |
| Samsung Galaxy A30s | SM-A307GT | Android 11 | [Auditoria e otimização cirúrgica concluídas](../reports/samsung/galaxy-a30s/README.md) | 392 — pacotes catalogados no firmware de fábrica |

## Como interpretar os números

- **Contagens de componentes não são somadas.** Os relatórios usam escopos e estados diferentes: o Moto G54 registra componentes auditados; o Edge 60 Pro registra componentes mapeados no inventário inicial.
- A contagem do Moto G54 é de 462 componentes na coleta local; a versão pública omite 29 aplicativos instalados pelo usuário e publica 433 componentes: 394 pacotes de sistema/fabricante e 39 módulos APEX.
- A contagem do Edge 60 Pro (501) refere-se ao inventário inicial mapeado e não significa que todos os componentes tenham sido validados funcionalmente.
- Versões Android pendentes não entram na contagem de versões confirmadas.
- **Dispositivo catalogado**, **auditoria publicada**, **validação funcional** e **homologação de script** são estados diferentes. A presença nesta página não implica homologação.
- Não são estimados ganhos de bateria, RAM, armazenamento, privacidade ou compatibilidade.

## Atualização e validação

Os dados são mantidos em data/device_catalog.json. Ao adicionar ou atualizar uma auditoria, revise esse arquivo com informações sustentadas pelos documentos do dispositivo e execute:

    python scripts/generate_statistics.py
    python scripts/generate_statistics.py --check

A validação automatizada verifica se esta página corresponde ao catálogo. A geração não consulta a API do GitHub, não conta Pull Requests e não acessa nem modifica aparelhos.

Consulte o [catálogo completo de auditorias](../reports/README.md).
