# Security Reviewer — Estado

Modelo: Claude Opus 4.6
Ultima atualizacao: 2026-04-11

## Responsabilidade

- Audit de seguranca OWASP Top 10
- Revisao de auth/JWT
- Validacao de input (injection, XSS)
- Seguranca de APIs externas (secrets, tokens)
- Revisao de CORS e headers de seguranca
- Dependencias com vulnerabilidades conhecidas

## Estado Atual

Nenhuma auditoria de seguranca realizada ate o momento.

### Pontos de Atencao Conhecidos

| Area | Risco | Severidade |
|------|-------|------------|
| CORS allow_origins=["*"] | Qualquer dominio pode acessar | MEDIA (dev only) |
| JWT sem refresh token | Token valido por 24h se comprometido | BAIXA (MVP) |
| Auth in-memory | Sem persistencia, sem rate limit no login | MEDIA |
| Sem HTTPS | Tokens trafegam em texto claro (localhost) | ALTA (producao) |
| Secrets em .env | Sem vault, sem rotacao | MEDIA |
| Sem rate limit no login | Brute force possivel | MEDIA |
| httpx verify=True | Correto, mas SICAR tentou verify=False | BAIXA (nao usado) |
| SQL injection | SQLAlchemy ORM protege, mas verificar raw queries | BAIXA |
| Dependencias | Nunca auditadas (pip-audit) | DESCONHECIDA |

## Proximas Tarefas

1. [ ] Rodar pip-audit nas dependencias
2. [ ] Audit OWASP Top 10 completo no backend
3. [ ] Revisar JWT: algoritmo, secret strength, claims
4. [ ] Verificar se ha raw SQL queries (risco injection)
5. [ ] Revisar validacao de input em todos os endpoints (CPF, CNPJ, coords, etc.)
6. [ ] Adicionar rate limit no endpoint de login
7. [ ] Revisar headers de seguranca (X-Content-Type-Options, X-Frame-Options, CSP)
8. [ ] Verificar se .env.example nao contem secrets reais
9. [ ] Plano de seguranca para producao (HTTPS, vault, rotacao de secrets)
