# Data Engineer — Estado

Modelo: Claude Opus 4.6
Ultima atualizacao: 2026-04-11

## Estado Atual

- Collectors existentes: 18
- Fontes reais funcionando: 13
- Fontes com fallback: 3 (CEPEA, noticias, Lista Suja parcial)
- Fontes bloqueadas: 3 (SICAR 503, SIGEF 404, INMET 503)

## Fontes Integradas

| Fonte | Collector | Dados Reais | Status |
|-------|-----------|-------------|--------|
| BrasilAPI (CNPJ) | receita_federal.py | Sim | OK |
| FUNAI WFS (TIs) | geolayers.py | Sim | OK |
| INPE/DETER (desmat) | geolayers.py | Sim | OK |
| IBGE (malhas) | ibge.py | Sim | OK |
| IBGE SIDRA (producao) | ibge.py | Sim | OK |
| BCB (indicadores) | bcb.py | Sim | OK |
| BCB SICOR (credito) | financial.py | Sim | OK |
| NASA POWER (clima) | nasa_power.py | Sim | OK |
| ANM (mineracao) | camadas.py | Sim | OK |
| ANEEL (energia) | camadas.py | Sim | OK |
| Nominatim (geocode) | ibge.py | Sim | OK |
| IBAMA (embargos) | ibama.py | Parcial | Referencia local |
| MTE (Lista Suja) | slave_labour.py | Parcial | Referencia local |
| CEPEA (cotacoes) | cepea.py | Nao | 403, fallback |
| DataJud (processos) | datajud.py | Nao | Sem API key |
| SICAR (CAR) | sicar.py | Nao | 503 |
| SIGEF (parcelas) | sigef.py | Nao | 404 |
| CPF (SERPRO) | cpf.py | Nao | Pago |

## Proximas Tarefas (Fase 1)

1. [ ] IBAMA embargos coords (CSV 8MB) — download + parser
2. [ ] Lista Suja completa (CSV Portal Transparencia)
3. [ ] Shapefiles UCs/Unidades Conservacao (ICMBio)
4. [ ] Shapefiles Quilombolas (INCRA)
5. [ ] PRODES desmatamento acumulado (TerraBrasilis WFS)

## Proximas Tarefas (Fase 2)

6. [ ] IBAMA embargos completo (168MB CSV -> PostgreSQL)
7. [ ] CONAB: custo producao, precos, safra
8. [ ] Precos de terra (INCRA + IEA-SP)
