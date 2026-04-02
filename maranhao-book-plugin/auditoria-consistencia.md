# Auditoria de Consistencia Factual — "Quem e o Maranhao?"

**Data**: 2026-04-01
**Escopo**: 20 fatos mais citados, cruzados entre verbetes
**Metodo**: leitura dos texto.md relevantes + busca por padroes em todos os 105 verbetes
**Tipo**: READ-ONLY (nenhum arquivo foi modificado)

---

## Legenda

- **CONSISTENTE** — mesmo valor em todos os verbetes verificados
- **INCONSISTENTE** — valores divergentes (detalhado abaixo)
- **AUSENTE** — dado esperado nao mencionado no verbete indicado

---

## 1. Area do MA: 329.651 km2

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V01 | 329.651 km2 (epígrafe + texto + notas) | OK |
| V02 | Nao menciona a area total | AUSENTE |
| V61 | Nao menciona a area total | AUSENTE |
| V100 | **331.983 km2** | **INCONSISTENTE** |
| V101 | **331.983 km2** (3x no texto) | **INCONSISTENTE** |

**Diagnostico**: INCONSISTENTE. V01 usa 329.651 km2 (IBGE Areas Territoriais 2024). V100 e V101 usam 331.983 km2 (sem fonte explicita). A diferenca de ~2.332 km2 e significativa. Possivelmente V100/V101 usam um dado IBGE mais antigo ou de outra serie. **Necessario padronizar para um unico valor com fonte IBGE especifica.**

---

## 2. Biomas: Cerrado ~65%, Amazonia ~34%, Caatinga ~1%

| Verbete | Cerrado | Amazonia | Caatinga | Status |
|---------|---------|----------|----------|--------|
| V01 | ~65% | ~34% | ~1% | OK |
| V02 | ~65% (138 municipios) | 76% destruida | nao menciona | OK |
| V03 | ~65% (~214 mil km2) | — | — | OK |
| V04 | — | 34% (bioma); 76% destruida | — | OK |
| V07 | — | — | ~1% (~3.300 km2) | OK |

**Diagnostico**: CONSISTENTE. Os percentuais de biomas sao uniformes em todos os verbetes que os mencionam.

---

## 3. Mangues: ~36% do Brasil, ~500.000 ha

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V02 | "quase 500.000 hectares, 36% de todos os mangues brasileiros" | OK |
| V05 | "36% de todos os manguezais brasileiros"; "entre 480 mil e 500 mil hectares" | OK |

**Diagnostico**: CONSISTENTE. Ambos os verbetes usam os mesmos valores.

---

## 4. Amazonia destruida: 76%

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V01 | 76% | OK |
| V02 | 76% | OK |
| V04 | 76% (texto + notas: "74-78%, 76% consolidado MapBiomas") | OK |
| V14 | 76% | OK |
| V16 | Menciona "mais desmatou proporcionalmente" sem % exato | AUSENTE (nao e erro) |
| V21 | 76% | OK |

**Diagnostico**: CONSISTENTE. Todos os verbetes que citam o percentual usam 76%.

---

## 5. Quilombos certificados: 1.152

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V35 | **1.152** comunidades certificadas (Palmares 2024). "O MA lidera" | OK |
| V37 | **868** comunidades certificadas (Palmares). "Segundo maior, atras da Bahia" | **INCONSISTENTE** |
| V39 | **653** comunidades reconhecidas pela Palmares | **INCONSISTENTE** |

**Diagnostico**: INCONSISTENTE GRAVE. Tres valores diferentes para o mesmo dado:
- V35: 1.152 (MA lidera o ranking)
- V37: 868 (MA e segundo, atras da BA)
- V39: 653 (sem ranking)

Alem dos numeros divergirem, a **posicao no ranking** tambem diverge (1o vs. 2o). Isto precisa de correcao urgente com dado unico da Palmares.

---

## 6. Populacao indigena: 57.214 (Censo 2022)

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V14 | 57.214 (Censo 2022) | OK |
| V21 | 57.214 (repetido 5x no texto) | OK |

**Diagnostico**: CONSISTENTE. V16 nao cita o numero exato do censo estadual (usa "entre 27 mil e 30 mil" para os Guajajara especificamente), o que e correto para o escopo daquele verbete.

---

