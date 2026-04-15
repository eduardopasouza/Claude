# PROMPT DE CONTINUIDADE — AgroJus Enterprise

## Contexto do Projeto

Você está assumindo o desenvolvimento do **AgroJus**, uma plataforma de inteligência agropecuária enterprise para o mercado brasileiro. O projeto está sendo construído em:

- **Repositório:** `c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus`
- **Branch Git:** `claude/continue-backend-dev-sVLGG`
- **Último commit:** `f3cb2cc` — Handoff 2026-04-15
- **Handoff completo:** `docs/HANDOFF_2026-04-15.md` (leia este arquivo primeiro)

---

## O Que É o AgroJus

Plataforma SaaS B2B de inteligência fundiária, ambiental e de mercado para:
- **Bancos e Cooperativas de Crédito Rural** — compliance MCR 2.9 (BCB), auditoria EUDR
- **Traders e Exportadores** — monitoramento de commodities e cadeia de fornecimento limpa
- **Escritórios Jurídicos Rurais** — dossiê consolidado de CPF/CNPJ (IBAMA, MTE, DataJud)
- **Fintechs Agro** — motor de score de risco ambiental e trabalhista

**Diferencial:** cruzamento em tempo real de 13+ bases de dados oficiais (IBAMA, FUNAI, MapBiomas, INPE, MTE, BCB, IBGE, CEPEA) em uma única API REST.

---

## Stack Tecnológico

| Camada | Tecnologia |
|---|---|
| Backend API | FastAPI + SQLAlchemy + Uvicorn |
| Banco de Dados | PostgreSQL 15 + PostGIS (dados geoespaciais) |
| Frontend Principal | Vanilla JS + Vite + Leaflet (GIS) |
| Frontend Enterprise | Next.js 14 (TypeScript) — em desenvolvimento paralelo |
| Infraestrutura | Docker Compose (2 containers: `db` + `backend`) |
| ETL / Coleta | Python scripts (Playwright, pdfplumber, httpx, ogr2ogr) |

---

## Estado Atual do Banco de Dados

```bash
# Para verificar o estado do banco, rode:
docker exec agrojus-backend-1 python scripts/db_status.py
```

| Tabela | Registros | Status |
|---|---|---|
| `environmental_alerts` IBAMA | 103.668 | ✅ Completo |
| `mapbiomas_credito_rural` | 5.614.207 | ✅ Completo |
| `market_quotes` | 14 (seed) | ⚠️ Precisa scraper real |
| `environmental_alerts` MTE | 4 (incompleto) | ❌ ETL falhou |

---

## APIs Funcionando (http://localhost:8000)

```
GET  /api/v1/market/quotes           → Cotações das 14 cadeias (lê PostgreSQL)
GET  /api/v1/compliance/dossier/{id} → Dossiê CPF/CNPJ (IBAMA + MTE)
GET  /api/v1/geo/layers/{id}/geojson → GeoJSON do PostGIS para o mapa Leaflet
GET  /api/v1/geo/analyze-point       → Análise de coordenada (risco, FUNAI, DETER)
POST /api/v1/consulta/completa       → Busca profunda multi-fonte
GET  /docs                           → Swagger UI
```

---

## Frontend GIS Engine v2 (http://localhost:5173)

Motor geoespacial completo com:
- **Basemap Switcher:** Satélite (ArcGIS) / Terreno / OSM
- **Multi-layer Overlay:** Empilha camadas (Embargos + TI + Crédito Rural)
- **Right-click → Análise de Ponto:** Popup com risco, município, DETER, FUNAI, clima
- **Bounding Box Search:** Shift+drag → busca desmatamento na região desenhada
- **Coord Picker:** Click esquerdo copia lat,lon para clipboard
- **Legenda Dinâmica:** Remove camadas individualmente pelo botão ✕

Camadas disponíveis:
- `embargos` — 🔴 103k polígonos IBAMA do PostGIS
- `desmatamento` / `desmatamento_cerrado` — 🔥 DETER/INPE
- `terras_indigenas` — 🟡 FUNAI
- `parcelas_financiamento` — 🟢 5.6M parcelas MapBiomas
- `municipios` — ⬜ Malha IBGE

---

## ROADMAP — Próximas Tarefas (Ordem de Prioridade)

### 🔴 FASE 7 — Completar a Base de Dados (URGENTE)

**7.1 — Corrigir ETL Lista Suja MTE**
- Arquivo: `backend/scripts/etl_mte_escravo.py`
- Problema: O PDF `data/mte_trabalho_escravo.pdf` tem tabelas multi-página que o pdfplumber não parsou corretamente. Apenas 4 de ~2.000 CNPJs foram importados.
- Solução: Reescrever o parser usando estratégia de extração por texto bruto (`page.extract_text()`) em vez de `extract_table()`, ou usar `camelot-py` como alternativa.
- Resultado esperado: ~2.000 CNPJs/CPFs na tabela `environmental_alerts` com `source='MTE'`

**7.2 — Ativar Coletor CEPEA Diário**
- Arquivo: `backend/scripts/fetch_cepea_playwright.py`
- Problema: Playwright precisa de Chromium instalado no container Docker.
- Solução A: Instalar Chromium no Dockerfile do backend.
- Solução B: Usar scraping HTTP puro (sem browser) via `fetch_market_prices.py`.
- Resultado esperado: Cotações reais de 14 cadeias atualizadas diariamente em `market_quotes`.

