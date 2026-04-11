# AgroJus v0.5.0

**Plataforma de Inteligência Fundiária, Jurídica, Ambiental e de Mercado para o Agronegócio**

AgroJus cruza dados de 15+ fontes públicas em tempo real para oferecer due diligence rural automatizada, compliance ambiental (MCR 2.9 / EUDR), dossiês de pessoas, inteligência regional e monitoramento — tudo com score de risco jurídico em 5 dimensões.

## Números da plataforma

| Métrica | Valor |
|---------|-------|
| Endpoints da API | 75 |
| Collectors de dados | 18 |
| Fontes de dados integradas | 15+ |
| Camadas geoespaciais catalogadas | 27 (13 ativas) |
| Testes automatizados | 82 passando |
| Categorias de dados | 10 (fundiário, ambiental, administrativo, infraestrutura, hidrografia, solo, clima, financeiro, mineração, energia) |

## O que o AgroJus faz

### Consulta Unificada
Um único endpoint (`POST /consulta/completa`) consulta **6 fontes em paralelo** para qualquer CPF/CNPJ: dados cadastrais (Receita Federal), embargos IBAMA, Lista Suja trabalho escravo, processos judiciais (DataJud/CNJ), crédito rural (SICOR/BCB) e protestos — com score de risco consolidado.

### Análise de Ponto no Mapa
Click em qualquer ponto do mapa e receba instantaneamente: município, estado, órgão ambiental competente, percentual de Reserva Legal obrigatório, sobreposição com Terras Indígenas (FUNAI), alertas de desmatamento (INPE/DETER), dados climáticos (NASA POWER) — tudo em paralelo.

### Compliance
- **MCR 2.9** — Verifica aptidão ao crédito rural (Resolução CMN 5.193/2024)
- **EUDR** — Verifica conformidade com Regulamento Europeu anti-desmatamento

### Jurisdição Legal
27 estados mapeados com regras específicas de licenciamento ambiental, regularização fundiária, Reserva Legal e particularidades estaduais. Comparador entre estados.

### Dados Agropecuários Reais
Série histórica de produção (10 anos), pecuária municipal, Censo Agropecuário 2017 — tudo do IBGE/SIDRA em tempo real.

### Indicadores Financeiros
SELIC, dólar, IPCA, IGP-M, CDI do Banco Central em tempo real. Crédito rural por município via SICOR/BCB.

## Arquitetura

```
Frontend (Next.js 14+)      ←→    Backend (FastAPI)         ←→    Fontes Públicas
  App Router + TypeScript          75 endpoints                    BrasilAPI (CNPJ)
  Tailwind CSS + shadcn/ui         18 collectors                   FUNAI WFS (TIs)
  Leaflet (mapa interativo)        Consulta paralela               INPE/DETER WFS
  React Query (cache)              Score de risco 5D               IBGE API (malhas, SIDRA)
                                   PDF (ReportLab)                 BCB API (indicadores)
                                   Rate limiting                   NASA POWER (clima)
                                   JWT auth                        DataJud/CNJ (processos)
                                                                   IBAMA (embargos)
                                                                   MTE (Lista Suja)
                                                                   ANM (mineração)
                                                                   ANEEL (energia)
```

## Início Rápido

```bash
cd agrojus/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Acessar
open http://localhost:8000/docs    # Swagger UI (75 endpoints documentados)
open http://localhost:8000/health  # Health check
```

## API — Endpoints Principais

### Busca e Consulta
| Método | Rota | Descrição | Dados |
|--------|------|-----------|-------|
| POST | `/api/v1/search/smart` | Smart search (auto-detecta tipo) | REAL |
| POST | `/api/v1/consulta/completa` | 6 fontes em paralelo | REAL |
| GET | `/api/v1/search/cnpj/{cnpj}` | CNPJ completo | REAL (BrasilAPI) |
| GET | `/api/v1/search/lista-suja` | Lista Suja trabalho escravo | FUNCIONAL |
| GET | `/api/v1/search/validate/{doc}` | Validar CPF/CNPJ | REAL |

