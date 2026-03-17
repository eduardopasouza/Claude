---
id: VIS-V67-A
verbete: V67
tipo: mapa
posicao: página-inteira
---

# Visual V67-A: Mapa sonoro — cinco regiões, cinco sotaques

## 1. Briefing para designer
**O que é**: Mapa ilustrado do Maranhão mostrando a origem geográfica de cada sotaque do bumba-meu-boi, com regiões codificadas por cor e ícones dos instrumentos-chave. Página inteira — visual principal do verbete.
**Dados**:
- MATRACA = Ilha de São Luís (azul, #1A3A5C): ícone de duas tábuas de madeira cruzadas + pandeirão. 100+ grupos. Matriz indígena + africana.
- ZABUMBA = Guimarães, litoral ocidental (vermelho, #C45A3C): ícone de tambor de duas peles com baqueta. 30-40 grupos. Matriz africana.
- ORQUESTRA = Rosário / Axixá (dourado, #D4AC0D): ícone de saxofone. 50-60 grupos. Matriz europeia + africana.
- BAIXADA = Baixada Maranhense / Pindaré (verde, #2D5A27): ícone de tambor-onça com vareta + máscara de cazumbá. 40-50 grupos. Matriz africana + indígena.
- COSTA-DE-MÃO = Cururupu, litoral das Reentrâncias (preto, #1C1C1C): ícone de mão com dorso marcado sobre pandeiro. 8 grupos. Risco crítico. Matriz africana.
- Total: 450+ grupos em todo o Maranhão
- Setas conectando cada região ao nome do sotaque e seu instrumento
- Litoral e rios como referência geográfica
**Referência de estilo**: Mapa ilustrado editorial tipo DK (Dorling Kindersley) — regiões coloridas, ícones desenhados à mão, legendas limpas
**Paleta**: Azul-mar (#1A3A5C), Terracota (#C45A3C), Dourado-babaçu (#D4AC0D), Verde-mangue (#2D5A27), Preto-mangue (#1C1C1C), Branco/creme para fundo
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Silhueta do Maranhão com divisões regionais
- 5 zonas coloridas correspondendo a cada sotaque
- Ícones de instrumentos posicionados sobre cada região
- Legendas com nome do sotaque, n.º de grupos e nível de risco
- Escala de risco visual: barras ou sinalizadores (verde/amarelo/vermelho/preto)
**Layout**: Mapa central, legendas nas margens

```svg
<svg viewBox="0 0 650 550" xmlns="http://www.w3.org/2000/svg">
  <!-- Título -->
  <text x="325" y="30" text-anchor="middle" fill="#333" font-size="16" font-weight="bold">MAPA SONORO DO BUMBA-MEU-BOI</text>
  <text x="325" y="50" text-anchor="middle" fill="#666" font-size="11">Cinco regiões, cinco sotaques, 450+ grupos</text>

  <!-- Silhueta simplificada do Maranhão -->
  <path d="M150,120 L280,100 L400,110 L480,130 L520,180 L500,260 L480,340 L450,400 L380,430 L300,440 L220,420 L160,380 L130,300 L120,220 L130,160 Z" fill="#F5F0E6" stroke="#999" stroke-width="1.5"/>

  <!-- Região: Ilha de São Luís — Matraca (azul) -->
  <circle cx="370" cy="145" r="30" fill="#1A3A5C" opacity="0.7"/>
  <text x="370" y="142" text-anchor="middle" fill="#FFF" font-size="8" font-weight="bold">MATRACA</text>
  <text x="370" y="154" text-anchor="middle" fill="#CCC" font-size="7">Ilha de São Luís</text>
  <!-- Ícone: matracas -->
  <rect x="360" y="160" width="4" height="16" fill="#1A3A5C" transform="rotate(-15,362,168)"/>
  <rect x="368" y="160" width="4" height="16" fill="#1A3A5C" transform="rotate(15,370,168)"/>

  <!-- Legenda Matraca -->
  <line x1="400" y1="145" x2="530" y2="90" stroke="#1A3A5C" stroke-width="1"/>
  <text x="535" y="85" fill="#1A3A5C" font-size="10" font-weight="bold">MATRACA</text>
  <text x="535" y="98" fill="#666" font-size="9">100+ grupos | Risco: baixo</text>
  <text x="535" y="111" fill="#888" font-size="8">Indígena + africana</text>
  <rect x="535" y="114" width="50" height="4" rx="2" fill="#2D5A27"/>

  <!-- Região: Guimarães — Zabumba (vermelho) -->
  <circle cx="220" cy="180" r="28" fill="#C45A3C" opacity="0.7"/>
  <text x="220" y="178" text-anchor="middle" fill="#FFF" font-size="8" font-weight="bold">ZABUMBA</text>
  <text x="220" y="190" text-anchor="middle" fill="#FDD" font-size="7">Guimarães</text>
  <!-- Ícone: tambor -->
  <ellipse cx="220" cy="205" rx="8" ry="5" fill="none" stroke="#C45A3C" stroke-width="1.5"/>
  <line x1="212" y1="205" x2="212" y2="218" stroke="#C45A3C" stroke-width="1.5"/>
  <line x1="228" y1="205" x2="228" y2="218" stroke="#C45A3C" stroke-width="1.5"/>
  <ellipse cx="220" cy="218" rx="8" ry="5" fill="none" stroke="#C45A3C" stroke-width="1.5"/>

  <!-- Legenda Zabumba -->
  <line x1="192" y1="180" x2="50" y2="140" stroke="#C45A3C" stroke-width="1"/>
  <text x="5" y="135" fill="#C45A3C" font-size="10" font-weight="bold">ZABUMBA</text>
  <text x="5" y="148" fill="#666" font-size="9">30-40 grupos | Risco: alto</text>
  <text x="5" y="161" fill="#888" font-size="8">Africana</text>
  <rect x="5" y="164" width="50" height="4" rx="2" fill="#C45A3C"/>

  <!-- Região: Rosário/Axixá — Orquestra (dourado) -->
  <circle cx="330" cy="220" r="28" fill="#D4AC0D" opacity="0.7"/>
  <text x="330" y="218" text-anchor="middle" fill="#333" font-size="8" font-weight="bold">ORQUESTRA</text>
  <text x="330" y="230" text-anchor="middle" fill="#555" font-size="7">Rosário / Axixá</text>
  <!-- Ícone: saxofone simplificado -->
  <path d="M325,240 Q330,248 335,240 L340,255 Q335,260 325,258 Z" fill="none" stroke="#D4AC0D" stroke-width="1.5"/>

  <!-- Legenda Orquestra -->
  <line x1="358" y1="220" x2="530" y2="200" stroke="#D4AC0D" stroke-width="1"/>
  <text x="535" y="195" fill="#D4AC0D" font-size="10" font-weight="bold">ORQUESTRA</text>
  <text x="535" y="208" fill="#666" font-size="9">50-60 grupos | Risco: baixo</text>
  <text x="535" y="221" fill="#888" font-size="8">Europeia + africana (em expansão)</text>
  <rect x="535" y="224" width="50" height="4" rx="2" fill="#2D5A27"/>

  <!-- Região: Baixada/Pindaré — Baixada (verde) -->
  <circle cx="240" cy="320" r="32" fill="#2D5A27" opacity="0.7"/>
  <text x="240" y="318" text-anchor="middle" fill="#FFF" font-size="8" font-weight="bold">BAIXADA</text>
  <text x="240" y="330" text-anchor="middle" fill="#CFC" font-size="7">Pindaré</text>
  <!-- Ícone: máscara cazumbá -->
  <ellipse cx="240" cy="345" rx="7" ry="9" fill="none" stroke="#2D5A27" stroke-width="1.5"/>
  <circle cx="236" cy="343" r="2" fill="#2D5A27"/>
  <circle cx="244" cy="343" r="2" fill="#2D5A27"/>

  <!-- Legenda Baixada -->
  <line x1="208" y1="320" x2="50" y2="310" stroke="#2D5A27" stroke-width="1"/>
  <text x="5" y="305" fill="#2D5A27" font-size="10" font-weight="bold">BAIXADA</text>
  <text x="5" y="318" fill="#666" font-size="9">40-50 grupos | Risco: médio</text>
  <text x="5" y="331" fill="#888" font-size="8">Africana + indígena</text>
  <rect x="5" y="334" width="50" height="4" rx="2" fill="#D4AC0D"/>

  <!-- Região: Cururupu — Costa-de-mão (preto) -->
  <circle cx="280" cy="140" r="22" fill="#1C1C1C" opacity="0.85"/>
  <text x="280" y="136" text-anchor="middle" fill="#FFF" font-size="7" font-weight="bold">COSTA-</text>
  <text x="280" y="146" text-anchor="middle" fill="#FFF" font-size="7" font-weight="bold">DE-MÃO</text>
  <text x="280" y="156" text-anchor="middle" fill="#CCC" font-size="6">Cururupu</text>

  <!-- Legenda Costa-de-mão -->
  <line x1="258" y1="140" x2="50" y2="230" stroke="#1C1C1C" stroke-width="1"/>
  <text x="5" y="225" fill="#1C1C1C" font-size="10" font-weight="bold">COSTA-DE-MÃO</text>
  <text x="5" y="238" fill="#C0392B" font-size="9" font-weight="bold">8 grupos | Risco: CRÍTICO</text>
  <text x="5" y="251" fill="#888" font-size="8">Africana</text>
  <rect x="5" y="254" width="50" height="4" rx="2" fill="#1C1C1C"/>

  <!-- Oceano Atlântico -->
  <text x="440" y="120" fill="#1A3A5C" font-size="9" font-style="italic" opacity="0.5">Oceano Atlântico</text>

  <!-- Legenda geral -->
  <rect x="140" y="470" width="370" height="55" rx="6" fill="#F5F0E6" stroke="#CCC" stroke-width="0.5"/>
  <text x="325" y="488" text-anchor="middle" fill="#333" font-size="10" font-weight="bold">ESCALA DE RISCO</text>
  <rect x="170" y="498" width="12" height="12" rx="2" fill="#2D5A27"/>
  <text x="188" y="508" fill="#666" font-size="9">Baixo</text>
  <rect x="240" y="498" width="12" height="12" rx="2" fill="#D4AC0D"/>
  <text x="258" y="508" fill="#666" font-size="9">Médio</text>
  <rect x="310" y="498" width="12" height="12" rx="2" fill="#C45A3C"/>
  <text x="328" y="508" fill="#666" font-size="9">Alto</text>
  <rect x="380" y="498" width="12" height="12" rx="2" fill="#1C1C1C"/>
  <text x="398" y="508" fill="#666" font-size="9">Crítico</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Illustrated editorial map of the Brazilian state of Maranhão showing the geographic origins of five bumba-meu-boi musical styles (sotaques). The map has a cream/parchment background with the state silhouette clearly defined. Five color-coded regions: (1) Ilha de São Luís in deep blue with an icon of two wooden clappers (matracas), (2) Guimarães on the western coast in terracotta red with a double-headed drum icon, (3) Rosário/Axixá inland in gold with a saxophone icon, (4) Baixada Maranhense lowlands in forest green with a friction drum and a carved wooden mask (cazumbá) icon, (5) Cururupu on the northern coast in black with an icon of a hand playing a drum with the back of the hand. Each region has a label with the sotaque name, number of active groups, and risk level. Rivers and coastline visible for geographic reference. Style: DK (Dorling Kindersley) illustrated map — hand-drawn instrument icons, clean typography, warm editorial palette. No text — labels will be added in Portuguese."
**Estilo**: Mapa ilustrado editorial (DK / Dorling Kindersley)
**NÃO incluir**: Texto definitivo, molduras decorativas excessivas

---

---
id: VIS-V67-B
verbete: V67
tipo: infográfico
posicao: meia-página
---

# Visual V67-B: Os 5 sotaques lado a lado — instrumentos, números, risco

## 1. Briefing para designer
**O que é**: Infográfico comparativo dos cinco sotaques em formato "tier" — colunas lado a lado com altura proporcional ao número de grupos, mostrando para cada um: instrumentos-chave, número de grupos, nível de risco e matriz cultural (indígena/africana/europeia). Meia página.
**Dados**:

| Sotaque | Instrumento-chave | Nº de grupos | Risco | Matriz |
|---|---|---|---|---|
| Matraca | Matraca + pandeirão | 100+ | Baixo | Indígena + africana |
| Orquestra | Saxofone + sopros | 50-60 | Baixo (cresce) | Europeia + africana |
| Baixada | Pandeiro + tambor-onça | 40-50 | Médio | Africana + indígena |
| Zabumba | Zabumba (duas peles) | 30-40 | Alto | Africana |
| Costa-de-mão | Pandeiro (dorso) | 8 | Crítico | Africana |

- Barras ou colunas de altura proporcional ao nº de grupos
- Ícone de instrumento no topo de cada coluna
- Faixa de cor indicando risco na base
- Barra de matriz cultural tricolor (indígena/africana/europeia) por sotaque
- Destaque visual para costa-de-mão: coluna mínima, cor preta, sinal de alerta
**Referência de estilo**: The Pudding — infográfico comparativo limpo, minimalista, com dados empilhados e hierarquia visual clara
**Paleta**: Azul-mar (#1A3A5C), Terracota (#C45A3C), Dourado-babaçu (#D4AC0D), Verde-mangue (#2D5A27), Preto-mangue (#1C1C1C)
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**:
- 5 colunas de barras com altura proporcional (Matraca: 100, Orquestra: 55, Baixada: 45, Zabumba: 35, Costa-de-mão: 8)
- Ícones de instrumentos sobre cada barra
- Faixa de risco colorida na base de cada coluna
- Barras de matriz cultural empilhadas (tricolor)
- Label com nome e número de grupos
**Layout**: Horizontal, 5 colunas equidistantes

```svg
<svg viewBox="0 0 600 420" xmlns="http://www.w3.org/2000/svg">
  <!-- Título -->
  <text x="300" y="25" text-anchor="middle" fill="#333" font-size="14" font-weight="bold">OS 5 SOTAQUES — COMPARATIVO</text>
  <text x="300" y="42" text-anchor="middle" fill="#666" font-size="10">Instrumentos, número de grupos e nível de risco</text>

  <!-- Eixo base -->
  <line x1="50" y1="340" x2="560" y2="340" stroke="#CCC" stroke-width="1"/>

  <!-- Escala: max = 100 grupos → 240px de altura. 1 grupo ≈ 2.4px -->
  <!-- Matraca: 100+ → 240px -->
  <rect x="65" y="100" width="70" height="240" rx="4" fill="#1A3A5C" opacity="0.85"/>
  <text x="100" y="90" text-anchor="middle" fill="#1A3A5C" font-size="11" font-weight="bold">MATRACA</text>
  <text x="100" y="130" text-anchor="middle" fill="#FFF" font-size="20" font-weight="bold">100+</text>
  <text x="100" y="148" text-anchor="middle" fill="#AAC" font-size="9">grupos</text>
  <text x="100" y="310" text-anchor="middle" fill="#FFF" font-size="8">Matraca</text>
  <text x="100" y="322" text-anchor="middle" fill="#FFF" font-size="8">+ pandeirão</text>
  <!-- Risco: baixo -->
  <rect x="65" y="342" width="70" height="8" rx="2" fill="#2D5A27"/>
  <text x="100" y="362" text-anchor="middle" fill="#2D5A27" font-size="8">BAIXO</text>

  <!-- Orquestra: 55 → 132px -->
  <rect x="165" y="208" width="70" height="132" rx="4" fill="#D4AC0D" opacity="0.85"/>
  <text x="200" y="198" text-anchor="middle" fill="#D4AC0D" font-size="11" font-weight="bold">ORQUESTRA</text>
  <text x="200" y="245" text-anchor="middle" fill="#333" font-size="20" font-weight="bold">55</text>
  <text x="200" y="263" text-anchor="middle" fill="#665" font-size="9">grupos</text>
  <text x="200" y="322" text-anchor="middle" fill="#333" font-size="8">Saxofone</text>
  <!-- Risco: baixo (cresce) -->
  <rect x="165" y="342" width="70" height="8" rx="2" fill="#2D5A27"/>
  <text x="200" y="362" text-anchor="middle" fill="#2D5A27" font-size="8">BAIXO ↑</text>

  <!-- Baixada: 45 → 108px -->
  <rect x="265" y="232" width="70" height="108" rx="4" fill="#2D5A27" opacity="0.85"/>
  <text x="300" y="222" text-anchor="middle" fill="#2D5A27" font-size="11" font-weight="bold">BAIXADA</text>
  <text x="300" y="270" text-anchor="middle" fill="#FFF" font-size="20" font-weight="bold">45</text>
  <text x="300" y="288" text-anchor="middle" fill="#CFC" font-size="9">grupos</text>
  <text x="300" y="322" text-anchor="middle" fill="#FFF" font-size="8">Tambor-onça</text>
  <!-- Risco: médio -->
  <rect x="265" y="342" width="70" height="8" rx="2" fill="#D4AC0D"/>
  <text x="300" y="362" text-anchor="middle" fill="#D4AC0D" font-size="8">MÉDIO</text>

  <!-- Zabumba: 35 → 84px -->
  <rect x="365" y="256" width="70" height="84" rx="4" fill="#C45A3C" opacity="0.85"/>
  <text x="400" y="246" text-anchor="middle" fill="#C45A3C" font-size="11" font-weight="bold">ZABUMBA</text>
  <text x="400" y="290" text-anchor="middle" fill="#FFF" font-size="20" font-weight="bold">35</text>
  <text x="400" y="308" text-anchor="middle" fill="#FDD" font-size="9">grupos</text>
  <text x="400" y="322" text-anchor="middle" fill="#FFF" font-size="8">Zabumba</text>
  <!-- Risco: alto -->
  <rect x="365" y="342" width="70" height="8" rx="2" fill="#C45A3C"/>
  <text x="400" y="362" text-anchor="middle" fill="#C45A3C" font-size="8">ALTO</text>

  <!-- Costa-de-mão: 8 → 19px -->
  <rect x="465" y="321" width="70" height="19" rx="4" fill="#1C1C1C" opacity="0.9"/>
  <text x="500" y="311" text-anchor="middle" fill="#1C1C1C" font-size="11" font-weight="bold">COSTA-DE-MÃO</text>
  <text x="500" y="335" text-anchor="middle" fill="#FFF" font-size="11" font-weight="bold">8</text>
  <!-- Risco: crítico -->
  <rect x="465" y="342" width="70" height="8" rx="2" fill="#1C1C1C"/>
  <text x="500" y="362" text-anchor="middle" fill="#C0392B" font-size="8" font-weight="bold">CRÍTICO ⚠</text>

  <!-- Matriz cultural — barras tricolores -->
  <text x="300" y="390" text-anchor="middle" fill="#333" font-size="10" font-weight="bold">MATRIZ CULTURAL</text>

  <!-- Legenda matriz -->
  <rect x="140" y="400" width="10" height="10" fill="#C45A3C"/>
  <text x="155" y="409" fill="#666" font-size="8">Indígena</text>
  <rect x="220" y="400" width="10" height="10" fill="#1C1C1C"/>
  <text x="235" y="409" fill="#666" font-size="8">Africana</text>
  <rect x="310" y="400" width="10" height="10" fill="#D4AC0D"/>
  <text x="325" y="409" fill="#666" font-size="8">Europeia</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Clean comparative infographic showing five columns representing the five sotaques (musical styles) of Brazilian bumba-meu-boi from Maranhão. Each column is a vertical bar with height proportional to the number of active groups: Matraca (100+, tallest, deep blue), Orquestra (55, gold), Baixada (45, forest green), Zabumba (35, terracotta red), Costa-de-mão (8, dramatically small, black). At the top of each bar, a minimalist icon of the key instrument: wooden clappers, saxophone, friction drum, double-headed drum, hand hitting drum with back of hand. At the base, a color-coded risk indicator strip: green (low), yellow (medium), red (high), black (critical). Below each column, a small stacked horizontal bar showing cultural matrix proportions: indigenous (warm red), African (black), European (gold). Minimalist data visualization style inspired by The Pudding — clean lines, generous white space, clear hierarchy. No text — labels will be added in Portuguese."
**Estilo**: Infográfico comparativo editorial (The Pudding)
**NÃO incluir**: Texto definitivo, elementos decorativos, fotografias
