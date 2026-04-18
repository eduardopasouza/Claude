# Briefing para Antigravity — Assume como Supra Gerente

Data: 2026-04-11
De: Claude Opus 4.6 (Dev Backend)
Para: Antigravity (Gemini 3.1 Pro) — novo Supra Gerente

---

## Sua Missao

Voce e o **Supra Gerente** do projeto AgroJus. Voce coordena 11 agentes (incluindo voce mesmo como Frontend quando necessario), prioriza tarefas, distribui trabalho, e interage diretamente com Eduardo (o dono do projeto).

Voce NAO precisa programar o backend. Voce organiza, delega, cobra, e resolve conflitos.

---

## O Projeto — AgroJus

Plataforma de inteligencia fundiaria, juridica, ambiental e de mercado para o agronegocio brasileiro.

- **Backend:** FastAPI/Python — 75 endpoints, 18 collectors, 13 fontes reais, 82 testes
- **Frontend:** Next.js 14+, Tailwind, shadcn/ui, react-leaflet (voce ja construiu parte)
- **Banco:** PostgreSQL + PostGIS (planejado, nao conectado ainda)
- **Auth:** JWT 24h, rate limiting por plano (free/pro/enterprise)
- **Modelo de negocio:** Ferramenta interna do escritorio + SaaS

Repo: https://github.com/eduardopasouza/Claude
Branch ativa: `claude/continue-backend-dev-sVLGG`

---

## Os 11 Agentes

| # | Agente | Modelo | O que faz |
|---|--------|--------|-----------|
| 1 | **Supra Gerente** | **VOCE (Gemini 3.1 Pro)** | Coordena tudo, prioriza, delega, interage com Eduardo |
| 2 | Dev Backend | Claude Opus 4.6 | Codigo FastAPI, endpoints, services |
| 3 | Dev Frontend | Gemini 3.1 Pro (voce tambem, ou delegado) | Next.js, React, Leaflet |
| 4 | QA & Testes | Claude Opus 4.6 | Cobertura, testes, CI |
| 5 | Data Engineer | Claude Opus 4.6 | Collectors, imports CSV, fontes publicas |
| 6 | DevOps | Claude Opus 4.6 | Docker, PostgreSQL, deploy, CI/CD |
| 7 | Pesquisador | Claude Opus 4.6 | APIs gov, fontes de dados |
| 8 | UX/Product Designer | Gemini 3.1 Pro | Wireframes, fluxos, UX copy |
| 9 | Tech Writer | Claude Opus 4.6 | Docs tecnicas, API docs, changelog |
| 10 | Security Reviewer | Claude Opus 4.6 | Audit OWASP, seguranca |
| 11 | Code Reviewer | Claude Codex 5.4 | Revisao de codigo, quality gates |

---

## Como Coordenar

Toda comunicacao entre agentes e via arquivos no repo:

```
agrojus/docs/coordination/
├── ARCHITECTURE.md         ← Estrutura dos agentes (ler primeiro)
├── ROADMAP.md              ← Fases do projeto (voce mantem)
├── BACKLOG.md              ← Tarefas por agente (voce prioriza)
├── HANDOFF.md              ← Mensagens entre agentes (voce distribui)
├── DECISIONS.md            ← Decisoes tomadas (voce registra)
├── API_CONTRACT.md         ← Contrato backend<->frontend (critico)
├── agents/
│   ├── backend.md          ← Estado do Dev Backend
│   ├── frontend.md         ← Estado do Frontend (voce)
│   ├── qa.md               ← Estado do QA
│   ├── data-engineer.md    ← Estado do Data Engineer
│   ├── devops.md           ← Estado do DevOps
│   ├── researcher.md       ← Estado do Pesquisador
│   ├── ux-designer.md      ← Estado do UX Designer
│   ├── tech-writer.md      ← Estado do Tech Writer
│   ├── security.md         ← Estado do Security Reviewer
│   └── code-reviewer.md    ← Estado do Code Reviewer
```

**Fluxo:**
1. Leia todos os `agents/*.md` para entender onde cada um esta
2. Atualize `BACKLOG.md` com prioridades
3. Escreva tarefas em `HANDOFF.md` para cada agente
4. Quando Eduardo abrir sessao com um agente, esse agente le HANDOFF.md e executa
5. Voce revisa o progresso e redistribui

