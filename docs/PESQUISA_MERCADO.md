# PESQUISA DE MERCADO v3.0 — RESUMO EXECUTIVO

> **Pesquisa completa: 7 agentes em paralelo, 15/04/2026**
> Substitui: ANALISE_COMPETITIVA_v2_COMPLETA.md (que manteve apenas concorrentes)
> Esta versao adiciona: como cada um entrega, precos reais, fontes de dados, leiloes, BCB/SISBACEN, BasedosDados, InfoSimples, necessidades do publico

---

## NUMEROS DO MERCADO

| Metrica | Valor | Fonte |
|---|---|---|
| Plano Safra 2025/26 | **R$ 516,2 bilhoes** (maior da historia) | MAPA |
| Leiloes rurais monitorados 2025 | **R$ 420 bilhoes** (1a praca) | SPY Leiloes |
| Imoveis rurais em leilao (snapshot) | **~1.900 ativos** a qualquer momento | Portal Leilao Imovel |
| Desconto medio leilao vs avaliacao | **37,3%** | Mercado 2025 |
| Preco medio terra Brasil | **R$ 22.951,94/ha** (+28,36% em 2 anos) | SIMET/INCRA 2024 |
| Processos IBAMA pendentes | **183.000** (R$ 29 bilhoes) | IBAMA dados abertos |
| IBAMA arrecada das multas | **apenas ~5%** | Dados publicos |
| Due diligence manual hoje | **R$ 5.000-30.000, 15-45 dias** | Mercado |
| Propriedades com passivos ocultos | **40%+** | Pesquisa fundiaria |
| Cooperativas de credito (canal) | **750 cooperativas, 10k+ agencias** | Sistema cooperativista |

---

## CONCORRENTES — COMO ENTREGAM E QUANTO COBRAM

### Precos Reais Confirmados

| Empresa | Modelo | Preco confirmado |
|---|---|---|
| **AdvLabs** | Assinatura anual + creditos | R$ 997/ano (basico) a R$ 4.997/ano (avancado) |
| **Registro Rural** | Assinatura + API por consulta | R$ 149,90/mes PRO; R$ 2,50/consulta CAR avulsa |
| **SpotSat Digital** | Pacotes de consultas | R$ 6/consulta desmatamento; R$ 10-25/consulta ESG |
| **Docket** | Freemium + assinatura | Gratis (IA basica) a R$ 150.000/mes (enterprise) |
| **Agrotools** | Enterprise B2B | ~R$ 50.000+/mes estimado |
| **Serasa Agro** | Enterprise B2B | ~R$ 15-50/consulta Farm Check estimado |
| **Softfocus** | Enterprise bancos | Nao publico (33% dos bancos BR usam) |
| **Chaozao** | Marketplace (anunciante paga) | Gratis p/ comprador; semestral/anual p/ anunciante |
| **RELAND** | Success fee | Comissao 6% na venda |

### O que Cada Um Faz que Nos Podemos Replicar

| Feature | Quem faz | Replicavel? | Como |
|---|---|---|---|
| Radar autos IBAMA por raio geografico | AdvLabs | **SIM** | Dados IBAMA publicos + geocodificacao |
| Calculadora prescricao ambiental | AdvLabs | **SIM** | Regras juridicas codificaveis |
| Consulta consolidada CAR+SNCR+SIGEF | Registro Rural | **SIM** | APIs publicas + InfoSimples |
| Score 0-1000 gauge visual | Serasa Agro | **SIM** | Componente UI + motor proprio |
| Compliance desmatamento por imovel | SpotSat (R$6!) | **SIM, custo zero** | PRODES e publico e gratuito |
| OCR de matriculas de imoveis | Docket/AgRisk | **SIM** | LLM + pdfplumber |
| 54 validacoes credito rural | Softfocus | **PARCIAL** | Socioambientais sim; SICOR/BNDES requer credenciamento |
| Monitoramento SEI/IBAMA | AdvLabs | **SIM** | Scraping portais publicos |
| WhatsApp como canal | Agrolend/DadosFazenda | **SIM** | WhatsApp Business API (~R$ 0,25/msg) |

