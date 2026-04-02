# Auditoria Factual — Quem é o Maranhão?

> Verificação dos 20 dados mais críticos do livro contra fontes web reais.
> Data: 2026-04-01

---

## Dados Confirmados ✅

| # | Dado | Valor | Fonte verificada | Status |
|---|------|-------|-----------------|--------|
| 1 | Área MA | 329.651,478 km² | IBGE 2024 | ✅ |
| 2 | Biomas | Cerrado ~65%, Amazônia ~34%, Caatinga ~1% | IBGE | ✅ |
| 3 | População | 6.776.699 | Censo IBGE 2022 | ✅ |
| 4 | IDH | 0,676 (menor do Brasil) | PNUD 2021 | ✅ |
| 5 | Quilombos certificados | 1.152 | Fundação Palmares | ✅ |
| 6 | Indígenas | 57.214 | Censo IBGE 2022 | ✅ |
| 7 | Mangues | 505.490 ha, 36% do Brasil | ICMBio Atlas | ✅ |
| 8 | Vale > PIB MA | Lucro Vale 2021 > PIB MA 2019 | Mongabay | ✅ |
| 9 | Quebradeiras | ~300.000 | MIQCB/JMTV | ✅ |
| 10 | Porto Itaqui | 23m profundidade natural | Porto do Itaqui oficial | ✅ |
| 11 | Soja MA | ~1,2M ha (2024) | IBGE/Conab | ✅ |
| 12 | Quilombolas autodeclarados | 269.074 | Censo 2022 (DADO NOVO) | 📝 |

## Dados com Divergência ⚠️ — CORRIGIR

| # | Dado | Valor no livro | Valor correto | Ação |
|---|------|---------------|---------------|------|
| 13 | Amazônia destruída | 76% | **75-76%** (fontes variam: ISA diz 76%, SOS Amazônia diz 75%) | Manter 76% com nota de que fontes variam entre 75-76% |
| 14 | Lençóis área | 156.562 ha | **155.000 ha** (Decreto 86.060/1981). A UNESCO/SGB pode usar área expandida (156.562 incluindo zona de amortecimento) | **CORRIGIR** V09, V10: usar 155.000 ha como área do Parque. Notar que UNESCO pode citar área maior |
| 15 | Esgoto tratado | 3,92% | **13,6%** (Trata Brasil 2022, dado SNIS). 3,92% é dado antigo/incorreto | **CORRIGIR** V94, V98: atualizar para 13,6% (tratamento) e 32,49% (coleta). Ainda péssimo, mas não 3,92% |

## Dados Não Verificados — Fontes insuficientes

| # | Dado | Observação |
|---|------|-----------|
| 16 | Algodão 651 → 30.000 arrobas | Fonte: Meireles (2001). Dado histórico, difícil verificar online. Manter com citação de Meireles |
| 17 | Escravizados 85% Itapecuru | Fonte: Meireles/Ribeiro Jr. Dado histórico. Manter com citação |
| 18 | Negro Cosme 3.000 escravizados | Fonte: Assunção (1988). Dado histórico. Manter com citação |

## Ações Necessárias

### Prioridade 1 — Corrigir dados errados
1. ~~Esgoto 3,92%~~ → **13,6%** em V94 e V98
2. ~~Lençóis 156.562 ha~~ → **155.000 ha** em V09 e V10 (com nota sobre UNESCO)

### Prioridade 2 — Adicionar dados novos
1. Quilombolas autodeclarados: 269.074 (Censo 2022) → adicionar ao banco YAML e V35

### Prioridade 3 — Padronizar dados variáveis
1. Amazônia destruída: padronizar como "76%" com nota "(fontes variam entre 75-76%)"

---

*Auditoria realizada em 2026-04-01 com busca web via Tavily.*
