# AgroJus — Handoff Sessão 5 (16/04/2026)

> **Cole este arquivo inteiro no início da próxima sessão do Claude Code.**
> É autocontido. Substitui todos os handoffs anteriores.
> Sessão 5: auditoria honesta + pesquisa de mercado profunda + reestruturação.

---

## SEÇÃO 1 — O QUE É O AGROJUS

### Produto
AgroJus é uma plataforma SaaS B2B de inteligência fundiária, ambiental, jurídica e financeira para o agronegócio brasileiro. Combina dados geoespaciais (CAR, SIGEF, IBAMA, DETER, PRODES, MapBiomas) com análise jurídica especializada — nenhum concorrente faz isso.

### A brecha regulatória
**Resoluções CMN 5.267/5.268 (MCR 2.9)** — desde 01/04/2026, todo banco do Brasil verifica automaticamente conformidade ambiental antes de liberar crédito rural. **EUDR** — desde 30/12/2026, exportadores para a UE provam ausência de desmatamento pós-2020. Dois regulamentos obrigatórios convergindo = demanda garantida.

### Posicionamento
*"O compliance do exportador brasileiro que fala tanto com Bruxelas quanto com o Banco Central — e ainda defende quando o IBAMA bate na porta."*

### Advogado
Eduardo Pinho Alves de Souza — OAB/MA 12.147 — Guerreiro Advogados Associados — São Luís/MA. Áreas: agronegócio, ambiental, tributário, cível/possessório.

---

## SEÇÃO 2 — AUDITORIA HONESTA DO ESTADO ATUAL

> **REGRA CRÍTICA:** Não confie nos handoffs anteriores. Eles inflam números e misturam o que existe com o que foi planejado. Esta seção reflete o estado REAL verificado no código.

### Stack técnica

```
Backend:    FastAPI + SQLAlchemy + PostGIS (PostgreSQL 16 + PostGIS 3.4)
Frontend:   Next.js 16.2.3 + React 19 + react-leaflet 5 + Tailwind v4 + shadcn/ui
Infra:      Docker Compose (containers: db + backend)
ETL:        Python scripts (pdfplumber, httpx, geopandas, ogr2ogr)
Branch git: claude/continue-backend-dev-sVLGG
Repo:       https://github.com/eduardopasouza/Claude
Diretório:  c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus
```

**ATENÇÃO:** Documentos anteriores dizem "Next.js 14" e "Vite" — AMBOS estão errados. O frontend real é **Next.js 16.2.3**.

### Backend — O que funciona DE VERDADE

**Endpoints confirmados funcionais (testados com curl):**
- `GET /health` — health check
- `POST /api/v1/report/due-diligence` — relatório completo (~250-400ms para CARs do MA)
- `GET /api/v1/dashboard/metrics` — KPIs via materialized view (~5ms)
- `GET /api/v1/property/search` — busca CARs por texto/UF
- `GET /api/v1/property/{car_code}/geojson` — polígono do imóvel
- `GET /api/v1/property/{car_code}/overlaps/geojson` — sobreposições 14 camadas
- `GET /api/v1/geo/layers/{layer}/geojson` — camadas GeoJSON com bbox
- `POST /api/v1/consulta/completa` — dossiê CPF/CNPJ (7 fontes)

**APIs externas realmente conectadas:**
| API | Status | Notas |
|---|---|---|
| BrasilAPI (CNPJ) | ✅ Funciona | Sem auth |
| BCB API (SELIC, IPCA, câmbio) | ✅ Funciona | Sem auth |
| NASA POWER (clima) | ✅ Funciona | Sem auth |
| DataJud/CNJ | ⚠️ Configurado | API key pública, testado TJMA |
| Earth Engine | ⚠️ Depende de credenciais | Flag `include_satellite`, +20s |
| MapBiomas GraphQL | ⚠️ Depende de conta | Flag `include_realtime_alerts` |
| BigQuery | ❌ Bloqueado | GCP_PROJECT_ID não configurado |
| BCB SICOR OData | ❌ Retornou 503 | API em manutenção na sessão 4 |

