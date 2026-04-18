# IBAMA — Consulta Pública de Áreas Embargadas

- **URL:** https://servicos.ibama.gov.br/ctf/publico/areasembargadas/ConsultaPublicaAreasEmbargadas.php
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (reCAPTCHA Enterprise)

## Status da auditoria
A página retornou conteúdo limitado ao WebFetch — possivelmente porque os formulários de filtro são renderizados via JavaScript após proteção reCAPTCHA Enterprise. Apenas a moldura estática (cabeçalho, brasão, links de política) foi capturada. Os campos específicos de busca (CPF/CNPJ, TAD, UF) não puderam ser observados diretamente. Seções abaixo marcadas como **conhecimento externo** baseiam-se em uso prévio público documentado.

## Propósito declarado
"Consulta de Autuações Ambientais e Embargos" — permite ao cidadão consultar áreas com embargo vigente decretado pelo IBAMA (Lei 9.605/1998 + Decreto 6.514/2008). O embargo suspende atividade econômica sobre a área infratora até regularização. É fonte crítica para due diligence de aquisição rural, crédito rural (Resolução BCB 140/2021) e defesa em ações ambientais.

## Layout e navegação
Elementos observados:
- **Brasão da República + logo IBAMA + "Ministério do Meio Ambiente"** — assinatura institucional típica.
- Referência ao **Cadastro Técnico Federal (CTF)** — o embargo está linkado ao CTF/APP.
- **"Fechar janela"** como botão — sugere que a consulta abre em popup/iframe.
- Seção "Ajuda ao Usuário" disponível.
- **reCAPTCHA Enterprise** na base da página, com links a política Google.

## Dados e funcionalidades expostas
**Conhecimento externo aplicável:**
- Filtros típicos: CPF/CNPJ do autuado, nome, UF, município, número do TAD (Termo de Autuação e Documentação), número de processo, período de autuação.
- Resultado é tabela paginada com colunas: nome do autuado, CPF/CNPJ, município/UF, área embargada (ha), coordenadas (às vezes), tipo de infração, data do embargo, situação (vigente/suspenso/cancelado).
- Visualização em mapa via link cruzado para o "Painel do IBAMA" (arcgis.com) — mas não integrada à consulta nominal.
- Download CSV/XLS varia por perfil de resultado — historicamente limitado.

## UX / interações (consulta, busca, filtros, download)
- Formulário vertical simples com validação server-side.
- Paginação clássica (10/25/50 por página).
- Sem busca por polígono (essa fica no Painel ArcGIS separado).
- Exportação historicamente limitada a visualização; bulk exige requisição LAI.

## API pública (endpoints, auth, formatos)
- **Não há API REST documentada** neste endpoint.
- IBAMA publica **serviços ArcGIS REST** em `siscom.ibama.gov.br/arcgis/rest/services/` com a feature layer "embargos" — consumível por WMS/WFS/GeoJSON.
- Dados abertos CSV consolidados em `dadosabertos.ibama.gov.br` (CKAN) com atualização mensal, incluindo dataset "ADA — Autos de Infração" e "Áreas Embargadas".

## Rate limits / cotas conhecidas
Não declarados. **reCAPTCHA Enterprise** é o rate-limiting implícito — impede scraping automatizado. Excesso de acessos do mesmo IP gera bloqueio visual sem mensagem formal.

## Autenticação
- **Pública**, sem login.
- reCAPTCHA obrigatório antes de submeter consulta.
- Não integra gov.br (ferramenta anterior à política unificada).

## Conhecimento externo aplicável
- Lista de áreas embargadas é **prova pré-constituída** em ação civil pública ambiental e impedimento de crédito rural (Bacen).
- Embargo IBAMA é diferente de embargo ICMBio (Unidades de Conservação) — ambos precisam ser cruzados.
- Dataset CKAN do IBAMA tem atraso de 30-45 dias em relação ao sistema transacional.
- Em litígios, advogados frequentemente precisam obter a "Ficha do Embargo" em PDF — não exposta via API.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Brasão + logo ministerial no header** é a assinatura de credibilidade esperada — AgroJus pode adotar brasão gov.br discreto em relatórios de compliance.
2. **reCAPTCHA Enterprise** é o padrão atual gov — AgroJus deve usar hCaptcha/reCAPTCHA apenas em endpoints anônimos, e tier pago sem CAPTCHA.
3. **Consulta em popup/iframe** é padrão legado a evitar — AgroJus deve usar SPA navegável.
4. **Serviço ArcGIS REST desacoplado** do front HTML é padrão: o advogado técnico vai direto ao ArcGIS; o leigo usa o form. AgroJus pode oferecer **ambas as portas** (UI + API desde o free tier).
5. **Dataset CKAN paralelo** é "dados abertos" oficial — AgroJus deve indexar e reexpor com busca mais rica (full-text + geo).

## Gaps vs AgroJus (tabela)

| Dimensão | IBAMA Embargos | AgroJus (alvo) |
|---|---|---|
| API REST | Apenas ArcGIS (não documentada como API pública) | REST documentada |
| Filtros | Formulário estático | Busca facetada + geo + texto |
| Proteção | reCAPTCHA opaco | Tier free c/ limite + pago sem CAPTCHA |
| Exportação | Visualização, sem bulk fácil | CSV/GeoJSON/Parquet/PDF laudo |
| Cruzamento CAR × embargo | Manual | Automático em background |
| Histórico temporal | Tabular | Timeline + mapa |
| Ficha do embargo PDF | Não exposta | Gerada via AgroJus |
| Webhook novo embargo | Não | Sim (alerta para advogado) |
| Autenticação | Anônimo + CAPTCHA | gov.br + token |
| Embargo ICMBio | Fora do escopo | Incluído (multi-fonte) |
| Linkagem a processo judicial | Não | Sim (cruzamento Datajud) |
| UI mobile | Desktop-first | Responsivo |
