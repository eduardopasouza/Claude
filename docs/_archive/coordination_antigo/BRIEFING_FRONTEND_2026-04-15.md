# BRIEFING FRONTEND — AgroJus

> Para o desenvolvedor frontend (Gemini 3.1 ou outro agente IA).
> Atualizado: 2026-04-15 07:30 BRT
> Backend rodando em: http://localhost:8000 | Swagger: http://localhost:8000/docs

---

## SITUACAO ATUAL

O backend tem **42 tabelas com 10.2M registros** no PostGIS, mais acesso a 7B linhas via BigQuery e 515k alertas via MapBiomas Alerta GraphQL. O que FALTA e o frontend que transforma isso em produto.

O frontend atual e um prototipo em Vanilla JS + Vite + Leaflet. A decisao tomada e migrar para **Next.js 14 App Router + Tailwind + shadcn/ui + react-leaflet** com **dark mode (Forest/Onyx)** como tema default.

---

## STACK DEFINIDA

| Tecnologia | Uso |
|---|---|
| Next.js 14+ (App Router) | Framework React com SSR |
| TypeScript | Tipagem |
| Tailwind CSS | Estilizacao |
| shadcn/ui | Componentes base |
| react-leaflet | Mapa interativo |
| recharts | Graficos |
| Inter + Inter Display | Tipografia |

---

## DESIGN SYSTEM — DARK MODE FOREST/ONYX

### Tokens de cor (CSS variables)

```css
:root {
  /* Dark mode (default) */
  --bg-base: #0D1117;
  --bg-surface: #161B22;
  --bg-sidebar: #1C2128;
  --bg-hover: #2D333B;
  --border: #30363D;
  --text-primary: #E6EDF3;
  --text-secondary: #8B949E;
  --accent-green: #3FB950;
  --danger: #F85149;
  --warning: #D29922;
  --info: #58A6FF;
  --success: #3FB950;

  /* Light mode (alternativa) */
  --bg-base-light: #FFFFFF;
  --bg-surface-light: #F6F9FC;
  --bg-sidebar-light: #FAFBFC;
  --bg-hover-light: #F0F2F5;
  --border-light: #E1E4E8;
  --text-primary-light: #1F2328;
  --text-secondary-light: #656D76;
}
```

### Tipografia

- Headings: Inter Display, weight 600-700
- Body: Inter, weight 400-500
- Monospace (dados tecnicos): Geist Mono ou JetBrains Mono
- KPI numero principal: 28-32px, weight 600-700
- Comparacao/variacao: 14px, cor semantica

### Espacamento (8-point grid)

| Token | Valor |
|---|---|
| xxsmall | 2px |
| xsmall | 4px |
| small | 8px |
| medium | 16px |
| large | 24px |
| xlarge | 32px |
| xxlarge | 48px |

---

## LAYOUT PRINCIPAL

```
+----------------------------------------------------------+
|  Top Bar: Logo + Search (Cmd+K) + Notifications + User   |
+----------+-----------------------------------------------+
| Sidebar  |                                               |
| 240px    |           MAPA (area principal)                |
| colapsa- |                                               |
| vel      |   [Layer Manager]       [Inspector Panel]      |
|          |                                               |
| - Dash   |   [Drawing Tools]       [Legend]               |
| - Mapa   |                                               |
| - Imoveis|   [Time Slider]         [Basemap Switcher]     |
| - Alertas|                                               |
| - Compli.|  +------------+---------------------------+   |
| - Relat. |  | KPI Strip  | Charts + Table area        |  |
| - Mercado|  +------------+---------------------------+   |
+----------+-----------------------------------------------+
```

### Regras de layout
- Mapa e o protagonista — ocupa toda a area disponivel
- Sidebar colapsa para 64px (so icones) em tela pequena
- KPI strip abaixo do mapa: 4-6 cards com sparklines (padrao Stripe)
- Inspector panel abre no right-click do mapa
- Mobile: sidebar vira bottom sheet, mapa fullscreen, bottom bar flutuante

---

## PAGINAS E ROTAS

```
/                       → Dashboard (KPIs + mapa mini + alertas recentes)
/mapa                   → Mapa fullscreen com camadas e ferramentas
/imovel/:car            → Ficha completa do imovel (relatorio)
/imovel/:car/relatorio  → PDF viewer do relatorio
/busca                  → Busca universal (CAR, CPF, CNPJ, municipio)
/compliance             → Score MCR 2.9 e EUDR
/mercado                → Cotacoes, credito rural, noticias
/alertas                → Central de alertas e monitoramento
/processos              → Busca de processos judiciais (DataJud)
/configuracoes          → Perfil, plano, API keys
/login                  → Login / Registro
```

---

## COMPONENTES OBRIGATORIOS (por referencia de UX)

