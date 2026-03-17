---
id: VIS-V85-A
verbete: V85
tipo: infográfico
posicao: página-inteira
---

# Visual V85-A: Anatomia do coco babaçu — 64 produtos de uma palmeira

## 1. Briefing para designer
**O que é**: Infográfico explodido mostrando as camadas do fruto do babaçu e todos os produtos derivados de cada parte. Página inteira — visual principal do verbete.
**Dados**:
- EPICARPO (casca externa): fibras para artesanato
- MESOCARPO (camada intermediária): farinha nutritiva, mingau, bolo, biscoito, complemento alimentar
- ENDOCARPO (casca dura): carvão de alta eficiência (80% carbono), combustível doméstico
- AMÊNDOAS (3-8 por fruto): óleo de cozinha, sabão, cosméticos, biodiesel, leite de coco babaçu
- FOLHAS: palha para telhado, paredes, cestos, esteiras
- TRONCO: madeira de construção
- PALMITO: alimentação
- RAIZ: remédio popular
- Total: 64+ subprodutos catalogados (Embrapa/WWF)
- Dimensão do fruto: oval, tamanho de punho, castanho
- Palmeira: 20m de altura, 15-20 anos para maturidade, 2.000 frutos/ano
**Referência de estilo**: Infográfico "explodido" tipo DK ou Kurzgesagt — fruto cortado ao meio com setas apontando para produtos derivados
**Paleta**: Dourado-babaçu (#D4AC0D) para o coco, Verde-mangue (#1E8449) para folhas/palmeira, Terracota (#BA4A00) para carvão/casca, Branco para amêndoas
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Centro: coco babaçu cortado ao meio, mostrando 4 camadas concêntricas (epicarpo, mesocarpo, endocarpo, amêndoas)
- Setas radiais apontando para ícones de cada produto derivado
- Palmeira inteira (silhueta) ao lado, com setas para folhas, tronco, palmito, raiz
- Dados numéricos: 64 produtos, 300 mil mulheres, 2.000 frutos/palmeira/ano
**Layout**: Central, radiante

```svg
<svg viewBox="0 0 600 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Título -->
  <text x="300" y="30" text-anchor="middle" fill="#333" font-size="16" font-weight="bold">ANATOMIA DO BABAÇU</text>
  <text x="300" y="50" text-anchor="middle" fill="#666" font-size="11">64 produtos de uma única palmeira</text>

  <!-- Coco cortado — camadas concêntricas -->
  <!-- Epicarpo -->
  <ellipse cx="250" cy="250" rx="80" ry="100" fill="#8B6914" opacity="0.8"/>
  <!-- Mesocarpo -->
  <ellipse cx="250" cy="250" rx="65" ry="85" fill="#D4AC0D" opacity="0.7"/>
  <!-- Endocarpo -->
  <ellipse cx="250" cy="250" rx="45" ry="60" fill="#5D3A1A"/>
  <!-- Amêndoas -->
  <ellipse cx="235" cy="230" rx="10" ry="15" fill="#FFFFF0" stroke="#D4AC0D"/>
  <ellipse cx="265" cy="230" rx="10" ry="15" fill="#FFFFF0" stroke="#D4AC0D"/>
  <ellipse cx="250" cy="260" rx="10" ry="15" fill="#FFFFF0" stroke="#D4AC0D"/>

  <!-- Setas e produtos — Epicarpo -->
  <line x1="330" y1="170" x2="420" y2="100" stroke="#8B6914" stroke-width="1.5"/>
  <text x="425" y="95" fill="#8B6914" font-size="10" font-weight="bold">EPICARPO</text>
  <text x="425" y="110" fill="#666" font-size="9">→ fibras, artesanato</text>

  <!-- Setas e produtos — Mesocarpo -->
  <line x1="330" y1="220" x2="420" y2="180" stroke="#D4AC0D" stroke-width="1.5"/>
  <text x="425" y="175" fill="#D4AC0D" font-size="10" font-weight="bold">MESOCARPO</text>
  <text x="425" y="190" fill="#666" font-size="9">→ farinha, mingau, bolo</text>
  <text x="425" y="203" fill="#666" font-size="9">→ complemento nutricional</text>

  <!-- Setas e produtos — Endocarpo -->
  <line x1="330" y1="280" x2="420" y2="270" stroke="#5D3A1A" stroke-width="1.5"/>
  <text x="425" y="265" fill="#5D3A1A" font-size="10" font-weight="bold">ENDOCARPO</text>
  <text x="425" y="280" fill="#666" font-size="9">→ carvão (80% carbono)</text>
  <text x="425" y="293" fill="#666" font-size="9">→ combustível doméstico</text>

  <!-- Setas e produtos — Amêndoas -->
  <line x1="330" y1="330" x2="420" y2="350" stroke="#BA4A00" stroke-width="1.5"/>
  <text x="425" y="345" fill="#BA4A00" font-size="10" font-weight="bold">AMÊNDOAS (3-8)</text>
  <text x="425" y="360" fill="#666" font-size="9">→ óleo, sabão, cosmético</text>
  <text x="425" y="373" fill="#666" font-size="9">→ biodiesel, leite de coco</text>

  <!-- Palmeira (silhueta) -->
  <line x1="80" y1="450" x2="80" y2="150" stroke="#1E8449" stroke-width="4"/>
  <!-- Copa -->
  <path d="M30,150 Q80,80 130,150" fill="none" stroke="#1E8449" stroke-width="2"/>
  <path d="M40,140 Q80,70 120,140" fill="none" stroke="#1E8449" stroke-width="2"/>
  <path d="M20,160 Q80,100 140,160" fill="none" stroke="#1E8449" stroke-width="2"/>

  <!-- Setas da palmeira -->
  <line x1="60" y1="145" x2="10" y2="110" stroke="#1E8449" stroke-width="1"/>
  <text x="5" y="100" fill="#1E8449" font-size="9">FOLHAS → palha, cestos, telhado</text>

  <line x1="75" y1="300" x2="10" y2="300" stroke="#1E8449" stroke-width="1"/>
  <text x="5" y="295" fill="#1E8449" font-size="9">TRONCO → madeira</text>

  <line x1="75" y1="440" x2="10" y2="460" stroke="#1E8449" stroke-width="1"/>
  <text x="5" y="465" fill="#1E8449" font-size="9">RAIZ → remédio popular</text>

  <!-- Dados-chave -->
  <text x="300" y="430" text-anchor="middle" fill="#333" font-size="11">20m de altura | 2.000 frutos/ano | maturidade aos 15-20 anos</text>
  <text x="300" y="450" text-anchor="middle" fill="#BA4A00" font-size="11" font-weight="bold">300 mil mulheres vivem da quebra do coco</text>
  <text x="300" y="475" text-anchor="middle" fill="#666" font-size="10">70% dos babaçuais do Brasil estão no Maranhão</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Detailed botanical infographic of the babassu palm (Attalea speciosa) and its fruit. Center: large cross-section of the babassu coconut showing four concentric layers — outer brown epicarp, golden starchy mesocarp, hard dark endocarp, and white almonds (3-8 per fruit). Radiating arrows pointing to icons of derived products: cooking oil, soap, charcoal, flour, roof thatch, baskets, biodiesel. Side: full silhouette of a 20-meter babassu palm with arrows to leaves (thatch), trunk (construction wood), roots (traditional medicine). Clean exploded-view infographic style, DK or Kurzgesagt quality. Color palette: golden amber for mesocarp, dark brown for endocarp, white for almonds, green for palm fronds. Scientific botanical illustration meets modern infographic design. No text — labels will be added in Portuguese."
**Estilo**: Infográfico botânico-editorial (DK / Kurzgesagt)
**NÃO incluir**: Texto definitivo, pessoas (serão tratadas em visual separado)

---

---
id: VIS-V85-B
verbete: V85
tipo: mapa
posicao: meia-página
---

# Visual V85-B: Mapa da Mata dos Cocais — o território do babaçu

## 1. Briefing para designer
**O que é**: Mapa mostrando a distribuição do babaçu no Brasil, com ênfase na concentração maranhense. Meia página.
**Dados**:
- Área total: 13-18 milhões de hectares
- Maranhão: 70% (~141 mil km² — maior que a Grécia)
- Piauí, Tocantins, Pará: parcelas menores
- Manchas em Goiás, Mato Grosso, Minas Gerais
- Sobreposição com avanço do MATOPIBA (soja/pecuária) como ameaça
- Municípios-chave: Pedreiras, Bacabal, Codó, Lago do Junco, Esperantinópolis, Imperatriz
- 12 municípios com Lei do Babaçu Livre destacados
**Referência de estilo**: Mapa temático editorial — cobertura de babaçu em gradiente dourado, avanço do agronegócio em cinza/vermelho
**Paleta**: Dourado-babaçu (#D4AC0D) para cobertura de babaçu, Vermelho-soja (#C0392B) para frente do MATOPIBA, Verde para áreas preservadas, Branco para fundo
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**: Mapa do Brasil com estados relevantes (MA, PI, TO, PA) destacados, gradiente dourado sobre área de babaçu, setas vermelhas indicando avanço do agronegócio, pontos para municípios com Lei do Babaçu Livre
**Layout**: Vertical, com inset de detalhe do Maranhão

## 3. Prompt para IA generativa
**Prompt**: "Thematic map of Brazil showing the distribution of babassu palm forests (Mata dos Cocais). Golden-amber shading over the babassu zone concentrated in Maranhão (70%), with lighter extensions into Piauí, Tocantins, and Pará. Red arrows or shading showing the advancing agricultural frontier (MATOPIBA — soy and cattle) encroaching on the palm zone from the south and east. Small palm tree icons scattered across the golden zone. Key municipalities marked with dots. Inset comparing the babassu area (141,000 km²) to Greece for scale. Clean editorial cartography, The Pudding or National Geographic style. Color palette: golden amber for babassu, red for agribusiness threat, green for preserved areas, neutral background."
**Estilo**: Cartografia temática editorial
**NÃO incluir**: Texto definitivo, grade de coordenadas
