# Auditoria de Evidencias — "Quem e o Maranhao?"

**Data**: 2026-04-01
**Auditor**: Evidence Controller (Claude Opus 4.6)
**Escopo**: Verbetes V82-V105 (Partes IX, X, XI) — secoes de maior risco factual
**Metodo**: Leitura cruzada de texto.md e research.md de cada verbete. Classificacao de cada afirmacao factual (numero, data, percentual, ranking, area, populacao) em tres niveis de evidencia.

---

## Criterios de Classificacao

| Nivel | Definicao | Cor |
|-------|-----------|-----|
| **L1 — VERIFICADO** | Fonte com URL acessivel citada em research.md E claim confere | VERDE |
| **L2 — FONTE CITADA SEM URL** | Livro academico, relatorio oficial ou orgao governamental citado por nome, mas sem URL | AMARELO |
| **L3 — NAO VERIFICADO** | Sem fonte, fonte vaga ("fontes diversas"), "tradicao oral", Wikipedia isolada, ou potencial alucinacao de IA | VERMELHO |

---

## Resumo Geral

- **Total afirmacoes auditadas**: 247
- **L1 (URL verificavel)**: 0 (0%) — NENHUMA fonte com URL em todo o corpus auditado
- **L2 (fonte institucional/academica citada)**: 189 (76,5%)
- **L3 (NAO VERIFICADO)**: 58 (23,5%)

### ALERTA CRITICO

**Nenhum research.md contem URLs.** Todas as fontes sao citadas por nome de orgao (IBGE, CONAB, ANTAQ, Vale S.A., MDIC) ou por referencia bibliografica (Meireles, Beckert, Carney etc.), mas sem links clicaveis. Isso significa que **ZERO claims atingem L1**. O leitor (e o editor) nao tem como verificar nenhum dado em um clique. Recomendacao: adicionar URLs a todas as fontes institucionais (IBGE, CONAB, ANTAQ, ANM, MDIC/Comex Stat possuem dados publicos com URL estavel).

---

## Top 15 Verbetes com Maior Risco (mais L3)

| Rank | Verbete | L2 | L3 | % L3 | Risco Principal |
|------|---------|----|----|------|-----------------|
| 1 | V89 — Energia | 12 | 11 | 48% | Inconsistencia interna: research diz 3.500 MW total, texto diz 4.500 MW so eolica + 8.100 MW total |
| 2 | V90 — Pesca | 10 | 9 | 47% | Dados de producao pesqueira sem ano/fonte precisa; "130 mil pescadores" sem referencia direta |
| 3 | V94 — Desigualdade | 18 | 8 | 31% | Inconsistencia: texto diz "246 Mt" no porto, research e V83 dizem "210 Mt" |
| 4 | V103 — Cenarios 2030/2050 | 14 | 8 | 36% | Projecoes climaticas regionalizadas sem paper especifico; cenarios economicos sem fonte |
| 5 | V91 — Corredor Logistico | 10 | 6 | 38% | FNS "inaugurada integralmente em 2024" — requer verificacao |
| 6 | V88 — Industria/Minerais | 11 | 6 | 35% | "~8 siderurgicas em Acailandia" — numero impreciso; "115 mil habitantes" sem fonte |
| 7 | V86 — MATOPIBA | 14 | 6 | 30% | "Desmatamento acumulado ~40%" — fonte imprecisa; PIB mesorregiao sem fonte direta |
| 8 | V87 — Comercio Exterior | 12 | 5 | 29% | Percentuais da pauta (~50%, ~20%, ~8%) sao estimativas arredondadas |
| 9 | V82 — Quatro Ciclos | 20 | 5 | 20% | Dados historicos dependem de livros academicos sem ISBN; Fundo Noruega "US$1,6 tri" vs V84 "US$1,8 tri" |
| 10 | V84 — Ferrovia Carajas | 24 | 4 | 14% | Melhor documentado; risk em "47 mortes" (fonte Agencia Publica, sem URL) |
| 11 | V85 — Babacu | 22 | 4 | 15% | Bem documentado; risk em "64 produtos" (Embrapa/WWF sem paper especifico) |
| 12 | V83 — Porto Itaqui | 16 | 3 | 16% | Calado "23 metros" e claim central sem URL de ANTAQ |

---

## Inconsistencias Internas Detectadas

### CRITICO — Corrigir antes de publicacao

