# AgroJus — Handoff Sessão 4 (15/04/2026)

> **Cole este arquivo inteiro no início da próxima sessão do Claude Code.**
> É autocontido: não é necessário ler nenhum outro documento primeiro.
> Sessão 4 de ~3h. Resultado: 15 personas mapeadas + decisão estratégica crédito/valuation na Fase 1.

---

## SEÇÃO 1 — CONTEXTO DO PRODUTO

### O que é o AgroJus

AgroJus é uma plataforma SaaS B2B de inteligência fundiária, ambiental, jurídica e financeira para o agronegócio brasileiro. O produto combina mais de 10,7 milhões de registros geoespaciais com análise jurídica especializada — nenhum concorrente faz isso simultaneamente.

### A brecha regulatória (MCR 2.9)

O produto nasceu da **brecha regulatória criada pelas Resoluções CMN 5.267/5.268 de 2025** (MCR 2.9), que obrigam **todo banco do Brasil** a verificar automaticamente conformidade ambiental antes de liberar crédito rural — desde 01/04/2026 para imóveis grandes, a partir de 04/01/2027 para os demais. O BCB já bloqueou mais de R$6 bilhões em operações com irregularidades. Isso cria uma demanda obrigatória, não opcional, para o produto.

### Posicionamento

O AgroJus não compete com GIS puro (Agrotools, SpectraX) nem com jurídico puro (AdvLabs). Ocupa a interseção: dados geoespaciais + inteligência jurídica + crédito rural + valuation — tudo integrado em um único relatório gerado em segundos. O diferencial central é que o sistema não só mostra dados, mas interpreta e diz o que fazer: defesa sugerida, tese aplicável, alongamento viável, valor estimado.

### Stack técnica

```
Backend:    FastAPI + SQLAlchemy + PostGIS (PostgreSQL 15)
Frontend:   Vanilla JS + Vite + Leaflet (frontend_v2/ — problema de renderização pendente)
Infra:      Docker Compose (containers: db + backend)
ETL:        Python scripts (pdfplumber, httpx, geopandas, ogr2ogr)
Branch git: claude/continue-backend-dev-sVLGG
Diretório:  c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus
```

---

## SEÇÃO 2 — ESTADO TÉCNICO ATUAL (pós-sessão 4)

### Backend — Funcional

**Banco de dados:** 59 tabelas PostGIS | ~10,7M+ registros

| Tabela | Registros | Fonte |
|---|---|---|
| `geo_car` | 135.000 CARs | WFS 27 UFs (5k cada) |
| `sicar_completo` | ~72k MA (BigQuery rodando) | BigQuery BasedosDados (79,3M disponíveis) |
| `sigef_parcelas` | 493.913 | Download INCRA direto (6 UFs: MA, MT, PA, GO, TO, MS) |
| `geo_mapbiomas_alertas` | 515.823 | MapBiomas Alerta |
| `mapbiomas_credito_rural` | 5.614.207 | MapBiomas (4,7GB GPKG) |
| `environmental_alerts` | 104.284 | IBAMA + MTE |
| `geo_deter_amazonia` + `geo_deter_cerrado` | 100.000 | DETER (limite WFS — real: 1M+) |
| `geo_prodes` | 50.000 | PRODES (limite WFS) |
| `geo_terras_indigenas` | 655 | FUNAI |
| `geo_unidades_conservacao` | 346 | ICMBio |
| `geo_embargos_icmbio` + `geo_autos_icmbio` | 15.000 | ICMBio |
| `sicor_custeio_uf` | 50.000 | BCB SICOR |
| `mapbiomas_*` (7 tabelas stats) | ~26.659 | MapBiomas stats |
| `geo_armazens_silos` + 4 tabelas infra | ~33.417 | MapBiomas Infra |
| `mv_dashboard_kpis` | 1 row | Materialized view (5ms) |

**APIs conectadas em tempo real:**
- Earth Engine (LULC, fogo, solo, água) — via flag `include_satellite`
- MapBiomas Alerta GraphQL — via flag `include_realtime_alerts`
- BigQuery BasedosDados — scripts ETL prontos
- DataJud/CNJ — API key pública configurada, 88 tribunais, testado TJMA
- BrasilAPI — CNPJ em tempo real
- BCB API — SELIC, IPCA, câmbio
- NASA POWER — clima por coordenada

**Motor de relatório:** pipeline CAR code → PostGIS (13 camadas) → Compliance → JSON/PDF em ~250ms

**42+ endpoints FastAPI** — Swagger: http://localhost:8000/docs

### Frontend — Problema crítico

