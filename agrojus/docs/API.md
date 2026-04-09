# API Reference — AgroJus Backend

Base URL: `http://localhost:8000/api/v1`

Swagger UI interativo: `http://localhost:8000/docs`

---

## Autenticação

MVP sem autenticação. Em produção: JWT Bearer token via header `Authorization`.

---

## 1. Busca (`/search`)

### POST `/search/property`
Busca universal de imóvel rural. Aceita qualquer identificador.

**Request Body:**
```json
{
  "car_code": "MA-2101400-5E53....",
  "matricula": "12345",
  "sncr_code": "123.456.789.012-1",
  "nirf": "1234567",
  "ccir": "1234567890",
  "itr_number": "12345678",
  "sigef_code": "abc-def-123",
  "latitude": -5.0892,
  "longitude": -42.8019,
  "municipality": "Teresina",
  "state": "PI",
  "cpf_cnpj": "12.345.678/0001-90",
  "owner_name": "Fazenda XYZ Ltda",
  "persona": "buyer"
}
```
Todos os campos são opcionais. Informe ao menos um.

**Response:**
```json
{
  "found": true,
  "identifiers_used": ["CAR", "CNPJ"],
  "data": {
    "car": { "car_code": "...", "area_total_ha": 500.0, "municipality": "...", "state": "..." },
    "owner": { "cnpj": "...", "razao_social": "...", "situacao_cadastral": "ATIVA" }
  },
  "pending_identifiers": [
    { "type": "matricula", "value": "12345", "status": "Consulta a cartorios em desenvolvimento" }
  ]
}
```

### GET `/search/cnpj/{cnpj}`
Consulta dados cadastrais de um CNPJ.

**Response:**
```json
{
  "source": "Receita Federal (BrasilAPI)",
  "data": {
    "cnpj": "12345678000190",
    "razao_social": "Fazenda XYZ Ltda",
    "nome_fantasia": "Fazenda XYZ",
    "situacao_cadastral": "ATIVA",
    "cnae_principal": "Cultivo de soja",
    "municipio": "Sorriso",
    "uf": "MT",
    "socios": [{ "nome": "João Silva", "qualificacao": "Sócio-Administrador" }]
  }
}
```

### GET `/search/validate/{document}`
Valida CPF ou CNPJ.

**Response:** `{ "type": "CNPJ", "valid": true, "document": "12345678000190" }`

---

## 2. Relatórios (`/report`)

### POST `/report/due-diligence`
Gera relatório completo de due diligence em JSON.

**Request Body:** Mesmo que `/search/property`.

**Response:**
```json
{
  "report_id": "uuid",
  "generated_at": "2026-04-09T12:00:00Z",
  "persona": "buyer",
  "property_info": { "car_code": "...", "area_total_ha": 500.0, ... },
  "sigef_info": { "parcel_code": "...", "certified": true, ... },
  "matricula_info": { "matricula_number": "...", "has_onus": false, ... },
  "sncr_info": { "sncr_code": "...", "nirf": "...", "classification": "Grande Propriedade" },
  "ccir_info": { "ccir_number": "...", "valid": true },
  "itr_info": { "nirf": "...", "vti": 5000000.0, "status_pagamento": "Em dia" },
  "owner_info": { "cnpj": "...", "razao_social": "...", ... },
  "ibama_embargos": [],
  "slave_labour": [],
  "overlap_analysis": {
    "overlaps_indigenous_land": false,
    "overlaps_conservation_unit": false,
    "overlaps_embargo": false,
    "overlaps_deforestation": false,
    "overlaps_quilombo": false,
    "overlaps_settlement": false
  },
  "financial_summary": {
    "rural_credits": [],
    "total_credit_amount": 0,
    "land_prices": [],
    "avg_land_price_per_ha": 25000.0
  },
  "risk_score": {
    "overall": "low",
    "land_tenure": "low",
    "environmental": "low",
    "legal": "low",
    "labor": "low",
    "financial": "low",
    "details": ["Nenhum alerta encontrado nas fontes consultadas"]
  },
  "sources_consulted": ["SICAR/CAR", "SIGEF/INCRA", "Receita Federal (CNPJ)", "IBAMA"]
}
```

### POST `/report/due-diligence/pdf`
Mesmo request. Retorna PDF (`application/pdf`).

### POST `/report/buyer`
Atalho para due diligence com `persona: "buyer"`.

