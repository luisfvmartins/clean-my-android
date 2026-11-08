# Registro de Alterações Executadas (Change Log)

Data da execução: 2026-11-08 13:13:14
Dispositivo: Samsung Galaxy A30s (SM-A307GT)
Ambiente: Android 11 / One UI 3.1 / Exynos 7904

| Horário | Grupo | Pacote | Comando Executado | Saída | Estado Verificado | Comando de Reversão |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| 2026-11-08 13:12:59 | Grupo A | `com.odete.samsung` | `pm uninstall -k --user 0 com.odete.samsung` | Success | **Desinstalado para user 0** | `cmd package install-existing com.odete.samsung` |
| 2026-11-08 13:13:01 | Grupo A | `com.samsung.shop` | `pm uninstall -k --user 0 com.samsung.shop` | Success | **Desinstalado para user 0** | `cmd package install-existing com.samsung.shop` |
| 2026-11-08 13:13:02 | Grupo A | `com.facebook.katana` | `pm disable-user --user 0 com.facebook.katana` | Package com.facebook.katana new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.facebook.katana` |
| 2026-11-08 13:13:03 | Grupo A | `com.facebook.system` | `pm disable-user --user 0 com.facebook.system` | Package com.facebook.system new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.facebook.system` |
| 2026-11-08 13:13:04 | Grupo A | `com.facebook.appmanager` | `pm disable-user --user 0 com.facebook.appmanager` | Package com.facebook.appmanager new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.facebook.appmanager` |
| 2026-11-08 13:13:04 | Grupo A | `com.facebook.services` | `pm disable-user --user 0 com.facebook.services` | Package com.facebook.services new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.facebook.services` |
| 2026-11-08 13:13:05 | Grupo A | `com.netflix.partner.activation` | `pm disable-user --user 0 com.netflix.partner.activation` | Package com.netflix.partner.activation new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.netflix.partner.activation` |
| 2026-11-08 13:13:05 | Grupo A | `com.microsoft.skydrive` | `pm disable-user --user 0 com.microsoft.skydrive` | Package com.microsoft.skydrive new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.microsoft.skydrive` |
| 2026-11-08 13:13:06 | Grupo B | `com.samsung.android.rubin.app` | `pm disable-user --user 0 com.samsung.android.rubin.app` | Package com.samsung.android.rubin.app new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.rubin.app` |
| 2026-11-08 13:13:07 | Grupo B | `com.samsung.android.knox.analytics.uploader` | `pm disable-user --user 0 com.samsung.android.knox.analytics.uploader` | Package com.samsung.android.knox.analytics.uploader new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.knox.analytics.uploader` |
| 2026-11-08 13:13:07 | Grupo B | `com.samsung.android.securitylogagent` | `pm disable-user --user 0 com.samsung.android.securitylogagent` | Package com.samsung.android.securitylogagent new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.securitylogagent` |
| 2026-11-08 13:13:08 | Grupo B | `com.sec.android.soagent` | `pm disable-user --user 0 com.sec.android.soagent` | Package com.sec.android.soagent new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.sec.android.soagent` |
| 2026-11-08 13:13:09 | Grupo B | `com.sec.spp.push` | `pm disable-user --user 0 com.sec.spp.push` | Package com.sec.spp.push new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.sec.spp.push` |
| 2026-11-08 13:13:09 | Grupo B | `com.samsung.android.mateagent` | `pm disable-user --user 0 com.samsung.android.mateagent` | Package com.samsung.android.mateagent new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.mateagent` |
| 2026-11-08 13:13:10 | Grupo B | `com.samsung.android.app.spage` | `pm disable-user --user 0 com.samsung.android.app.spage` | Package com.samsung.android.app.spage new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.app.spage` |
| 2026-11-08 13:13:10 | Grupo C | `com.samsung.android.game.gos` | `pm disable-user --user 0 com.samsung.android.game.gos` | Package com.samsung.android.game.gos new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.game.gos` |
| 2026-11-08 13:13:11 | Grupo C | `com.samsung.android.game.gamehome` | `pm disable-user --user 0 com.samsung.android.game.gamehome` | Package com.samsung.android.game.gamehome new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.game.gamehome` |
| 2026-11-08 13:13:12 | Grupo C | `com.samsung.android.game.gametools` | `pm disable-user --user 0 com.samsung.android.game.gametools` | Package com.samsung.android.game.gametools new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.samsung.android.game.gametools` |
| 2026-11-08 13:13:12 | Grupo D | `com.google.mainline.telemetry` | `pm disable-user --user 0 com.google.mainline.telemetry` | Package com.google.mainline.telemetry new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.google.mainline.telemetry` |
| 2026-11-08 13:13:13 | Grupo D | `com.google.android.feedback` | `pm disable-user --user 0 com.google.android.feedback` | Package com.google.android.feedback new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.google.android.feedback` |
| 2026-11-08 13:13:13 | Grupo D | `com.google.android.partnersetup` | `pm disable-user --user 0 com.google.android.partnersetup` | Package com.google.android.partnersetup new state: disabled-user | **Desativado (disabled-user)** | `pm enable com.google.android.partnersetup` |
