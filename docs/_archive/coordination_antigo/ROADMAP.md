# AgroJus — Roadmap de Coordenação

**Atualizado:** 2026-04-15 (03:15 BRT)
**Versão:** 2.0

> Documento de controle vivo. Leia `docs/CONTEXTO_COMPLETO.md` para o contexto completo de produto.
> Leia `docs/HANDOFF_2026-04-15.md` para o estado técnico atual.

---

## 📊 Visão Geral dos 5 Módulos

| Módulo | Nome | Status |
|--------|------|--------|
| M1 | Relatório de Conformidade por Imóvel | 🔶 Em desenvolvimento |
| M2 | GIS Map — Mapa Interativo | 🟢 Funcional (GIS Engine v2) |
| M3 | Assessor Agropecuário | 🔶 Parcial (consulta/notícias) |
| M4 | Motor de Valuation Rural | ❌ Não iniciado |
| M5 | Dashboard Bancário (Carteira) | ❌ Não iniciado |

---

## ✅ Fase 1 — Infraestrutura e Dados Core (CONCLUÍDA)

| Tarefa | Status | Entregue em |
|--------|--------|-------------|
| Docker Compose backend + PostgreSQL/PostGIS | ✅ | 2026-04-11 |
| IBAMA embargos: 103.668 registros no PostGIS | ✅ | 2026-04-12 |
| MTE Lista Suja: 614 registros (ETL PDF regex) | ✅ | 2026-04-15 |
| MapBiomas Crédito Rural: 5.6M parcelas (GPKG) | ✅ | 2026-04-12 |
| FUNAI Terras Indígenas: 655 polígonos (WFS) | ✅ | 2026-04-12 |
| DETER Amazônia: 50k alertas no PostGIS | ✅ | 2026-04-13 |
| DETER Cerrado: 50k alertas no PostGIS | ✅ | 2026-04-15 |
| MapBiomas Infraestrutura (armazéns, rodovias, ferrovias, portos) | ✅ | 2026-04-13 |
| MapBiomas Stats (irrigação, mineração, pastagem, cobertura) | ✅ | 2026-04-13 |
| Yahoo Finance scraper (10 cotações CBOT/CME) | ✅ | 2026-04-15 |
| NASA POWER (clima por coordenada) | ✅ | 2026-04-13 |
| IBGE SIDRA (PAM por município) | ✅ | 2026-04-13 |
| Auth JWT (login, registro, rate limiting) | ✅ | 2026-04-15 |
| Dashboard metrics (8 KPIs reais PostgreSQL) | ✅ | 2026-04-15 |

---

## 🔶 Fase 2 — Módulo 1: Relatório de Conformidade (ATUAL)

**Objetivo:** Usuário fornece código CAR ou CPF/CNPJ → AgroJus retorna relatório completo

| Tarefa | Prioridade | Status |
|--------|------------|--------|
| `POST /api/v1/imovel/relatorio` — motor de análise por geometria | ALTA | ❌ Pendente |
| SICAR (CAR): integrar consulta pública por código | ALTA | ❌ Pendente |
| Score MCR 2.9: checklist IBAMA + DETER + CAR + TI | ALTA | ❌ Pendente |
| Score EUDR: desmatamento pós-2019 (PRODES) | ALTA | ❌ Pendente |
| DataJud/CNJ: processos judiciais por CPF/CNPJ | ALTA | ❌ Pendente |
| BCB SICOR: crédito rural por CPF/CNPJ | MEDIA | ⏳ BCB em manutenção |
| ANA Outorgas: risco hídrico por coordenada | MEDIA | ⏳ URL pendente |
| ICMBio UCs: sobreposição no PostGIS | MEDIA | ❌ Download pendente |
| Análise logística: distância a silos, portos, rodovias | MEDIA | ❌ Pendente |
| Export PDF do relatório (WeasyPrint) | MEDIA | ❌ Pendente |
| Export JSON/KML do relatório | BAIXA | ❌ Pendente |

---

## 🔶 Fase 3 — Módulo 2: GIS Map (EM ANDAMENTO)

**Status atual:** GIS Engine v2 funcional — multi-layer, análise de ponto, bbox search

