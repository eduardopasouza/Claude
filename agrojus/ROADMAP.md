# AgroJus — Roadmap Consolidado (2026-04-17 · pós-Sessão 9)

> Atualizado após Sessão 9. Sincronizado com `docs/HANDOFF_2026-04-17_sessao9.md`.

## Estado atual do produto (pós-sessão 9)

| Camada | Completo | Parcial | Ausente |
|---|---|---|---|
| Backend | ~100 endpoints · 18 camadas PostGIS · DJEN · DataJud · Embrapa (7/9) · MapBiomas Alerta GraphQL · IBGE choropleth (16 métricas) · IBAMA 16k autos · **Webhooks CRUD + dispatch** · **Laudo PDF ficha** · **Exports GeoJSON/GPKG/SHP** · **Minuta Claude API** | MCR 2.9 (6/30 critérios) · SICAR MA-only (faltam 79M) · DETER/PRODES parcial (800k+ real) | Motor jurídico STJ · valuation · leilões · Portal Transparência coletor · dados.gov.br coletores |
| Frontend | `/login`, `/`, `/mapa` v2, `/mercado`, `/processos`, `/publicacoes`, **`/imoveis/[car]` 12/12 abas** | `/consulta`, `/compliance` standalone, `/alertas` (mocks) | `/valuation`, `/portfolio`, `/leiloes`, `/teses`, `/minutas`, `/perfil`, `/plano`, `/equipe`, `/radar-ibama` |
| Dados | 18 camadas PostGIS × 7.7M registros · 42 pub DJEN · alertas MapBiomas tempo real · **webhooks + deliveries persistidos** | SICAR (só MA) · DETER/PRODES (50k vs 800k+) | Earth Engine · SIGMINE · ANA outorgas · SNCI · CNES |
| Docs | HANDOFF sessões 1-9 · ROADMAP · README · 48 auditorias visuais · 6 blueprints detalhados · SYNTHESIS | — | Manual do usuário · API pública doc |

---

## 8 Sprints (~43 dias) — progresso

### Sprint 1 — Ativação rápida (3 dias) ✅ **CONCLUÍDO**
Destravou múltiplas camadas com pouco código.
- [x] Descobrir paths Embrapa (via Swagger + OAuth2) — **7/9 APIs funcionais**
- [x] Coletor IBGE choropleth — **16 métricas ativas, 14 camadas saíram de stub**
- [x] Coletor IBAMA dados abertos — **16.121 autos carregados**
- [x] Coletor MapBiomas Alerta GraphQL — **JWT + query alerts por CAR**

### Sprint 2 — Ficha do imóvel `/imoveis/[car]` ✅ **12/12 ABAS CONCLUÍDAS**
A tela mais importante do produto está **completa**.
- [x] **Sprint 2a** — scaffold + 4 abas (Visão · Dossiê · Histórico · Agronomia)
- [x] **Sprint 2b** — +3 abas (Compliance · Clima · Jurídico)
- [x] **Sprint 2c** — +3 abas (Valuation · Logística · Crédito) + MapPreview header
- [x] **Sprint 2d** — ferramentas de mapa: point analysis + draw polygon + upload KML/GeoJSON + fix choropleth quintis
- [x] **Sprint 2e** (sessão 9) — **Monitoramento** (webhooks CRUD + dispatch async + logs) e **Ações** (laudo PDF reportlab + GeoJSON/GPKG/SHP via geopandas + minuta Claude API)

### Sprint Market ✅ **CONCLUÍDO (sessão 8)**
Tela `/mercado` reescrita com foco na UF do usuário + integração no mapa.
- [x] Collector Agrolink (13 commodities × até 26 UFs × até 265 meses)
- [x] `/mercado` UX centrada: UFPicker + cards por commodity + gráfico histórico
- [x] `/noticias` feed RSS agro (3 filtros: Todas · Mercado · Jurídico)
- [x] Widget "Colorir por preço" no mapa (10 camadas choropleth preço UF)
- [x] Zoom +/- no MapPreview (ficha do imóvel)
- [x] Remoção de todas as indicações de fonte no frontend

