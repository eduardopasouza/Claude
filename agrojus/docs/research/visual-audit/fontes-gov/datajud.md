# DataJud — API Pública (CNJ)

- **URL:** https://www.cnj.jus.br/sistemas/datajud/api-publica/ (doc técnica em https://datajud-wiki.cnj.jus.br)
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (APIKey compartilhada)

## Status da auditoria
A URL institucional do CNJ (`www.cnj.jus.br/sistemas/datajud/api-publica/`) retornou **HTTP 403** ao WebFetch — bloqueio por user-agent ou WAF. A auditoria foi feita via wiki técnica `datajud-wiki.cnj.jus.br`, que contém a documentação operacional da API. A parte institucional (layout, menus, imagens) não pôde ser observada diretamente nesta sessão.

## Propósito declarado
Disponibilizar, via API pública, os metadados de processos judiciais públicos da Base Nacional de Dados do Poder Judiciário (DataJud), em conformidade com a Resolução CNJ nº 331/2020 e a Portaria CNJ nº 160/2020. A API expõe o padrão Elasticsearch "cru" — o cliente escreve queries DSL diretamente.

## Layout e navegação
**Wiki técnica observada** (`datajud-wiki.cnj.jus.br`):
- Menu lateral com seções: "Visão Geral", "Acesso" (chave de API), "Endpoints" (por tribunal), "Consultas" (exemplos Elasticsearch), "Campos" (dicionário), "Avisos".
- Navegação simples em wiki estilo markdown (MkDocs).
- Sem login para ver documentação.

## Dados e funcionalidades expostas
Escopo total: **mais de 90 endpoints** — um por tribunal — cobrindo:

- **Tribunais Superiores:** STJ, TST, TSE, STM.
- **Justiça Federal:** TRF1 a TRF6 (6 regionais).
- **Justiça Estadual:** 27 TJs (todos os estados + DF).
- **Justiça do Trabalho:** 24 TRTs regionais.
- **Justiça Eleitoral:** TREs regionais por estado.
- **Justiça Militar:** TJMs de MG, RS, SP + STM.

Cada processo traz metadados padronizados: número único CNJ, classe processual, assunto, órgão julgador, movimentações, data de autuação, data da última movimentação.

## UX / interações (consulta, busca, filtros, download)
- **Elasticsearch Query DSL** como linguagem de consulta — alto poder, alta curva de aprendizado.
- Consulta por número único CNJ, classe, assunto, órgão, data.
- Paginação via `from` + `size` (limite padrão ES 10.000 sem `search_after`).
- Não há UI de consulta oficial na API — o CNJ publica separadamente o "Consulta Processual" para humanos.

## API pública (endpoints, auth, formatos)
- **Base URL:** `https://api-publica.datajud.cnj.jus.br/{tribunal_alias}/_search`
- Exemplo: `https://api-publica.datajud.cnj.jus.br/api_publica_trf1/_search`
- **Protocolo:** HTTPS POST (Elasticsearch-like).
- **Formato:** JSON request body com query DSL; resposta JSON Elasticsearch-style (`hits.hits[]._source`).
- **Autenticação:** header `Authorization: APIKey <chave-pública-publicada-na-wiki>`.
  - Chave é **pública** e pode ser rotacionada a qualquer momento pelo CNJ.
- **Dicionário de campos:** publicado em `datajud-wiki.cnj.jus.br/campos/`.

## Rate limits / cotas conhecidas
Não detalhados na página de endpoints observada. Conhecimento externo: a API tem throttle agressivo em queries não paginadas corretamente; queries com `size` > 10.000 sem `search_after` falham. Uso massivo requer paginação com `search_after` + `sort` por `_id`.

## Autenticação
- **APIKey pública compartilhada** — qualquer pessoa usa a mesma chave, publicada na wiki.
- Chave pode ser rotacionada (risco operacional: integrações precisam monitorar wiki).
- Sem gov.br. Sem OAuth. Sem token por usuário.

## Conhecimento externo aplicável
- DataJud é **a mais completa base processual do Brasil** (todos os tribunais) — fonte obrigatória para monitoramento, inteligência jurídica e pesquisa empírica de direito.
- Dados não incluem peças processuais (texto completo) — apenas metadados e movimentações.
- Atualização é quase-real-time (incremental diário ou horário) para a maioria dos tribunais.
- Chave pública rotaciona tipicamente 1x por ano ou em incidentes — integradores precisam ler wiki ao quebrar.
- Alguns tribunais têm lag de sincronização (TJMA, TJPA, por exemplo).

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Elasticsearch como API** é potente mas hostil — AgroJus deve **abstrair** (oferecer endpoints REST simples) e **opcionalmente** passar DSL cru para power users.
2. **APIKey pública compartilhada** é um padrão interessante: zero friction para teste, mas exposto a abuso. AgroJus pode oferecer "chave demo" + tiers pagos.
3. **Endpoint por tribunal/alias** é modelo de namespace que AgroJus pode adotar (`/tribunal/trf1/`, `/tribunal/tjma/`).
4. **Dicionário de campos separado** é fundamental — AgroJus deve publicar dicionário de dados por fonte.
5. **Wiki MkDocs** com navegação lateral é padrão leve e funcional para doc técnica — AgroJus pode usar MkDocs Material ou Docusaurus.
6. **Movimentações como stream** no DataJud sugere: AgroJus deve ingerir DataJud e oferecer **webhook por processo/parte** — killer feature para advogado.

## Gaps vs AgroJus (tabela)

| Dimensão | DataJud | AgroJus (alvo) |
|---|---|---|
| Cobertura tribunais | 90+ | Indireta (consome DataJud) |
| API | Elasticsearch DSL cru | REST + GraphQL + DSL opcional |
| Autenticação | APIKey pública | gov.br + token por usuário |
| Rate limit | Opaco | Por tier |
| Paginação | from/size + search_after | Cursor estável |
| UI oficial | Nenhuma | Dashboard + busca facetada |
| Alertas por processo | Manual | Webhook + push |
| Cruzamento parte × imóvel | Não | Core do AgroJus |
| Texto completo de decisões | Não | Cruzado com DJen/LexML |
| Extração de teses | Não | Enriquecimento NLP |
| Timeline processual | JSON bruto | Visualizada e narrada |
| Laudo de dossiê | Não | Gerado por AgroJus |
