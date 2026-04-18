# AgroJus API — Contrato para Frontend

> Base URL: `http://localhost:8000`
> Swagger UI: `http://localhost:8000/docs`
> Versao: 0.9.1 (2026-04-15)

---

## 1. Busca de Imoveis

### GET `/api/v1/property/search`

Busca paginada de imoveis rurais. Ideal para autocomplete e listagem.

| Param | Tipo | Descricao |
|---|---|---|
| `q` | string | Texto livre (CAR code, municipio) |
| `uf` | string | Sigla do estado (MA, PA, MT...) |
| `municipio` | string | Nome do municipio (busca parcial) |
| `status` | string | Status CAR: AT, PE, CA, SU |
| `area_min` | float | Area minima em hectares |
| `area_max` | float | Area maxima em hectares |
| `page` | int | Pagina (default 1) |
| `page_size` | int | Itens por pagina (default 20, max 100) |

**Response:**
```json
{
  "total": 5000,
  "page": 1,
  "page_size": 20,
  "pages": 250,
  "results": [
    {
      "car_code": "MA-2102101-XXXX",
      "municipio": "Brejo",
      "uf": "MA",
      "area_ha": 80.36,
      "status": "AT",
      "tipo": "IRU",
      "modulos_fiscais": 1.148,
      "cod_municipio_ibge": 2102101,
      "centroid": { "lat": -3.698, "lon": -42.734 }
    }
  ]
}
```

### GET `/api/v1/property/ufs`

Lista UFs com contagem de CARs.

### GET `/api/v1/property/municipios?uf=MA`

Lista municipios de uma UF com contagem de CARs.

---

## 2. Relatorio Due Diligence (Motor Principal)

### POST `/api/v1/report/due-diligence`

Relatorio completo com cruzamento PostGIS + compliance.

**Request:**
```json
{
  "car_code": "AC-1200435-XXXX",
  "cpf_cnpj": "12345678000190",
  "owner_name": "Joao Silva"
}
```

Pelo menos `car_code` OU `cpf_cnpj` deve ser fornecido. `car_code` ativa o motor PostGIS (13 camadas espaciais). `cpf_cnpj` ativa consultas externas (DataJud, Lista Suja, Receita).

**Response (campos principais):**
```json
{
  "report_id": "uuid",
  "generated_at": "2026-04-15T11:04:00Z",
  "persona": null,
  
  "property_info": {
    "car_code": "AC-1200435-XXXX",
    "status": "AT",
    "area_total_ha": 100.1,
    "municipality": "Santa Rosa do Purus",
    "state": "AC",
    "geometry_wkt": "{GeoJSON string}"
  },
  
  "overlap_analysis": {
    "overlaps_indigenous_land": false,
    "overlaps_conservation_unit": false,
    "overlaps_embargo": false,
    "overlaps_deforestation": true,
    "deforestation_area_ha": 32.73
  },
  
  "risk_score": {
    "overall": "medium",
    "land_tenure": "low",
    "environmental": "medium",
    "legal": "low",
    "labor": "low",
    "financial": "low",
    "details": ["6 alerta(s) de desmatamento", "MCR 2.9: APROVADO", ...]
  },
  
  "compliance": {
    "mcr_29": {
      "passed": true,
      "score": 100,
      "items": [
        {
          "code": "MCR-01",
          "description": "CAR ativo e regular",
          "passed": true,
          "details": "Status: AT",
          "weight": 2.0
        }
      ]
    },
    "eudr": {
      "passed": false,
      "score": 63,
      "items": [...]
    },
    "overall_score": 817,
    "risk_level": "BAIXO",
    "summary": "Elegivel para credito rural (MCR 2.9). Nao conforme EUDR (EUDR-01)."
  },
  
  "spatial_analysis": {
    "property": { "car_code": "...", "municipio": "...", "uf": "...", "area_ha": 100.1 },
    "terras_indigenas": [],
    "unidades_conservacao": [],
    "embargos": [],
    "desmatamento": {
      "prodes": [],
      "deter": [{ "classe": "DESMATAMENTO_CR", "data": "2025-01-15", "overlap_ha": 3.83 }],
      "mapbiomas": [{ "ano": 2025, "bioma": "Amazonia", "overlap_ha": 7.73 }]
    },
    "autos_icmbio": [],
    "credito_rural": [],
    "infraestrutura": {
      "armazens": [],
      "frigorificos": [],
      "rodovias": [],
      "portos": []
    },
    "flags": {
      "prodes_pos_2019": false,
      "prodes_pos_2020": false,
      "embargo_ativo": false,
      "terra_indigena": false,
      "uc_protecao_integral": false
    },
    "metadata": {
      "layers_checked": 13,
      "layers_with_hits": 2,
      "query_time_ms": 786.3,
      "errors": []
    }
  },
  
  "ibama_embargos": [],
  "slave_labour": [],
  "lawsuits": [],
  "owner_info": null,
  "financial_summary": null,
  "sources_consulted": ["PostGIS local (13 camadas, 786ms)", "Compliance: 817/1000 (BAIXO)"]
}
```