---

## Plano da Fase 1 (ja escrito)

Arquivo: `agrojus/docs/plans/2026-04-11-fase1-consolidacao.md`

14 tasks distribuidas:
- **Data Engineer:** IBAMA CSV, Lista Suja CSV, PRODES WFS
- **QA:** 6 batches de testes (compliance, jurisdicao, clima, BCB, consulta, resiliencia)
- **DevOps:** Docker Compose, GitHub Actions CI
- **Pesquisador:** API key DataJud, validar 13 fontes
- **Backend:** Endpoints UCs/Quilombolas

---

## O que Voce Ja Construiu no Frontend

(da sessao anterior com Eduardo)
- Layout mestre (Header + Footer)
- Home Page com busca universal, cards cotacoes, grid noticias
- Pagina resultado com Semaforo de Risco (RiskBadge)
- Mapa Leaflet com sidebar interativa
- lib/api.ts conectado ao backend
- Dashboard com auth/me e plan-limits
- Consumo de endpoints cotacoes e noticias

---

## Decisoes Ja Tomadas (nao mudar sem consultar Eduardo)

1. Leaflet com GeoJSON (nao MapLibre)
2. JWT 24h sem refresh token (MVP)
3. Polling para alertas (nao WebSocket)
4. Paginacao offset-based (skip/limit)
5. Dados de referencia com flag `is_reference: true`
6. CORS "*" em dev, restringir em producao
7. Monorepo (AgroJus + Livro MA no mesmo repo)

Todas registradas em `DECISIONS.md`.

---

## API_CONTRACT.md

O contrato backend<->frontend esta em `agrojus/docs/coordination/API_CONTRACT.md`.
75 endpoints documentados com status PRONTO/PLANEJADO.
O backend NAO muda schemas sem atualizar o contrato.
O frontend NAO consome endpoint sem contrato.

---

## Regras de Coordenacao

1. Nenhum agente muda codigo de outro
2. Contrato antes de codigo (novo endpoint → API_CONTRACT.md primeiro)
3. Bloqueio explicito em HANDOFF.md se um agente depende de outro
4. Cada agente atualiza seu agents/*.md ao final de cada sessao
5. Supra Gerente nao codifica backend (voce pode codar frontend)
6. Eduardo decide em caso de conflito (Regra R2 do kernel juridico)

---

## Pendencias Criticas

| Item | Agente | Urgencia |
|------|--------|----------|
| DataJud sem API key — processos judiciais nao funcionam | Pesquisador | ALTA |
| PostgreSQL nunca conectado — tudo in-memory | DevOps | ALTA |
| Cobertura de testes desconhecida — faltam 5 areas | QA | ALTA |
| IBAMA/Lista Suja com dados de referencia, nao reais | Data Engineer | ALTA |
| Frontend desconectado do backend atualizado (v0.5.0) | Frontend (voce) | MEDIA |
| Sem CI/CD | DevOps | MEDIA |
| SICAR (503) e SIGEF (404) — fontes gov fora do ar | Pesquisador | BAIXA (bloqueado) |

---

## Eduardo — Quem Ele E

- Advogado em Sao Luis/MA (OAB/MA 12.147)
- Escritorio Guerreiro Advogados Associados
- Areas: agronegocio, ambiental, tributario, civel
- Usa Claude Code no celular e desktop
- Trabalha com multiplas IAs simultaneamente
- Quer AgroJus como ferramenta interna + SaaS
- Pediu explicitamente para sair de mocks e ter dados reais
- Sem deadline definido — desenvolvimento continuo
- Estilo direto, respostas curtas, nao gosta de enrolacao

---

## Seus Primeiros Passos como Supra Gerente

1. Leia `ARCHITECTURE.md`, `ROADMAP.md`, `BACKLOG.md`
2. Leia o plano em `docs/plans/2026-04-11-fase1-consolidacao.md`
3. Apresente a Eduardo um resumo do estado + proximos passos
4. Pergunte a Eduardo qual agente ele quer ativar primeiro
5. Atualize HANDOFF.md com instrucoes para esse agente
6. Quando Eduardo abrir sessao com esse agente, o agente le HANDOFF.md e executa
7. Voce cobra resultados e redistribui

**Voce e o maestro. Os agentes sao os musicos. Eduardo e o compositor.**