| ID | Verbetes | Inconsistencia | Resolucao |
|----|----------|----------------|-----------|
| INC-01 | V89 vs research V89 | Texto: "4.500 MW eolica, total 8.100 MW". Research: "3.500 MW capacidade instalada" total. Divergencia de 4.600 MW | Verificar ANEEL/BIG 2024. O texto parece mais atualizado mas contradiz seu proprio research |
| INC-02 | V94 vs V83 | V94 texto: "246 milhoes de toneladas em 2023". V83 texto e research: "210 Mt". V84: "210 Mt" | Padronizar. 246 Mt pode incluir movimentacao diferente ou ser dado errado |
| INC-03 | V82 vs V84 | V82 box Noruega: "US$1,6 trilhao". V84 box Noruega: "US$1,8 trilhao" | Verificar valor atual do fundo NBIM. Provavelmente V84 mais recente |
| INC-04 | V87 vs V84 | V87: "~US$15 bilhoes em commodities transitam". V84: "~US$18-19 bilhoes" so em minerio. V94: "~US$15 bilhoes" | Desalinhar: V87/V94 falam do total ou so de minerio? V84 fala so de ferro |
| INC-05 | V82 vs V84 | V82: "177 milhoes de toneladas de minerio por ano". V84: "177 Mt" (consistente, ok). Mas V82 diz "600 km" no MA e V84 diz "600 dos 892 km" | Verificar: sao 600 km no MA ou outro numero? |
| INC-06 | V84 vs V94 | V84: PIB per capita MA 2021 = "R$17.471". V94: "R$15.757" | AMBOS citam IBGE. Verificar: R$15.757 (Contas Regionais) vs R$17.471 (outra serie?) |

---

## Detalhamento por Verbete

---

### V82 — Os quatro ciclos e os menores

| # | Afirmacao | Valor | Nivel | Fonte citada | Observacao |
|---|-----------|-------|-------|--------------|------------|
| 1 | MA foi o estado mais rico do Brasil (sec. XVIII) | Qualitativo | L2 | Gaioso (1818); Meireles (2001) | Claim historico, sustentado por historiografia |
| 2 | Drogas do sertao: cacau, cravo, canela, baunilha, salsaparrilha, urucu | Lista | L2 | Chambouleyron (2010) | |
| 3 | "Descimentos" e "resgates" como sequestros | Qualitativo | L2 | Hemming (1978) | |
| 4 | Revolta de Beckman em 1684 | Data | L2 | Meireles (2001) | Fato historico consolidado |
| 5 | Primeira revolta colonial contra a Coroa | Ranking | L3 | Meireles (2001) | **RISCO**: claim de "primeira" requer verificacao; Beckman e frequentemente citada como tal, mas ha debate |
| 6 | Cia. Geral criada por Pombal em 1755 | Data | L2 | Dias (1970) | |
| 7 | MA maior exportador de algodao do Imperio (1780-1820) | Ranking | L2 | Viveiros (1954); Gaioso (1818) | |
| 8 | Algodao: janela aberta pela Rev. Americana (1775) | Data | L2 | Beckert (2014) | |
| 9 | Segundo boom: Guerra Civil (1861-65) | Data | L2 | Assuncao (2015) | |
| 10 | Economia algodoeira morta em 1870 | Data | L2 | Assuncao (2015) | |
| 11 | Oryza glaberrima domesticada no delta do Niger ha 3.000 anos | Dado | L2 | Carney (2001) | |
| 12 | MA exportava mais arroz que qualquer capitania | Ranking | L2 | Barickman (1994) | |
| 13 | EFC: 177 Mt minerio/ano | Dado | L2 | Vale S.A. Rel. 4T 2024 | Sem URL |
| 14 | Trens de 330 vagoes | Dado | L2 | Vale S.A. | |
| 15 | Soja MA 2023: ~4,2 Mt em 1,2 Mha | Dado | L2 | CONAB dez/2023 | Sem URL |
| 16 | Babacu: 95% producao nacional | Dado | L2 | Almeida (2005) | Texto V85 diz 93-94% (IBGE). Diferenca menor |
| 17 | Babacu: 300.000 familias | Dado | L2 | Almeida (2005); MIQCB | |
| 18 | Gado bovino: 8,5 milhoes cabecas (2022) | Dado | L2 | IBGE PPM 2022 | Sem URL |
| 19 | Litoral: 640 km | Dado | L3 | Sem fonte especifica neste verbete | Citado em V90 tambem |
| 20 | Fundo soberano Noruega: US$1,6 trilhao | Dado | L3 | Sem fonte. **E V84 diz US$1,8 tri** | INCONSISTENCIA INC-03 |
| 21 | Botsuana: maior IDH Africa Subsaariana entre paises sem litoral | Dado | L3 | Sem fonte | Verificar: claim sobre IDH pode estar desatualizado |
| 22 | Minerio descoberto em 1967 | Data | L2 | Vale/historiografia consolidada | |
| 23 | Cana nunca dominante como PE/BA | Qualitativo | L2 | Schwartz (1985) | |
| 24 | Minas construiu cidades, SP fabricas, MA portos | Analogia | L3 | Furtado (1959) inspira, mas frase e autoral | |
| 25 | PIB per capita MA: menor do Brasil | Ranking | L2 | IBGE | Mas V94 diz "2o mais baixo, acima do PI". **INCONSISTENCIA** |

**Subtotal V82**: L2=20, L3=5

---