**Motor de relatório:**
- Funciona para CARs do Maranhão (~250-400ms)
- Cruza 14 camadas via ST_Intersects no PostGIS
- Para CARs de outros estados: dados muito parciais ou inexistentes
- Compliance MCR 2.9: 6 checks binários (pass/fail). NÃO é a "calculadora auditável" prometida nos docs

### Banco de dados — Números REAIS

**~24 tabelas com dados reais. NÃO 60 como dizem os docs (o resto são tabelas de sistema, vazias ou auxiliares).**

| Tabela | Registros reais | Completude |
|---|---|---|
| `mapbiomas_credito_rural` | 5.614.207 | ✅ Completo (GPKG importado) |
| `geo_mapbiomas_alertas` | 515.823 | ✅ Completo |
| `sigef_parcelas` | 493.913 | ⚠️ Parcial (6 de 27 UFs) |
| `sicar_completo` | ~308.000 | ❌ Só MA (79.3M disponíveis) |
| `geo_car` | 135.000 | ⚠️ Parcial (WFS 5k/UF) |
| `environmental_alerts` (IBAMA) | 104.284 | ✅ Completo |
| `geo_deter_amazonia` | 50.000 | ❌ Parcial (real: 800k+) |
| `geo_deter_cerrado` | 50.000 | ❌ Parcial (real: 200k+) |
| `geo_prodes` | 50.000 | ❌ Parcial |
| `sicor_custeio_uf` | 50.000 | ❌ Parcial |
| `geo_armazens_silos` + infra | ~33.417 | ✅ Completo |
| `mapbiomas_*` (7 tabelas stats) | ~26.659 | ✅ Completo |
| `geo_autos_icmbio` + embargos | ~15.000 | ⚠️ Parcial |
| `geo_terras_indigenas` | 655 | ✅ Completo |
| `environmental_alerts` (MTE) | 614 | ✅ (parser PDF frágil) |
| `geo_unidades_conservacao` | 346 | ✅ Completo |
| `rural_credits` | **0** | ❌ BCB em manutenção |
| `ana_outorgas` | **0** | ❌ URL não encontrada |

**Total real: ~7M registros (não 10.7M como dizem os docs)**

### Frontend — O que existe

**Existem DOIS frontends no repo:**
1. `frontend/` — Vite vanilla, scaffold vazio. IGNORAR.
2. `frontend_v2/` — Next.js 16 real. **ESTE é o frontend.**

**frontend_v2 — Páginas (verificado no código, 19 arquivos, 2.060 linhas):**
| Rota | Linhas | Backend real? | Estado |
|---|---|---|---|
| `/login` | 100 | ✅ SIM (POST /auth/login, JWT) | Funcional |
| `/` (Dashboard) | 138 | ✅ SIM (GET /dashboard/metrics, SWR 60s) | KPIs reais. Feed notícias + cotações = HARDCODED |
| `/mapa` | 253+244 | ✅ SIM (GET /geo/layers, /property/search, /overlaps) | **Funcional e bem construído** |
| `/mercado` | 81 | ✅ SIM (GET /market/quotes + /indicators) | Funcional com fallback mock se offline |
| `/consulta` | 291 | ❌ NÃO (setTimeout mock, zero API) | **Esqueleto visual sofisticado, zero dados reais** |
| `/compliance` | 69 | ❌ NÃO (3 linhas hardcoded, botões decorativos) | Placeholder |
| `/alertas` | 41 | ❌ NÃO (4 alertas hardcoded) | Placeholder |

**Build:** Passa 100% limpo (0 erros TypeScript) após `@types/leaflet` + `turbopack.root: "."` (sessão 5).

