# AgroJus — API Contract (Backend <-> Frontend)

Atualizado: 2026-04-11
Responsavel: Supra Gerente + Dev Backend

Este documento e o contrato entre backend e frontend.
O backend NAO muda response schemas sem atualizar este contrato.
O frontend NAO consome endpoints sem contrato.

---

## Convencoes

- Base URL: `http://localhost:8000/api/v1`
- Auth: Bearer token JWT no header `Authorization`
- Paginacao: `?skip=0&limit=20` (offset-based)
- Erros: `{ "detail": "mensagem" }` com HTTP status code
- Dados de referencia: campo `is_reference: true` quando fonte real indisponivel
- Rate limit headers: `X-RateLimit-Remaining-Searches`, `X-RateLimit-Remaining-Reports`

---

## Endpoints — Status

### Auth
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| POST | /auth/register | PRONTO | `{ access_token, token_type, user: { id, email, name, plan } }` |
| POST | /auth/login | PRONTO | `{ access_token, token_type, user: { id, email, name, plan } }` |
| GET | /auth/me | PRONTO | `{ id, email, name, plan, searches_today, reports_today }` |

### Smart Search
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| POST | /search/smart | PRONTO | `{ detected_type, query, results: [...], suggestions: [...] }` |

### Busca
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| GET | /search/cnpj/{cnpj} | PRONTO | Dados completos CNPJ (BrasilAPI) |
| GET | /search/lista-suja | PRONTO | `{ records: [...], total, is_reference }` |
| GET | /search/validate/{doc} | PRONTO | `{ document, type, valid, formatted }` |

### Consulta Unificada
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| POST | /consulta/completa | PRONTO | `{ cpf_cnpj, sources: { receita, ibama, lista_suja, datajud, sicor, protestos }, risk_score, timestamp }` |

### Relatorios
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| POST | /report/due-diligence | PRONTO | JSON completo de due diligence |
| POST | /report/due-diligence/pdf | PRONTO | application/pdf |
| POST | /report/person | PRONTO | Dossie de pessoa |
| POST | /report/region | PRONTO | Inteligencia regional |
| POST | /report/buyer | PRONTO | Relatorio comprador |
| POST | /report/lawyer | PRONTO | Relatorio advogado |
| POST | /report/investor | PRONTO | Relatorio investidor |

### Compliance
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| POST | /compliance/mcr29 | PRONTO | `{ compliant, checks: [...], score, recommendations }` |
| POST | /compliance/eudr | PRONTO | `{ compliant, checks: [...], risk_level }` |

### Geoespacial
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| GET | /geo/analyze-point?lat=X&lng=Y | PRONTO | `{ municipio, estado, orgao_ambiental, reserva_legal_pct, terras_indigenas, desmatamento, clima }` |
| GET | /geo/layers/{id}/geojson | PRONTO | GeoJSON FeatureCollection |
| GET | /geo/terras-indigenas?bbox=X | PRONTO | GeoJSON FeatureCollection |
| GET | /geo/desmatamento/alertas?bbox=X | PRONTO | GeoJSON FeatureCollection |
| GET | /geo/clima?lat=X&lng=Y | PRONTO | `{ temperature, precipitation, humidity, wind, solar }` |
| GET | /geo/catalogo | PRONTO | `{ layers: [{ id, name, category, active, source }] }` |
| GET | /geo/municipios/busca?q=X | PRONTO | `{ municipios: [{ codigo, nome, uf }] }` |
| GET | /geo/municipios/{cod}/malha | PRONTO | GeoJSON do contorno |
| GET | /geo/municipios/{cod}/producao | PRONTO | Producao agricola |
| GET | /geo/municipios/{cod}/producao/historico | PRONTO | Serie 10 anos |
| GET | /geo/municipios/{cod}/pecuaria | PRONTO | Rebanho municipal |
| GET | /geo/municipios/{cod}/censo-agro | PRONTO | Censo 2017 |
| GET | /geo/estados/{uf}/municipios | PRONTO | Malha municipal |
| GET | /geo/unidades-conservacao | PLANEJADO | GeoJSON UCs |
| GET | /geo/quilombolas | PLANEJADO | GeoJSON comunidades |

### Jurisdicao
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| GET | /jurisdicao/estado/{uf} | PRONTO | Regras do estado |
| GET | /jurisdicao/estados | PRONTO | Lista 27 estados |
| GET | /jurisdicao/reserva-legal | PRONTO | Calculo RL |
| GET | /jurisdicao/comparar?uf1=X&uf2=Y | PRONTO | Comparativo |

### Mercado
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| GET | /market/indicators | PRONTO | `{ selic, dolar, ipca, igpm, cdi }` |
| GET | /market/indicators/{serie} | PRONTO | Serie historica BCB |
| GET | /market/quotes | PRONTO | Cotacoes commodities (referencia) |
| GET | /market/credit/municipality/{cod} | PRONTO | Credito rural SICOR |

### Processos
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| GET | /lawsuits/search/{cpf_cnpj} | PRONTO* | *Precisa API key DataJud |
| GET | /lawsuits/subject/{code} | PRONTO* | *Precisa API key DataJud |
| GET | /lawsuits/tribunais | PRONTO | Lista tribunais e assuntos agro |

### Noticias
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| GET | /news/ | PRONTO | `{ articles: [...], total }` |
| GET | /news/legal | PRONTO | Noticias juridicas |
| GET | /news/market | PRONTO | Noticias mercado |

### Monitoramento
| Metodo | Rota | Status | Response |
|--------|------|--------|----------|
| POST | /monitoring/property | PRONTO | Registrar monitoramento |
| GET | /monitoring/alerts | PRONTO | Alertas de mudanca |
