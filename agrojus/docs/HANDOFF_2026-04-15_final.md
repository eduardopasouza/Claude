# AgroJus — Handoff Final Sessao 15/04/2026

> Leia este arquivo primeiro na proxima sessao.
> Sessao de ~4 horas. Resultado: pesquisa competitiva completa + base de dados pronta.

---

## O QUE FOI FEITO NESTA SESSAO

### 1. Pesquisa Competitiva (53 sites)
- 7 lotes de pesquisa em paralelo via Tavily + Chrome
- Documentos produzidos:
  - `docs/ANALISE_COMPETITIVA_COMPLETA.md` — 53 sites analisados
  - `docs/INVENTARIO_FEATURES.md` — 336 features catalogadas
  - `docs/STATUS_FONTES_DADOS.md` — status de cada fonte de dados
  - `docs/coordination/BRIEFING_FRONTEND_2026-04-15.md` — orientacoes pro frontend

### 2. Carga de Dados (de 5.8M para 10.2M registros)

**Novas tabelas criadas (18):**

| Tabela | Registros | Fonte | Como |
|---|---|---|---|
| geo_mapbiomas_alertas | 515.823 | MapBiomas GCS | Shapefile 441MB download |
| geo_car | 135.000 | SICAR WFS | 27 estados, SSL fix |
| bigquery_pam_permanente | 1.052.486 | BigQuery | basedosdados.br_ibge_pam |
| bigquery_sicor_operacoes | 500.000 | BigQuery | basedosdados.br_bcb_sicor |
| bigquery_sicor_propriedades | 500.000 | BigQuery | br_bcb_sicor (tem id_car!) |
| bigquery_cnpj_agro | 500.000 | BigQuery | br_me_cnpj CNAE 01/02/03 |
| mapbiomas_legality | 493.032 | CSV Eduardo | alerta x embargo x fiscalizacao |
| bigquery_pam_temporaria | 183.579 | BigQuery | basedosdados.br_ibge_pam |
| bigquery_prodes_municipio | 156.864 | BigQuery | br_inpe_prodes |
| bigquery_ppm_rebanhos | 108.467 | BigQuery | br_ibge_ppm |
| bigquery_ppm_producao_animal | 50.682 | BigQuery | br_ibge_ppm |
| geo_prodes | 50.000 | INPE WFS | prodes-legal-amz |
| sicor_custeio_uf | 50.000 | BCB OData | SICOR custeio por UF 2013-2026 |
| geo_autos_icmbio | 10.000 | INDE WFS | ICMBio autos_infracao |
| geo_embargos_icmbio | 5.000 | INDE WFS | ICMBio embargos |
| bigquery_censo_municipio | 5.570 | BigQuery | br_ibge_censo_2022 |
| bigquery_geo_municipios | 5.570 | BigQuery | br_geobr_mapas |
| geo_unidades_conservacao | 346 | INDE WFS | ICMBio UCs federais |
| + 9 tabelas menores | ~12k | BigQuery | UFs, biomas, TIs, UCs, censo |

### 3. APIs Conectadas e Configuradas

| API | Status | Config |
|---|---|---|
| **Google Earth Engine** | Autenticado | LULC Col.10 (52 assets), Agua Col.4, Fogo Col.4, Solo Col.2 |
| **MapBiomas Alerta GraphQL** | Token funcional | signIn com eduardo@guerreiro.adv.br |
| **BigQuery BasedosDados** | Autenticado | Project: agrojus, ADC credentials montado |
| **DataJud/CNJ** | API key configurada | Key publica em config.py |
| **agrobr** | Instalado | 38 fontes (CEPEA, B3, CONAB, IBGE, NASA) |

### 4. Scripts Criados

| Script | Funcao |
|---|---|
| `scripts/etl_sicar_nacional.py` | Carrega CAR 27 UFs (SSL fix) |
| `scripts/etl_icmbio_ucs.py` | UCs via INDE WFS (layer corrigido) |
| `scripts/etl_prodes.py` | PRODES via TerraBrasilis (layer corrigido) |
| `scripts/etl_anm_sigmine.py` | ANM mineracao (paginacao com problemas) |
| `scripts/etl_mte_lista_suja_csv.py` | MTE CSV (portais instáveis) |
| `scripts/etl_earth_engine.py` | **Funcoes EE por propriedade** (LULC, fogo, solo, agua) |

