# PESQUISA DE FONTES DE DADOS — AgroJus

> **Este documento requer muita dedicação de pesquisa antes de qualquer implementação.**
> Nenhuma das fontes abaixo pode ser considerada "pronta" sem validação técnica detalhada.
> Atualizado: 2026-04-15

---

## ⚠️ AVISO GERAL — Por que esta pesquisa é crítica

O AgroJus depende de **fontes públicas instáveis, mal documentadas e em constante migração**.
Antes de implementar qualquer ETL, é obrigatório:

1. **Verificar se a URL ainda existe** (portais governamentais mudam sem aviso)
2. **Verificar o formato real dos dados** (CSV pode não ter o schema documentado)
3. **Verificar o tamanho** (um CSV "simples" pode ter 10GB)
4. **Verificar a licença** (dados públicos nem sempre são de uso livre para comercialização)
5. **Verificar a frequência de atualização** (dados de 2019 são inúteis para MCR 2.9)
6. **Testar dentro do container Docker** (alguns endpoints bloqueiam IPs de cloud/VPS)

---

## 1. dados.gov.br — SITUAÇÃO ATUAL E COMO USAR

### O que é
Portal Nacional de Dados Abertos do governo federal. Hospeda metadados e links de download de centenas de datasets de todos os ministérios. É baseado no **CKAN** (Comprehensive Knowledge Archive Network), o mesmo software usado pela ONU e União Europeia.

### 🚨 Situação Atual (verificado em 15/04/2026): INSTÁVEL

O portal passou por uma **migração de plataforma em 2024-2025** e ainda apresenta:
- API CKAN retornando `401 Unauthorized` na maioria dos endpoints
- Muitos datasets com links quebrados (arquivos movidos de servidor)
- Interface web funciona, API programática falha

```bash
# Teste feito em 15/04/2026 dentro do container:
GET https://dados.gov.br/api/3/action/site_read → 401 Unauthorized
GET https://dados.gov.br/api/3/action/package_list → 401
GET https://dados.gov.br/api/3/action/package_search?q=ibama → 401
```

### Como navegar CORRETAMENTE

**✅ O que funciona:**
```
# Busca via interface web (FUNCIONA)
https://dados.gov.br/dados/conjuntos-dados?q=embargo

# URLs diretas dos arquivos (ignorar CKAN, ir direto ao servidor dos ministérios)
https://dadosabertos.ibama.gov.br/   → IBAMA (tem CKAN próprio — funciona)
https://dadosabertos.ana.gov.br/     → ANA (CKAN próprio — instável)
https://dados.agricultura.gov.br/    → MAPA (funciona)
https://dados.incra.gov.br/          → INCRA (funciona)
```

**❌ O que NÃO funciona:**
```
# API CKAN central do dados.gov.br → 401 em todas as rotas
https://dados.gov.br/api/3/action/...
```

### Estratégia recomendada
Ignorar a API CKAN central. Ir **diretamente aos portais de dados abertos dos ministérios**.
Cada ministério tem seu próprio CKAN independente:

| Ministério | Portal direto | Status |
|---|---|---|
| IBAMA | `dadosabertos.ibama.gov.br` | ✅ Funciona |
| MTE (Trabalho) | `portaldatransparencia.gov.br/download-de-dados` | ✅ Funciona |
| INCRA | `dados.incra.gov.br` | ✅ Funciona |
| MAPA (Agricultura) | `dados.agricultura.gov.br` | ✅ Funciona |
| ANEEL | `dadosabertos.aneel.gov.br` | ✅ Funciona |
| ANA (Água) | `dadosabertos.ana.gov.br` | ⚠️ Instável |
| BCB (Banco Central) | `dadosabertos.bcb.gov.br` | ✅ Funciona |
| ANM (Mineração) | `geo.anm.gov.br` (ArcGIS REST) | ✅ Funciona |

### Datasets confirmados com URL direta

```
IBAMA — Embargos (✅ 103k no PostGIS):
https://dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo_csv.zip
Tamanho: ~180MB zip / ~800MB descomprimido
Frequência atualização: diária
Schema: cpf_cnpj, nome_embargo, municipio, uf, coordenada_lat, coordenada_lon, dat_embargo, situacao

IBAMA — Autos de Infração (❌ Pendente):
https://dadosabertos.ibama.gov.br/dados/SICAFI/autuacao/Autuacao.csv
⚠️ PROBLEMA: portal retorna CSV com 4 linhas (bug ativo em 15/04/2026)
Solução: monitorar ou solicitar via LAI (Lei de Acesso à Informação)
Conteúdo esperado: ~300k multas ambientais, valor, tipo, localização

MTE — Lista Suja Trabalho Escravo (✅ 614 no PostGIS):
https://portaldatransparencia.gov.br/download-de-dados/trabalho-escravo
Frequência: semestral (jan e jul)
Formato atual: PDF com tabela (CSV pode estar com link quebrado)
ETL: etl_mte_escravo.py usa regex no PDF — solução funcionando

INCRA — Assentamentos (❌ Pendente):
https://dados.incra.gov.br/dataset/relacao-de-projetos-de-assentamento
Formato: CSV + SHP
Conteúdo: ~1M famílias assentadas, coordenadas dos PAs

MAPA — Agrofit (agrotóxicos):
https://dados.agricultura.gov.br/dataset/agrofit
Relevância: saber se o imóvel usa agrotóxicos regulamentados
```

---

## 2. basedosdados.org — GUIA TÉCNICO COMPLETO

### O que é
Organização sem fins lucrativos que **normaliza e hospeda dados públicos brasileiros no Google BigQuery**.
Em vez de baixar e parsear CSVs sujos de cada portal, você executa SQL diretamente.

**Site:** `basedosdados.org`
**BigQuery:** `basedosdados.*`
**GraphQL (catálogo):** `https://backend.basedosdados.org/api/v1/graphql`
**Documentação:** `https://basedosdados.github.io/mais/`

### Por que é tão valioso para o AgroJus

| Sem BasedosDados | Com BasedosDados |
|---|---|
| Baixar CSV de 8GB do IBGE | `SELECT * FROM basedosdados.br_ibge_pam.municipio` |
| Parsear 30 formatos diferentes | Schema normalizado, UTF-8, tipos corretos |
| Cruzar 3 arquivos manualmente | JOIN em SQL direto |
| Dados de 2019 porque atualizou | Pipeline automático → sempre atualizado |

### Formas de acesso (verificado na doc oficial 15/04/2026)

| Método | Detalhes |
|---|---|
| **BigQuery (SQL)** | 1TB grátis/mês. Requer GCP project. Queries em segundos |
| **Python** | `pip install basedosdados` → `bd.read_sql(query, billing_project_id)` |
| **R** | Pacote R disponível |
| **Download CSV** | Direto no site, mas apenas tabelas <200k linhas |
| **Mecanismo de busca** | `basedosdados.org/search` → buscar por tema |

### Situação atual (15/04/2026)

```
Status da API GraphQL (metadados sem login):
✅ https://backend.basedosdados.org/api/v1/graphql → 200 OK

Status do BigQuery (dados reais):
❌ Requer GCP_PROJECT_ID configurado no ambiente
❌ Não configurado ainda — BLOQUEIO PRINCIPAL
```

### Como desbloquear o BigQuery

**Passo a passo para o usuário:**
1. Acesse `console.cloud.google.com`
2. Crie um novo projeto (ex: `agrojus-dados`)
3. Ative a fatura (cartão de crédito, mas fica no free tier)
4. O BigQuery tem **1TB grátis por mês** de queries — suficiente para todo o AgroJus
5. Adicione ao arquivo `.env` do projeto:
   ```
   GCP_PROJECT_ID=agrojus-dados
   ```
6. Execute dentro do container:
   ```bash
   docker exec -e PYTHONPATH=/app agrojus-backend-1 python /app/scripts/etl_basedosdados.py
   ```

### Catálogo de tabelas de alto valor para o AgroJus

#### Grupo 1 — CNPJ / Empresas (mais crítico para o dossiê)
```sql
-- Razão social, natureza jurídica, capital social, data de abertura
SELECT razao_social, cnpj, natureza_juridica_id, capital_social, data_abertura_empresa
FROM `basedosdados.br_me_cnpj.empresas`
WHERE cnpj = '12345678000100'

-- Estabelecimentos: CNAE, endereço, situação atual, telefone
SELECT cnpj_basico, nome_fantasia, situacao_cadastral, cnae_fiscal_principal,
       logradouro, municipio, uf, cep
FROM `basedosdados.br_me_cnpj.estabelecimentos`
WHERE cnpj_basico = '12345678'

-- Sócios e quadro societário
SELECT cnpj_basico, nome_socio, identificador_socio, data_entrada_sociedade
FROM `basedosdados.br_me_cnpj.socios`
WHERE cnpj_basico = '12345678'
```
**Tamanho:** >50M linhas por tabela. Requer filtro — nunca fazer SELECT * sem WHERE.

