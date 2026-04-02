---
id: VIS-V07-A
verbete: V07
tipo: mapa-climático
posicao: corpo
---

# Visual V07-A: Mapa de precipitação — o gradiente úmido-seco

## 1. Briefing para designer
**O que é**: Mapa do Maranhão mostrando gradiente de precipitação anual: norte/oeste úmido (2.200 mm, azul intenso) degradando para leste seco (700 mm, ocre/terracota). Cidades marcadas com precipitação anual.
**Dados**:
- São Luís: 2.200 mm/ano (azul)
- Imperatriz: 1.600 mm/ano (verde-azulado)
- Presidente Dutra: 1.200 mm/ano (verde)
- Caxias: 700 mm/ano (ocre)
- Pastos Bons: 800 mm/ano (ocre claro)
- Gradiente contínuo norte→leste
- Faixa de caatinga no extremo leste (terracota)
- Rio Parnaíba como fronteira leste
**Referência de estilo**: Kurzgesagt — gradiente limpo, dados integrados
**Paleta**: Azul-mar #1B4965 (úmido) → Verde-mata #2D6A4F → Ocre #C8952E → Terracota #B5533E (seco). Creme #FAF3E8 (fundo)
**Tamanho**: Meia página

## 2. SVG simplificado

```svg
<svg viewBox="0 0 400 450" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="450" fill="#FAF3E8"/>
  <text x="200" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">PRECIPITAÇÃO ANUAL — O GRADIENTE ÚMIDO-SECO</text>
  <!-- Gradiente simplificado -->
  <defs>
    <linearGradient id="precip" x1="0%" y1="0%" x2="100%" y2="50%">
      <stop offset="0%" style="stop-color:#1B4965"/>
      <stop offset="40%" style="stop-color:#2D6A4F"/>
      <stop offset="70%" style="stop-color:#C8952E"/>
      <stop offset="100%" style="stop-color:#B5533E"/>
    </linearGradient>
  </defs>
  <rect x="30" y="40" width="340" height="350" fill="url(#precip)" rx="10" opacity="0.7"/>
  <!-- Cidades -->
  <circle cx="100" cy="70" r="5" fill="white"/>
  <text x="110" y="65" fill="white" font-size="9" font-weight="bold">São Luís</text>
  <text x="110" y="78" fill="white" font-size="8">2.200 mm</text>
  <circle cx="80" cy="220" r="4" fill="white"/>
  <text x="90" y="218" fill="white" font-size="8">Imperatriz 1.600 mm</text>
  <circle cx="200" cy="200" r="4" fill="white"/>
  <text x="210" y="198" fill="white" font-size="8">Pres. Dutra 1.200 mm</text>
  <circle cx="320" cy="180" r="5" fill="white"/>
  <text x="265" y="170" fill="white" font-size="9" font-weight="bold">Caxias</text>
  <text x="265" y="183" fill="white" font-size="8">700 mm</text>
  <circle cx="300" cy="280" r="4" fill="white"/>
  <text x="240" y="278" fill="white" font-size="8">Pastos Bons 800 mm</text>
  <!-- Rio Parnaíba -->
  <line x1="355" y1="40" x2="355" y2="390" stroke="#1B4965" stroke-width="2" stroke-dasharray="4,3"/>
  <text x="370" y="200" fill="#1B4965" font-size="8">Parnaíba</text>
  <text x="375" y="215" fill="#2B2B2B" font-size="7" font-style="italic">PIAUÍ</text>
  <!-- Legenda -->
  <rect x="30" y="405" width="60" height="8" fill="#1B4965"/>
  <rect x="90" y="405" width="60" height="8" fill="#2D6A4F"/>
  <rect x="150" y="405" width="60" height="8" fill="#C8952E"/>
  <rect x="210" y="405" width="60" height="8" fill="#B5533E"/>
  <text x="30" y="430" font-size="7" fill="#2B2B2B">2.200 mm</text>
  <text x="270" y="430" text-anchor="end" font-size="7" fill="#2B2B2B">600 mm</text>
  <text x="370" y="440" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: INMET, 2023</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Editorial map of Maranhão state showing annual precipitation gradient. Northwest/coast in deep blue (2200mm rain), transitioning through green to golden ochre and terracotta in the east (700mm). Five cities marked with rainfall data: São Luís, Imperatriz, Presidente Dutra, Caxias, Pastos Bons. Parnaíba River as eastern border. Caatinga strip in terracotta on far east. Clean gradient map, warm cream background. Style: Kurzgesagt meets climate atlas. No photorealism, data-rich."
**Estilo**: Mapa climático editorial
**NÃO incluir**: fotografias, relevo detalhado, excesso de toponímia