**Mapa Leaflet:** RENDERIZA CORRETAMENTE. O "problema de mapa" dos handoffs anteriores era do `frontend/` antigo (Vite), não do `frontend_v2/`. Código real de produção (~500 linhas MapComponent + PropertySearch). CARTO Dark tiles, 9 camadas com zoom-lock, busca CARs, fly-to, painel overlaps, glassmorphism HUD.

**Problemas identificados:**
- `/processos` (link "DataJud" na Sidebar) → rota NÃO EXISTE → 404
- `API_URL = "http://localhost:8000/api/v1"` hardcoded sem env var
- TopBar search não tem handler (digitar não faz nada)
- "SYSTEM ONLINE 1.2ms" na Sidebar é texto fixo (não consulta API)
- DeepSearch é a página mais elaborada visualmente (gauge Recharts) mas é 100% mock

### O que NÃO existe (ZERO código)

| Feature | Status | Impacto |
|---|---|---|
| **Motor jurídico** (prescrição, teses, defesa) | ZERO | Diferencial principal |
| **Valuation** (renda capitalizada) | ZERO | Diferencial para bancos |
| **Scoring 5 eixos** (0-1000 cada) | ZERO | Diferencial competitivo |
| **Recuperação de crédito / alongamento** | ZERO | Feature financeira |
| **Contratos / checklists regulatórios** | ZERO | Fase 2 roadmap |
| **WhatsApp / alertas / monitoramento** | ZERO | Fase 4 roadmap |
| **Jurimetria ambiental** | ZERO | Ninguém no mercado faz |
| **Cadeia dominial automatizada** | ZERO | Ninguém no mercado faz |
| **Agregador de leilões rurais** | ZERO | Porta de entrada monetização |

---

## SEÇÃO 3 — PESQUISA DE MERCADO (Resumo da v3)

> Documentos completos em: `docs/ANALISE_COMPETITIVA_v2_COMPLETA.md` e `docs/PESQUISA_MERCADO_v3_EXECUTIVO.md`

### Números do mercado
- Plano Safra 2025/26: **R$ 516,2 bilhões**
- Leilões rurais 2025: **R$ 420 bilhões** monitorados, ~1.900 rurais ativos
- Processos IBAMA: **183.000** (R$ 29 bi), arrecadação de apenas 5%
- Due diligence manual: **R$ 5.000-30.000, 15-45 dias**
- Preço médio terra: **R$ 22.951,94/ha** (+28% em 2 anos)

### Concorrentes — preços reais
| Empresa | Preço | Gap que exploramos |
|---|---|---|
| AdvLabs | R$ 997-4.997/ano | Zero GIS, só ambiental admin |
| Registro Rural | R$ 149,90/mês | Zero jurídico, zero score |
| SpotSat | R$ 6-25/consulta | Detecta mas não defende |
| Softfocus | Enterprise (33% bancos) | Zero jurídico, zero valuation |
| Agrotools | ~R$ 50k+/mês | Zero jurídico, inacessível |
| Serasa Agro | Enterprise | Zero jurídico |

### 10 gaps confirmados (ninguém atende)
1. Integração jurídica + geoespacial
2. Jurimetria ambiental (% êxito por tese/tribunal)
3. Score unificado 5 eixos
4. Due diligence automatizada (minutos vs semanas)
5. Compliance multi-regulatório (MCR + EUDR + certificações)
6. Self-service para produtor ("Minha fazenda está apta?")
7. Cadeia dominial sobre mapa
8. Monitoramento integrado (admin + judicial + DOU)
9. Recuperação de crédito rural + análise jurídica
10. Base de preços de terras rurais (nenhuma API pública existe)

### 15 personas mapeadas
Bancos/cooperativas, traders/exportadores, advogados rurais, advogados respondendo auto, compradores, vendedores, corretores, agrimensores, engenheiros, produtores, fintechs, investidores, agentes públicos, gestores públicos, cidadãos.

---