---

## FONTES DE DADOS — MAPA COMPLETO

### Gratis e Imediatas

| Fonte | Acesso | Dados |
|---|---|---|
| **BasedosDados** (60+ tabelas) | BigQuery (1TB/mes gratis) | SICOR, CNPJ, PAM, PPM, PRODES, CAFIR, RAIS, CAGED, MapBiomas, BDMEP |
| **agrobr** (39 fontes) | `pip install agrobr` | CEPEA, CONAB, IBGE, BCB, B3, USDA, NASA, MapBiomas — **NOTA: testado em sessoes anteriores, tem limitacoes praticas. Usar como fallback, nao como camada primaria** |
| **BCB SGS** (600+ series) | API REST sem auth | SELIC, TR, IPCA, TJLP, TLP, cambio, inadimplencia |
| **BCB SICOR OData** (17 endpoints) | API REST sem auth | Credito rural por municipio/programa/produto |
| **Portal Transparencia** | API REST (token gratis) | CEIS, CNEP, Garantia-Safra, Seguro Defeso |
| **DataJud/CNJ** | API key publica | 88 tribunais, processos judiciais |
| **IBGE SIDRA** | API REST sem auth | PAM (tabela 5457), PPM (3939), Censo Agro |
| **CVM CKAN** | API REST sem auth | FIAGRO informes, CRA informes |
| **MapBiomas Alerta GraphQL** | Bearer token (cadastro gratis) | Alertas desmatamento por CAR |
| **Embrapa AgroAPI** | OAuth (1k req/mes gratis) | ZARC, ClimAPI, SATVeg, AGROFIT |
| **NASA POWER** | API REST sem auth | Clima por coordenada desde 1981 |

### Pagas (custo baixo, alto valor)

| Fonte | Custo | Dados exclusivos |
|---|---|---|
| **InfoSimples** | ~R$ 1.010/mes (5k consultas) | IBAMA certidoes, SIGEF detalhes, CAR shapefile, matriculas ARISP, CENPROT protestos, PGFN |
| **BigDataCorp** | ~R$ 200-500/mes | Dados ambientais pre-processados (R$ 0,05/consulta com 500 gratis) |
| **SERPRO** | ~R$ 200/mes | CCIR oficial, CPF/CNPJ direto Receita |

### Descobertas Importantes

1. **Nao existe API de cadeia dominial automatica em lugar nenhum** — oportunidade para IA/LLM
2. **Nao existe API publica de preco de terras rurais** — oportunidade para AgroJus criar a primeira base integrando SIMET + VTN + precos de anuncio + precos de leilao
3. **PRONAF e PRONAMP nao sao datasets separados** — estao dentro do SICOR, campo programa/subprograma
4. **agrobr tem MCP server** (agrobr-mcp) que integra com Claude diretamente — 10 tools prontas
5. **CAFIR** (Receita Federal) esta no BigQuery — cross-reference com CAR/SIGEF para validacao fundiaria

---

## LEILOES RURAIS — OPORTUNIDADE NOVA

### Mercado
- ~275.000 imoveis leiloados em 2024 (+86% vs 2023)
- R$ 420 bilhoes em 1a praca monitorados 2025
- ~1.900 rurais ativos a qualquer momento
- 73% extrajudiciais, 27% judiciais

### Sites Mapeados (30+)

**Marketplaces rurais:** Chaozao (R$500B listings), RELAND (2.600 props), Fazenda Aberta, MF Rural, Bolsa de Terras, Mercado de Terras, Banco de Terras
**Generalistas:** ImovelWeb (29.500 rurais), ZAP (88.680), OLX, Viva Real
**Agregadores leilao:** Nucleo Leiloes (60k), SPY Leiloes (300k), Portal Leilao Imovel (80k), Spot Leiloes, Mapa do Leilao
**Leiloeiros:** Superbid, Mega Leiloes, Portal Zuk, Sold, Lance Total
**Bancos:** Caixa (21k, Apify scraper pronto!), BB, Bradesco, Itau, Sicredi, Sicoob

