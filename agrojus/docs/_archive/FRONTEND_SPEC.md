# Especificação do Frontend — AgroJus

> Este documento é a demanda de estruturação do frontend para ser executado por outro assistente de IA (Antigravity). O backend já está implementado em FastAPI/Python.

---

## 1. Visão do Produto

AgroJus é uma plataforma de inteligência para o agronegócio que combina:
- **Dados fundiários** de imóveis rurais (CAR, SIGEF, SNCR, matrícula)
- **Inteligência jurídica** (embargos, processos, certidões, lista suja)
- **Portal de notícias** do agronegócio (curadoria RSS)
- **Dados de mercado** (cotações, crédito rural, preços de terra)
- **Mapa interativo** com camadas de informação geoespacial

O frontend deve ser moderno, bonito, responsivo (mobile-first) e intuitivo.

---

## 2. Stack Recomendada

| Tecnologia | Uso |
|-----------|-----|
| **Next.js 14+** (App Router) | Framework React com SSR |
| **TypeScript** | Tipagem |
| **Tailwind CSS** | Estilização |
| **shadcn/ui** | Componentes UI |
| **Leaflet** ou **MapLibre GL** | Mapa interativo |
| **react-leaflet** | Integração React + Leaflet |
| **recharts** ou **Chart.js** | Gráficos de cotações |
| **react-pdf** ou download direto | Visualização de PDF |
| **next-auth** | Autenticação (fase futura) |

---

## 3. Backend API

O backend roda em `http://localhost:8000`. Documentação Swagger em `/docs`.

Arquivo de referência completo: [API.md](API.md)

### Endpoints que o frontend consome:

| Endpoint | Método | Uso no Frontend |
|----------|--------|-----------------|
| `/api/v1/search/property` | POST | Busca universal de imóveis |
| `/api/v1/search/cnpj/{cnpj}` | GET | Consulta CNPJ |
| `/api/v1/search/validate/{doc}` | GET | Validação CPF/CNPJ |
| `/api/v1/report/due-diligence` | POST | Relatório DD (JSON) |
| `/api/v1/report/due-diligence/pdf` | POST | Download PDF |
| `/api/v1/report/buyer` | POST | Relatório comprador |
| `/api/v1/report/lawyer` | POST | Relatório advogado |
| `/api/v1/report/investor` | POST | Relatório investidor |
| `/api/v1/report/person` | POST | Dossiê de pessoa |
| `/api/v1/report/region` | POST | Inteligência regional |
| `/api/v1/map/layers` | GET | Camadas do mapa |
| `/api/v1/map/geojson/car/{code}` | GET | GeoJSON de imóvel |
| `/api/v1/map/geojson/sigef/{code}` | GET | GeoJSON parcela SIGEF |
| `/api/v1/map/search/bbox` | GET | Features por bounding box |
| `/api/v1/market/quotes` | GET | Cotações commodities |
| `/api/v1/market/production/{code}` | GET | Produção agrícola |
| `/api/v1/market/credit/municipality/{code}` | GET | Crédito rural |
| `/api/v1/market/land-prices/{state}` | GET | Preços de terra |
| `/api/v1/news/` | GET | Notícias gerais |
| `/api/v1/news/legal` | GET | Notícias jurídicas |
| `/api/v1/news/market` | GET | Notícias de mercado |

---

## 4. Estrutura de Páginas

### 4.1 Página Inicial (`/`)

