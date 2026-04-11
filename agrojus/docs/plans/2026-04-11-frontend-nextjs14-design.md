# AgroJus Frontend — Design Spec

**Data:** 2026-04-11
**Stack:** Next.js 14 (App Router), React 18, TypeScript, TailwindCSS, shadcn/ui (Radix), react-leaflet
**Tema:** Dark mode imersivo — Forest/Onyx com glassmorphism escuro
**Inspiracao visual:** SpectraX (painel cibernetico), Agrotools (dashboard enterprise), Linear (navegacao), MapBiomas (mapa interativo)
**Idioma da UI:** Portugues brasileiro

---

## 1. Layout Principal

**Modelo: Sidebar esquerda + Top bar (estilo Agrotools/Linear)**

```
┌─────────────────────────────────────────────────────┐
│ TOPBAR: Logo | OmniSearch (busca inteligente) | User│
├────────┬────────────────────────────────────────────┤
│        │                                            │
│ SIDE   │          CONTENT AREA                      │
│ BAR    │                                            │
│        │    (muda conforme a pagina ativa)           │
│ Nav    │                                            │
│ icons  │                                            │
│ +      │                                            │
│ labels │                                            │
│        │                                            │
│        │                                            │
│ Status │                                            │
│ API    │                                            │
├────────┴────────────────────────────────────────────┤
```

### Sidebar (240px, colapsavel para 64px)
- Logo AgroJus + badge "Enterprise" / "Pro" / "Free"
- Navegacao: 8 itens com icone + label
- Status da API (orb pulsante: online/offline + latencia)
- Botao colapsar/expandir
- Em mobile (< 768px): vira drawer com hamburger

### Top bar (h-16, fixed)
- OmniSearch: input global que detecta tipo (CPF, CNPJ, CAR, coordenadas, municipio)
- Notificacoes (badge com contagem)
- Avatar do usuario + dropdown (perfil, plano, logout)

---

## 2. Paginas (8 rotas)

### 2.1 Dashboard (`/`)
- 4 KPI cards: Fontes Online (13 APIs), Buscas Restantes, Relatorios/Mes, Latencia
- OmniSearch duplicado (hero section)
- Feed de noticias agro (ultimas 6, com tag juridico/mercado)
- Cotacoes rapidas (SELIC, dolar, soja, boi gordo) — cards compactos

### 2.2 Consulta / Due Diligence (`/consulta`)
- Input CPF/CNPJ com validacao em tempo real (digitos verificadores)
- Botao "Auditar" → chama POST /consulta/completa
- Resultado em grid:
  - Risk Matrix (4 celulas: Geral, Ambiental, Juridico, Financeiro) com cores LOW/MEDIUM/HIGH/CRITICAL
  - Blocos colapsaveis por fonte (Receita Federal, IBAMA, Lista Suja, DataJud, SICOR, Protestos)
  - Cada bloco mostra: dados + status da fonte (real vs referencia) + timestamp
- Botao "Gerar PDF" → chama POST /report/due-diligence/pdf

### 2.3 Mapa GIS (`/mapa`)
- react-leaflet fullscreen no content area
- HUD overlay (glassmorphism escuro):
  - Top: seletor de camadas (dropdown ou painel lateral)
  - Bottom-right: coordenadas do cursor, zoom level
  - Info box: resultado do analyze-point
- Right-click no mapa → POST /geo/analyze-point → popup/sidebar com resultado
- Painel de camadas (drawer direito):
  - Toggle por camada (checkbox)
  - Agrupado por categoria (fundiario, ambiental, administrativo, etc.)
  - Badge de status (online/offline) por fonte
- Camadas disponiveis: TIs (FUNAI), DETER (INPE), PRODES, UCs, Quilombolas, Municipios (IBGE)

