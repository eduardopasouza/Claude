# AgroJus — Handoff de Contexto (coordination)

> Este é o handoff de coordenação entre agentes/sessões.
> Para o handoff técnico completo, veja: `docs/HANDOFF_2026-04-15.md`
> Para o contexto de produto completo, veja: `docs/CONTEXTO_COMPLETO.md`
> Atualizado: 2026-04-15

---

## Estado de Desenvolvimento — Fase Atual

**Fase:** 7.5 concluída → iniciando Módulo 1 (Relatório de Conformidade)
**Versão:** v0.7.0
**Branch:** `claude/continue-backend-dev-sVLGG`
**Último commit:** `42d6413` — docs: PESQUISA_FONTES.md

---

## O que está funcional

```
✅ Infrastructure: Docker Compose (backend FastAPI + PostgreSQL/PostGIS)
✅ Auth: JWT login/register (backend completo, frontend overlay adicionado)
✅ GIS Engine v2: Leaflet multi-layer, análise de ponto, bbox search
✅ Dashboard: 8 KPIs reais de PostgreSQL + cotações Yahoo Finance
✅ Compliance API: /dossier/{cpf_cnpj} (IBAMA + MTE)
✅ Geo API: /layers/{id}/geojson (20+ camadas do PostGIS)
✅ Market API: /quotes (10 commodities CBOT/CME em BRL)
✅ NASA POWER: clima por coordenada
✅ IBGE SIDRA: produção agrícola por município
```

## O que está bloqueado / pendente

```
⏳ BasedosDados BigQuery → precisa GCP_PROJECT_ID (ação do usuário)
⏳ BCB SICOR → 503 manutenção BCB
⏳ ANA Outorgas → URL de download desconhecida
⚠️ ICMBio UCs → download manual pendente (DNS falha no container)
❌ Score MCR 2.9 → não implementado
❌ POST /api/v1/imovel/relatorio → não implementado
❌ MapBiomas Alerta → conta não criada
❌ PRODES full → só 50k do WFS, precisamos 800k+
```

## Próxima tarefa de desenvolvimento

**Módulo 1 — Relatório de Conformidade:**
```
POST /api/v1/imovel/relatorio
Input:  { tipo: "car"|"geojson"|"cpf_cnpj", valor: "..." }
Output: Score MCR 2.9 + Score EUDR + Embargos + TIs + DETER + Crédito + Logística + PDF
```

---

## Agentes e Responsabilidades

| Agente | Foco |
|---|---|
| **Antigravity (Claude/Gemini)** | Desenvolvimento full-stack — código, ETLs, APIs, frontend |
| **Supra Gerente** | Coordenação, decisões de produto, roadmap |
| **Usuário (Eduardo)** | Fornece credenciais (GCP), valida dados, testa no browser |