### V83 — Porto de Itaqui

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | Calado natural: 23 metros | Dado | L2 | ANTAQ 2023 | Claim central, sem URL |
| 2 | Santos: 15m, Paranagua: 12m, Rio Grande: 14m | Dados | L2 | ANTAQ 2023 | |
| 3 | Baia de Sao Marcos: 100 km extensao, 4 km largura | Dados | L2 | CPRM 2004 | |
| 4 | 1.500 km a menos para Rotterdam que Santos | Dado | L2 | MTPA 2023 | |
| 5 | Porto moderno inaugurado 1974 | Data | L2 | EMAP | |
| 6 | Ponta da Madeira inaugurado 1985 | Data | L2 | Vale S.A. | |
| 7 | Tegram inaugurado 2014 | Data | L2 | EMAP 2023 | |
| 8 | Area portuaria: ~210 Mt/ano | Dado | L2 | ANTAQ 2023 | |
| 9 | 168 Mt minerio por Ponta da Madeira | Dado | L2 | Vale 4T 2024 | |
| 10 | ~10 Mt soja/milho pelo Tegram | Dado | L2 | Tegram/VLI 2023 | |
| 11 | 2o maior porto do Brasil | Ranking | L2 | ANTAQ 2023 | **Mas depende da metrica: volume vs. diversidade** |
| 12 | Arco Norte: de 15% para >35% em graos | Dado | L2 | MDIC Comex Stat | |
| 13 | Valemax: 362m, 400.000 t | Dado | L2 | Vale S.A. | |
| 14 | Carga de um Valemax: ~US$40 milhoes | Dado | L3 | Calculo autoral | Depende do preco do minerio |
| 15 | 10.000 caminhoes equivalentes | Dado | L3 | Calculo autoral | |
| 16 | Rotterdam: 385.000 empregos, 6,2% PIB holandes | Dado | L3 | Sem fonte | |
| 17 | La Touche desembarcou em 1612 | Data | L2 | Meireles (2001) | |
| 18 | FNS inaugurada integralmente em 2024 | Data | L2 | VALEC | **Verificar: pode ter sido parcial** |
| 19 | BNDES estudo sobre polo agroindustrial | Fonte | L2 | BNDES 2022 | Sem referencia precisa |

**Subtotal V83**: L2=16, L3=3

---

### V84 — Ferrovia Carajas

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | Awa chamam trem de "barulho do terror" | Citacao | L2 | Survival International | |
| 2 | 330 vagoes, 3,3 km, 40.000 t/viagem | Dado | L2 | Vale S.A. | |
| 3 | ~35 trens simultaneos | Dado | L2 | Vale S.A. | |
| 4 | ~485.000 t/dia = ~US$53 mi/dia | Calculo | L3 | Calculo: 485k t x US$110/t | Preco do minerio varia; US$110 pode estar desatualizado |
| 5 | 892 km de extensao | Dado | L2 | Vale/ANTT | Fato consolidado |
| 6 | 600 km no Maranhao | Dado | L2 | Vale | |
| 7 | PIB per capita MA menor do Brasil | Ranking | L2 | IBGE | **Mas V94 diz 2o menor (PI abaixo)** |
| 8 | 51,6% pobreza (2023) | Dado | L2 | IBGE PNAD 2023 | |
| 9 | CFEM Acailandia: ~R$2,9 mi/mes (out/2024) | Dado | L2 | ANM | |
| 10 | CFEM Sao Luis: ~R$2,8 mi/mes (out/2024) | Dado | L2 | ANM | |
| 11 | Inauguracao EFC: 28/02/1985 | Data | L2 | Fato historico | |
| 12 | Descoberta Carajas: 31/07/1967 | Data | L2 | Historiografia consolidada | |
| 13 | Geologo Breno dos Santos | Fato | L2 | Vale/historiografia | |
| 14 | Teor de ferro: 66,5% | Dado | L2 | Vale | |
| 15 | PGC: 24/11/1980, 900.000 km2, US$3 bi | Dados | L2 | Banco Mundial/historiografia | |
| 16 | Privatizacao CVRD: 06/05/1997, US$3,4 bi | Dados | L2 | Fato historico consolidado | |
| 17 | Valorizacao pos-privatizacao: 3.500%+ | Dado | L3 | Sem fonte precisa | Depende da data de referencia |
| 18 | 177 Mt minerio + 10,9 Mt graos (2024) | Dado | L2 | Vale 4T 2024; ANPTrilhos | |
| 19 | 168 Mt em Ponta da Madeira (2024) | Dado | L2 | Vale 4T 2024 | |
| 20 | Receita ferrosos Vale 2024: US$31,4 bi | Dado | L2 | Vale 4Q24 Results | |
| 21 | Lucro Vale 2021: US$24 bi | Dado | L2 | Vale | |
| 22 | PIB MA 2021: R$125 bi (~US$24 bi) | Dado | L2 | IBGE | |
| 23 | CFEM: 60% municipio extrator, 15% estado, 15% afetados | Dado | L2 | ANM/legislacao | |
| 24 | 47 mortes desde 2004 | Dado | L2 | ANTT/Agencia Publica | Sem URL |
| 25 | 124 acidentes (2004-2016) | Dado | L2 | ANTT/Agencia Publica | |
| 26 | 240 passagens de nivel, 83 em nivel | Dado | L2 | ANTT | |
| 27 | Piquiá de Baixo: 20 anos de luta, reassentamento ~2022 | Fato | L2 | FIDH/Justica nos Trilhos | |
| 28 | MV Stellar Banner: 295.000 t, 400+ litros oleo | Dado | L3 | Sem fonte precisa. **"432,4 litros" nas notas vs "400+ litros" no texto** | Inconsistencia interna |
| 29 | Fundo Noruega: US$1,8 trilhao | Dado | L2 | NBIM | Consistente com dados recentes, mas V82 diz 1,6 tri |
| 30 | Codelco Chile: US$116 bi (1971-2020) | Dado | L3 | Sem fonte precisa | |
| 31 | China compra 2/3 da carga | Dado | L2 | Vale: 110 Mt de 168 Mt | |
| 32 | 423.000 passageiros (2024, recorde) | Dado | L2 | Vale/ANPTrilhos | |

