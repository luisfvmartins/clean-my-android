# Notas de Segurança: disabled_packages.txt

> **Aviso obrigatório:** este arquivo é registro/candidatos; os scripts não o consomem; não use como lista de execução.

Este documento acompanha `data/disabled_packages.txt`. O arquivo representa uma lista histórica de candidatos levantada nas primeiras iterações do repositório. Ele **não** é consumido por nenhum script de execução (`debloat.sh`, `restore.sh`, etc.) nem por workflows de automação.

## Pacotes protegidos presentes na lista histórica de candidatos

Os seguintes 18 pacotes constam no arquivo histórico, mas foram classificados como protegidos essenciais em `data/protected_essential_packages.txt` para prevenir desativações inadvertidas de subsistemas críticos do Android:

1. `com.android.bluetoothmidiservice` — Serviço MIDI Bluetooth.
2. `com.android.carrierdefaultapp` — Provedor de fallback da operadora.
3. `com.android.companiondevicemanager` — Gerenciador de dispositivos emparelhados/wearables.
4. `com.android.contacts` — Provedor e aplicativo AOSP de contatos.
5. `com.android.dialer` — Discador e telefonia AOSP.
6. `com.android.emergency` — Discagem de emergência e informações SOS.
7. `com.android.printspooler` — Spooler de impressão e exportação para PDF.
8. `com.android.providers.contactkeys` — Provedor de chaves de contatos criptografados.
9. `com.android.providers.userdictionary` — Dicionário do usuário no teclado.
10. `com.android.settings.intelligence` — Mecanismos de busca e inteligência das Configurações.
11. `com.android.simappdialog` — Diálogos do SIM card.
12. `com.android.stk` — SIM Toolkit da operadora.
13. `com.android.vending` — Google Play Store (gestão de pacotes e licenças).
14. `com.dolby.daxservice` — Serviço de processamento de áudio Dolby Atmos.
15. `com.google.android.apps.messaging` — Google Mensagens (SMS/MMS/RCS).
16. `com.google.android.dialer` — Google Telefone (discador e chamadas).
17. `com.motorola.dolby.dolbyui` — Interface e controle do efeito de áudio Dolby Motorola.
18. `com.motorola.nfwlocationattribution` — Atribuição de localização non-framework (requisito regulatório E911).

Para fins de integridade dos registros e rastreabilidade documental, o arquivo original é mantido inalterado.