## 7. Escravizados no Itapecuru: 85%

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V33 | "Ate 85% da populacao era escravizada" | OK |
| V34 | "ate oitenta por cento de sua populacao composta por pessoas 'de cor'" | **INCONSISTENTE** |
| V36 | "85% de escravizados no Vale do Itapecuru" (3x) | OK |
| V40 | Nao menciona o percentual especifico | AUSENTE |

**Diagnostico**: INCONSISTENTE. V34 diz "80%" enquanto V33 e V36 dizem "85%". Alem disso, V34 usa "pessoas de cor — escravizados e libertos" (inclui libertos), enquanto V33/V36 falam apenas em "escravizados". A diferenca pode ser conceitual (escravizados vs. populacao negra total), mas precisa de padronizacao.

---

## 8. Ferrovia Carajas: receita Vale > PIB MA

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V84 | "Lucro recorde 2021 (US$24 bi) superou o PIB inteiro do MA naquele mesmo ano" | OK |
| V40 | Mencao em nota: "Receita Vale > PIB do MA" (dado YAML ECO-001) | OK |
| V82 | Nao encontrada mencao direta | AUSENTE |
| V94 | Nao encontrada mencao direta | AUSENTE |

**Diagnostico**: CONSISTENTE nos verbetes que mencionam (V84, V40). V82 e V94 nao citam este dado especifico, mas nao e erro — e ausencia em verbetes cujo foco e outro.

---

## 9. Algodao: 651 arrobas (1760) -> 30.000 (1800)

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V40 | "651 arrobas (1760) [...] 30 mil (1800)" — dado repetido em texto + notas | OK |
| V82 | Nao encontrada mencao a esses numeros especificos | AUSENTE |

**Diagnostico**: CONSISTENTE no verbete principal (V40). V82 nao repete o dado, o que e aceitavel.

---

## 10. IDH: 0,676

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V94 | 0,676 (repetido 5x; comparativos com DF, CE, Brasil) | OK |
| V92 | ~0,676 (em tabela historica, linha 2020) | OK |
| V60 | 0,676 (em nota de rodape) | OK |
| V100 | Nao menciona o valor exato | AUSENTE |
| V101 | Nao menciona o valor exato | AUSENTE |

**Diagnostico**: CONSISTENTE nos verbetes que citam. V100 e V101 poderiam mencionar para reforco, mas a ausencia nao e erro.

---

## 11. Esgoto tratado: 3,92%

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V94 | 3,92% (repetido 3x; fonte: SNIS) | OK |
| V98 | 3,92% (repetido 3x) | OK |
| V96 | 3,92% (repetido 3x) | OK |

**Diagnostico**: CONSISTENTE. Mesmo valor em todos os tres verbetes que citam o dado.

---

## 12. Populacao: 6.776.699 (Censo 2022)

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V01 | Nao menciona a populacao total | AUSENTE |
| V94 | Nao menciona a populacao total especifica | AUSENTE |
| V100 | "~7,1 milhoes de habitantes" | **INCONSISTENTE** |
| V101 | "7 milhoes de habitantes" | **INCONSISTENTE** |
| V103 | "~7,15 milhoes" | **INCONSISTENTE** |
| V84 | "Metade da populacao vive abaixo da linha de pobreza" (sem numero total) | AUSENTE |

**Diagnostico**: INCONSISTENTE. O valor de referencia (6.776.699, Censo 2022) nao aparece em nenhum verbete. V100/V101/V103 usam arredondamentos variados (~7,1M / 7M / ~7,15M) que estao **acima** do Censo 2022 (possivelmente usando estimativas IBGE mais recentes ou projecoes). O Censo 2022 contou 6.776.699 — nenhum verbete cita este numero exato. **Necessario decidir se o livro usa o Censo 2022 ou estimativas populacionais mais recentes, e padronizar.**

---

## 13. Latitude Sao Luis: 2 graus 31' S

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V01 | "2 graus 31' de latitude sul" | OK |

**Diagnostico**: CONSISTENTE. Mencionado apenas em V01, que e o verbete correto para este dado.

---

## 14. Babacu: 60+ produtos, 300.000 quebradeiras

| Verbete | Produtos | Quebradeiras | Status |
|---------|----------|-------------|--------|
| V06 | "mais de 60 produtos"; "300.000 mulheres" (fonte: MIQCB, 300-350 mil em 4 estados) | OK |
| V85 | "mais de 64 subprodutos"; "300 mil+" mulheres | OK (ligeira diferenca: 60+ vs 64) |
| V81 | Nao cita numero de produtos nem de quebradeiras | AUSENTE |
| V82 | "300.000" quebradeiras | OK |
| V65 | **"~400.000 mulheres quebradeiras entre MA, TO, PA e PI"** | **INCONSISTENTE** |