#### Grupo 2 — Agropecuária IBGE
```sql
-- PAM: Produção Agrícola Municipal (soja, milho, café, etc.)
SELECT ano, id_municipio, produto, area_plantada, area_colhida,
       quantidade_produzida, rendimento_medio, valor_producao
FROM `basedosdados.br_ibge_pam.municipio`
WHERE produto = 'Soja (em grão)' AND ano = 2023
ORDER BY quantidade_produzida DESC LIMIT 100

-- PPM: Produção Pecuária Municipal (rebanho, leite, ovos)
SELECT ano, id_municipio, tipo_de_rebanho, quantidade_cabecas,
       valor_producao
FROM `basedosdados.br_ibge_ppm.municipio`
WHERE tipo_de_rebanho = 'Bovino' AND ano = 2023

-- Censo Agropecuário 2017 por município
SELECT id_municipio, numero_estabelecimentos, area_total_ha,
       area_lavouras_ha, area_pastagens_ha, pessoal_ocupado
FROM `basedosdados.br_ibge_censo_agropecuario.municipio_2017`
```

#### Grupo 3 — Meio Ambiente e Compliance
```sql
-- Trabalho escravo com localização (complementa MTE)
SELECT ano, cnpj_cpf, nome_empregador, municipio, uf,
       trabalhadores_resgatados, atividade_economica
FROM `basedosdados.br_mte_trabalho_escravo.microdados`
ORDER BY ano DESC

-- RAIS: Vínculos empregatícios formais (valida se empresa existe)
SELECT cnpj, razao_social, municipio, uf, quantidade_vinculos_ativos
FROM `basedosdados.br_me_rais.microdados_estabelecimentos`
WHERE ano = 2022 AND cnpj = '12345678000100'
```

#### Grupo 4 — Valor da Terra e Mercado
```sql
-- Preços de terra agrícola (FGV/CEPEA histórico se disponível)
-- Nota: verificar se BasedosDados tem esta tabela

-- Financiamentos rurais por município
SELECT municipio, uf, ano_contrato, valor_custeio, valor_investimento,
       area_financiada, produto
FROM `basedosdados.br_bcb_sicor.microdados_operacoes`
WHERE ano_contrato >= 2020
-- Nota: SICOR no BD pode ser mais estável que a API OData direta
```

### Consulta via Python (como implementar)
```python
# Requer: pip install basedosdados google-cloud-bigquery
import basedosdados as bd

# Método 1: SQL direto
df = bd.read_sql(
    query="""
        SELECT razao_social, cnpj, cnae_fiscal_principal, municipio, uf
        FROM `basedosdados.br_me_cnpj.estabelecimentos`
        WHERE cnpj_basico = '12345678'
        LIMIT 10
    """,
    billing_project_id="agrojus-dados"  # GCP_PROJECT_ID
)

# Método 2: read_table (mais simples para tabelas pequenas)
df = bd.read_table(
    dataset_id="br_ibge_pam",
    table_id="municipio",
    billing_project_id="agrojus-dados",
    query_project_id="basedosdados"
)
```

### Pesquisa de datasets pendente no BasedosDados

Os seguintes tópicos precisam ser pesquisados no catálogo:
```
# Acesse: https://basedosdados.org/dataset
# Busque por: sicar, car, incra, sigef, ibama, ana, mapbiomas

Verificar se existem:
- [ ] SICAR/CAR (Cadastro Ambiental Rural)
- [ ] SIGEF/INCRA (parcelas certificadas)
- [ ] IBAMA embargos (pode estar no BD além do dadosabertos)
- [ ] ANA outorgas de água
- [ ] FUNAI Terras Indígenas
- [ ] MapBiomas statistics no BigQuery
- [ ] Transações imobiliárias rurais (ONR futuro)
- [ ] ZARC/EMBRAPA zoneamento
- [ ] Dados de preço de terra por município
```

---

## 3. MapBiomas — GUIA TÉCNICO COMPLETO

### O que é
MapBiomas é um **consórcio de universidades, ONGs e empresas tech** que usa Google Earth Engine (GEE) para mapear uso e cobertura do solo do Brasil anualmente desde 1985. É a referência científica oficial usada pelo INPE, ICMBio, Ministério do Meio Ambiente e pelo próprio governo federal para o PRODES.

**Site principal:** `mapbiomas.org`
**Plataforma interativa:** `plataforma.brasil.mapbiomas.org`
**Dados:** `storage.googleapis.com/mapbiomas-public/...`
**GEE Assets:** `projects/mapbiomas-public/assets/brazil/...`

### Por que é o diferencial máximo do AgroJus

Nenhum concorrente usa **todos** os 18 subprodutos. Nós vamos usar todos.
O MapBiomas tem **38 anos de histórico** de cada metro quadrado do Brasil — isso é o que permite provar (ou não) conformidade EUDR e MCR 2.9.

---

### Inventário completo dos 18 Subprodutos

#### 1. Cobertura e Uso da Terra (Coleção 10.1) — CARRO-CHEFE

**O que é:** Mapeamento anual de 1985 a 2023. Classifica **cada pixel de 30m** do Brasil em uma das categorias:
- Floresta: Formação florestal, Savana, Mangue, Restinga...
- Agropecuária: Soja, Milho, Cana, Café, Citrus, Arroz, Algodão, Pastagem...
- Não-vegetação: Área urbanizada, Mineração, Praia/Duna, Aquicultura...
- Água: Rio, Lago, Reservatório...

**Por que é essencial:**
- MCR 2.9: banco precisa provar que não financiou desmatamento pós-31/07/2019
- EUDR: exportador precisa provar que produto não veio de área desmatada pós-2020
- Valuation: saber se terra é soja, pasto ou floresta muda tudo no preço/ha

**Como acessar (4 métodos confirmados no site oficial):**

**Método 1 — Download direto GeoTIFF (VERIFICADO 15/04/2026):**
```
# Cobertura Brasil 2024 (30m):
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_10/lulc/coverage/brazil_coverage_2024.tif

# Cobertura 10 metros (Sentinel-2, Collection 2 Beta):
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/lulc_10m/collection_2/integration/mapbiomas_10m_collection2_integration_v1-classification_2023.tif

# ⚠️ Tamanhos: 3-15GB por bioma. Usar COG ou GEE para consulta pontual.
```

**Método 2 — GEE Asset (requer conta Google Earth Engine):**
```python
# Coverage (Collection 10.1) — CONFIRMADO
asset = "projects/mapbiomas-public/assets/brazil/lulc/collection10_1/mapbiomas_brazil_collection10_1_coverage_v1"

# Deforestation & Secondary Vegetation (Collection 10.1)
asset_defor = "projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_deforestation_secondary_vegetation_v2"
```

**Método 3 — Toolkit GEE (interface interativa para download custom):**
```
# Land use and cover:
https://code.earthengine.google.com/?accept_repo=users/mapbiomas/user-toolkit&scriptPath=users/mapbiomas/user-toolkit:mapbiomas-user-toolkit-lulc.js

# Deforestation:
https://code.earthengine.google.com/?accept_repo=users/mapbiomas/user-toolkit&scriptPath=users/mapbiomas/user-toolkit:mapbiomas-user-toolkit-deforestation-regeneration.js

# Instruções: https://github.com/mapbiomas/user-toolkit
```

**Método 4 — Plataforma MapBiomas (download via interface web):**
```
https://plataforma.brasil.mapbiomas.org  →  "Criar análise" → download
https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/10/how_to_download_maps_MapBiomas_platform_PT_EN_v4.pdf
```

**Legenda de classes (parcial):**
```
1   = Floresta       3  = Formação Florestal   4  = Savana Arborizada
9   = Silvicultura   11 = Área Alagável        12 = Formação Campestre
14  = Agropecuária   15 = Pastagem             19 = Lavoura Temporária
20  = Cana-de-Açúcar 21 = Mosaico Agropecuário 24 = Área Urbanizada
25  = Outra Área não Vegetada                  29 = Afloramento Rochoso
30  = Mineração      33 = Rio/lago             36 = Lavoura Perene
39  = Soja           40 = Arroz                41 = Outras Lavouras
46  = Café           47 = Citrus               48 = Algodão
62  = Algodoeiro     ...
```