## SEÇÃO 4 — FONTES DE DADOS DISPONÍVEIS

### Gratuitas e imediatas (APIs diretas)
| Fonte | Acesso | Dados |
|---|---|---|
| BCB SGS | REST sem auth | SELIC, TR, IPCA, TJLP, câmbio (600+ séries) |
| BCB SICOR OData | REST sem auth | 17 endpoints crédito rural por município/programa |
| BasedosDados | BigQuery (1TB/mês grátis) | 60+ tabelas: SICOR, CNPJ, PAM, PRODES, CAFIR, RAIS |
| Portal Transparência | REST (token grátis) | CEIS, CNEP, Garantia-Safra |
| DataJud/CNJ | API key pública | 88 tribunais |
| IBGE SIDRA | REST sem auth | PAM (5457), PPM (3939), Censo |
| CVM CKAN | REST sem auth | FIAGRO, CRA informes |
| MapBiomas GraphQL | Bearer token (cadastro grátis) | Alertas desmatamento por CAR |
| Embrapa AgroAPI | OAuth (1k req/mês grátis) | ZARC, clima, NDVI |
| SICAR WFS | Sem auth | 7.4M+ CARs, polígonos por UF |
| INPE WFS | Sem auth | DETER, PRODES (shapefiles) |
| NASA POWER | REST sem auth | Clima por coordenada desde 1981 |

### Pagas (custo baixo, alto valor)
| Fonte | Custo estimado | Dados |
|---|---|---|
| InfoSimples | ~R$ 1.010/mês (5k consultas) | IBAMA certidões, SIGEF, matriculas, protestos, PGFN |
| BigDataCorp | ~R$ 200-500/mês | Dados ambientais pré-processados (R$ 0,05/consulta) |
| SERPRO | ~R$ 200/mês | CCIR oficial, CPF/CNPJ fonte Receita |

### Cadastros que Eduardo precisa fazer (~30 min)
1. **console.cloud.google.com** — projeto GCP gratuito → desbloqueia BigQuery
2. **plataforma.alerta.mapbiomas.org** — conta gratuita → alertas desmatamento por CAR
3. **portaldatransparencia.gov.br/api-de-dados** — email → CEIS, CNEP, MTE
4. **agroapi.cnptia.embrapa.br** — conta gratuita → ZARC, ClimAPI, SATVeg
5. **InfoSimples** (opcional, pago) — ~R$ 100/mês teste → matrículas, certidões

---

## SEÇÃO 5 — ROADMAP REESTRUTURADO

> **Princípio:** Tudo é prioritário. Organizado por dependência técnica, não por "nice to have".

### Bloco 0 — Fundação de Dados (2-3 dias)
Sem dados completos, nada funciona direito.

| # | Tarefa | Prioridade | Estado |
|---|---|---|---|
| 0.1 | **Garantir mapa renderiza no browser** — testar `next dev`, diagnosticar se há problema real ou se era só o frontend antigo | CRÍTICA | Fix parcial (build passa, dev server rodou) |
| 0.2 | **DETER completo** — baixar shapefiles diretos TerraBrasilis (não WFS limitado) | CRÍTICA | 50k de 800k+ |
| 0.3 | **PRODES completo** — baixar shapefiles diretos | CRÍTICA | 50k de dataset maior |
| 0.4 | **SICAR nacional** — expandir ETL BigQuery para todos os estados OU usar WFS direto | ALTA | Só MA (308k de 79.3M) |
| 0.5 | **SIGEF restante** — completar 21 UFs faltantes | ALTA | 6 de 27 UFs |
| 0.6 | **Cadastros Eduardo** (GCP, MapBiomas, Transparência, Embrapa) | ALTA | Nenhum feito |
| 0.7 | **Configurar GCP_PROJECT_ID** — desbloqueia BigQuery inteiro | ALTA | Bloqueado |