### Sprint 3 — Compliance MCR 2.9 expandido ✅ **CONCLUÍDO (sessão 9)**
De 6 para **32 critérios** auditáveis em 5 eixos.
- [x] Backend: 8 fundiários (CAR + SIGEF + TI + UC + SIGMINE + CCIR + ITR + SPU)
- [x] Backend: 8 ambientais (PRODES + DETER + MapBiomas + embargos + autos IBAMA + RL + APP + ANA)
- [x] Backend: 6 trabalhistas (MTE lista suja + CNDT + CAGED + eSocial + NR-31 + CIPATR)
- [x] Backend: 5 jurídicos (DataJud + DJEN + protestos + CNJ + execução fiscal)
- [x] Backend: 5 financeiros (SICOR + CEIS + CNEP + PIX + CCIR)
- [x] Frontend: `/compliance` com checklist interativo + laudo PDF
- [x] Integração com aba Compliance da ficha do imóvel

**Status dos 32 critérios** (pós-Sprint 3):
- 13 com dados reais integrados (41%) — verificação automática
- 19 com status `pending` aguardando Sprint 4 (dados.gov.br) e fontes que exigem integração adicional (CCIR, ITR, CNDT, CEIS/CNEP via Portal Transparência, protestos CENPROT, SPU, SIGMINE, etc.)

### Sprint 4 — 10 coletores dados.gov.br ✅ **CONCLUÍDO (sessão 9)**
Infraestrutura de ingestão + 2 ETLs reais executados.
- [x] Base clients CKAN + Portal Transparência
- [x] 12 modelos PostGIS + log de ingestão
- [x] 10 loaders unificados (sigmine · ana_outorgas · ana_bho · assentamentos · quilombolas · aneel_usinas · aneel_linhas · garantia_safra · ceis · cnep)
- [x] Script master com --all / --only / --status
- [x] Endpoints REST `/api/v1/dados-gov/*` (loaders, status, stats, run)
- [x] Página admin `/dados-gov` frontend com execução inline
- [x] **CEIS** populado com 3.000 registros reais
- [x] **CNEP** populado com 1.620 registros reais
- [x] MCR 2.9 — critérios F05, A08, FI02, FI03 consumindo dados reais

**Status dos loaders** (pós-iteração sessão 9):

| Loader | Status | Registros |
|---|---|---:|
| CEIS | ✅ ativo | 3.000 |
| CNEP | ✅ ativo | 1.620 |
| INCRA Assentamentos | ✅ ativo | 8.214 |
| INCRA Quilombolas | ✅ ativo | 427 |
| ANEEL SIGA usinas | ✅ ativo | 25.417 |
| ANEEL Linhas SIGET | ✅ ativo | 176 |
| IBAMA Termos de Embargo | ✅ ativo | 88.586 |
| **IBAMA Autos de Infração (SIFISC)** | ✅ ativo | **695.439** |
| SIGMINE | ❌ ANM em 502 (externo) | 0 |
| ANA Outorgas | ❌ sem URL CSV estável | 0 |
| ANA BHO | ❌ sem URL CSV estável | 0 |
| Garantia-Safra | ❌ token sem permissão CGU | 0 |
| IBAMA CTF | ❌ dataset específico não identificado | 0 |

**Total operacional**: **822.879 registros reais em 8/12 tabelas**. O fallback automático em `KNOWN_RESOURCES` permite que loaders pendentes sejam ativados adicionando URLs novas sem reescrever código.

### Sprint 5 — Mapa v3 (4 dias) — padrões SYNTHESIS ⏳
- [ ] URL state serializado (Zustand + useSearchParams)
- [ ] Drill-down UF → Município breadcrumb
- [ ] Slider temporal duplo (início/fim YYYY-MM)
- [ ] Legenda dinâmica painel direito com "Ver só esta"
- [ ] Tabs laterais (Camadas/Filtros/Mapa/Exportar)
- [ ] Opacidade por camada
- [ ] Export GeoJSON/CSV/Shapefile/PDF

