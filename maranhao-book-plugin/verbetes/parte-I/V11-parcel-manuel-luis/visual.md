---
id: VIS-V11-A
verbete: V11
tipo: ilustracao-subaquatica
posicao: página-inteira
---

# Visual V11-A: O cemitério que virou berçário — corte transversal

## 1. Briefing para designer
**O que é**: Corte transversal do Parcel de Manuel Luís mostrando: superfície do mar (linha), bancos rasos (~1m), profundidade ao redor (~50m), navio afundado no fundo coberto de corais, peixes, tartarugas. Acima da superfície: barco de mergulho. Abaixo: ecossistema submarino.
**Dados**:
- Superfície: mar aberto, sem terra visível
- Profundidade mínima: ~1m (bancos rasos)
- Profundidade ao redor: ~50m
- Navio afundado a ~15m (HMS Douro)
- Corais crescendo sobre o casco
- Espécies: cardumes, tartaruga-verde, raia, tubarão-lixa
- Distância da costa: 86 km
**Referência de estilo**: BBC Blue Planet infographic + Kurzgesagt
**Paleta**: Azul-mar #1B4965 (água profunda), Azul-claro (raso), Verde-mata #2D6A4F (corais/algas), Ocre #C8952E (arenito), Terracota #B5533E (casco), Creme #FAF3E8 (fundo do quadro)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado

```svg
<svg viewBox="0 0 500 600" xmlns="http://www.w3.org/2000/svg">
  <rect width="500" height="600" fill="#FAF3E8"/>
  <text x="250" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">O CEMITÉRIO QUE VIROU BERÇÁRIO</text>
  <!-- Céu -->
  <rect x="0" y="30" width="500" height="80" fill="#87CEEB" opacity="0.3"/>
  <!-- Barco na superfície -->
  <rect x="220" y="95" width="60" height="15" fill="#5C4033" rx="3"/>
  <text x="250" y="88" text-anchor="middle" font-size="7" fill="#2B2B2B">barco de mergulho</text>
  <!-- Linha d'água -->
  <line x1="0" y1="110" x2="500" y2="110" stroke="#1B4965" stroke-width="2"/>
  <text x="490" y="108" text-anchor="end" font-size="8" fill="#1B4965">superfície</text>
  <!-- Água rasa (banco) -->
  <rect x="150" y="110" width="200" height="20" fill="#1B4965" opacity="0.2"/>
  <text x="250" y="125" text-anchor="middle" font-size="7" fill="#1B4965">~1m (banco raso)</text>
  <!-- Água profunda dos lados -->
  <rect x="0" y="110" width="150" height="450" fill="#1B4965" opacity="0.4"/>
  <rect x="350" y="110" width="150" height="450" fill="#1B4965" opacity="0.4"/>
  <text x="75" y="400" text-anchor="middle" fill="white" font-size="9">~50m</text>
  <text x="425" y="400" text-anchor="middle" fill="white" font-size="9">~50m</text>
  <!-- Banco rochoso -->
  <rect x="140" y="130" width="220" height="30" fill="#C8952E" opacity="0.6" rx="5"/>
  <text x="250" y="150" text-anchor="middle" font-size="8" fill="#5C4033">arenito + coral</text>
  <!-- Navio afundado -->
  <rect x="190" y="280" width="120" height="40" fill="#B5533E" rx="5" opacity="0.7"/>
  <text x="250" y="305" text-anchor="middle" fill="white" font-size="8" font-weight="bold">HMS Douro (~15m)</text>
  <!-- Corais sobre o navio -->
  <circle cx="200" cy="275" r="12" fill="#2D6A4F" opacity="0.7"/>
  <circle cx="230" cy="270" r="15" fill="#2D6A4F" opacity="0.6"/>
  <circle cx="270" cy="272" r="10" fill="#3A8F60" opacity="0.7"/>
  <circle cx="300" cy="276" r="13" fill="#2D6A4F" opacity="0.7"/>
  <text x="250" y="260" text-anchor="middle" font-size="7" fill="#2D6A4F">corais colonizando o casco</text>
  <!-- Fauna -->
  <text x="170" y="230" font-size="9" fill="#1B4965">🐢</text>
  <text x="320" y="200" font-size="8" fill="#1B4965">🐟🐟🐟</text>
  <text x="350" y="340" font-size="8" fill="#1B4965">🦈</text>
  <!-- Dados -->
  <text x="250" y="450" text-anchor="middle" font-size="9" fill="white">200+ naufrágios • 50+ espécies de coral • 160+ espécies de peixe</text>
  <text x="250" y="500" text-anchor="middle" font-size="8" fill="white">MAIOR BANCO DE CORAIS DA AMÉRICA DO SUL</text>
  <!-- Fonte -->
  <text x="490" y="590" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: ICMBio, Marinha do Brasil, 2022</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Cross-section illustration of Parcel de Manuel Luís underwater ecosystem. Water surface at top with small dive boat. Shallow coral banks (~1m depth) in center. Deep water (~50m) on either side. A shipwreck (HMS Douro, iron hull) at 15m depth covered in colorful corals — hard corals in greens and oranges growing over the iron structure. Schools of fish swimming around. Sea turtle passing by. Nurse shark resting on bottom. Arenite/sandstone substrate visible. Clean scientific illustration style with data labels. Warm palette: deep blue water, green corals, ochre rock, terracotta hull. Style: BBC Blue Planet meets Kurzgesagt. No photorealism."
**Estilo**: Corte transversal submarino editorial
**NÃO incluir**: fotografias subaquáticas reais, CGI realista