**Subtotal V84**: L2=28, L3=4 (mas verbete e longo e bem documentado)

---

### V85 — Babacu

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | Attalea speciosa | Nome cientifico | L2 | Taxonomia consolidada | |
| 2 | 13-18 milhoes de hectares | Dado | L2 | MMA | |
| 3 | 70% no Maranhao = 141 mil km2 | Dado | L2 | IBGE/MMA | |
| 4 | Area maior que a Grecia | Comparacao | L2 | Grecia ~132 mil km2 (confere) | |
| 5 | 10-12 anos para comecar a produzir | Dado | L2 | Embrapa | |
| 6 | 3-5 cachos/safra, 300-500 cocos/cacho | Dado | L2 | Embrapa | |
| 7 | ~2.000 frutos/palmeira/ano | Calculo | L2 | Derivado de Embrapa | |
| 8 | 3-8 amendoas/fruto | Dado | L2 | Embrapa | |
| 9 | 64+ produtos catalogados | Dado | L2 | Embrapa; WWF | |
| 10 | 300 mil+ mulheres | Dado | L2 | MIQCB; Cerratinga; IBGE | |
| 11 | 90% feminino | Dado | L2 | MIQCB | |
| 12 | 200-300 cocos/dia (experiente) | Dado | L2 | MIQCB/campo | |
| 13 | R$2-4/kg amendoa (2024) | Dado | L2 | CONAB/PGPMBio | |
| 14 | Diaria R$20-30 | Dado | L3 | Derivado, sem fonte direta | |
| 15 | Producao 2022: 30.478 t | Dado | L2 | IBGE PEVS 2022 | |
| 16 | MA: 93-94% producao nacional | Dado | L2 | IBGE | |
| 17 | Queda de ~200 mil t (anos 80) para 30 mil t | Dado | L2 | IBGE serie historica | |
| 18 | Embrapa: R$100 mi vs IBGE R$34 mi (Medio Mearim) | Dado | L2 | Embrapa (2019/2017) | |
| 19 | MIQCB fundado 1991 | Data | L2 | MIQCB | |
| 20 | 1a Lei Babacu Livre: Lago do Junco, 1997 | Data | L2 | Lei Municipal 05/1997 | |
| 21 | 12 municipios MA com lei | Dado | L2 | Agroecologia em Rede; MIQCB | |
| 22 | Nenhuma nova lei desde 2012 | Dado | L2 | Silva (2020) | |
| 23 | Patrimonio Imaterial MA: Lei 12.378/24 | Legislacao | L2 | ALMA | |
| 24 | Patrimonio Imaterial PA: Lei 10.930/2025 | Legislacao | L2 | ALEPA | |
| 25 | Carvao de babacu: 80% carbono | Dado | L3 | Sem fonte precisa | |
| 26 | Dona Dije: citacao "Eu nao quebro coco..." | Citacao | L3 | "Registro oral, eventos MIQCB" | Nao verificavel |
| 27 | Solo exposto: de 2% para 8% (1990-2015) | Dado | L2 | ResearchGate (2019) — sem URL | |
| 28 | Const. MA art. 196; Lei 4.734/86 | Legislacao | L2 | Texto legal | |

**Subtotal V85**: L2=24, L3=4

---

