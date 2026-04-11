# Eduardo Pinho — Projetos Claude

Monorepo pessoal com projetos desenvolvidos via Claude Code.

## Projetos

| Pasta | Projeto | Status |
|-------|---------|--------|
| `agrojus/` | **AgroJus** — Plataforma de inteligência fundiária, jurídica e de mercado para o agronegócio | Em desenvolvimento (v0.5.0) |
| `maranhao-book-plugin/` | **Livro do Maranhão** — Pesquisa e redação de livro sobre história e desigualdade no MA | Em produção editorial |

## AgroJus — Início Rápido

```bash
cd agrojus/backend
pip install -r requirements.txt
uvicorn app.main:app --reload
# Swagger: http://localhost:8000/docs (75 endpoints)
```

Detalhes completos em [`agrojus/README.md`](agrojus/README.md).
