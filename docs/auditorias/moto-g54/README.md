# Motorola Moto G54 5G — auditoria técnica

**Dispositivo:** Motorola Moto G54 5G · XT2343-1 · `cancunf`  
**Sistema:** Android 15 · Hello UI  
**Relatório principal:** [Resumo, metodologia, conclusões e limitações](../../AUDITORIA_MOTO_G54_5G.md)

Esta pasta reúne o inventário individual dos componentes do dispositivo, separado por lotes para facilitar leitura e revisão. O conteúdo foi extraído do relatório original sem reclassificar pacotes nem alterar recomendações.

## Inventário de componentes

| Lote | Escopo | Itens | Arquivo |
|---|---|---:|---|
| 2 | Google, GMS, Mainline APKs e serviços proprietários | 30–111 (82) | [Lote 2](lote-02-ecossistema-google.md) |
| 3 | Motorola e Lenovo | 112–199 (88) | [Lote 3](lote-03-motorola-lenovo.md) |
| 4 | Parceiros comerciais, operadoras e hardware | 200–224 (25) | [Lote 4](lote-04-parceiros-comerciais-e-hardware.md) |
| 5 | Sistema base Android AOSP | 225–296 (72) | [Lote 5](lote-05-sistema-base-aosp.md) |
| 6 | Overlays RRO AOSP, Google Mainline e MediaTek | 297–358 (62) | [Lote 6](lote-06-overlays-aosp-google-mediatek.md) |
| 7 | Overlays Motorola, operadoras regionais e eUICC/eSIM | 359–423 (65) | [Lote 7](lote-07-overlays-motorola-operadoras-esim.md) |
| 8 | Módulos Project Mainline e sistema em formato APEX | 424–462 (39) | [Lote 8](lote-08-modulos-project-mainline-apex.md) |

**Lote 1:** os 29 aplicativos instalados pelo usuário foram omitidos da versão pública para preservar a privacidade do proprietário. A omissão é intencional.

## Como interpretar

- A divisão é editorial e preserva a numeração do inventário original.
- A auditoria descreve uma coleta específica; não generalize suas conclusões para outro aparelho, região ou firmware.
- Classificação de risco não é autorização para desativar ou remover pacotes.
- Consulte o relatório principal para metodologia, limitações, histórico operacional, reversão e recomendações.
- Um inventário publicado não significa que um script de debloat esteja homologado para o aparelho.