**Estratégia de implementação:**
- Para consultas pontuais(coordenada): usar GEE Python SDK
- Para carregar no PostGIS: `raster2pgsql` com GeoTIFF por bioma
- Para o mapa: WMS tile service do MapBiomas (não precisa baixar)

**WMS Tiles (para o mapa Leaflet — já funciona):**
```
https://tiles.mapbiomas.org/collections/{coleção}/coverage/tiles/{z}/{x}/{y}.png?year={ano}
```

---

#### 2. MapBiomas 10 metros (Coleção Beta) — DIFERENCIAL EXCLUSIVO

**O que é:** Mesmo conceito da Col.10 mas com **10m de resolução** (Sentinel-2, desde 2016).
Resolução 9× maior — diferencia variedades de culturas, detalha APP ripária.

**Acesso (VERIFICADO):**
```
# GEE Asset:
projects/mapbiomas-public/assets/brazil/lulc_10m/collection2/mapbiomas_10m_collection2_integration_v1

# Download direto GeoTIFF (2023):
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/lulc_10m/collection_2/integration/mapbiomas_10m_collection2_integration_v1-classification_2023.tif

# Toolkit GEE:
https://code.earthengine.google.com/?accept_repo=users/mapbiomas/user-toolkit&scriptPath=users/mapbiomas/user-toolkit:mapbiomas-user-toolkit-lulc.js
```
**Status:** Nenhum concorrente usa isso publicamente.

---

#### 3. MapBiomas Fogo (Coleção 4) — SEGURO E COMPLIANCE

**O que é:** Cicatrizes de incêndio anuais e mensais de 1985 a 2024.
Mapeia **onde e quando** o Brasil pegou fogo.

**Por que importa:**
- Histórico de incêndios por propriedade = risco para seguro rural
- Fogo em APP = infração ambiental mesmo que não seja desmatamento
- Fogo recorrente em pasto = manejo inadequado

**Acesso (VERIFICADO — URLs reais do site oficial):**
```
# Download direto GeoTIFF — Annual burned 2024:
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/fire-col4/annual_burned/mapbiomas_fire_col4_br_annual_burned_2024.tif

# Vetorial (shapefile zip):
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/fire-col4/annual_burned_vectors_v1/mapbiomas_fire_col4_br_annual_burned_2024.zip

# Monthly burned 2024:
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/fire-col4/monthly_burned_v1/mapbiomas_fire_col4_br_monthly_burned_2024.tif

# Accumulated burned 1985-2024:
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/fire-col4/accumulated_burned_v1/mapbiomas_fire_col4_br_accumulated_burned_1985_2024.tif

# Fire frequency:
https://storage.googleapis.com/mapbiomas-public/initiatives/brasil/collection_9/fire-col4/fire_frequency_v1/mapbiomas_fire_col4_br_fire_frequency_1985_2024.tif

# GEE Assets:
projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_fire_collection4_annual_burned_v1
projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_fire_collection4_monthly_burned_v1
projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_fire_collection4_fire_frequency_v1
projects/mapbiomas-public/assets/brazil/fire/collection4/mapbiomas_fire_collection4_year_last_fire_v1

# Fire Monitor (mensal — quase tempo real):
projects/mapbiomas-public/assets/brazil/fire/monitor/mapbiomas_fire_monthly_burned_v1
```

---

#### 4. Monitor Mensal do Fogo — ALERTAS EM TEMPO REAL

**Plataforma:** `https://plataforma.monitorfogo.mapbiomas.org/`
**O que tem:** Alertas de fogo em tempo quase-real (atualização mensal)
**Aplicação:** Alerta imediato para proprietários com imóvel em área de fogo recente

---

#### 5. MapBiomas Alerta (API GraphQL) — PEÇA CENTRAL PARA EUDR

**O que é:** Alertas de desmatamento **validados por técnicos** com laudos técnicos georreferenciados.
Diferente do DETER (alerta automático, sem laudo), o MapBiomas Alerta tem laudo técnico que tem **validade jurídica** para defesa ou acusação em processo.

**Por que é diferente do DETER:**
- DETER: detecção automática por satélite (falsos positivos)
- MapBiomas Alerta: validação humana + laudo técnico assinado

**Acesso:**
```
# GraphQL endpoint (requer conta gratuita):
https://plataforma.alerta.mapbiomas.org/api/v2/graphql

# Queries disponíveis:
alerts         → lista de alertas na região
alert(id)      → detalhe + laudo técnico
alertReport    → exportar CSV/SHP em massa
```

**Como usar:**
```graphql
query AlertasPorPoligono($geometry: String!) {
  alerts(
    where: { geometry: { intersects: $geometry } }
    orderBy: { detectedAt: desc }
    first: 100
  ) {
    id
    alertCode
    areaHa
    detectedAt
    confirmedAt
    source
    biome
    territory { name }
    geometry { type coordinates }
  }
}
```

**Status atual:** ❌ Conta não criada ainda. Criar em `plataforma.alerta.mapbiomas.org`

---

#### 6. Monitor do Crédito Rural — EXCLUSIVIDADE MAPBIOMAS

**O que é:** Integração dos polígonos de parcelas de financiamento rural (BCB) com detecções de desmatamento.
**Plataforma:** `https://plataforma.creditorural.mapbiomas.org`

**Por que é ouro:** Permite responder: *"Este crédito rural financiou atividade em área desmatada?"*
Nenhum concorrente tem isso automatizado.

**Status atual:** ✅ 5.614.207 parcelas carregadas no PostGIS
**Pendência:** Não cruzamos ainda os polígonos com DETER/PRODES automaticamente via PostGIS

---

#### 7. Monitor da Recuperação — ESG e Mercado de Carbono

**Plataforma:** `https://plataforma.recuperacao.mapbiomas.org/`
**O que tem:** Áreas em processo de regeneração/recuperação da vegetação nativa
**Aplicação:**
- Proprietário em recuperação = risco ESG MENOR (pode cobrar mais no valuation)
- Potencial de créditos de carbono REDD+ na propriedade
- Prova de conformidade com PLANAVEG

**Status:** ✅ Download parcial (132 MB Col.10) — precisa carregar no PostGIS

---

#### 8. Monitor da Mineração — GARIMPO ILEGAL

**Plataforma:** `https://plataforma.monitormineracao.mapbiomas.org/`
**O que detecta:** Garimpo ilegal por satélite (Amazônia, TIs)
**Aplicação:** Imóvel com garimpo detectado = risco crítico (crime ambiental + trabalhista)

**Status:** ✅ Stats no PostGIS (1.294 registros) — falta polígonos para o mapa

---

#### 9. Módulo Urbano — IMÓVEL RURAL NA FRANJA URBANA

**O que é:** Mapeamento de expansão urbana 1985-2023
**Aplicação:** Classificar se imóvel está em zona rural ou franja urbana (impacto tributário e de uso)

**Status:** ✅ Baixado (59 MB zip)

---

#### 10. MapBiomas Água — RISCO HÍDRICO

**O que é:** Mapeamento anual de superfícies hídricas (rios, lagos, várzeas, reservatórios)
**Aplicação:**
- Compliance de APP ripária (30m ao redor de rios)
- Risco de alagamento histórico
- Base para análise de outorga de água

**Status:** ❌ Não baixado ainda
**Como acessar (VERIFICADO):**
```
# GEE Assets:
projects/mapbiomas-public/assets/brazil/water/collection4/mapbiomas_brazil_collection4_water_v3
projects/mapbiomas-public/assets/brazil/water/collection4/mapbiomas_brazil_collection4_water_bodies_v1

# Toolkit GEE:
https://code.earthengine.google.com/?accept_repo=users/mapbiomas/user-toolkit&scriptPath=users/mapbiomas/user-toolkit:mapbiomas-user-toolkit-water.js
```

---

#### 11. MapBiomas Solo — CARBONO E APTIDÃO (MAIOR DIFERENCIAL)

**O que é:** Estoque de carbono orgânico do solo, granulometria, textura
**Dados:** Mapeamento de 0-30cm e 0-100cm de profundidade

**Por que é ENORME para o valuation:**
- Solo rico em carbono = terra mais fértil = maior valor/ha
- Permite calcular potencial de créditos de carbono no solo
- Aptidão agrícola: argiloso (soja) vs arenoso (pastagem) mudam o preço radicalmente

