# SIDRA — Sistema IBGE de Recuperação Automática

- **URL:** https://sidra.ibge.gov.br/
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (login opcional para salvar consultas)

## Propósito declarado
"Sistema IBGE de Recuperação Automática" — é o hub oficial de **tabelas estatísticas** produzidas pelas pesquisas do IBGE. Permite acesso granular a séries temporais com recorte territorial e variáveis escolhidas pelo usuário. É o mecanismo padrão para extrair estatísticas oficiais no Brasil.

## Layout e navegação
- **Menu principal:** "Pesquisas", "Acervo", "Território", "Contato".
- **Organização temática:** indicador, população, economia, ambiente, agropecuária.
- **Página de tabela:** interface de "construtor de consulta" — usuário escolhe variáveis, classificações, território e período em caixas sequenciais antes de gerar resultado.
- Identidade visual IBGE (azul institucional), layout em colunas, alta densidade informacional — UI pensada para pesquisadores, não leigos.

## Dados e funcionalidades expostas
**Relevantes para AgroJus:**
- **PAM — Produção Agrícola Municipal** (área plantada, produção, valor por cultura por município).
- **PPM — Pesquisa da Pecuária Municipal** (rebanho bovino, suíno, aves por município).
- **Censo Agropecuário** (decenal — última edição 2017).
- **PEVS — Produção da Extração Vegetal e da Silvicultura**.

**Outras pesquisas:**
- PIB Munic, PIA, CNA, CEMPRE (economia).
- IPCA, INPC, IPP, SINAPI (preços).
- PNADC mensal/trimestral/anual (trabalho).
- PMC, PMS, PAS, PAC (setoriais).

## UX / interações (consulta, busca, filtros, download)
- Fluxo de construção de tabela (stepper): "Variáveis → Classificações → Territórios → Períodos → Visualizar".
- Paginação de células grandes: consultas com muitos municípios × períodos podem retornar 100k+ células.
- **Formatos de download:** CSV, XLS, XLSX, HTML (versão lida na tela), ODS, JSON.
- **Copiar URL da consulta** — permalink com os parâmetros — é feature crítica (pesquisador compartilha link).
- Visualização em tabela pivotada + gráfico de linhas/barras opcional.

## API pública (endpoints, auth, formatos)
- **Base:** `https://apisidra.ibge.gov.br/values/...`
- **Formato da URL:** estilo "path-param" onde cada segmento é um filtro:
  - `/t/{tabela}` — tabela
  - `/n{nivel}/{territorios}` — nível territorial (N3=UF, N6=Município etc.) e códigos IBGE
  - `/v/{variáveis}` — variáveis
  - `/p/{períodos}` — períodos
  - `/c{classificação}/{categorias}` — classificação (ex.: produto agrícola)
  - `/f/{formato}` — formato (`u` padrão, `n` nome, `c` código)
- Exemplo: `https://apisidra.ibge.gov.br/values/t/1612/n6/all/v/215/p/last%2010/c81/all/f/u`
- **Resposta:** JSON array (primeiro item é o dicionário de colunas).
- **Documentação:** `https://apisidra.ibge.gov.br/home/ajuda` (estilo wiki).

## Rate limits / cotas conhecidas
Não declarados formalmente. Experiência prática:
- Queries muito grandes (todos os municípios × todos os anos × todas as culturas) retornam HTTP 500 ou truncam.
- Regra prática: manter abaixo de ~50.000 células por requisição; paginar por UF ou por período.

## Autenticação
- Consulta web: pública, sem login necessário.
- **Login opcional** para salvar consultas favoritas (conta SIDRA + OAuth Facebook/Google/Microsoft).
- API pública: **sem token**, sem autenticação.

## Conhecimento externo aplicável
- Tabelas PAM/PPM são **fonte oficial** para indenização, seguro agrícola, perícia econômica em ações indenizatórias rurais.
- Código IBGE de município (7 dígitos) é o identificador territorial canônico no Brasil — AgroJus deve adotar.
- Censo Agropecuário 2017 é a base mais rica (tamanho de estabelecimento, relações de posse, mão de obra, maquinário) mas desatualizada — próxima edição 2026/2027.
- Existe o pacote R `sidrar` e Python `sidrapy` amplamente usados pela comunidade — padrão de facto.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Construtor de consulta em stepper** (variáveis → território → período → visualizar) é o padrão mental do pesquisador BR — AgroJus pode oferecer o mesmo pattern para busca avançada em jurisprudência ou base fundiária.
2. **Permalink da consulta com todos os params na URL** é fundamental — AgroJus precisa ter estado 100% refletido em URL (filtros + zoom + layer).
3. **URL "path-param" estilo REST rígido** (`/t/1612/n6/all/v/215`) é legível e cacheável — bom para ingestão programática.
4. **Primeiro item do JSON como dicionário de colunas** é peculiaridade SIDRA — AgroJus deve **evitar** esse padrão (preferir `schema` separado + `data`).
5. **Código IBGE de município** deve ser atributo de qualquer entidade territorial no AgroJus.
6. **Exportação em múltiplos formatos** (CSV/XLS/JSON/ODS/HTML) é expectativa — AgroJus deve oferecer ao menos 3.
7. **Login opcional com OAuth social** é UX leve — AgroJus pode oferecer gov.br + Google como opções.

## Gaps vs AgroJus (tabela)

| Dimensão | SIDRA | AgroJus (alvo) |
|---|---|---|
| Dados | Estatística oficial IBGE | Multi-fonte (inclui SIDRA via ingestão) |
| API | REST path-param "IBGE-style" | REST query-param convencional |
| Autenticação | Anônima | gov.br + token + OAuth |
| Rate limit | Opaco | Declarado |
| Granularidade | Município (mínimo) | Imóvel/polígono (mínimo) |
| Consulta | Construtor stepper | Busca livre + construtor |
| Permalink | Sim | Sim |
| Exportação | CSV/XLS/JSON/ODS/HTML | CSV/Parquet/GeoJSON/PDF laudo |
| Cruzamento com imóvel | Não | PAM por município do imóvel |
| Interpretação | Dado bruto | Contextualizado (tese aplicável) |
| Timeline temporal | Tabela pivô | Gráfico + mapa animado |
| Swagger | Não oficial | Sim |
| Cache inteligente | Não | Sim (queries comuns) |
