# AgroJus — Prompt de Abertura · Sessão 8

> **Copiar este bloco inteiro no início da sessão 8.**
> Eduardo começa a sessão colando o prompt abaixo.

---

Você é o AgroJus assistant iniciando a SESSÃO 8. Toda pesquisa, decisões arquiteturais e pendências estão persistidas no disco. NÃO repita trabalho que já foi feito.

PROJETO
-------
AgroJus — plataforma SaaS B2B de inteligência agrojurídica para imóveis rurais brasileiros. Integra dados geoespaciais (CAR, SIGEF, MapBiomas, INPE, IBGE) + jurídicos (DataJud, DJEN/Comunica.PJe, STJ) + compliance (MCR 2.9, EUDR) + mercado (CEPEA, BCB, CONAB) + Embrapa AgroAPI (7/9 APIs ativas).

USUÁRIO
-------
Eduardo Pinho Alves de Souza — OAB/MA 12.147, Guerreiro Advogados Associados, São Luís/MA. Email: eduardo@guerreiro.adv.br. Áreas: agronegócio, ambiental, tributário, cível/possessório.

REGRAS INVIOLÁVEIS
------------------
1. Ler `C:\dev\agrojus-workspace\agrojus\docs\HANDOFF_2026-04-17_sessao7.md` na íntegra ANTES de qualquer ação. Substitui todos os handoffs anteriores.
2. Consultar `C:\dev\agrojus-workspace\agrojus\ROADMAP.md` para priorização.
3. Consultar `C:\dev\agrojus-workspace\agrojus\CHANGELOG.md` para histórico de mudanças.
4. NÃO repetir auditoria dos 48 sites — já está em `docs/research/visual-audit/`.
5. NÃO criar nova camada sem checar `docs/research/catalog-layers-complete.md`.
6. NÃO pedir ao Eduardo o que consigo fazer sozinho — **autonomia total**, ele deu explicitamente (ver `memory/feedback_autonomy.md`). Se é público (WebFetch, tavily, docker, curl) → faço. Se tem credencial em `.env` → uso.
7. NÃO rotular como "feito" o que está parcial ou mock.
8. Sem mocks — código real com dados reais. UI em português. Dark mode Forest/Onyx + glassmorphism.
9. Path do projeto: `C:\dev\agrojus-workspace\agrojus\` (fora do OneDrive).
10. Branch git: `claude/continue-backend-dev-sVLGG`. Fazer commits pequenos e push ao fim.
11. Registrar tudo no disco. CHANGELOG.md atualizado a cada commit lógico.

ESTADO APÓS SESSÃO 7 (resumo)
-----------------------------
**Backend** — ~90 endpoints, 18 camadas PostGIS, Embrapa 7/9 APIs, IBGE choropleth 16 métricas, MapBiomas Alerta com JWT, DJEN, DataJud, IBAMA 16k autos, property endpoints (search/overlaps/neighbors/credit/valuation), AOI analyze.

**Frontend** — Next.js 16, ficha `/imoveis/[car]` com **10/12 abas funcionais** (Visão, Compliance, Dossiê, Histórico, Agronomia, Clima, Jurídico, Valuation, Logística, Crédito) + MapPreview no header. Mapa `/mapa` com toolbar (point analysis, draw polygon, upload KML/GeoJSON), 18 camadas PostGIS renderizando, 14 choropleth IBGE com quintis funcionais.

**Dados PostgreSQL** — 7.7M+ registros. Tabelas-chave preservadas entre sessões: `mapbiomas_credito_rural` (5.6M), `sigef_parcelas` (1.7M), `geo_mapbiomas_alertas` (515k), `sicar_completo` (352k MA), `geo_autos_ibama` (16k — NOVO sessão 7), `publicacoes_djen` (42 — Eduardo OAB/MA).

PENDÊNCIAS PRIORITÁRIAS (ordenadas por ROI)
-------------------------------------------
### 🔴 CRÍTICAS

1. **Sprint 2e — fechar ficha (2 abas restantes)**
   - **Monitoramento** — CRUD de webhooks por CAR/CPF/OAB, tabela `webhooks` + ao detectar novo alerta MapBiomas/DETER/DJEN/DataJud, POST no URL configurado. UI: form cadastro + lista ativos + logs de envio.
   - **Ações** — geração de laudo PDF (Playwright ou WeasyPrint) consumindo dados de todas as abas, download direto. Export GeoJSON/GeoPackage (ogr2ogr). Botão "gerar minuta jurídica" delegando à Claude API com contexto da ficha.

2. **Sprint 3 — MCR 2.9 expandido (6 → 30 critérios)**
   - O endpoint atual tem 6 checks básicos. Eduardo quer 30 auditáveis.
   - 8 fundiários: CAR ativo, SIGEF sobreposto, TI, UC federal+estadual, SIGMINE, CCIR, ITR, SPU.
   - 8 ambientais: PRODES pós-2019, DETER 12m, MapBiomas validado, embargos IBAMA, autos IBAMA, reserva legal, APP, outorga ANA.
   - 6 trabalhistas: lista suja MTE, CNDT, CAGED, e-Social, NR-31, CIPATR.
   - 5 jurídicos: DataJud, DJEN, protestos, CNJ reclamação, CNJ execução fiscal.
   - 5 financeiros: SICOR inadimplência, CEIS, CNEP, PIX negativado, CCIR ausente.
   - Frontend `/compliance` standalone (hoje mock) com checklist + PDF.

### 🟠 ALTAS

3. **Coletores dados.gov.br** — guia pronto em `docs/research/dados-gov-guia.md` com 32 datasets priorizados. Escrever 10 coletores:
   - IBAMA embargos polígonos (só autos pontos foram carregados)
   - Garantia-Safra beneficiários (semiárido)
   - SIGMINE processos minerários
   - ANA outorgas + BHO
   - INCRA assentamentos + Quilombolas
   - ANEEL usinas + linhas transmissão
   - CEIS + CNEP (via Portal Transparência, token em `.env`)

4. **Ficha do proprietário** (cruzamento pessoa+imóveis)
   - Dado um CPF/CNPJ → listar todos CARs vinculados (via tabela MTE ou SICOR ou inferência por proximidade)
   - Resumo: N imóveis, área total, compliance médio, processos ativos, crédito rural tomado
   - Rota `/proprietarios/[cpf_cnpj]`

### 🟡 MÉDIAS

5. **Melhorias do mapa v3** (padrões SYNTHESIS)
   - URL state serializado (Zustand + useSearchParams) para compartilhar estado
   - Drill-down UF → Município breadcrumb
   - Slider temporal duplo (YYYY-MM início/fim para PRODES/DETER/MapBiomas)
   - Legenda dinâmica painel direito com "Ver só esta classe"
   - Tabs laterais (Camadas/Filtros/Mapa/Exportar)
   - Opacidade por camada (slider individual)
   - Export da view atual em GeoJSON/CSV/Shapefile/PDF

6. **Motor jurídico base (Sprint 6)**
   - STJ dados abertos + TCU webservice → tabela `jurisprudencia`
   - Embedding bge-m3 (modelo em mia-project local Eduardo tem)
   - Busca híbrida vetorial+textual
   - Rota `/teses` com citação verificável

### 🟢 BAIXAS (dívida técnica)

7. OpenAPI codegen → types TypeScript
8. State global Zustand
9. Middleware auth frontend (Next middleware.ts)
10. JWT httpOnly cookie (remover localStorage — XSS risk)
11. Error boundaries (`app/error.tsx`)
12. Testes Vitest + Playwright (ao menos MapComponent + PropertySearch + login)
13. Alembic migrations (substituir `create_tables`)
14. Redis para rate_limiter + monitoring persistido
15. Logger Sentry/Axiom + Analytics PostHog
16. Dark/Light toggle completo + tema Gov.br opcional

PRIMEIRA AÇÃO DA SESSÃO 8
-------------------------
1. Ler `docs/HANDOFF_2026-04-17_sessao7.md` completo
2. Ler `CHANGELOG.md` para entender o que foi feito
3. Validar ambiente:
   ```bash
   cd C:\dev\agrojus-workspace\agrojus
   docker compose up -d
   curl http://localhost:8000/health
   curl "http://localhost:8000/api/v1/property/MA-2100055-0013026E975B48D9B4F045D7352A1CB9/valuation"
   curl -X POST http://localhost:8000/api/v1/geo/aoi/analyze -H "Content-Type: application/json" -d '{"geometry":{"type":"Polygon","coordinates":[[[-47.81,-4.82],[-47.80,-4.82],[-47.80,-4.83],[-47.81,-4.83],[-47.81,-4.82]]]},"name":"Teste"}'
   ```
4. Se tudo saudável, apresentar ao Eduardo as 3 opções prioritárias de Sprint para escolher:
   - **Sprint 2e** (2-3 dias) — Monitoramento webhooks + Ações laudo PDF/minuta. Fecha a ficha 12/12.
   - **Sprint 3** (5 dias) — MCR 2.9 expandido 30 critérios. Destrava valor do produto (compliance é o WHY dos clientes).
   - **Sprint 4** (4 dias) — 10 coletores dados.gov.br. Destrava 10 camadas stub do catálogo.

5. Aguardar escolha do Eduardo antes de iniciar código substancial.

CREDENCIAIS ATIVAS (já em `backend/.env`)
-----------------------------------------
```bash
GCP_PROJECT_ID=agrojus
MAPBIOMAS_EMAIL=eduardo@guerreiro.adv.br
MAPBIOMAS_PASSWORD=1qasw23edFR$
EMBRAPA_CONSUMER_KEY=Ts5fkuUf9CT6ycU3LrmHQ9ylNBUa
EMBRAPA_CONSUMER_SECRET=eDJph7PEE9xKDor739rgXwcUc0ca
EMBRAPA_ACCESS_TOKEN=2aef1f08-a5e9-3480-b68b-2184057e3a6d  # opcional
DADOS_GOV_TOKEN=eyJhbGc...  # CKAN federal
PORTAL_TRANSPARENCIA_TOKEN=0cedbd7584d9f76c779981fadd4a984a
DATAJUD_API_KEY=cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQdw==
```

STACK TÉCNICA
-------------
Backend: Python 3.12 · FastAPI · SQLAlchemy 2.0 sync · PostGIS 3.4 · asyncio.gather · cache SHA256 disco 24h TTL
Frontend: Next.js 16.2.3 · React 19.2 · TypeScript strict · Tailwind v4 · shadcn/ui · react-leaflet 5 · SWR 2.4 · Recharts · Lucide
Infra: Docker Compose 2 containers · WSL2 8GB · volume named `agrojus_pgdata`
JWT hardcoded em dev (trocar antes de produção)

DOCUMENTOS ESSENCIAIS
---------------------
- `docs/HANDOFF_2026-04-17_sessao7.md` — mestre atual (800+ linhas)
- `docs/HANDOFF_2026-04-18_sessao8_INICIO.md` — **ESTE ARQUIVO** (prompt da sessão)
- `CHANGELOG.md` — histórico sessão por sessão
- `ROADMAP.md` — 8 sprints, métricas, dívida técnica
- `README.md` — overview, stack, endpoints principais
- `docs/research/visual-audit/SYNTHESIS.md` — 25 padrões + 7 killer gaps de 48 sites
- `docs/research/catalog-layers-complete.md` — 119 camadas documentadas
- `docs/research/analise-agronomica-integrada.md` — blueprint das 12 abas da ficha
- `docs/research/dados-gov-guia.md` — 32 datasets priorizados
- `docs/research/embrapa-integracao-status.md` — paths confirmados sessão 7
- `memory/feedback_autonomy.md` — regra de autonomia total

ARMADILHAS CONHECIDAS
---------------------
- **NÃO mover projeto de volta para OneDrive** (loop Turbopack)
- **NÃO usar `&&` no PowerShell** — usar `;` ou comandos em linhas separadas. Git Bash funciona.
- **Docker network às vezes quebra** após restart — `docker compose down && up -d` reconstrói
- **Múltiplos node.exe travando** → `powershell -Command "Stop-Process -Name node -Force"`
- **SIDRA `/f/n` vs `/f/u`** — sempre `/f/u` pra ter códigos IBGE
- **MapBiomas REST `/auth/login` é deprecated** — usar mutation GraphQL `signIn`
- **SmartSolos path correto é `/smartsolos/expert/v1`** (não `/v1`)
- **Choropleth usa quintis** — NÃO voltar para linear

META-META
---------
Sessão 7 foi massiva: Sprint 1 + 2a + 2b + 2c + 2d em um dia. Ficha passou de zero para 10/12 abas, 4 features críticas do mapa (choropleth quintis, point analysis, draw, upload) implementadas + validadas com Eduardo. 8 commits pushed.

Sessão 8 deve manter ritmo autônomo. Eduardo é OAB, não programador — respeite o tempo dele, pergunte apenas estratégia, faça tudo o mais.

Confirme ter lido este prompt, carregue o HANDOFF mestre, valide o ambiente, apresente as 3 opções de Sprint e aguarde escolha.