**Status:** ❌ Não explorado — **nenhum concorrente usa isso**
**Como acessar (VERIFICADO):**
```
# GEE Assets — Soil Organic Carbon Stock:
projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_soc_kgc_m2_000_030cm
projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_soc_tc_ha_000_030cm

# GEE Assets — Soil Texture:
projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_granulometry_clay_percentage
projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_granulometry_sand_percentage
projects/mapbiomas-public/assets/brazil/soil/collection2/mapbiomas_soil_collection2_textural_classes

# Toolkit GEE:
https://code.earthengine.google.com/?accept_repo=users/mapbiomas/user-toolkit&scriptPath=users/mapbiomas/user-toolkit:mapbiomas-user-toolkit-soil.js
```

---

#### 12. MapBiomas Degradação (Beta) — EUDR DIFERENCIADO

**O que é:** Detecta degradação da vegetação nativa (não é desmatamento — floresta ainda existe mas está prejudicada)

**Por que é crítico para EUDR:**
A regulação europeia exige conformidade em dois níveis: **sem desmatamento** E **sem degradação**. Nossos concorrentes verificam o primeiro, mas não o segundo.

**Status:** ❌ Não explorado — diferencial exclusivo
**Como acessar (VERIFICADO):**
```
# Toolkit GEE:
https://code.earthengine.google.com/?accept_repo=users/mapbiomas/user-toolkit&scriptPath=users/mapbiomas/user-toolkit:mapbiomas-user-toolkit-degradation.js
```

---

#### 13–18. Atmosfera, Risco Climático, Cacau, Mosaicos, Infraestrutura, Camadas

**13. MapBiomas Atmosfera (NOVO — verificado 15/04/2026):**
```
# Temperatura do ar (anual + mensal + anomalia):
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_air_temperature_annual_v2
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_air_temperature_monthly_v2
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_temperature_anomaly_monthly_v2

# Precipitação:
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_precipitation_annual_v2
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_precipitation_monthly_v2

# Pressão de vapor / Qualidade do ar (PM10, PM2.5):
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_vapor_pressure_deficit_annual_v2
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_pm10_annual_v2
projects/mapbiomas-public/assets/brazil/atmosphere/collection1/mapbiomas_brazil_collection1_pm2p5_annual_v2
```

**14. MapBiomas Risco Climático (NOVO — verificado 15/04/2026):**
```
# Deslizamento urbano, inundação, segurança hídrica:
projects/mapbiomas-public/assets/brazil/climate_risk/collection1/mapbiomas_brazil_collection1_urban_landslide_risk_v1
projects/mapbiomas-public/assets/brazil/climate_risk/collection1/mapbiomas_brazil_collection1_urban_flood_risk_v1
projects/mapbiomas-public/assets/brazil/climate_risk/collection1/mapbiomas_brazil_collection1_water_security_index_v1
```

**15. MapBiomas Agricultura (Collection 10 — verificado):**
```
# Sistemas de irrigação:
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_agriculture_irrigation_systems_v3
# Frequência de cultivo (média + anual):
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_agriculture_number_cycles_mean_v2
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_agriculture_number_cycles_v2
```

**16. MapBiomas Pastagem (Collection 10 — verificado):**
```
# Vigor, idade, biomassa:
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_vigor_v3
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_age_v2
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_pasture_biomass_v2
```

**17. MapBiomas Mineração (Collection 10 — verificado):**
```
projects/mapbiomas-public/assets/brazil/lulc/collection10/mapbiomas_brazil_collection10_mining_substances_v3
```

