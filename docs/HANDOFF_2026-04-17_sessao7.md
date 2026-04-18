# AgroJus — Handoff Sessão 7 (2026-04-17)

> **Substitui o handoff da sessão 6.**
> Sessão 7: Sprint 1 **+ Sprint 2a + 2b** completos — **7 abas da ficha do imóvel funcionais**, 4 frentes de dados destravadas (Embrapa 7/9 APIs, IBGE choropleth 16 métricas, IBAMA 16k autos carregados, MapBiomas Alerta com JWT).
> **Prioridade:** ler Seção 1 (tudo novo) → Seção 3 (pendências) → Seção 10 (próximos sprints).

---

## 1. O QUE FOI FEITO NESTA SESSÃO

### 1.1 Sprint 1a — Embrapa AgroAPI (🟢 7/9 APIs ativas)

**Problema anterior:** OAuth funcionava mas os paths individuais das 9 APIs retornavam HTTP 404 — o collector tinha paths inventados.

**Solução:** extraídos Swagger specs de cada API via `/store/api-docs/agroapi/<Name>/<Version>` + probe com curl + token OAuth2. Collector e router reescritos com paths REAIS:

| API | Base path | Endpoints úteis | Status |
|---|---|---|---|
| Agritec | `/agritec/v2` | `/culturas` (188 culturas), `/municipios?uf=MA`, `/zoneamento?idCultura=&codigoIBGE=&risco=`, `/cultivares?safra=&idCultura=&uf=` | ✅ |
| AGROFIT | `/agrofit/v1` | `/culturas`, `/search/produtos-formulados?cultura=&praga=`, `/produtos-tecnicos/{num}`, `/titulares-registros` | ✅ |
| Bioinsumos | `/bioinsumos/v2` | `/search/inoculantes?cultura=`, `/search/produtos-biologicos`, `/pragas`, `/plantas-daninhas` | ✅ |
| AgroTermos | `/agrotermos/v1` | `/termo?descricao=`, `/termoParcial?descricao=`, `/relacoes` | ✅ |
| BovTrace | `/bovtrace/v1` | `/racas`, `/protocolos`, `/transitos/{codigo}` | ✅ |
| RespondeAgro | `/respondeagro/v1` | `/_doc/{id}`, `/_search/template` (POST) | ✅ (semântica Q&A) |
| SmartSolosExpert | `/smartsolos/expert/v1` ⚠ | `/health`, `/classification` (POST), `/verification` (POST) | ✅ |
| PlantAnnot | `/plantannot/v2` | `/autocomplete` (bioinfo — pouco útil) | ⚠ minimal |
| Sting | `/sting/v1` | PDB proteínas (NÃO é geo — descartado) | ⚠ minimal |

**Descobertas importantes:**
- SmartSolos tem base DIFERENTE: `/smartsolos/expert/v1` (não `/smartsolos/v1`)
- Sting é biologia estrutural (PDB), não georreferenciamento como antes documentado
- Endpoints WSO2 retornam HTTP 400 "dados-invalidos" para params errados (válido = auth OK)

**Arquivos:**
- `backend/app/collectors/embrapa.py` — reescrito
- `backend/app/api/embrapa.py` — reescrito (27 endpoints)

### 1.2 Sprint 1b — IBGE Choropleth (🟢 16 métricas, 14 camadas ativadas)

**Problema anterior:** 14 camadas stub no catálogo (`comingSoon: true`) apontando para `endpoint: "ibge"` inexistente.

**Solução:** criado módulo `/api/v1/geo/ibge/choropleth/{metric}/{ano}?uf=MA` que:
1. Baixa malha municipal do IBGE v3 (GeoJSON intermediário)
2. Baixa valores SIDRA paralelamente (via `/f/u` unified = códigos+nomes)
3. Merge por código IBGE (`D1C`)
4. Retorna FeatureCollection com `properties.value` para colorir

**16 métricas disponíveis:**
- **PAM** (SIDRA 1612): pam_soja, pam_milho, pam_cana, pam_cafe, pam_algodao, pam_arroz, pam_feijao, pam_trigo, pam_area_soja, pam_valor_soja
- **PPM** (SIDRA 3939): ppm_bovinos, ppm_suinos, ppm_ovinos, ppm_bubalinos
- **Socioeconômico**: populacao (SIDRA 6579), pib_total, pib_per_capita (SIDRA 5938)