### 5. Arquivos Modificados

| Arquivo | Mudanca |
|---|---|
| `backend/requirements.txt` | +agrobr, basedosdados, google-cloud-bigquery, earthengine-api |
| `backend/app/config.py` | +datajud_api_key (publica), +gcp_project_id, +mapbiomas_email/password |
| `backend/app/collectors/camadas.py` | +car, +ucs, +embargos_icmbio, +autos_icmbio, +prodes (URLs corretas) |
| `docker-compose.yml` | +GCP_PROJECT_ID, +GOOGLE_APPLICATION_CREDENTIALS volume |
| `backend/.env` | Criado (MAPBIOMAS_EMAIL/PASSWORD, GCP_PROJECT_ID) |

---

## BANCO DE DADOS — ESTADO ATUAL

**42 tabelas com dados | 10.205.404 registros no PostGIS**

Alem disso:
- BigQuery: 7B+ linhas acessiveis (CNPJ, PAM completo, SICOR completo, censo)
- Earth Engine: 52+ assets MapBiomas acessiveis (LULC, agua, fogo, solo) — sob demanda por propriedade
- MapBiomas Alerta: 515k alertas via GraphQL (query por CAR funciona)
- DataJud: 88 tribunais via Elasticsearch
- agrobr: 38 fontes (CEPEA, B3, CONAB) em tempo real

---

## O QUE NAO FUNCIONA / PENDENCIAS

| Item | Problema | Acao |
|---|---|---|
| ANM/SIGMINE | Paginacao com geometria falha | Tentar download KMZ por estado |
| Quilombolas INCRA | Login gov.br obrigatorio | Eduardo baixar manualmente |
| MTE Lista Suja CSV | Portal Transparencia retorna 500 | Manter parser PDF (614 registros OK) |
| CONAB | Sem API publica | Scraping Pentaho ou agrobr |
| Earth Engine bulk | Timeout em queries Brasil inteiro | Usar sob demanda por propriedade (OK) |
| SICOR BigQuery | Puxamos 500k operacoes (de 28M total) | Ampliar se necessario |
| Dependencias pip | Perdem-se ao rebuildar container | Rebuildar imagem com `docker compose build` |

---

## PROXIMA SESSAO — FASE 2: MOTOR DE RELATORIO

O objetivo e construir o endpoint que transforma dados em produto:

```
POST /api/v1/imovel/relatorio
Body: { "tipo": "car", "codigo": "MA-2107357-XXX" }
```

### Passos:

1. **Buscar geometria do imovel** — consultar `geo_car` por codigo CAR
2. **Cruzar com todas as camadas** via PostGIS ST_Intersects:
   - Embargos IBAMA (environmental_alerts)
   - Alertas DETER (geo_deter_amazonia + geo_deter_cerrado)
   - PRODES desmatamento anual (geo_prodes) — filtrar por year >= 2019 para MCR 2.9
   - MapBiomas Alertas (geo_mapbiomas_alertas)
   - Terras Indigenas (geo_terras_indigenas)
   - Unidades Conservacao (geo_unidades_conservacao)
   - Embargos ICMBio (geo_embargos_icmbio)
   - Processos minerarios (quando ANM funcionar)
   - Credito rural parcelas (mapbiomas_credito_rural)
3. **Consultar APIs em tempo real**:
   - DataJud: processos judiciais do proprietario
   - BrasilAPI: dados CNPJ
   - Earth Engine: uso do solo, fogo, solo, agua (etl_earth_engine.py)
   - MapBiomas Alerta GraphQL: alertas especificos do CAR
4. **Calcular scores**:
   - MCR 2.9: checklist (CAR ativo + sem PRODES pos-2019 + sem embargo + sem TI/UC + sem Lista Suja)
   - EUDR: sem desmatamento pos-2020 + sem degradacao
   - Geral: 0-1000 combinando todos os eixos
5. **Gerar resposta JSON** com todos os dados consolidados
6. **Export PDF** via WeasyPrint