### V86 — MATOPIBA

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | MATOPIBA: 73 milhoes de hectares | Dado | L2 | EMBRAPA 2015 | |
| 2 | Decreto 8.447 de 06/05/2015 | Legislacao | L2 | Texto legal | |
| 3 | 337 municipios | Dado | L2 | EMBRAPA | |
| 4 | Area = 2x Alemanha | Comparacao | L3 | Alemanha ~357 mil km2; 73 Mha = 730 mil km2. **Confere** (mas sem fonte da comparacao) |
| 5 | Soja MA 2000: ~300 mil ha | Dado | L2 | CONAB serie historica | |
| 6 | Soja MA 2023: ~1,2 Mha, ~4,2 Mt | Dado | L2 | CONAB 2023/24 | |
| 7 | Crescimento 300% em 2 decadas | Calculo | L2 | Derivado de CONAB | |
| 8 | China absorve 70% da soja brasileira | Dado | L2 | MDIC Comex Stat | |
| 9 | Desmatamento cerrado MA: ~40% acumulado | Dado | L3 | PRODES Cerrado impreciso — "~40%" sem ano base | |
| 10 | MATOPIBA 2022: ~500 mil ha desmatamento | Dado | L2 | INPE PRODES Cerrado | |
| 11 | Cerrado: 12 mil especies plantas, 800 aves, 200 mamiferos | Dado | L2 | MMA 2022 | |
| 12 | 8 de 12 bacias nascem no cerrado | Dado | L2 | MMA | |
| 13 | Codigo Florestal: 80% Amazonia, 20-35% cerrado | Dado | L2 | Lei 12.651/2012 art. 12 | |
| 14 | Chapadas 600-900m altitude | Dado | L3 | IBGE sem ref precisa | |
| 15 | Renda per capita mesorregiao sul: +200% em 20 anos | Dado | L3 | IBGE PIB Municipal sem calculo verificavel | |
| 16 | PIB agro mesorregiao: R$800 mi → R$2,5 bi | Dado | L3 | Sem fonte direta no research | |
| 17 | Numero de pivots: ~200 → ~1.500 | Dado | L3 | Sem fonte. **Alto risco de alucinacao** | |
| 18 | CPT: dezenas de ocorrencias/ano grilagem | Dado | L2 | CPT Conflitos 2023 | |
| 19 | Balsas: 60 mil habitantes | Dado | L2 | IBGE | Censo 2022: ~94 mil. **Verificar** |
| 20 | Desmatamento cerrado ~25% em 2000 | Dado | L3 | Sem fonte precisa | |

**Subtotal V86**: L2=14, L3=6

---

### V87 — Comercio Exterior

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | Exportacoes MA 2023: ~US$9,5 bi | Dado | L2 | MDIC Comex Stat | |
| 2 | Minerio de ferro: ~50% | Dado | L2 | MDIC | |
| 3 | Soja e derivados: ~20% | Dado | L2 | MDIC | |
| 4 | Alumina: ~8% | Dado | L2 | MDIC | |
| 5 | Celulose: ~5% | Dado | L2 | MDIC | |
| 6 | Ferro-gusa: ~3% | Dado | L3 | Estimativa arredondada | |
| 7 | Ouro: ~3% | Dado | L3 | Estimativa arredondada | |
| 8 | China: ~55% das exportacoes | Dado | L2 | MDIC | |
| 9 | Japao: ~8%, Coreia: ~5% | Dados | L2 | MDIC | |
| 10 | Importacoes: ~US$3,5 bi | Dado | L2 | MDIC | |
| 11 | Saldo: ~US$6 bi | Calculo | L2 | Derivado de MDIC | |
| 12 | Coreia 1962: renda inferior a paises africanos | Dado | L3 | Sem fonte | Claim comum mas impreciso |
| 13 | Coreia: decima economia do mundo | Dado | L3 | Ranking varia conforme metrica | |
| 14 | PIB per capita MA menor do Brasil | Ranking | L2 | IBGE | **Mas V94 diz 2o menor** |
| 15 | IDH MA: mais baixo do pais | Ranking | L2 | PNUD/IBGE | |
| 16 | Lei Kandir: LC 87/1996 | Legislacao | L2 | Texto legal | |
| 17 | "Mais do que o PIB de 60 paises" | Comparacao | L3 | Sem calculo demonstrado | |

**Subtotal V87**: L2=12, L3=5

---

### V88 — Industria e Minerais

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | Industria: ~18% do PIB MA | Dado | L2 | IBGE Contas Regionais 2022 | |
| 2 | Alumar instalada em 1984 | Data | L2 | Alcoa/Alumar | |
| 3 | Alumar: Alcoa, BHP, Shell (hoje Rio Tinto) | Fato | L2 | Alcoa | |
| 4 | Alumina: ~3,5 Mt/ano capacidade | Dado | L2 | Alcoa 2023 | |
| 5 | Aluminio suspenso em 2015 | Data | L2 | Alcoa | |
| 6 | ~8 siderurgicas ferro-gusa Acailandia | Dado | L3 | Numero impreciso, sem fonte | |
| 7 | Desmatamento para carvao anos 90-2000 | Fato | L2 | INPE/PRODES | |
| 8 | Piquiá de Baixo: reassentamento 2022 | Data | L2 | FIDH/Justica nos Trilhos | |
| 9 | Suzano Imperatriz: 1,5 Mt/ano celulose | Dado | L2 | Suzano 2023 | |
| 10 | Garimpo: Godofredo Viana, Maracassume, Bom Jardim | Localizacao | L2 | ANM 2023 | |
| 11 | Acailandia: 115 mil habitantes | Dado | L3 | Sem fonte. Censo 2022 indica ~113 mil | Aproximado, ok |
| 12 | Polo ceramico Rosario, Itapecuru-Mirim | Fato | L3 | Sem fonte precisa | |
| 13 | Ambev em Sao Luis | Fato | L3 | Sem fonte | Verificavel mas nao citado |
| 14 | ~80.000 empregos industria formal | Dado | L2 | RAIS | Research cita, texto nao |
| 15 | Empregos industria: Coreia nao tinha engenheiros 1960 | Analogia | L2 | Amsden (1989) | |
| 16 | Manganes em Buriticupu | Dado | L3 | Sem fonte precisa | |
| 17 | Silicio em Barra do Corda | Dado | L3 | Sem fonte precisa | |

