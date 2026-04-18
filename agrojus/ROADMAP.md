# AgroJus — Roadmap Consolidado (2026-04-17)

> Atualizado após Sessão 7. Sincronizado com `docs/HANDOFF_2026-04-17_sessao7.md`.

## Estado atual do produto (pós-sessão 7)

| Camada | Completo | Parcial | Ausente |
|---|---|---|---|
| Backend | ~90 endpoints · 18 camadas PostGIS · DJEN · DataJud · Embrapa (7/9) · MapBiomas Alerta GraphQL · IBGE choropleth (16 métricas) · IBAMA 16k autos | MCR 2.9 (6/30 critérios) · SICAR MA-only (faltam 79M) · DETER/PRODES parcial (800k+ real) | Motor jurídico STJ · valuation · leilões · Portal Transparência coletor · dados.gov.br coletores |
| Frontend | `/login`, `/`, `/mapa` v2, `/mercado`, `/processos`, `/publicacoes`, **`/imoveis/[car]` 7/12 abas** | `/consulta`, `/compliance` standalone, `/alertas` (mocks) | `/valuation`, `/portfolio`, `/leiloes`, `/teses`, `/minutas`, `/perfil`, `/plano`, `/equipe`, `/radar-ibama` |
| Dados | 18 camadas PostGIS × 7.7M registros · 42 pub DJEN · alertas MapBiomas tempo real | SICAR (só MA) · DETER/PRODES (50k vs 800k+) | Earth Engine · SIGMINE · ANA outorgas · SNCI · CNES |
| Docs | HANDOFF sessões 1-7 · ROADMAP · README · 48 auditorias visuais · 6 blueprints detalhados · SYNTHESIS | — | Manual do usuário · API pública doc |

---

## 8 Sprints (~43 dias) — progresso

### Sprint 1 — Ativação rápida (3 dias) ✅ **CONCLUÍDO**
Destravou múltiplas camadas com pouco código.
- [x] Descobrir paths Embrapa (via Swagger + OAuth2) — **7/9 APIs funcionais**
- [x] Coletor IBGE choropleth — **16 métricas ativas, 14 camadas saíram de stub**
- [x] Coletor IBAMA dados abertos — **16.121 autos carregados**
- [x] Coletor MapBiomas Alerta GraphQL — **JWT + query alerts por CAR**

### Sprint 2 — Ficha do imóvel `/imoveis/[car]` ✅ **10/12 ABAS CONCLUÍDAS**
A tela mais importante do produto agora existe.
- [x] **Sprint 2a** — scaffold + 4 abas (Visão · Dossiê · Histórico · Agronomia)
- [x] **Sprint 2b** — +3 abas (Compliance · Clima · Jurídico)
- [x] **Sprint 2c** — +3 abas (Valuation · Logística · Crédito) + MapPreview header
- [x] **Sprint 2d** — ferramentas de mapa: point analysis + draw polygon + upload KML/GeoJSON + fix choropleth quintis
- [ ] **Sprint 2e** — 2 abas restantes (Monitoramento webhooks · Ações laudo PDF/DOCX)

### Sprint 3 — Compliance MCR 2.9 expandido (5 dias) ⏳
De 6 para 30 critérios auditáveis + EUDR expandido.
- [ ] Backend: 8 checks fundiários (CAR + SIGEF + TI + UC + SIGMINE + ...)
- [ ] Backend: 8 ambientais (PRODES + DETER + MapBiomas + embargos + autos IBAMA + ...)
- [ ] Backend: 6 trabalhistas (MTE lista suja + CNDT + CAGED + ...)
- [ ] Backend: 5 jurídicos (DataJud + DJEN + protestos + CNES + ...)
- [ ] Backend: 5 financeiros (SICOR + CEIS + CNEP + ...)
- [ ] Frontend: `/compliance` com checklist interativo + PDF

### Sprint 4 — 10 coletores dados.gov.br (4 dias) ⏳
Guia em `docs/research/dados-gov-guia.md` com 32 datasets priorizados.
- [ ] IBAMA embargos polígonos + CTF
- [ ] Garantia-Safra beneficiários
- [ ] SIGMINE processos minerários
- [ ] ANA outorgas + BHO (bacias hidrográficas)
- [ ] INCRA assentamentos + Quilombolas
- [ ] ANEEL usinas + linhas transmissão
- [ ] CEIS + CNEP (Portal Transparência)

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
| Sprint 1-2 | Ficha do imóvel funcional com score de compliance | ✅ atingido (10/12 abas + toolbar mapa) |
| Sprint 3-5 | 50+ camadas ativas (~42% do catálogo) + mapa v3 | 32 ativas (27%) · choropleth com quintis ✅ · AOI custom ✅ |
| Sprint 6-8 | Produto demonstrável end-to-end: mapa + ficha + compliance + motor jurídico + leilões | ⏳ |
| Longo prazo | 100% das 119 camadas ativadas ou marcadas "não viáveis sem parceria" | ⏳ |

---

## Decisões técnicas já tomadas (não questionar sem motivo)

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
