# Análise Agronômica Integrada — Blueprint da Ficha do Imóvel

**Contexto:** para cada imóvel rural, nosso cliente (comprador, corretor, avaliador, banco, produtor, advogado) faz perguntas agronômicas concretas. Esta página da ficha `/imoveis/[car]` aba **"Agronomia"** responde todas cruzando MapBiomas + IBGE + Embrapa + CONAB + CEPEA + NASA/INMET.

Documento de referência junto a `catalog-layers-complete.md` e `visual-audit/SYNTHESIS.md`.

---

## 1. As 15 perguntas que definem o valor agronômico de um imóvel

Cada pergunta foi mapeada para fontes de dados disponíveis + cálculo necessário.

| # | Pergunta do cliente | Fonte primária | Fonte comparativa | Saída visual |
|---|---|---|---|---|
| 1 | Qual o histórico de uso do solo nesta fazenda desde 1985? | MapBiomas Cobertura (Coleção 10 via GEE) | — | Timeline LULC 1985-2024 no polígono |
| 2 | Qual cultura foi plantada em cada ano nos últimos 10 anos? | MapBiomas Agricultura (soja, milho, cana, café, algodão, arroz) | IBGE PAM do município | Gantt de culturas por ano |
| 3 | Teve rotação de culturas ou monocultura? | Derivado MapBiomas | — | Sequência "pastagem 5a → soja 3a → milho 2a" + diversidade Shannon |
| 4 | Qual a produtividade média desta região? | IBGE PAM (kg/ha) por município | IBGE PAM estado + Brasil | KPI + ranking percentil |
| 5 | Esta região tem aptidão climática para a cultura X? | Embrapa ZARC (AgroAPI) | Janelas de plantio portaria MAPA | Semáforo + dekêndios aptos |
| 6 | Qual o NDVI histórico do pixel? (vigor vegetativo) | Embrapa SATVeg (MODIS 250m) | Média municipal SATVeg | Gráfico NDVI mensal 2000-2026 |
| 7 | Qual a classe de solo? Tem aptidão agrícola? | Embrapa SmartSolos + IBGE Pedologia | — | Mapa mini + classes + recomendações |
| 8 | Qual a estrutura do solo? (areia/silte/argila, carbono) | MapBiomas Solo + Embrapa | — | Perfil tabelado |
| 9 | Qual o clima histórico? Chove quanto? Quando? | NASA POWER + CHIRPS + INMET | — | Climograma + média anual + anomalia |
| 10 | Teve fogo/queimada no polígono? Frequência? | MapBiomas Fogo | — | Timeline de eventos + nº de vezes queimado |
| 11 | Tem pastagem? Qual a qualidade? | MapBiomas Pastagem (vigor/idade/biomassa) | IBGE PPM do município (rebanho) | Score vigor + idade média |
| 12 | Tem irrigação detectada? Onde? | MapBiomas Agricultura Irrigação + ANA Atlas | — | Polígonos de pivôs centrais |
| 13 | Qual o custo de produção na região? | CONAB Custos de Produção (microrregião) | — | Tabela R$/ha por cultura + decomposição |
| 14 | Qual a margem esperada? | CONAB custo × IBGE rendimento × CEPEA preço | — | R$ líquido/ha por cultura |
| 15 | Qual a expansão da fronteira na região? | MapBiomas expansão agrícola | — | Hectares convertidos de natural → agrícola/ano |

---

## 2. Estrutura da aba "Agronomia" na ficha do imóvel

