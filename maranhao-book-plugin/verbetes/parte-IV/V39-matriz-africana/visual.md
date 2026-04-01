---
id: VIS-V39-A
verbete: V39
tipo: infografico
posicao: pagina-inteira
---

# Visual V39-A: Mosaico "A heranca viva" — seis dimensoes da matriz africana

## 1. Briefing para designer

**O que e**: Infografico de pagina inteira em formato de mosaico hexagonal. Seis hexagonos tematicos representando as seis dimensoes da heranca africana no Maranhao: O Sagrado, O Corpo, O Som, A Mesa, A Palavra, A Terra. Cada hexagono contem um icone, um titulo e um dado-chave. No centro, o numero "78%" (populacao negra e parda) une tudo.

**Dados**:
- O SAGRADO: Tambor de Mina — terreiros desde ~1840 — os encantados
- O CORPO: Tambor de Crioula — Patrimonio IPHAN 2007 — a punga
- O SOM: Reggae — unica "Jamaica" fora da Jamaica — radiolas
- A MESA: Arroz de cuxa — vinagreira, gergelim, camarao seco — tudo africano
- A PALAVRA: Cuxa, quilombo, samba, batuque, quiabo — lingua viva
- A TERRA: 653 quilombos certificados — maior numero do Brasil
- CENTRO: 78% negra/parda (IBGE 2022)

**Referencia de estilo**: Mosaico editorial geometrico, tipo NYT interactives ou National Geographic. Hexagonos com bordas finas, fundo suavemente colorido, tipografia serifada para titulos e sans-serif para dados. Elegante, nao infantil.

**Paleta**:
- Fundo geral: creme #FAF3E8
- Hexagonos: preenchimento sutil em variantes de roxo-tambor #5E3A7E (10-20% opacidade)
- Bordas: roxo-tambor #5E3A7E (solido)
- Icones: ocre #C8952E
- Textos titulos: carvao #2B2B2B
- Textos dados: roxo-tambor #5E3A7E
- Numero central (78%): roxo-tambor #5E3A7E, grande, bold

**Tamanho**: Pagina inteira (23x28cm)

## 2. SVG simplificado

**Elementos**:
- 6 hexagonos dispostos em anel ao redor de um circulo central
- Circulo central com "78%" em fonte grande
- Cada hexagono: icone (emoji placeholder) + titulo + dado-chave (1 linha)

**Layout**: Radial, simetrico. Hexagonos nos vertices de um hexagono maior.

**Cores**: roxo-tambor para estrutura, ocre para icones, carvao para texto