O frontend (`frontend_v2/`) existe mas **não renderiza o mapa**. O backend está correto e os endpoints GeoJSON funcionam. O problema está no lado cliente — a integração Leaflet/Vite não está funcionando. Diagnóstico e correção é a **primeira tarefa da próxima sessão**.

### Motor jurídico — Não implementado

Ainda não existe. É o diferencial central do produto. Fase 1 começa aqui.

---

## SEÇÃO 3 — PERSONAS COMPLETAS (15 personas — atualização sessão 4)

Esta é a grande atualização da sessão 4: mapeamento completo do mercado endereçável.

---

### Persona 1 — Banco / Cooperativa de Crédito Rural

**O que precisa:** Enquadrar operações de crédito rural na MCR 2.9 antes da liberação. Verificar se o imóvel dado em garantia está regular ambientalmente. Fazer due diligence de garantias fundiárias.

**O que o AgroJus entrega:**
- Calculadora MCR 2.9 com output APTO / INAPTO / PENDENTE e checklist auditável para o Bacen
- Análise de garantias: área líquida real (descontando embargo, TI, APP, sobreposições)
- Score de risco ambiental 0–1000 com decomposição em 5 eixos
- Relatório auditável com rastreabilidade de fonte (para auditoria interna)
- Histórico de financiamentos SICOR sobre o imóvel

**Fontes necessárias:** SICAR, SIGEF, IBAMA embargos, DETER/PRODES, FUNAI, ICMBio, DataJud, BCB SICOR, MapBiomas alertas

**Profundidade do relatório:** Alta — relatório técnico completo com checklist MCR 2.9 explícito, assinável por responsável técnico do banco

**Decisão estratégica sessão 4:** Movido para Fase 1 (prioridade máxima). Banco e cooperativa são os maiores pagadores — não compram o produto sem enquadramento MCR 2.9 confiável.

---

### Persona 2 — Trader / Exportador

**O que precisa:** Compliance EUDR (Regulamento Europeu de Desmatamento) para exportar para a UE. Rastreabilidade da cadeia produtiva. Due diligence de compra de commodity (soja, milho, carne, café).

**O que o AgroJus entrega:**
- Score EUDR (Conformado / Crítico / Verificação necessária) por imóvel ou por CPF/CNPJ do produtor
- Certificação de ausência de desmatamento pós-2020 (corte regulatório EUDR)
- Relatório de rastreabilidade com polígono SIGEF + CAR + histórico MapBiomas
- Exportação de dados no formato exigido pela Comissão Europeia

**Fontes necessárias:** SICAR, SIGEF, PRODES, DETER, MapBiomas Cobertura, Earth Engine

**Profundidade do relatório:** Média-Alta — foco no checklist EUDR exportável, com dados de desmatamento georreferenciados

---

### Persona 3 — Advogado Rural (consulta para pautar processos)

**O que precisa:** Dados citáveis com fonte rastreável para embasar petições, laudos e pareceres. Dossiê rápido do imóvel ou do cliente para triagem de casos. Verificar se há embargos, processos, irregularidades antes de aceitar o mandato.

**O que o AgroJus entrega:**
- Dossiê consolidado CPF/CNPJ: DataJud + IBAMA + MTE + SICAR + SIGEF em uma tela
- Dados com referência de fonte oficial (citável em peça processual)
- Busca de jurisprudência ambiental aplicável ao caso concreto (STJ, TRFs)
- Análise geoespacial do imóvel com metadados de cada sobreposição

**Fontes necessárias:** DataJud/CNJ, IBAMA embargos, MTE lista suja, SICAR, SIGEF, ICMBio, FUNAI, base de jurisprudência

**Profundidade do relatório:** Média — triagem rápida + detalhe sob demanda por eixo

---

### Persona 4 — Advogado / Produtor Respondendo Notificação ou Auto de Infração

**O que precisa:** Analisar auto de infração IBAMA ou ICMBio para montar defesa. Verificar prescrição, nulidades formais, competência, motivação do ato. Identificar teses aplicáveis e jurisprudência favorável.

**O que o AgroJus entrega:**
- Análise do embargo: classificação (desmatamento, APP, RL, fauna, poluição)
- Cálculo automático de prescrição (administrativa 5 anos, criminal 12–20 anos, trabalhista 2 anos)
- Identificação de nulidades formais (prazo de notificação, competência, motivação do ato)
- Teses de defesa sugeridas com jurisprudência aplicável (STJ, TRFs)
- Estimativa da multa esperada e possibilidade de conversão (Dec. 6.514/08)
- Minuta de defesa administrativa gerada automaticamente

**Fontes necessárias:** IBAMA embargos, ICMBio autos, DataJud, base de jurisprudência ambiental interna

