# AgroJus — Handoff Sessão 8 (2026-04-18)

> **Substitui o handoff da sessão 7.**
> Sessão 8: Sprint Market (Agrolink 13 commodities), UX centrada na UF do usuário, widget de preço no mapa, housekeeping de docs.
> **Prioridade:** Seção 3 (pendências) → Seção 6 (próximos sprints).

---

## 1. O QUE FOI FEITO NESTA SESSÃO

### 1.1 Sprint Market — Agrolink + /mercado regionalizado ✅

**Problema:** mercado/cotações só nacional + produtor não localiza preço da UF dele.

**Descoberta chave:** Agrolink anti-scraping a tabela principal (sprite PNG com background-position), mas `/cotacoes/historico/{uf}/{slug}` é **HTML puro** com até **265 meses** de histórico mensal (desde 2003!) por UF. Texto puro, não OCR.

**Implementação backend:**
- `app/collectors/agrolink.py` — 13 commodities × até 26 UFs
- Endpoints:
  - `GET /api/v1/market/quotes/agrolink/{commodity}` → uf_stats + histórico por UF
  - `GET /api/v1/geo/ibge/choropleth/uf/preco/{commodity}` → GeoJSON BR UF com preço atual
- Tesseract OCR + pytesseract instalados no container (fallback futuro)

**13 commodities cobertas:**

| Grupo | Commodities | Cobertura |
|---|---|---|
| Grãos | Soja, Milho, Sorgo, Trigo, Arroz, Feijão | 5-26 UFs cada |
| Permanentes / Industriais | Café, Algodão, Cana, Açúcar VHP | 7-14 UFs |
| Proteínas | Boi gordo, Frango, Leite | 14-20 UFs |

**Frontend `/mercado` reescrito:**
- `UFPicker` grande (default MA, persistido em localStorage)
- Hero "Preço de hoje em {Estado}" com 13 commodity cards (preço estadual + seta colorida % vs Brasil)
- Gráfico histórico Recharts ao clicar num card (range 1/2/5/10 anos + "tudo")
- Indicadores BCB compactos
- 6 notícias embutidas com link "Ver todas"
- Removido: CBOT/Yahoo, cards CEPEA duplicados, labels de fonte

### 1.2 Widget de preço direto no `/mapa` ✅

`PriceChoroplethWidget.tsx` no topo-esquerdo do mapa:
- Botão "Colorir por preço" com dropdown agrupado (Grãos / Industriais / Proteínas)
- 10 commodities selecionáveis
- Ao escolher, mapa BR pinta por preço na UF (quintis ColorBrewer)
- Toggle exclusivo + botão X

### 1.3 Zoom +/- no MapPreview ✅

Mini-mapa da ficha ganhou:
- `ZoomControl` posição topright
- `scrollWheelZoom` e `dragging` habilitados (antes bloqueados)

### 1.4 /noticias feed RSS agro ✅

Nova rota com curadoria Canal Rural, Agrolink, Notícias Agrícolas, Portal do Agronegócio, Embrapa. 3 filtros (Todas / Mercado / Jurídico).

### 1.5 Housekeeping ✅

- `docs/` reorganizado: 22+ arquivos → 9 ativos
- 7 handoffs antigos em `docs/_archive/handoffs_antigos/`
- 6 docs superseded em `docs/_archive/` (CONTEXTO, CONTINUIDADE, FRONTEND_SPEC, INVENTARIO, ROADMAP_FASEADO, STATUS_FONTES)
- README reescrito com estrutura real + índice de documentação
- Indicações de fonte ("fonte: Agrolink", "source: CEPEA", etc) removidas do frontend

---

## 2. ESTADO REAL DO PRODUTO (pós-sessão 8)

### Backend — FastAPI + PostGIS
**~95 endpoints** em 22 routers. Camadas PostGIS: **18 ativas** + **10 choropleth preço UF** + **16 choropleth IBGE** + **4 choropleth UF SIDRA** = **48 camadas renderáveis no mapa**.