Layout:
```
┌──────────────────────────────────────────────────────┐
│  HEADER: Logo AgroJus + Navegação + Login/Cadastro   │
├──────────────────────────────────────────────────────┤
│                                                      │
│  HERO: Barra de busca universal centralizada         │
│  "Busque por CAR, matrícula, CPF/CNPJ, coordenadas  │
│   ou nome do proprietário"                           │
│  [ Campo de busca ]  [ Buscar ]                      │
│                                                      │
│  Ícones de atalho:                                   │
│  🏠 Consultar Imóvel  👤 Consultar Pessoa            │
│  📊 Ver Cotações      🗺️ Abrir Mapa                  │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  COTAÇÕES: Cards horizontais com preços              │
│  Soja R$XX | Milho R$XX | Boi R$XX | Café R$XX      │
│  (slider horizontal, atualização automática)         │
│                                                      │
├──────────────────────────────────────────────────────┤
│                                                      │
│  NOTÍCIAS: Grid de cards de notícias                 │
│  - Destaque principal (imagem grande)                │
│  - 4-6 cards menores abaixo                          │
│  - Tabs: Todas | Jurídicas | Mercado                 │
│                                                      │
├──────────────────────────────────────────────────────┤
│  FOOTER: Links, sobre, contato, redes sociais        │
└──────────────────────────────────────────────────────┘
```

**Comportamento da busca:**
- Campo inteligente que detecta automaticamente o tipo de entrada:
  - Começa com dígitos e tem `/`: CNPJ
  - 11 dígitos: CPF
  - Começa com UF (ex: "MT-"): código CAR
  - Contém `,` com decimais: coordenadas (lat, lon)
  - Texto livre: nome de proprietário ou município
- Ao buscar, redireciona para `/resultado` com os dados

### 4.2 Resultado da Busca (`/resultado`)

```
┌──────────────────────────────────────────────────────┐
│  HEADER + Barra de busca (menor, no topo)            │
├──────────────────────────────────────────────────────┤
│                                                      │
│  SEMÁFORO DE RISCO (card grande no topo)             │
│  ┌────────────────────────────────────┐              │
│  │  🟢 RISCO GERAL: BAIXO            │              │
│  │  Fundiário: 🟢  Ambiental: 🟢     │              │
│  │  Jurídico: 🟡   Trabalhista: 🟢   │              │
│  │  Financeiro: 🟢                    │              │
│  └────────────────────────────────────┘              │
│                                                      │
│  [ Baixar PDF ]  [ Compartilhar ]                    │
│                                                      │
├──────────┬───────────────────────────────────────────┤
│ SIDEBAR  │  CONTEÚDO PRINCIPAL                       │
│          │                                           │
│ Sumário: │  Accordion/Tabs com seções:               │
│ • Imóvel │  ┌─ Dados do Imóvel (CAR, SIGEF, área)    │
│ • Regist │  ├─ Dados Registrais (matrícula, CCIR)    │
│ • Propri │  ├─ Proprietário (CNPJ, sócios)           │
│ • Ambie  │  ├─ Situação Ambiental (embargos)         │
│ • Juríd  │  ├─ Trabalhista (lista suja)              │
│ • Trabah │  ├─ Sobreposições (TI, UC, quilombo)      │
│ • Financ │  ├─ Financeiro (crédito, preço terra)     │
│ • Mapa   │  └─ Mapa do Imóvel                        │
│          │                                           │
└──────────┴───────────────────────────────────────────┘
```

**Semáforo de risco:**
- `low` → Verde 🟢
- `medium` → Amarelo 🟡
- `high` → Laranja 🟠
- `critical` → Vermelho 🔴

### 4.3 Mapa Interativo (`/mapa`)

```
┌──────────────────────────────────────────────────────┐
│  HEADER                                              │
├──────────┬───────────────────────────────────────────┤
│ PAINEL   │                                           │
│ LATERAL  │            MAPA FULLSCREEN                │
│          │         (Leaflet / MapLibre)               │
│ Camadas: │                                           │
│ ☑ CAR    │     Tiles: OpenStreetMap / Satellite      │
│ ☑ SIGEF  │                                           │
│ ☐ Embarg │     Ao clicar em polígono:                │
│ ☐ TI     │     → Popup com dados resumidos           │
│ ☐ UC     │     → Botão "Ver Relatório Completo"      │
│ ☐ Desmat │                                           │
│          │                                           │
│ Busca:   │                                           │
│ [Campo]  │                                           │
│          │                                           │
│ Filtros: │                                           │
│ Estado:  │                                           │
│ [Select] │                                           │
│ Municip: │                                           │
│ [Select] │                                           │
│          │                                           │
└──────────┴───────────────────────────────────────────┘
```