**Validado via curl:**
- MA 2021 populacao → 217/217 municípios, São Luís 113.783 habitantes ✅
- MA 2022 soja → 217/217 (71 com produção), top produtor Balsas 200.720 ton ✅
- MA 2022 bovinos → 217/217, top Açailândia 395.335 cabeças ✅

**Bug crítico descoberto:** SIDRA `/f/n` retorna só NOMES (sem D1C). Usar `/f/u` (unified). 1h perdida diagnosticando.

**Códigos SIDRA PAM c81**: 2713=Soja, 2707=Milho, 2711=Cana, 2702=Café, 2696=Algodão, 2692=Arroz, 2704=Feijão, 2716=Trigo
**Códigos PPM c79**: 2670=Bovino, 2681=Suíno, 2684=Ovino, 2672=Bubalino

**Arquivos:**
- `backend/app/api/ibge_choropleth.py` — novo
- `frontend_v2/src/lib/layers-catalog.ts` — 14 camadas saíram de stub, agora apontam para `endpoint: "ibge_choropleth"`

### 1.3 Sprint 1c — IBAMA CSV ETL (🟡 script pronto, não executado)

**Problema anterior:** 104.284 registros em `environmental_alerts` misturando IBAMA+MTE sem lat/lon dedicado para camada de mapa.

**Solução:** script standalone para baixar o CSV oficial e carregar numa tabela PostGIS dedicada `geo_autos_ibama`:
```bash
docker compose exec backend python scripts/download_ibama_autos.py
```

- Fonte: `dadosabertos.ibama.gov.br/dados/SICAFI/relatorio_auto_infracao_ibama_coords.csv` (~200MB, ~1.2M autos)
- Schema: `seq_auto, num_auto, data_auto, nome, cpf_cnpj, descricao, valor, municipio, uf, latitude, longitude, geometry`
- Índices: cpf_cnpj, (uf, municipio), GIST(geometry)
- Idempotente via `ON CONFLICT (num_auto) DO NOTHING`

**NÃO EXECUTADO** — Eduardo precisa aprovar (vai demorar 2-3 min, 200MB download). Para rodar:
```bash
cd C:\dev\agrojus-workspace\agrojus
docker compose exec backend python scripts/download_ibama_autos.py
```

**Arquivos:**
- `backend/scripts/download_ibama_autos.py` — novo

### 1.4 Sprint 1d — MapBiomas Alerta GraphQL (🟢 auth + alerts tempo real)

**Descobertas via introspection (2 horas de trabalho):**

1. **Endpoint público:** `https://plataforma.alerta.mapbiomas.org/api/v2/graphql`
2. **REST `/auth/login` retorna HTTP 500** (deprecated — ignore)
3. **Auth correta = GraphQL mutation:**
   ```graphql
   mutation($e: String!, $p: String!) {
     signIn(email: $e, password: $p) { token }
   }
   ```
4. **Queries públicas (sem auth):** `version`, `alertDateRange`
5. **Queries autenticadas:** `alerts`, `alert`, `ruralProperty`, `territoryOptions`
6. **Schema:**
   - `alerts(startDate, endDate, territoryIds, sources: [SourceTypes!], page, limit)`
   - `AlertData.coordenates { latitude longitude }` (não `lat/lng`)
   - `AlertData.crossedStates`, `crossedCities`, `crossedBiomes` (LIST)
   - `AlertData.sources` (LIST no objeto; enum `SourceTypes` no argumento)

**Validado:** query alerts dez/2025 retornou alertCode 1551312, Mata Atlântica/PR/Coronel Vivida, 0.3248ha, coordenadas (-25.967, -52.641) ✅

**Arquivos:**
- `backend/app/collectors/mapbiomas_alerta.py` — novo
- `backend/app/api/mapbiomas.py` — novo (6 endpoints)

### 1.5 Sprint 2 — Ficha do imóvel `/imoveis/[car]` (🟢 7/12 abas funcionais)

**A tela mais importante do produto agora EXISTE.**