### Frontend — Next.js 16.2.3
| Rota | Status |
|---|---|
| `/` dashboard | ✅ KPIs |
| `/login` | ✅ JWT |
| `/mapa` | ✅ 42+ camadas · widget preço · draw/upload/analyze · quintis |
| `/imoveis/[car]` | ✅ 10/12 abas + MapPreview com zoom |
| `/mercado` | ✅ UFPicker + 13 commodities + gráfico histórico |
| `/noticias` | ✅ feed RSS agro |
| `/publicacoes` | ✅ DJEN real (42 do Eduardo) |
| `/processos` | ✅ DataJud CNJ |
| `/consulta` | ⚠ DeepSearch mock |
| `/compliance`, `/alertas` | ⚠ mocks standalone |

### Dados no Postgres (7.7M+ registros, inalterado)

| Tabela | Registros |
|---|---|
| `mapbiomas_credito_rural` | 5.614.207 |
| `sigef_parcelas` | 1.717.474 |
| `geo_mapbiomas_alertas` | 515.823 |
| `sicar_completo` (MA) | 352.215 |
| `geo_car` | 135.000 |
| `environmental_alerts` | 104.284 |
| `geo_deter_amazonia` / `cerrado` | 50.000 cada |
| `geo_prodes` | 50.000 |
| `geo_autos_ibama` | **16.121** (sessão 7) |
| `publicacoes_djen` | 42 (Eduardo OAB/MA 12147) |
| ...e outras 10+ | ~20k total |

---

## 3. PENDÊNCIAS — TODAS

### 🔴 CRÍTICAS (impacto direto no valor do produto)

1. **Ficha do imóvel — 2 abas restantes**
   - **Monitoramento**: tabela `webhooks`, CRUD, POST automático ao detectar novo alerta MapBiomas/DETER/DJEN. UI: form cadastro + lista ativos + logs.
   - **Ações**: gerador PDF (Playwright ou WeasyPrint) consumindo dados de todas as 10 abas. Export GeoJSON/GeoPackage (ogr2ogr). Botão "gerar minuta jurídica" delegando à Claude API.

2. **Compliance MCR 2.9 expandido (6 → 30 critérios)**
   - Hoje só 6 checks básicos no endpoint `/compliance/mcr29`. Eduardo quer 30 auditáveis divididos em 5 eixos.
   - **8 fundiários**: CAR ativo, SIGEF sobreposto, TI, UC fed+est, SIGMINE, CCIR, ITR, SPU.
   - **8 ambientais**: PRODES pós-2019, DETER 12m, MapBiomas validado, embargos IBAMA, autos IBAMA, reserva legal, APP, outorga ANA.
   - **6 trabalhistas**: lista suja MTE, CNDT, CAGED, e-Social, NR-31, CIPATR.
   - **5 jurídicos**: DataJud, DJEN, protestos, reclamação CNJ, execução fiscal.
   - **5 financeiros**: SICOR inadimplência, CEIS, CNEP, PIX negativado, CCIR ausente.
   - Frontend `/compliance` standalone (hoje mock) com checklist interativo + PDF.

3. **Motor jurídico base (Sprint 6)**
   - STJ dados abertos + TCU webservice → tabela `jurisprudencia`.
   - Embedding bge-m3 (modelo em mia-project local).
   - Busca híbrida vetorial+textual.
   - Rota `/teses` com citação verificável anti-alucinação.

4. **`/alertas` standalone real** (hoje é 4 mocks hardcoded)
   - Consumir endpoint `/api/v1/monitoring/*` + integrar com webhooks da ficha.

### 🟠 ALTAS

5. **10 coletores dados.gov.br** (guia pronto em `docs/research/dados-gov-guia.md`)
   - IBAMA embargos polígonos (complemento aos 16k autos de ponto)
   - Garantia-Safra (semiárido)
   - SIGMINE processos minerários
   - ANA outorgas + BHO (bacias hidrográficas)
   - INCRA assentamentos + Quilombolas
   - ANEEL usinas + linhas transmissão
   - CEIS + CNEP (via Portal Transparência — token já no .env)

6. **Ficha do proprietário** (cruzamento CPF/CNPJ → imóveis)
   - Dado um CPF/CNPJ: listar todos CARs vinculados (MTE ou SICOR ou inferência)
   - Resumo: N imóveis, área total, compliance médio, processos, crédito rural
   - Rota `/proprietarios/[cpf_cnpj]`