### POST `/api/v1/report/due-diligence/pdf`

Mesmo request, retorna PDF binario.
Header: `Content-Type: application/pdf`

### POST `/api/v1/report/buyer`
### POST `/api/v1/report/lawyer`
### POST `/api/v1/report/investor`

Atalhos com persona pre-definida. Mesmo request/response.

---

## 3. GeoJSON para Mapa (Leaflet)

### GET `/api/v1/property/{car_code}/geojson`

Retorna FeatureCollection com o poligono do imovel.
Usar para: `L.geoJSON(data).addTo(map)` e `map.fitBounds(layer.getBounds())`

```json
{
  "type": "FeatureCollection",
  "features": [{
    "type": "Feature",
    "id": "MA-2102101-XXXX",
    "properties": {
      "car_code": "MA-2102101-XXXX",
      "municipio": "Brejo",
      "uf": "MA",
      "area_ha": 7.12,
      "status": "AT",
      "layer": "imovel"
    },
    "geometry": { "type": "MultiPolygon", "coordinates": [...] }
  }]
}
```

### GET `/api/v1/property/{car_code}/overlaps/geojson`

Retorna FeatureCollection com TODAS as camadas sobrepostas.
Cada feature tem `properties.layer` e `properties.color` para estilizar no mapa.

```json
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "properties": {
        "layer": "deter_amazonia",
        "color": "#FF4500",
        "classe": "DESMATAMENTO_CR",
        "data": "2025-01-15"
      },
      "geometry": { "type": "Polygon", "coordinates": [...] }
    },
    {
      "type": "Feature",
      "properties": {
        "layer": "mapbiomas_alerta",
        "color": "#CC00CC",
        "bioma": "Amazonia",
        "ano": 2025
      },
      "geometry": { "type": "Polygon", "coordinates": [...] }
    }
  ],
  "metadata": {
    "car_code": "AC-1200435-XXXX",
    "total_features": 6,
    "layers_found": ["deter_amazonia", "mapbiomas_alertas"],
    "layers_checked": ["terras_indigenas", "unidades_conservacao", "embargos_icmbio", "prodes", "deter_amazonia", "deter_cerrado", "mapbiomas_alertas"]
  }
}
```

**Cores por camada (sugestao):**

| Layer | Cor | Hex |
|---|---|---|
| imovel (principal) | Azul | #3388ff |
| terra_indigena | Vermelho | #FF0000 |
| unidade_conservacao | Verde | #00AA00 |
| embargo_icmbio | Laranja | #FF6600 |
| prodes | Vinho | #8B0000 |
| deter_amazonia | Laranja-vermelho | #FF4500 |
| deter_cerrado | Laranja-escuro | #FF8C00 |
| mapbiomas_alerta | Roxo | #CC00CC |

---

## 4. Dashboard

### GET `/api/v1/dashboard/metrics`

KPIs agregados do banco.

```json
{
  "generated_at": "2026-04-15T...",
  "db_latency_ms": 1699.9,
  "kpis": {
    "cars_imoveis": { "total": 135000, "ufs": 27 },
    "desmatamento": {
      "deter_amazonia": 50000,
      "deter_cerrado": 50000,
      "prodes": 50000,
      "mapbiomas_alertas": 515823,
      "total": 665823
    },
    "areas_protegidas": { "terras_indigenas": 655, "unidades_conservacao": 346, "total": 1001 },
    "icmbio": { "embargos": 5000, "autos": 10000, "total": 15000 },
    "ibama_embargos": { "total": 104284, "last_30d": 0 },
    "credito_rural": { "total": 5614207 },
    "infraestrutura": { "armazens": 16676, "frigorificos": 207, "rodovias": 14255, "portos": 35 },
    ...
  }
}
```

---

## 5. Consulta Unificada (por CPF/CNPJ)

### POST `/api/v1/consulta/completa`

Dossie completo de uma pessoa. Agrega TODAS as fontes em paralelo.

```json
{
  "cpf_cnpj": "12345678000190",
  "include_cadastral": true,
  "include_environmental": true,
  "include_labour": true,
  "include_legal": true,
  "include_financial": true,
  "include_protests": true
}
```

---

## 6. Geo (Mapa Geral)

### GET `/api/v1/geo/analyze-point?lat=-3.6&lon=-42.7&radius_km=5`

Analise de ponto no mapa. Retorna TIs, DETER, municipio, clima, jurisdicao.

### GET `/api/v1/geo/layers/{layer_id}/geojson`

Camadas WFS para o mapa. IDs: `terras_indigenas`, `desmatamento`, `desmatamento_cerrado`, `municipios`, `parcelas_financiamento`, `embargos`.

### GET `/api/v1/geo/catalogo`

Catalogo de todas as camadas disponiveis.

---

## 7. Outros Endpoints Uteis