### Bloco 1 — Compliance Real (3-5 dias)
O MCR 2.9 é obrigatório AGORA. Sem isso, bancos não compram.

| # | Tarefa | Descrição |
|---|---|---|
| 1.1 | **Calculadora MCR 2.9 auditável** | 6 critérios com pontuação, fontes, dados. Output: APTO/INAPTO/PENDENTE + checklist assinável. Endpoint: `POST /api/v1/compliance/mcr29` |
| 1.2 | **EUDR compliance report** | Cruzamento PRODES pós-2020 + CAR + coordenadas. Relatório exportável para autoridades EU |
| 1.3 | **Score 5 eixos** | fundiário (CAR+SIGEF+INCRA), ambiental (IBAMA+DETER+PRODES), trabalhista (MTE), jurídico (DataJud+embargos), financeiro (SICOR+BCB). Cada um 0-1000 |
| 1.4 | **Deep Search completo** | Busca por CAR/CPF/CNPJ/coordenada → relatório consolidando TODAS as fontes em 1 tela |

### Bloco 2 — Motor Jurídico (5-7 dias)
O diferencial que ninguém tem. Sem isso, somos mais um GIS viewer.

| # | Tarefa | Descrição |
|---|---|---|
| 2.1 | **Prescrição automática** | Dado auto de infração IBAMA: calcular prescrição administrativa (5a), criminal (12-20a), trabalhista (2a) com marcos interruptivos |
| 2.2 | **Análise de embargos** | Classificação do embargo + identificação de nulidades formais + defesa sugerida |
| 2.3 | **Base de jurisprudência** | Tabela de precedentes ambientais (STJ, TRFs) com tese, tribunal, resultado, artigo |
| 2.4 | **Teses de defesa sugeridas** | Dado o tipo de infração + dados do imóvel → sugerir teses aplicáveis com jurisprudência |
| 2.5 | **Geração de minuta** | Defesa administrativa gerada com fundamentos, legislação e jurisprudência |

### Bloco 3 — Motor Financeiro (3-5 dias)
Bancos e cooperativas precisam disso junto com MCR 2.9.

| # | Tarefa | Descrição |
|---|---|---|
| 3.1 | **Valuation simplificado** | VTN = (produtividade PAM × preço CEPEA × fator solo) / taxa capitalização BCB. Ajuste por passivos. Endpoint: `POST /api/v1/valuation/estimar` |
| 3.2 | **Calculadora saldo devedor** | Taxas reais BCB SGS (SELIC, TR, IPCA, TJLP). Input: contrato. Output: saldo real vs cobrado |
| 3.3 | **Simulador alongamento** | Cenários de renegociação com custos. PESA/PRONAF/PRONAMP |
| 3.4 | **Tabela taxas históricas** | Ingerir séries SGS para cálculos de correção monetária |
| 3.5 | **Comparador programas** | PRONAF vs PRONAMP vs recurso livre — taxa, limite, elegibilidade |

### Bloco 4 — Frontend Completo (5-7 dias)
O frontend_v2 existe mas precisa de páginas reais com dados reais.

| # | Tarefa | Descrição |
|---|---|---|
| 4.1 | **Dashboard com dados reais** | KPIs do banco, gráficos, scores visuais (gauge 0-1000) |
| 4.2 | **Mapa completo** | Todas as camadas carregando, inspector on-click, drawing tools |
| 4.3 | **Tela Deep Search** | Busca + resultado completo (compliance + jurídico + financeiro + mapa) |
| 4.4 | **Tela Compliance** | MCR 2.9 + EUDR com checklist interativo |
| 4.5 | **Tela Mercado** | Cotações CEPEA, futuros B3, SICOR por região |
| 4.6 | **Relatório PDF** | Export do due-diligence completo em PDF profissional |

