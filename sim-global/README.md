# sim-global

Simulador histórico-estratégico turn-based local. Frontend visual no
browser, backend Python, motor narrativo via Claude Opus 4.7 com OAuth
da assinatura Claude Pro/Max — sem API key paga, sem cloud externa.

Documentação completa em [`BRIEFING.md`](BRIEFING.md) (estratégia) e
[`CLAUDE.md`](CLAUDE.md) (constituição operacional).

## Como rodar (a implementar)

```bash
# uma vez, na sua máquina
claude setup-token                    # gera CLAUDE_CODE_OAUTH_TOKEN
export CLAUDE_CODE_OAUTH_TOKEN=...    # ou põe no .env

# instalar dependências
cd backend
pip install -e ".[dev]"
cd ..

# rodar
python -m simglobal
# → backend sobe em http://localhost:8000
# → browser abre automaticamente
```

## Estrutura

```
sim-global/
├── backend/                # Python: FastAPI + simengine + Agent SDK
├── frontend/               # HTMX + Alpine.js + Tailwind via CDN
├── data/                   # mapa Natural Earth + bandeiras + retratos
├── examples/               # cenários-piloto (Brasil/1930)
└── saves/                  # SQLite local (gitignored)
```

## Cenário de exemplo

[`examples/brasil-vargas-1930/`](examples/brasil-vargas-1930/) é o
cenário-piloto: Brasil em 03/11/1930 (posse de Vargas), 10 regiões
brasileiras + 10 polities-bloco externas, 30 eventos pré-programados
até 1945. Lore com fontes citadas em Wikipedia, IBGE, FGV CPDOC e
Biblioteca Nacional Digital. Serve como fixture de teste e como
referência de formato esperado pelo `scenario_builder`.

## Status

Em construção. Roadmap em [`BRIEFING.md`](BRIEFING.md) §10. Acompanhe
em `git log --oneline`.