**Profundidade do relatório:** Alta — relatório jurídico com raciocínio explícito, teses e minutas

---

### Persona 5 — Comprador de Imóvel Rural

**O que precisa:** Due diligence pré-compra para não comprar imóvel com passivo ambiental, trabalhista, fundiário ou judicial. Checklist de regularidade antes de assinar escritura.

**O que o AgroJus entrega:**
- Checklist completo de regularidade: CAR ativo, SIGEF certificado, embargo IBAMA, lista suja MTE, processos judiciais, sobreposições com TI/UC/assentamento
- Área líquida comprável (descontando sobreposições e passivos)
- Score de risco geral com decomposição por eixo
- Valuation estimado para comparar com o preço pedido

**Fontes necessárias:** SICAR, SIGEF, IBAMA, MTE, DataJud, FUNAI, ICMBio, INCRA assentamentos, MapBiomas

**Profundidade do relatório:** Média — checklist objetivo com semáforo verde/amarelo/vermelho por item

---

### Persona 6 — Vendedor de Imóvel Rural

**O que precisa:** Laudo de valorização que justifique o preço pedido. Demonstrar produtividade histórica, uso do solo, infraestrutura logística, regularidade ambiental. Comparativo de preço por hectare na região.

**O que o AgroJus entrega:**
- Relatório de valorização: produtividade histórica por cultura (PAM/IBGE), uso do solo MapBiomas, infraestrutura logística (silos, portos, rodovias)
- Comparativo R$/ha por município, microrregião e estado
- Certificação de regularidade ambiental (MCR 2.9 + EUDR) como argumento de venda
- Exportação de laudo em PDF com dados e mapas

**Fontes necessárias:** IBGE PAM/PPM, MapBiomas Cobertura, MapBiomas Infra, SICAR, SIGEF, ONR (futuro)

**Profundidade do relatório:** Média — relatório de marketing técnico, com dados de valorização e comparativos

---

### Persona 7 — Corretor de Imóveis Rurais

**O que precisa:** Ficha técnica rápida do imóvel para apresentar ao comprador. Score de risco resumido em 1 página. Comparativo de preço regional para argumentar a negociação.

**O que o AgroJus entrega:**
- Ficha técnica de 1 página: área, bioma, município, CAR, uso do solo, infraestrutura logística, score de risco
- Comparativo de preço R$/ha na microrregião
- QR Code para o comprador verificar os dados diretamente

**Fontes necessárias:** SICAR, SIGEF, MapBiomas, IBGE, BCB

**Profundidade do relatório:** Baixa-Média — resumo executivo de 1 página, visual

---

### Persona 8 — Agrimensor

**O que precisa:** Situação geoespacial completa do imóvel: SIGEF, SICAR, sobreposições, vértices, histórico de perímetro, confrontantes. Identificar inconsistências antes de certificar.

**O que o AgroJus entrega:**
- Comparativo SIGEF vs CAR: polígonos sobrepostos, diferença de área, vértices
- Sobreposições críticas georreferenciadas: TI, UC, assentamento, quilombo
- Histórico de alterações de perímetro
- Exportação em shapefile, GeoJSON e KML

**Fontes necessárias:** SIGEF, SICAR, FUNAI, ICMBio, INCRA assentamentos

**Profundidade do relatório:** Alta técnica — GIS puro, sem análise jurídica, com exportação de camadas

---

### Persona 9 — Engenheiro Ambiental / Biólogo / Agrônomo

**O que precisa:** Análise técnica detalhada de cobertura vegetal, aptidão de solo, hidrografia, passivo de Reserva Legal. Exportação de dados em formatos GIS para uso em laudos e projetos.

**O que o AgroJus entrega:**
- Série histórica de cobertura vegetal 1985–2023 (MapBiomas Col. 10)
- Passivo de Reserva Legal calculado sobre o polígono real
- Aptidão de solo e bioma (Embrapa GeoInfo)
- Outorgas de água ANA na área de influência
- Exportação shapefile / GeoJSON / CSV por camada

**Fontes necessárias:** MapBiomas Cobertura, Embrapa GeoInfo, ANA Outorgas, SICAR (RL e APP), Earth Engine

**Profundidade do relatório:** Alta técnica — séries históricas + exportação GIS

---

### Persona 10 — Pecuarista / Produtor Rural

**O que precisa:** Monitorar a própria propriedade. Receber alertas de novos embargos ou desmatamento detectado. Saber o status ambiental atual antes de ir ao banco pedir crédito.

