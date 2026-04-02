---
id: VIS-V10-A
verbete: V10
tipo: infográfico
posicao: página-inteira
---

# Visual V10-A: Turismo vs. Saneamento — o paradoxo em números

## 1. Briefing para designer
**O que é**: Infográfico de página inteira justapondo dois conjuntos de dados: o crescimento exponencial de visitantes no PNLM (2019-2025) e a precariedade do saneamento em Barreirinhas. Dois gráficos lado a lado — um subindo (turismo), outro estagnado (infraestrutura). A tensão visual entre os dois conta a história.
**Dados**:
- Gráfico de barras — Visitantes/ano:
  - 2019: 141.000
  - 2020: ~50.000 (pandemia)
  - 2021: ~120.000
  - 2022: ~250.000
  - 2023: ~350.000
  - 2024: 440.000 (selo UNESCO em julho)
  - 2025: 656.388 (recorde)
- Gráfico de barras / waffle chart — Saneamento de Barreirinhas (64 mil hab.):
  - 60% fossas rudimentares
  - 33% outros sistemas precários
  - 7% rede de esgoto
- Linha conectora visual: seta mostrando "esgoto → solo → lençol freático → lagoas"
- Dado de comparação: Fernando de Noronha — R$179/dia de taxa; Lençóis — R$0
- Marco: estrela/ícone UNESCO em 2024 na linha temporal
**Referência de estilo**: The Pudding / Vox — data storytelling visual, gráficos limpos com forte impacto narrativo. Contraste entre a beleza dos números de crescimento e a crueza dos números de saneamento.
**Paleta**: Azul-mar (#1B4F72) para dados de turismo/água, Terracota (#BA4A00) para dados de saneamento/ameaça, Branco-areia (#F5F5DC) para fundo
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Metade esquerda: gráfico de barras vertical (2019-2025), barras em azul, crescendo da esquerda para a direita, ícone UNESCO sobre a barra de 2024
- Metade direita: waffle chart ou barras horizontais mostrando 60% fossas / 33% precário / 7% rede, em tons de terracota
- Entre os dois gráficos: seta pontilhada conectando "656 mil visitantes" a "7% de rede de esgoto"
- Rodapé: barra comparativa Galápagos (US$100) / Noronha (R$179/dia) / Lençóis (R$0)
**Layout**: Horizontal, dois painéis lado a lado, leitura da esquerda para a direita
**Cores**: Azul (#1B4F72) turismo, Terracota (#BA4A00) saneamento, Branco (#F5F5DC) fundo

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect x="0" y="0" width="800" height="500" fill="#F5F5DC"/>

  <!-- Título -->
  <text x="400" y="35" text-anchor="middle" fill="#1B4F72" font-size="18" font-weight="bold">TURISMO × SANEAMENTO — O PARADOXO EM NÚMEROS</text>

  <!-- PAINEL ESQUERDO: Gráfico de barras — Visitantes -->
  <text x="200" y="65" text-anchor="middle" fill="#1B4F72" font-size="13" font-weight="bold">Visitantes/ano no PNLM</text>

  <!-- Barras (base y=400, escala: 1k = 0.5px) -->
  <rect x="55"  y="329" width="35" height="71"  fill="#1B4F72" opacity="0.7"/>
  <text x="72"  y="325" text-anchor="middle" fill="#1B4F72" font-size="9">141k</text>
  <text x="72"  y="415" text-anchor="middle" fill="#1B4F72" font-size="9">2019</text>

  <rect x="100" y="375" width="35" height="25"  fill="#1B4F72" opacity="0.4"/>
  <text x="117" y="371" text-anchor="middle" fill="#999" font-size="8">~50k</text>
  <text x="117" y="415" text-anchor="middle" fill="#1B4F72" font-size="9">2020</text>

  <rect x="145" y="340" width="35" height="60"  fill="#1B4F72" opacity="0.5"/>
  <text x="162" y="336" text-anchor="middle" fill="#1B4F72" font-size="9">~120k</text>
  <text x="162" y="415" text-anchor="middle" fill="#1B4F72" font-size="9">2021</text>

  <rect x="190" y="275" width="35" height="125" fill="#1B4F72" opacity="0.6"/>
  <text x="207" y="271" text-anchor="middle" fill="#1B4F72" font-size="9">~250k</text>
  <text x="207" y="415" text-anchor="middle" fill="#1B4F72" font-size="9">2022</text>

  <rect x="235" y="225" width="35" height="175" fill="#1B4F72" opacity="0.7"/>
  <text x="252" y="221" text-anchor="middle" fill="#1B4F72" font-size="9">~350k</text>
  <text x="252" y="415" text-anchor="middle" fill="#1B4F72" font-size="9">2023</text>

  <rect x="280" y="180" width="35" height="220" fill="#1B4F72" opacity="0.85"/>
  <text x="297" y="176" text-anchor="middle" fill="#1B4F72" font-size="9">440k</text>
  <text x="297" y="415" text-anchor="middle" fill="#1B4F72" font-size="9">2024</text>
  <!-- Ícone UNESCO -->
  <text x="297" y="164" text-anchor="middle" fill="#D4AC0D" font-size="12">★ UNESCO</text>

  <rect x="325" y="72"  width="35" height="328" fill="#1B4F72"/>
  <text x="342" y="67"  text-anchor="middle" fill="#1B4F72" font-size="10" font-weight="bold">656k</text>
  <text x="342" y="415" text-anchor="middle" fill="#1B4F72" font-size="9" font-weight="bold">2025</text>

  <!-- Linha de base -->
  <line x1="45" y1="400" x2="370" y2="400" stroke="#1B4F72" stroke-width="1"/>

  <!-- Seta conectora central -->
  <line x1="400" y1="150" x2="400" y2="350" stroke="#BA4A00" stroke-width="1.5" stroke-dasharray="6,4"/>
  <text x="400" y="240" text-anchor="middle" fill="#BA4A00" font-size="10" font-weight="bold" transform="rotate(-90,400,240)">esgoto → solo → lençol → lagoas</text>

  <!-- PAINEL DIREITO: Saneamento de Barreirinhas -->
  <text x="610" y="65" text-anchor="middle" fill="#BA4A00" font-size="13" font-weight="bold">Saneamento em Barreirinhas</text>
  <text x="610" y="82" text-anchor="middle" fill="#BA4A00" font-size="10">(64 mil habitantes)</text>

  <!-- Barras horizontais -->
  <rect x="470" y="110" width="270" height="50" fill="#BA4A00" opacity="0.85"/>
  <text x="605" y="140" text-anchor="middle" fill="white" font-size="13" font-weight="bold">60% — FOSSAS RUDIMENTARES</text>

  <rect x="470" y="175" width="148" height="50" fill="#BA4A00" opacity="0.55"/>
  <text x="544" y="205" text-anchor="middle" fill="white" font-size="12" font-weight="bold">33% — outros precários</text>

  <rect x="470" y="240" width="32" height="50" fill="#BA4A00" opacity="0.3"/>
  <text x="540" y="270" text-anchor="start" fill="#BA4A00" font-size="12" font-weight="bold">7% — rede de esgoto</text>

  <!-- Comparativo de taxas -->
  <rect x="440" y="340" width="330" height="80" fill="white" stroke="#1B4F72" stroke-width="1" rx="8"/>
  <text x="605" y="362" text-anchor="middle" fill="#1B4F72" font-size="11" font-weight="bold">TAXA DE PRESERVAÇÃO</text>
  <text x="605" y="382" text-anchor="middle" fill="#1B4F72" font-size="10">Galápagos: US$ 100 + limite diário</text>
  <text x="605" y="398" text-anchor="middle" fill="#1B4F72" font-size="10">Fernando de Noronha: R$ 179/dia</text>
  <text x="605" y="414" text-anchor="middle" fill="#BA4A00" font-size="11" font-weight="bold">Lençóis Maranhenses: R$ 0</text>

  <!-- Rodapé -->
  <text x="400" y="475" text-anchor="middle" fill="#888" font-size="9">Fontes: ICMBio (2025); Rádio Timbira (2025); Portal do Holanda (2025); UNESCO WHC (2024)</text>
  <text x="400" y="490" text-anchor="middle" fill="#888" font-size="8">Quem é o Maranhão? — V10</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Data visualization infographic comparing two datasets side by side. Left panel: vertical bar chart showing visitor growth at Lençóis Maranhenses National Park from 2019 to 2025 (141k to 656k), with a UNESCO star icon marking 2024. Bars in deep ocean blue, growing dramatically. Right panel: horizontal bar chart showing sanitation in Barreirinhas, Brazil — 60% rudimentary cesspits (large terracotta bar), 33% precarious systems (medium bar), 7% sewage network (tiny bar). A dashed arrow between the two panels shows the connection: sewage goes into the same water table that feeds the lagoons. Bottom: comparison box showing preservation fees — Galápagos US$100, Fernando de Noronha R$179/day, Lençóis R$0. Clean data storytelling style like The Pudding or Vox. Color palette: deep blue (#1B4F72) for tourism data, terracotta (#BA4A00) for sanitation data, sand white (#F5F5DC) background. Professional editorial infographic, high contrast, impactful."
**Estilo**: Data storytelling editorial (The Pudding / Vox / Our World in Data)
**Referência**: Infográficos de contraste — onde a beleza dos números esconde um problema
**NÃO incluir**: Fotos realistas, pessoas, texto em inglês (o texto será adicionado em português pelo designer)

---

---
id: VIS-V10-B
verbete: V10
tipo: mapa
posicao: meia-página
---

# Visual V10-B: Mapa de ameaças — o que cerca os Lençóis

## 1. Briefing para designer
**O que é**: Mapa editorial do Parque Nacional dos Lençóis Maranhenses mostrando os limites do parque, comunidades internas, pontos de entrada e ícones de ameaças. Meia página. Estilo cartográfico DK (Dorling Kindersley) — limpo, informativo, com ícones simbólicos.
**Dados**:
- Limite do parque: polígono 155.000 ha (Decreto 86.060/1981), costa norte (Oceano Atlântico)
- Comunidades internas:
  - Queimada dos Britos (centro do campo de dunas) — ícone de oásis/comunidade
  - Outras 16 comunidades distribuídas (indicar com pontos menores)
- Pontos de referência:
  - Barreirinhas (sul, principal entrada) — ícone de porta de entrada
  - Atins (leste, foz do Rio Preguiças) — ícone de kitesurfe/vila
  - Santo Amaro do Maranhão (oeste)
  - Primeira Cruz (sudoeste)
- Ameaças (ícones distribuídos):
  - 🏭 Poços de petróleo abandonados (~60, zona de amortecimento sul/sudoeste)
  - 💨 Parques eólicos (costa vizinha, faixa leste e oeste)
  - 🚗 Turismo desordenado (ícone de toyotas/multidão, entrada Barreirinhas e Atins)
  - 🚽 Esgoto sem tratamento (ícone em Barreirinhas)
- Rios: Preguiças (leste), Negro (oeste), Periá (centro)
- Oceano Atlântico ao norte
- São Luís (referência, ~260 km a oeste)
**Referência de estilo**: Mapa editorial DK — fundo claro, contornos limpos, ícones simbólicos coloridos, legendas com dados, sem grid de coordenadas
**Paleta**: Branco-areia (#F5F5DC) para dunas, Azul-mar (#1B4F72) para oceano/rios/lagoas, Terracota (#BA4A00) para ameaças e comunidades, Verde-mangue (#1E8449) para vegetação de restinga/mangue
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**:
- Retângulo superior: Oceano Atlântico (azul escuro)
- Polígono central: área do parque (branco-areia com textura de dunas)
- Pontos de comunidade: Queimada dos Britos (centro, ícone maior, terracota), demais comunidades (pontos menores)
- Cidades externas: Barreirinhas (sul), Atins (leste), Santo Amaro (oeste)
- Rios: linhas azuis finas
- Ícones de ameaça distribuídos nas posições correspondentes
- Legenda no canto inferior direito
**Layout**: Orientado ao norte (oceano no topo), leitura de mapa convencional

```svg
<svg viewBox="0 0 600 450" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect x="0" y="0" width="600" height="450" fill="#E8E4D4"/>

  <!-- Oceano Atlântico -->
  <rect x="0" y="0" width="600" height="100" fill="#1B4F72" opacity="0.8"/>
  <text x="300" y="50" text-anchor="middle" fill="white" font-size="14" font-weight="bold">OCEANO ATLÂNTICO</text>

  <!-- Limite do parque -->
  <polygon points="80,100 520,100 540,160 500,260 420,280 180,280 60,240 50,160"
           fill="#F5F5DC" stroke="#1B4F72" stroke-width="2" stroke-dasharray="8,4"/>
  <text x="300" y="135" text-anchor="middle" fill="#1B4F72" font-size="10" font-style="italic">PARQUE NACIONAL DOS LENÇÓIS MARANHENSES — 155.000 ha</text>

  <!-- Rios -->
  <path d="M480,100 Q470,180 460,280 L455,340" fill="none" stroke="#1B4F72" stroke-width="2"/>
  <text x="488" y="200" fill="#1B4F72" font-size="9" transform="rotate(10,488,200)">Rio Preguiças</text>

  <path d="M120,100 Q130,170 140,260 L145,320" fill="none" stroke="#1B4F72" stroke-width="2"/>
  <text x="105" y="200" fill="#1B4F72" font-size="9" transform="rotate(-5,105,200)">Rio Negro</text>

  <!-- Queimada dos Britos (centro) -->
  <circle cx="290" cy="195" r="10" fill="#BA4A00" stroke="white" stroke-width="2"/>
  <text x="290" y="220" text-anchor="middle" fill="#BA4A00" font-size="10" font-weight="bold">QUEIMADA DOS BRITOS</text>
  <text x="290" y="232" text-anchor="middle" fill="#BA4A00" font-size="8">(oásis — ~110 anos)</text>

  <!-- Outras comunidades (pontos menores) -->
  <circle cx="220" cy="180" r="4" fill="#BA4A00" opacity="0.6"/>
  <circle cx="350" cy="175" r="4" fill="#BA4A00" opacity="0.6"/>
  <circle cx="200" cy="220" r="4" fill="#BA4A00" opacity="0.6"/>
  <circle cx="380" cy="210" r="4" fill="#BA4A00" opacity="0.6"/>
  <circle cx="260" cy="250" r="4" fill="#BA4A00" opacity="0.6"/>
  <circle cx="340" cy="250" r="4" fill="#BA4A00" opacity="0.6"/>

  <!-- Barreirinhas (entrada sul) -->
  <rect x="370" y="320" width="12" height="12" fill="#1B4F72"/>
  <text x="390" y="332" fill="#1B4F72" font-size="11" font-weight="bold">BARREIRINHAS</text>
  <text x="390" y="344" fill="#1B4F72" font-size="8">(64 mil hab. — entrada principal)</text>

  <!-- Atins (leste) -->
  <rect x="490" y="120" width="10" height="10" fill="#1B4F72"/>
  <text x="508" y="130" fill="#1B4F72" font-size="10" font-weight="bold">ATINS</text>
  <text x="508" y="142" fill="#1B4F72" font-size="8">(foz do Preguiças)</text>

  <!-- Santo Amaro (oeste) -->
  <rect x="50" y="290" width="10" height="10" fill="#1B4F72"/>
  <text x="68" y="300" fill="#1B4F72" font-size="10">Santo Amaro</text>

  <!-- ÍCONES DE AMEAÇAS -->

  <!-- Petróleo (sudoeste) -->
  <text x="100" y="270" font-size="16">⛽</text>
  <text x="80" y="285" fill="#BA4A00" font-size="7">~60 poços abandonados</text>

  <!-- Eólicas (costa leste e oeste) -->
  <text x="530" y="170" font-size="16">💨</text>
  <text x="525" y="185" fill="#BA4A00" font-size="7">eólicas</text>
  <text x="40" y="140" font-size="16">💨</text>
  <text x="35" y="155" fill="#BA4A00" font-size="7">eólicas</text>

  <!-- Turismo (Barreirinhas e Atins) -->
  <text x="420" y="310" font-size="14">🚗</text>
  <text x="505" y="110" font-size="14">🚗</text>

  <!-- Esgoto (Barreirinhas) -->
  <text x="355" y="360" font-size="14">🚽</text>
  <text x="373" y="360" fill="#BA4A00" font-size="7">60% fossas</text>

  <!-- Legenda -->
  <rect x="420" y="380" width="170" height="65" fill="white" stroke="#888" stroke-width="1" rx="4"/>
  <text x="430" y="395" fill="#333" font-size="9" font-weight="bold">LEGENDA</text>
  <circle cx="435" cy="407" r="4" fill="#BA4A00"/><text x="445" y="411" fill="#333" font-size="8">Comunidades tradicionais (700 fam.)</text>
  <text x="430" y="425" font-size="9">⛽ Poços de petróleo abandonados</text>
  <text x="430" y="437" font-size="9">💨 Parques eólicos  🚗 Turismo 4x4</text>

  <!-- Norte -->
  <text x="570" y="30" fill="white" font-size="16" font-weight="bold">N ↑</text>

  <!-- Crédito -->
  <text x="300" y="445" text-anchor="middle" fill="#888" font-size="8">Quem é o Maranhão? — V10 | Fontes: ICMBio, UNESCO, ANP, ((o))eco</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Clean editorial map of Lençóis Maranhenses National Park, Brazil. DK (Dorling Kindersley) cartographic style — minimal, informative, with symbolic icons. Show: park boundary as dashed line enclosing white/beige dune area along Atlantic coast. Center of dunes: Queimada dos Britos community marked as an oasis (prominent terracotta dot). Scattered smaller dots for 16 other traditional communities. South entry: Barreirinhas town. East coast: Atins village at the mouth of Rio Preguiças. Rivers as thin blue lines. Threat icons distributed around the map: oil derrick icons (southwest, abandoned wells), wind turbine icons (east and west coast), jeep/4x4 icons (near entries), sewage warning icon (at Barreirinhas). Atlantic Ocean in deep blue at top. Legend box in corner. Color palette: sand white (#F5F5DC) for dunes, deep blue (#1B4F72) for ocean and rivers, terracotta (#BA4A00) for communities and threats, green (#1E8449) for vegetation borders. Clean, modern, editorial map quality. No excessive topographic detail."
**Estilo**: Cartografia editorial DK — limpa, informativa, com ícones simbólicos
**Referência**: Mapas de parques nacionais em guias DK Eyewitness ou atlas editorial
**NÃO incluir**: Grid de coordenadas, estradas secundárias, relevo sombreado, texto em inglês (será adicionado em português pelo designer)
