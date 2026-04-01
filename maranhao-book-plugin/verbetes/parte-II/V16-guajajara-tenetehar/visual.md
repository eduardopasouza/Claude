---
id: VIS-V16-A
verbete: V16
tipo: mapa
posicao: pagina-inteira
---

# Visual V16-A: Terras Indigenas Guajajara no Maranhao

## 1. Briefing para designer
**O que e**: Mapa das quatro principais Terras Indigenas Guajajara no centro-oeste do Maranhao, mostrando o contraste entre a cobertura florestal dentro das TIs e o desmatamento ao redor. Pagina inteira.
**Dados**:
- TI Arariboia: ~413.000 ha (a maior). Municipios: Amarante do MA, Bom Jesus das Selvas, Arame, Buriticupu
- TI Caru: ~172.000 ha. Municipios: Bom Jardim, Alto Alegre do Pindare
- TI Pindare: ~15.000 ha. Municipio: Bom Jardim
- TI Governador: ~41.000 ha. Municipios: Governador, Amarante do MA
- Povos presentes: Guajajara (todas), Awa-Guaja (Arariboia e Caru), Gaviao (Governador)
- Rios: Pindare, Grajau, Mearim e afluentes
- Entorno: areas desmatadas (pasto/soja) — contraste visual forte
- Indicar Barra do Corda e Grajau como cidades de referencia
- Ponto vermelho na localizacao aproximada do assassinato de Paulo Paulino (TI Arariboia, proximo a Bom Jesus das Selvas)
- Dado em destaque: "52% da floresta remanescente do MA esta em TIs"
**Referencia de estilo**: Mapa editorial com dados de satelite estilizados — inspiracao National Geographic ou Mongabay. Contraste dramatico verde/marrom.
**Paleta**: Verde-floresta (#1E6B37) para TIs/floresta, Terracota (#B5533E) para areas desmatadas e destaques, Ocre (#D4AC0D) para cidades e textos, Cinza (#666666) para limites municipais
**Tamanho**: Pagina inteira (23x28 cm)

## 2. SVG simplificado
**Elementos**:
- Contorno do estado do Maranhao (simplificado)
- Quatro TIs como poligonos verdes no centro-oeste
- Entorno em terracota/marrom claro (desmatamento)
- Rios Pindare, Grajau, Mearim em azul
- Icones de aldeia dentro das TIs
- Icone especial para localizacao do assassinato de Paulo Paulino
- Cidades de referencia: Barra do Corda, Grajau, Amarante, Buriticupu
- Legenda com areas (ha) de cada TI
- Dado em caixa de destaque: "52%"
- Inset: localizacao do MA no Brasil

```svg
<svg viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo estado (simplificado) -->
  <rect x="0" y="0" width="600" height="500" fill="#F5F0E8"/>
  <path d="M100,50 L500,30 L550,200 L520,400 L400,480 L200,460 L80,350 Z" fill="#D4A574" opacity="0.3" stroke="#999" stroke-width="1"/>
  <text x="420" y="80" fill="#999" font-size="10" font-style="italic">MARANHAO</text>

  <!-- Area desmatada (entorno das TIs) -->
  <ellipse cx="250" cy="280" rx="180" ry="120" fill="#B5533E" opacity="0.15"/>

  <!-- TI Arariboia (maior) -->
  <ellipse cx="250" cy="260" rx="80" ry="55" fill="#1E6B37" opacity="0.7" stroke="#1E6B37" stroke-width="2"/>
  <text x="210" y="255" fill="white" font-size="11" font-weight="bold">TI ARARIBOIA</text>
  <text x="220" y="270" fill="white" font-size="9">413.000 ha</text>

  <!-- TI Caru -->
  <ellipse cx="180" cy="200" rx="35" ry="25" fill="#1E6B37" opacity="0.7" stroke="#1E6B37" stroke-width="2"/>
  <text x="155" y="200" fill="white" font-size="8" font-weight="bold">TI CARU</text>
  <text x="155" y="210" fill="white" font-size="7">172.000 ha</text>

  <!-- TI Pindare -->
  <circle cx="155" cy="240" r="15" fill="#1E6B37" opacity="0.7" stroke="#1E6B37" stroke-width="2"/>
  <text x="130" y="260" fill="#1E6B37" font-size="7" font-weight="bold">TI Pindare</text>

  <!-- TI Governador -->
  <ellipse cx="310" cy="310" rx="25" ry="18" fill="#1E6B37" opacity="0.7" stroke="#1E6B37" stroke-width="2"/>
  <text x="280" y="335" fill="#1E6B37" font-size="7" font-weight="bold">TI Governador</text>

  <!-- Rios -->
  <path d="M120,150 Q180,200 200,300 Q220,380 240,430" fill="none" stroke="#1B4F72" stroke-width="1.5" opacity="0.6"/>
  <text x="130" y="170" fill="#1B4F72" font-size="8" font-style="italic">R. Pindare</text>
  <path d="M300,150 Q280,250 290,350 Q300,400 310,440" fill="none" stroke="#1B4F72" stroke-width="1.5" opacity="0.6"/>
  <text x="305" y="170" fill="#1B4F72" font-size="8" font-style="italic">R. Grajau</text>

  <!-- Cidades -->
  <circle cx="350" cy="350" r="4" fill="#D4AC0D"/>
  <text x="358" y="354" fill="#333" font-size="9">Barra do Corda</text>
  <circle cx="320" cy="200" r="4" fill="#D4AC0D"/>
  <text x="328" y="204" fill="#333" font-size="9">Grajau</text>

  <!-- Ponto Paulo Paulino -->
  <circle cx="220" cy="240" r="6" fill="#CC0000" stroke="white" stroke-width="2"/>
  <text x="230" y="235" fill="#CC0000" font-size="7" font-weight="bold">Paulo Paulino</text>
  <text x="230" y="243" fill="#CC0000" font-size="6">assassinado 2019</text>

  <!-- Legenda -->
  <rect x="380" y="360" width="200" height="120" fill="white" opacity="0.95" rx="5" stroke="#ccc"/>
  <text x="390" y="380" fill="#333" font-size="12" font-weight="bold">TERRAS INDIGENAS GUAJAJARA</text>
  <rect x="390" y="390" width="12" height="12" fill="#1E6B37"/>
  <text x="408" y="400" fill="#333" font-size="9">Terra Indigena (floresta)</text>
  <rect x="390" y="408" width="12" height="12" fill="#B5533E" opacity="0.3"/>
  <text x="408" y="418" fill="#333" font-size="9">Entorno desmatado</text>
  <circle cx="396" cy="433" r="4" fill="#CC0000"/>
  <text x="408" y="436" fill="#333" font-size="9">Guardiao assassinado</text>
  <text x="390" y="460" fill="#B5533E" font-size="14" font-weight="bold">52%</text>
  <text x="425" y="460" fill="#333" font-size="9">da floresta do MA</text>
  <text x="425" y="470" fill="#333" font-size="9">esta em TIs</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Editorial map of the central-western Maranhao state (Brazil) showing four indigenous territories (Terras Indigenas) of the Guajajara people: Arariboia (largest, 413,000 hectares), Caru, Pindare, and Governador. The key visual contrast: the indigenous territories are covered in dense green Amazon forest, while the surrounding area is brown/terracotta colored cleared land (cattle ranches and soy farms). The boundary between forest and cleared land is sharp and dramatic — visible from satellite. Rivers (Pindare, Grajau, Mearim) flow through the region in blue. Small indigenous villages marked inside the green zones. A red marker in the Arariboia territory indicating where a forest guardian was killed. Towns of reference: Barra do Corda, Grajau. Bold statistic overlay: '52% of Maranhao's remaining forest is inside Indigenous Territories.' Style: editorial cartography meets satellite imagery, clean layout, coffee table book quality. Colors: forest green, terracotta, gold accents, navy blue for rivers."
**Estilo**: Cartografia editorial com dados de satelite estilizados
**NAO incluir**: Texto definitivo (designer adicionara), estereotipos visuais indigenas

---

---
id: VIS-V16-B
verbete: V16
tipo: infografico
posicao: meia-pagina
---

# Visual V16-B: A muralha verde — o que os Guajajara protegem

## 1. Briefing para designer
**O que e**: Infografico comparativo mostrando a relacao entre Terras Indigenas e cobertura florestal no Maranhao. Meia pagina.
**Dados**:
- Cobertura florestal total remanescente do MA: ~30% do territorio (dados MapBiomas)
- Parcela dentro de TIs: 52%
- TI Arariboia: 413.000 ha (maior que o DF, que tem 5.760 km2 = 576.000 ha — comparacao: Arariboia = ~72% do DF)
- 4 TIs Guajajara: area total ~641.000 ha
- Populacao Guajajara: ~30.000 pessoas
- Guardioes da Floresta: criados em 2012
- Guardioes assassinados: pelo menos 4 (2016-2020)
- Incendios na TI Arariboia: >40% da area afetada (2015, 2017)
**Referencia de estilo**: Infografico comparativo tipo The Economist / National Geographic — dados visuais, pouca palavra
**Paleta**: Verde (#1E6B37), Terracota (#B5533E), Dourado (#D4AC0D), Preto (#1C1C1C)
**Tamanho**: Meia pagina (~11x14 cm)

## 2. SVG simplificado
**Elementos**:
- Grafico de pizza ou barra mostrando 52% / 48% (floresta em TIs vs. fora de TIs)
- Comparacao de area: TI Arariboia vs. Distrito Federal (silhuetas sobrepostas)
- Timeline simplificada: 2012 (Guardioes criados) → 2015/2017 (incendios) → 2019 (Paulo Paulino) → 2023 (Sonia ministra)
- Icones: arvore (floresta), motosserra (ameaca), escudo (protecao)

## 3. Prompt para IA generativa
**Prompt**: "Clean editorial infographic about indigenous forest protection in Maranhao, Brazil. Central data point: 52% of the state's remaining forest is inside Indigenous Territories. Visual elements: (1) A dramatic pie chart or split bar showing 52% vs 48%, green vs terracotta; (2) Size comparison — Arariboia indigenous territory (413,000 ha) shown as a silhouette overlapping the Federal District of Brasilia for scale; (3) A minimal timeline: 2012 (Forest Guardians created) — 2015/2017 (fires) — 2019 (guardian killed) — 2023 (first indigenous minister). Icons: tree for forest, chainsaw for threat, shield for protection. Style: The Economist meets National Geographic infographics. Colors: deep green, terracotta, gold, black. Coffee table book quality. Half-page format, horizontal."
**Estilo**: Infografico editorial comparativo
**NAO incluir**: Texto definitivo, decoracao excessiva
