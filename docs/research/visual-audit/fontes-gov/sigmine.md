# SIGMINE — ArcGIS REST Service (ANM)

- **URL:** https://geo.anm.gov.br/arcgis/rest/services/SIGMINE/dados_anm/MapServer
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (endpoint REST aberto)

## Propósito declarado
"Serviço de compartilhamento dos dados espaciais mantidos pela Agência Nacional de Mineração." Expõe os dados cadastrais de processos minerários e camadas correlatas para consumo via ArcGIS REST API — é a fonte oficial consumida por ferramentas GIS para detecção de interferência com imóveis rurais, UCs, terras indígenas.

## Layout e navegação
Este endpoint não é uma página web navegável, e sim um **service descriptor JSON/HTML** do ArcGIS Server. A página HTML gerada pelo servidor contém:
- Cabeçalho com nome do serviço e breadcrumb `Home > SIGMINE > dados_anm (MapServer)`.
- Metadados do serviço (descrição, cópia, extensão espacial).
- **Lista de camadas** (Layers) com link para cada sub-endpoint.
- **Seção de operações suportadas** (Export Map, Identify, Find, Query).
- Links para representações alternativas: JSON, SOAP, KMZ.

UI é auto-gerada pelo ArcGIS — idêntica em todo órgão que usa ArcGIS Server (IBAMA, FUNAI, INCRA etc.), o que cria familiaridade entre técnicos GIS.

## Dados e funcionalidades expostas

**Camadas disponíveis:**

| ID | Camada |
|---|---|
| 0 | Processos minerários ativos |
| 1 | Áreas de proteção de fonte |
| 2 | Arrendamentos |
| 3 | Áreas de bloqueio |
| 4 | Reservas garimpeiras |

Cada camada oferece: atributos cadastrais (número do processo, titular, substância, fase, área em ha) + geometria poligonal.

## UX / interações (consulta, busca, filtros, download)
- **Query por atributo** via parâmetro `where` (SQL-like).
- **Query por geometria** via `geometry` + `spatialRel` (intersects, contains etc.).
- **Identify** para clique em mapa.
- **Export Map** para gerar imagem renderizada (PNG/JPG/PDF).
- **Find** para busca textual em múltiplos campos.
- **Paginação:** via `resultOffset` + `resultRecordCount` (padrão ArcGIS).

## API pública (endpoints, auth, formatos)
- **Arquitetura:** ArcGIS REST API (padrão Esri, não OpenAPI).
- **Formatos de query response:** JSON, GeoJSON, PBF (Protocol Buffers).
- **Formatos de export:** PNG32, PNG24, PNG, JPG, DIB, TIFF, EMF, PS, **PDF**, GIF, SVG, SVGZ, BMP.
- **Operações:** Export Map, Identify, Find, QueryLegends, QueryDomains, Return Updates.
- **CRS:** SIRGAS2000 (EPSG:4674) — padrão oficial brasileiro.
- Serviço também publica **WMS** paralelo em `/WMSServer` e **WFS** em `/WFSServer`.

## Rate limits / cotas conhecidas
- **MaxRecordCount:** 5000 registros por requisição (paginação obrigatória acima).
- **MaxSelectionCount:** 2000.
- Escala máxima: 1:10.000.000 a 1:0.
- Não há rate limit numérico declarado por IP, mas o servidor ArcGIS tem throttle implícito sob carga.

## Autenticação
- **Pública** para consulta (GET query).
- Informação do descritor diz "Login requerido" em contextos de edição/escrita — não se aplica a leitura pública.
- Não integra gov.br. Não exige token.

## Conhecimento externo aplicável
- Processo minerário ativo sobreposto a imóvel rural cria **direito de superfície minerário** (CF art. 176) — crítica em ações possessórias e aquisição rural.
- Requerimentos de lavra e alvarás de pesquisa têm tratamento distinto (ambos na camada 0 com atributo `FASE`).
- Camadas são **atualizadas diariamente** — maior frequência entre fontes gov brasileiras.
- Dataset shapefile consolidado é publicado em `https://app.anm.gov.br/dadosabertos/SIGMINE/PROCESSOS_MINERARIOS/` com download por UF.
- Integra o "triângulo de sobreposição" crítica em AgroJus: CAR × SIGMINE × Terras Indígenas FUNAI.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **ArcGIS REST é o lingua franca GIS gov** — AgroJus deve **consumir** como cliente (ou oferecer **proxy** que traduz ArcGIS → OGC API padrão).
2. **Self-descriptive endpoint HTML** do ArcGIS é padrão: usuário GIS espera que colocar `?f=html` ou abrir a URL mostre descrição. AgroJus pode replicar: cada endpoint deve ter representação HTML navegável.
3. **GeoJSON + PBF** como formatos de query: AgroJus deve oferecer GeoJSON (universal) + MVT (tiles vetoriais para mapa web).
4. **maxRecordCount=5000** com paginação por offset é o padrão que integradores esperam — AgroJus deve implementar paginação estável.
5. **SIRGAS2000 (EPSG:4674)** é o CRS brasileiro oficial — AgroJus deve aceitar/retornar em SIRGAS2000 + WGS84, nunca só WGS84.
6. **Atualização diária** é a barra mínima para dado "vivo" — AgroJus deve documentar frequência de atualização por fonte.

## Gaps vs AgroJus (tabela)

| Dimensão | SIGMINE ArcGIS | AgroJus (alvo) |
|---|---|---|
| Padrão de API | ArcGIS REST (Esri) | OGC API + REST próprio |
| Formato | JSON, GeoJSON, PBF | GeoJSON, MVT, Parquet geo |
| Paginação | Offset-based (5000/req) | Offset + cursor |
| CRS | SIRGAS2000 | SIRGAS2000 + WGS84 negociáveis |
| Autenticação | Anônimo | gov.br + token |
| Rate limit declarado | Implícito | Explícito por tier |
| Atualização | Diária | Diária + webhook de mudança |
| Cruzamento com CAR | Manual | Automático |
| Busca nominal por titular | Por atributo SQL | Full-text + facetas |
| Visual HTML do endpoint | Auto-gerado ArcGIS | HTML + Swagger customizado |
| PDF de interferência | Não gerado | Laudo automático de sobreposição |
| Atributos em português | Sim | Sim + glossário técnico linkado |
