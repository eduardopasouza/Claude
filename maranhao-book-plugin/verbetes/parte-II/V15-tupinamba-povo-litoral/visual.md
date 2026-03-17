---
id: VIS-V15-A
verbete: V15
tipo: mapa
posicao: página-inteira
---

# Visual V15-A: O mundo Tupinambá no Maranhão — 1612

## 1. Briefing para designer
**O que é**: Mapa ilustrado da ilha de São Luís e arredores mostrando a ocupação Tupinambá conforme descrita por d'Abbeville (1612). Página inteira.
**Dados**:
- 27 aldeias identificadas na ilha e entorno
- ~12.000 habitantes estimados
- Nome indígena: Upaon-Açu ("ilha grande")
- Aldeias principais: Juniparã (Japiaçu), Eussauap (Momboreuaçu), Timbohu, Itapari
- Localização do futuro Forte São Luís
- Roças de mandioca indicadas ao redor das aldeias
- Rios e igarapés com nomes Tupinambá
- Canoas nas águas da baía
- Rota marítima para a costa (indicação das aldeias do continente)
**Referência de estilo**: Mapa estilizado inspirado nas gravuras de d'Abbeville, porém com tratamento editorial moderno (DK / Atlas histórico). Traço limpo, cores limitadas.
**Paleta**: Verde-mangue (#1E8449) para floresta/vegetação, Azul-mar (#1B4F72) para água, Terracota (#BA4A00) para aldeias e caminhos, Dourado-babaçu (#D4AC0D) para destaques e nomes
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Silhueta simplificada da ilha de São Luís (forma orgânica)
- Baía de São Marcos ao oeste, Baía de São José ao sul
- Pontos terracota para as 27 aldeias (os maiores para Juniparã e Eussauap)
- Linhas tracejadas para caminhos entre aldeias
- Pequenos ícones de maloca para aldeias principais
- Canoas estilizadas na baía
- Áreas verdes hachuradas para roças
- Ponto dourado onde será construído o Forte São Luís
- Legenda com dados populacionais

```svg
<svg viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Água -->
  <rect x="0" y="0" width="600" height="500" fill="#1B4F72" opacity="0.15"/>
  <text x="50" y="100" fill="#1B4F72" font-size="14" font-style="italic">Baía de São Marcos</text>
  <text x="250" y="470" fill="#1B4F72" font-size="12" font-style="italic">Baía de São José</text>

  <!-- Ilha de São Luís (forma simplificada) -->
  <ellipse cx="320" cy="250" rx="200" ry="140" fill="#1E8449" opacity="0.3" stroke="#1E8449" stroke-width="2"/>
  <text x="280" y="200" fill="#1E8449" font-size="10" font-weight="bold">UPAON-AÇU</text>
  <text x="290" y="215" fill="#1E8449" font-size="9">"a ilha grande"</text>

  <!-- Aldeias principais -->
  <!-- Juniparã (Japiaçu) -->
  <circle cx="280" cy="260" r="8" fill="#BA4A00"/>
  <text x="240" y="285" fill="#BA4A00" font-size="10" font-weight="bold">Juniparã</text>
  <text x="245" y="296" fill="#BA4A00" font-size="8">(chefe Japiaçu)</text>

  <!-- Eussauap (Momboreuaçu) -->
  <circle cx="370" cy="240" r="7" fill="#BA4A00"/>
  <text x="385" y="240" fill="#BA4A00" font-size="10" font-weight="bold">Eussauap</text>
  <text x="385" y="251" fill="#BA4A00" font-size="8">(Momboreuaçu)</text>

  <!-- Outras aldeias (menores) -->
  <circle cx="200" cy="230" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="350" cy="180" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="420" cy="270" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="300" cy="310" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="250" cy="190" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="440" cy="220" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="380" cy="300" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="180" cy="270" r="4" fill="#BA4A00" opacity="0.7"/>
  <circle cx="330" cy="150" r="4" fill="#BA4A00" opacity="0.7"/>

  <!-- Forte São Luís (futuro) -->
  <rect x="295" cy="225" width="10" height="10" fill="#D4AC0D" stroke="#D4AC0D" stroke-width="1"/>
  <text x="310" y="235" fill="#D4AC0D" font-size="8" font-style="italic">futuro Forte São Luís</text>

  <!-- Canoas na baía -->
  <text x="80" y="200" fill="#1B4F72" font-size="20">⛵</text>
  <text x="120" y="250" fill="#1B4F72" font-size="16">⛵</text>
  <text x="60" y="300" fill="#1B4F72" font-size="18">⛵</text>

  <!-- Legenda -->
  <rect x="20" y="380" width="250" height="100" fill="white" opacity="0.9" rx="5"/>
  <text x="30" y="400" fill="#333" font-size="11" font-weight="bold">O MUNDO TUPINAMBÁ — 1612</text>
  <circle cx="35" cy="415" r="5" fill="#BA4A00"/>
  <text x="45" y="419" fill="#333" font-size="9">27 aldeias identificadas por d'Abbeville</text>
  <text x="30" y="435" fill="#333" font-size="9">~12.000 habitantes na ilha e arredores</text>
  <text x="30" y="450" fill="#333" font-size="9">Língua: Tupinambá (tronco Tupi)</text>
  <text x="30" y="465" fill="#666" font-size="8">Fonte: ABBEVILLE, Claude d'. Histoire de la mission (1614)</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Historical illustrated map of São Luís island (Maranhão, Brazil) in 1612, showing the Tupinambá indigenous settlements before European colonization. The island is called Upaon-Açu ('great island'). Show approximately 27 small villages marked by longhouses (malocas) surrounded by forest. The Bay of São Marcos on the west side with indigenous canoes carved from single tree trunks. Manioc fields around the villages. A large central village (Juniparã) prominently marked. The style should blend 16th-century cartographic aesthetics (like Claude d'Abbeville's engravings) with modern editorial map design (clean, limited color palette). Colors: forest green, ocean blue, terracotta for settlements, gold for highlights. No modern buildings. No roads. Pure pre-colonial landscape. Bird's eye view, slightly tilted. Coffee table book quality."
**Estilo**: Cartografia histórica editorial — fusão de gravura seiscentista com design contemporâneo
**NÃO incluir**: Edifícios coloniais, estradas modernas, texto definitivo em português (designer adicionará)

---

---
id: VIS-V15-B
verbete: V15
tipo: infográfico
posicao: meia-página
---

# Visual V15-B: A embaixada Tupinambá — do Maranhão a Paris (1613)

## 1. Briefing para designer
**O que é**: Infográfico narrativo mostrando a jornada dos seis embaixadores Tupinambá do Maranhão a Paris em 1613. Meia página.
**Dados**:
- Saída: Ilha de São Luís (Upaon-Açu), início de 1613
- Chegada: Paris, julho de 1613
- 6 embaixadores: Uaruajá, Ity-assú, Arimã, Manéo, Patua, Japouay
- 3 batizados em Paris (nomes franceses: Luís, Luísa(?), Francisco)
- 3 morreram na França (doenças respiratórias)
- 2-3 retornaram ao Maranhão em 1614
- Presentes na cerimônia: Maria de Médici, Luís XIII (12 anos)
- Distância: ~7.000 km por mar
**Referência de estilo**: Timeline/jornada — estilo Monocle ou New York Times infographics
**Paleta**: Azul-mar (#1B4F72) para o oceano/travessia, Terracota (#BA4A00) para marcos, Dourado (#D4AC0D) para Paris/destaque, Preto (#1C1C1C) para texto
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**:
- Linha curva representando a travessia atlântica (MA → Paris)
- Silhueta de 6 figuras no início (Maranhão)
- 3 figuras com X ao chegar à França (mortos)
- 3 figuras seguindo para Paris
- Ícone da igreja dos Capuchinhos (batismo)
- Silhueta de coroa (Luís XIII)
- Linha de retorno com 2-3 figuras

## 3. Prompt para IA generativa
**Prompt**: "Editorial infographic showing the journey of six Tupinambá indigenous ambassadors from Maranhão, Brazil to Paris, France in 1613. Visual narrative: START with six standing figures in indigenous attire on the Brazilian coast, then an oceanic crossing shown as a curved path across the Atlantic, then arrival in Paris where three figures fade away (died of disease) and three are shown at a baptism ceremony in a church with the French royal court watching. Return journey with only 2-3 figures. Clean editorial style, limited color palette (navy blue, terracotta, gold), modern infographic design for coffee table book. Horizontal layout. Somber but dignified tone."
**Estilo**: Infográfico narrativo editorial
**NÃO incluir**: Caricaturas, estereótipos indígenas, texto definitivo
