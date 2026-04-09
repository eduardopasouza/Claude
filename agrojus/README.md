# AgroJus

**Plataforma de Inteligência Fundiária, Jurídica e de Mercado para o Agronegócio**

AgroJus é uma plataforma que cruza dados públicos de múltiplas fontes para oferecer relatórios de due diligence rural, dossiês de pessoas, inteligência regional, cotações de mercado e notícias curadas do agronegócio — tudo com foco em segurança jurídica.

## O que o AgroJus faz

### Para o Comprador de Imóvel Rural
Informe qualquer dado que você tenha do imóvel (CAR, matrícula, SNCR, NIRF, CCIR, ITR, coordenadas GPS) e receba um relatório completo: regularidade fundiária, sobreposições com terras indígenas e unidades de conservação, embargos IBAMA, situação do proprietário, preço de mercado da região.

### Para o Advogado
Diligência automatizada sobre pessoas e imóveis: processos judiciais, certidões negativas, lista suja do trabalho escravo, situação cadastral, embargos ambientais, histórico fundiário. Score de risco jurídico.

### Para o Investidor / Banco / Cooperativa
Análise de risco para crédito rural, avaliação de ativos, dados de produção agrícola, preços de terra, informações de FIAGRO. Integração via API.

### Para o Agropecuarista
Cotações de commodities, notícias do agronegócio, previsão de safra, dados da região, documentação do imóvel.

## Arquitetura

```
Frontend (Next.js)          ←→    Backend (FastAPI/Python)    ←→    PostgreSQL + PostGIS
  - Portal de notícias               - API REST                      - Imóveis
  - Mapa interativo                  - Coletores de dados             - Pessoas
  - Relatórios PDF                   - Processamento geoespacial      - Processos
  - Dashboard                        - Score de risco                  - Cotações
                                     - Geração de PDF                  - Cache
```

## Stack Técnica

| Camada | Tecnologia |
|--------|-----------|
| Backend | Python 3.12 + FastAPI |
| Banco de dados | PostgreSQL 16 + PostGIS 3.4 |
| Geoespacial | GeoPandas, Shapely, PyProj |
| Scraping | Playwright, httpx, BeautifulSoup |
| PDF | ReportLab |
| Frontend | Next.js + React + Leaflet/MapLibre |
| Infraestrutura | Docker + docker-compose |

## Início Rápido

```bash
# Subir banco de dados + backend
docker-compose up -d

# Ou rodando localmente
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Testar
curl http://localhost:8000/health
curl http://localhost:8000/docs  # Swagger UI
```

## Endpoints Principais

| Método | Rota | Descrição |
|--------|------|-----------|
| POST | `/api/v1/search/property` | Busca universal de imóvel (qualquer identificador) |
| POST | `/api/v1/report/due-diligence` | Relatório de due diligence (JSON) |
| POST | `/api/v1/report/due-diligence/pdf` | Relatório de due diligence (PDF) |
| POST | `/api/v1/report/buyer` | Relatório para comprador |
| POST | `/api/v1/report/lawyer` | Relatório para advogado |
| POST | `/api/v1/report/investor` | Relatório para investidor |
| POST | `/api/v1/report/person` | Dossiê de pessoa (CPF/CNPJ) |
| POST | `/api/v1/report/region` | Inteligência regional |
| GET | `/api/v1/map/layers` | Camadas do mapa |
| GET | `/api/v1/market/quotes` | Cotações de commodities |
| GET | `/api/v1/news/` | Notícias do agronegócio |
| GET | `/api/v1/news/legal` | Notícias jurídicas |

Documentação completa: [docs/API.md](docs/API.md)

## Fontes de Dados

| Fonte | Dados | Status |
|-------|-------|--------|
| SICAR/CAR | Perímetros de imóveis, APP, RL | Ativo |
| SIGEF/INCRA | Parcelas certificadas | Ativo |
| Receita Federal | CNPJ (BrasilAPI) | Ativo |
| IBAMA | Embargos ambientais | Ativo |
| Lista Suja/MTE | Trabalho escravo | Ativo |
| SICOR/BCB | Crédito rural | Ativo |
| IBGE/SIDRA | Produção agrícola | Ativo |
| CEPEA/ESALQ | Cotações commodities | Placeholder |
| CONAB | Dados de safra | Placeholder |
| Portais Agro | Notícias (RSS) | Ativo |
| Cartórios/ONR | Matrícula | Em desenvolvimento |
| Tribunais | Processos judiciais | Em desenvolvimento |
| FUNAI | Terras indígenas | Shapefile (manual) |
| ICMBio | Unidades de conservação | Shapefile (manual) |

Documentação completa: [docs/DATA_SOURCES.md](docs/DATA_SOURCES.md)

## Documentação

- [Arquitetura Técnica](docs/ARCHITECTURE.md)
- [API Completa](docs/API.md)
- [Fontes de Dados](docs/DATA_SOURCES.md)
- [Especificação do Frontend](docs/FRONTEND_SPEC.md)

## Licença

Projeto proprietário. Todos os direitos reservados.