### 2.4 Compliance (`/compliance`)
- Duas tabs: MCR 2.9 | EUDR
- Formulario: CPF/CNPJ, CAR, Lat, Lon, Produto (para EUDR)
- Resultado: checklist visual (check verde / X vermelho por item)
  - MCR 2.9: CAR ativo, PRODES limpo, georreferenciado, sem embargo, sem Lista Suja
  - EUDR: sem desmatamento pos-2020, rastreabilidade, georreferenciamento
- Badge final: APTO / INAPTO / PENDENTE
- Exportar resultado como JSON ou PDF

### 2.5 Jurisdicao (`/jurisdicao`)
- Seletor de estado (dropdown ou mapa do Brasil clicavel)
- Card do estado: orgao ambiental, % Reserva Legal, biomas, particularidades
- Tab "Comparar": selecionar 2 estados lado a lado
- Dados de: GET /jurisdicao/estado/{uf}, GET /jurisdicao/comparar

### 2.6 Mercado & Indicadores (`/mercado`)
- Cards de indicadores BCB: SELIC, Dolar, IPCA, IGP-M, CDI (tempo real)
- Cotacoes de commodities: Soja, Milho, Boi Gordo, Cafe, Algodao (CEPEA)
- Credito rural por municipio: busca por nome → GET /market/credit/municipality/{cod}
- Graficos de serie historica (sparklines ou line charts)

### 2.7 Noticias (`/noticias`)
- 3 tabs: Todas | Juridicas | Mercado
- Cards de noticia: titulo, resumo, fonte, data, tag
- Paginacao (offset/limit)

### 2.8 Processos Judiciais (`/processos`)
- Busca por CPF/CNPJ → GET /lawsuits/search/{doc}
- Busca por assunto (TPU/CNJ) → GET /lawsuits/subject/{code}
- Lista de tribunais e assuntos agro → GET /lawsuits/tribunais
- Resultado: tabela com numero, tribunal, assunto, data, status

---

## 3. Design System

### Paleta Dark Forest/Onyx
```
--bg-body:       #0A0F0D      (quase preto esverdeado)
--bg-surface:    #111916      (superficie de cards)
--bg-elevated:   #1A2420      (cards hover, modais)
--bg-glass:      rgba(17, 25, 22, 0.85)  (glassmorphism)
--border:        rgba(255, 255, 255, 0.06)
--border-hover:  rgba(255, 255, 255, 0.12)

--emerald-500:   #10B981      (primary action, links)
--emerald-400:   #34D399      (hover, active)
--emerald-600:   #059669      (pressed)
--emerald-glow:  rgba(16, 185, 129, 0.15) (glow effects)

--text-primary:  #F0FDF4      (titulos, texto principal)
--text-secondary:#A7C4B5      (texto secundario, labels)
--text-muted:    #5F7A6E      (placeholders, hints)

--risk-low:      #10B981      (verde)
--risk-medium:   #F59E0B      (amarelo)
--risk-high:     #F97316      (laranja)
--risk-critical: #EF4444      (vermelho)
```

### Tipografia
- Display/titulos: `Outfit` (700-800)
- Corpo: `Inter` (400-600)
- Monospace (dados tecnicos): `JetBrains Mono` ou system monospace
- Scale: 12/14/16/20/24/32/48px

### Componentes shadcn/ui customizados
- Todos com tema dark Forest
- Cards com `bg-surface` + `border` + `shadow-glow` on hover
- Buttons: primary (emerald), secondary (ghost), destructive (red)
- Inputs: `bg-elevated` com `border-hover` on focus
- Tables: striped com `bg-surface`/`bg-elevated` alternando
- Badges de risco: coloridos conforme `--risk-*`

### Glassmorphism
- `backdrop-filter: blur(16px)`
- `background: var(--bg-glass)`
- `border: 1px solid var(--border)`
- Usado em: sidebar, modais, HUD do mapa, dropdowns

---

## 4. Integracao com Backend

### API Client (`lib/api.ts`)
- Base URL configuravel via env (NEXT_PUBLIC_API_URL)
- Wrapper com try/catch que retorna `{ data, error, source }`
- Headers: Authorization Bearer (quando logado)
- Interceptor para 429 (rate limit) → toast com mensagem do backend

