---
id: VIS-V01-A
verbete: V01
tipo: mapa
posicao: página-inteira
---

# Visual V01-A: Mapa dos três biomas do Maranhão

## 1. Briefing para designer
**O que é**: Mapa temático do Maranhão mostrando a divisão em três biomas + sobreposição da Amazônia Legal.
**Dados**:
- Cerrado: ~65% do território (sul e centro) — cor Ocre #C8952E
- Amazônia: ~34% do território (noroeste) — cor Verde-mata #2D6A4F
- Caatinga: ~1% do território (extremo leste) — cor Terracota #B5533E
- Amazônia Legal: tracejado sobre 79,3% do território (181/217 municípios)
- Mata dos Cocais: hachura suave no centro-norte (zona de transição)
- Fronteiras: rios nomeados (Parnaíba, Gurupi, Tocantins)
- Capital: São Luís marcada com ponto
- Estados vizinhos: PI, TO, PA nomeados fora do contorno
**Referência de estilo**: Kurzgesagt — limpo, cores vibrantes, sem ruído visual
**Paleta**: Verde-mata (Amazônia) + Ocre (Cerrado) + Terracota (Caatinga) + Azul-mar (rios/litoral) sobre Creme
**Tamanho**: Página inteira (23×28cm)

## 2. SVG simplificado
**Elementos**:
- Contorno do Maranhão (polígono simplificado)
- 3 zonas de cor (Cerrado/Amazônia/Caatinga)
- Linha tracejada para limite da Amazônia Legal
- 3 linhas azuis para rios-fronteira
- Ponto para São Luís
- Rótulos: nomes dos biomas + porcentagens, nomes dos rios, estados vizinhos
**Layout**: Mapa centralizado, legenda no canto inferior esquerdo, fonte no canto inferior direito
**Cores**: #C8952E (cerrado), #2D6A4F (amazônia), #B5533E (caatinga), #1B4965 (rios), #2B2B2B (contorno/texto), #FAF3E8 (fundo)

```svg
<!-- SVG esquemático — placeholder para designer -->
<svg viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="500" fill="#FAF3E8"/>
  <text x="200" y="30" text-anchor="middle" font-family="Source Sans Pro" font-size="14" fill="#2B2B2B">MARANHÃO — TRÊS BIOMAS</text>
  <!-- Placeholder: contorno do MA com 3 zonas -->
  <rect x="50" y="50" width="300" height="180" fill="#2D6A4F" rx="10" opacity="0.7"/>
  <text x="200" y="145" text-anchor="middle" fill="white" font-size="12">AMAZÔNIA ~34%</text>
  <rect x="50" y="230" width="300" height="180" fill="#C8952E" rx="10" opacity="0.7"/>
  <text x="200" y="325" text-anchor="middle" fill="white" font-size="12">CERRADO ~65%</text>
  <rect x="330" y="150" width="40" height="100" fill="#B5533E" rx="5" opacity="0.7"/>
  <text x="350" y="205" text-anchor="middle" fill="white" font-size="8">CAA ~1%</text>
  <!-- Rios -->
  <line x1="350" y1="50" x2="350" y2="410" stroke="#1B4965" stroke-width="2" stroke-dasharray="5,3"/>
  <text x="370" y="230" fill="#1B4965" font-size="8">Parnaíba</text>
  <line x1="50" y1="50" x2="50" y2="250" stroke="#1B4965" stroke-width="2"/>
  <text x="25" y="150" fill="#1B4965" font-size="8" writing-mode="tb">Gurupi</text>
  <!-- Legenda -->
  <rect x="20" y="440" width="10" height="10" fill="#2D6A4F"/>
  <text x="35" y="450" font-size="9" fill="#2B2B2B">Amazônia</text>
  <rect x="100" y="440" width="10" height="10" fill="#C8952E"/>
  <text x="115" y="450" font-size="9" fill="#2B2B2B">Cerrado</text>
  <rect x="180" y="440" width="10" height="10" fill="#B5533E"/>
  <text x="195" y="450" font-size="9" fill="#2B2B2B">Caatinga</text>
  <text x="380" y="490" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: IBGE, 2024</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Editorial map illustration of Maranhão state, Brazil, showing three biomes in distinct warm colors: Amazon rainforest in deep green (northwest), Cerrado savanna in golden ochre (south/center), and a thin strip of Caatinga in terracotta (far east). Clean cartographic style with river borders labeled (Parnaíba, Gurupi, Tocantins). Atlantic Ocean at top. Capital São Luís marked on island. Overlay showing Amazônia Legal boundary as dashed line covering 79% of state. Warm cream background. Style: Kurzgesagt meets National Geographic editorial. Clean, modern, data-rich. No photorealism."
**Estilo**: Infográfico editorial — Kurzgesagt warmth + NatGeo precision
**Referência**: Vox Atlas-style thematic maps
**NÃO incluir**: fotografias, texturas realistas, 3D, sombras dramáticas

---

---
id: VIS-V01-B
verbete: V01
tipo: mapa
posicao: corpo
---

# Visual V01-B: Latitudes irmãs — faixa equatorial

## 1. Briefing para designer
**O que é**: Mapa-múndi simplificado mostrando a faixa equatorial (0° a 5°S) com 6 cidades marcadas: São Luís, Singapura, Nairobi, Kinshasa, Quito, Manaus.
**Dados**:
- São Luís: 2,5°S
- Singapura: 1,3°N
- Nairobi: 1,3°S
- Kinshasa: 4,4°S
- Quito: 0,2°S
- Manaus: 3,1°S
**Referência de estilo**: Kurzgesagt world map — simplificado, sem fronteiras nacionais detalhadas
**Paleta**: Faixa equatorial em Ocre 15%; continentes em Areia; oceanos em Azul-mar 20%; pontos das cidades em Terracota; São Luís destacada em Vermelho-bumba
**Tamanho**: Meia página (inline no texto)

## 2. SVG simplificado
**Elementos**: Retângulo representando mapa-múndi, faixa horizontal equatorial, 6 pontos com rótulos
**Layout**: Horizontal, faixa de 5°N a 5°S destacada

## 3. Prompt para IA generativa
**Prompt**: "Minimalist world map illustration showing the equatorial belt from 5°N to 5°S highlighted in warm golden tone. Six cities marked with dots and labels: São Luís (Brazil), Singapore, Nairobi (Kenya), Kinshasa (DR Congo), Quito (Ecuador), Manaus (Brazil). São Luís highlighted in red. Continents in warm sand color, oceans in muted blue. Clean, modern editorial style. Warm cream background. No country borders, no unnecessary detail. Style: Kurzgesagt meets data visualization."
**Estilo**: Infográfico minimalista
**NÃO incluir**: detalhes geográficos excessivos, fronteiras nacionais, relevo