### Sprint 6 — Motor jurídico base (5 dias) ⏳
- [ ] STJ dados abertos + TCU webservice → tabela `jurisprudencia`
- [ ] Embedding bge-m3 (modelo em mia-project)
- [ ] Busca híbrida vetorial+textual
- [ ] Tela `/teses` com citações verificáveis

### Sprint 7 — Gerador de minutas (7 dias) ⏳
- [ ] Claude API integration
- [ ] Redação com fundamentação
- [ ] Verificação anti-alucinação contra base jurisprudência
- [ ] Tela `/minutas` + export DOCX

### Sprint 8 — Agregador de leilões (10 dias) ⏳
- [ ] Scrapers (Caixa, Spy, Portal Leilão, TJs)
- [ ] Deduplicação + classificação rural
- [ ] Parser LLM edital (red flags)
- [ ] Enriquecimento geo
- [ ] Timeline do lote (1ª → 2ª → 3ª praça)
- [ ] Alertas WhatsApp/email/webhook

---

## Dívida técnica (paralelo aos sprints)

- [ ] OpenAPI codegen → types TypeScript (`openapi-typescript`)
- [ ] State global Zustand
- [ ] Middleware auth frontend (Next middleware.ts)
- [ ] JWT httpOnly cookie (remover localStorage — XSS risk)
- [ ] Error boundaries (`app/error.tsx`)
- [ ] Testes Vitest + Playwright (mínimo MapComponent + PropertySearch + login)
- [ ] Storybook para design system
- [ ] Alembic migrations (substituir `create_tables`)
- [ ] Redis para rate_limiter + monitoring persistido
- [ ] Logger Sentry/Axiom
- [ ] Analytics PostHog/Plausible
- [ ] Dark/Light toggle completo + tema Gov.br opcional

---

## Camadas adicionais a ativar quando backlog permitir

- [ ] NDVI histórico SATVeg (Embrapa)
- [ ] ONR matrículas (via InfoSimples pago — aba documental, não é layer de mapa)
- [ ] SNCI legado (download manual + ETL)
- [ ] SPU Terras União
- [ ] ZEE por estado (9 UFs diferentes)
- [ ] ANAC aeroportos
- [ ] Terminais intermodais ANTT/ANTAQ
- [ ] CNT condição rodovias

---

## Métricas de sucesso

| Fase | Objetivo | Status |
|---|---|---|
| Sprint 1-2 | Ficha do imóvel funcional com score de compliance | ✅ (10/12 abas + toolbar mapa + MapPreview) |
| Sprint Market | /mercado regionalizado + notícias + choropleth de preço | ✅ (13 commodities × 26 UFs) |
| Sprint 3-5 | 50+ camadas ativas + mapa v3 | 42 ativas (35%) · quintis ✅ · AOI custom ✅ · preço UF ✅ |
| Sprint 6-8 | Produto demonstrável end-to-end: motor jurídico + leilões + webhook | ⏳ |
| Longo prazo | 100% das 119 camadas ativadas ou marcadas "não viáveis sem parceria" | ⏳ |

---

## Decisões técnicas já tomadas (não questionar sem motivo plausível)

- Monolítico modular em FastAPI
- PostGIS 3.4 com GIST em todas geometrias
- SQLAlchemy 2.0 sync (não async) — simplicidade
- JWT stateless (localStorage dev, httpOnly cookie em prod)
- Cache SHA256 em disco com TTL 24h padrão
- Materialized view para dashboard
- Next.js App Router com grupo `(dashboard)`
- Tailwind v4 + shadcn/ui
- react-leaflet 5 + CARTO Dark default
- SWR 2.4 para data fetching
- Docker Compose 2 containers + volume named `agrojus_pgdata`

---

*Documento vivo. Atualizar ao fim de cada sprint.*
