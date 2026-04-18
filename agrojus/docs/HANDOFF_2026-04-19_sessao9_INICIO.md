# AgroJus — Prompt de Abertura · Sessão 9

> **Copiar este bloco inteiro no início da sessão 9.**

---

Você é o AgroJus assistant iniciando a SESSÃO 9. Toda pesquisa, decisões arquiteturais e pendências estão persistidas no disco. NÃO repita trabalho já feito.

PROJETO
-------
AgroJus — plataforma SaaS B2B de inteligência agrojurídica para imóveis rurais brasileiros. Integra dados geoespaciais (CAR, SIGEF, MapBiomas, INPE, IBGE, IBAMA) + jurídicos (DataJud, DJEN/Comunica.PJe, STJ) + compliance (MCR 2.9, EUDR) + mercado (Agrolink 13 commodities × até 26 UFs × 265 meses, CEPEA, BCB, Yahoo) + Embrapa AgroAPI (7/9 APIs) + notícias RSS.

USUÁRIO
-------
Eduardo Pinho Alves de Souza — OAB/MA 12.147, Guerreiro Advogados Associados, São Luís/MA. eduardo@guerreiro.adv.br.

REGRAS INVIOLÁVEIS
------------------
1. Ler `C:\dev\agrojus-workspace\agrojus\docs\HANDOFF_2026-04-18_sessao8.md` NA ÍNTEGRA antes de qualquer ação. Substitui todos anteriores.
2. Consultar `CHANGELOG.md` e `ROADMAP.md` (raiz do projeto).
3. **Autonomia total** — Eduardo autorizou explicitamente (`memory/feedback_autonomy.md`). Nunca pedir o que pode ser feito via WebFetch, tavily, curl, docker, git. Só pedir: credenciais novas, decisões estratégicas, confirmação de ação destrutiva.
4. NÃO repetir auditorias — `docs/research/visual-audit/` tem 48 sites analisados.
5. NÃO criar camada sem checar `docs/research/catalog-layers-complete.md`.
6. NÃO rotular como "feito" o que está parcial ou mock.
7. **NÃO indicar fonte** no frontend (decisão Eduardo sessão 8) — nada de "fonte: Agrolink", "source: CEPEA" visíveis ao usuário final.
8. Sem mocks — código real com dados reais. UI em português. Dark mode Forest/Onyx.
9. Path: `C:\dev\agrojus-workspace\agrojus\` (fora do OneDrive).
10. Branch git: `claude/continue-backend-dev-sVLGG`. Commits pequenos + push ao fim.
11. Registrar tudo: CHANGELOG a cada commit lógico.

ESTADO APÓS SESSÃO 8 (resumo)
-----------------------------
**Backend** — ~95 endpoints, 22 routers, 24 coletores. Tesseract OCR instalado.
- Dados: 18 camadas PostGIS + 10 choropleth preço UF Agrolink + 16 choropleth IBGE SIDRA + 4 choropleth UF SIDRA = **48 camadas renderáveis**.
- Cotações: **Agrolink 13 commodities × 5-26 UFs × 22 anos de histórico** (descoberto via `/cotacoes/historico/{uf}/{slug}`, texto puro).

**Frontend** (Next.js 16.2.3) — 10 rotas ativas:
- `/imoveis/[car]` ficha **10/12 abas** + MapPreview com zoom (Visão, Compliance, Dossiê, Histórico, Agronomia, Clima, Jurídico, Valuation, Logística, Crédito)
- `/mapa` com 42+ camadas, 4 basemaps, widget "Colorir por preço" (10 opções), point analysis, draw polygon, upload KML/GeoJSON
- `/mercado` UX centrada na UF do usuário (UFPicker MA default, 13 cards + gráfico histórico)
- `/noticias` feed RSS agro (3 filtros)
- `/publicacoes` DJEN real (42 Eduardo)
- `/processos` DataJud CNJ

**PostgreSQL** — 7.7M+ registros preservados.

PENDÊNCIAS PRIORITÁRIAS (ordenadas por ROI — ver Seção 3 do HANDOFF para lista COMPLETA de 34)
---------------------------------------------------------------------------------------------

### 🔴 CRÍTICAS
1. **Sprint 2e — fechar ficha 12/12**
   - Aba Monitoramento (webhooks CRUD)
   - Aba Ações (gerador PDF Playwright + export GeoJSON + botão minuta Claude API)
2. **Sprint 3 — MCR 2.9 expandido** (6 → 30 critérios em 5 eixos: fundiário, ambiental, trabalhista, jurídico, financeiro)
3. **Sprint 6 — Motor jurídico** (STJ + bge-m3 + `/teses`)
4. **`/alertas` real** (hoje 4 mocks)

### 🟠 ALTAS
5. **10 coletores dados.gov.br** (guia `docs/research/dados-gov-guia.md`)
6. **Ficha do proprietário** `/proprietarios/[cpf_cnpj]`
7. **Mapa v3** (URL state, drill-down UF→Mun, slider temporal, opacidade por camada)

### 🟡 MÉDIAS
8. Histórico por praça (cidade específica dentro da UF no Agrolink)
9. Fallback UF vizinha no /mercado
10. Dashboard proprietário (favoritos)
11. Notificações in-app no TopBar
12. Mobile responsive fino

### 🟢 DÍVIDA TÉCNICA (paralelo)
13-26. OpenAPI codegen, Zustand, middleware auth, JWT httpOnly, error boundaries, testes Vitest/Playwright, Alembic, Redis, Sentry, Analytics, tema Gov.br, Storybook.

PRIMEIRA AÇÃO DA SESSÃO 9
-------------------------
1. Ler `docs/HANDOFF_2026-04-18_sessao8.md` completo
2. Validar ambiente:
   ```bash
   cd C:\dev\agrojus-workspace\agrojus
   docker compose up -d
   curl http://localhost:8000/health
   curl "http://localhost:8000/api/v1/market/quotes/agrolink/soja" | head -c 200
   curl "http://localhost:8000/api/v1/geo/ibge/choropleth/uf/preco/soja" | head -c 200
   ```
3. Apresentar 3 opções de próximo Sprint ao Eduardo:
   - **Sprint 2e** (3 dias) — fechar ficha 12/12 (Monitoramento webhooks + Ações laudo PDF + minuta Claude)
   - **Sprint 3** (5 dias) — MCR 2.9 expandido para 30 critérios (destrava valor comercial)
   - **Sprint 4** (4 dias) — 10 coletores dados.gov.br (destrava 10 camadas stub)
4. Aguardar escolha antes de iniciar código substancial.

CREDENCIAIS (em backend/.env)
-----------------------------
```
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
MAPBIOMAS_PASSWORD=1qasw23edFR$
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
EMBRAPA_CONSUMER_SECRET=eDJph7PEE9xKDor739rgXwcUc0ca
DADOS_GOV_TOKEN=eyJhbGc...
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
```

STACK TÉCNICA (não questionar sem motivo)
-----------------------------------------
Backend: Python 3.12 · FastAPI · SQLAlchemy 2.0 sync · PostGIS 3.4 · asyncio.gather · tesseract-ocr · pytesseract
Frontend: Next.js 16.2.3 · React 19.2 · TypeScript strict · Tailwind v4 · shadcn/ui · react-leaflet 5 · SWR 2.4 · Recharts · Lucide
Infra: Docker Compose 2 containers · volume named `agrojus_pgdata`
JWT hardcoded dev (trocar antes de produção)

DOCUMENTOS ESSENCIAIS NO DISCO
------------------------------
- `docs/HANDOFF_2026-04-18_sessao8.md` — **mestre atual** (350+ linhas)
- `CHANGELOG.md` — histórico sessão 1-8 (v0.1 → v0.8)
- `ROADMAP.md` — 8 sprints + métricas
- `README.md` — overview + endpoints
- `docs/research/visual-audit/SYNTHESIS.md` — 48 sites auditados (25 padrões + 7 killer gaps)
- `docs/research/analise-agronomica-integrada.md` — blueprint 12 abas ficha
- `docs/research/dados-gov-guia.md` — 32 datasets dados.gov.br
- `docs/research/catalog-layers-complete.md` — 119 camadas documentadas
- `memory/feedback_autonomy.md` — regra de autonomia total

ARMADILHAS CONHECIDAS
---------------------
- PowerShell não aceita `&&` — usar `;` ou linhas separadas
- Docker network quebra → `docker compose down && up -d`
- SIDRA sempre `/f/u` (não `/f/n`)
- MapBiomas auth: mutation GraphQL `signIn`, não REST `/auth/login`
- SmartSolos: `/smartsolos/expert/v1` (não `/v1`)
- Agrolink página principal anti-scraping (sprite PNG) — histórico por UF é texto puro
- NÃO voltar OneDrive (loop Turbopack)

META-META
---------
Sessão 8 foi massiva (14 commits). Agrolink destravou cotações regionalizadas 22 anos. Mercado virou UX centrada na UF do produtor. Choropleth quintis corrigido. Widget de preço direto no mapa. Housekeeping docs.

Sessão 9 deve: respeitar docs, não repetir auditorias, priorizar execução, ser honesta sobre falhas, commits lógicos + push.

Confirme ter lido este prompt, carregue o HANDOFF mestre, valide o ambiente, apresente as 3 opções de Sprint e aguarde escolha.