**Arquitetura:**
- Rota dinâmica `/imoveis/[car]` (Next.js 16 App Router com `use(params)`)
- Componentes em `src/components/imovel/`: PropertyHeader, TabNav, tabs/*
- Dark mode Forest/Onyx, useSWR cache, fetchWithAuth
- OmniSearch (TopBar) agora detecta código CAR (regex UF-XXXX-HEX32) e roteia

**Abas implementadas:**

1. **Visão Geral** — score de compliance (0-100) + 8 KPI cards + alertas MapBiomas tempo real + resumo das 8 camadas verificadas. Fórmula: 100 base, -40 TI, -35 embargo ICMBio, -25 UC, -15 PRODES/DETER, -10 MapBiomas, -5/alerta recente.
2. **Compliance** — wrapper de `/api/v1/compliance/mcr29` e `/eudr`. Toggle MCR 2.9 ↔ EUDR. POST automático com car_code + centroid. Banner overall (APTO/RESTRITO/BLOQUEADO) + lista de checks com regulamentação citada.
3. **Dossiê** — chama `/property/{car}/overlaps/geojson`, agrupa por tipo (TI, UC, embargo, PRODES, DETER, MapBiomas, SIGEF). Cada grupo mostra gravidade + top 8 features + contagem.
4. **Histórico** — MapBiomas Alerta `/mapbiomas/property/{car}`, timeline mensal (YYYY-MM), área total afetada, % do imóvel.
5. **Agronomia** — Embrapa Agritec: município (com região ZARC soja/trigo), culturas disponíveis, destaque ZARC.
6. **Clima** — NASA POWER (últimos 30 dias): temperatura média, precipitação total + diária, mini-gráfico de barras.
7. **Jurídico** — Form CPF/CNPJ (LGPD: CAR não expõe), query DataJud `/lawsuits/search/{cpf}`, lista processos 13 tribunais.

**Abas pendentes (marcadas "em breve" no TabNav):**
8. Valuation (NBR 14.653-3 — sprint 4)
9. Logística (armazéns/frigos/portos próximos)
10. Crédito (SICOR BCB)
11. Monitoramento (webhooks alertas)
12. Ações (laudo PDF, minuta DOCX, export GeoPackage)

### 1.6 Sprint 2c — Fix de renderização choropleth no mapa 🟢

**Problema reportado:** usuário clica nas 14 camadas IBGE choropleth no `LayerTreePanel`, mas elas não renderizam no mapa.

**Causa:** o switch em `MapComponent.tsx → ActiveLayer.endpoint` só tratava `"postgis"` e `"geo"`. As 14 camadas IBGE tinham `endpoint: "ibge_choropleth"` que caía no `default: return null` — nenhum fetch.

**Correção:**
1. Adicionado `case "ibge_choropleth"` que monta URL `/geo/ibge/choropleth/{metric}/{ano}` (ano default por camada)
2. Adicionada função `interpolateColor()` com 14 paletas ColorBrewer-like (YlGn, YlOrBr, Reds, etc — 5 stops cada)
3. Campos `defaultYear` e `colorScheme` adicionados ao `LayerConfig`; 16 camadas IBGE populadas com valores apropriados (2022 para PAM/PPM, 2021 para POP/PIB)
4. Estilo do GeoJSON calcula `vMin/vMax` dos `properties.value` e interpola cor proporcional

**Resultado:** 14 camadas choropleth renderizam município por município com gradiente. Primeira carga ~10-15s (~5570 polygons + merge SIDRA); re-visita instantânea (cache SHA256 24h).

### 1.7 Sprint 2c — Valuation, Logística, Crédito + MapPreview 🟢

3 novas abas implementadas (ficha → 10/12 abas):

8. **Valuation** — NBR 14.653-3 nível expedito. Endpoint `/property/{car}/valuation` calcula:
   - Preço base por UF (heurística 2025: MT R$40k/ha, MA R$13k/ha, SP R$55k/ha, ...)
   - Valor base = área × preço_UF
   - Descontos: TI −100% (ilíquido), UC −50%, embargo ICMBio −40%
   - Disclaimer NBR exigindo avaliador credenciado para nível II/III
9. **Logística** — endpoint `/property/{car}/neighbors` com PostGIS KNN (`ST_DistanceSphere`) retorna top 5 armazéns CONAB, frigoríficos SIF, portos ANTAQ + distância mínima rodovia federal DNIT e ferrovia ANTT.
10. **Crédito** — endpoint `/property/{car}/credit` busca contratos em `mapbiomas_credito_rural` (5.6M) que intersectam o CAR, agrupa por ano, top 20 contratos com IF e valor em BRL.

Novo componente **MapPreview** no header da ficha — mini-mapa leaflet (dynamic import) mostrando o polígono do CAR com estilo pontilhado verde sobre basemap dark.

### 1.8 Sprint 2d — Fix choropleth + toolbar interativa do mapa 🟢

**Feedback do Eduardo:** "carregou a quantidade de rebanho bovino dos municipios, mas pintou quase tudo da mesma cor. Falta opção para desenhar polígono, mandar arquivo com memorial descritivo, clicar no mapa e pedir informações sobre aquela localização."

**4 correções/features implementadas:**

#### a) Choropleth: escala linear → quintis (quantile breaks)

Problema: distribuições agrícolas são log-normais. Um Corumbá/MS com 2M cabeças vs Açailândia/MA com 400k → escala linear pintava 99% dos municípios no primeiro bucket (claro).

Solução em `MapComponent.tsx → ActiveLayer`:
```ts
const sorted = values.sort((a,b) => a-b);
breaks = [20%, 40%, 60%, 80%];  // 4 cortes = 5 buckets
bucket = count(v > break);       // bucket 0..4
```

Resultado: top 20% municípios = cor escura, próximos 20% = média-escura, ..., bottom 20% = cor clara. Diferenciação visual forte.

#### b) Click no mapa → análise de ponto (estilo Registro Rural)

- Botão 🎯 no toolbar canto superior direito
- Quando ativo, click em qualquer ponto do mapa chama `/geo/analyze-point?lat=&lon=&radius_km=5`
- Retorna município (IBGE reverse geocode), TIs próximas (FUNAI), DETER alerts (INPE), clima (NASA POWER), jurisdição/reserva legal
- Drawer inferior esquerdo mostra tudo com risk level e flags

#### c) Desenhar polígono (AOI customizada)

- Botão ✏️ no toolbar
- Click adiciona vértices (≥3 para fechar)
- Banner superior mostra contagem + botões "Fechar" / "Cancelar"
- Ao fechar, envia GeoJSON para `POST /geo/aoi/analyze`
- Endpoint retorna: área em ha (via `ST_Area` + `ST_Transform 3857`), centróide, overlaps em 9 camadas (TI, UC, embargo ICMBio, PRODES, DETER AM/CE, MapBiomas, SIGEF, autos IBAMA), score 0-100, risk level
- Polígono fica plotado permanentemente no mapa com cor laranja pontilhada

#### d) Upload de GeoJSON/KML

- Botão 📤 no toolbar
- Aceita `.geojson`, `.json`, `.kml`, `.gml`
- Parser built-in em `MapTools.tsx`:
  - GeoJSON: lê Feature/FeatureCollection/geometry, extrai Polygon/MultiPolygon
  - KML: DOMParser XML, percorre `<Placemark><Polygon>` e `<coordinates>`
- Plota todos os polígonos encontrados + analisa o primeiro automaticamente

### 1.9 Commits

Branch: `claude/continue-backend-dev-sVLGG` — 8 commits na sessão:
- **324b3f6** — Sprint 1 completo (Embrapa + IBGE choropleth + MapBiomas + IBAMA script)
- **2d6bd06** — Sprint 2a (ficha com 4 abas + IBAMA 16k autos)
- **df70f47** — Sprint 2b (Compliance + Clima + Jurídico = 7 abas)
- **2732e38** — OmniSearch CAR routing + handoff update
- **bd0815f** — Fix render choropleth + docs consolidadas
- **d3f2dcf** — Sprint 2c (Valuation + Logística + Crédito + MapPreview = 10 abas)
- **(próximo)** — Sprint 2d (quintis + toolbar point/draw/upload + AOI endpoint)
- **(próximo)** — CHANGELOG + docs consolidados sessão 7 fechada

Arquivos novos na sessão 7:
- 2 coletores novos (embrapa rewrite + mapbiomas_alerta)
- 4 routers backend (embrapa, ibge_choropleth, mapbiomas) + 3 endpoints novos em property.py + 1 endpoint novo em geo.py (aoi/analyze)
- 1 script ETL (download_ibama_autos)
- 1 rota frontend `/imoveis/[car]`
- 12 componentes imovel (PropertyHeader, TabNav, MapPreview, 10 Tabs)
- 1 componente MapTools (toolbar + parser KML/GeoJSON + drawer análise)
- 14 camadas catálogo ativadas + 14 paletas choropleth
- 1 nova camada PostGIS: autos_ibama (18ª)
- 1 tabela nova: geo_autos_ibama (16.121 linhas)

---

## 2. ESTADO REAL DO PRODUTO (HOJE)

### Backend — FastAPI + PostGIS

✅ **Funcionando (validado via curl):**
- `/health`
- 17 camadas PostGIS via `/api/v1/geo/postgis/{layer}/geojson`
- DJEN 42 publicações — `/api/v1/publicacoes/*`
- DataJud CNJ — `/api/v1/lawsuits/*`
- **NOVO Embrapa**: 27 endpoints REST em `/api/v1/embrapa/*` (7 APIs reais)
- **NOVO IBGE choropleth**: `/api/v1/geo/ibge/choropleth/*` (16 métricas)
- **NOVO MapBiomas Alerta**: `/api/v1/mapbiomas/*` (auth JWT + alerts tempo real)
- Mercado: 11 endpoints CEPEA/BCB
- Dashboard, property, search, etc.

⚠ **Configurado mas não carregado:**
- Portal Transparência CKAN (token .env)
- dados.gov.br CKAN (token .env)
- BCB SICOR OData
- Earth Engine

❌ **Pendente:**
- Coletor Portal Transparência (CEIS/CNEP/Garantia-Safra)
- Coletor 32 datasets dados.gov.br (guia escrito, código zero)
- STJ dados abertos
- Base jurisprudência + bge-m3 embeddings

### Frontend — Next.js 16.2.3

✅ **Build limpo** (`npm run build` → 10 rotas estáticas geradas em 3.3s)

✅ **Funcionais:** /login, /, /mapa (v2), /mercado, /processos, /publicacoes
⚠ **Mocks:** /consulta, /compliance, /alertas
❌ **Não existem:** /imoveis/[car], /valuation, /portfolio, /leiloes, /teses, /minutas, /perfil, /radar-ibama

### Dados no PostgreSQL (inalterado desde sessão 6)

| Tabela | Registros |
|---|---|
| mapbiomas_credito_rural | 5.614.207 |
| sigef_parcelas | 1.717.474 |
| geo_mapbiomas_alertas | 515.823 |
| sicar_completo (MA) | 352.215 |
| publicacoes_djen | 42 (Eduardo OAB/MA 12147) |
| ...e outras | (ver sessão 6) |

---

## 3. PENDÊNCIAS CRÍTICAS RESTANTES (das 10 da sessão 6)

| # | Pendência | Status sessão 7 |
|---|---|---|
| 1 | Paths Embrapa | ✅ **RESOLVIDO** (7/9 APIs ativas) |
| 2 | Coletores dados.gov.br | ❌ ainda só guia |
| 3 | Motor jurídico (prescrição, teses, minuta) | ❌ zero |
| 4 | Base jurisprudência STJ + bge-m3 | ❌ zero |
| 5 | Ficha do imóvel `/imoveis/[car]` | ✅ **PARCIAL** (7/12 abas) |
| 6 | Tela `/valuation` NBR 14.653-3 | ❌ |
| 7 | Agregador de leilões | ❌ |
| 8 | MCR 2.9 expandido (6→30) | ⚠ parcial — 6 checks do /compliance/mcr29 ainda (embora o endpoint seja POST real e use 5 fontes: FUNAI, ICMBio, IBAMA, INPE, MTE). Expandir para 30 é próximo sprint. |
| 9 | `/compliance` real | ✅ **RESOLVIDO NA FICHA** — aba Compliance consome endpoint real. Tela `/compliance` standalone ainda é mock. |
| 10 | `/alertas` real | ❌ ainda mock |

**Ativados esta sessão:**
- ✅ 14 camadas do catálogo (PAM soja/milho/cana/café/algodão/arroz/feijão/trigo + área/valor soja + PPM bovinos/suínos/ovinos/bubalinos + pop/PIB total/PIB per capita)
- ✅ 27 endpoints REST Embrapa para perícia/compliance
- ✅ MapBiomas Alerta em tempo real por CAR

---

## 4. CREDENCIAIS (inalterado desde sessão 6 — em backend/.env)

```bash
GCP_PROJECT_ID=agrojus
GCP_PROJECT_NUMBER=1064767214292
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
MAPBIOMAS_PASSWORD=1qasw23edFR$
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
EMBRAPA_CONSUMER_SECRET=eDJph7PEE9xKDor739rgXwcUc0ca
EMBRAPA_ACCESS_TOKEN=2aef1f08-a5e9-3480-b68b-2184057e3a6d  # opcional — collector regenera
DADOS_GOV_TOKEN=eyJhbGc...
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
```

---

## 5. COMANDOS RÁPIDOS

```bash
# Subir ambiente
cd C:\dev\agrojus-workspace\agrojus
docker compose up -d

# Health + Embrapa
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/embrapa/status
curl "http://localhost:8000/api/v1/embrapa/agritec/culturas" | head -c 200
curl "http://localhost:8000/api/v1/embrapa/agrofit/produtos?cultura=Soja&praga=Ferrugem"

# IBGE Choropleth
curl "http://localhost:8000/api/v1/geo/ibge/choropleth/metrics"
curl "http://localhost:8000/api/v1/geo/ibge/choropleth/pam_soja/2022?uf=MT" -o pam_soja_mt.json
curl "http://localhost:8000/api/v1/geo/ibge/choropleth/populacao/2021?uf=MA"

# MapBiomas
curl "http://localhost:8000/api/v1/mapbiomas/status"
curl "http://localhost:8000/api/v1/mapbiomas/alerts?start=2025-12-01&end=2025-12-31&limit=5"
curl "http://localhost:8000/api/v1/mapbiomas/property/<CAR_CODE>"

# IBAMA (executar quando tiver tempo — 2-3 min)
docker compose exec backend python scripts/download_ibama_autos.py

# Frontend
cd frontend_v2 && npm run dev
# http://localhost:3000
```

---

## 6. ESTRUTURA DE ARQUIVOS NOVOS / MODIFICADOS

```
backend/app/
├── api/
│   ├── embrapa.py              (REESCRITO sessão 7 — 27 endpoints)
│   ├── ibge_choropleth.py      (NOVO sessão 7)
│   ├── mapbiomas.py            (NOVO sessão 7)
│   ├── geo_layers.py           (sessão 6)
│   └── publicacoes.py          (sessão 6)
├── collectors/
│   ├── embrapa.py              (REESCRITO sessão 7 — paths reais)
│   ├── mapbiomas_alerta.py     (NOVO sessão 7)
│   └── djen.py                 (sessão 6)
└── main.py                     (+ 2 routers)

backend/scripts/
└── download_ibama_autos.py     (NOVO sessão 7)

frontend_v2/src/lib/
└── layers-catalog.ts           (14 camadas saíram de stub)

docs/
├── HANDOFF_2026-04-17_sessao7.md  (ESTE ARQUIVO)
├── HANDOFF_2026-04-17_sessao6.md  (anterior)
└── research/                   (inalterado)
```

---

## 7. ROADMAP PRÓXIMA SESSÃO (Sprint 2+)

### Sprint 2 (5 dias) — Ficha do imóvel `/imoveis/[car]`
**Tela mais importante do produto, ainda não existe.** Blueprint completo em `docs/research/analise-agronomica-integrada.md` com 15 perguntas-chave e mapeamento fonte→endpoint. 12 abas:

**Sprint 2a (3 dias):** scaffold rota + 6 abas primeiras
1. Visão Geral (resumo KPIs)
2. Compliance (MCR + EUDR)
3. Dossiê Ambiental (UC, TI, embargos, desmatamento cruzado)
4. Histórico MapBiomas (timeline 40 anos)
5. Produção Agrícola (SIDRA + **Agritec zoneamento**)
6. Clima (NASA POWER + estações INMET)

**Sprint 2b (2 dias):** 6 abas restantes
7. Valuation (NBR 14.653-3)
8. Logística (armazéns/frigos/portos mais próximos)
9. Jurídico (DataJud + DJEN + protestos)
10. Crédito Rural (SICOR + MapBiomas)
11. Monitoramento (webhooks + alertas)
12. Ações (gerar laudo PDF, minuta, etc.)

### Sprint 3 (5 dias) — Compliance MCR 2.9 expandido
De 6 para 30 critérios auditáveis + 4 EUDR. Usar dados já disponíveis:
- Fundiário: SICAR + SIGEF + CAR × SIGMINE
- Ambiental: embargos IBAMA + UC + TI + PRODES + DETER
- Trabalhista: MTE lista suja (já no banco)
- Jurídico: DataJud + DJEN + protestos
- Financeiro: SICOR + CEIS/CNEP (Portal Transparência)

### Sprint 4 (4 dias) — Coletores dados.gov.br
Guia pronto em `docs/research/dados-gov-guia.md`. 32 datasets priorizados:
- IBAMA autos/embargos/CTF
- Garantia-Safra (semiárido)
- SIGMINE (mineração)
- ANA outorgas + BHO
- Assentamentos INCRA, Quilombolas
- ANEEL usinas + LTs

### Sprint 5 (4 dias) — Mapa v3 (padrões SYNTHESIS)
- URL state serializado
- Drill-down UF → Município
- Slider temporal duplo
- Legenda dinâmica "Ver só esta"
- Tabs laterais
- Opacidade por camada

### Sprint 6 (5 dias) — Motor jurídico base
- STJ dados abertos + TCU webservice → base `jurisprudencia`
- Embedding bge-m3 (modelo em mia-project)
- Busca híbrida vetorial + textual
- `/teses` com citações verificáveis

### Sprint 7 (7 dias) — Gerador de minutas
- Claude API integration
- Verificação anti-alucinação contra base
- `/minutas` + export DOCX

### Sprint 8 (10 dias) — Agregador de leilões
- Scrapers (Caixa, Spy, Portal Leilão, TJs)
- Parser LLM edital
- Timeline do lote + alertas

**Total: ~40 dias para produto demonstrável end-to-end.**

---

## 8. REGRAS INVIOLÁVEIS (sessão 7 adiciona)

1-10. Ver sessão 6 (inalterado)

11. **Sempre validar paths de API via Swagger + curl antes de escrever collector** — 7 paths Embrapa estavam inventados; perdi 2h debugando
12. **SIDRA usa `/f/u`, não `/f/n`** — bug sutil, `/n` retorna só nomes sem códigos IBGE
13. **MapBiomas auth = GraphQL mutation signIn, NÃO REST `/auth/login`** — o REST é deprecated
14. **Antes de commitar frontend, sempre `npm run build`** — TypeScript vai pegar `LayerEndpoint` faltando

---

## 9. ARMADILHAS NOVAS (sessão 7)

- **Introspect GraphQL sempre** — schemas mudam (MapBiomas tinha `detectedAt` em AlertData mas `coordenates.latitude` não `coordenates.lat`)
- **SIDRA `/f/n` vs `/f/u`** — bug que levou 1h
- **Embrapa WSO2 retorna HTTP 400 "dados-invalidos"** quando params errados (válido = auth OK, não está quebrado)
- **SmartSolos base path = `/smartsolos/expert/v1`** (não `/smartsolos/v1` — específico desta API)
- **MapBiomas JWT duração real ~2 anos** (mas cache 24h por segurança)

---

## 10. META-META

Eduardo deu **autonomia total** nesta sessão: "nao entendi pq precisa de mim... nao ja te dei autorizacao pra tudo? usa o navegador, acessa, faz o download, prossiga... faz tudo que puder".

**Próximas sessões devem manter esse padrão:**
- Nunca pedir o que pode ser feito via WebFetch / tavily / curl / docker / grep
- Introspectar schemas/APIs antes de escrever código que depende deles
- Validar cada passo via curl antes de marcar como feito
- Commitar em blocos lógicos + atualizar HANDOFF no fim

---

*AgroJus — Handoff Sessão 7 — 2026-04-17 BRT*
*Sprint 1 completo: Embrapa + IBGE choropleth + IBAMA (script) + MapBiomas tempo real*
