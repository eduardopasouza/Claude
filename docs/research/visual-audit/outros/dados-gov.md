# dados.gov.br — Portal Brasileiro de Dados Abertos

- **URL:** https://dados.gov.br/
- **Categoria:** mercado-dados (catálogo federal CKAN)
- **Data auditoria:** 2026-04-17
- **Acesso:** público, sem login para consulta

## Status da auditoria
**PARCIAL — WebFetch retornou estrutura mínima** (SPA e/ou conteúdo renderizado dinamicamente). Foi possível confirmar que é um **portal CKAN customizado no padrão gov.br** com catálogo, listagem, filtros e ficha de dataset. Detalhes granulares vêm de conhecimento externo do CKAN federal.

## Propósito declarado
Portal Brasileiro de Dados Abertos — ponto único federal de catalogação de datasets abertos publicados por órgãos do governo federal (e, opcionalmente, estaduais/municipais que aderem). É o catálogo-meta: não hospeda todos os dados, mas **referencia e descreve** onde estão.

## Layout e navegação
Padrão **gov.br + CKAN**:
- **Header gov.br** com selo federal, busca, acessibilidade.
- **Hero**: barra de busca "Pesquise por conjunto de dados..." centrada + contadores globais (X mil datasets, Y organizações, Z temas).
- **Destaques**: seção com "conjuntos mais acessados", "recém publicados", "organizações em destaque".
- **Navegação por**: Organização (ministérios, autarquias, estatais), Tema (agricultura, saúde, educação, meio ambiente), Formato, Grupo.
- **Ficha do dataset**: título, órgão publicador, descrição, tags, licença, frequência de atualização, lista de **recursos** (cada arquivo/endpoint anexado: CSV/XLSX/PDF/JSON/SHP/WMS/API), data da última modificação.

## Features / dados expostos
- **Conjuntos de dados** filtráveis por:
  - Organização (órgão publicador)
  - Grupo / Tema (agricultura, meio ambiente, economia etc.)
  - Formato (CSV, XLSX, JSON, XML, SHP, GeoJSON, PDF, API/HTTP)
  - Licença (ODbL, CC-BY, domínio público)
  - Frequência de atualização (diária, mensal, anual, única)
- **Busca full-text** em título, descrição, tags.
- **Ficha com metadados ricos** (DCAT compatível).
- **API CKAN** exposta: `/api/3/action/package_search?q=...`, `package_show?id=...`, `group_list`, `organization_list`, `resource_show?id=...` — padrão CKAN mundial.

## UX / interações
- Facetas à esquerda, resultados à direita (padrão CKAN).
- Download direto dos recursos via URL fixa (CSV/XLSX direto do órgão publicador).
- Preview limitado (CKAN DataStore às vezes, mas nem todos datasets usam).
- Paleta gov.br com customizações CKAN.
- Tom utilitário, zero marketing.

## Preço e modelo de negócio
100% gratuito.

## API pública (se houver)
**Sim — CKAN API padrão**, extensamente documentada:
- `GET /api/3/action/package_search?q=agro&rows=50`
- `GET /api/3/action/package_show?id=<dataset-id>`
- `GET /api/3/action/organization_list`
- `GET /api/3/action/group_list`
- `GET /api/3/action/resource_search`
- Quando o recurso é um CSV num DataStore, há `datastore_search` e `datastore_search_sql` (SQL direto sobre o dataset).
- Sem chave, sem rate limit agressivo declarado. Pode haver throttling prático.

## Autenticação
Navegação e consulta: sem login. Publicar dataset (órgão): gov.br login com permissões.

## Conhecimento externo aplicável
- dados.gov.br hospeda **~12-15 mil datasets** em 2024-26, de centenas de órgãos. Cobertura irregular — alguns ministérios publicam rotineiramente, outros abandonam.
- Datasets agro-relevantes conhecidos: CONAB (safras, custos), MAPA (AGROFIT, ZARC), IBGE (produção agrícola municipal PAM, LSPA), INCRA (CNIR, SIGEF, assentamentos), IBAMA (embargos, autos de infração), ICMBio (UCs, RL).
- **Qualidade dos metadados varia** enormemente. Alguns datasets têm descrição rica + schema documentado; outros são um "link para CSV" sem explicação.
- **CKAN SQL API** é tesouro escondido: permite queries SQL diretas em alguns datasets, sem baixar o CSV inteiro.
- Oportunidade: construir agregador temático "agro-brasileiro" consumindo dados.gov.br + APIs bilaterais (IBGE, Embrapa, BCB). Nenhum player faz bem hoje.

## Insights para AgroJus
1. **dados.gov.br como plumbing ingestion**: AgroJus deve ter um crawler CKAN que periodicamente varre a organização "Conab", "Incra", "Ibama", "Embrapa" e sincroniza datasets atualizados. Pipeline confiável e legal.
2. **Dataset discovery para features futuras**: usar CKAN search para descobrir dados que ainda não ingerimos (ex.: assentamentos INCRA, embargos IBAMA, desapropriações históricas).
3. **Exemplo de UX para nossa tela de dados**: dados.gov.br mostra como listar dataset com faceted filters + ficha rica. AgroJus pode reaproveitar padrão — mas verticalizado para "temas agro".
4. **Badge de fonte oficial**: sempre que AgroJus usar dataset oficiado em dados.gov.br, exibir "Fonte: dados.gov.br — CONAB | dataset XYZ | atualizado em 2026-02-10". Credibilidade + rastreabilidade.
5. **Cruzamento SQL-like**: usando CKAN SQL API, AgroJus pode rodar queries cross-dataset sem baixar tudo (ex.: SELECT UF, SUM(area) FROM paam_soja WHERE ano=2025) — economiza infra.

## Gaps vs AgroJus (tabela)

| Dimensão | dados.gov.br | AgroJus |
|---|---|---|
| Propósito | Catálogo federal meta | Aplicação especializada agro-jurídica |
| Cobertura | Multi-setor (saúde, educação, agro, etc.) | Só agro + imóvel rural |
| UX | Utilitária CKAN | Visualização, mapa, laudo |
| Usabilidade | Engenheiro de dados / analista | Advogado, perito, banco, investidor |
| API | CKAN completo | CKAN consumido + REST agregada AgroJus |
| Qualidade de dado | Varia por órgão | Validada e normalizada por AgroJus |
| Contexto agro | Disperso em muitos datasets | Consolidado em ficha de imóvel |
| Atualização | Varia por órgão | Crawler com monitor de freshness |
| Dashboard | Nenhum | Dashboards interativos |
| Output usuário final | CSV/XLSX bruto | Laudo + relatório + API |