| Tarefa | Prioridade | Status |
|--------|------------|--------|
| Desenho de polígono no mapa → dispara relatório M1 | ALTA | ❌ Pendente |
| Timeline deslizante 1985-2023 (MapBiomas cobertura) | ALTA | ❌ Pendente |
| Busca por código CAR no mapa | ALTA | ❌ Pendente |
| Camada ICMBio UCs | MEDIA | ⏳ Download shapefile |
| Camada PRODES (desmatamento anual) | MEDIA | ❌ Pendente |
| Camada ANM/SIGMINE (mineração) | BAIXA | ❌ Pendente |
| Export PNG do mapa com legenda | BAIXA | ❌ Pendente |
| Login UI: testar fluxo completo no browser | ALTA | 🔶 Em progresso |

---

## 🔴 Fase 4 — Dados Externos Bloqueados

| Tarefa | Bloqueador | Ação necessária |
|--------|------------|-----------------|
| BasedosDados/BigQuery (CNPJ, PAM) | GCP_PROJECT_ID não configurado | Usuário criar projeto GCP grátis |
| BCB SICOR (crédito rural) | 503 em manutenção | Tentar novamente |
| ANA Outorgas de água | URL de download desconhecida | Pesquisar portal |
| ICMBio UCs (shapes) | DNS falha no container | Download manual |
| IBAMA Autos de Infração | CSV retorna vazio (bug portal) | Monitorar |
| SICAR polígonos (via WFS ou API) | Rate limit/autenticação | Avaliar estratégia |

---

## 🟡 Fase 5 — Módulos 3, 4 e 5 (Futuros)

### Módulo 3 — Assessor Agropecuário
| Tarefa | Prioridade |
|--------|------------|
| CONAB safras (área plantada, produção, estoque) | ALTA |
| EMBRAPA ZARC (zoneamento de risco climático por cultura) | ALTA |
| Calendário agrícola interativo por cultura e estado | MEDIA |
| Chat em linguagem natural (integração LLM) | BAIXA |

### Módulo 4 — Motor de Valuation
| Tarefa | Prioridade |
|--------|------------|
| Modelo preditivo R$/ha por município (SIDRA + MapBiomas) | ALTA |
| Comparáveis por bioma, solo, uso da terra | MEDIA |
| Fatores de risco/bonus automatizado | MEDIA |
| MapBiomas Solo (carbono, textura) | BAIXA |

### Módulo 5 — Dashboard Bancário
| Tarefa | Prioridade |
|--------|------------|
| Cadastro de carteira (lista de imóveis) | ALTA |
| Monitor de alertas por carteira (IBAMA, DETER, MTE) | ALTA |
| Webhook para sistemas bancários | MEDIA |
| APScheduler cotações automáticas 09h/18h | ALTA |

---

## 🚀 Fase 6 — Deploy e Produção

| Tarefa | Status |
|--------|--------|
| Deploy backend em Render/AWS/GCP | ❌ Pendente |
| PostgreSQL + PostGIS em produção | ❌ Pendente |
| CORS restrito ao domínio de produção | ❌ Pendente |
| HTTPS + domínio próprio (agrojus.com.br) | ❌ Pendente |
| CI/CD GitHub Actions | ❌ Pendente |
| Rate limiting por plano (free/pro/enterprise) | ❌ Pendente |

---

## 📋 Dependências Externas (requerem ação do usuário)

| Dependência | Para que serve | Como obter |
|---|---|---|
| **GCP_PROJECT_ID** | BasedosDados BigQuery (CNPJ, PAM) | `console.cloud.google.com` → criar projeto grátis |
| **Conta MapBiomas Alerta** | Alertas de desmatamento validados c/ laudo | `plataforma.alerta.mapbiomas.org` → criar conta |
| **Conta GEE** | Google Earth Engine (MapBiomas rasters) | `earthengine.google.com` → solicitar acesso |
| **Convênio ONR** | Matrículas de registro de imóveis | `onr.org.br` → contato comercial |
| **DataJud API key** | Processos judiciais CNJ | `api-publica.datajud.cnj.jus.br` → gratuita |

---

*AgroJus Enterprise — Roadmap v2.0 — 2026-04-15*
