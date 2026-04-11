# Code Reviewer — Estado

Modelo: Claude Codex 5.4 (mente externa)
Ultima atualizacao: 2026-04-11

## Responsabilidade

- Revisao de codigo produzido por outros agentes
- Quality gates antes de merge
- Identificar bugs, code smells, problemas de performance
- Verificar aderencia aos padroes do projeto
- Sugerir refatoracoes e melhorias
- Revisar PRs antes de merge para main

## Quando Acionar

- Apos Dev Backend completar uma feature/task
- Apos Data Engineer entregar novo collector
- Antes de merge de qualquer branch para main
- Quando QA encontrar bug — revisar causa raiz
- Periodicamente para audit geral de code quality

## Padroes do Projeto

- Python 3.11+, FastAPI, async/await
- Collectors herdam de BaseCollector (app/collectors/base.py)
- Cache filesystem com TTL (BaseCollector._get_cached/_set_cached)
- Erros nao silenciados — logger.warning + fallback
- Pydantic para schemas, SQLAlchemy para models
- Testes com pytest + TestClient(app)

## Proximas Tarefas

1. [ ] Revisar collectors existentes — consistencia de padrao
2. [ ] Revisar score de risco — logica de comparacao
3. [ ] Revisar due diligence engine — tratamento de erros
4. [ ] Revisar auth JWT — seguranca basica
5. [ ] Estabelecer checklist de review padrao