### Data Fetching
- React Query (TanStack Query) para cache e revalidacao
- SWR-like: stale-while-revalidate para dados que mudam pouco (cotacoes, noticias)
- No SSR para APIs externas (client-side only) — evita timeout no server

### Auth
- JWT armazenado em cookie httpOnly (ou localStorage pro MVP)
- Middleware Next.js para proteger rotas (redirect para /login se nao autenticado)
- Rotas publicas: /, /login, /registro

---

## 5. Responsividade

| Breakpoint | Layout |
|-----------|--------|
| < 768px (mobile) | Sidebar vira drawer, cards empilham, mapa fullscreen |
| 768-1024px (tablet) | Sidebar colapsada (64px), cards em 2 colunas |
| > 1024px (desktop) | Layout completo, sidebar expandida, cards em 3-4 colunas |

---

## 6. Estrutura de Arquivos

```
agrojus/frontend/
├── app/
│   ├── layout.tsx              (root layout: sidebar + topbar)
│   ├── page.tsx                (dashboard)
│   ├── consulta/page.tsx
│   ├── mapa/page.tsx
│   ├── compliance/page.tsx
│   ├── jurisdicao/page.tsx
│   ├── mercado/page.tsx
│   ├── noticias/page.tsx
│   ├── processos/page.tsx
│   ├── login/page.tsx
│   ├── registro/page.tsx
│   └── globals.css
├── components/
│   ├── layout/
│   │   ├── Sidebar.tsx
│   │   ├── TopBar.tsx
│   │   ├── OmniSearch.tsx
│   │   └── ApiStatus.tsx
│   ├── dashboard/
│   │   ├── KpiCard.tsx
│   │   ├── NewsFeed.tsx
│   │   └── QuotesTicker.tsx
│   ├── consulta/
│   │   ├── RiskMatrix.tsx
│   │   ├── SourceBlock.tsx
│   │   └── DocInput.tsx
│   ├── mapa/
│   │   ├── GisMap.tsx
│   │   ├── LayerPanel.tsx
│   │   ├── AnalyzePointPopup.tsx
│   │   └── MapHud.tsx
│   ├── compliance/
│   │   ├── ChecklistItem.tsx
│   │   └── ComplianceBadge.tsx
│   ├── jurisdicao/
│   │   ├── StateCard.tsx
│   │   └── StateComparator.tsx
│   ├── mercado/
│   │   ├── IndicatorCard.tsx
│   │   └── SparklineChart.tsx
│   ├── shared/
│   │   ├── RiskBadge.tsx
│   │   └── DataSourceTag.tsx
│   └── ui/                     (shadcn/ui components)
│       ├── button.tsx
│       ├── card.tsx
│       ├── input.tsx
│       ├── badge.tsx
│       ├── table.tsx
│       ├── tabs.tsx
│       ├── dropdown-menu.tsx
│       ├── dialog.tsx
│       ├── toast.tsx
│       └── ...
├── lib/
│   ├── api.ts                  (API client wrapper)
│   ├── auth.ts                 (JWT helpers)
│   ├── hooks/
│   │   ├── useConsulta.ts
│   │   ├── useIndicators.ts
│   │   ├── useNews.ts
│   │   └── useCompliance.ts
│   └── utils.ts                (formatters, validators)
├── public/
│   └── favicon.svg
├── tailwind.config.ts
├── next.config.ts
├── tsconfig.json
├── package.json
└── .env.local.example
```

---

## 7. Fora do Escopo (MVP)

- Monitoramento de propriedades (polling/alertas) — Fase 3
- Upload de documentos (OCR de matriculas) — Fase 4
- Roles/permissoes (admin/user/viewer) — Fase 4
- PWA / service worker
- i18n (so portugues no MVP)
- Testes E2E (Playwright) — apos MVP funcional