**Diagnostico**: INCONSISTENTE PARCIAL.
- Produtos: V06 diz "60+", V85 diz "64" (compativel, mas V85 e mais preciso).
- Quebradeiras: V06/V82/V85 dizem "300.000". V65 diz "~400.000". A diferenca (300k vs 400k) e significativa e precisa de padronizacao. V65 pode estar usando uma estimativa diferente ou mais ampla.

---

## 15. Sonia Guajajara: primeira ministra Povos Indigenas 2023

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V14 | "nomeada em janeiro de 2023 a primeira Ministra dos Povos Indigenas" | OK |
| V16 | "primeira ministra dos Povos Indigenas do Brasil" (jan 2023); deixou cargo marco 2025 | OK |
| V21 | "primeira Ministra dos Povos Indigenas do Brasil" (jan 2023) | OK |
| V65 | "ministra dos Povos Indigenas do Brasil" (2023); TIME 100 | OK |

**Diagnostico**: CONSISTENTE. Todos os verbetes concordam no fato e na data.

---

## 16. Negro Cosme: 3.000 escravizados

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V35 | "cerca de tres mil escravizados" | OK |
| V36 | "tres mil escravizados" (texto principal) + "~3.000 pessoas no quilombo" (box) | OK |

**Diagnostico**: CONSISTENTE. Ambos os verbetes usam o mesmo valor (~3.000).

---

## 17. Lencois: 156.562 ha, UNESCO 2024

| Verbete | Area | UNESCO | Status |
|---------|------|--------|--------|
| V09 | 156.562 ha | Patrimonio Natural da Humanidade, julho 2024 | OK |
| V10 | Nao repete area exata | UNESCO 2024 confirmado | OK |
| V80 | **"155 mil hectares"** | **"candidato a Patrimonio Natural [...] processo em andamento"** | **INCONSISTENTE** |

**Diagnostico**: INCONSISTENTE GRAVE em V80.
1. **Area**: V80 diz "155 mil hectares" (arredondamento impreciso); V09 diz 156.562 ha.
2. **Status UNESCO**: V80 trata os Lencois como CANDIDATURA em andamento ("Se aprovado, sera o primeiro..."). V09 e V10 ja registram a APROVACAO em julho de 2024. **V80 esta desatualizado** — foi escrito antes da aprovacao da UNESCO e nao foi revisado.

---

## 18. Porto Itaqui: 23m de profundidade

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V01 | "23 metros de profundidade natural" | OK |
| V83 | "23 metros de agua sob a quilha" | OK |
| V84 | Nao menciona 23m diretamente (menciona navios de 400 mil toneladas) | AUSENTE |
| V49 | "23 metros" (referencia a baia) | OK |
| V48 | "23 metros de calado natural" | OK |
| V56 | "23 metros de calado natural" | OK |
| V88 | "porto de 23 metros" | OK |
| V91 | "23 metros de calado natural" | OK |
| V101 | "23 metros de calado portuario natural" | OK |

**Diagnostico**: CONSISTENTE. Dado uniforme em todos os verbetes que o mencionam (8 ocorrencias).

---

## 19. MATOPIBA: soja >1M ha

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V02 | "~268.000 ha (2003) -> >1 milhao ha (2023)" | OK |
| V03 | "3,2 milhoes de hectares de soja" (producao total, nao so MATOPIBA) | Dado diferente mas nao contraditorio |
| V86 | "300 mil ha (2000) -> 1,2 milhao (2023)" | **INCONSISTENTE PARCIAL** |
| V82 | "1,2 milhao de hectares" (2023) | OK com V86 |
| V40 | Nao menciona area de soja diretamente | AUSENTE |

**Diagnostico**: INCONSISTENTE PARCIAL.
- V02 usa ano-base 2003 com 268 mil ha; V86 usa ano-base 2000 com 300 mil ha. Anos diferentes explicam parte da diferenca.
- V03 cita "3,2 milhoes de hectares" — este parece ser o total de AREA PLANTADA de graos (nao so soja), pois e incompativel com os demais.
- V82 e V86 concordam em 1,2 milhao ha para 2023.
- V02 diz ">1 milhao ha" para 2023, que e compativel com 1,2M.
- **O dado de V03 (3,2M ha de soja) parece ser producao em toneladas ou area total de graos, nao area de soja.** Verificar.

