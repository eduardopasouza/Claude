# Teste Real de Acesso às Fontes de Dados — AgroJus

Data do teste: 2026-04-09 (2 rodadas)
Ambiente: servidor Linux, acesso direto à internet

---

## RESULTADOS CONSOLIDADOS

### ✅ FUNCIONA — Testado com dados reais

| # | Fonte | Teste Real | HTTP | Dados Obtidos |
|---|-------|-----------|------|---------------|
| 1 | **BrasilAPI (CNPJ)** | Banco do Brasil | 200, 0.19s | Sócios, CNAE, capital social, endereço. COMPLETO |
| 2 | **IBGE/SIDRA (PAM)** | Sorriso-MT, soja | 200 | Produção agrícola. **Variáveis: v/214, v/215, v/216** |
| 3 | **SICOR/BCB** | Crédito Sorriso 2024 | 200 | Milho R$602K, Bovinos R$7.5M. **Endpoint: CusteioMunicipioProduto, campo: codIbge** |
| 4 | **IBAMA Embargos ZIP** | Download | 206 | **URL nova**: /SIFISC/termo_embargo/...zip |
| 5 | **IBAMA Coordenadas** | Download CSV | 200 | LAT, LON, WKT (POINT). **Atualizado 2026-04-08!** |
| 6 | **IBAMA Autos Infração** | Download ZIP | 206 | Disponível: /SIFISC/auto_infracao/...zip |
| 7 | **FUNAI GeoServer WFS** | Terras Indígenas | 200, 2.4s | **655 TIs em tempo real!** GeoJSON com geometria. Campos: nome, etnia, UF, município, fase, área(ha) |
| 8 | **TST CNDT** | Portal | 200, 1.2s | Acessível para scraping por CPF/CNPJ |
| 9 | **ANA Dados Abertos** | Portal | 200 | Outorgas WebApp disponível |
| 10 | **ANM Geo Portal** | ArcGIS REST | 200 | No ar. Serviço "grade" exposto |
| 11 | **SPU Dados Abertos** | dados.gov.br | 200 | Imóveis da União disponíveis |
| 12 | **CONAB Portal** | Portal informações | 200 | Acessível |
| 13 | **TerraBrasilis (INPE)** | Portal | 200 | No ar. WMS lento (10s+) |
| 14 | **Portal Transparência** | Download page | 200 | Página de download acessível |
| 15 | **SIGEF Portal** | sigef.incra.gov.br | 200 | Portal no ar |

### ⚠️ PARCIAL — Requer ação adicional

| # | Fonte | Resultado | O que precisa |
|---|-------|-----------|--------------|
| 16 | **SICAR/CAR** | **503 em TUDO** | Fora do ar (instabilidade crônica). Cache agressivo + retry |
| 17 | **SIGEF WFS/WMS** | **404** | Endpoints /geoserver/ removidos/migrados. Investigar novo path |
| 18 | **DataJud/CNJ** | **401** | Requer chave API (cadastro gratuito em datajud-wiki.cnj.jus.br) |
| 19 | **MapBiomas GraphQL** | Schema público, dados **requerem token** | 100+ campos disponíveis. Solicitar token de acesso |
| 20 | **CEPEA** | **403 Cloudflare** | Domínio mudou → cepea.org.br + Cloudflare. Precisa Playwright |
| 21 | **ANM Cadastro Mineiro** | **Timeout 10s** | Lento. Testar com timeout maior |

### ❌ BLOQUEADO neste ambiente

| # | Fonte | HTTP | Alternativa |
|---|-------|------|-------------|
| 22 | **Portal Transparência API** | timeout | Chave API ou outra rede |
| 23 | **PGFN Devedores** | conn reset | CSVs via dados.gov.br |
| 24 | **CENPROT Protestos** | 403 | Playwright (tem captcha) |
| 25 | **ICMBio UCs** | 404 no path testado | Buscar URL atualizada |
| 26 | **ANA GeoServer SNIRH** | 403 | Outra rede |
| 27 | **MAPA dados.agricultura** | 403 | Outra rede |

---

## DESCOBERTAS CHAVE

