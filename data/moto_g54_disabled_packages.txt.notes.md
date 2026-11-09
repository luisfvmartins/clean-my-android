# Notas de Segurança: moto_g54_disabled_packages.txt

> **Aviso obrigatório:** este arquivo é registro/candidatos; os scripts não o consomem; não use como lista de execução.

Este documento acompanha `data/moto_g54_disabled_packages.txt`. O arquivo contém o snapshot bruto dos pacotes encontrados desativados na coleta do Moto G54 5G. Ele **não** é consumido por nenhum script de execução (`debloat.sh`, `restore.sh`, etc.) nem por workflows de automação.

## Pacotes protegidos presentes no snapshot histórico

Os seguintes 4 pacotes constam no snapshot histórico do Moto G54 5G, mas são classificados como essenciais/protegidos pelo projeto em `data/protected_essential_packages.txt` e **não** devem ser desativados em execuções futuras:

1. `com.android.bluetoothmidiservice` — Serviço MIDI de Bluetooth (áudio e periféricos).
2. `com.android.carrierdefaultapp` — Provedor de configuração de operadora de telefonia.
3. `com.android.simappdialog` — Interface de diálogos do SIM card.
4. `com.android.stk` — SIM Toolkit (aplicativo da operadora e autenticação de rede).

Para fins de integridade dos registros e auditoria técnica retrospectiva, o arquivo bruto é mantido inalterado.
