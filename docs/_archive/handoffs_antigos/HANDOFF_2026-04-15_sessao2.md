# AgroJus — Handoff Sessao 2 (2026-04-15 ~06:50 BRT)

**Branch:** `claude/continue-backend-dev-sVLGG`

---

## O que foi feito nesta sessao

### Pesquisa Competitiva Completa
- **53 sites analisados** em 7 lotes paralelos (Tavily crawl/extract/search)
- 7 concorrentes diretos, 2 fintechs, 8 portais, 18 gov, 6 clima, 5 APIs, 7 UX
- Documento: `docs/ANALISE_COMPETITIVA_COMPLETA.md`
- 336 features catalogadas: `docs/INVENTARIO_FEATURES.md`
- Status de todas as fontes: `docs/STATUS_FONTES_DADOS.md`

### Descobertas Estrategicas
- **agrobr** (pip): 38 fontes agro unificadas — resolve CEPEA 403
- **DataJud API key publica** — sem cadastro, 88 tribunais
- **AdvLabs** — concorrente juridico real com 128 teses + CRM
- **Embrapa AgroAPI** — ZARC, clima, NDVI, agrotoxicos gratis (1K/mes)

### Novos Dados Carregados no PostGIS

| Tabela | Registros | Fonte |
|---|---|---|
| `geo_unidades_conservacao` | 346 | ICMBio via INDE WFS |
| `geo_prodes` | 50.000 | INPE TerraBrasilis WFS |
| `sicor_custeio_uf` | 50.000 | BCB SICOR OData |
| `geo_embargos_icmbio` | 5.000 | ICMBio via INDE WFS |
| `geo_autos_icmbio` | 10.000 | ICMBio via INDE WFS |
| `geo_car` | ~135.000 (carregando) | SICAR WFS, 27 estados |

### Configuracoes Realizadas
- DataJud API key publica em `app/config.py`
- GCP Project ID `agrojus` em config + docker-compose
- Google Cloud auth credentials montado no container Docker
- `basedosdados` e `agrobr` adicionados ao `requirements.txt`
- BigQuery testado e funcionando (CNPJ 3B linhas, PAM 20M acessiveis)
- Catalogo de camadas (`camadas.py`) atualizado com novas tabelas

### ETL Scripts Criados/Corrigidos
- `scripts/etl_icmbio_ucs.py` — layer name corrigido para `ICMBio:limiteucsfederais_a`
- `scripts/etl_prodes.py` — layer name corrigido para `prodes-legal-amz:accumulated_deforestation_2007`
- `scripts/etl_anm_sigmine.py` — criado (paginacao ainda com problemas)
- `scripts/etl_sicar_nacional.py` — NOVO, carrega 27 estados com SSL fix
- `scripts/etl_mte_lista_suja_csv.py` — NOVO, tenta CSV em vez de PDF (portais instáveis)

---

## Estado do Banco de Dados (apos sessao 2)

**~6.1M registros em 26+ tabelas** (sem contar geo_car que esta carregando)

### Tabelas com dados:
```
environmental_alerts          104.284  (IBAMA + MTE)
mapbiomas_credito_rural     5.614.207  (MapBiomas GPKG)
geo_car                      ~135.000  (SICAR WFS, 27 UFs) ← CARREGANDO
geo_deter_amazonia             50.000  (INPE WFS)
geo_deter_cerrado              50.000  (INPE WFS)
geo_prodes                     50.000  (INPE WFS) ← NOVO
geo_unidades_conservacao          346  (ICMBio/INDE) ← NOVO
geo_embargos_icmbio             5.000  (ICMBio/INDE) ← NOVO
geo_autos_icmbio               10.000  (ICMBio/INDE) ← NOVO
geo_terras_indigenas              655  (FUNAI WFS)
geo_armazens_silos             16.676  (MapBiomas)
geo_frigorificos                  207  (MapBiomas)
geo_rodovias_federais          14.255  (MapBiomas)
geo_ferrovias                   2.244  (MapBiomas)
geo_portos                         35  (MapBiomas)
sicor_custeio_uf               50.000  (BCB OData) ← NOVO
mapbiomas_stats (~7 tabelas)  ~26.659  (MapBiomas)
market_quotes                      24  (Yahoo Finance)
```

### BigQuery (acesso externo via google-cloud-bigquery):
- Project: agrojus
- br_me_cnpj.empresas: 2.8B linhas
- br_me_cnpj.estabelecimentos: 3.0B linhas
- br_me_cnpj.socios: 1.2B linhas
- br_ibge_pam: 20M linhas (lavoura temporaria + permanente)

---

## Pendencias para Proxima Sessao

### Fase 1 restante (fontes de dados):
1. **MapBiomas Alerta** — Eduardo criar conta em plataforma.alerta.mapbiomas.org
2. **Embrapa AgroAPI** — Eduardo criar conta em agroapi.cnptia.embrapa.br
3. **Portal Transparencia** — Eduardo cadastrar email para API key
4. **ANM/SIGMINE** — corrigir paginacao (download KMZ como alternativa)
5. **Quilombolas INCRA** — bloqueado (login gov.br necessario)
6. **DETER completo** — baixar shapefile 800k+ (nao WFS)
7. Criar wrappers agrobr para CEPEA/B3/CONAB como endpoints

### Fase 2 (motor central):
1. `POST /api/v1/imovel/relatorio` — cruzar imovel com TODAS as tabelas via PostGIS
2. Motor Score MCR 2.9 (checklist auditavel)
3. Motor Score EUDR
4. Export PDF (WeasyPrint)

---

## Comandos Rapidos

```bash
# Subir
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# Reinstalar deps novas (se container foi recriado)
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 pip install agrobr basedosdados

# Inventario do banco
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python //app/scripts/db_inventory.py

# Testar BigQuery
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python -c "
from google.cloud import bigquery
client = bigquery.Client(project='agrojus')
df = client.query('SELECT COUNT(*) as total FROM \`basedosdados.br_me_cnpj.empresas\`').to_dataframe()
print(df)
"

# Testar DataJud
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python -c "
import httpx
r = httpx.post('https://api-publica.datajud.cnj.jus.br/api_publica_tjma/_search',
    json={'query':{'match':{'assuntos.nome':'Usucapião'}},'size':1},
    headers={'Authorization':'APIKey cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==','Content-Type':'application/json'})
print(r.json()['hits']['total'])
"
```

---

*AgroJus v0.8.0 — Handoff Sessao 2 — 2026-04-15*