### Valor Unico do AgroJus

Nenhum agregador de leiloes faz cruzamento com dados fundiarios. Todos mostram: foto + preco + edital. AgroJus adiciona: CAR + IBAMA + TI/UC + PRODES + DETER + SICOR + SIGEF + MTE = due diligence automatizada em minutos.

### Monetizacao Proposta

| Camada | O que | Preco |
|---|---|---|
| 1. Agregador gratis | Listagem leiloes rurais + busca | Gratis (aquisicao usuarios) |
| 2. Relatorio due diligence | Score 0-1000 + cruzamento 14 camadas | R$ 99-499/relatorio |
| 3. Assinatura profissional | Acesso ilimitado + alertas + API | R$ 299-999/mes |
| 4. API enterprise | Bancos, escritorios, fundos | Por consulta / enterprise |
| 5. Comissao indicacao | Lead qualificado p/ corretor/leiloeiro | 0,5-1% transacao |

---

## SERVICOS FINANCEIROS VIAVEIS

| Servico | Fonte de dados | Viabilidade |
|---|---|---|
| Calculadora saldo devedor taxas reais | BCB SGS (SELIC, TR, IPCA, TJLP) | **ALTA** |
| Simulador alongamento/renegociacao | SGS + MCR + Plano Safra | **ALTA** |
| Comparador taxas entre programas | SICOR OData + Plano Safra | **ALTA** |
| Verificacao elegibilidade PRONAF/PRONAMP | MCR + Plano Safra | **ALTA** |
| Alerta Plano Safra | DOU + MAPA | **ALTA** |
| Score risco do tomador | SICOR + compliance AgroJus | **ALTA** |
| Simulador credito vs CPR | MCR + SGS + CEPEA | **ALTA** |
| Dashboard FIAGRO/CRA | CVM CKAN | **ALTA** |

---

## BASEDEDADOS.ORG — TOP 20 TABELAS PARA AGROJUS

| Prioridade | Dataset | BigQuery ID | Uso |
|---|---|---|---|
| P0 | CNPJ (empresas+socios) | `br_me_cnpj.*` | Due diligence empresarial |
| P0 | SICOR credito rural (11 tabelas) | `br_bcb_sicor.*` | Mapeamento credito, saldo devedor |
| P0 | MapBiomas (9 tabelas) | `br_mapbiomas_estatisticas.*` | Uso solo historico 1985-2021 |
| P0 | Diretorios Brasil (24 tabelas) | `br_bd_diretorios_brasil.*` | Tabela-chave para JOINs |
| P1 | CAFIR (imoveis rurais Receita) | `br_rf_cafir.*` | Cadastro fundiario fiscal |
| P1 | PRODES desmatamento | `br_inpe_prodes.*` | Desmatamento por municipio |
| P1 | CAR/SICAR | `br_sfb_sicar.*` | Regularidade ambiental |
| P1 | PAM producao agricola | `br_ibge_pam.*` | Producao por municipio |
| P1 | PPM pecuaria | `br_ibge_ppm.*` | Rebanhos por municipio |
| P1 | RAIS emprego formal | `br_me_rais.*` | Emprego agro por municipio |
| P2 | BDMEP meteorologia | `br_inmet_bdmep.*` | Comprovacao eventos climaticos |
| P2 | SEEG emissoes | `br_seeg_emissoes.*` | ESG scoring, carbono |
| P2 | geobr geometrias | `br_ipea_geobr.*` | Shapefiles oficiais |
| P2 | SICONFI financas publicas | `br_me_siconfi.*` | Orcamento municipal |
| P2 | IPCA inflacao | `br_ibge_ipca.*` | Correcao monetaria |
| P2 | CAGED emprego mensal | `br_me_caged.*` | Dinamica emprego rural |
| P3 | Censo Agropecuario | `br_ibge_censo_agropecuario.*` | Referencia decenal |
| P3 | PIB municipios | `br_ibge_pib.*` | Economia municipal |
| P3 | DOU | `br_imprensa_nacional_dou.*` | Monitoramento normativo |
| P3 | S2ID desastres | dataset S2ID | Defesa inadimplencia rural |

