# LexML — Rede de Informação Legislativa e Jurídica

- **URL:** https://www.lexml.gov.br/
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Status da auditoria
O portal principal `www.lexml.gov.br` excedeu o timeout de 60s no WebFetch (o site responde lento historicamente). A auditoria foi feita no site técnico `projeto.lexml.gov.br`, que descreve arquitetura e padrões. Layout do portal de busca não foi observado diretamente — seções marcadas abaixo como **conhecimento externo** são públicas e documentadas.

## Propósito declarado
Rede brasileira de informação legislativa e jurídica mantida pelo Senado Federal (GT LexML + PRODASEN + Interlegis). Integra, em catálogo único, legislação federal, estadual, municipal, jurisprudência e propostas legislativas produzidas pelos três poderes e três esferas federativas. O objetivo é padronizar a identificação, descoberta e citação de atos normativos via **URN LEX**.

## Layout e navegação
**Conhecimento externo:**
- Header com logo LexML + barra de busca simples + link "Busca Avançada".
- Resultado em lista com facetas à esquerda: tipo de documento, autoridade, localidade, ano, vigência.
- Cada documento tem página canônica com URN LEX (ex.: `urn:lex:br:federal:lei:2012-05-25;12651`) + links para provedores originais (Planalto, Senado, DOU).
- Barra lateral institucional com "Sobre", "Provedores", "Documentação técnica".

## Dados e funcionalidades expostas
**Conhecimento externo:**
- Legislação federal (Constituição, leis, decretos, medidas provisórias).
- Legislação estadual e municipal (cobertura heterogênea, depende da adesão do ente).
- Jurisprudência de tribunais federais (STF, STJ, TST, TSE).
- Doutrina indexada parcialmente.
- Proposições legislativas em tramitação.

## UX / interações (consulta, busca, filtros, download)
**Conhecimento externo:**
- Busca full-text com operadores booleanos.
- Facetas para refino.
- URL permalink por URN.
- Exportação: links aos provedores originais (redireciona para Planalto, DJE etc.) — LexML é **metadado + link**, não armazena íntegra.
- Formato técnico: XML LexML (esquemas `lexml-base`, `lexml-br-rigido`).

## API pública (endpoints, auth, formatos)
- **OAI-PMH** (Open Archives Initiative Protocol for Metadata Harvesting) — endpoint padrão para harvesting do catálogo por agregadores.
- **SRU** (Search/Retrieve via URL) — endpoint de busca federada.
- **URN LEX resolver:** resolve URN para URL do provedor original.
- Formato de dado: **XML estruturado** conforme schemas LexML + **RDF** com vocabulários controlados (localidade, autoridade, tipo, evento, língua, conteúdo).
- Schemas XSD disponíveis para validação local.

## Rate limits / cotas conhecidas
Não declarados publicamente. OAI-PMH historicamente permite harvesting completo; SRU tem limite implícito por requisição.

## Autenticação
- **Pública**, sem login, sem chave.
- Sem gov.br.

## Conhecimento externo aplicável
- URN LEX é **a forma canônica** de citar ato normativo em trabalhos técnicos — advogados sofisticados e juízes usam.
- Ex.: Lei 12.651/2012 → `urn:lex:br:federal:lei:2012-05-25;12651`.
- OAI-PMH permite **espelhar todo o catálogo** em base interna — estratégia para AgroJus obter baseline legislativo.
- Cobertura municipal é falha — depende da adesão do município. Muitos códigos municipais ambientais/tributários não estão em LexML.
- LexML não resolve "qual artigo está vigente hoje?" — responsabilidade fica com provedor ou curadoria externa (ex.: Normas Legais, Lexis).

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **URN LEX como identificador estável** deve ser adotada pelo AgroJus para citações de leis (legível por máquina + estável no tempo).
2. **OAI-PMH harvesting** é a forma correta de construir um índice legislativo interno — AgroJus ingere uma vez e enriquece.
3. **Facetas em busca de legislação** (tipo, ano, autoridade, localidade) é UX esperada por operador jurídico.
4. **Permalink por URN** é a cultura: não quebrar URL, garantir citabilidade em petição.
5. **Catálogo de metadados + link ao provedor** é estratégia leve — AgroJus pode adotar: armazenamos referência + cache do PDF, não tentamos ser "dono" do texto.
6. **Schema XML aberto** + **vocabulários RDF controlados** permite enriquecimento: AgroJus pode aumentar com temas específicos (agro, ambiental, tributário rural).

## Gaps vs AgroJus (tabela)

| Dimensão | LexML | AgroJus (alvo) |
|---|---|---|
| Cobertura | Federal forte, estadual/municipal fraca | Curadoria forte em legislação rural |
| API | OAI-PMH + SRU (arcaicos) | REST + GraphQL + OAI-PMH opcional |
| Busca | Full-text + facetas | Full-text + vetorial (bge-m3) + semântica |
| Identificador | URN LEX | URN LEX + slug interno |
| Vigência do artigo | Não calculada | Calculada (texto vigente em data X) |
| Cruzamento com caso | Não | Automático (lei citada no caso) |
| Busca por tema rural | Genérica | Taxonomia específica (Código Florestal, Lei da Mata Atlântica, etc.) |
| Doutrina | Parcial | Integrada (RT, Conjur, doutrina aberta) |
| Alerta de alteração legislativa | Não | Sim (webhook por norma/tema) |
| Performance | Lenta | Rápida (índice local) |
| Exportação | XML/RDF | JSON + BibTeX + ABNT |
| Interface | Clássica gov.br | Dark mode moderno |
