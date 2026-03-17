---
id: VIS-V54-A
verbete: V54
tipo: mapa
posicao: página-inteira
---

# Visual V54-A: Mapa ilustrado de Alcântara — ruínas, quilombos e foguetes

## 1. Briefing para designer
**O que é**: Mapa ilustrado da cidade e do município de Alcântara, mostrando três camadas sobrepostas: o patrimônio colonial (ruínas), o território quilombola (comunidades) e a base espacial (CLA). Página inteira.
**Dados**:
- Centro histórico: Praça da Matriz, pelourinho, Igreja Matriz de São Matias (ruína), Igreja do Carmo, Igreja de São Francisco, Igreja de N.S. do Rosário, ruínas dos palácios dos Barões de Pindaré e Mearim, Museu Casa Histórica, fontes coloniais, Passos da Paixão
- Porto de embarque (travessia de 1h desde São Luís)
- CLA: 9.256 ha de operação, torre de lançamento na faixa costeira norte
- Território quilombola: 78.105 ha delimitados, 122 localidades quilombolas
- Agrovilas (7): onde as 312 famílias foram reassentadas nos anos 1980
- São Luís visível do outro lado da Baía de São Marcos
**Referência de estilo**: Mapa turístico-editorial ilustrado — tipo DK Eyewitness, com ícones desenhados para cada ponto
**Paleta**: Terracota (#BA4A00) para ruínas coloniais, Preto-mangue (#1C1C1C) para território quilombola, Azul-mar (#1B4F72) para baía/oceano, Cinza-claro para CLA/base espacial
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Contorno do município de Alcântara (peninsula/costa)
- Zona sul: centro histórico (ícones de igrejas, ruínas, pelourinho)
- Zona norte costeira: CLA com ícone de torre de lançamento
- Interior: pontos distribuídos para comunidades quilombolas e agrovilas
- Baía de São Marcos ao sul com São Luís indicada na outra margem
- Legenda tripla: colonial (terracota) / quilombola (preto) / espacial (cinza)
**Layout**: Vertical, norte no topo

```svg
<svg viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
  <!-- Baía de São Marcos -->
  <rect x="0" y="450" width="500" height="150" fill="#1B4F72" opacity="0.3"/>
  <text x="250" y="520" text-anchor="middle" fill="#1B4F72" font-size="14">BAÍA DE SÃO MARCOS</text>
  <text x="250" y="560" text-anchor="middle" fill="#1B4F72" font-size="10">← São Luís (1h de barco)</text>

  <!-- Oceano (norte) -->
  <rect x="0" y="0" width="500" height="60" fill="#1B4F72" opacity="0.2"/>
  <text x="250" y="35" text-anchor="middle" fill="#1B4F72" font-size="12">ATLÂNTICO</text>

  <!-- CLA — Zona Norte -->
  <rect x="100" y="60" width="300" height="100" fill="#888" opacity="0.2" rx="8"/>
  <text x="250" y="90" text-anchor="middle" fill="#555" font-size="12" font-weight="bold">CLA — 9.256 ha</text>
  <text x="250" y="110" text-anchor="middle" fill="#555" font-size="10">Centro de Lançamento de Alcântara</text>
  <!-- Torre -->
  <rect x="240" y="115" width="20" height="35" fill="#888"/>
  <polygon points="235,115 265,115 250,95" fill="#888"/>

  <!-- Território Quilombola -->
  <rect x="30" y="170" width="440" height="200" fill="#1C1C1C" opacity="0.1" rx="10" stroke="#1C1C1C" stroke-width="1" stroke-dasharray="5,5"/>
  <text x="250" y="195" text-anchor="middle" fill="#1C1C1C" font-size="11" font-weight="bold">TERRITÓRIO QUILOMBOLA — 78.105 ha</text>
  <text x="250" y="215" text-anchor="middle" fill="#1C1C1C" font-size="9">122 localidades | 84,6% da população</text>
  <!-- Comunidades -->
  <circle cx="100" cy="250" r="4" fill="#1C1C1C"/>
  <circle cx="200" cy="270" r="4" fill="#1C1C1C"/>
  <circle cx="350" cy="240" r="4" fill="#1C1C1C"/>
  <circle cx="400" cy="280" r="4" fill="#1C1C1C"/>
  <circle cx="150" cy="300" r="4" fill="#1C1C1C"/>
  <!-- Agrovilas -->
  <rect x="270" cy="310" width="8" height="8" fill="#666" x="270" y="306"/>
  <text x="285" y="314" fill="#666" font-size="8">agrovila</text>

  <!-- Centro Histórico — Zona Sul -->
  <rect x="150" y="380" width="200" height="70" fill="#BA4A00" opacity="0.2" rx="8"/>
  <text x="250" y="400" text-anchor="middle" fill="#BA4A00" font-size="11" font-weight="bold">CENTRO HISTÓRICO</text>
  <text x="250" y="415" text-anchor="middle" fill="#BA4A00" font-size="9">IPHAN 1948 | 140 ha | ~400 imóveis</text>
  <!-- Ícones -->
  <circle cx="200" cy="435" r="4" fill="#BA4A00"/>
  <text x="210" y="438" fill="#BA4A00" font-size="7">Matriz (ruína)</text>
  <circle cx="300" cy="435" r="4" fill="#BA4A00"/>
  <text x="310" y="438" fill="#BA4A00" font-size="7">Pelourinho</text>

  <!-- Porto -->
  <circle cx="250" cy="455" r="5" fill="#1B4F72"/>
  <text x="265" y="458" fill="#1B4F72" font-size="8">Porto</text>

  <!-- Legenda -->
  <rect x="20" y="555" width="10" height="10" fill="#BA4A00"/>
  <text x="35" y="564" fill="#333" font-size="9">Colonial</text>
  <rect x="120" y="555" width="10" height="10" fill="#1C1C1C"/>
  <text x="135" y="564" fill="#333" font-size="9">Quilombola</text>
  <rect x="230" y="555" width="10" height="10" fill="#888"/>
  <text x="245" y="564" fill="#333" font-size="9">Base espacial</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Illustrated map of Alcântara municipality, Maranhão, Brazil, showing three overlapping layers: (1) Colonial heritage in the south — ruined churches, stone arches, pelourinho column, crumbling sobrados with terracotta accents; (2) Quilombola territory across the interior — scattered communities represented by small thatched houses, palm trees, agricultural plots; (3) Space center (CLA) on the northern coast — modern launch tower, satellite dishes, fenced perimeter. São Marcos Bay to the south with São Luís visible across the water. Bird's eye view, slightly angled. Editorial illustrated map style, DK Eyewitness quality. Color coding: terracotta for colonial, dark earth tones for quilombola, grey/steel for space center, deep blue for water. Warm tropical light. No text — labels will be added separately."
**Estilo**: Mapa editorial ilustrado (DK Eyewitness / Lonely Planet)
**NÃO incluir**: Texto definitivo em português, grade de coordenadas

---

---
id: VIS-V54-B
verbete: V54
tipo: timeline
posicao: meia-página
---

# Visual V54-B: Linha do tempo — Alcântara em 4 séculos

## 1. Briefing para designer
**O que é**: Timeline horizontal mostrando a ascensão e queda de Alcântara, desde Tapuitapera até a sentença da Corte IDH. Meia página.
**Dados**:
- Pré-1612: Aldeia Tupinambá de Tapuitapera
- 1612: Chegada dos franceses (França Equinocial)
- 1648: Vila de Santo Antônio de Alcântara (portugueses)
- 1755: Companhia de Pombal — escravizados africanos em escala industrial
- 1776-1820: Auge — algodão para Lancashire, palácios, 155 navios/ano
- 1836: Elevada a cidade
- 1860s: Declínio — algodão americano volta, migração das elites
- 1888: Abolição — golpe final, esvaziamento
- 1948: Tombamento IPHAN
- 1983: Criação do CLA
- 1986-87: Remoção de 312 famílias quilombolas
- 2004: IPHAN amplia classificação
- 2019: Acordo EUA-Brasil para lançamentos
- 2024: Termo de Compromisso (AGU) — titulação quilombola
- 2025: Sentença da Corte IDH — 1ª sobre quilombolas
**Referência de estilo**: Timeline editorial com ícones — estilo Vox ou The Pudding
**Paleta**: Dourado (#D4AC0D) para o apogeu, Terracota (#BA4A00) para declínio/colonial, Preto (#1C1C1C) para período quilombola/conflito, Cinza para período espacial
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**: Linha horizontal com marcos temporais, ícones acima/abaixo, gradiente de cor do dourado (apogeu) ao cinza (declínio) ao preto (conflito)
**Layout**: Horizontal, leitura da esquerda para a direita

## 3. Prompt para IA generativa
**Prompt**: "Horizontal timeline infographic showing the history of Alcântara, Maranhão, Brazil across 400 years. Key moments marked with icons: indigenous village (1612), Portuguese colonial period with cotton wealth (1755-1836), golden age with mansions and ships (peak), decline and abandonment (1860s-1888), heritage protection (1948), space center installation (1983), quilombola family displacement (1986), international court ruling (2025). Color gradient from golden (prosperity) through terracotta (decline) to dark grey (modern conflict). Clean editorial infographic style, minimal, with room for Portuguese text labels. Timeline curves slightly upward during golden age and downward during decline."
**Estilo**: Infográfico editorial (Vox / The Pudding)
**NÃO incluir**: Texto definitivo (será inserido pelo designer)