**Funcionalidades do mapa:**
- Toggle de camadas (checkbox na sidebar)
- Tiles: OpenStreetMap, Satélite (Esri/Google), Terreno
- Zoom para bounding box ao selecionar município
- Click em polígono abre popup com dados resumidos
- Busca por endereço/coordenada com pin
- Desenhar polígono para selecionar área
- Botão de tela cheia

### 4.4 Dossiê de Pessoa (`/pessoa`)

```
┌──────────────────────────────────────────────────────┐
│  HEADER                                              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Busca: [CPF ou CNPJ]  [Consultar]                   │
│                                                      │
├──────────────────────────────────────────────────────┤
│  CARD: Dados Cadastrais                              │
│  Razão Social / Nome | CNPJ/CPF | Situação           │
│  Endereço | CNAE | Capital Social                    │
│  Sócios (lista)                                      │
├──────────────────────────────────────────────────────┤
│  SEMÁFORO DE RISCO (mesmo formato)                   │
├──────────────────────────────────────────────────────┤
│  Tabs:                                               │
│  [ Imóveis ] [ Embargos ] [ Trabalhista ]            │
│  [ Financeiro ] [ Notícias ]                         │
│                                                      │
│  Conteúdo da tab selecionada                         │
│  (tabelas, cards, etc)                               │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 4.5 Cotações e Mercado (`/mercado`)

```
┌──────────────────────────────────────────────────────┐
│  HEADER                                              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  CARDS DE COTAÇÕES (grid responsivo)                 │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Soja     │ │ Milho    │ │ Boi Gordo│             │
│  │ R$142/sc │ │ R$72/sc  │ │ R$310/@  │             │
│  │ ▲ +1.2%  │ │ ▼ -0.5%  │ │ ▲ +0.8%  │             │
│  └──────────┘ └──────────┘ └──────────┘             │
│                                                      │
│  GRÁFICO DE EVOLUÇÃO (recharts/chart.js)             │
│  Selector: [Commodity] [Período]                     │
│  ┌──────────────────────────────────────┐            │
│  │          Gráfico de linha            │            │
│  └──────────────────────────────────────┘            │
│                                                      │
│  CRÉDITO RURAL POR REGIÃO                            │
│  Selector: [Estado] [Município]                      │
│  Tabela com dados do SICOR/BCB                       │
│                                                      │
│  NOTÍCIAS DE MERCADO                                 │
│  Cards de notícias filtradas por categoria "mercado"  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 4.6 Notícias (`/noticias`)

```
┌──────────────────────────────────────────────────────┐
│  HEADER                                              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Tabs: [ Todas ] [ Jurídicas ] [ Mercado ]           │
│                                                      │
│  Grid de cards de notícias:                          │
│  ┌──────────────────┐ ┌──────────────────┐           │
│  │ [Imagem]         │ │ [Imagem]         │           │
│  │ Título da matéria│ │ Título da matéria│           │
│  │ Fonte · Data     │ │ Fonte · Data     │           │
│  │ Resumo breve...  │ │ Resumo breve...  │           │
│  │ [Tag: jurídico]  │ │ [Tag: mercado]   │           │
│  └──────────────────┘ └──────────────────┘           │
│                                                      │
│  [ Carregar mais ]                                   │
│                                                      │
└──────────────────────────────────────────────────────┘
```

### 4.7 Inteligência Regional (`/regiao`)