### Relatórios e Due Diligence
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/report/due-diligence` | Due diligence completa (JSON) |
| POST | `/api/v1/report/due-diligence/pdf` | Due diligence (PDF) |
| POST | `/api/v1/report/person` | Dossiê de pessoa |
| POST | `/api/v1/report/region` | Inteligência regional |
| POST | `/api/v1/report/buyer` | Relatório comprador |
| POST | `/api/v1/report/lawyer` | Relatório advogado |
| POST | `/api/v1/report/investor` | Relatório investidor |

### Compliance
| Método | Rota | Descrição | Dados |
|--------|------|-----------|-------|
| POST | `/api/v1/compliance/mcr29` | Compliance crédito rural MCR 2.9 | REAL |
| POST | `/api/v1/compliance/eudr` | Compliance EUDR exportação UE | REAL |

### Geoespacial e Mapa
| Método | Rota | Descrição | Dados |
|--------|------|-----------|-------|
| GET | `/api/v1/geo/analyze-point` | Análise completa de ponto (right-click) | REAL |
| GET | `/api/v1/geo/layers/{id}/geojson` | GeoJSON de camada para Leaflet | REAL |
| GET | `/api/v1/geo/terras-indigenas` | Terras Indígenas (FUNAI) | REAL |
| GET | `/api/v1/geo/desmatamento/alertas` | Alertas DETER | REAL |
| GET | `/api/v1/geo/clima` | Dados climáticos (NASA POWER) | REAL |
| GET | `/api/v1/geo/catalogo` | Catálogo de 27 camadas | REAL |
| GET | `/api/v1/geo/municipios/busca` | Buscar município por nome | REAL |
| GET | `/api/v1/geo/municipios/{cod}/malha` | GeoJSON contorno municipal | REAL |
| GET | `/api/v1/geo/municipios/{cod}/producao` | Produção agrícola | REAL |
| GET | `/api/v1/geo/municipios/{cod}/producao/historico` | Série histórica 10 anos | REAL |
| GET | `/api/v1/geo/municipios/{cod}/pecuaria` | Rebanho municipal | REAL |
| GET | `/api/v1/geo/municipios/{cod}/censo-agro` | Censo Agropecuário 2017 | REAL |
| GET | `/api/v1/geo/estados/{uf}/municipios` | Malha municipal do estado | REAL |

### Jurisdição Legal
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/jurisdicao/estado/{uf}` | Regras do estado |
| GET | `/api/v1/jurisdicao/estados` | 27 estados |
| GET | `/api/v1/jurisdicao/reserva-legal` | Cálculo Reserva Legal |
| GET | `/api/v1/jurisdicao/comparar` | Comparar 2 estados |

### Mercado e Financeiro
| Método | Rota | Descrição | Dados |
|--------|------|-----------|-------|
| GET | `/api/v1/market/indicators` | SELIC, dólar, IPCA, CDI | REAL (BCB) |
| GET | `/api/v1/market/indicators/{serie}` | Série histórica BCB | REAL |
| GET | `/api/v1/market/quotes` | Cotações commodities | REFERÊNCIA |
| GET | `/api/v1/market/credit/municipality/{cod}` | Crédito rural SICOR | REAL |

### Processos Judiciais
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/lawsuits/search/{cpf_cnpj}` | Buscar processos por CPF/CNPJ |
| GET | `/api/v1/lawsuits/subject/{code}` | Buscar por assunto (TPU/CNJ) |
| GET | `/api/v1/lawsuits/tribunais` | Listar tribunais e assuntos agro |

### Notícias
| Método | Rota | Descrição |
|--------|------|-----------|
| GET | `/api/v1/news/` | Notícias agro (paginadas) |
| GET | `/api/v1/news/legal` | Notícias jurídicas |
| GET | `/api/v1/news/market` | Notícias de mercado |

### Auth e Monitoramento
| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/auth/register` | Registrar usuário |
| POST | `/api/v1/auth/login` | Login (JWT 24h) |
| GET | `/api/v1/auth/me` | Perfil do usuário |
| POST | `/api/v1/monitoring/property` | Monitorar imóvel |
| GET | `/api/v1/monitoring/alerts` | Alertas de mudança |

## Fontes de Dados — Status Real

### Funcionando com dados REAIS
| Fonte | Dados | API |
|-------|-------|-----|
| **BrasilAPI** | CNPJ completo (razão social, sócios, CNAE, endereço) | REST gratuita |
| **FUNAI GeoServer** | 655+ Terras Indígenas com polígonos | WFS público |
| **INPE/TerraBrasilis** | Alertas desmatamento DETER + biomas | WFS público |
| **IBGE API** | Malhas municipais (5.570 municípios) | REST gratuita |
| **IBGE SIDRA** | Produção agrícola, pecuária, Censo Agro | REST gratuita |
| **BCB API** | SELIC, dólar, IPCA, IGP-M, CDI | REST gratuita |
| **BCB SICOR** | Crédito rural por município | OData gratuita |
| **NASA POWER** | Clima (temp, chuva, umidade, vento) | REST gratuita |
| **ANM** | Processos minerários | ArcGIS REST |
| **ANEEL** | Infraestrutura energética | REST gratuita |
| **IBAMA** | Embargos ambientais (168MB CSV) | Dados abertos |
| **MTE** | Lista Suja trabalho escravo | Dados abertos |
| **Nominatim** | Reverse geocode (coordenada → município) | REST gratuita |

