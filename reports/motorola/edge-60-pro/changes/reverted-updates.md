# Atualizações de Sistema Revertidas em `/data/app` — Motorola Edge 60 Pro (`XT2507-1`)

> **Nota técnica:** este documento registra os 10 pacotes de sistema pré-instalados cujas atualizações baixadas da Google Play Store residiam na partição `/data/app` e foram revertidas à imagem base da ROM via `pm uninstall <pacote>`.

## Contexto e distinção técnica

No sistema Android sem root:
1. **Reversão de atualizações (`/data/app`):** Quando um aplicativo pré-instalado de sistema é atualizado, o novo binário é armazenado em `/data/app`. O comando `pm uninstall <pacote>` sem a flag `--user 0` remove unicamente essa atualização, restaurando a versão original gravada na partição de sistema (`/system` ou `/product`).
2. **Desativação posterior:** Após a reversão das atualizações, os 10 pacotes listados abaixo foram subsequentemente desativados para o Usuário 0 via `pm disable-user --user 0` e constam catalogados no arquivo canônico [`disabled-packages.txt`](disabled-packages.txt).
3. **Armazenamento:** A reversão das atualizações em conjunto com a limpeza de dados e caches contribuiu para o ganho agregado de **~4 GB** de espaço livre observado na partição `/data` (de 193 GB para ~197 GB). O ganho individual por pacote não foi mensurado isoladamente.

## Componentes com atualizações revertidas (10 pacotes)

| Pacote | Nome amigável | Destino pós-reversão |
|---|---|---|
| `com.android.chrome` | Google Chrome | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.google.android.apps.maps` | Google Maps | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.google.android.apps.photos` | Google Fotos | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.google.android.gm` | Gmail | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.google.android.googlequicksearchbox` | Google App / Busca | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.google.android.inputmethod.latin` | Teclado Gboard | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.google.android.youtube` | YouTube | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.inmobi.weather` | InMobi Clima | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.motorola.mobiledesktop` | Moto Ready For / Desktop | Desativado para o Usuário 0 (`disabled-packages.txt`) |
| `com.motorola.smartfeed` | Moto Smart Feed | Desativado para o Usuário 0 (`disabled-packages.txt`) |