### POST `/report/lawyer`
Atalho para due diligence com `persona: "lawyer"`.

### POST `/report/investor`
Atalho para due diligence com `persona: "investor"`.

### POST `/report/person`
Gera dossiê completo de pessoa (CPF/CNPJ).

**Request Body:**
```json
{
  "cpf_cnpj": "12.345.678/0001-90",
  "include_properties": true,
  "include_legal": true,
  "include_environmental": true,
  "include_labour": true,
  "include_news": true,
  "include_financial": true
}
```

**Response:**
```json
{
  "dossier_id": "uuid",
  "generated_at": "2026-04-09T12:00:00Z",
  "cpf_cnpj": "12345678000190",
  "person_type": "CNPJ",
  "owner_info": { ... },
  "properties": [],
  "properties_count": 0,
  "ibama_embargos": [],
  "slave_labour": [],
  "financial_summary": { ... },
  "news_mentions": [],
  "risk_score": { ... },
  "sources_consulted": [...]
}
```

### POST `/report/region`
Relatório de inteligência regional.

**Request Body:**
```json
{
  "municipality": "Sorriso",
  "state": "MT",
  "municipality_code": "5107925"
}
```

**Response:**
```json
{
  "report_id": "uuid",
  "municipality": "Sorriso",
  "state": "MT",
  "total_properties": 150,
  "total_area_ha": 450000.0,
  "ibama_embargos": [],
  "main_crops": [{ "name": "Soja", "value": "1500000", "unit": "Toneladas" }],
  "financial_summary": { ... },
  "quotes": [...],
  "news": [...]
}
```

---

## 3. Mapa (`/map`)

### GET `/map/layers`
Lista camadas disponíveis para o mapa interativo.

**Response:**
```json
{
  "layers": [
    { "id": "car", "name": "Cadastro Ambiental Rural (CAR)", "source": "SICAR", "type": "polygon" },
    { "id": "sigef", "name": "Parcelas Certificadas (SIGEF)", "source": "INCRA/SIGEF", "type": "polygon" },
    { "id": "embargos", "name": "Áreas Embargadas (IBAMA)", "source": "IBAMA", "type": "polygon" },
    { "id": "terras_indigenas", "name": "Terras Indígenas", "source": "FUNAI", "type": "polygon" },
    { "id": "unidades_conservacao", "name": "Unidades de Conservação", "source": "ICMBio", "type": "polygon" },
    { "id": "desmatamento", "name": "Alertas de Desmatamento", "source": "INPE/DETER", "type": "polygon" }
  ]
}
```

### GET `/map/geojson/car/{car_code}`
Retorna geometria GeoJSON de um imóvel CAR.

### GET `/map/geojson/sigef/{parcel_code}`
Retorna geometria GeoJSON de uma parcela SIGEF.

### GET `/map/search/bbox?west=&south=&east=&north=&layer=sigef`
Busca features dentro de um bounding box (para o mapa interativo).

---

## 4. Mercado (`/market`)

### GET `/market/quotes`
Cotações mais recentes de commodities agrícolas.

### GET `/market/production/{municipality_code}`
Produção agrícola por município (IBGE/SIDRA).

### GET `/market/harvest/{crop}`
Dados de safra (CONAB). Crops: `soja`, `milho`, `cafe`, `algodao`.

### GET `/market/credit/municipality/{municipality_code}?year=2025`
Crédito rural por município (SICOR/BCB).

### GET `/market/land-prices/{state}?municipality=Sorriso`
Preços de terra por estado/município.

### GET `/market/fiagro`
Fundos FIAGRO (CVM).

---

## 5. Notícias (`/news`)

### GET `/news/?limit=30`
Últimas notícias do agronegócio (curadoria de múltiplas fontes RSS).

### GET `/news/legal?limit=20`
Notícias com relevância jurídica (legislação, regulamentação, embargos).

### GET `/news/market?limit=20`
Notícias de mercado (cotações, safras, commodities).

---

## Enums

### RiskLevel
`"low"` | `"medium"` | `"high"` | `"critical"`

### PersonaType
`"buyer"` | `"lawyer"` | `"farmer"` | `"investor"`

---

## Códigos de Erro

| Código | Significado |
|--------|------------|
| 200 | Sucesso |
| 404 | Não encontrado |
| 422 | Erro de validação (campo inválido) |
| 500 | Erro interno |
