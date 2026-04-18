# Dev Backend — Estado

Modelo: Claude Opus 4.6 (Claude Code)
Ultima atualizacao: 2026-04-11

## Estado Atual

- Versao: v0.5.0
- Endpoints: 75
- Collectors: 18
- Testes: 82 passando
- Branch: claude/continue-backend-dev-sVLGG (12 commits)

## Progresso

- [x] FastAPI base com lifespan, CORS, rate limiting
- [x] Auth JWT (register/login/me) com fallback in-memory
- [x] 13 fontes de dados reais funcionando
- [x] Consulta unificada (6 fontes em paralelo)
- [x] Smart search (auto-detect input)
- [x] Analyze-point (right-click no mapa)
- [x] Compliance MCR 2.9 + EUDR
- [x] Jurisdicao legal 27 estados + comparador
- [x] Serie historica producao/pecuaria (IBGE SIDRA)
- [x] Indicadores BCB tempo real
- [x] Due diligence engine + PDF report
- [x] Score de risco 5 dimensoes
- [x] Logging estruturado
- [x] Alembic migrations configuradas

## Bloqueios

- DataJud precisa de API key (Pesquisador vai cadastrar)
- Endpoints UCs/Quilombolas aguardam Data Engineer entregar shapefiles

## Proximas Tarefas

1. Preparar endpoints GET /geo/unidades-conservacao e /geo/quilombolas
2. Revisar API_CONTRACT.md quando Gerente criar
3. Aguardar Data Engineer para novos collectors