7. **Mapa v3 — padrões SYNTHESIS**
   - URL state serializado (Zustand + useSearchParams)
   - Drill-down UF → Município breadcrumb
   - Slider temporal duplo (YYYY-MM início/fim para PRODES/DETER/MapBiomas)
   - Legenda dinâmica painel direito com "Ver só esta classe"
   - Tabs laterais (Camadas/Filtros/Mapa/Exportar)
   - Opacidade por camada (slider individual)
   - Export da view atual em GeoJSON/CSV/Shapefile/PDF

8. **Gerador de minutas** (Sprint 7)
   - Claude API integration
   - Redação com fundamentação
   - Verificação anti-alucinação contra `jurisprudencia`
   - Rota `/minutas` + export DOCX

9. **Agregador de leilões** (Sprint 8)
   - Scrapers (Caixa, Spy, Portal Leilão, TJs)
   - Dedup + classificação rural
   - Parser LLM edital (red flags via Claude)
   - Enriquecimento geo
   - Timeline do lote (1ª → 2ª → 3ª praça)
   - Alertas WhatsApp/email/webhook

### 🟡 MÉDIAS

10. **Cotações regionais com menos UF** — suínos/ovinos/laranja (só 3-5 UFs mas podem ser úteis em contextos específicos)
11. **Fallback UF vizinha** — quando usuário seleciona UF sem dado no /mercado, sugerir UF próxima
12. **Histórico integrado por praça específica** (dentro de cada UF) — Agrolink tem detalhe por cidade, não implementado
13. **Dashboard proprietário** — lista de CARs favoritos/monitorados por login
14. **Notificações in-app** — sino no TopBar com alertas MapBiomas/DJEN
15. **Mobile responsive fino** — algumas telas (ficha, mapa) não estão 100% mobile

### 🟢 BAIXAS (dívida técnica)

16. OpenAPI codegen → types TypeScript (`openapi-typescript`)
17. State global Zustand (hoje prop drilling)
18. Middleware auth frontend (Next middleware.ts)
19. JWT httpOnly cookie (remover localStorage — XSS risk)
20. Error boundaries (`app/error.tsx`)
21. Testes Vitest + Playwright (ao menos MapComponent + PropertySearch + login)
22. Alembic migrations (substituir `create_tables`)
23. Redis para rate_limiter + monitoring persistido
24. Logger Sentry/Axiom + Analytics PostHog
25. Dark/Light toggle completo + tema Gov.br opcional
26. Storybook para design system

### 🔵 Camadas específicas (backlog)

27. NDVI histórico SATVeg (Embrapa)
28. ONR matrículas (via InfoSimples pago — aba documental, não layer)
29. SNCI legado (download manual + ETL)
30. SPU Terras União
31. ZEE por estado (9 UFs diferentes)
32. ANAC aeroportos
33. Terminais intermodais ANTT/ANTAQ
34. CNT condição rodovias (por solicitação)

---

## 4. CREDENCIAIS (em backend/.env — inalteradas)

```bash
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
MAPBIOMAS_PASSWORD=1qasw23edFR$
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
EMBRAPA_CONSUMER_SECRET=eDJph7PEE9xKDor739rgXwcUc0ca
DADOS_GOV_TOKEN=eyJhbGc...
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
```

---

## 5. COMANDOS RÁPIDOS

```bash
cd C:\dev\agrojus-workspace\agrojus
docker compose up -d
curl http://localhost:8000/health

# Testar 13 commodities Agrolink
for c in soja milho cafe boi trigo arroz feijao algodao cana leite frango sorgo acucar; do
  curl -sS "http://localhost:8000/api/v1/market/quotes/agrolink/$c" | \
    python3 -c "import json,sys;d=json.loads(sys.stdin.read());print(f'$c: {d.get(\"total_ufs\",0)} UFs')"
done

# Testar choropleth de preço
curl "http://localhost:8000/api/v1/geo/ibge/choropleth/uf/preco/soja" | head -c 500

# Frontend
cd frontend_v2 && npm run dev
# http://localhost:3000
```

---

## 6. ROADMAP PRÓXIMOS SPRINTS

### Sprint 2e (próximo — 3 dias)
Fechar a ficha: **Monitoramento (webhooks)** + **Ações (laudo PDF + minuta)**.

### Sprint 3 (5 dias)
**MCR 2.9 expandido (6 → 30 critérios)** — destrava valor comercial. Frontend `/compliance` real.

### Sprint 4 (4 dias)
**10 coletores dados.gov.br** — ativa 10 camadas stub do catálogo.

