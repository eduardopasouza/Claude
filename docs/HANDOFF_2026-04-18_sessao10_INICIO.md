# AgroJus — Handoff Sessão 10 (2026-04-18)

> **Substitui todos os handoffs anteriores.** Mestre atual.
> Sessão 9 foi massiva: 21 commits, 2 sprints concluídos, 3 sprints novos propostos.

---

## 1. CONTEXTO RÁPIDO

**AgroJus** é plataforma SaaS B2B de **inteligência agrojurídica integrada** para imóveis rurais brasileiros.
O produto não é "ferramenta para advogado" — é um **hub multi-persona**: comprador de imóvel, trading, banco/cooperativa, consultor ambiental, produtor rural, advogado agrário.

**Eduardo** (OAB/MA 12.147, Guerreiro Advogados, São Luís/MA) quer o produto "mostrável em qualquer reunião" cruzando dados oficiais com análise automática.

---

## 2. O QUE FOI FEITO NESTA SESSÃO (9)

### 🏁 Sprints concluídos

| Sprint | Entrega |
|---|---|
| **2e** | Ficha do imóvel 12/12 abas (Monitoramento webhooks + Ações PDF/exports/minuta Claude) |
| **3** | MCR 2.9 × 32 critérios em 5 eixos + evidências + explicação humana + inline na ficha |
| **4** | 10 coletores dados.gov.br + Portal Transparência → 822.879 registros reais em 8/12 tabelas (CEIS 3k, CNEP 1,6k, INCRA Assent 8,2k, Quilombolas 427, ANEEL SIGA 25k, ANEEL Linhas 176, IBAMA embargos 88k, IBAMA autos 695k) |
| **Dossiê Agrofundiário** | Service multi-input (6 tipos entrada) + PDF 20-45 págs com análises cruzadas + frontend `/dossie` + CTAs em 3 pontos do mapa |
| **Hub Jurídico-Agro (backend)** | 5 models + 75 seeds (12 contratos + 12 teses + 51 normativos) + 12 endpoints |

### 🎨 UX do mapa (correções do feedback Eduardo)
- Painel de camadas colapsável (badge compacta)
- ZoomControl movido para bottomright
- minZoom reduzido em 6 camadas densas (aparecem com zoom menor)
- LayerInspector: 4 botões rápidos (copiar texto/JSON, baixar GeoJSON/KML)
- Export KML de AOI desenhada/upada
- StatsDashboard reescrito estilo MapBiomas (barras horizontais, toggle camada/tema)

### 🧠 ComplianceTab inline
- 3 modos: completo 32 critérios · rápido 6 · EUDR
- Evidência JSON expansível por critério
- **Explicação humana** de cada apontamento (pending e failed)

---

## 3. ESTADO ATUAL DO PRODUTO

### Backend
- **~120 endpoints** em 26 routers
- **PostgreSQL**: 18 camadas PostGIS originais + 12 tabelas Sprint 4 (8 populadas) + 5 tabelas jurídico-agro (populadas) + webhooks + logs + market_prices = **~40 tabelas**
- **Registros totais**: ~8,5M (7,7M originais + 822k Sprint 4 + 75 seeds jurídicos)
- Coletores: 28 (24 originais + Sprint 4)

### Frontend — 14 rotas

| Rota | Status |
|---|---|
| `/` dashboard | ✅ KPIs |
| `/login` | ✅ JWT |
| `/mapa` | ✅ v2.1 (painel colapsa, inspector copy/KML, stats MapBiomas-style, CTA dossiê) |
| `/imoveis/[car]` | ✅ 12/12 abas (Monitoramento webhooks + Ações dossiê/PDF/exports/minuta) |
| `/mercado` | ✅ UFPicker + 13 commodities + gráfico |
| `/noticias` | ✅ RSS agro |
| `/publicacoes` | ✅ DJEN |
| `/processos` | ✅ DataJud |
| `/compliance` | ✅ 32 critérios standalone + laudo PDF |
| `/dados-gov` | ✅ admin ETL |
| `/dossie` | ✅ **NOVO** multi-input + 6 personas + PDF 20-45pg |
| `/juridico` | ❌ **PENDENTE** backend pronto, falta UI |
| `/alertas` | ⚠ mock |
| `/consulta` | ⚠ mock |

### MCR 2.9 cobertura
- **15/32 critérios** com dados reais (47%)
- A04/A05 **massivamente melhorados** com IBAMA embargos (88k) + autos (695k)
- 17 pending aguardam fontes pagas (CCIR/ITR/CNDT) ou novos ETLs

---

## 4. PRÓXIMA SESSÃO — O QUE FAZER

### 🔴 Prioridade alta