```
┌──────────────────────────────────────────────────────┐
│  HEADER                                              │
├──────────────────────────────────────────────────────┤
│                                                      │
│  Seletores: [Estado ▾] [Município ▾]  [Analisar]     │
│                                                      │
├──────────────────────────────────────────────────────┤
│  CARDS DE RESUMO                                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐             │
│  │ Imóveis  │ │ Área     │ │ Embargos │             │
│  │ 1.234    │ │ 450mil ha│ │ 12       │             │
│  └──────────┘ └──────────┘ └──────────┘             │
│                                                      │
│  MAPA DA REGIÃO (mapa menor, focado no município)    │
│                                                      │
│  PRODUÇÃO AGRÍCOLA (tabela ou gráfico de barras)     │
│  Cultura | Área | Produção | Rendimento              │
│                                                      │
│  CRÉDITO RURAL (tabela)                              │
│  Banco | Linha | Finalidade | Valor                  │
│                                                      │
│  NOTÍCIAS DA REGIÃO                                  │
│                                                      │
└──────────────────────────────────────────────────────┘
```

---

## 5. Componentes Reutilizáveis

### RiskBadge
Exibe nível de risco com cor.
```
Props: { level: "low" | "medium" | "high" | "critical", label?: string }
Render: chip/badge colorido (verde/amarelo/laranja/vermelho)
```

### RiskDashboard
Painel de semáforo com todos os riscos.
```
Props: { riskScore: RiskScore }
Render: card com grid de RiskBadges para cada área
```

### PropertyCard
Card resumido de um imóvel.
```
Props: { carCode, area, municipality, state, status }
```

### NewsCard
Card de notícia.
```
Props: { title, url, source, publishedAt, summary, category, imageUrl }
```

### QuoteCard
Card de cotação de commodity.
```
Props: { commodity, price, unit, variationPct }
Render: nome, preço, seta verde/vermelha com variação
```

### SearchBar
Barra de busca inteligente com detecção automática de tipo.
```
Props: { onSearch: (request: PropertySearchRequest) => void }
```

### MapViewer
Componente de mapa com Leaflet/MapLibre.
```
Props: { layers: Layer[], geojson?: GeoJSON, center?: [lat, lon], zoom?: number }
```

### ReportSection
Seção colapsável do relatório.
```
Props: { title, icon, children, defaultOpen? }
```

---

## 6. Design System

### Cores
```
Primary (verde agro):  #2D6A4F
Secondary:             #40916C
Accent:                #95D5B2
Background:            #F8F9FA
Text:                  #212529
Text muted:            #6C757D

Risk colors:
  Low:      #2D6A4F (verde)
  Medium:   #F77F00 (amarelo)
  High:     #E63946 (laranja)
  Critical: #D62828 (vermelho)
```

### Tipografia
- Headings: Inter ou DM Sans (bold)
- Body: Inter (regular)
- Monospace (códigos CAR, CNPJ): JetBrains Mono

### Responsividade
- Mobile: < 768px (menu hamburger, cards empilhados, mapa fullscreen)
- Tablet: 768-1024px (sidebar colapsável)
- Desktop: > 1024px (layout completo com sidebar)

---

## 7. Navegação

```
Header fixo:
  Logo AgroJus | Início | Mapa | Mercado | Notícias | [Busca] | [Login]

Rotas:
  /              → Página inicial
  /resultado     → Resultado de busca / relatório DD
  /mapa          → Mapa interativo
  /pessoa        → Dossiê de pessoa
  /mercado       → Cotações e mercado
  /noticias      → Portal de notícias
  /regiao        → Inteligência regional
  /login         → Login (fase futura)
  /dashboard     → Dashboard do assinante (fase futura)
```

---

## 8. Integração com o Backend

### Configuração
```typescript
// lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export async function searchProperty(request: PropertySearchRequest) {
  const res = await fetch(`${API_BASE}/api/v1/search/property`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  return res.json();
}

export async function getDueDiligence(request: PropertySearchRequest) {
  const res = await fetch(`${API_BASE}/api/v1/report/due-diligence`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  return res.json();
}

export async function downloadPDF(request: PropertySearchRequest) {
  const res = await fetch(`${API_BASE}/api/v1/report/due-diligence/pdf`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  return res.blob();
}

export async function getNews(category?: "legal" | "market", limit = 30) {
  const path = category ? `/api/v1/news/${category}` : "/api/v1/news/";
  const res = await fetch(`${API_BASE}${path}?limit=${limit}`);
  return res.json();
}

export async function getQuotes() {
  const res = await fetch(`${API_BASE}/api/v1/market/quotes`);
  return res.json();
}

export async function getMapLayers() {
  const res = await fetch(`${API_BASE}/api/v1/map/layers`);
  return res.json();
}

export async function getGeoJSON(type: "car" | "sigef", code: string) {
  const res = await fetch(`${API_BASE}/api/v1/map/geojson/${type}/${code}`);
  return res.json();
}

export async function getPersonDossier(request: PersonSearchRequest) {
  const res = await fetch(`${API_BASE}/api/v1/report/person`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  return res.json();
}

export async function getRegionReport(request: RegionSearchRequest) {
  const res = await fetch(`${API_BASE}/api/v1/report/region`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(request),
  });
  return res.json();
}
```

