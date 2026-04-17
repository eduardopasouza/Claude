# AgroJus — Roadmap Consolidado (2026-04-17)

> Substitui roadmaps anteriores. Sincronizado com `docs/HANDOFF_2026-04-17_sessao6.md`.

## Estado atual do produto

| Camada | Completo | Parcial | Ausente |
|---|---|---|---|
| Backend | 71 endpoints, 17 camadas PostGIS, DJEN, DataJud, Embrapa OAuth | Embrapa paths individuais, coletores dados.gov.br | Motor jurídico, agregador leilões, valuation, MCR expandido |
| Frontend | /login, /mapa v2, /mercado, /processos, /publicacoes | /consulta, /compliance, /alertas (mocks) | /imoveis/[car], /valuation, /portfolio, /teses, /minutas, /leiloes, /perfil |
| Dados | 17 camadas × 7M registros | SICAR 350k (faltam 79M), DETER/PRODES 50k (real 800k+) | Embrapa, dados.gov.br, ANA, SIGMINE, Earth Engine |
| Docs | Auditoria 48 sites + SYNTHESIS + 6 blueprints detalhados | — | Manual do usuário, API pública doc |

## 8 Sprints próximos (~43 dias)

### Sprint 1 — Ativação rápida (3 dias)
Destrava múltiplas camadas com pouco código.
- [ ] Descobrir paths Embrapa (5 min Eduardo + ajuste coletor)
- [ ] Coletor IBGE choropleth (endpoint + 14 camadas stub ativadas)
- [ ] Coletor IBAMA dados abertos (autos + embargos + CTF)
- [ ] Coletor MapBiomas Alerta GraphQL (credenciais prontas)

### Sprint 2 — Ficha do imóvel (5 dias)
**Rota mais importante que ainda não existe.** Blueprint em `docs/research/analise-agronomica-integrada.md`.
- [ ] `/imoveis/[car]` scaffold + 12 abas
- [ ] Abas 2a: Visão · Compliance · Dossiê · Histórico · Produção · Clima
- [ ] Abas 2b: Valuation · Logística · Jurídico · Crédito · Monitoramento · Ações

### Sprint 3 — Compliance MCR 2.9 expandido (5 dias)
- [ ] Backend: de 6 para 30 validações auditáveis
- [ ] Backend: EUDR 4 critérios completos
- [ ] Frontend `/compliance` real com checklist interativo + score 5 eixos + PDF

### Sprint 4 — 10 coletores dados.gov.br (4 dias)
Guia em `docs/research/dados-gov-guia.md` com 32 datasets priorizados.
- [ ] IBAMA autos/embargos/CTF
- [ ] Garantia-Safra, SIGMINE, ANA outorgas+BHO
- [ ] Assentamentos INCRA, Quilombolas
- [ ] ANEEL usinas + linhas transmissão

### Sprint 5 — Mapa v3: padrões prioritários SYNTHESIS (4 dias)
- [ ] URL state serializado (Zustand + useSearchParams)
- [ ] Drill-down UF → Município breadcrumb
- [ ] Slider temporal duplo
- [ ] Legenda dinâmica painel direito ("Ver só esta")
- [ ] Tabs laterais (Camadas/Filtros/Mapa/Exportar)
- [ ] Opacidade por camada

### Sprint 6 — Motor jurídico base (5 dias)
- [ ] STJ dados abertos + TCU webservice → tabela `jurisprudencia`
- [ ] Embedding bge-m3 (modelo em mia-project)
- [ ] Busca híbrida vetorial+textual
- [ ] Tela `/teses` com citação verificável

### Sprint 7 — Gerador de minutas (7 dias)
- [ ] Claude API integration
- [ ] Redação com fundamentação
- [ ] Verificação anti-alucinação contra base
- [ ] Tela `/minutas` + export DOCX

### Sprint 8 — Agregador de leilões (10 dias)
- [ ] Scrapers Caixa + Spy + Portal Leilão + TJs
- [ ] Deduplicação + classificação rural
- [ ] Parser LLM edital (red flags)
- [ ] Enriquecimento geo
- [ ] Timeline do lote
- [ ] Alertas WhatsApp + email + webhook

## Dívida técnica a resolver (paralelo aos sprints)

- [ ] OpenAPI codegen → types TypeScript
- [ ] State global Zustand
- [ ] Middleware auth frontend (Next middleware.ts)
- [ ] JWT httpOnly cookie (remover localStorage)
- [ ] Error boundaries (app/error.tsx)
- [ ] Testes Vitest + Playwright (mínimo MapComponent + PropertySearch + login)
- [ ] Storybook para design system
- [ ] Alembic migrations (substituir create_tables)
- [ ] Redis para rate_limiter + monitoring persistido
- [ ] Logger Sentry/Axiom
- [ ] Analytics PostHog/Plausible
- [ ] Dark/Light toggle completo + tema Gov.br opcional

## Camadas específicas a adicionar quando backlog permitir

- [ ] NDVI histórico SATVeg
- [ ] ONR matrículas (via InfoSimples pago — não é camada de mapa, é aba documental)
- [ ] SNCI legado (download manual + ETL)
- [ ] SPU Terras União
- [ ] ZEE por estado (9 UFs diferentes)
- [ ] ANAC aeroportos
- [ ] Terminais intermodais ANTT/ANTAQ
- [ ] CNT condição rodovias (por solicitação)

## Métricas de sucesso

- Objetivo curto (fim Sprint 5): 50+ camadas ativas no mapa (~42% do catálogo)
- Objetivo médio (fim Sprint 8): produto demonstrável end-to-end (mapa + ficha imóvel + compliance + motor jurídico + leilões)
- Objetivo longo: 100% das 119 camadas ativadas ou marcadas explicitamente como "não viáveis sem parceria"

---

*Documento vivo. Atualizar ao fim de cada sprint.*