```svg
<svg viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="500" height="600" fill="#FAF3E8"/>

  <!-- Titulo -->
  <text x="250" y="35" text-anchor="middle" font-family="serif" font-size="16" font-weight="bold" fill="#2B2B2B">A HERANCA VIVA</text>
  <text x="250" y="52" text-anchor="middle" font-family="sans-serif" font-size="9" fill="#5E3A7E">Seis dimensoes da matriz africana no Maranhao</text>

  <!-- Centro: 78% -->
  <circle cx="250" cy="300" r="55" fill="#5E3A7E" opacity="0.08" stroke="#5E3A7E" stroke-width="2.5"/>
  <text x="250" y="292" text-anchor="middle" font-family="serif" font-size="36" font-weight="bold" fill="#5E3A7E">78%</text>
  <text x="250" y="312" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#2B2B2B">negra ou parda</text>
  <text x="250" y="322" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#5E3A7E">IBGE 2022</text>

  <!-- Hexagono 1: O SAGRADO (topo) -->
  <g transform="translate(250, 145)">
    <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" fill="#5E3A7E" fill-opacity="0.08" stroke="#5E3A7E" stroke-width="1.5"/>
    <text y="-18" text-anchor="middle" font-size="16">🕯</text>
    <text y="2" text-anchor="middle" font-family="serif" font-size="9" font-weight="bold" fill="#2B2B2B">O SAGRADO</text>
    <text y="14" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#5E3A7E">Tambor de Mina</text>
    <text y="24" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#2B2B2B">Terreiros desde ~1840</text>
  </g>

  <!-- Hexagono 2: O CORPO (superior direito) -->
  <g transform="translate(380, 220)">
    <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" fill="#5E3A7E" fill-opacity="0.08" stroke="#5E3A7E" stroke-width="1.5"/>
    <text y="-18" text-anchor="middle" font-size="16">💃</text>
    <text y="2" text-anchor="middle" font-family="serif" font-size="9" font-weight="bold" fill="#2B2B2B">O CORPO</text>
    <text y="14" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#5E3A7E">Tambor de Crioula</text>
    <text y="24" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#2B2B2B">Patrimonio IPHAN 2007</text>
  </g>

  <!-- Hexagono 3: O SOM (inferior direito) -->
  <g transform="translate(380, 380)">
    <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" fill="#5E3A7E" fill-opacity="0.08" stroke="#5E3A7E" stroke-width="1.5"/>
    <text y="-18" text-anchor="middle" font-size="16">🎵</text>
    <text y="2" text-anchor="middle" font-family="serif" font-size="9" font-weight="bold" fill="#2B2B2B">O SOM</text>
    <text y="14" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#5E3A7E">Reggae + Radiolas</text>
    <text y="24" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#2B2B2B">Unica Jamaica fora da Jamaica</text>
  </g>

  <!-- Hexagono 4: A TERRA (baixo) -->
  <g transform="translate(250, 455)">
    <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" fill="#5E3A7E" fill-opacity="0.08" stroke="#5E3A7E" stroke-width="1.5"/>
    <text y="-18" text-anchor="middle" font-size="16">🌍</text>
    <text y="2" text-anchor="middle" font-family="serif" font-size="9" font-weight="bold" fill="#2B2B2B">A TERRA</text>
    <text y="14" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#5E3A7E">653 quilombos</text>
    <text y="24" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#2B2B2B">Maior numero do Brasil</text>
  </g>

  <!-- Hexagono 5: A PALAVRA (inferior esquerdo) -->
  <g transform="translate(120, 380)">
    <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" fill="#5E3A7E" fill-opacity="0.08" stroke="#5E3A7E" stroke-width="1.5"/>
    <text y="-18" text-anchor="middle" font-size="16">📝</text>
    <text y="2" text-anchor="middle" font-family="serif" font-size="9" font-weight="bold" fill="#2B2B2B">A PALAVRA</text>
    <text y="14" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#5E3A7E">Lingua africana viva</text>
    <text y="24" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#2B2B2B">cuxa, quilombo, samba...</text>
  </g>

  <!-- Hexagono 6: A MESA (superior esquerdo) -->
  <g transform="translate(120, 220)">
    <polygon points="0,-50 43,-25 43,25 0,50 -43,25 -43,-25" fill="#5E3A7E" fill-opacity="0.08" stroke="#5E3A7E" stroke-width="1.5"/>
    <text y="-18" text-anchor="middle" font-size="16">🍚</text>
    <text y="2" text-anchor="middle" font-family="serif" font-size="9" font-weight="bold" fill="#2B2B2B">A MESA</text>
    <text y="14" text-anchor="middle" font-family="sans-serif" font-size="7" fill="#5E3A7E">Arroz de cuxa</text>
    <text y="24" text-anchor="middle" font-family="sans-serif" font-size="6" fill="#2B2B2B">Ingredientes 100% africanos</text>
  </g>

  <!-- Linhas conectoras ao centro -->
  <line x1="250" y1="195" x2="250" y2="245" stroke="#5E3A7E" stroke-width="0.8" opacity="0.3"/>
  <line x1="337" y1="220" x2="295" y2="270" stroke="#5E3A7E" stroke-width="0.8" opacity="0.3"/>
  <line x1="337" y1="380" x2="295" y2="330" stroke="#5E3A7E" stroke-width="0.8" opacity="0.3"/>
  <line x1="250" y1="405" x2="250" y2="355" stroke="#5E3A7E" stroke-width="0.8" opacity="0.3"/>
  <line x1="163" y1="380" x2="205" y2="330" stroke="#5E3A7E" stroke-width="0.8" opacity="0.3"/>
  <line x1="163" y1="220" x2="205" y2="270" stroke="#5E3A7E" stroke-width="0.8" opacity="0.3"/>

  <!-- Rodape -->
  <text x="250" y="540" text-anchor="middle" font-size="8" fill="#2B2B2B" font-style="italic">V39 — Matriz africana: a heranca viva</text>
  <text x="250" y="555" text-anchor="middle" font-size="7" fill="#5E3A7E">Fontes: IBGE 2022, IPHAN, Ferretti (1996), Silva (1995), Fundacao Palmares (2023)</text>
</svg>
```