### Bloco 5 — Monetização (3-5 dias)
| # | Tarefa | Descrição |
|---|---|---|
| 5.1 | **API REST documentada** | Swagger + Postman Collection para fintechs/cooperativas |
| 5.2 | **Agregador leilões rurais** | Scraping Caixa + Portal Leilão Imóvel → cruzamento com 14 camadas PostGIS |
| 5.3 | **Sistema de créditos/assinatura** | Modelo de cobrança (por consulta + SaaS mensal) |
| 5.4 | **Landing page** | Explicar o produto, converter leads |

### Bloco 6 — Escala (5-7 dias)
| # | Tarefa | Descrição |
|---|---|---|
| 6.1 | **WhatsApp bot** | Consulta por CAR, alertas de embargos |
| 6.2 | **Monitoramento contínuo** | Webhooks: novo embargo, novo desmatamento, novo processo |
| 6.3 | **Contratos agro** | Templates: arrendamento, parceria, CPR, compra/venda |
| 6.4 | **Checklists regulatórios** | Licenciamento, CAR, outorga, SIGEF — interativos |
| 6.5 | **IA avançada** | Raciocínio auditável, teses automáticas, radar prospecção |

**Estimativa total: 25-40 dias de desenvolvimento**

---

## SEÇÃO 6 — REGRAS PARA A PRÓXIMA SESSÃO

### Regras do Eduardo (invioláveis)
1. **Sem mocks** — código funcionando com dados reais, não wireframes
2. **Sem mudança de stack sem autorização** — Next.js 16 + FastAPI + PostGIS é o padrão
3. **UI em português** — público brasileiro
4. **Dark mode** — Forest/Onyx, glassmorphism, CARTO Dark tiles
5. **Consultar antes de decidir** — agentes executam, não decidem (R2)

### Regras técnicas
1. **Não confiar nos handoffs anteriores** — usar ESTE handoff como fonte de verdade
2. **Verificar no código** antes de afirmar que algo funciona
3. **Docker Desktop precisa estar rodando** antes de qualquer trabalho
4. **Testar com curl** antes de assumir que um endpoint funciona

### O que NÃO repetir
1. Não prometer "39 fontes do agrobr" — testado e tem limitações práticas
2. Não inflar números (24 tabelas reais, não 60)
3. Não marcar "Fase 0 concluída" se os dados estão parciais
4. Não documentar features como existentes se são roadmap

---

## SEÇÃO 7 — COMANDOS RÁPIDOS

```bash
# ── SUBIR AMBIENTE ──────────────────────────────────────────────────
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# ── VERIFICAR STATUS ────────────────────────────────────────────────
curl -s http://localhost:8000/health | python -m json.tool

# ── TESTAR RELATÓRIO ────────────────────────────────────────────────
curl -s -X POST http://localhost:8000/api/v1/report/due-diligence \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2102101-10D7FC904AA2437FBEAD782C13E8AF21"}' | python -m json.tool

# ── FRONTEND ────────────────────────────────────────────────────────
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus/frontend_v2"
npm run dev
# Abrir http://localhost:3000/mapa

# ── BANCO DIRETO ────────────────────────────────────────────────────
docker exec -it agrojus-db-1 psql -U agrojus -d agrojus
# \dt = listar tabelas
# SELECT count(*) FROM environmental_alerts;

# ── SWAGGER ─────────────────────────────────────────────────────────
# http://localhost:8000/docs

# ── GIT ─────────────────────────────────────────────────────────────
# Branch: claude/continue-backend-dev-sVLGG
# Repo: https://github.com/eduardopasouza/Claude
```

---

## SEÇÃO 8 — ESTRUTURA DE ARQUIVOS

