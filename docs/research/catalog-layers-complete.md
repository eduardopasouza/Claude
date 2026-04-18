# Catálogo Completo de Camadas do AgroJus

**Total declarado:** 105 camadas organizadas em 23 temas
**Data:** 2026-04-17 (v2 — removido tema "Cartório (ONR)")
**Arquivo fonte:** `frontend_v2/src/lib/layers-catalog.ts`

> **Correção v2:** tema "Cartório (ONR)" foi removido. Matrículas e cadeia dominial **não são camadas geoespaciais de acesso público** — exigem pagamento por consulta ou upload do PDF pelo próprio usuário. Tratamento correto em: `docs/research/cadeia-dominial-acesso-real.md` + ficha do imóvel `/imoveis/[car]` aba "Cadeia Dominial" (upload PDF / texto colado / consulta paga InfoSimples).

## Resumo por tema

| Tema | Camadas | Status dos dados |
|---|---|---|
| **Fundiário** | 10 | 5 ativas (SICAR, CAR, SIGEF, TIs), 5 stubs (SNCI, quilombolas, assentamentos, SPU, faixa fronteira, glebas) |
| **Ambiental** | 8 | 3 ativas (UCs federais, embargos/autos ICMBio), 5 stubs (UCs estaduais, embargos IBAMA pontos, CTF IBAMA, ZEE, biomas) |
| **Desmatamento** | 5 | 4 ativas (PRODES, DETER A/C, MapBiomas Alertas), 1 stub (MapBiomas Desmat Acumulado GEE) |
| **Fogo** | 4 | Todas stubs (GEE + BDQueimadas) |
| **Vegetação Secundária** | 3 | Todas stubs (MapBiomas Recuperação + PRAD) |
| **Degradação Florestal** | 3 | Todas stubs (MapBiomas Degradação) |
| **Agricultura** | 8 | Todas stubs (MapBiomas Agricultura por cultura específica) |
| **Pastagem & Pecuária** | 4 | Todas stubs (MapBiomas Pastagem) |
| **Água & Hidrografia** | 5 | Todas stubs (ANA BHO/outorgas/HidroWeb, Atlas Irrigação, MapBiomas Água) |
| **Solo & Aptidão** | 5 | Todas stubs (Embrapa SmartSolos, IBGE Pedologia, MapBiomas Solo) |
| **Mineração** | 3 | Todas stubs (SIGMINE + MapBiomas) |
| **Logística/Infraestrutura** | 9 | 5 ativas (rodovias federais, ferrovias, portos, armazéns, frigoríficos), 4 stubs (rodovias estaduais, aeroportos, terminais, CNT) |
| **Energia** | 3 | Todas stubs (ANEEL usinas/LTs/subestações) |
| **Crédito & Finanças** | 3 | 1 ativa (MapBiomas Crédito Rural), 2 stubs (SICOR choropleth, Garantia-Safra) |
| **Produção Agrícola IBGE (PAM)** | 6 | Todas stubs choropleth — soja/milho/cana/café/algodão/valor |
| **Pecuária IBGE (PPM)** | 4 | Todas stubs choropleth — bovino/ovino/suíno/leite |
| **Socioeconômico** | 5 | Todas stubs — IDHM, PIB, população 2022, REGIC, CNES |
| **Clima** | 4 | Todas stubs — INMET, NASA POWER, CHIRPS, ZARC |
| **Atmosfera (MapBiomas)** | 3 | Todas stubs — temperatura, precipitação, qualidade do ar |
| **Risco Climático (MapBiomas)** | 3 | Todas stubs — deslizamento, inundação, segurança hídrica |
| **Urbano** | 3 | Todas stubs — MapBiomas urbanização, limites IBGE |
| **Jurídico Georreferenciado** | 3 | Todas stubs — autos IBAMA pontos, DataJud choropleth, DJEN por OAB |
| **Fiscal / Compliance** | 4 | Todas stubs — CEIS, CNEP, Lista Suja MTE pontos, CNDT por UF |

**Totais:**
- ✅ **17 camadas com dados reais no PostGIS** (renderizam imediatamente no mapa)
- 🕒 **91 camadas declaradas como stubs** (estrutura de UI pronta, dados a integrar por onda)

## Fontes mapeadas (todas cobertas no catálogo)

### Cadastrais / Fundiárias
- SICAR/SFB/MMA ✅
- INCRA SIGEF ✅
- INCRA SNCI legado 🕒
- FUNAI Terras Indígenas ✅
- INCRA/Palmares Quilombolas 🕒
- INCRA Assentamentos 🕒
- SPU Terras União 🕒
- IBGE Faixa Fronteira 🕒
- INCRA Glebas Federais 🕒
- ONR Matrículas 🕒
- ONR Cadeia Dominial 🕒
- ONR Averbações 🕒

### Ambientais
- ICMBio UCs Federais ✅
- SEMAS Estaduais UCs 🕒
- ICMBio Embargos ✅
- ICMBio Autos ✅
- IBAMA dados abertos (embargos) 🕒
- IBAMA CTF/APP 🕒
- MapBiomas Alerta ✅
- INPE PRODES ✅
- INPE DETER Amazônia ✅
- INPE DETER Cerrado ✅
- INPE BDQueimadas 🕒
- Governos estaduais ZEE 🕒
- IBGE Biomas 🕒

### MapBiomas Coleção 10 (via Earth Engine)
- Cobertura LULC (34 classes) 🕒
- Desmatamento acumulado 🕒
- Fogo anual/mensal/frequência 🕒
- Vegetação secundária anual/idade 🕒
- Degradação (borda, fragmento, freq. fogo) 🕒
- Agricultura (soja, milho, cana, café, algodão, arroz, irrigação, 2ª safra) 🕒
- Pastagem (vigor, idade, biomassa, transição) 🕒
- Água anual/mensal 🕒
- Solo (carbono, textura) 🕒
- Mineração (industrial, garimpo) 🕒
- Urbano anual 🕒
- Atmosfera (temperatura, precipitação, qualidade ar) 🕒
- Risco climático (deslizamento, inundação, segurança hídrica) 🕒