## 3. Prompt para IA generativa

**Prompt**: "Editorial infographic mosaic with six hexagonal panels arranged in a ring around a central circle showing '78%'. Each hexagon represents a dimension of African heritage in Maranhao, Brazil: sacred rituals (candles, drums), dance (women in circle), music (giant speakers, reggae), food (green rice dish), language (words floating), land (quilombo map). Color palette: deep purple #5E3A7E as primary accent, cream background #FAF3E8, ochre #C8952E for icons, charcoal #2B2B2B for text. Style: elegant editorial design, geometric layout, serif typography for headers, clean and respectful — NOT folkloric or exotic. Inspired by National Geographic infographics and New York Times visual essays. No photographs, pure illustrated/diagrammatic style."

**Estilo**: Infografico editorial geometrico, mosaico hexagonal
**Referencia**: National Geographic infographics, NYT visual features, The Economist data viz
**NAO incluir**: fotografias, elementos folcloricos estereotipados, exotismo, clipart, emojis no design final

---

---
id: VIS-V39-B
verbete: V39
tipo: mapa
posicao: corpo
---

# Visual V39-B: Mapa dos quilombos do Maranhao

## 1. Briefing para designer

**O que e**: Mapa do estado do Maranhao mostrando a distribuicao das 653 comunidades quilombolas certificadas. Mapa esquematico (nao cartografico puro), com pontos representando comunidades, concentracao por mesorregiao, e dado comparativo com outros estados.

**Dados**:
- 653 comunidades quilombolas certificadas (Fundacao Palmares, 2023)
- Concentracao: litoral norte (Alcantara — 150+ comunidades), Baixada Maranhense, vale do Itapecuru
- Comparativo: MA = 653, BA = 597, MG = 310, PA = 253 (os 4 maiores)
- Destaque: Quilombo de Frechal (Mirinzal) — primeiro do Brasil com titulo coletivo (1992)
- Destaque: Quilombos de Alcantara — conflito com Centro de Lancamento de Foguetes

**Referencia de estilo**: Mapa tematico editorial, estilo Bloomberg / The Economist. Fundo limpo, pontos de tamanho proporcional, sem poluicao visual.

**Paleta**:
- Fundo: creme #FAF3E8
- Contorno do estado: carvao #2B2B2B
- Pontos quilombolas: roxo-tambor #5E3A7E
- Destaque Frechal: verde-mata #2D6A4F
- Destaque Alcantara: vermelho-bumba #C1292E
- Barra comparativa: terracota #B5533E

**Tamanho**: Meia pagina (coluna larga)

## 2. SVG simplificado

**Elementos**:
- Contorno esquematico do Maranhao
- Pontos (circulos pequenos) representando concentracao de quilombos
- 2 labels de destaque (Frechal e Alcantara)
- Barra comparativa lateral: MA vs BA vs MG vs PA

**Layout**: Mapa a esquerda (60%), barra comparativa a direita (40%)

**Cores**: roxo-tambor para pontos, carvao para contorno, terracota para barra