**7.3 — Endpoint de Métricas do Dashboard**
- Criar `GET /api/v1/dashboard/metrics`
- Deve retornar: total IBAMA, total MTE, total cotações, total parcelas, latência do banco
- Conectar os KPI cards do `index.html` (atualmente hardcoded) a esse endpoint

---

### 🟡 FASE 8 — Login e Controle de Acesso

**8.1 — Tela de Login no Frontend**
- Criar `view-login` no `index.html` que chama `POST /api/v1/auth/login`
- Armazenar JWT no `localStorage`
- Adicionar header `Authorization: Bearer <token>` em todos os fetch calls
- Redirecionar para dashboard após login bem-sucedido

**8.2 — Hardening do JWT_SECRET**
- Adicionar ao `docker-compose.yml`:
  ```yaml
  environment:
    JWT_SECRET: ${JWT_SECRET}
  ```
- Criar `.env` com `JWT_SECRET=<random-32-chars>` (não commitar)
- Adicionar `.env` ao `.gitignore`

**8.3 — Rate Limiting por API Key**
- Implementar throttle no FastAPI usando `slowapi`
- Tier Gratuito: 10 consultas/dia
- Tier Pro: ilimitado
- Exibir uso no dashboard (KPI "Searches")

---

### 🟡 FASE 9 — Relatórios e Export

**9.1 — Export PDF do Dossiê**
- Endpoint: `GET /api/v1/compliance/dossier/{cpf_cnpj}/export?format=pdf`
- Usar `WeasyPrint` (já deve estar disponível no container)
- Template HTML com logo AgroJus, tabela de alertas, score de risco, mapa simplificado
- Retornar `Content-Type: application/pdf` com download

**9.2 — Export do Mapa como Imagem**
- No GIS Engine v2, adicionar botão "Exportar PNG" no HUD
- Usar `leaflet-image` ou `html2canvas` para capturar o mapa
- Embutir legenda e metadados na imagem

---

### 🟢 FASE 10 — Dados Avançados (BigQuery/BasedosDados)

**10.1 — PAM/PPM via BigQuery**
- Script: `backend/scripts/etl_basedosdados.py`
- Requer: Conta de Serviço Google Cloud (JSON key) configurada como env var
- Dados disponíveis: Produção Agrícola Municipal (PAM), Pecuária Municipal (PPM)
- Importar para tabela `ibge_producao_municipal`

**10.2 — CNPJ Receita Federal via BasedosDados**
- Tabela pública no BigQuery: `basedosdados.br_me_natureza_juridica.empresa`
- Enriquecer o endpoint de dossiê com dados cadastrais da Receita
- Permitir busca por nome/razão social além de CNPJ

**10.3 — Dados.gov.br via API CKAN**
- Script: `backend/scripts/explore_dadosgovbr.py`
- Buscar e importar datasets de: Outorga de Água (ANA), GTA Pecuário, PLDAg (MAPA)
- Criar tabela `datasets_govbr` com metadados e links de download

---

### 🟢 FASE 11 — UX e Produto

**11.1 — Next.js Frontend Enterprise**
- Migrar gradualmente do frontend Vanilla JS para o Next.js 14 (já iniciado em `frontend-next/`)
- Implementar server-side rendering para SEO
- Usar Recharts para gráficos de tendência de preços

**11.2 — Alertas em Tempo Real (WebSocket)**
- Implementar `WebSocket` no FastAPI para push de novos embargos IBAMA
- Dashboard recebe alerta em tempo real sem refresh
- Badge de notificação no sidebar

**11.3 — Motor de Score de Risco**
- Algoritmo que combina: Embargos IBAMA + Lista Suja MTE + Processos DataJud + Sobreposição TI
- Score de 0-100 com classificação: Baixo / Médio / Alto / Crítico
- Exibir no dossiê e no right-click do mapa

---

## Como Iniciar o Ambiente

```bash
# 1. Subir containers (PostgreSQL + FastAPI)
cd "c:/Users/eduar/OneDrive/Escritório/_Pessoal/AgroJus/Claude/agrojus"
docker compose up -d

# 2. Verificar saúde do banco
docker exec agrojus-backend-1 python scripts/db_status.py

# 3. Iniciar frontend Vite
cd frontend
npm run dev

# 4. Acessar
# Frontend: http://localhost:5173
# Backend:  http://localhost:8000
# Swagger:  http://localhost:8000/docs
```

---

## Credenciais

| Serviço | Detalhes |
|---|---|
| PostgreSQL | host: `localhost:5432` · db: `agrojus` · user: `agrojus` · pass: `agrojus` |
| Backend API | `http://localhost:8000` |
| Frontend | `http://localhost:5173` |

---

## Instruções para o Agente de IA

1. **Leia primeiro** o arquivo `docs/HANDOFF_2026-04-15.md` e este arquivo
2. **Verifique o estado** rodando `docker exec agrojus-backend-1 python scripts/db_status.py`
3. **Comece pela Fase 7.1** (ETL Lista Suja MTE) — é o bloqueador de compliance mais crítico
4. **Nunca use mock data** — toda informação deve vir do PostgreSQL ou de APIs reais
5. **Mantenha os commits atômicos** com mensagens descritivas em português
6. **Ao finalizar a sessão**, atualize este arquivo e o `docs/HANDOFF_*.md` com o progresso

---

*AgroJus Enterprise — Prompt de Continuidade v1.0 — 2026-04-15*