| Componente | Referencia | Onde usar |
|---|---|---|
| KPI Card com sparkline | Stripe | Dashboard, ficha imovel |
| Command Palette (Cmd+K) | Linear | Busca global em qualquer pagina |
| Sidebar colapsavel | Stripe/Vercel | Navegacao principal |
| Layer Manager + opacity slider | Google Earth Engine | Painel de camadas do mapa |
| Inspector on-click | GEE | Right-click no mapa → dados do ponto |
| Upload Anything (drag-drop) | Felt | Import de shapefile/GeoJSON/CSV |
| Breadcrumbs | Notion | Hierarquia: Dashboard > Imovel X > Compliance |
| Data Table linkada ao mapa | Felt/Kepler | Lista de imoveis syncada com mapa |
| Drawing Tools | GEE/Felt | Desenhar poligono para analise |
| Badge de status | Stripe/Vercel | LOW/MEDIUM/HIGH/CRITICAL |
| Time Slider | Kepler.gl | Evolucao temporal DETER/PRODES |
| Split Map View | Kepler.gl | Comparar antes/depois |
| Hexbin aggregation | Kepler.gl | Densidade de risco por regiao |
| Toast notifications | Stripe | Confirmacoes e alertas |
| Skeleton loading | Best practice | Loading state pra dados remotos |
| Empty state com CTA | Notion | Onboarding de usuario novo |
| Gauge visual 0-1000 | Serasa Agro | Score MCR 2.9, Score fundiario |

---

## API DO BACKEND — ENDPOINTS DISPONIVEIS

Backend: `http://localhost:8000`
Swagger: `http://localhost:8000/docs`
Auth: Bearer JWT via header `Authorization`

### Funcionando AGORA (testar no Swagger):

```
POST /api/v1/auth/register    → { email, password, name, plan }
POST /api/v1/auth/login       → { email, password }
GET  /api/v1/auth/me          → dados do usuario logado

GET  /api/v1/dashboard/metrics → 8 KPIs reais do PostGIS

GET  /api/v1/geo/catalogo     → 20+ camadas disponiveis
GET  /api/v1/geo/layers/{id}/geojson?bbox=x1,y1,x2,y2&max_features=1000
GET  /api/v1/geo/analyze-point?lat=X&lng=Y
GET  /api/v1/geo/municipios/busca?q=nome
GET  /api/v1/geo/municipios/{cod}/producao
GET  /api/v1/geo/clima?lat=X&lng=Y

GET  /api/v1/compliance/dossier/{cpf_cnpj}  → IBAMA + MTE

GET  /api/v1/market/quotes    → cotacoes CBOT/CME
GET  /api/v1/market/indicators → SELIC, dolar, IPCA

POST /api/v1/search/smart     → busca inteligente
GET  /api/v1/search/cnpj/{cnpj}
GET  /api/v1/search/lista-suja/{cpf_cnpj}

GET  /api/v1/news/            → noticias agro (RSS)

GET  /api/v1/lawsuits/search/{cpf_cnpj}  → DataJud (88 tribunais)
```

### Em construcao (Fase 2 — eu estou criando):

```
POST /api/v1/imovel/relatorio → relatorio completo por CAR/CPF/geometria
     Body: { "tipo": "car", "codigo": "MA-2107357-XXX" }
     Response: { score_mcr29, score_eudr, score_geral, embargos, deter, prodes,
                 sobreposicoes, processos, credito_rural, uso_solo, clima, logistica }

GET  /api/v1/imovel/relatorio/{id}/export?format=pdf
GET  /api/v1/geo/layers/car/geojson         → poligonos CAR (135k imoveis)
GET  /api/v1/geo/layers/prodes/geojson      → desmatamento anual
GET  /api/v1/geo/layers/ucs/geojson         → unidades conservacao (346)
GET  /api/v1/geo/layers/mapbiomas-alertas/geojson → 515k alertas
GET  /api/v1/geo/layers/embargos-icmbio/geojson
GET  /api/v1/geo/layers/autos-icmbio/geojson
```

---

## DADOS DISPONIVEIS NO BANCO (para o frontend saber o que pode exibir)

### Camadas GIS (para o mapa):