| Endpoint | Metodo | Descricao |
|---|---|---|
| `/api/v1/search/smart` | POST | Busca inteligente por texto natural |
| `/api/v1/market/quotes` | GET | Cotacoes de commodities |
| `/api/v1/lawsuits/search` | POST | Busca de processos judiciais |
| `/api/v1/compliance/mcr29/check` | POST | Check MCR 2.9 rapido |
| `/api/v1/geo/municipios/busca?nome=...` | GET | Busca municipios IBGE |
| `/api/v1/geo/municipios/{cod}/producao` | GET | Producao agricola PAM |
| `/api/v1/geo/municipios/{cod}/pecuaria` | GET | Pecuaria PPM |
| `/api/v1/geo/clima?lat=&lon=` | GET | Dados climaticos NASA POWER |

---

## Fluxo Tipico do Frontend

```
1. Usuario abre app
   → GET /api/v1/dashboard/metrics (KPIs para cards)

2. Usuario busca imovel
   → GET /api/v1/property/search?q=MA-210 (autocomplete)
   → GET /api/v1/property/search?uf=MA&municipio=Brejo (filtros)

3. Usuario seleciona imovel
   → GET /api/v1/property/{car}/geojson (renderizar poligono no mapa)
   → GET /api/v1/property/{car}/overlaps/geojson (renderizar sobreposicoes)
   → POST /api/v1/report/due-diligence (relatorio completo)

4. Usuario quer PDF
   → POST /api/v1/report/due-diligence/pdf (download binario)

5. Usuario consulta pessoa
   → POST /api/v1/consulta/completa (dossie CPF/CNPJ)
```

---

## Compliance Score — Como Interpretar

| Score | Nivel | Significado |
|---|---|---|
| 800-1000 | BAIXO | Imovel com poucos ou nenhum alerta |
| 600-799 | MEDIO | Alertas menores, elegivel com ressalvas |
| 300-599 | ALTO | Problemas serios, investigacao necessaria |
| 0-299 | CRITICO | Multiplos problemas graves |

**MCR 2.9** (Credito Rural): `passed: true` = elegivel para financiamento
**EUDR** (EU Deforestation): `passed: true` = conforme para exportacao UE

---

## 8. Enriquecimentos Opcionais (lentos)

### Earth Engine (include_satellite: true)

Adiciona ~20s. Retorna uso do solo (LULC), historico de fogo, dados de solo e agua.

```json
POST /api/v1/report/due-diligence
{
  "car_code": "MA-...",
  "include_satellite": true
}
```

Campo `satellite_data` no response:
```json
{
  "available": true,
  "year": 2023,
  "lulc": { "Pastagem": 45.2, "Formacao Florestal": 30.1, "Agricultura": 20.5 },
  "fire_history": [
    { "ano": 2023, "area_queimada_ha": 0 },
    { "ano": 2022, "area_queimada_ha": 5.3 }
  ],
  "soil": { "carbono_organico_kg_m2": 3.2, "argila_pct": 28.5, "areia_pct": 45.1, "silte_pct": 26.4 },
  "water": { "area_agua_ha": 1.2 },
  "query_time_ms": 18500
}
```

### MapBiomas Alerta GraphQL (include_realtime_alerts: true)

Adiciona ~3s. Consulta alertas em tempo real com imagens antes/depois.

```json
POST /api/v1/report/due-diligence
{
  "car_code": "MA-...",
  "include_realtime_alerts": true
}
```

Campo `mapbiomas_realtime` no response:
```json
{
  "available": true,
  "total_count": 3,
  "alerts": [
    {
      "alert_code": 12345,
      "area_ha": 2.5,
      "detected_at": "2025-08-15",
      "source": "SAD",
      "biome": "Amazonia",
      "status": "Publicado",
      "images": {
        "before": { "url": "...", "date": "2025-06-01" },
        "after": { "url": "...", "date": "2025-08-15" }
      }
    }
  ],
  "query_time_ms": 2800
}
```

---

## 9. Dashboard Refresh

### POST `/api/v1/dashboard/refresh`

Atualiza a materialized view do dashboard. Chamar periodicamente (ex: a cada 1h).

---

## Notas Tecnicas

- **CORS**: Liberado para todas as origens (`*`)
- **Auth**: JWT via `/api/v1/auth/login` (opcional em dev)
- **Rate Limit**: 100 buscas/min, 20 relatorios/min
- **PostGIS**: 57+ tabelas, 10.2M+ registros, 13 camadas espaciais cruzadas
- **SICAR BigQuery**: 79.3M CARs com geometria (basedosdados.br_sfb_sicar)
- **Dashboard**: Materialized view, ~5ms (refresh via POST /dashboard/refresh)
- **Tempo de resposta**: ~250ms (report basico), ~3s (com GraphQL), ~20s (com satelite)
- **PDF**: ReportLab com compliance MCR/EUDR, ~6KB
- **ETL SICAR**: `scripts/etl_sicar_bigquery.py MA MT PA GO TO MS` para baixar mais UFs
