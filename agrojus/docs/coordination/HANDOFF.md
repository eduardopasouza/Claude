# AgroJus — Handoff entre Agentes

Mensagens entre agentes. Formato: `### ORIGEM -> DESTINO` com data.
Cada agente le as mensagens destinadas a ele ao iniciar sessao.
Mensagens resolvidas sao movidas para o final em "## Arquivo".

---

## 2026-04-11

### GERENTE -> TODOS
Arquitetura multi-agente aprovada. Cada agente deve:
1. Ler seu arquivo em `agents/[nome].md` ao iniciar
2. Ler este HANDOFF.md filtrando mensagens para si
3. Atualizar `agents/[nome].md` ao final da sessao
4. Escrever aqui se precisar de algo de outro agente

### GERENTE -> DATA-ENGINEER
Prioridade AGORA (Fase 1):
1. Importar IBAMA embargos coordenadas (CSV 8MB)
2. Importar Lista Suja completa (CSV Portal Transparencia)
3. Baixar shapefiles UCs (ICMBio) e Quilombolas (INCRA)
Quando pronto, atualizar agents/data-engineer.md.

### GERENTE -> QA
Prioridade AGORA (Fase 1):
1. Medir cobertura atual com pytest-cov
2. Adicionar testes para: compliance, jurisdicao, clima, BCB, consulta unificada
3. Adicionar testes de resiliencia (timeout, 500, JSON invalido)

### GERENTE -> DEVOPS
Prioridade AGORA (Fase 1):
1. Testar docker-compose.yml existente
2. Garantir PostgreSQL + PostGIS subindo
3. Testar Alembic migrations contra banco real
4. Configurar GitHub Actions basico (lint + pytest)

### GERENTE -> PESQUISADOR
Prioridade AGORA:
1. Cadastrar API key DataJud/CNJ (gratuita, 5 min)
2. Testar se SICAR e SIGEF voltaram ao ar
3. Validar as 13 fontes reais — quais ainda respondem?

### GERENTE -> BACKEND
Aguardar Data Engineer entregar collectors UCs/Quilombolas.
Enquanto isso:
1. Preparar endpoints GET /geo/unidades-conservacao e /geo/quilombolas
2. Revisar API_CONTRACT.md quando Gerente criar

### GERENTE -> FRONTEND
API_CONTRACT.md sera criado em breve.
Prioridades quando contrato estiver pronto:
1. Integrar analyze-point no right-click do Leaflet
2. Painel de camadas toggle
3. Paginas de compliance e jurisdicao

---

## Arquivo (resolvidos)

(vazio)