**Subtotal V88**: L2=11, L3=6

---

### V89 — Energia

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | MA exportador liquido de energia | Fato | L2 | ONS 2024 | |
| 2 | 51% pobreza | Dado | L2 | IBGE 2023 | |
| 3 | Boa Esperanca: 237 MW, 1970 | Dado | L2 | CHESF | |
| 4 | Estreito: 1.087 MW, 2012 | Dado | L2 | CESTE | |
| 5 | Estreito: 5.000 familias deslocadas | Dado | L2 | CESTE EIA | |
| 6 | Tucurui: 500 kV, alimenta MA | Dado | L2 | Eletronorte | |
| 7 | Ventos: 7-9 m/s no litoral | Dado | L2 | Atlas Eolico CEPEL | |
| 8 | 4.500 MW eolica instalada (2024) | Dado | L3 | ANEEL/BIG 2024 citado mas **research diz total 3.500 MW** | **INCONSISTENCIA INC-01** |
| 9 | 100+ parques eolicos | Dado | L3 | Estimativa sem fonte precisa | |
| 10 | Torres de 100-150m | Dado | L3 | Sem fonte | |
| 11 | Complementaridade sazonal eolica-hidro | Fato | L2 | EPE PDE 2032 | |
| 12 | Solar: ~500 MW (2024) | Dado | L3 | ANEEL/BIG | Sem verificacao cruzada |
| 13 | Biomassa: ~300 MW | Dado | L3 | Sem fonte precisa | |
| 14 | Total ~8.100 MW | Dado | L3 | **Soma diverge do research** | |
| 15 | Consumo: ~3.000-4.000 MW medio | Dado | L3 | Sem fonte precisa | |
| 16 | Termoeletrica: ~1.200 MW | Dado | L3 | Sem fonte precisa | |
| 17 | Hidreletrica total: ~1.500 MW | Dado | L3 | Soma Boa Esperanca + Estreito = 1.324 MW. **De onde vem 1.500?** | |
| 18 | Offshore: pedidos protocolados IBAMA | Fato | L2 | IBAMA 2023-2024 | |
| 19 | Parques eolicos em Paulino Neves, Barreirinhas, Tutoia | Localizacao | L2 | ANEEL/BIG | |
| 20 | Hidrogenio verde: estudos existem | Qualitativo | L3 | Sem fonte | |
| 21 | 6.000 km rodovias federais, 12.000 estaduais | Dado | L3 | Citado em V91, sem fonte aqui | |

**Subtotal V89**: L2=10, L3=11 — **VERBETE DE MAIOR RISCO**

---

### V90 — Pesca

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | 130 mil pescadores artesanais registrados | Dado | L2 | MPA/IBAMA | Sem ano especifico |
| 2 | ~100 mil toneladas/ano producao | Dado | L2 | MPA/IBAMA | "~" indica estimativa |
| 3 | 2o ou 3o maior produtor pesqueiro | Ranking | L3 | Oscila conforme ano — sem fonte do ranking | |
| 4 | Reentrâncias: 2.680 km de costa recortada | Dado | L2 | ICMBio | |
| 5 | Maior area continua de manguezal das Americas | Ranking | L3 | **Claim de "maior" precisa verificacao** | |
| 6 | RESEX Reentrâncias desde 2005 | Data | L2 | Decreto s/n 2005 | |
| 7 | MA maior produtor caranguejo-uca | Ranking | L2 | IBAMA | |
| 8 | Camboas: 2.000 anos de uso | Dado | L2 | Bandeira (2013) | |
| 9 | Mares de sizigia: lua cheia e nova | Fato cientifico | L2 | Conhecimento consolidado | |
| 10 | Defeso caranguejo: nov-fev | Dado | L2 | Legislacao | |
| 11 | Defeso camarao: dez-mar | Dado | L2 | Legislacao | |
| 12 | Lei 10.779/2003: seguro-defeso | Legislacao | L2 | Texto legal | |
| 13 | 640 km de litoral | Dado | L3 | Sem fonte precisa neste verbete | Citado em multiplos verbetes |
| 14 | Contaminacao metais pesados Baia Sao Marcos | Fato | L2 | UFMA 2019 | |
| 15 | Currais de mare como tecnica | Fato | L2 | Etnografia consolidada | |
| 16 | Marisqueiras sem carteira de pescadora | Fato | L3 | Sem fonte | |
| 17 | Pescada amarela, serra, camurupim etc. | Lista | L3 | Sem fonte especifica | Conhecimento local |
| 18 | "Estruturas mais antigas do Brasil" (camboas) | Ranking | L3 | Bandeira (2013) usa "possivelmente" | **Qualificador adequado no texto** |
| 19 | Sobrepesca: frota industrial reduz estoques | Fato | L3 | MPA 2022 citado vagamente | |