| ID da camada | Registros | O que mostra |
|---|---|---|
| `embargos_ibama` | 104.284 | Areas embargadas IBAMA (poligonos vermelhos) |
| `mapbiomas_alertas` | 515.823 | Alertas desmatamento MapBiomas (poligonos laranjas) |
| `car` | 135.000 | Imoveis rurais CAR 27 UFs (poligonos verdes) |
| `deter_amazonia` | 50.000 | Alertas DETER Amazonia (poligonos amarelos) |
| `deter_cerrado` | 50.000 | Alertas DETER Cerrado |
| `prodes` | 50.000 | Desmatamento anual consolidado (vermelho escuro) |
| `unidades_conservacao` | 346 | UCs federais (poligonos azuis) |
| `embargos_icmbio` | 5.000 | Embargos em UCs |
| `autos_icmbio` | 10.000 | Autos de infracao em UCs |
| `terras_indigenas` | 655 | TIs FUNAI (poligonos roxos) |
| `credito_rural` | 5.614.207 | Parcelas financiamento MapBiomas |
| `armazens_silos` | 16.676 | Pontos de armazenagem (icone silo) |
| `frigorificos` | 207 | Frigorificos (icone faca) |
| `rodovias` | 14.255 | Rodovias federais (linhas cinzas) |
| `ferrovias` | 2.244 | Ferrovias (linhas pontilhadas) |
| `portos` | 35 | Portos (icone ancora) |

### Dados tabulares (para dashboards e fichas):

| Dado | Volume | Uso no frontend |
|---|---|---|
| PAM producao agricola | 1.2M registros | Graficos de producao por municipio |
| CNPJ agro | 500k empresas | Enrichment de proprietario |
| SICOR credito rural | 1M registros | Volume de credito por regiao |
| PPM pecuaria | 159k registros | Rebanho por municipio |
| PRODES municipio | 156k | Desmatamento por municipio/bioma |
| Legality MapBiomas | 493k | Cruzamento alerta x embargo x fiscalizacao |
| Censo 2022 | 12k | Populacao, TIs, quilombolas |

---

## PRIORIDADE DE IMPLEMENTACAO FRONTEND

### Fase 1 — Esqueleto (1-2 dias)
1. Next.js 14 scaffold com App Router
2. Tailwind + shadcn/ui configurados
3. Dark mode Forest/Onyx como default
4. Layout: sidebar colapsavel + area principal
5. Rota /login funcional (POST /auth/login + /auth/register)
6. Rota / (dashboard) com KPI cards consumindo GET /dashboard/metrics

### Fase 2 — Mapa (2-3 dias)
7. Rota /mapa com react-leaflet fullscreen
8. Layer Manager: checkbox por camada (GET /geo/catalogo)
9. Carregar GeoJSON de cada camada (GET /geo/layers/{id}/geojson)
10. Click direito → analise de ponto (GET /geo/analyze-point)
11. Basemap switcher (satelite, dark, light, topo)
12. Legenda auto-gerada por camada ativa

### Fase 3 — Busca e Ficha (2-3 dias)
13. Command Palette (Cmd+K) com POST /search/smart
14. Rota /busca com input + resultados
15. Rota /imovel/:car com ficha completa (quando POST /imovel/relatorio estiver pronto)
16. Badge de score (gauge 0-1000)
17. Breadcrumbs de navegacao

### Fase 4 — Complementos (1-2 dias)
18. Rota /mercado com cotacoes (GET /market/quotes + /market/indicators)
19. Rota /alertas com lista de alertas recentes
20. Rota /processos com busca DataJud (GET /lawsuits/search/{cpf_cnpj})
21. News feed (GET /news/)

---

## COMO TESTAR

```bash
# Backend ja roda em Docker
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# Swagger UI
abrir http://localhost:8000/docs

# Criar usuario teste
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"dev@agrojus.br","password":"test123","name":"Dev","plan":"enterprise"}'

# Dashboard metrics
curl http://localhost:8000/api/v1/dashboard/metrics

# Catalogo de camadas
curl http://localhost:8000/api/v1/geo/catalogo

# Camada GIS (DETER Amazonia, bbox Sao Luis)
curl "http://localhost:8000/api/v1/geo/layers/desmatamento_deter/geojson?max_features=100"

# Analise de ponto (centro de Sao Luis)
curl "http://localhost:8000/api/v1/geo/analyze-point?lat=-2.53&lng=-44.28"

# CNPJ
curl http://localhost:8000/api/v1/search/cnpj/00000000000191

# Cotacoes
curl http://localhost:8000/api/v1/market/quotes
```

---

## COMUNICACAO BACKEND <-> FRONTEND

O backend (Claude) esta criando novos endpoints em paralelo. Quando um endpoint novo ficar pronto, eu atualizo este documento e o API_CONTRACT.md. O frontend deve:

1. **Sempre consultar o Swagger** (http://localhost:8000/docs) antes de consumir um endpoint
2. **Nao inventar endpoints** — so usar o que esta documentado aqui
3. **Tratar `is_reference: true`** — significa dado de referencia (mock), nao dado real
4. **Usar try/catch** em todas as chamadas — alguns endpoints podem estar temporariamente offline

---

*Briefing Frontend v2.0 — AgroJus — 2026-04-15*