**A. Frontend `/juridico` (5 abas)** — backend pronto, basta UI
```
Tabs: [Processos] [Contratos] [Teses] [Legislação] [Monitoramento]
```
- **Processos**: form CPF/CNPJ → chama `/juridico/processos/{cpf}/dossie` → mostra DataJud + DJEN + IBAMA + CEIS + CNEP + Lista Suja com risco classificado
- **Contratos**: grid de 12 cards clicáveis → modal com markdown renderizado + campos preenchíveis → download .docx
- **Teses**: grid por área (ambiental/fundiário/trabalhista/tributário/previdenciário) → accordion com argumentos, precedentes, próxima ação
- **Legislação**: filtros UF/município/tema/esfera → lista de normativos com link oficial
- **Monitoramento**: form cadastrar CPF → grid dos monitoramentos ativos com última checagem

**B. Calculadora de prescrição administrativa** (pedido explícito Eduardo)
- Lei 9.873/99 art. 1 (5 anos) + art. 21 (intercorrente 3 anos)
- Timeline visual mostrando os prazos
- Variações estaduais (ver se existem)
- Concorrentes consolidados (LegalDoc, Legalyze) tem isso — replicar

**C. Sprint 5 pendente**: integrar Zustand store ao MapComponent + slider temporal + drill-down + opacidade

### 🟠 Prioridade média

**D. Cron de monitoramento ativo**
- Job diário que verifica para cada CPF em `monitoramento_partes`:
  - Novos autos IBAMA
  - Novas sanções CEIS/CNEP
  - Novos processos DataJud
  - Novas publicações DJEN
- Insere em `monitoramento_partes_eventos`
- Dispara webhook se configurado

**E. Sprint 6 — Motor jurídico (STJ + bge-m3)**
- Enriquece as teses_defesa_agro com precedentes reais verificáveis

**F. Expansão de seeds jurídico-agro**
- +15 contratos (outros integração aves/suínos, contratos silagem, etc.)
- +20 teses (direito ambiental, previdenciário rural, trabalhista rural)
- +30 normativos estaduais (hoje só ~10, precisa cobrir 27 UFs)

### 🟡 Prioridade baixa (backlog)

- Dossiê com QSA Receita Federal
- Dossiê com histórico MapBiomas (1985-atual)
- Clima histórico 10 anos INMET
- Embrapa ZARC integrado (aptidão culturas)
- Embrapa SmartSolos

---

## 5. COMANDOS RÁPIDOS

```bash
cd C:\dev\agrojus-workspace\agrojus
docker compose up -d
curl http://localhost:8000/health

# Seed jurídico-agro (se recriado DB)
curl -X POST "http://localhost:8000/api/v1/juridico/seed?force=true"

# Dossiê por CAR
curl -X POST http://localhost:8000/api/v1/dossie \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2100055-0013026E975B48D9B4F045D7352A1CB9","persona":"investidor"}'

# Dossiê PDF
curl -o dossie.pdf -X POST http://localhost:8000/api/v1/dossie/pdf \
  -H "Content-Type: application/json" \
  -d '{"car_code":"MA-2100055-...","persona":"comprador"}'

# Consulta jurídica por CPF
curl http://localhost:8000/api/v1/juridico/processos/00818544000165/dossie

# Lista contratos agro
curl "http://localhost:8000/api/v1/juridico/contratos?categoria=exploracao_rural"

# Lista teses ambientais
curl "http://localhost:8000/api/v1/juridico/teses?area=ambiental"

# Legislação para MA + tema ambiental
curl "http://localhost:8000/api/v1/juridico/legislacao?uf=MA&tema=ambiental"

# Frontend
cd frontend_v2 && npm run dev
```

---

## 6. ESTRUTURA DE ARQUIVOS (pós-sessão 9)

```
agrojus/
├── CHANGELOG.md              ← v0.12 consolidado
├── README.md
├── ROADMAP.md                ← 15 sprints + ideias cross-cutting
├── .claude/settings.json     ← advIA disabled neste projeto
│
├── backend/
│   ├── app/
│   │   ├── api/              # 26 routers
│   │   │   ├── dossie.py       ← NOVO
│   │   │   ├── juridico.py     ← NOVO
│   │   │   ├── dados_gov.py    ← Sprint 4
│   │   │   ├── webhooks.py     ← Sprint 2e
│   │   │   ├── property_actions.py  ← Sprint 2e
│   │   │   └── ... (21 outros)
│   │   ├── services/
│   │   │   ├── dossie_generator.py  ← NOVO 850 linhas
│   │   │   ├── dossie_pdf.py        ← NOVO 850 linhas
│   │   │   ├── juridico_seeds.py    ← NOVO 12+12+51
│   │   │   ├── mcr29_expanded.py    ← 32 critérios com explicações
│   │   │   ├── webhook_dispatcher.py
│   │   │   ├── minuta_generator.py
│   │   │   └── ... (15 outros)
│   │   ├── collectors/     # 28 coletores
│   │   │   ├── dados_gov.py             ← KNOWN_RESOURCES + fallback
│   │   │   ├── dados_gov_loaders.py    ← 11 loaders (10 dados.gov + IBAMA autos)
│   │   │   ├── portal_transparencia.py ← CEIS/CNEP
│   │   │   └── ... (25 outros)
│   │   ├── models/database.py  ← ~40 modelos
│   │   └── main.py
│   └── scripts/run_dados_gov_etl.py
│
├── frontend_v2/src/
│   ├── app/(dashboard)/
│   │   ├── dossie/page.tsx       ← NOVO tela cheia
│   │   ├── dados-gov/page.tsx    ← Sprint 4 admin
│   │   ├── compliance/page.tsx   ← Sprint 3 standalone
│   │   ├── imoveis/[car]/page.tsx ← 12 abas
│   │   ├── mapa/page.tsx
│   │   ├── mercado/, noticias/, processos/, publicacoes/, compliance/...
│   │   └── juridico/             ← PENDENTE criar
│   ├── components/
│   │   ├── mapa/                 ← v2.1 (colapso + KML + stats MapBiomas)
│   │   ├── imovel/tabs/          ← 12 tabs
│   │   │   ├── ComplianceTab.tsx  ← expandido com 32 criterios
│   │   │   ├── AcoesTab.tsx       ← CTA dossiê
│   │   │   └── ... (10 outros)
│   │   └── layout/
│   └── lib/
│       ├── stores/map-store.ts   ← Zustand scaffold (aguarda integração)
│       └── layers-catalog.ts
│
└── docs/
    ├── HANDOFF_2026-04-18_sessao10_INICIO.md   ← ESTE (mestre)
    ├── HANDOFF_2026-04-17_sessao9.md           ← ver para contexto
    ├── research/
    └── _archive/
```

