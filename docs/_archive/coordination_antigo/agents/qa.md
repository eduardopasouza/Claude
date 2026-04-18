# QA & Testes — Estado

Modelo: Claude Opus 4.6
Ultima atualizacao: 2026-04-11

## Estado Atual

- Testes: 82 passando (11 arquivos)
- Cobertura: nao medida (sem pytest-cov)
- CI: nao configurado

## Cobertura por Area

| Area | Testes | Status |
|------|--------|--------|
| Auth | 5 | Coberto |
| Validators (CPF/CNPJ) | 8 | Coberto |
| Smart Search | 18 | Coberto |
| Risk Score | 9 | Coberto |
| API Health | 14 | Coberto |
| Lista Suja | 13 | Coberto |
| Rate Limit | 6 | Coberto |
| Dossie Pessoa | 5 | Coberto |
| Geo + Lawsuits | 9 | Coberto |
| Compliance | 0 | **FALTA** |
| Jurisdicao | 0 | **FALTA** |
| Clima (NASA) | 0 | **FALTA** |
| BCB indicadores | 0 | **FALTA** |
| Consulta unificada | 0 | **FALTA** |
| Resiliencia (timeout/500) | 0 | **FALTA** |

## Proximas Tarefas

1. Instalar pytest-cov, medir cobertura baseline
2. Testes compliance (MCR 2.9, EUDR)
3. Testes jurisdicao (27 estados, comparador)
4. Testes clima (NASA POWER)
5. Testes BCB (indicadores, SICOR)
6. Testes consulta unificada
7. Testes de resiliencia: simular timeout, HTTP 500, JSON invalido
8. Meta: 90%+ cobertura