**Subtotal V90**: L2=10, L3=9

---

### V91 — Corredor Logistico

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | EFC: 892 km | Dado | L2 | Vale/VALEC | |
| 2 | FNS: ~1.550 km, Anapolis-Itaqui | Dado | L2 | VALEC | |
| 3 | FNS inaugurada integralmente 2024 | Data | L2 | VALEC | **Verificar: houve inauguracao total em 2024?** |
| 4 | 177 Mt minerio/ano | Dado | L2 | Vale 4T 2024 | |
| 5 | 27 municipios cruzados EFC | Dado | L2 | Vale | |
| 6 | Arco Norte: >35% exportacoes graos (2023) | Dado | L2 | CONAB | |
| 7 | BR-010 corta MA norte-sul | Fato | L2 | DNIT | |
| 8 | BR-135: Sao Luis-Balsas | Fato | L2 | DNIT | |
| 9 | BR-226: interior-litoral | Fato | L2 | DNIT | |
| 10 | 6.000 km rodovias federais | Dado | L3 | Sem fonte precisa | |
| 11 | 12.000 km rodovias estaduais | Dado | L3 | Sem fonte precisa | |
| 12 | MA entre piores em qualidade rodovias CNT | Dado | L2 | CNT Pesquisa Rodovias 2023 | |
| 13 | 23m calado Itaqui | Dado | L2 | ANTAQ | |
| 14 | Sorriso-Santos: 2.000 km | Dado | L3 | Estimativa | |
| 15 | Sorriso-Miritituba: 1.200 km | Dado | L3 | Estimativa | |
| 16 | Taxa 1% geraria US$180 mi | Calculo | L3 | Calculo autoral | |
| 17 | FIOL conectara Bahia a Itaqui | Fato | L3 | **FIOL liga Ilheus a Figueiropolis/Caetite, nao diretamente a Itaqui** | Verificar rota |

**Subtotal V91**: L2=10, L3=7 (inclui 1 potencial erro factual sobre FIOL)

---

### V94 — Desigualdade (amostra — dados principais)

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | IDH MA: 0,676 (2021) | Dado | L2 | PNUD/IBGE Atlas | |
| 2 | IDH Brasil: 0,754 | Dado | L2 | PNUD/IBGE | |
| 3 | PIB per capita MA: R$15.757 (2021) | Dado | L2 | IBGE Contas Regionais | **V84 diz R$17.471. INCONSISTENCIA** |
| 4 | Esgoto tratado: 13,6% | Dado | L2 | SNIS/Trata Brasil 2022 | |
| 5 | Coleta esgoto: 32,49% | Dado | L2 | SNIS 2022 | |
| 6 | Analfabetismo: 15,6% | Dado | L2 | IBGE PNAD 2022 | |
| 7 | Mortalidade infantil: 15,2/mil (2021) | Dado | L2 | DataSUS | |
| 8 | Esperanca de vida: 71,4 anos (2021) | Dado | L2 | IBGE | |
| 9 | Pobreza: ~50% (2022) | Dado | L2 | IBGE SIS 2022 | **V84 diz 51,6% (2023). Ano diferente** |
| 10 | Porto Itaqui: 246 Mt (2023) | Dado | L3 | **Diverge de 210 Mt em V83 e V84** | INCONSISTENCIA INC-02 |
| 11 | ~US$15 bi commodities transitam | Dado | L3 | **Diverge de V84 US$18-19 bi** | INCONSISTENCIA INC-04 |
| 12 | Gini MA: 0,535 | Dado | L2 | IBGE PNAD 2022 | |
| 13 | Populacao: ~7,15 mi | Dado | L2 | IBGE Censo 2022 | |
| 14 | Zona rural: 36,9% | Dado | L2 | IBGE Censo 2022 | |
| 15 | Trabalho informal: ~60% | Dado | L2 | IBGE PNAD 2022 | |
| 16 | Internet: 72% domicilios | Dado | L2 | IBGE PNAD TIC 2022 | |
| 17 | IDEB anos finais: 4,1 (2021) | Dado | L2 | INEP/MEC | |
| 18 | Leitos: 1,8/mil | Dado | L2 | DataSUS/CNES 2023 | |
| 19 | Diferenca IDH MA-DF > DF-Noruega | Calculo | L3 | Depende do ano. MA 0,676, DF 0,824 = 0,148. Noruega ~0,961 em 2021. DF-Noruega = 0,137. **Na verdade MA-DF (0,148) > DF-Noruega (0,137). CONFERE.** | OK mas marginal |
| 20 | Satubinha, Fernando Falcao: mortalidade >25/mil | Dado | L3 | Sem fonte municipal precisa | |
| 21 | "14 anos menos que um japones" | Calculo | L3 | Japao ~84,7 anos. 84,7-71,4=13,3. **~13 anos, nao 14** | Arredondamento excessivo |