### Hidrografia
- ANA BHO Ottocodificada 🕒
- ANA Outorgas 🕒
- ANA HidroWeb estações 🕒
- ANA Atlas Irrigação 2021 🕒
- CHIRPS via GEE 🕒

### Clima
- INMET estações 🕒
- NASA POWER 🕒
- CHIRPS precipitação 🕒
- Embrapa AgroAPI ZARC ✅ (credencial ativa, falta integrar)
- Embrapa SmartSolos ✅ (credencial ativa)

### Logística
- DNIT rodovias federais ✅
- DERs rodovias estaduais 🕒
- ANTT/DNIT ferrovias ✅
- ANTAQ portos ✅
- ANAC aeroportos 🕒
- ANTT/ANTAQ terminais 🕒
- CONAB SICARM armazéns ✅
- MAPA SIF frigoríficos ✅
- CNT rodovias condição 🕒

### Energia
- ANEEL usinas 🕒
- ONS/ANEEL linhas transmissão 🕒
- ANEEL subestações 🕒

### Crédito
- BCB SICOR OData ✅ (stub choropleth, endpoint existe)
- MapBiomas Crédito Rural (parcelas) ✅
- Portal Transparência Garantia-Safra ✅ (token ativo)

### IBGE (dados quantitativos por município → choropleth)
- IBGE SIDRA PAM 5457 (soja, milho, cana, café, algodão, arroz, valor) ✅
- IBGE SIDRA PPM 3939 (bovino, bubalino, ovino, suíno, leite, ovos) ✅
- IBGE Censo Agropecuário 2017 ✅
- IBGE PIB Municipal 5938 ✅
- IBGE Censo Demográfico 2022 ✅
- IBGE REGIC 2018 🕒
- IBGE Pedologia 🕒
- PNUD/IPEA/FJP IDHM 🕒
- DataSUS CNES estabelecimentos 🕒

### Jurídico
- CNJ DataJud (88 tribunais) ✅
- CNJ DJEN/Comunica.PJe ✅ (DJEN integrado — 42 publicações de Eduardo)
- STJ Dados Abertos ✅ (planejado onda 2 backend)
- TCU webservice ✅ (planejado)
- LexML legislação 🕒

### Fiscal
- MTE Lista Suja ✅
- Portal Transparência CEIS/CNEP ✅ (token ativo)
- TST CNDT 🕒
- PGFN Dívida Ativa 🕒
- SERPRO CCIR 🕒 (serviço pago)

### Mercado
- CEPEA/ESALQ ✅ (planejado)
- CONAB safras/custos ✅ (planejado)
- BCB SGS indicadores ✅
- USDA PSD 🕒
- CVM FIAGRO 🕒

## Por onde começar ativando stubs (prioridade estratégica)

### Prioridade ALTA — dados já disponíveis, só falta integração
1. **IBGE PAM/PPM/Censo choropleth** (13 camadas) — endpoint SIDRA já existe, só criar endpoint que devolve GeoJSON da malha municipal colorida
2. **MapBiomas via GEE** (30+ camadas) — GCP Project `agrojus` já configurado, credenciais MapBiomas ativas
3. **Embrapa AgroAPI** (SmartSolos, ZARC) — credenciais já obtidas
4. **IBGE malhas** (municipal, estadual, REGIC, biomas) — API gratuita sem auth

### Prioridade MÉDIA — precisa construir coletor/scraper
5. **ANA BHO + Outorgas** (ArcGIS REST, sem auth)
6. **SIGMINE** (ArcGIS REST, sem auth)
7. **IBAMA embargos pontos** (CSV dados abertos)
8. **Portal Transparência CEIS/CNEP/Garantia-Safra** (token ativo, REST)
9. **ANEEL usinas/LTs** (APIs públicas)

### Prioridade BAIXA — dependem de parceria/pagamento
10. **ONR matrículas** — sem API pública, precisa convênio ou scraping controlado
11. **SNCI legado** — download manual de shapefile INCRA
12. **SPU Terras União** — download de shapefile
13. **CNT condição rodovias** — dados consolidados sob solicitação
14. **ZEE estaduais** — 9 portais estaduais diferentes (UF × UF)

## Próximos sprints

- **Sprint IBGE-1** (~3 dias): criar endpoint `/api/v1/geo/ibge/choropleth/{layer}/{year}` que retorna GeoJSON da malha municipal com valores agregados para PAM/PPM/PIB/população. Frontend renderiza como choropleth.

- **Sprint MapBiomas-1** (~5 dias): conectar GCP Project, criar endpoint `/api/v1/gee/layer/{layer_id}/tile/{z}/{x}/{y}` que serve tiles PNG via Earth Engine. Integrar no `MapComponent` como `TileLayer` dinâmico.

- **Sprint Coletores-1** (~4 dias): escrever coletores Python para ANA BHO, ANA Outorgas, SIGMINE, IBAMA embargos. Todos com ETL inicial para PostGIS.

- **Sprint Embrapa-1** (~3 dias): coletores OAuth Embrapa para ZARC + SmartSolos. Frontend consulta por coordenada/município.

- **Sprint ONR-1** (~7 dias, depende de convênio): negociar acesso ONR ou implementar InfoSimples (R$ 0,10/consulta).

Total para ativar ~80% das camadas stub: **~22 dias de desenvolvimento backend**.
