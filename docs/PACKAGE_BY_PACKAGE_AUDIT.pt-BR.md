# Auditoria pacote por pacote — Clean My Android

## Cobertura sem exceções
Crie inventário mestre de todos os package names detectados, incluindo componentes invisíveis ao launcher: sistema/AOSP, OEM, Google, operadora, terceiros pré-carregados e instalados pelo usuário, módulos/APEX, overlays, serviços e componentes headless. Uma linha individual por pacote; agrupamentos só em sínteses. Reconcile total inventariado = analisado + pendente. Não omita pacote por parecer irrelevante. Não fabrique campos: marque desconhecido, não coletado ou inconclusivo. Não reutilize evidência de outro modelo, variante, build, ROM ou usuário.

## Inspeção exigida por pacote
Registre, quando disponíveis: package name, label, version/versionCode, UID e shared UID; estado por usuário/perfil; origem/caminho/partição e distinção entre observação e inferência; componentes declarados (activities/services/receivers/providers/jobs/intent filters); permissões do manifesto, runtime concedidas e especiais separadas; AppOps, modo e escopo package ou UID; serviços persistentes, startup, jobs, alarmes e execução background; dependências diretas/indiretas com framework, APEX, overlays, OEM APIs, telefonia, IMS, GMS/FCM/Play Integrity, biometria, câmera, áudio, localização, launcher/QuickStep; acessos sensíveis e justificativa; evidências de rede/telemetria; relação com apps/funções usadas pelo proprietário; comandos/fontes e evidências sanitizadas.

A permissão INTERNET, SDK analítico, nome do fabricante, domínio encontrado em DNS ou política de privacidade não provam transmissão real. Não acesse conteúdo privado nem intercepte tráfego protegido sem autorização e escopo.

## Matriz de saída — uma linha por package name
Campos obrigatórios: package name; nome/versão/UID; fabricante/origem e evidência; categoria; função individual e confiança; estado por usuário; permissões (manifesto/runtime/especiais); AppOps (operação, modo, escopo e UID compartilhado); componentes/serviços; dependências e confiança; dados sensíveis e justificativa; telemetria (confirmada/provável/suspeita/inconclusiva/não observada no escopo), método e limites; alternativa FOSS/package name/compatibilidade/migração ou motivo N/A; recomendação; justificativa; risco; impacto funcional; pré-condições; comando apropriado ao modelo/build; validação; rollback; confiança; IDs de evidência, fontes e URLs. Campos N/A ou desconhecidos devem ser explicitamente rotulados, nunca vazios.

## Categorias de decisão
- MANTER — essencial/protegido: boot, framework, System UI, Package Manager/Installer, KeyStore/KeyChain, SELinux, modem/RIL, IMS/VoLTE/VoWiFi, chamadas/SMS/emergência, Wi-Fi/Bluetooth, áudio, câmera, biometria, atualizações, launcher/QuickStep e teclado ativo.
- MANTER — funcionalidade solicitada/usada pelo proprietário, inclusive bancos/autenticação e dependências.
- REVISAR PERMISSÕES — acesso sensível sem necessidade confirmada; avaliar efeitos antes da revogação.
- MONITORAR / EVIDÊNCIA INSUFICIENTE — função/dependência/atividade desconhecida.
- CANDIDATO A RESTRIÇÃO REVERSÍVEL — somente após função dispensável e dependências confirmadas, plano e testes.
- CANDIDATO A REMOÇÃO PARA USUÁRIO — último recurso, autorização individual, backup/rollback e teste.
“Bloatware” não é evidência nem justificativa suficiente.

## Níveis de evidência para telemetria
Confirmada: tráfego/dado observado e atribuído validamente ao pacote, método descrito. Provável: indicadores corroborantes, mas sem prova direta suficiente. Suspeita: indício limitado. Inconclusiva: ambígua/insuficiente. Não observada no escopo: não foi encontrada durante a coleta, sem afirmar que nunca ocorre. Cite fontes técnicas confiáveis (AOSP/Android, OEM oficial, código, manifesto) com título, URL e data de acesso; diferencie fato observado, documentação e hipótese.

## Arquivos requeridos
1. package-audit.csv/tsv: matriz completa, linha individual por pacote.
2. package-audit.md: análise detalhada alfabética, sem omissões.
3. package-summary.md: contagens por categoria/estado/recomendação/risco e cobertura.
4. change-plan.md: apenas proposta, com pré-condições, comandos, impacto, teste e reversão.
5. registro de evidências/fontes sanitizado.
6. relatório before/after após execução autorizada, separando proposto de realizado.

Se contexto/limite técnico impedir cobertura total, declare limite, enumere pendências e prossiga em lotes. Nunca declare cobertura integral sem reconciliação. Auditoria inicial somente leitura; aguarde autorização explícita antes de qualquer ação. Aprovação para um pacote/grupo não autoriza os demais.

## Escopo por fabricante e prevenção de contaminação cruzada

O prompt e a matriz de auditoria são genéricos. Identifique fabricante/modelo/variante/Android/ROM/build com evidência antes de qualquer pesquisa OEM. O inventário ADB deste dispositivo é a fonte primária. Consulte pacotes e documentação específicos somente do fabricante identificado; referências de Samsung não devem orientar Motorola, nem Motorola orientar Samsung, e assim por diante. Nunca trate pacote de referência como instalado ou removível sem constatação no inventário. Mantenha listas OEM em documentos separados, etiquetados por modelo/build e usados apenas como referência. Pacote desconhecido permanece pendente/inconclusivo. Componentes AOSP também precisam de validação no build real.