**O que o AgroJus entrega:**
- Dashboard do imóvel: status MCR 2.9, alertas ativos, situação CAR
- Monitoramento contínuo: alerta WhatsApp quando novo embargo ou alerta DETER for detectado
- Diagnóstico de regularidade simplificado ("Você está apto para crédito rural? Sim/Não — e por quê")
- Checklist de regularização passo a passo se houver pendências

**Fontes necessárias:** SICAR, IBAMA, DETER, MapBiomas Alerta, ICMBio

**Profundidade do relatório:** Baixa — linguagem simples, semáforo, ação concreta recomendada

---

### Persona 11 — Fintech Agro

**O que precisa:** Scoring de risco para crédito rural via API. Valuation de garantias em tempo real. Integração com core bancário ou app próprio de crédito.

**O que o AgroJus entrega:**
- API REST com score de risco 5 eixos (0–1000) e componente MCR 2.9
- Valuation de garantia com intervalo de confiança e metodologia auditável
- Webhook de alertas: notifica quando um imóvel da carteira muda de status
- SLA de resposta < 500ms para consultas de triagem

**Fontes necessárias:** Todas as fontes do motor de relatório

**Profundidade do relatório:** API-first — JSON estruturado, sem PDF, com todos os campos necessários para scoring automatizado

---

### Persona 12 — Investidor em Terras

**O que precisa:** Valuation fundamentado em dados reais. Rentabilidade esperada por cultura e região. Comparativo de terras em diferentes estados. Risco ambiental que pode desvalorizar o ativo.

**O que o AgroJus entrega:**
- Valuation por renda capitalizada: produtividade histórica × preço de commodity × fator de risco
- Comparativo R$/ha por microrregião com série histórica
- Análise de risco de desvalorização (embargo, desmatamento, sobreposição TI)
- Radar de oportunidades: terras regularizadas, com infraestrutura, abaixo do comparativo regional

**Fontes necessárias:** IBGE PAM/PPM, CEPEA, B3 futuros, MapBiomas, IBAMA, DETER, SIGEF

**Profundidade do relatório:** Alta financeira — valuation com metodologia explícita + análise de risco

---

### Persona 13 — Agente Público (Fiscal / Servidor)

**O que precisa:** Consulta técnica de dados rurais para fiscalização, licenciamento e análise de processos administrativos. Acesso integrado a dados que hoje estão dispersos em 10+ portais governamentais.

**O que o AgroJus entrega:**
- Consulta unificada: um CAR devolve dados de IBAMA, ICMBio, FUNAI, INCRA, DataJud em uma tela
- Histórico de embargo e autos de infração por imóvel ou por CPF/CNPJ
- Visualização geoespacial: sobreposições críticas no mapa
- Exportação de dados em formatos oficiais

**Fontes necessárias:** IBAMA, ICMBio, FUNAI, SICAR, SIGEF, DataJud, INCRA

**Profundidade do relatório:** Média — agregação de fontes, sem análise jurídica, com exportação

---

### Persona 14 — Gestor Público (Secretário, Prefeito, Técnico de Secretaria)

**O que precisa:** Dados agregados por município ou região para políticas públicas, planejamento territorial, concessão de crédito rural, monitoramento de desmatamento e regularização fundiária.

**O que o AgroJus entrega:**
- Dashboard municipal: área de CAR ativo, % de conformidade ambiental, alertas DETER, embargos, crédito rural liberado vs bloqueado
- Comparativo entre municípios do estado
- Mapas temáticos exportáveis para apresentações e relatórios de gestão
- Dados agregados para orientar metas de regularização fundiária

**Fontes necessárias:** SICAR, DETER, PRODES, BCB SICOR, IBAMA, MapBiomas, IBGE

**Profundidade do relatório:** Agregada — painel executivo com drill-down por município

---

### Persona 15 — Cidadão em Geral

**O que precisa:** Consulta pública de imóvel vizinho. Denúncia de desmatamento. Verificação de regularidade de produtor. Acesso democrático a dados públicos que hoje são inacessíveis na prática (15+ portais com logins diferentes).

**O que o AgroJus entrega:**
- Consulta pública gratuita por CAR ou por município (tier freemium)
- Verificação simplificada: "este imóvel está regular?" — resposta em linguagem acessível
- Mapa público de alertas de desmatamento na sua região
- Canal de denúncia com georreferenciamento

**Fontes necessárias:** SICAR, DETER, MapBiomas Alerta, IBAMA (dados públicos)

**Profundidade do relatório:** Mínima — linguagem acessível, dados públicos, sem análise jurídica

---

## SEÇÃO 4 — DECISÃO ESTRATÉGICA: PRIORIZAÇÃO DE CRÉDITO E VALUATION