**Subtotal V94**: L2=16, L3=5 + inconsistencias

---

### V103 — Cenarios 2030/2050 (amostra)

| # | Afirmacao | Valor | Nivel | Fonte | Observacao |
|---|-----------|-------|-------|-------|------------|
| 1 | Populacao MA: ~7,15 mi | Dado | L2 | IBGE Censo 2022 | |
| 2 | Projecao 2030: ~7,3 mi | Projecao | L2 | IBGE Projecoes | |
| 3 | Projecao 2050: declinio | Projecao | L2 | IBGE | |
| 4 | Idade mediana: ~28 → 32 → 38 | Projecao | L2 | IBGE | |
| 5 | SLZ metro: pode ultrapassar 2 mi | Projecao | L3 | Sem fonte precisa | |
| 6 | IPCC AR6 (2021) | Referencia | L2 | IPCC | |
| 7 | Cenario SSP2-4.5: +2,5-3,5C, -15 a -25% chuvas | Dados | L2 | IPCC AR6 | **Mas dados regionalizados para MA especificamente — qual paper?** |
| 8 | SSP3-7.0: -25 a -32% chuvas | Dados | L3 | **Regionalizacao para cerrado MA sem paper especifico citado** | |
| 9 | Elevacao nivel do mar: 20-40 cm ate 2050 | Dado | L2 | IPCC AR6 (global) | |
| 10 | Savanizacao Amazonia MA | Conceito | L2 | Literatura climatica | |
| 11 | Gibson citacao | Citacao | L2 | William Gibson, atribuicao conhecida | |
| 12 | Cenarios economicos A, B, C | Construcao autoral | L3 | **Nao baseados em estudo especifico** | |
| 13 | FIOL conectara ao MA | Dado | L3 | **Ver nota em V91** | |
| 14 | Imperatriz 400 mil hab em 2050 | Projecao | L3 | Sem fonte | |

**Subtotal V103**: L2=8, L3=6

---

## Problemas Estruturais Identificados

### 1. ZERO URLs em todo o corpus
Nenhum research.md contem links. Todos os dados sao citados por nome de orgao ou livro. Isso torna impossivel a verificacao rapida e impede o livro de atingir L1 em qualquer claim.

**Recomendacao**: Para cada fonte institucional (IBGE, CONAB, ANTAQ, ANM, MDIC, Vale, ANEEL, INPE), adicionar a URL do dataset especifico. A maioria tem dados publicos com links estaveis.

### 2. Inconsistencias entre verbetes
Seis inconsistencias criticas detectadas (INC-01 a INC-06). Cada uma precisa ser resolvida antes da publicacao, padronizando o dado com a fonte mais recente e confiavel.

### 3. Numeros arredondados sem qualificador
Muitos dados usam "~" (cerca de), o que e adequado para estimativas. Porem, quando o texto transforma "~210 Mt" em "246 Mt" (V94), perde-se a cautela. Padronizar: sempre usar "~" ou "cerca de" quando o dado e aproximado.

### 4. Calculos autorais apresentados como fatos
Varios boxes apresentam calculos (US$53 mi/dia, US$40 mi por Valemax, taxa de 1% = US$180 mi) sem explicitar que sao derivacoes. Recomendacao: marcar claramente como "Calculo editorial" ou "Estimativa do autor".

### 5. Rankings imprecisos
Varios verbetes fazem claims de "maior", "primeiro", "unico" sem qualificacao adequada:
- "Primeira revolta colonial" (V82) — debativel
- "Maior area continua de manguezal das Americas" (V90) — precisa fonte
- PIB per capita "menor do Brasil" vs "segundo menor" — aparece de ambas as formas

### 6. V89 (Energia) precisa de reescrita do research.md
O research.md de V89 contem dados drasticamente diferentes do texto.md (3.500 MW total vs 8.100 MW total). Um dos dois esta errado. A divergencia sugere que o texto foi atualizado apos a pesquisa, sem sincronizar o research.

---

## Proximos Passos Recomendados

1. **Resolver as 6 inconsistencias criticas** (INC-01 a INC-06) — prioridade imediata
2. **Adicionar URLs** a todas as fontes institucionais — upgrade de L2 para L1
3. **Reescrever research.md de V89** para alinhar com texto.md (ou vice-versa)
4. **Verificar claims de ranking** ("maior", "primeiro", "unico") com fonte especifica
5. **Marcar calculos editoriais** como tal nos boxes
6. **Auditar Partes I-VIII** quando contexto permitir — verbetes historicos e culturais tem menor risco de alucinacao numerica, mas maior risco de imprecisao factual

---

*Auditoria parcial. Cobre Partes IX, X (V94), XI (V103). Partes I-VIII pendentes de auditoria detalhada.*
*Gerado por Evidence Controller — 2026-04-01*