### Funcoes ja prontas para usar:
- `etl_earth_engine.py`: `extract_lulc_for_property()`, `extract_fire_for_property()`, `extract_soil_for_property()`, `extract_water_for_property()`
- `collectors/datajud.py`: `DataJudCollector.search_by_cpf_cnpj()`
- `collectors/receita_federal.py`: consulta CNPJ via BrasilAPI

---

## COMANDOS RAPIDOS

```bash
# Subir
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# Reinstalar deps (se container foi recriado)
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 pip install agrobr basedosdados earthengine-api

# Inventario do banco
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python -c "
from sqlalchemy import create_engine, text
engine = create_engine('postgresql://agrojus:agrojus@db:5432/agrojus')
tables = ['environmental_alerts','mapbiomas_credito_rural','geo_car','geo_deter_amazonia','geo_deter_cerrado','geo_prodes','geo_unidades_conservacao','geo_embargos_icmbio','geo_autos_icmbio','geo_terras_indigenas','geo_armazens_silos','geo_frigorificos','geo_rodovias_federais','geo_ferrovias','geo_portos','geo_mapbiomas_alertas','sicor_custeio_uf','bigquery_pam_temporaria','bigquery_pam_permanente','bigquery_cnpj_agro','bigquery_ppm_rebanhos','bigquery_ppm_producao_animal','bigquery_prodes_municipio','bigquery_sicor_operacoes','bigquery_sicor_propriedades','bigquery_geo_municipios','bigquery_censo_municipio','mapbiomas_legality','mapbiomas_cobertura_2024','mapbiomas_cobertura_serie']
total=0
for t in tables:
    with engine.connect() as c:
        try:
            r=c.execute(text(f'SELECT COUNT(*) FROM \"{t}\"'));n=r.scalar();total+=n;print(f'{t}: {n:,}')
        except: pass
print(f'TOTAL: {total:,}')
"

# Testar Earth Engine
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python -c "
import ee; ee.Initialize(project='agrojus')
img = ee.Image('projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_integration_v2')
print(f'EE OK: {len(img.getInfo()[\"bands\"])} bandas')
"

# Testar MapBiomas Alerta
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python -c "
import httpx
url='https://plataforma.alerta.mapbiomas.org/api/v2/graphql'
r=httpx.post(url,json={'query':'mutation{signIn(email:\"eduardo@guerreiro.adv.br\",password:\"1qasw23edFR\$\"){token}}'})
token=r.json()['data']['signIn']['token']
r2=httpx.post(url,json={'query':'{alerts(limit:1,page:1){metadata{totalCount}}}'}, headers={'Authorization':f'Bearer {token}','Content-Type':'application/json'})
print(r2.json())
"

# Testar DataJud
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python -c "
import httpx
r=httpx.post('https://api-publica.datajud.cnj.jus.br/api_publica_tjma/_search',json={'query':{'match_all':{}},'size':1},headers={'Authorization':'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==','Content-Type':'application/json'})
print(f'DataJud OK: {r.json()[\"hits\"][\"total\"][\"value\"]:,} processos no TJMA')
"

# Swagger UI
# http://localhost:8000/docs

# Frontend (prototipo atual)
# cd frontend && npm run dev → http://localhost:5173
```

---

## CREDENCIAIS (nao commitar .env!)

| Servico | Localizacao |
|---|---|
| PostgreSQL | localhost:5432, agrojus/agrojus |
| GCP Project | agrojus |
| GCP Credentials | ${APPDATA}/gcloud/application_default_credentials.json (montado no container) |
| MapBiomas | eduardo@guerreiro.adv.br (em .env) |
| DataJud | API key publica em config.py |
| JWT Secret | Valor default dev (trocar antes de deploy!) |

---

## RESUMO PARA QUEM NAO LEU NADA

AgroJus tem 42 tabelas com 10.2M registros sobre imoveis rurais do Brasil: embargos, desmatamento, areas protegidas, credito rural, processos minerarios, infraestrutura logistica, producao agricola, empresas agro, censo. Mais acesso a 7B linhas via BigQuery, 515k alertas via MapBiomas, 88 tribunais via DataJud, dados de satelite via Earth Engine.

Falta o motor que junta tudo: usuario digita codigo do imovel, sistema cruza com as 42 tabelas, calcula score de risco, gera PDF. Isso e a Fase 2.

---

*AgroJus v0.9.0 — Handoff Final — 2026-04-15 07:30 BRT*
