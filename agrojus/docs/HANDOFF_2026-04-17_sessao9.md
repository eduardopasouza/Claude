# AgroJus — Handoff Sessão 9 (2026-04-17)

> **Substitui o handoff da sessão 8.**
> Sessão 9: **Sprint 2e** — fecha ficha do imóvel 12/12 (Monitoramento webhooks + Ações laudo PDF/exports/minuta Claude).

---

## 1. O QUE FOI FEITO NESTA SESSÃO

### 1.1 Sistema de Webhooks — dispatch em tempo real ✅

**Problema:** alertas do monitoramento só ficavam em memória no singleton `MonitoringService`. Nenhum canal externo (Slack, n8n, Zapier, bot interno) recebia notificação.

**Implementação backend**
- 2 tabelas novas em Postgres: `webhooks`, `webhook_deliveries`
- Service `app/services/webhook_dispatcher.py` com `dispatch()` async, filtros por `event_type` + `car_code` + `cpf_cnpj`, assinatura HMAC-SHA256 opcional, timeout configurável
- Router `app/api/webhooks.py` em `/api/v1/webhooks`:
  - `GET /webhooks` — lista
  - `POST /webhooks` — cria (retorna secret em plain text apenas 1x)
  - `GET /webhooks/{id}` — detalhe (secret mascarado)
  - `PUT /webhooks/{id}` — atualiza
  - `DELETE /webhooks/{id}` — remove (cascade deliveries)
  - `POST /webhooks/{id}/test` — dispara payload sintético
  - `GET /webhooks/{id}/deliveries?limit=20` — logs paginados
  - `GET /webhooks/event-types` — lista 9 event types
- `MonitoringService._record_alert()` substitui `self._alerts.append()` direto e dispara webhooks em background task (non-blocking)

**9 event types suportados**
```
mapbiomas_alert, deter_alert, prodes_alert,
ibama_embargo, ibama_auto,
djen_publicacao, datajud_movimento,
car_status_change, slave_labour
```

**Validação**: `curl -X POST .../test` com `httpbin.org` retornou 200, delivery persistida com duration_ms, status_code, payload JSON.

### 1.2 Aba Ações — 5 endpoints backend + UI ✅

**Endpoints em `/api/v1/property`:**
1. `GET /{car}/laudo.pdf` — reportlab A4, 2 páginas, seções: identificação, sobreposições com destaque para TI/embargos/autos, crédito rural, avisos. Consumo interno via SQL.
2. `GET /{car}/export.geojson` — FeatureCollection EPSG:4326 (CAR + overlaps)
3. `GET /{car}/export.gpkg` — GeoPackage SQLite com 1 layer por tipo (geopandas, sem ogr2ogr)
4. `GET /{car}/export.shp.zip` — Shapefile ESRI zipado (1 .shp por layer)
5. `POST /{car}/minuta` — Claude API via anthropic SDK. Tipos: notificação extrajudicial, ação anulatória, defesa administrativa, contrarrazões, livre. 501 com mensagem amigável se `ANTHROPIC_API_KEY` ausente.

**Service `services/minuta_generator.py`**
- System prompt especializado em direito agrário/ambiental brasileiro (Lei 9.605/98, Dec 6.514/08, CF/88, CC, CPC)
- **Anti-alucinação**: proibido inventar números de acórdãos — lacunas explícitas `[buscar precedente]` quando contexto não fornece
- Contexto montado com: CAR, município, UF, área, overlaps críticos, processos informados pelo advogado, observações

### 1.3 Ficha do imóvel 12/12 abas ✅

**Novas tabs frontend:**
- `MonitoramentoTab.tsx` — form cadastro (9 events como chips toggleáveis) + secret HMAC com botão copiar + lista webhooks com ações (testar, pausar, logs, remover) + drawer expansível de deliveries auto-refresh 15s
- `AcoesTab.tsx` — 4 export cards (PDF/GeoJSON/GPKG/SHP) com download via blob (mantém Bearer) + painel minuta integrado (select tipo, destinatário, processos, observações, resultado markdown com tokens + copiar + download .md)

`page.tsx` atualizado: `implemented: true` em ambas + imports + renders.

### 1.4 Fix — UNION types no SQL

`_fetch_property_base` fazia `UNION` entre `sicar_completo.cod_municipio_ibge` (integer) e `geo_car.cod_municipio_ibge` (text). Fix: `::text` cast em ambos.

### 1.5 Requirements + config

- `anthropic>=0.45.0` em `requirements.txt`
- Novas settings: `anthropic_api_key`, `anthropic_model="claude-opus-4-7"`, `webhook_timeout_seconds=10`, `webhook_max_retries=3`
- **Eduardo**: adicionar `ANTHROPIC_API_KEY=sk-ant-...` em `backend/.env` para ativar minuta.

---

## 2. ESTADO REAL DO PRODUTO (pós-sessão 9)