### Aguardando retorno do governo
| Fonte | Problema | Dados |
|-------|----------|-------|
| SICAR/CAR | GeoServer 503 (TLS quebrado) | Polígonos de 6M+ imóveis |
| SIGEF/INCRA | URL mudou (404) | Parcelas certificadas |
| INMET | API intermitente (503) | Estações meteorológicas |

### Planejados (precisam investimento)
| Fonte | Bloqueio | Custo |
|-------|----------|-------|
| SERPRO (CPF completo) | API paga | R$0.66/consulta |
| CENPROT (protestos) | Bloqueia automação | R$0.20 via InfoSimples |
| CAFIR/CNIR | Login gov.br necessário | Playwright + sessão |
| Certidões negativas | Captcha | Scraping + solver |

## Concorrentes e Diferencial

| Funcionalidade | AgroJus | SpectraX | Registro Rural | InfoSimples | ONR |
|---|---|---|---|---|---|
| Consulta unificada (6 fontes) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Smart search auto-detect | ✅ | ❌ | ❌ | ❌ | ❌ |
| Compliance MCR 2.9 + EUDR | ✅ | ✅ | ❌ | ❌ | ❌ |
| Score risco 5 dimensões | ✅ | ❌ | ❌ | ❌ | ❌ |
| Jurisdição 27 estados | ✅ | ❌ | ❌ | ❌ | ❌ |
| Análise de ponto (mapa) | ✅ | ❌ | ❌ | ❌ | ❌ |
| Dados clima por coordenada | ✅ | ✅ | ❌ | ❌ | ❌ |
| API gratuita com Swagger | ✅ | ❌ | Pago | Pago | ❌ |
| Série histórica produção | ✅ | ❌ | ❌ | ❌ | ❌ |
| Indicadores BCB tempo real | ✅ | ❌ | ❌ | ❌ | ❌ |
| Matrícula de imóvel | ❌ | ❌ | ❌ | ❌ | ✅ |
| Satélite alta resolução | ❌ | ✅ | ❌ | ❌ | ❌ |

## Estrutura do Projeto

```
agrojus/
├── backend/
│   ├── app/
│   │   ├── api/              # 14 routers (75 endpoints)
│   │   │   ├── auth.py       # JWT auth (register/login/me)
│   │   │   ├── compliance.py # MCR 2.9 + EUDR
│   │   │   ├── consulta.py   # Consulta unificada 6 fontes
│   │   │   ├── geo.py        # Geoespacial + mapa + clima
│   │   │   ├── jurisdicao.py # Regras por estado
│   │   │   ├── lawsuits.py   # Processos judiciais
│   │   │   ├── market.py     # Cotações + indicadores BCB
│   │   │   ├── monitoring.py # Alertas e monitoramento
│   │   │   ├── news.py       # Notícias agro
│   │   │   ├── report.py     # Due diligence + PDF
│   │   │   ├── search.py     # Busca universal + Lista Suja
│   │   │   └── smart_search.py # Auto-detecção de input
│   │   ├── collectors/       # 18 coletores de dados
│   │   │   ├── bcb.py        # Banco Central (SELIC, dólar)
│   │   │   ├── camadas.py    # Catálogo de 27 camadas geo
│   │   │   ├── cepea.py      # Cotações CEPEA/ESALQ
│   │   │   ├── cpf.py        # CPF (Receita Federal/SERPRO)
│   │   │   ├── datajud.py    # Processos judiciais CNJ
│   │   │   ├── financial.py  # Crédito rural SICOR
│   │   │   ├── geolayers.py  # FUNAI + TerraBrasilis WFS
│   │   │   ├── ibama.py      # Embargos + autuações
│   │   │   ├── ibge.py       # Municípios + SIDRA + malhas
│   │   │   ├── nasa_power.py # Clima (temperatura, chuva)
│   │   │   ├── protestos.py  # CENPROT protestos
│   │   │   └── ...
│   │   ├── services/         # Lógica de negócio
│   │   │   ├── due_diligence.py  # Motor de due diligence
│   │   │   ├── jurisdicao.py     # 27 estados mapeados
│   │   │   ├── pdf_report.py     # Gerador de PDF
│   │   │   └── ...
│   │   ├── middleware/       # Rate limiting por plano
│   │   ├── models/           # SQLAlchemy + Pydantic
│   │   └── config.py         # Settings (env vars)
│   ├── alembic/              # Migrations PostgreSQL
│   ├── tests/                # 82 testes (11 arquivos)
│   └── requirements.txt
├── docs/                     # Documentação
└── docker-compose.yml
```

## Licença

Projeto proprietário. Todos os direitos reservados.