---

## 10 GAPS DE MERCADO CONFIRMADOS (NINGUEM ATENDE)

1. **Integracao juridica + geoespacial** — AdvLabs tem teses sem mapa; Agrotools tem mapa sem teses
2. **Jurimetria ambiental** — % exito por tese/tribunal/tipo infracao. NINGUEM faz
3. **Score unificado 5 eixos** — Serasa faz 1 eixo financeiro. NINGUEM faz 5
4. **Due diligence automatizada** — R$ 5-30k / 15-45 dias → AgroJus faz em minutos
5. **Compliance multi-regulatorio** — MCR 2.9 + EUDR + certificacoes na mesma plataforma
6. **Self-service para produtor** — "Minha fazenda esta apta?" Agrotools e R$ 50k/mes
7. **Cadeia dominial sobre mapa** — Serasa tem cadeia sem mapa. GIS tem mapa sem cadeia
8. **Monitoramento integrado** — admin (IBAMA) + judicial (DataJud) + DOU num unico painel
9. **Recuperacao credito rural + analise juridica de divida** — R$ 60 bi em securitizacao no Senado
10. **Base de precos de terras rurais** — NENHUMA API publica existe. AgroJus pode ser a primeira

---

## ARQUITETURA RECOMENDADA PARA INTEGRACAO

```
APIs diretas (BCB SGS, SICOR OData, DataJud, BrasilAPI) ──→ Dados em tempo real
BigQuery (BasedosDados) ──────────────────────────────────→ 60+ tabelas SQL (SICOR, CNPJ, PAM, PRODES, etc.)
InfoSimples API ──────────────────────────────────────────→ IBAMA certidoes, SIGEF, matriculas, protestos
MapBiomas GraphQL ────────────────────────────────────────→ Alertas desmatamento por CAR
Portal Transparencia API ─────────────────────────────────→ CEIS, CNEP, Garantia-Safra
CVM CKAN ─────────────────────────────────────────────────→ FIAGRO, CRA
SICAR WFS + INPE WFS ────────────────────────────────────→ CAR poligonos, DETER, PRODES
Earth Engine ─────────────────────────────────────────────→ LULC, fogo, solo, agua
Apify scrapers ───────────────────────────────────────────→ Leiloes Caixa + Portal Leilao Imovel
Scripts ETL proprios (pdfplumber, httpx, geopandas) ──────→ CONAB, CEPEA, IBGE, Lista Suja MTE, ANM
           ↓
    [PostGIS 60 tabelas + 10.7M registros]
           ↓
    [FastAPI endpoints (42+)]
           ↓
    [Frontend Next.js + WhatsApp Bot (futuro)]
```

**NOTA:** agrobr pode ser util como fallback/referencia, mas as sessoes anteriores mostraram limitacoes praticas. A camada primaria de dados e composta por APIs diretas + BigQuery + ETL proprio + InfoSimples.

---

## POSICIONAMENTO FINAL

**"O compliance do exportador brasileiro que fala tanto com Bruxelas quanto com o Banco Central — e ainda defende quando o IBAMA bate na porta."**

**Moat:** Nenhuma empresa no mundo integra juridico + geoespacial + credito + valuation para imoveis rurais brasileiros. Confirmado em 100+ empresas pesquisadas globalmente, incluindo unicornios e big techs agro.

**Timing:** MCR 2.9 obrigatorio este mes. EUDR enforcement dez/2026. Dois regulamentos obrigatorios convergindo = demanda garantida.

**Canal:** Cooperativas (750, 10k+ agencias) + leiloes rurais (1.900 ativos, R$ 420 bi) como porta de entrada.

---

*AgroJus — Pesquisa de Mercado v3.0 — 7 agentes — 15/04/2026*
*Relatórios detalhados salvos separadamente para cada eixo de pesquisa*