### Backend — FastAPI + PostGIS
**~100 endpoints** em 24 routers. Camadas PostGIS: **18 ativas** + **10 choropleth preço UF** + **16 choropleth IBGE** + **4 choropleth UF SIDRA** = **48 camadas renderáveis no mapa**.

### Frontend — Next.js 16.2.3

| Rota | Status |
|---|---|
| `/` dashboard | ✅ KPIs |
| `/login` | ✅ JWT |
| `/mapa` | ✅ 42+ camadas · widget preço · draw/upload/analyze · quintis |
| `/imoveis/[car]` | ✅ **12/12 abas + laudo PDF + exports + minuta** |
| `/mercado` | ✅ UFPicker + 13 commodities + gráfico histórico |
| `/noticias` | ✅ feed RSS agro |
| `/publicacoes` | ✅ DJEN real (42 do Eduardo) |
| `/processos` | ✅ DataJud CNJ |
| `/consulta` | ⚠ DeepSearch mock |
| `/compliance`, `/alertas` | ⚠ mocks standalone |

### Dados no Postgres (7.7M+ registros, inalterado)

**Adicionado nesta sessão:** 2 tabelas novas (`webhooks`, `webhook_deliveries`) vazias aguardando uso em produção.

---

## 3. PENDÊNCIAS (ordenadas por ROI)

### 🔴 CRÍTICAS

1. **Compliance MCR 2.9 expandido (6 → 30 critérios)** — Sprint 3. Hoje só 6 checks básicos. Eduardo quer 30 auditáveis em 5 eixos (8 fundiários, 8 ambientais, 6 trabalhistas, 5 jurídicos, 5 financeiros). Frontend `/compliance` standalone (hoje mock) com checklist interativo + PDF.
2. **Motor jurídico base (Sprint 6)** — STJ dados abertos + TCU webservice → tabela `jurisprudencia`. Embedding bge-m3. Busca híbrida vetorial+textual. Rota `/teses` com citação verificável. **Dá base para minuta de qualidade superior.**
3. **`/alertas` standalone real** — hoje 4 mocks hardcoded. Consumir `/api/v1/monitoring/*` + integrar com webhooks da ficha.

### 🟠 ALTAS

4. **10 coletores dados.gov.br** (guia em `docs/research/dados-gov-guia.md`): IBAMA embargos polígonos, Garantia-Safra, SIGMINE, ANA outorgas+BHO, INCRA assentamentos+Quilombolas, ANEEL, CEIS+CNEP.
5. **Ficha do proprietário** `/proprietarios/[cpf_cnpj]` — dado CPF/CNPJ lista todos CARs + resumo consolidado.
6. **Mapa v3** — URL state (Zustand + useSearchParams), drill-down UF→Município, slider temporal, opacidade por camada, tabs laterais, export da view.

### 🟡 MÉDIAS

7. Webhook retries com backoff exponencial (hoje: 1 tentativa)
8. Webhook dashboard `/webhooks` standalone (UI global, não só por imóvel)
9. Minuta em DOCX (hoje só markdown) — Sprint 7 amplia
10. Cotações regionais com menos UF (suínos/ovinos/laranja)
11. Fallback UF vizinha no `/mercado`
12. Histórico por praça específica (cidade dentro da UF no Agrolink)
13. Dashboard proprietário (CARs favoritos)
14. Notificações in-app no TopBar
15. Mobile responsive fino

### 🟢 DÍVIDA TÉCNICA

16. OpenAPI codegen → types TypeScript
17. State global Zustand (hoje prop drilling)
18. Middleware auth frontend (Next middleware.ts)
19. JWT httpOnly cookie (remover localStorage)
20. Error boundaries (`app/error.tsx`)
21. Testes Vitest + Playwright (ao menos MapComponent + PropertySearch + login)
22. Alembic migrations (substituir `create_tables`)
23. Redis para rate_limiter + monitoring persistido
24. Logger Sentry/Axiom + Analytics PostHog
25. Dark/Light toggle completo + tema Gov.br opcional
26. Storybook para design system

### 🔵 Camadas específicas (backlog)

27. NDVI histórico SATVeg (Embrapa)
28. ONR matrículas (via InfoSimples pago)
29. SNCI legado + SPU + ZEE por estado + ANAC + ANTT/ANTAQ + CNT

---

## 4. CREDENCIAIS (em backend/.env)

```bash
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
MAPBIOMAS_PASSWORD=1qasw23edFR$
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
EMBRAPA_CONSUMER_SECRET=eDJph7PEE9xKDor739rgXwcUc0ca
DADOS_GOV_TOKEN=eyJhbGc...
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==

# NOVO nesta sessão (Sprint 2e):
# ANTHROPIC_API_KEY=sk-ant-...   ← adicionar para ativar minuta Claude
```

---

## 5. COMANDOS RÁPIDOS