### 1. FUNAI GeoServer WFS — 655 TIs em tempo real
```
URL: https://geoserver.funai.gov.br/geoserver/Funai/ows
     ?service=WFS&version=1.0.0&request=GetFeature
     &typeName=Funai:tis_poligonais&outputFormat=application/json
Autenticação: NENHUMA
Dados: 655 TIs com geometria GeoJSON
Campos: terrai_nome, etnia_nome, municipio_nome, uf_sigla,
        superficie_perimetro_ha, fase_ti, modalidade_ti
CRS: EPSG:4674 (SIRGAS 2000) — reprojetar para 4326
```
**Substitui importação manual de shapefile. Query em tempo real.**

### 2. MapBiomas Alerta GraphQL — 100+ campos
```
URL: https://plataforma.alerta.mapbiomas.org/api/graphql
Schema: PÚBLICO (introspecção livre)
Dados: REQUEREM TOKEN
Campos: alertCode, areaHa, geometryWkt, detectedAt, publishedAt,
        crossedIndigenousLands(Area), crossedConservationUnits(Area),
        crossedEmbargoes(Total), crossedQuilombos(Area),
        crossedSettlements(Area), crossedRuralProperties,
        ruralPropertiesTotal, deforestationClasses, sources...
```
**Se conseguir token: desmatamento + cruzamento com tudo numa fonte.**

### 3. CEPEA mudou domínio + Cloudflare
```
ANTES: www.cepea.esalq.usp.br → redireciona
AGORA: www.cepea.org.br → HTTP 403 (Cloudflare challenge)
SOLUÇÃO: Playwright (browser headless) em vez de httpx
```

### 4. IBAMA tem 3 CSVs separados (não 1)
```
Embargos: /SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip
Coordenadas: /SIFISC/termo_embargo/coordenadas/coordenadas.csv  ← TEM WKT!
Autos de Infração: /SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip
```

### 5. SICAR fora do ar, SIGEF WFS migrou
SICAR: 503 em todos endpoints. Problema crônico.
SIGEF: /geoserver/ retorna 404. Novo endpoint desconhecido.

---

## URLs CORRETAS CONFIRMADAS

```python
# FUNAI WFS (TIs) — FUNCIONA ✅
FUNAI_WFS = "https://geoserver.funai.gov.br/geoserver/Funai/ows"

# BrasilAPI CNPJ — FUNCIONA ✅
BRASILAPI_CNPJ = "https://brasilapi.com.br/api/cnpj/v1/{cnpj}"

# IBGE/SIDRA PAM — FUNCIONA ✅ (variáveis corrigidas)
SIDRA_PAM = "https://apisidra.ibge.gov.br/values/t/5457/n6/{codIbge}/v/214,215,216/p/last%201/c782/39,33,9,31/f/n"

# SICOR/BCB Crédito Rural — FUNCIONA ✅ (endpoint e campo corrigidos)
SICOR_CUSTEIO = "https://olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata/CusteioMunicipioProduto?$filter=AnoEmissao eq '{ano}' and codIbge eq '{codIbge}'&$format=json"

# IBAMA Embargos — FUNCIONA ✅ (URLs atualizadas)
IBAMA_EMBARGOS_ZIP = "https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo/termo_embargo_csv.zip"
IBAMA_COORDS_CSV = "https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/coordenadas/coordenadas.csv"
IBAMA_AUTOS_ZIP = "https://dadosabertos.ibama.gov.br/dados/SIFISC/auto_infracao/auto_infracao/auto_infracao_csv.zip"

# TST CNDT — FUNCIONA ✅ (scraping)
TST_CNDT = "https://cndt-certidao.tst.jus.br/"

# MapBiomas GraphQL — SCHEMA PÚBLICO, DADOS REQUEREM TOKEN ⚠️
MAPBIOMAS_GRAPHQL = "https://plataforma.alerta.mapbiomas.org/api/graphql"

# CEPEA — PRECISA PLAYWRIGHT ⚠️
CEPEA_SOJA = "https://www.cepea.org.br/br/indicador/soja.aspx"

# SICAR — FORA DO AR ❌
# SIGEF WFS — MIGROU ❌
```