**Decisão tomada na sessão 4:** Crédito rural e valuation movidos da Fase 2 para a **Fase 1**, junto com o motor jurídico.

**Motivo central:** Bancos e cooperativas são os maiores pagadores do mercado — produto com ticket alto, compra institucional, renovação recorrente. Eles não compram o AgroJus sem dois requisitos inegociáveis: (1) enquadramento MCR 2.9 defensável perante o Bacen e (2) valuation de garantias com metodologia auditável. Sem esses dois, não há negociação.

**Sequência de implementação — Fase 1:**

1. **Calculadora MCR 2.9** — output APTO/INAPTO/PENDENTE com checklist explícito auditável, pontuando os 6 critérios do regulamento (CAR ativo, ausência de embargo IBAMA ativo, ausência de sobreposição TI/UC, sem trabalho escravo MTE, CAR não cancelado, ausência de desmatamento pós-2020 em biomas críticos)

2. **Valuation simplificado — renda capitalizada** — R$/ha estimado via fórmula: produtividade histórica PAM/IBGE × preço de commodity CEPEA × fator de aptidão do solo Embrapa × taxa de capitalização BCB, com desconto proporcional por passivo ambiental

3. **Análise saldo devedor / alongamento** — usuário informa banco, programa, valor, safra, data de vencimento → sistema calcula saldo devedor real, compara com taxas legais (Selic, TR, TJLP), identifica abusos, verifica elegibilidade para PESA/PRONAF/PRONAMP, gera minuta de notificação

4. **Motor jurídico — prescrição e teses** — dado um auto de infração ou processo, calcular prescrição (administrativa 5a, criminal 12–20a, trabalhista 2a) e sugerir teses aplicáveis com jurisprudência citada

---

## SEÇÃO 5 — ROADMAP ATUALIZADO (pós-sessão 4)

### Fase 0 — Fundação (2–3 dias) ← COMEÇAR AQUI

| # | Tarefa | Prioridade |
|---|---|---|
| 0.1 | **Consertar mapa frontend** — diagnosticar `frontend_v2/`, problema na integração Leaflet/Vite | CRÍTICA |
| 0.2 | Completar download SICAR todos os estados via BigQuery | ALTA |
| 0.3 | Completar download SIGEF todos os estados | ALTA |
| 0.4 | Baixar DETER/PRODES completos (shapefiles diretos TerraBrasilis, não WFS) | ALTA |
| 0.5 | Cadastros Eduardo (Seção 6) | MÉDIA |

### Fase 1 — Motor Jurídico + Crédito + Valuation (5–7 dias) ← DIFERENCIAL ÚNICO

| # | Tarefa | Prioridade |
|---|---|---|
| 1.1 | **Calculadora MCR 2.9** — 6 critérios, output auditável, endpoint POST /api/v1/compliance/mcr29 | CRÍTICA |
| 1.2 | **Valuation simplificado** — renda capitalizada, endpoint POST /api/v1/valuation/estimar | CRÍTICA |
| 1.3 | **Análise de saldo devedor / alongamento** — POST /api/v1/credito/analisar-alongamento | ALTA |
| 1.4 | **Scoring 5 eixos** — fundiário, ambiental, trabalhista, jurídico, financeiro (0–1000 cada) | CRÍTICA |
| 1.5 | **Prescrição automática** — dado auto de infração, calcular prescrição | CRÍTICA |
| 1.6 | **Análise de embargos** — classificação + nulidades + defesa sugerida | CRÍTICA |
| 1.7 | Base de jurisprudência ambiental interna (STJ, TRFs — tabela de precedentes) | ALTA |
| 1.8 | Tabela de taxas históricas BCB (Selic, TR, TJLP) para cálculo de saldo devedor | ALTA |

### Fase 2 — Contratos e Checklists (3–5 dias)

Templates de contratos agro (arrendamento, parceria, CPR, compra/venda), checklists regulatórios interativos (licenciamento, CAR, outorga, SIGEF), gerador de comunicações (notificação, requerimento, defesa administrativa).

### Fase 3 — Frontend Completo (7–10 dias)

Next.js 14 + Tailwind + shadcn/ui + react-leaflet. Mapa interativo com 13 camadas. Dashboard com scores 0–1000 visuais (gauge style). Telas dedicadas para cada persona principal (banco, advogado, produtor, comprador).

### Fase 4 — Canais (3–5 dias)

Bot WhatsApp (consulta por CAR, alerta de embargos, status processo). Alertas por e-mail. Monitoramento contínuo (webhook novo embargo/desmatamento).

### Fase 5 — IA Avançada (5–7 dias)