```
┌─────────────────────────────────────────────────────────┐
│ Ficha do Imóvel CAR MA-2102101-xxxxxxxxxx               │
│ Abas: Visão · Compliance · Dossiê · [Agronomia] · Jur   │
└─────────────────────────────────────────────────────────┘

┌── AGRONOMIA ────────────────────────────────────────────┐
│                                                          │
│ ▶ HISTÓRICO DE USO (1985-2024)                           │
│   Timeline visual 40 anos  [play/scrub]                  │
│   Mudanças detectadas: Cerrado→Pastagem 1998, →Soja 2016 │
│                                                          │
│ ▶ CULTURA NOS ÚLTIMOS 10 ANOS                            │
│   Gantt: soja 2016-2020, milho 2021, soja 2022-2024      │
│   Rotação: [2 culturas] · Diversidade: [baixa]           │
│                                                          │
│ ▶ PRODUTIVIDADE DA REGIÃO                                │
│   Município São Luís/MA:                                 │
│   Soja: 3.400 kg/ha (2024)    — estado 3.200 / BR 3.600  │
│   Milho: 5.800 kg/ha           — percentil 68º nacional   │
│                                                          │
│ ▶ APTIDÃO CLIMÁTICA (ZARC)                               │
│   ┌────────┬─────────┬────────┬────────┐                 │
│   │ Cultura│  Risco  │Dekêndio│ Plantio│                 │
│   ├────────┼─────────┼────────┼────────┤                 │
│   │ Soja   │ 20% (🟢) │ 31-36  │ nov-jan│                 │
│   │ Milho  │ 30% (🟡) │ 13-18  │ mar-mai│                 │
│   └────────┴─────────┴────────┴────────┘                 │
│                                                          │
│ ▶ CLIMA (NASA POWER + CHIRPS, 30 anos)                   │
│   Climograma mensal (chuva + temp)                       │
│   Precipitação anual: 1.850 mm                           │
│   Estação seca: jun-set (3 meses)                        │
│                                                          │
│ ▶ NDVI VIGOR VEGETATIVO (SATVeg/MODIS)                   │
│   Gráfico série 2000-2026                                │
│   Média: 0.72 (vigoroso)  · Máx: 0.89 · Mín: 0.45        │
│                                                          │
│ ▶ SOLO (SmartSolos + MapBiomas)                          │
│   Classe: Latossolo Amarelo (LAd)                        │
│   Textura: argila 48% · areia 35% · silte 17%            │
│   Carbono orgânico: 22.4 t/ha (acima da média bioma)     │
│                                                          │
│ ▶ FOGO / QUEIMADAS                                       │
│   Nº de eventos em 40 anos: 3                            │
│   Última queimada: 2022 (jul)                            │
│   Frequência: baixa (bom para preservação)               │
│                                                          │
│ ▶ PASTAGEM (se houver)                                   │
│   Área detectada: 240 ha                                 │
│   Vigor: alto (NDVI > 0.65)                              │
│   Idade média: 8 anos                                    │
│   Rebanho do município: 145k bovinos (IBGE PPM)          │
│                                                          │
│ ▶ IRRIGAÇÃO                                              │
│   Pivôs detectados: 2 (38 ha total)                      │
│                                                          │
│ ▶ ANÁLISE ECONÔMICA (CONAB × CEPEA × IBGE)               │
│   ┌─────────┬────────┬────────┬────────┬────────┐        │
│   │ Cultura │Custo/ha│Produt. │Preço   │Margem  │        │
│   │         │(CONAB) │(IBGE)  │(CEPEA) │(R$/ha) │        │
│   ├─────────┼────────┼────────┼────────┼────────┤        │
│   │ Soja    │ 3.200  │ 3.400k │ 138,50 │ +4.512 │        │
│   │ Milho   │ 2.850  │ 5.800k │  58,20 │ +4.526 │        │
│   │ Cana    │ 6.200  │92 t/ha │  95/t  │ +2.540 │        │
│   └─────────┴────────┴────────┴────────┴────────┘        │
│                                                          │
│ ▶ EXPANSÃO DA FRONTEIRA (contexto regional)              │
│   Município converteu 18.500 ha natural→agrícola (2015-24)│
│   Pressão de expansão: alta                              │
│                                                          │
└──────────────────────────────────────────────────────────┘
```

---

## 3. Mapeamento fonte → endpoint backend

| Dado | Endpoint backend (planejado) | Fonte |
|---|---|---|
| Histórico LULC por polígono | `POST /gee/imovel/{car}/lulc-history` | Earth Engine Coleção 10 |
| Cultura detectada ano-a-ano | `POST /gee/imovel/{car}/culturas?start=2015&end=2024` | MapBiomas Agricultura |
| Produtividade município | `GET /geo/municipios/{cod}/producao` (já existe) | IBGE SIDRA PAM 5457 |
| Comparativo produtividade | Derivado (query joins) | IBGE PAM agregado |
| Aptidão ZARC | `GET /embrapa/zarc/{cod_municipio}/{cultura}` | Embrapa AgroAPI v2 |
| NDVI série histórica | `GET /embrapa/satveg?lat=X&lon=Y&start=2000&end=2026` | Embrapa SATVeg MODIS |
| Classe de solo | `POST /embrapa/smartsolos/predict?lat&lon` | Embrapa SmartSolos v1 |
| Carbono no solo | `POST /gee/solo/carbono?geom=...` | MapBiomas Solo via GEE |
| Clima histórico | `GET /geo/clima?lat&lon&days=365` (já existe) | NASA POWER + CHIRPS via GEE |
| Focos de fogo | `POST /gee/fogo/historico?geom=...` | MapBiomas Fogo via GEE |
| Pastagem vigor/idade | `POST /gee/pastagem/metrics?geom=...` | MapBiomas Pastagem |
| Pivôs irrigação | `POST /gee/irrigacao/detect?geom=...` | MapBiomas Agricultura |
| Custos produção | `GET /market/custos/{uf}/{cultura}` | CONAB parsing |
| Preço commodities | `GET /market/quotes/{cultura}` (já existe) | CEPEA/ESALQ |
| Rendimento médio | Derivado IBGE PAM | IBGE SIDRA |
| Margem estimada | Cálculo: custo × produtividade × preço | Backend derivado |
| Expansão fronteira | `POST /gee/expansao/{municipio_cod}` | MapBiomas Coleção 10 |