### Tipos TypeScript
```typescript
// types/index.ts

type RiskLevel = "low" | "medium" | "high" | "critical";
type PersonaType = "buyer" | "lawyer" | "farmer" | "investor";

interface PropertySearchRequest {
  car_code?: string;
  matricula?: string;
  sncr_code?: string;
  nirf?: string;
  ccir?: string;
  itr_number?: string;
  sigef_code?: string;
  latitude?: number;
  longitude?: number;
  municipality?: string;
  state?: string;
  cpf_cnpj?: string;
  owner_name?: string;
  persona?: PersonaType;
}

interface PersonSearchRequest {
  cpf_cnpj: string;
  include_properties?: boolean;
  include_legal?: boolean;
  include_environmental?: boolean;
  include_labour?: boolean;
  include_news?: boolean;
  include_financial?: boolean;
}

interface RegionSearchRequest {
  municipality?: string;
  state?: string;
  municipality_code?: string;
}

interface RiskScore {
  overall: RiskLevel;
  land_tenure: RiskLevel;
  environmental: RiskLevel;
  legal: RiskLevel;
  labor: RiskLevel;
  financial: RiskLevel;
  details: string[];
}

interface CARData {
  car_code: string;
  status?: string;
  area_total_ha?: number;
  area_app_ha?: number;
  area_reserva_legal_ha?: number;
  municipality?: string;
  state?: string;
}

interface CNPJData {
  cnpj: string;
  razao_social?: string;
  nome_fantasia?: string;
  situacao_cadastral?: string;
  cnae_principal?: string;
  municipio?: string;
  uf?: string;
  socios?: Array<{ nome: string; qualificacao: string }>;
}

interface DueDiligenceReport {
  report_id: string;
  generated_at: string;
  persona?: PersonaType;
  property_info?: CARData;
  sigef_info?: any;
  matricula_info?: any;
  sncr_info?: any;
  ccir_info?: any;
  itr_info?: any;
  owner_info?: CNPJData;
  ibama_embargos: any[];
  slave_labour: any[];
  overlap_analysis?: any;
  financial_summary?: any;
  risk_score?: RiskScore;
  sources_consulted: string[];
}

interface NewsArticle {
  title: string;
  url: string;
  source: string;
  published_at?: string;
  summary?: string;
  category?: string;
  image_url?: string;
}

interface MarketQuote {
  commodity: string;
  price: number;
  unit: string;
  date: string;
  source: string;
  variation_pct?: number;
  location?: string;
}

interface MapLayer {
  id: string;
  name: string;
  source: string;
  type: string;
  description: string;
}
```

---

## 9. Prioridade de Implementação

### Fase 1 (MVP visual)
1. Layout base (header, footer, navegação)
2. Página inicial com barra de busca e notícias
3. Página de resultado com semáforo de risco
4. Download de PDF

### Fase 2 (Mapa + Mercado)
5. Mapa interativo com camadas
6. Página de cotações e mercado
7. Página de notícias com filtros

### Fase 3 (Pessoa + Região)
8. Dossiê de pessoa
9. Inteligência regional
10. Design polish e responsividade

### Fase 4 (Autenticação + Premium)
11. Login/cadastro
12. Dashboard do assinante
13. Histórico de relatórios
14. Alertas de monitoramento
