# AgroJus — Decisoes de Arquitetura

Registro de decisoes tomadas. Formato ADR simplificado.

---

## D001 — Monorepo pessoal (2026-04-11)

**Decisao:** Manter repo `eduardopasouza/Claude` como monorepo com multiplos projetos.
**Contexto:** Repo contem AgroJus e Livro do Maranhao.
**Alternativa rejeitada:** Repos separados por projeto.
**Motivo:** Eduardo prefere manter tudo junto.

## D002 — Arquitetura multi-agente com 7 sessoes (2026-04-11)

**Decisao:** 7 agentes especializados (Gerente, Backend, Frontend, QA, Data Engineer, DevOps, Pesquisador).
**Contexto:** Projeto cresceu alem do que 1 sessao consegue cobrir. Frontend com Antigravity (Gemini).
**Alternativa rejeitada:** 5 agentes (sem Data Engineer e Pesquisador separados).
**Motivo:** As pendencias de fontes de dados e pesquisa de APIs sao trabalho suficiente para agentes dedicados.

## D003 — Comunicacao via arquivos no repo (2026-04-11)

**Decisao:** Agentes se comunicam via `docs/coordination/` — HANDOFF.md, agents/*.md, API_CONTRACT.md.
**Contexto:** Agentes rodam em sessoes separadas sem comunicacao direta.
**Alternativa rejeitada:** Banco de dados compartilhado, Slack, ou issue tracker.
**Motivo:** Arquivos no repo sao versionados, auditaveis, e acessiveis por todos os agentes.

## D004 — Leaflet com GeoJSON (pre-existente)

**Decisao:** react-leaflet para mapa interativo, GeoJSON RFC 7946.
**Alternativa rejeitada:** MapLibre, Mapbox GL JS, Deck.gl.
**Motivo:** Simplicidade para MVP. Confirmado com Antigravity.

## D005 — JWT 24h sem refresh token (pre-existente)

**Decisao:** Access token de 24h, sem refresh token.
**Motivo:** Suficiente para MVP. Nao sobrecarregar arquitetura.

## D006 — PostgreSQL + PostGIS para producao (pre-existente)

**Decisao:** PostgreSQL com PostGIS. Em dev roda sem banco (in-memory).
**Motivo:** Necessario para queries geoespaciais em producao.

## D007 — Rate limiting por plano (pre-existente)

**Decisao:** free=10/dia, pro=500/dia, enterprise=ilimitado. In-memory.
**Motivo:** Modelo SaaS. Redis para producao (futuro).

## D008 — Dados de referencia como fallback (pre-existente)

**Decisao:** Quando fonte real indisponivel, retornar dados de referencia com flag `is_reference: true`.
**Motivo:** Frontend nunca recebe erro vazio. Transparencia sobre origem dos dados.