### Sprint 5 (4 dias)
**Mapa v3** — URL state + drill-down + slider temporal + opacidade.

### Sprint 6 (5 dias)
**Motor jurídico base** — STJ + bge-m3 + `/teses`.

### Sprint 7 (7 dias)
**Gerador de minutas** — Claude API + anti-alucinação + DOCX.

### Sprint 8 (10 dias)
**Agregador de leilões** — scrapers + parser LLM + timeline.

---

## 7. ESTRUTURA DE ARQUIVOS

```
agrojus/
├── CHANGELOG.md              # histórico v0.1 → v0.8
├── README.md                 # overview + estrutura + endpoints
├── ROADMAP.md                # 8 sprints + métricas
├── docker-compose.yml
│
├── backend/
│   ├── Dockerfile (tesseract-ocr + libs geo)
│   ├── requirements.txt (+ pytesseract, Pillow)
│   ├── app/
│   │   ├── api/            # 22 routers
│   │   ├── collectors/     # 24 coletores (inclui agrolink.py NOVO, regional_quotes.py)
│   │   ├── models/
│   │   └── main.py
│   └── scripts/            # ETLs
│
├── frontend_v2/
│   ├── src/
│   │   ├── app/(dashboard)/
│   │   │   ├── imoveis/[car]/        # ficha 10/12 abas
│   │   │   ├── mapa/, mercado/, noticias/, publicacoes/, ...
│   │   ├── components/
│   │   │   ├── imovel/     # MapPreview, TabNav, 10 Tabs
│   │   │   ├── mapa/       # MapComponent, MapTools, PriceChoroplethWidget, ...
│   │   │   └── layout/
│   │   └── lib/
│   │       ├── layers-catalog.ts     # 42 ativas + 10 preço = 52 renderáveis
│   │       └── api.ts
│
└── docs/
    ├── HANDOFF_2026-04-18_sessao8.md        # ← ESTE
    ├── HANDOFF_2026-04-19_sessao9_INICIO.md # prompt próxima sessão
    ├── API.md, ARCHITECTURE.md
    ├── research/                            # visual-audit + blueprints
    └── _archive/                            # handoffs antigos
```

---

## 8. CONTEXTO IMPORTANTE PRÓXIMA SESSÃO

### Regras invioláveis
1. **Ler** `docs/HANDOFF_2026-04-18_sessao8.md` ANTES de qualquer ação.
2. **Autonomia total** — Eduardo autorizou explicitamente (ver `memory/feedback_autonomy.md`).
3. **Sem mocks** — código real com dados reais.
4. **NÃO rotular** como "feito" o que está parcial ou mock.
5. **NÃO indicar fonte** no frontend — decisão do Eduardo sessão 8.
6. **PT-BR** UI + dark mode Forest/Onyx.
7. **Commits pequenos** e push ao fim.
8. **CHANGELOG.md** atualizado a cada commit lógico.

### Decisões técnicas tomadas
- FastAPI + PostGIS sync + JWT + cache SHA256 24h disco
- Next.js App Router + Tailwind v4 + shadcn/ui + react-leaflet 5 + SWR 2.4
- Tesseract OCR instalado (fallback futuro anti-scraping)
- Docker Compose 2 containers + volume `agrojus_pgdata` (preserva entre restarts)

### Armadilhas conhecidas
- PowerShell não aceita `&&` — usar `;` ou linhas separadas
- Docker network às vezes quebra → `docker compose down && up -d`
- Rebuild Docker: conflitos inmetpy (fixado em >=0.1.1)
- NÃO mover projeto pra OneDrive (loop Turbopack)
- MapBiomas auth: mutation GraphQL `signIn`, NÃO REST `/auth/login`
- SIDRA sempre com `/f/u` (unified = nomes + códigos IBGE)
- Agrolink: página principal tem anti-scraping (sprite PNG), histórico por UF é texto puro

### Meta-meta
Sessão 8 massiva: 14 commits pushed. Agrolink destravou cotações regionalizadas com 22 anos de histórico — antes impossível. Mercado passou de visão genérica nacional para "minha região como produtor". 13 commodities × 26 UFs × 265 meses de série.

---

*AgroJus — Handoff Sessão 8 — 2026-04-18 BRT*
*Substitui handoffs anteriores. Mestre atual.*
