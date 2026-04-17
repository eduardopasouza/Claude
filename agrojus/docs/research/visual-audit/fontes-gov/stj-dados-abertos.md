# STJ — Dados Abertos

- **URL:** https://dadosabertos.web.stj.jus.br/
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Propósito declarado
Portal oficial de dados abertos do Superior Tribunal de Justiça, rodando sobre **CKAN** (padrão mundial de catálogos de dados abertos). Visa "transparência" e "controle social" conforme política administrativa do STJ, expondo datasets jurisprudenciais e administrativos em formato legível por máquina.

## Layout e navegação
- **Header:** logo STJ + "Dados Abertos" + barra de pesquisa universal.
- **Grupos/Categorias** (ao estilo CKAN): Jurisprudência, Consulta Processual, Gestão de Precedentes, Sessão de Julgamento, Diário da Justiça Eletrônica.
- **URLs canônicas CKAN:** `/group/`, `/dataset/`, `/organization/`.
- **Total declarado:** "19 conjuntos de dados" (na página, apenas 2 destacados — Atas de Distribuição e Precedentes Qualificados).
- Footer com 8 links de redes sociais + formulário de avaliação do portal + ouvidoria.

## Dados e funcionalidades expostas
Datasets explícitos observados:
- **Atas de Distribuição**
- **Precedentes Qualificados**

Grupos temáticos indicam existência de:
- Jurisprudência (decisões, acórdãos)
- Consulta processual
- Sessões de julgamento (pautas, atas)
- DJe (publicações eletrônicas)

## UX / interações (consulta, busca, filtros, download)
- **Busca facetada CKAN** nativa: filtros por grupo, organização, tag, formato, licença.
- Página de dataset CKAN padrão: título, descrição, lista de "Resources" (arquivos individuais) com botão de download + preview quando CSV.
- Paginação por 20 resultados (default CKAN).
- Download direto + botão "API" por resource (API CKAN datastore quando disponível).

## API pública (endpoints, auth, formatos)
- **CKAN API** disponível em `/api/3/action/` — padrão CKAN.
- Endpoints principais: `package_search`, `package_show`, `resource_show`, `datastore_search`, `datastore_search_sql`.
- Documentação referenciada: `docs.ckan.org`.
- **DCAT/RDF** suportado por CKAN (catálogo legível por agregadores de dados abertos).
- Formatos de resource: tipicamente CSV, JSON, XML (varia por dataset — não declarado na home).

## Rate limits / cotas conhecidas
Não declarados publicamente. CKAN em geral não aplica rate limit por default — depende de configuração do deployer (throttle por IP via reverse proxy é comum mas não publicado).

## Autenticação
- **Pública**, sem login.
- API CKAN aceita API key opcional para escrita — não relevante para consulta pública.
- Sem integração gov.br.

## Conhecimento externo aplicável
- Dataset "Precedentes Qualificados" é uma das **fontes mais valiosas do Brasil jurídico**: expõe Temas Repetitivos, IACs, IRDRs com status de vigência — core para pesquisa de teses firmadas.
- CKAN é o padrão internacional (data.gov, dados.gov.br, data.europa.eu) — integradores conhecem o modelo.
- Há MCP disponível para CKAN (`mcp__CKAN_MCP_Server__*`) que permite consulta programática.
- STJ é o tribunal com maior maturidade de dados abertos no Judiciário BR — junto com CNJ/TSE.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **CKAN como catálogo** é a opção zero-esforço: AgroJus pode expor datasets derivados via CKAN interno (ou federado), e o usuário técnico já sabe navegar.
2. **Busca facetada** (por formato, tag, grupo) é expectativa mínima de qualquer catálogo — AgroJus search deve ter facetas (UF, bioma, fonte, ano).
3. **API key opcional** (CKAN) é bom padrão: tudo público sem token, mas token desbloqueia rate limits maiores.
4. **URLs canônicas previsíveis** (`/dataset/<slug>`, `/group/<slug>`) melhoram SEO e permalink — AgroJus deve ter URL estável por imóvel, caso, processo.
5. **Precedentes Qualificados** é dataset que AgroJus deve indexar e vincular ao caso (extrair tema → mostrar no dashboard do caso).
6. **DCAT/RDF** é bônus — AgroJus pode expor catálogo em DCAT para ser descoberto por crawlers gov.

## Gaps vs AgroJus (tabela)

| Dimensão | STJ Dados Abertos | AgroJus (alvo) |
|---|---|---|
| Plataforma | CKAN | CKAN interno + app próprio |
| Datasets | 19 (jurisprudência) | Multi-domínio (jurisprudência + geo + agro) |
| API | CKAN action API | CKAN + REST próprio + MCP |
| Busca | Facetada CKAN | Facetada + full-text + vetorial (bge-m3) |
| Precedentes qualificados | Dataset bruto | Extraído, linkado ao caso |
| Rate limit | Não declarado | Declarado e tiered |
| Autenticação | Anônima | gov.br + token opcional |
| Geo | Nenhum | Core |
| Cruzamento com imóvel | Nenhum | Jurisprudência por região/bioma |
| Visualização | Lista + preview CSV | Dashboard + timeline |
| Alertas | Não | Novos precedentes por tema |
| Relatório jurídico | Não | Laudo com jurisprudência linkada |