---

## 20. Tres potencias coloniais

| Verbete | Valor encontrado | Status |
|---------|-----------------|--------|
| V23 | "tres potencias coloniais europeias — francesa, portuguesa e holandesa" | OK |
| V26 | "tres potencias coloniais europeias diferentes" | OK |
| V56 | "colonizacao por tres potencias europeias distintas" | OK |
| V24 | Nao menciona o conceito de "tres potencias" diretamente | AUSENTE |

**Diagnostico**: CONSISTENTE. V23, V26 e V56 concordam. V24 trata da reconquista portuguesa sem usar a formula "tres potencias", o que e aceitavel.

---

## RESUMO EXECUTIVO

### Dados CONSISTENTES (12/20):
1. Biomas (65/34/1%)
2. Mangues (36%, ~500k ha)
3. Amazonia destruida (76%)
4. Populacao indigena (57.214)
5. Ferrovia Carajas (receita Vale > PIB MA)
6. Algodao (651 -> 30.000 arrobas)
7. IDH (0,676)
8. Esgoto tratado (3,92%)
9. Latitude Sao Luis (2 graus 31'S)
10. Sonia Guajajara (ministra 2023)
11. Negro Cosme (3.000 escravizados)
12. Porto Itaqui (23m)
13. Tres potencias coloniais

### Dados INCONSISTENTES (7/20):

| # | Fato | Problema | Gravidade |
|---|------|----------|-----------|
| 1 | **Area do MA** | V01: 329.651 km2 vs. V100/V101: 331.983 km2 | ALTA |
| 5 | **Quilombos certificados** | V35: 1.152 / V37: 868 / V39: 653 (tres valores!) | CRITICA |
| 7 | **Escravizados Itapecuru** | V33/V36: 85% vs. V34: 80% | MEDIA |
| 12 | **Populacao total** | Nenhum verbete cita 6.776.699; V100: ~7,1M; V101: 7M; V103: ~7,15M | ALTA |
| 14 | **Quebradeiras de coco** | V06/V82/V85: 300.000 vs. V65: ~400.000 | MEDIA |
| 17 | **Lencois UNESCO** | V80 trata como candidatura (desatualizado); area 155k vs. 156.562 ha | CRITICA |
| 19 | **Soja MATOPIBA** | V03: "3,2M ha" parece errado; V02 vs V86 usam anos-base diferentes | MEDIA |

### Dados AUSENTES em verbetes esperados (1/20):

| # | Fato | Onde falta |
|---|------|-----------|
| 12 | Populacao total (6.776.699) | V01, V94 — nenhum verbete cita o numero exato do Censo 2022 |

---

## ACOES RECOMENDADAS (por prioridade)

1. **CRITICA — V80 (Lencois)**: Atualizar para refletir aprovacao UNESCO em julho 2024 (ja registrada em V09 e V10). Corrigir area para 156.562 ha.

2. **CRITICA — Quilombos (V35/V37/V39)**: Unificar para um unico dado da Fundacao Cultural Palmares com data de referencia. Definir se MA e 1o ou 2o no ranking. Corrigir os tres verbetes.

3. **ALTA — Area do MA (V01 vs V100/V101)**: Decidir entre 329.651 km2 (IBGE Areas Territoriais 2024) e 331.983 km2. V01 usa o dado mais recente com fonte explicita. Corrigir V100 e V101 para o mesmo valor.

4. **ALTA — Populacao (V100/V101/V103)**: Decidir se o livro usa Censo 2022 (6.776.699) ou estimativa mais recente. Citar o valor exato em pelo menos V01 e V94.

5. **MEDIA — Escravizados Itapecuru (V34)**: Alinhar V34 com V33/V36 (85%) ou explicitar que 80% = escravizados+libertos enquanto 85% = apenas escravizados.

6. **MEDIA — Quebradeiras (V65)**: Alinhar com V06/V85 (300.000) ou explicitar que 400.000 inclui estados alem do MA.

7. **MEDIA — Soja V03**: Verificar se "3,2 milhoes de hectares de soja" esta correto ou se deveria ser "3,2 milhoes de hectares [de graos]" ou "3,2 milhoes de toneladas".

---

*Auditoria realizada por Claude Opus 4.6 em 2026-04-01. Nenhum arquivo foi modificado.*