---

## 7. CREDENCIAIS (em `backend/.env`)

```bash
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
DADOS_GOV_TOKEN=eyJhbGc...       # bug persistente no portal CloudFront (401 sistêmico)
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a  # OK
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
# ANTHROPIC_API_KEY=sk-ant-...    # adicionar se for usar gerador minutas Claude
```

---

## 8. REGRAS INVIOLÁVEIS (próxima sessão)

1. **Ler este handoff inteiro** antes de qualquer ação
2. **Autonomia total** — Eduardo autorizou (`memory/feedback_autonomy.md`)
3. **Sem mocks** — código real com dados reais
4. **NÃO rotular** como "feito" o que está parcial
5. **NÃO indicar fonte** visível ao usuário final no frontend (decisão sessão 8)
6. **PT-BR** UI + dark mode Forest/Onyx
7. **Commits pequenos** e push frequente
8. **CHANGELOG atualizado** a cada commit lógico
9. **Branch**: `claude/continue-backend-dev-sVLGG`
10. **Path**: `C:\dev\agrojus-workspace\agrojus\` (fora do OneDrive)

---

## 9. CONTEXTO IMPORTANTE

### Decisões tomadas na sessão 9

- **AgroJus não é focado em advogado** — é hub multi-persona. Isso guia todo o design da sessão 10+.
- **Dossiê** é o produto central: qualquer geometria → relatório 20-45 págs cruzando 15 fontes.
- **Hub Jurídico-Agro** estratégico: contratos + teses + legislação + monitoramento de terceiros.
- **Análises cruzadas** (`gerar_analises_cruzadas`) são diferencial: detectam correlações invisíveis em análise isolada.
- **Semáforo de risco** consolidado (verde/amarelo/laranja/vermelho) para decisão rápida.
- **MCR 2.9 com explicação humana** de cada apontamento — tradução do técnico para o acionável.

### Armadilhas conhecidas

- PowerShell não aceita `&&` — usar `;` ou linhas separadas
- Docker network quebra → `docker compose down && up -d`
- Token dados.gov.br retorna 401 mesmo renovado (bug CloudFront do portal)
- SIGMINE/ANM servidor em 502 externo
- `sicar_completo.cod_municipio_ibge` é integer; `geo_car.cod_municipio_ibge` é text — castar em UNION
- TeseDefesaAgro.situacao deve ser Text (não String(200)) — descrições longas
- ANEEL CSV usa Latin-1/ISO-8859-1 (não UTF-8) e separador `;`
- pandas NaN não serializa para JSON Postgres — usar `_clean_for_json`
- Dossiê PDF grande (>20 págs) leva ~3-5s para gerar

### Meta-meta

Sessão 9 validou 3 hipóteses importantes:
1. **Consolidação + análise** é mais valioso que dados brutos — o dossiê com 15 fontes cruzadas é o produto
2. **Múltiplas personas** usam os mesmos dados com lentes diferentes — arquitetura de `persona` no backend + templates no frontend funcionou
3. **Hub jurídico-agro** tem espaço de mercado óbvio — concorrentes (LegalDoc, Jusbrasil) não focam no setor

Próxima sessão deve acelerar o frontend `/juridico` + calculadora prescricional para fechar o ciclo de feedback.

---

*AgroJus — Handoff Sessão 10 — 2026-04-18 BRT*
*Versão 0.12.0 · 21 commits pushed · 40 tabelas · 8,5M registros · ~120 endpoints · 14 rotas frontend*