Raciocínio auditável cite-to-source. Teses automáticas com % de êxito. Radar de prospecção. CRM Kanban de teses.

**MVP para bancos (Fases 0–1):** ~10 dias
**MVP completo (Fases 0–2):** ~15 dias
**Produto completo (Fases 0–5):** ~37 dias

---

## SEÇÃO 6 — FONTES DE DADOS (135 fontes catalogadas)

### As 11 categorias com contagem estimada

| # | Categoria | Fontes catalogadas | No PostGIS | Ativas (tempo real) |
|---|---|---|---|---|
| 1 | Fundiário (SICAR, SIGEF, SNCR, INCRA) | ~18 | 2 | 1 |
| 2 | Ambiental (IBAMA, ICMBio, MTE, DETER, PRODES) | ~15 | 5 | 0 |
| 3 | Crédito Rural (BCB SICOR, MapBiomas Crédito, PRONAF) | ~12 | 2 | 1 |
| 4 | Geoespacial / Vegetação (MapBiomas, Earth Engine, Embrapa) | ~22 | 8 | 2 |
| 5 | Judiciário (DataJud/CNJ, 88 tribunais) | ~8 | 0 | 1 |
| 6 | Mercado / Preços (CEPEA, B3, CONAB, Yahoo Finance) | ~14 | 1 | 2 |
| 7 | Climático / Ambiental técnico (INMET, NASA POWER, Embrapa ClimAPI) | ~10 | 0 | 1 |
| 8 | Infraestrutura Logística (silos, portos, ferrovias) | ~8 | 5 | 0 |
| 9 | Cadastros / Registros (ONR, cartório, BrasilAPI CNPJ) | ~12 | 0 | 1 |
| 10 | Governamental / Transparência (Portal Transparência, DOU, IBGE) | ~10 | 1 | 1 |
| 11 | Hídrico (ANA Outorgas, HidroWeb, SNIRH) | ~6 | 0 | 0 |
| | **TOTAL** | **~135** | **24** | **10** |

### As 10 de maior impacto ainda não integradas

1. **DETER completo** — 800k+ alertas reais (temos apenas 50k do WFS). Baixar shapefile direto TerraBrasilis.
2. **MapBiomas Alerta GraphQL** — alertas por CAR em tempo real. Requer conta (cadastro gratuito).
3. **SICAR/CAR completo via WFS** — polígonos CAR direto do GeoServer SICAR (sem BigQuery). Crítico para cobertura nacional.
4. **ONR / Matrículas** — cadeia dominial completa. Sem API pública. Opções: InfoSimples (~R$0,50/consulta) ou parceria institucional.
5. **Embrapa AgroAPI (ZARC + SATVeg + ClimAPI)** — zoneamento agrícola, NDVI, clima. Gratuito após cadastro.
6. **CONAB safras** — estimativas de produção por cultura/estado. Via agrobr (já instalado).
7. **CEPEA histórico de preços** — cotações reais de commodities para valuation. Via agrobr (já instalado).
8. **Portal Transparência API (CEIS/CNEP/MTE)** — empresas e produtores com sanções. Gratuito após cadastro.
9. **ANA Outorgas (ArcGIS FeatureServer)** — risco hídrico por imóvel. URL disponível, sem autenticação.
10. **ANM/SIGMINE** — processos minerários sobrepostos ao imóvel. Corrigir ETL ou baixar KMZ.

### Os 5 cadastros que Eduardo precisa fazer (~30 min, alto impacto)

1. **console.cloud.google.com** — criar projeto GCP gratuito. Desbloqueia BigQuery para CNPJ (2,7 bilhões de linhas) e SICAR completo.
2. **plataforma.alerta.mapbiomas.org** — criar conta gratuita. Desbloqueia alertas de desmatamento por CAR em tempo real.
3. **portaldatransparencia.gov.br/api-de-dados** — cadastrar e-mail. Desbloqueia CEIS, CNEP, lista suja MTE via API.
4. **agroapi.cnptia.embrapa.br** — criar conta gratuita. Desbloqueia ZARC (zoneamento agrícola), ClimAPI, SATVeg (NDVI), AGROFIT.
5. **InfoSimples (opcional, pago)** — criar conta e depositar créditos (~R$0,50/consulta de matrícula). Desbloqueia cadeia dominial completa via ONR.

---

## SEÇÃO 7 — COMANDOS RÁPIDOS