---

## 4. Cruzamentos que agregam valor único (nossos moats)

### 4.1 "Fazenda-melhor-que-o-vizinho?" (benchmark automático)

Para cada métrica (produtividade, NDVI, vigor pasto, rotação diversidade), comparar:
- **Polígono** do CAR vs **média do município** vs **média do estado** vs **média do bioma**

Resultado: `Esta fazenda: NDVI 0.72 · percentil 78% do município São Luís/MA · percentil 62% do Maranhão`

Ninguém no mercado faz isso. Registro Rural, SpotSat, Agrotools mostram dados; não dão contexto comparativo.

### 4.2 "Pode plantar X com segurança?"

Cruzamento ZARC × solo × declividade × histórico NDVI × regime hídrico = veredicto com confiança:

> "Para plantar **soja**: aptidão ALTA. ZARC indica risco 20% na janela 31-36. Solo Latossolo Amarelo (argila 48%) é adequado. Histórico NDVI > 0.65 em 8 de 10 safras passadas. Chuva média acima da necessidade hídrica (1850 mm vs 1200 mm ideal). **Probabilidade de safra boa: 78%**."

### 4.3 "Quanto rende plantando cada cultura?"

Matriz simulada de margem líquida por cultura candidata → **ranking de aptidão econômica**.

### 4.4 "Quanto vale a terra produtiva aqui?"

Valuation por renda capitalizada (NBR 14.653-3):
- VTN mínimo = margem × fator capitalização BCB
- Comparativo com SIMET/INCRA VTN oficial
- Desconto por passivos (embargos, RL deficitária, distância logística)

### 4.5 "A fazenda tem degradação oculta?"

Cruzar:
- MapBiomas Pastagem idade (pasto >15 anos = degradado se vigor baixo)
- NDVI trending (queda > 10% em 5 anos = degradação)
- Desmatamento pós-2019 no polígono (MCR 2.9 violação)
- Cicatrizes de fogo > 3 vezes em 10 anos (solo esgotado)

Score de degradação 0-100 com evidências clicáveis.

### 4.6 "Potencial de crédito de carbono?"

- MapBiomas Solo carbono + Vegetação secundária idade
- Estoque acima da média bioma = potencial PSA/REDD+/Verra
- Output: hectares elegíveis × R$/tCO₂e = receita potencial

---

## 5. Ordem de implementação

**Sprint A (3-4 dias) — Baseline com dados já disponíveis:**
- Endpoint `/geo/municipios/{cod}/producao` (já existe) + UI de KPIs IBGE
- Endpoint clima (já existe) + climograma
- CEPEA quotes (já existe) + tabela preços
- UI da aba Agronomia com esses 3 blocos preenchidos

**Sprint B (5-7 dias) — MapBiomas via Earth Engine:**
- Ativar GCP credentials no container (já configurado)
- Endpoints GEE: LULC history, cultura por ano, fogo, pastagem, irrigação
- UI: timeline + gantt + NDVI chart

**Sprint C (3-4 dias) — Embrapa AgroAPI:**
- Coletor OAuth Embrapa (Consumer Key/Secret já obtidos)
- Endpoints: ZARC, SmartSolos, SATVeg NDVI, ClimAPI, Agritec
- UI: tabelas de aptidão ZARC + perfil solo

**Sprint D (4-5 dias) — Derivações analíticas:**
- CONAB scraping/parse de custos por microrregião
- Cálculo margem = custo × produtividade × preço
- Benchmark percentil (polígono vs município/estado/bioma)
- Score degradação

**Sprint E (3 dias) — Valuation integrada:**
- Valor-terra capitalizado via margem + taxa capitalização BCB
- Comparativo SIMET/INCRA
- PDF laudo exportável

**Total:** ~20 dias para aba Agronomia completa com valor único vs concorrentes.

---

## 6. Observação final

Este blueprint **não é só sobre camadas** no mapa. As **camadas adicionadas ao catálogo** (14 agricultura + 10 produção IBGE + 7 clima expandido) são insumos brutos. O valor está em:

1. **Contexto cruzado** — fazer as perguntas agronômicas certas e responder com dados integrados
2. **Visualização acionável** — timeline + gantt + climograma + tabela margem em uma tela
3. **Benchmark comparativo** — o polígono vs vizinhança
4. **Simulação econômica** — custo × produtividade × preço × cultura candidata

É o que nenhum concorrente faz (confirmado na auditoria das 48 plataformas) e o que realmente decide uma compra, arrendamento, financiamento ou defesa de um imóvel rural.

---

*Documento complementar a `visual-audit/SYNTHESIS.md` e `catalog-layers-complete.md`. Referenciado pela ficha do imóvel `/imoveis/[car]` aba "Agronomia".*