**Outras (nicho):**
- **Cacau:** mapeamento específico Sul da Bahia — nicho EUDR chocolateiros
- **Mosaicos Landsat:** `projects/nexgenmap/MapBiomas2/LANDSAT/BRAZIL/mosaics-2` — imagens brutas desde 1985
- **Pontos de validação:** dados de campo para checar acurácia
- **Recifes costeiros:** [vetor](https://drive.google.com/file/d/1NiydJsMhc-IO2SDSrlFvu2Yu53AUcGl6/view) + [raster](https://drive.google.com/file/d/1zxzqVmqEuFbS6wpDiWJYHIxrut7jQ8yQ/view)

**Ferramentas adicionais verificadas:**
- **QGIS Plugin:** disponível — instalar diretamente no QGIS via gerenciador de plugins
- **GitHub (códigos de processamento):** https://github.com/mapbiomas/brazil-all-initiatives
- **User Toolkit GitHub:** https://github.com/mapbiomas/user-toolkit

---

### Como o AgroJus usa MapBiomas na prática

```
CENÁRIO 1 — Banco pedindo MCR 2.9:
1. Banco envia coordenadas do imóvel (polígono CAR)
2. AgroJus cruza polígono com MapBiomas Col.10 ans 2019-2023
3. Se houver transição de classe floresta→agropecuária = DESMATAMENTO DETECTADO
4. Consulta MapBiomas Alerta GraphQL → laudo técnico validado
5. Resultado: APTO (sem desmatamento) ou INAPTO (desmatamento detectado)

CENÁRIO 2 — Comprador querendo valuation:
1. Comprador informa código CAR
2. AgroJus extrai uso atual do solo (MapBiomas 2023)
3. Modela valor: soja = R$25k/ha, pasto = R$12k/ha, floresta = R$8k/ha
4. Ajusta por: solo (MapBiomas Solo), infraestrutura (MapBiomas Infra)
5. Desconta riscos: embargos IBAMA, TI, alertas DETER
6. Retorna: R$/ha + intervalo de confiança + fatores positivos/negativos

CENÁRIO 3 — Monitoramento contínuo:
1. Proprietário cadastra imóvel
2. AgroJus verifica MapBiomas Alerta API toda semana
3. Se novo alerta → push notification imediato
4. Monitor do Fogo: se incêndio detectado → alerta urgente
```

---

## 4. IBAMA — FONTES DETALHADAS

### 4.1 Embargos (✅ 103k no PostGIS)
```
URL ZIP: dadosabertos.ibama.gov.br/dados/SIFISC/termo_embargo/termo_embargo_csv.zip
Arquivos internos:
  - termo_embargo.csv     → dados principais (cpf_cnpj, nome, municipio, uf, dat_embargo, situacao)
  - coordenadas.csv       → lat/lon de cada embargo
  - itens.csv             → itens embargados (área, tipo)
  - decisao.csv           → decisões administrativas
  - enquadramento.csv     → artigos legais aplicados
  - historico.csv         → histórico de status
  - anexo.csv             → documentos anexados

Frequência: Atualização mensal
Cuidado: situacao pode ser "Ativo", "Suspenso", "Cancelado", "Encerrado"
         Mostrar apenas "Ativo" para compliance
```

### 4.2 Autos de Infração (~300k multas) — ❌ PENDENTE
```
URL: dadosabertos.ibama.gov.br/dados/SICAFI/autuacao/Autuacao.csv
Problema ativo (15/04/2026): CSV retorna apenas 4 linhas (bug do portal)
Workaround: 
  1. Tentar novamente em dias diferentes (cache bug pode ter TTL)
  2. Solicitar via LAI: https://falabr.cgu.gov.br/
  3. Verificar se existe versão completa no basedosdados.org

Schema esperado:
  cpf_cnpj, nome_autuado, dat_autuacao, num_auto, des_infracao, vl_multa,
  municipio, uf, dat_pagamento, sit_debito
```

### 4.3 SISCOM — Polígonos Embargados — ❌ PENDENTE
```
Portal: siscom.ibama.gov.br
O que tem: shapefiles dos polígonos das áreas embargadas (diferente do CSV tabular)
Aplicação: renderizar no mapa o polígono exato do embargo
Como baixar: navegação manual no portal SISCOM → Dados Geoespaciais → Embargo
Formato: Shapefile → importar com ogr2ogr → PostGIS
```

---

## 5. INPE TERRABRASILIS — DETER E PRODES

### 5.1 DETER (✅ 50k cada no PostGIS)
```
# WFS Amazônia (50k alertas — máximo da query WFS)
https://terrabrasilis.dpi.inpe.br/geoserver/deter-amz/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=deter-amz:deter_amz

# WFS Cerrado (50k alertas — máximo da query WFS)
https://terrabrasilis.dpi.inpe.br/geoserver/deter-cerrado/ows?service=WFS&version=2.0.0&request=GetFeature&typeName=deter-cerrado:deter_cerrado

# Downloads completos (sem limite de 50k):
https://terrabrasilis.dpi.inpe.br/downloads/

DETER Amazônia total: ~800k alertas (precisamos carregar tudo, não só 50k)
DETER Cerrado total: ~200k alertas

Frequência: diária (alertas de hoje disponíveis amanhã)
Limitação WFS: 50.000 features por query (usar paginação ou download completo)
```

### 5.2 PRODES (❌ Pendente)
```
# PRODES: desmatamento ANUAL consolidado (não alerta — dado oficial)
https://terrabrasilis.dpi.inpe.br/geoserver/prodes-cerrado-nb/wfs?service=WFS
https://terrabrasilis.dpi.inpe.br/geoserver/prodes-amazon/wfs?service=WFS

Diferença DETER vs PRODES:
- DETER: alerta rápido (pode ser falso positivo), resolução menor
- PRODES: dado consolidado e validado (base para políticas), cumulativo

Aplicação MCR 2.9: usar PRODES como fonte primária (mais robusto juridicamente)
Aplicação EUDR: PRODES 2019-2020 é o cut-off oficial
```

---

## 6. ANA — AGÊNCIA NACIONAL DE ÁGUAS

### Situação atual (15/04/2026)
```
Portal CKAN: dadosabertos.ana.gov.br → CKAN retorna 404 nas rotas de API
Portal web: dadosabertos.ana.gov.br → Interface carrega (200 OK)
CSW Metadados: metadados.snirh.gov.br → Retorna 200 (218 datasets listados)
WFS GeoServer: metadados.snirh.gov.br/geoserver → Bloqueado pelo proxy Docker
```

### Datasets prioritários da ANA
```
1. Outorgas de Água (❌ URL de download pendente)
   - O que é: licenças para uso de recursos hídricos
   - Quem tem: proprietários com irrigação, abastecimento, recreação
   - Por que importa: irrigação sem outorga = infração regulatória grave
   - Onde buscar: https://dadosabertos.ana.gov.br/ → buscar "outorga"

2. Hidroweb (estações fluviométricas — parcialmente funciona)
   API: https://www.snirh.gov.br/hidroweb/rest/api/documento/convenio?tipo=2&documentoTipoId=3
   Conteúdo: séries históricas de vazão e nível por estação

3. Bacias Hidrográficas (SHP disponível)
   https://www.snirh.gov.br/portal/snirh/dados-abertos/geoespaciais
   Conteúdo: polígonos das 12 regiões hidrográficas + sub-bacias

4. Reservatórios críticos (API FUNCIONA)
   https://www.ana.gov.br/sar/api/reservatorios
```

### Estratégia para ANA
```
Passo 1: Navegar manualmente em dadosabertos.ana.gov.br
Passo 2: Identificar dataset "Outorgas Superficiais" e "Outorgas Subterrâneas"
Passo 3: Baixar CSV/SHP manualmente
Passo 4: Testar importação via ogr2ogr (para shapes) ou pandas (para CSV)
Passo 5: Atualizar etl_ana_outorgas.py com URL real validada
```

---

## 7. BCB / SICOR — CRÉDITO RURAL

### Situação (15/04/2026)
```
OData API: olinda.bcb.gov.br/olinda/servico/SICOR/versao/v2/odata → 503 (manutenção)
ETL escrito: backend/scripts/etl_sicor_bcb.py

Quando o BCB voltar:
GET .../MCOperacoes → operações de custeio (volume, banco, produto, município)
GET .../MCLimiteMcr → limites aplicados ao MCR (compliance bancária)
```

### Alternativa via BasedosDados (a pesquisar)
```sql
-- Se existir no BD (verificar):
SELECT * FROM `basedosdados.br_bcb_sicor.microdados_operacoes`
WHERE ano_contrato >= 2023
LIMIT 1000

-- Vantagem: sem problema de manutenção na API
```

---

## 8. INCRA — SIGEF E DADOS FUNDIÁRIOS

### Acesso ao SIGEF (parcelas certificadas)
```
WFS oficial: acervofundiario.incra.gov.br/geoserver/wfs
Status: ❌ Bloqueado pelo proxy Docker (DNS resolution timeout)

Alternativa i3geo:
https://acervofundiario.incra.gov.br/i3geo/ogc.php?uf=MT&service=WFS

Parcelas certificadas = imóveis com georreferenciamento aprovado pelo INCRA
Total Brasil: ~700k parcelas
```

### Assentamentos INCRA
```
CSV: https://dados.incra.gov.br/dataset/relacao-de-projetos-de-assentamento
SHP: https://dados.incra.gov.br/dataset/shapefile-projetos-de-assentamento
Conteúdo: ~10k projetos de assentamento, ~1M famílias
Por que importa: área de assentamento tem regime fundiário especial
```

### CNIR (Cadastro Nacional de Imóveis Rurais)
```
O que é: integração INCRA + Receita Federal
Acesso: requer conta Gov.br nível Prata
Portal: cnir.serpro.gov.br
Relevância: único ponto de consulta unificada de imóvel rural
Status: não integrado (requer autenticação pessoal)
```

---

## 9. ONR — REGISTRO DE IMÓVEIS

### O que é e o que tem
```
ONR: Operador Nacional do Registro de Imóveis
Papel: unifica todos os cartórios de registro de imóveis do Brasil
Total: ~3.500 cartórios em todo o Brasil

O que o ONR tem que nenhuma outra fonte tem:
- MATRÍCULA: documento jurídico de titularidade do imóvel
- ÔNUS/GRAVAMES: hipoteca, usufruto, penhora, etc.
- HISTÓRICO: quem foram os donos anteriores e quando venderam
- AVERBAÇÕES: construções, divisas, mudanças de área
- CÉDULAS RURAIS: financiamentos com garantia em imóvel rural

Diferença: CAR/SIGEF mostram onde está o imóvel. Matrícula mostra DE QUEM É.
```

### Como acessar
```
Interface pública: mapa.onr.org.br (NÃO tem API pública)
Consulta por código de matrícula: via cartório de origem
Custos: R$ 30-100 por certidão, dependendo do estado

Estratégias para integração:
1. Convênio B2B com ONR (via contato comercial em onr.org.br)
2. Parceria com serviço intermediário (ex: InfoSimples tem API para certidões)
3. Upload pelo usuário: proprietário faz upload da certidão PDF → OCR

A "interface antiga" refere-se aos 3.500 sistemas individuais dos cartórios
estaduais (ARISP em SP, ARIEMS no MS, etc.) que ainda existed antes do mapa.onr.org.br.
```

---

## 10. INVENTÁRIO COMPLETO DE PENDÊNCIAS TÉCNICAS

### Dados — Pendentes de pesquisa e validação

| # | Fonte | Tipo | Bloqueador | Pesquisa necessária |
|---|---|---|---|---|
| 1 | SICAR/CAR polígonos | WFS/API | Rate limit | Qual o endpoint WFS funcional? Tem API v2? |
| 2 | PRODES (desmatamento anual) | WFS/Download | Não iniciado | Download completo vs WFS. Paginação? |
| 3 | DETER completo (800k alertas) | Download | Só temos 50k | Baixar arquivo completo. Paginação para o WFS |
| 4 | IBAMA autos de infração | CSV | Bug portal | CSV retorna 4 linhas. Alternativa? BasedosDados? LAI? |
| 5 | IBAMA SISCOM polígonos | SHP | Manual | Navegação manual no SISCOM para baixar SHP |
| 6 | ICMBio UCs | SHP | DNS Docker | Download manual do SHP. ogr2ogr para PostGIS |
| 7 | ANA outorgas de água | CSV/WFS | URL desconhecida | Navegar dadosabertos.ana.gov.br para encontrar |
| 8 | ANA bacias hidrográficas | SHP | Não iniciado | Download simples disponível |
| 9 | INCRA SIGEF | WFS | DNS Docker | Testar i3geo alternativo fora do container |
| 10 | INCRA Assentamentos | SHP/CSV | Não iniciado | URL conhecida, baixar e importar |
| 11 | INCRA Quilombolas | SHP | Não iniciado | INCRA + Fundação Palmares |
| 12 | ANM/SIGMINE processos | ArcGIS REST | Não iniciado | URL funciona, criar ETL |
| 13 | DataJud/CNJ processos | Elasticsearch | Chave pendente | API gratuita, testar sem chave primeiro |
| 14 | BCB SICOR | OData | 503 Manutenção | Tentar novamente. Verificar BD como alternativa |
| 15 | MapBiomas Alerta | GraphQL | Conta não criada | Criar conta em plataforma.alerta.mapbiomas.org |
| 16 | MapBiomas Fogo | GEE | Conta GEE | Solicitar conta GEE + implementar query |
| 17 | MapBiomas Solo | GEE | Conta GEE | Maior diferencial vs concorrentes |
| 18 | MapBiomas Água | GEE/Download | Não iniciado | Download GeoTIFF disponível |
| 19 | MapBiomas Degradação | GEE | Não iniciado | Diferencial EUDR |
| 20 | MapBiomas 10m resolução | GEE | Conta GEE | Diferencial exclusivo |
| 21 | CONAB safras | Download | Não iniciado | Área plantada, produção, estimativa |
| 22 | Embrapa GeoInfo solos | WMS/Download | Não iniciado | Aptidão agrícola por imóvel |
| 23 | Embrapa ZARC | API | Não iniciado | Risco climático por cultura/município/ano |
| 24 | BasedosDados CNPJ | BigQuery | GCP_PROJECT_ID | Mais crítico: enriquecimento de dossiê |
| 25 | BasedosDados PAM | BigQuery | GCP_PROJECT_ID | Produção por município |
| 26 | BasedosDados SICOR | BigQuery | GCP_PROJECT_ID | Alternativa ao OData BCB |
| 27 | ONR Matrículas | API/Convênio | Convênio/Custos | Fechar ciclo de propriedade |
| 28 | SERPRO CPF | API paga | Contrato | CPF completo: renda, vínculos |
| 29 | CENPROT Protestos | InfoSimples | Contrato | Protestos cartoriais por CNPJ |
| 30 | CVM FIAGROs | API | Não iniciado | Fundos agro listados na bolsa |

### Código — Pendentes de implementação

| # | Feature | Módulo | Prioridade | Status |
|---|---|---|---|---|
| 1 | Score MCR 2.9 (checklist auditável) | M1 | CRÍTICA | ❌ |
| 2 | Score EUDR (pré/pós-2020) | M1 | CRÍTICA | ❌ |
| 3 | `POST /api/v1/imovel/relatorio` (motor central) | M1 | ALTA | ❌ |
| 4 | Lookup por código CAR no SICAR | M1 | ALTA | ❌ |
| 5 | Análise de sobreposição por polígono (PostGIS) | M1 | ALTA | ❌ |
| 6 | Export PDF WeasyPrint | M1 | ALTA | ❌ |
| 7 | Desenho de polígono no mapa → relatório | M2 | ALTA | ❌ |
| 8 | Timeline deslizante MapBiomas (1985-2023) | M2 | ALTA | ❌ |
| 9 | Login UI — testar fluxo completo | M2 | ALTA | 🔶 |
| 10 | Camada PRODES no mapa | M2 | MEDIA | ❌ |
| 11 | Valuation R$/ha por município | M4 | MEDIA | ❌ |
| 12 | APScheduler cotações 09h/18h | M5 | MEDIA | ❌ |
| 13 | Dashboard bancário (carteira) | M5 | BAIXA | ❌ |
| 14 | Alertas WebSocket em tempo real | M5 | BAIXA | ❌ |

---

## 11. ORDEM RECOMENDADA DE PESQUISA (Roteiro para próximas sessões)

### Semana 1 — Desbloquear fontes críticas
1. **GCP Project** → usuário cria projeto Google Cloud → desbloqueia BasedosDados
2. **MapBiomas Alerta** → criar conta → testar GraphQL → implementar collector
3. **PRODES WFS** → testar e carregar no PostGIS → fundamenta MCR 2.9
4. **DETER completo (800k)** → baixar arquivo completo, não só 50k via WFS

### Semana 2 — Fontes fundiárias
5. **ANA outorgas** → navegar portal manualmente → descobrir URL → ETL
6. **ICMBio UCs** → download manual SHP → importar PostGIS
7. **INCRA Assentamentos** → URL conhecida, baixar e importar
8. **ANM SIGMINE** → URL funciona, criar ETL

### Semana 3 — Score e Relatório (Módulo 1)
9. **Score MCR 2.9** → implementar motor com o que já temos
10. `POST /api/v1/imovel/relatorio` → motor central de análise
11. **DataJud/CNJ** → testar API pública → implementar busca por CPF/CNPJ
12. **Export PDF** → WeasyPrint com template HTML

### Mês 2 — MapBiomas avançado e Valuation
13. **Google Earth Engine** → solicitar conta → querier raster por polígono
14. **MapBiomas Solo** → carbono e aptidão para valuation
15. **Motor de Valuation** → modelo preditivo R$/ha

---

## 12. PLATAFORMAS DE MONITORES MAPBIOMAS (URLs verificadas)

| Monitor | URL | O que monitora |
|---|---|---|
| **Alerta** | `plataforma.alerta.mapbiomas.org` | Alertas de desmatamento validados com laudo |
| **Crédito Rural** | `plataforma.creditorural.mapbiomas.org` | Parcelas de financiamento x desmatamento |
| **Fogo Mensal** | `plataforma.monitorfogo.mapbiomas.org` | Queimadas mensais tempo quase-real |
| **Recuperação** | `plataforma.recuperacao.mapbiomas.org` | Áreas em regeneração de vegetação |
| **Mineração** | `plataforma.monitormineracao.mapbiomas.org` | Garimpo ilegal por satélite |
| **Plataforma principal** | `plataforma.brasil.mapbiomas.org` | Mapa interativo de cobertura e uso |

---

## 13. MERCADO, COTAÇÕES E COMMODITIES — Assessoria Completa

### 13.1 Cotações de Commodities Agrícolas

#### CEPEA/ESALQ (✅ Collector implementado — `cepea.py`)
```
Site: https://www.cepea.esalq.usp.br/br/indicador/
Status: Scraping funcionando (retorna 403 para bots — precisamos headers corretos)
Método: HTML scraping com BeautifulSoup

Commodities implementadas (9):
- Soja (R$/saca 60kg)        - Milho (R$/saca 60kg)
- Boi Gordo (R$/@)            - Café Arábica (R$/saca 60kg)
- Algodão (c/lp)              - Arroz (R$/saca 50kg)
- Trigo (R$/t)                - Açúcar Cristal (R$/saca 50kg)
- Etanol Hidratado (R$/litro)

⚠️ CEPEA bloqueia bots agressivos. Respeitar rate limit (1 req/min).
Alternativa: Notícias Agrícolas tem cotações CEPEA em formato mais acessível.
```

#### Notícias Agrícolas — Cotações (✅ verificado)
```
Portal: https://www.noticiasagricolas.com.br/cotacoes
30+ categorias de cotação verificadas:
  Algodão, Amendoim, Arroz, Boi Gordo, Cacau, Café, Feijão,
  Frango, Frutas, Laranja, Látex, Legumes, Leite, Mandioca,
  Milho, Ovos, Silvicultura, Soja, Sorgo, Suínos, Sucroenergético,
  Trigo, Verduras

Mercado Futuro (CME/B3): Soja, Milho, Trigo
Cotação do Dólar em tempo real
Mercado Físico (Safras & Mercado): cotações por praça regional

Método de acesso: Scraping HTML (sem API pública) ou RSS para notícias
RSS confirmado: https://www.noticiasagricolas.com.br/rss/noticias.xml
```

#### B3 / CME — Mercado Futuro (❌ Pendente)
```
O que falta:
- Cotações de futuros (soja CBOT, milho B3, boi gordo B3, café ICE)
- Contratos em aberto, volume negociado
- Basis regional (diferença entre físico e futuro)

Fontes possíveis:
- B3 Market Data: https://www.b3.com.br/pt_br/market-data-e-indices/
  → API paga para dados em tempo real
- CME Group via Notícias Agrícolas: gráficos futuros já disponíveis
- yfinance (Python): `pip install yfinance` → dados CME gratuitos (delay 15min)
  → SB=F (soja), ZC=F (milho), KC=F (café), LE=F (boi)
- B3 séries históricas: download gratuito de CSV diários
```

#### IBGE SIDRA (✅ Collector implementado — `market_data.py`)
```
API: https://apisidra.ibge.gov.br/values
Status: ✅ Implementado e funcional (sem autenticação)

Tabela 5457 — PAM (Produção Agrícola Municipal):
- Área plantada, colhida, quantidade produzida, rendimento médio
- 4 culturas principais: soja (39), milho (33), café (9), cana (31)
- Dados por município, estado ou Brasil
- Série histórica anual

Outras tabelas importantes:
- Tabela 3939: PPM — Pecuária Municipal (rebanho bovino por município)
- Tabela 1612: LSPA — Safra atual (estimativa em andamento)
- Tabela 5938: Valor da produção agrícola
```

### 13.2 Safras e Produção

#### CONAB — Acompanhamento de Safra (⚠️ Parcial)
```
Portal: https://portaldeinformacoes.conab.gov.br/
Dados: Séries históricas de grãos, cana-de-açúcar, café, algodão

Datasets disponíveis:
- safra-serie-historica-graos.html → área, produção, produtividade por UF
- custos-de-producao.html → custo/ha por cultura e região
- estoques.html → estoques reguladores
- preco-minimo.html → preços mínimos garantidos pelo governo

Formato: Tabelas interativas (JavaScript) — sem API REST
Estratégia: Scraping ou download manual periódico de planilhas
Frequência: Boletins mensais (12 levantamentos/safra)

Collector status: ⚠️ Stub implementado em market_data.py — precisa scraping real
```

#### USDA (❌ Pendente — mas crítico para exportação)
```
APIs gratuitas:
- FAS API: https://apps.fas.usda.gov/opendataweb/api/
  → Dados de comércio exterior agrícola (exportação BR→mundo)
- WASDE Reports: oferta/demanda mundial de grãos
  → Movimenta mercados toda segunda-feira

Por que importa: exportadores que usam AgroJus precisam saber
condições de mercado global para decidir quando vender
```

### 13.3 Indicadores Financeiros e Econômicos

#### BCB SGS API (✅ Collector implementado — `bcb.py`)
```
API: https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados
Status: ✅ Funcional, sem autenticação, testado

Séries implementadas:
- SELIC (série 11)           - Dólar comercial (série 1)
- IPCA (série 433)           - IGP-M (série 189)
- CDI (série 12)             - Poupança (série 25)
- TR (série 226)

Séries a adicionar (relevância agro):
- Preço médio de terra (INCRA/FNP) — verificar se existe no SGS
- Crédito rural liberado (série 20633)
- Índice de preços recebidos pelo produtor (série 19)
```

---

## 14. NOTÍCIAS E INTELIGÊNCIA — Cobertura Editorial

### NewsAggregator (✅ Implementado — `news_aggregator.py`)
```
Fontes RSS ativas (5):
1. Agrolink:             https://www.agrolink.com.br/rss/noticias.xml
2. Canal Rural:          https://www.canalrural.com.br/feed/
3. Notícias Agrícolas:   https://www.noticiasagricolas.com.br/rss/noticias.xml
4. Embrapa:              https://www.embrapa.br/rss/ultimas-noticias.xml
5. Portal do Agronegócio: https://www.portaldoagronegocio.com.br/feed

Classificação automática por keywords:
- "jurídico": legislação, embargo, multa, IBAMA, código florestal...
- "mercado": cotação, preço, safra, commodities, B3...
- "geral": tudo o resto
```

### Agrolink — Análise Profunda (verificado 15/04/2026)

**Portal:** `https://www.agrolink.com.br/`
**RSS (já no collector):** `https://www.agrolink.com.br/rss/noticias.xml`

A Agrolink é MUITO mais rica do que apenas notícias. É um ecossistema completo:

#### Cotações estruturadas por categoria (URLs verificadas)
```
GRÃOS (com subdivisão por praça):
- Arroz:   agrolink.com.br/cotacoes/graos/arroz/
- Feijão:  agrolink.com.br/cotacoes/graos/feijao/
- Café:    agrolink.com.br/cotacoes/graos/cafe/
- Milho:   agrolink.com.br/cotacoes/graos/milho/
- Soja:    agrolink.com.br/cotacoes/graos/soja/
- Trigo:   agrolink.com.br/cotacoes/graos/trigo/

CARNES (6 espécies):
- Aves:     agrolink.com.br/cotacoes/carnes/aves/
- Bovinos:  agrolink.com.br/cotacoes/carnes/bovinos/
- Bubalinos: agrolink.com.br/cotacoes/carnes/bubalinos/
- Caprinos: agrolink.com.br/cotacoes/carnes/caprinos/
- Ovinos:   agrolink.com.br/cotacoes/carnes/ovinos/
- Suínos:   agrolink.com.br/cotacoes/carnes/suinos/

DIVERSOS:
- Algodão:  agrolink.com.br/cotacoes/diversos/algodao/
- Alho:     agrolink.com.br/cotacoes/diversos/alho/
- Batata:   agrolink.com.br/cotacoes/diversos/batata/
- Cana:     agrolink.com.br/cotacoes/diversos/cana/
- Leite:    agrolink.com.br/cotacoes/diversos/leite/
- Mandioca: agrolink.com.br/cotacoes/diversos/mandioca/

HORTALIÇAS + CEASAS:
- Hortaliças: agrolink.com.br/cotacoes/hortalicas/
- Ceasas:     agrolink.com.br/cotacoes/ceasa/busca

ANÁLISES DE MERCADO:
- agrolink.com.br/cotacoes/analise/lista/
```

#### Ferramentas exclusivas Agrolink
```
1. AGROTEMPO — Previsão do tempo agro
   URL: agrolink.com.br/agrotempo/
   O que tem: Previsão por região agrícola, mapas de chuva, temperatura
   → Complementa NASA POWER com dados mais "user-friendly"

2. AGROLINKFITO — Base de defensivos agrícolas
   URL: agrolink.com.br/agrolinkfito/
   O que tem: Base completa de agrotóxicos registrados, bulas, doses
   → Relevância: compliance de uso correto de defensivos

3. BIOLÓGICOS — Defensivos biológicos
   URL: agrolink.com.br/biologicos/
   → ESG: agricultor que usa biológicos = perfil mais sustentável

4. FERTILIZANTES — Preços e informações
   URL: agrolink.com.br/fertilizantes/
   → Custo de produção: preço NPK impacta margem do produtor

5. CARBONO — Mercado de carbono
   URL: agrolink.com.br/carbono/
   → Relevância para valuation: potencial de créditos de carbono

6. SEMENTES — Tecnologias e preços
   URL: agrolink.com.br/sementes/
   → Custo de produção e estimativa de produtividade

7. CLASSIFICADOS — Máquinas e insumos
   URL: agrolink.com.br/classificados/
   → Termômetro de mercado de máquinas usadas

8. A VOZ DO MERCADO — Opinião de analistas
   URL: agrolink.com.br/avozdomercado/
   → Inteligência de mercado de especialistas

9. CONVERSOR DE UNIDADES
   URL: agrolink.com.br/conversao/
   → Útil para API: converter sacas→kg→tons, alqueires→hectares

10. REGIONAL — Conteúdo por estado/região
    URL: agrolink.com.br/regional/
    → Segmentação geográfica de informações
```

#### Seções AGRO por cultura (conteúdo técnico)
```
Culturas com páginas dedicadas:
- Algodão, Arroz, Café, Cana-de-Açúcar, Feijão,
  Hortifruti, Milho, Soja, Trigo + "Outros"

Pecuária com subdivisões:
- Aves, Bovinos, Ovinos, Suínos + "Outros"

Cada cultura tem: notícias, cotações, problemas/pragas, 
sementes, pós-colheita específicos
```

#### Estratégia de integração Agrolink no AgroJus
```
Nível 1 (já feito): RSS de notícias
Nível 2 (próximo): Scraping de cotações por cultura + praça
Nível 3 (futuro): Integrar Agrotempo no painel de clima
Nível 4 (diferencial): Cruzar cotação regional com MapBiomas
  → "Esta região plantou soja, preço atual R$X/saca, estimativa
     de produção Y toneladas, valor estimado R$ Z"
```

### Notícias Agrícolas — Cobertura temática verificada
```
Categorias editoriais confirmadas (25+ temas):
  Agronegócio, Algodão, Biocombustível, Boi, Café, Carnes, Clima,
  Código Florestal, Feijão/Grãos, Flores, Frango, Grãos, Hortifruti,
  Jurídico, Laranja/Citrus, Leite, Logística, Máquinas/Tech,
  Meio Ambiente, Milho, Petróleo, Política Agrícola, Política/Economia,
  Questões Indígenas, Segurança no Agro, Soja, Sucroenergético,
  Trigo, USDA

De alta relevância para AgroJus:
  - "Jurídico" → alertas de mudanças regulatórias
  - "Código Florestal" → impacto direto na compliance
  - "Clima" → risco climático por região
  - "Questões Indígenas" → risco fundiário
  - "Meio Ambiente" → embargos, autuações, EUDR
```

### Fontes a adicionar no futuro
```
- AgFeed: https://agfeed.com.br/feed/ (fintech agro, FIAGROs)
- Reuters Agro: feeds pagos, mas os melhores para mercado internacional
- Valor Econômico Agro: https://valor.globo.com/agronegocios/rss.xml
- Globo Rural: https://revistapesquisa.fapesp.br/feed/ (pesquisa agro)
- Diário Oficial da União: alertas de decretos e portarias agro
  → API: https://www.in.gov.br/servicos/diario-oficial-da-uniao
```

---

## 15. CLIMA E DADOS METEOROLÓGICOS — Risco Climático

### NASA POWER API (✅ Gratuita, verificada)
```
API: https://power.larc.nasa.gov/api/temporal/
Endpoint: daily, monthly, climatology
Parâmetros: lat/lon → dados meteorológicos para qualquer ponto do Brasil

Variáveis disponíveis para agro:
- T2M: temperatura a 2m (°C)
- PRECTOTCORR: precipitação total (mm/dia)
- RH2M: umidade relativa (%)
- ALLSKY_SFC_SW_DWN: radiação solar (W/m²)
- WS2M: velocidade do vento a 2m (m/s)
- GWETROOT: umidade do solo na zona de raízes (fração)

Exemplo de chamada:
GET https://power.larc.nasa.gov/api/temporal/daily/point?
  parameters=T2M,PRECTOTCORR,RH2M&
  community=AG&
  longitude=-47.93&latitude=-15.78&
  start=20240101&end=20241231&
  format=JSON

Por que é ESSENCIAL:
- Histórico climático por coordenada (40+ anos) → risco de seca/geada
- Sem limite de uso, sem autenticação
- Complementa MapBiomas Atmosfera (que é mais visual/raster)
- Calcula balanço hídrico, evapotranspiração potencial, graus-dia

Status: ❌ Collector não implementado — prioridade ALTA
```

### INMET — Estações Meteorológicas (❌ Pendente)
```
API: https://apitempo.inmet.gov.br/
Endpoints:
- /estacao/dados/{data} → dados diários por estação
- /estacao → lista de todas as estações automáticas (890+)
- /previsao/{codigoCidade} → previsão 5 dias

Por que usar junto com NASA POWER:
- NASA POWER: dados reanálise satellite (cobre todo Brasil, inclusive interior)
- INMET: dados de estação (mais preciso onde existe estação)
- Cruzamento dos dois: validação de qualidade
```

### MapBiomas Atmosfera (✅ GEE Assets documentados — seção 13)
```
Já documentado acima:
- Temperatura (anual, mensal, anomalia)
- Precipitação (anual, mensal, anomalia)
- Pressão de vapor (estresse hídrico)
- Qualidade do ar (PM10, PM2.5) — relevante para incêndios

Diferencial: dados RASTER → servem para visualização no mapa, não para
consulta pontual. Para consulta pontual, usar NASA POWER.
```

### Embrapa ZARC — Zoneamento Agrícola de Risco Climático (❌ Pendente)
```
O que é: Define quais culturas podem ser plantadas em cada município
por decêndio (10 dias), e qual o risco de perda por seca/geada/excesso.

Dados: https://indicadores.agricultura.gov.br/zarc/index.htm
API: Verificar se existe API ou se é download manual

Por que é ENORME para compliance bancária:
- Banco Central EXIGE ZARC para liberar crédito de custeio
- Plantio fora do ZARC = seguro não cobre → banco não financia
- AgroJus pode alertar: "Esta cultura neste município neste período
  está FORA do ZARC — risco de não cobertura pelo PROAGRO"
```

---

## 16. COMPARAÇÃO COMPETITIVA — Cobertura de Dados

### O que cada concorrente oferece vs AgroJus

| Dimensão | Agrosatélite | Agrotools | Terras/FNP | AgroJus (meta) |
|---|---|---|---|---|
| **Mapa LULC** | ✅ Próprio | ✅ MapBiomas | ❌ | ✅ MapBiomas Col.10 |
| **Resolução 10m** | ✅ Pago | ❌ | ❌ | ✅ MapBiomas 10m (grátis) |
| **Desmatamento DETER** | ✅ | ✅ | ❌ | ✅ 50k no PostGIS |
| **Desmatamento PRODES** | ✅ | ✅ | ❌ | ⚠️ Pendente |
| **Alertas MapBiomas** | ❌ | ❌ | ❌ | ⚠️ Pendente (GraphQL) |
| **MCR 2.9 Score** | ❌ | ✅ | ❌ | ⚠️ Motor a implementar |
| **EUDR Compliance** | ✅ Pago | ❌ | ❌ | ⚠️ Diferencial |
| **Embargos IBAMA** | ❌ | ✅ | ❌ | ✅ 103k no PostGIS |
| **Trabalho escravo** | ❌ | ❌ | ❌ | ✅ 614 no PostGIS |
| **Crédito rural BCB** | ❌ | ❌ | ❌ | ✅ 5.6M parcelas PostGIS |
| **Fogo histórico** | ✅ | ❌ | ❌ | ⚠️ GEE pendente |
| **Degradação (EUDR)** | ❌ | ❌ | ❌ | ⚠️ Diferencial exclusivo |
| **Solo (carbono)** | ❌ | ❌ | ❌ | ⚠️ Diferencial exclusivo |
| **Cotações CEPEA** | ❌ | ❌ | ✅ FNP | ✅ Collector pronto |
| **Indicadores BCB** | ❌ | ❌ | ❌ | ✅ API funcionando |
| **Notícias agro** | ❌ | ❌ | ❌ | ✅ 5 feeds RSS |
| **Clima por coordenada** | ❌ | ❌ | ❌ | ⚠️ NASA POWER pendente |
| **ZARC risco agrícola** | ❌ | ❌ | ❌ | ⚠️ Pendente |
| **Produção municipal** | ❌ | ❌ | ✅ | ✅ SIDRA implementado |
| **CNPJ/Sócios** | ❌ | ❌ | ❌ | ⚠️ BasedosDados (GCP) |
| **Valuation R$/ha** | ❌ | ❌ | ✅ FNP (pago) | ⚠️ Modelo pendente |
| **PDF Relatório** | ✅ PDF | ✅ PDF | ✅ PDF | ⚠️ WeasyPrint pendente |
| **API pública** | ❌ | ✅ B2B | ❌ | ✅ FastAPI pronta |

### Análise dos gaps

**Onde somos ÚNICOS (nenhum concorrente tem):**
- MapBiomas Degradação + Solo + Atmosfera combinados
- Crédito rural BCB (5.6M parcelas) cruzado com desmatamento
- Trabalho escravo MTE integrado com geolocalização
- Cotações CEPEA + notícias + compliance em UMA plataforma
- API REST aberta (concorrentes vendem B2B fechado)

**Onde estamos ATRÁS e precisa priorizar:**
1. ❌ Motor MCR 2.9 (Agrotools já tem)
2. ❌ EUDR compliance automatizado (Agrosatélite já tem)
3. ❌ PRODES (dado oficial de desmatamento — temos só DETER)
4. ❌ Export PDF profissional
5. ❌ Valuation R$/ha (Terras/FNP tem modelo proprietário)

**Onde estamos IGUAIS:**
- Mapa LULC MapBiomas (mesma fonte que Agrotools)
- DETER alertas (mesma fonte que todos)
- Embargos IBAMA (dados públicos)

### O que nenhum concorrente faz e nós vamos fazer:

```
1. ASSESSORIA COMPLETA EM UM PAINEL:
   - Compliance (MCR 2.9, EUDR) + Mercado (cotações, safra) + 
     Notícias (feeds jurídicos/regulatórios) + Clima (NASA POWER) +
     Financeiro (BCB, SELIC, dólar) + Fundiário (INCRA, ONR)

2. HISTÓRICO DE 38 ANOS POR PIXEL:
   MapBiomas Col.10 (1985-2023) = prova documental irrefutável

3. INTELIGÊNCIA CRUZADA:
   - Embargo IBAMA + polígono de financiamento BCB = "banco financiou desmatado?"
   - Solo + clima + cobertura = valuation automatizado com fundamento científico
   - Trabalho escravo + CNPJ + município = due diligence social automática

4. API ABERTA:
   POST /api/v1/imovel/relatorio → qualquer sistema integra
   GET /api/v1/cotacoes → cotações CEPEA em JSON
   GET /api/v1/noticias → feed classificado por relevância jurídica
```

---

*AgroJus — Pesquisa de Fontes de Dados v3.0 — 2026-04-15*
*Assessoria completa: Compliance + Mercado + Notícias + Clima + Financeiro*
*Atualizado com URLs verificados dos sites oficiais*
*Este documento deve ser revisado e expandido a cada sessão de pesquisa*