```
agrojus/
├── docker-compose.yml
├── backend/
│   ├── app/
│   │   ├── main.py                    ← FastAPI app
│   │   ├── config.py                  ← API keys, URLs
│   │   ├── api/
│   │   │   ├── property.py            ← busca, GeoJSON, overlaps
│   │   │   ├── report.py              ← due-diligence, buyer, lawyer, investor, PDF
│   │   │   ├── dashboard.py           ← materialized view
│   │   │   ├── geo.py                 ← analyze-point, layers GeoJSON
│   │   │   ├── consulta.py            ← dossiê CPF/CNPJ
│   │   │   ├── compliance.py          ← MCR 2.9 básico (6 checks), EUDR
│   │   │   ├── auth.py, market.py, smart_search.py, search.py
│   │   │   ├── lawsuits.py, jurisdicao.py, monitoring.py, news.py, map_data.py
│   │   │   └── __init__.py
│   │   ├── services/
│   │   │   ├── postgis_analyzer.py    ← 14 camadas espaciais
│   │   │   ├── compliance.py          ← MCR/EUDR checks
│   │   │   ├── earth_engine.py        ← LULC, fogo, solo, água
│   │   │   ├── mapbiomas_alerta.py    ← GraphQL alertas
│   │   │   ├── due_diligence.py       ← pipeline PostGIS-first
│   │   │   └── pdf_report.py          ← PDF
│   │   └── models/
│   │       ├── schemas.py
│   │       └── database.py
│   ├── scripts/                       ← 28 scripts ETL
│   └── requirements.txt
├── frontend/                          ← IGNORAR (Vite vanilla, scaffold vazio)
├── frontend_v2/                       ← FRONTEND REAL
│   ├── src/
│   │   ├── app/
│   │   │   ├── (dashboard)/           ← layout + 6 páginas
│   │   │   ├── login/
│   │   │   ├── layout.tsx, globals.css
│   │   ├── components/
│   │   │   ├── mapa/MapComponent.tsx   ← Leaflet 9 camadas
│   │   │   ├── mapa/PropertySearch.tsx ← Busca + overlaps
│   │   │   ├── layout/Sidebar.tsx, TopBar.tsx, CommandPalette.tsx
│   │   │   └── ui/ (button, command, dialog, input, textarea)
│   │   └── lib/api.ts, utils.ts
│   ├── next.config.ts (turbopack.root: ".")
│   ├── package.json
│   └── tsconfig.json
└── docs/                              ← 15+ documentos (muitos desatualizados)
```

---

## SEÇÃO 9 — DECISÕES PENDENTES DO EDUARDO

1. **Fazer os 5 cadastros gratuitos** (GCP, MapBiomas, Transparência, Embrapa, InfoSimples) — ~30 min, desbloqueia BigQuery + alertas + CEIS/CNEP + ZARC
2. **WhatsApp — Twilio ou Meta Cloud API?**
3. **IA para motor jurídico — Claude API ou OpenAI?** (Recomendação: Claude para raciocínio auditável)
4. **InfoSimples — contratar?** (~R$ 100/mês teste, desbloqueia matrículas e certidões)
5. **Modelo de precificação** — assinatura + créditos? Freemium? Enterprise?

---

## SEÇÃO 10 — O QUE A PRÓXIMA SESSÃO DEVE FAZER

**Ordem de execução:**

1. **Subir Docker** e confirmar que backend responde
2. **Abrir frontend_v2 no browser** e confirmar que mapa renderiza
3. **Se mapa não renderizar:** diagnosticar e consertar (problema provável: Leaflet CSS ou container height)
4. **Começar Bloco 0:** baixar DETER/PRODES completos, expandir SICAR
5. **Começar Bloco 1:** implementar Calculadora MCR 2.9 real (não o checklist básico)
6. **Começar Bloco 2:** motor jurídico — prescrição + teses
7. **Testar tudo com curl** antes de marcar como feito

**Meta:** Ao final da próxima sessão, ter MCR 2.9 real + prescrição automática + dados completos + mapa funcionando. Isso é o MVP que separa o AgroJus de um GIS viewer genérico.

---

*AgroJus — Handoff Sessão 5 — 2026-04-16 BRT*
*Este handoff substitui todos os anteriores. Use como fonte de verdade.*