```bash
cd C:\dev\agrojus-workspace\agrojus
docker compose up -d
curl http://localhost:8000/health

# Testar ficha completa 12/12 via API
CAR="MA-2100055-0013026E975B48D9B4F045D7352A1CB9"

# Laudo PDF
curl -o laudo.pdf "http://localhost:8000/api/v1/property/$CAR/laudo.pdf"

# Exports geoespaciais
curl -o car.geojson "http://localhost:8000/api/v1/property/$CAR/export.geojson"
curl -o car.gpkg    "http://localhost:8000/api/v1/property/$CAR/export.gpkg"
curl -o car.shp.zip "http://localhost:8000/api/v1/property/$CAR/export.shp.zip"

# Minuta (requer ANTHROPIC_API_KEY)
curl -X POST "http://localhost:8000/api/v1/property/$CAR/minuta" \
  -H "Content-Type: application/json" \
  -d '{"tipo":"notificacao_extrajudicial","observacoes":"..."}'

# Webhook CRUD
curl -X POST http://localhost:8000/api/v1/webhooks \
  -H "Content-Type: application/json" \
  -d "{\"name\":\"slack\",\"url\":\"https://hooks.slack.com/...\",\"event_types\":[\"mapbiomas_alert\"],\"car_filter\":\"$CAR\"}"

# Testar delivery
curl -X POST http://localhost:8000/api/v1/webhooks/1/test
curl "http://localhost:8000/api/v1/webhooks/1/deliveries"

# Frontend
cd frontend_v2 && npm run dev
# http://localhost:3000/imoveis/$CAR
```

---

## 6. ROADMAP PRÓXIMOS SPRINTS

### Sprint 3 (próximo — 5 dias)
**MCR 2.9 expandido (6 → 30 critérios)** — destrava valor comercial. Frontend `/compliance` real com checklist + PDF.

### Sprint 4 (4 dias)
**10 coletores dados.gov.br** — ativa 10 camadas stub.

### Sprint 5 (4 dias)
**Mapa v3** — URL state + drill-down + slider temporal + opacidade.

### Sprint 6 (5 dias)
**Motor jurídico base** — STJ + bge-m3 + `/teses`. Reduz [buscar precedente] nas minutas.

### Sprint 7 (7 dias)
**Gerador de minutas v2** — DOCX, anti-alucinação contra jurisprudência real, tela `/minutas` com histórico.

### Sprint 8 (10 dias)
**Agregador de leilões** — scrapers + parser LLM + timeline + alertas.

---

## 7. COMMITS DA SESSÃO 9

| Hash | Descrição |
|---|---|
| `77142b2` | feat(webhooks): sistema completo de webhooks para alertas em tempo real |
| `a34cf24` | feat(property): laudo PDF + exports GeoJSON/GPKG/SHP + minuta Claude |
| `1630150` | feat(ficha): MonitoramentoTab + AcoesTab — ficha 12/12 |

---

## 8. CONTEXTO IMPORTANTE PRÓXIMA SESSÃO

### Regras invioláveis
1. **Ler** `docs/HANDOFF_2026-04-17_sessao9.md` ANTES de qualquer ação.
2. **Autonomia total** — ver `memory/feedback_autonomy.md`.
3. **Sem mocks** — código real com dados reais.
4. **NÃO rotular** como "feito" o que está parcial ou mock.
5. **NÃO indicar fonte** no frontend.
6. **PT-BR** UI + dark mode Forest/Onyx.
7. **Commits pequenos** e push ao fim.
8. **CHANGELOG.md** atualizado a cada commit lógico.

### Decisões técnicas confirmadas
- FastAPI sync + PostGIS + JWT + cache SHA256 24h
- Next.js App Router + Tailwind v4 + shadcn/ui + react-leaflet 5 + SWR 2.4
- reportlab para PDF (weasyprint disponível como alternativa)
- geopandas para export geoespacial (sem ogr2ogr externo)
- anthropic SDK para Claude API

### Armadilhas conhecidas (atualizadas)
- PowerShell não aceita `&&` — usar `;` ou linhas separadas
- Docker network quebra → `docker compose down && up -d`
- MapBiomas auth: mutation GraphQL `signIn`, não REST
- SIDRA sempre `/f/u`
- Agrolink: histórico por UF é texto puro
- **NOVO**: `sicar_completo.cod_municipio_ibge` é integer, `geo_car.cod_municipio_ibge` é text — sempre castar para text em UNION

### Meta-meta
Sessão 9 fechou a **ficha do imóvel 12/12** — marco crítico para demo comercial. Sistema de webhooks destrava integrações externas. Geração de minutas via Claude API está pronta (aguarda chave). Próximo grande valor: Sprint 3 (MCR 2.9 expandido → 30 critérios) destrava vendas B2B a bancos/tradings.

---

*AgroJus — Handoff Sessão 9 — 2026-04-17 BRT*
*Substitui handoffs anteriores. Mestre atual.*