```bash
# ── SUBIR AMBIENTE ──────────────────────────────────────────────────────────
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# ── VERIFICAR STATUS ─────────────────────────────────────────────────────────
curl -s http://localhost:8000/health | python -m json.tool

# ── TESTAR RELATÓRIO COMPLETO (~250ms) ───────────────────────────────────────
curl -s -X POST http://localhost:8000/api/v1/report/due-diligence \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21"}' | python -m json.tool

# ── TESTAR COM SATÉLITE (~20s extra) ─────────────────────────────────────────
curl -s -X POST http://localhost:8000/api/v1/report/due-diligence \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21","include_satellite":true,"include_realtime_alerts":true}'

# ── DASHBOARD (5ms via materialized view) ────────────────────────────────────
curl -s http://localhost:8000/api/v1/dashboard/metrics | python -m json.tool

# ── BUSCAR IMÓVEIS ────────────────────────────────────────────────────────────
curl -s "http://localhost:8000/api/v1/property/search?uf=MA&page_size=5" | python -m json.tool

# ── GEOJSON PARA MAPA ────────────────────────────────────────────────────────
curl -s "http://localhost:8000/api/v1/property/MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21/geojson"

# ── OVERLAPS PARA MAPA ───────────────────────────────────────────────────────
curl -s "http://localhost:8000/api/v1/property/MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21/overlaps/geojson"

# ── SWAGGER UI ───────────────────────────────────────────────────────────────
# http://localhost:8000/docs

# ── ATUALIZAR MATERIALIZED VIEW ──────────────────────────────────────────────
curl -s -X POST http://localhost:8000/api/v1/dashboard/refresh

# ── ETL: COMPLETAR SIGEF TODOS OS ESTADOS (~1h) ──────────────────────────────
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python scripts/etl_sigef_download.py ALL

# ── ETL: COMPLETAR SICAR VIA BIGQUERY TODOS OS ESTADOS (~4h) ─────────────────
MSYS_NO_PATHCONV=1 docker exec agrojus-backend-1 python scripts/etl_sicar_bigquery.py ALL

# ── CHECAR LOGS DO BACKEND ───────────────────────────────────────────────────
docker compose logs backend --tail=50 -f

# ── CONECTAR AO BANCO DIRETAMENTE ────────────────────────────────────────────
docker exec -it agrojus-db-1 psql -U agrojus -d agrojus

# ── LISTAR TABELAS NO POSTGIS ────────────────────────────────────────────────
docker exec agrojus-db-1 psql -U agrojus -d agrojus -c "\dt"
```

---

## SEÇÃO 8 — PRÓXIMOS PASSOS CONCRETOS PARA A PRÓXIMA SESSÃO

Execute nesta ordem exata:

**1. Subir o ambiente**
```bash
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d
curl -s http://localhost:8000/health
```

**2. Verificar health check** — confirmar que backend responde e PostGIS está acessível. Se falhar, checar `docker compose logs`.

**3. Diagnosticar problema do mapa (Fase 0.1)** — abrir `frontend_v2/` e identificar por que o Leaflet não renderiza. Verificar: (a) se o container frontend está rodando, (b) se há erros no console do browser, (c) se os endpoints GeoJSON respondem corretamente via curl (já funcionam), (d) se há problema de CORS, (e) se o Vite está servindo o bundle correto. O backend está correto — o problema é no cliente.

**4. Implementar Calculadora MCR 2.9 (Fase 1 — prioridade 1)**
- Criar `backend/app/services/mcr29_calculator.py`
- Endpoint: `POST /api/v1/compliance/mcr29`
- Input: `car_code` ou `geometry`
- Output: `{"status": "APTO|INAPTO|PENDENTE", "score": 0-100, "checklist": [{criterio, status, fonte, dados}]}`
- 6 critérios MCR 2.9: CAR ativo sem pendência, ausência embargo IBAMA ativo, ausência sobreposição TI ativa, ausência lista suja MTE, sem desmatamento pós-2020 PRODES em bioma crítico, SIGEF certificado (se aplicável)

**5. Implementar Valuation Simplificado (Fase 1 — prioridade 2)**
- Criar `backend/app/services/valuation.py`
- Endpoint: `POST /api/v1/valuation/estimar`
- Fórmula base: `VTN = (produtividade_ibge × preco_cepea × fator_solo) / taxa_capitalizacao`
- Ajuste por: presença de embargo (desconto %), sobreposição TI/UC (desconto %), infraestrutura logística (prêmio %), uso do solo atual (MapBiomas)
- Output: `{"valor_ha_estimado": float, "intervalo_95": [min, max], "comparable_municipio": float, "fatores": [...], "metodologia": "renda_capitalizada"}`

---

## SEÇÃO 9 — DECISÕES PENDENTES DO EDUARDO

As seguintes decisões ainda dependem de escolha do Eduardo antes de implementar:

**1. WhatsApp — Twilio ou Meta Cloud API?**
- Twilio: mais fácil de integrar, custo ~R$0,05/mensagem, suporte técnico bom
- Meta Cloud API: gratuito até certo volume, mais complexo de configurar, precisa verificação de negócio
- Recomendação: Twilio para MVP, Meta Cloud API se volume crescer

**2. IA para teses jurídicas e scoring — Claude API ou OpenAI?**
- Claude API (Anthropic): melhor raciocínio jurídico em português, contexto longo (200k tokens), mais conservador em afirmações
- OpenAI GPT-4o: ecossistema maior, function calling maduro, fine-tuning disponível
- Recomendação: Claude API para o motor jurídico (raciocínio auditável é o diferencial)

**3. Fazer os 5 cadastros gratuitos** (detalhados na Seção 6) — ~30 min, alto impacto imediato no produto

**4. Contratar InfoSimples para matrículas (~R$0,50/consulta)?**
- Desbloqueia cadeia dominial completa (ONR), que é crítica para persona banco e comprador de imóvel
- Decisão: contratar? Qual orçamento mensal máximo?

**5. Personas agente público (13) e cidadão (15) — estratégia de produto:**
- **Opção A — Freemium público:** dados básicos gratuitos para qualquer pessoa, pago para dados completos. Gera tráfego orgânico e pressão pública por regularização.
- **Opção B — B2G (venda para governo):** produto pago para secretarias, prefeituras, órgãos de fiscalização. Ticket alto, ciclo de venda longo, dependência de licitação.
- **Opção C — Ambos:** freemium para cidadão + B2G para gestores. Mais complexo, mas cobre o mercado inteiro.
- Recomendação: Opção C a médio prazo. No MVP, focar apenas no B2B (banco, advogado, trader).

---

## APÊNDICE — CREDENCIAIS E LOCALIZAÇÃO

| Serviço | Localização |
|---|---|
| PostgreSQL/PostGIS | `postgresql://agrojus:agrojus@localhost:5432/agrojus` |
| GCP Project ID | `agrojus` |
| GCP Credentials | `${APPDATA}/gcloud/application_default_credentials.json` |
| MapBiomas | `eduardo@guerreiro.adv.br` (em .env) |
| DataJud | API key pública em `backend/app/config.py` |
| JWT Secret | Valor default dev (alterar antes de produção) |

## APÊNDICE — ESTRUTURA DE ARQUIVOS RELEVANTE

```
Claude/agrojus/
  docker-compose.yml
  backend/
    app/
      api/
        property.py          ← busca, GeoJSON, overlaps
        report.py            ← due-diligence, buyer, lawyer, investor, PDF
        dashboard.py         ← materialized view (5ms)
        geo.py               ← analyze-point, layers GeoJSON
        consulta.py          ← dossiê CPF/CNPJ (7 fontes)
      services/
        postgis_analyzer.py  ← 13 camadas espaciais (~250ms)
        compliance.py        ← MCR 2.9 básico, EUDR, score 0-1000
        earth_engine.py      ← LULC, fogo, solo, água
        mapbiomas_alerta.py  ← GraphQL alertas tempo real
        due_diligence.py     ← PostGIS-first pipeline
        pdf_report.py        ← PDF com tabelas de compliance
      models/
        schemas.py           ← +compliance, +spatial, +satellite
        database.py          ← SQLAlchemy engine
      config.py              ← API keys, URLs
    scripts/
      etl_sicar_bigquery.py  ← download SICAR via BigQuery
      etl_sigef_download.py  ← download SIGEF via INCRA
  frontend_v2/               ← PROBLEMA: mapa não renderiza (diagnosticar)
  docs/
    HANDOFF_2026-04-15_sessao4.md   ← ESTE ARQUIVO
    HANDOFF_2026-04-15_sessao3.md   ← Estado técnico pós-sessão 3
    ROADMAP_FASEADO_v1.md           ← Roadmap detalhado pré-sessão 4
    STATUS_FONTES_DADOS.md          ← Inventário de fontes (v1, 53 fontes)
    CONTEXTO_COMPLETO.md            ← Briefing do produto (versão 2.0)
    API_FRONTEND_CONTRACT.md        ← Contrato API para frontend
    ANALISE_COMPETITIVA_COMPLETA.md ← 53 sites analisados
    INVENTARIO_FEATURES.md          ← 336 features catalogadas
```

---

*AgroJus v0.9.3 — Handoff Sessão 4 — 2026-04-15 BRT*
*Próxima sessão: Fase 0.1 (mapa) → Fase 1 (MCR 2.9 + valuation + motor jurídico)*