```svg
<svg viewBox="0 0 460 320" xmlns="http://www.w3.org/2000/svg">
  <rect width="460" height="320" fill="#FAF3E8"/>

  <!-- Titulo -->
  <text x="230" y="25" text-anchor="middle" font-family="serif" font-size="14" font-weight="bold" fill="#2B2B2B">653 QUILOMBOS</text>
  <text x="230" y="40" text-anchor="middle" font-family="sans-serif" font-size="8" fill="#5E3A7E">O Maranhao tem o maior numero de comunidades quilombolas do Brasil</text>

  <!-- Contorno esquematico do MA -->
  <path d="M 50 80 L 120 60 L 200 55 L 240 70 L 220 100 L 230 140 L 250 180 L 240 220 L 200 260 L 150 270 L 100 250 L 70 200 L 55 150 Z" fill="none" stroke="#2B2B2B" stroke-width="2"/>

  <!-- Pontos quilombolas (clusters) -->
  <!-- Alcantara / litoral norte — alta concentracao -->
  <circle cx="140" cy="80" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="150" cy="75" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="145" cy="85" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="155" cy="82" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="135" cy="78" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="148" cy="90" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="160" cy="88" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="130" cy="85" r="3" fill="#5E3A7E" opacity="0.7"/>

  <!-- Baixada maranhense -->
  <circle cx="100" cy="140" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="110" cy="145" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="95" cy="150" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="105" cy="155" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="115" cy="135" r="3" fill="#5E3A7E" opacity="0.7"/>

  <!-- Vale do Itapecuru -->
  <circle cx="175" cy="130" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="180" cy="140" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="190" cy="135" r="3" fill="#5E3A7E" opacity="0.7"/>
  <circle cx="185" cy="150" r="3" fill="#5E3A7E" opacity="0.7"/>

  <!-- Dispersos -->
  <circle cx="150" cy="180" r="2.5" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="130" cy="200" r="2.5" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="170" cy="210" r="2.5" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="200" cy="190" r="2.5" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="160" cy="230" r="2.5" fill="#5E3A7E" opacity="0.5"/>

  <!-- Label Alcantara -->
  <line x1="150" y1="70" x2="180" y2="55" stroke="#C1292E" stroke-width="0.8"/>
  <text x="182" y="53" font-size="7" fill="#C1292E" font-weight="bold">Alcantara</text>
  <text x="182" y="61" font-size="6" fill="#2B2B2B">150+ quilombos</text>

  <!-- Label Frechal -->
  <line x1="90" y1="130" x2="60" y2="115" stroke="#2D6A4F" stroke-width="0.8"/>
  <text x="30" y="113" font-size="7" fill="#2D6A4F" font-weight="bold">Frechal</text>
  <text x="20" y="121" font-size="6" fill="#2B2B2B">1o titulo coletivo (1992)</text>

  <!-- Barra comparativa -->
  <text x="360" y="80" text-anchor="middle" font-family="serif" font-size="10" font-weight="bold" fill="#2B2B2B">Ranking</text>

  <!-- MA -->
  <rect x="300" y="95" width="120" height="18" fill="#5E3A7E" rx="2"/>
  <text x="305" y="108" font-size="8" fill="#FAF3E8" font-weight="bold">MA — 653</text>

  <!-- BA -->
  <rect x="300" y="120" width="110" height="18" fill="#B5533E" rx="2"/>
  <text x="305" y="133" font-size="8" fill="#FAF3E8" font-weight="bold">BA — 597</text>

  <!-- MG -->
  <rect x="300" y="145" width="57" height="18" fill="#B5533E" opacity="0.7" rx="2"/>
  <text x="305" y="158" font-size="8" fill="#FAF3E8" font-weight="bold">MG — 310</text>

  <!-- PA -->
  <rect x="300" y="170" width="46" height="18" fill="#B5533E" opacity="0.5" rx="2"/>
  <text x="305" y="183" font-size="8" fill="#FAF3E8" font-weight="bold">PA — 253</text>

  <text x="360" y="205" text-anchor="middle" font-size="7" fill="#2B2B2B" font-style="italic">Fundacao Palmares, 2023</text>

  <!-- Rodape -->
  <text x="230" y="300" text-anchor="middle" font-size="7" fill="#2B2B2B" font-style="italic">Cada ponto representa um cluster de comunidades certificadas</text>
</svg>
```

## 3. Prompt para IA generativa

**Prompt**: "Thematic map of Maranhao state, Brazil, showing distribution of 653 quilombo (maroon) communities. Schematic/editorial style map with dot clusters concentrated along the northern coast (Alcantara region), the Baixada Maranhense lowlands, and the Itapecuru river valley. Two highlighted locations: Alcantara (red, 150+ quilombos) and Frechal (green, first collective land title 1992). Side bar chart comparing quilombo counts: Maranhao 653, Bahia 597, Minas Gerais 310, Para 253. Color palette: deep purple #5E3A7E for quilombo dots, cream background #FAF3E8, charcoal outline #2B2B2B, terracotta #B5533E for comparison bars. Style: Bloomberg / The Economist data visualization, clean, minimal, no decorative elements."

**Estilo**: Mapa tematico editorial, data visualization
**Referencia**: Bloomberg, The Economist, NYT maps
**NAO incluir**: satelite, Google Maps, decoracoes, molduras ornamentais
