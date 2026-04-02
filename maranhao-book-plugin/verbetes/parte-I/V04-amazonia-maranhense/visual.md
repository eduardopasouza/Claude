---
id: VIS-V04-A
verbete: V04
tipo: mapa-satelite
posicao: página-inteira
---

# Visual V04-A: O que resta da Amazônia maranhense

## 1. Briefing para designer
**O que é**: Mapa do noroeste do Maranhão mostrando remanescentes florestais (verde) vs. áreas desmatadas (marrom/bege). TIs e REBIO Gurupi em destaque com contornos nomeados. Inspirado em imagem de satélite estilizada.
**Dados**:
- REBIO Gurupi: 271.197 ha — contorno verde com hachura (30% invadida)
- TI Alto Turiaçu: 530.525 ha — verde sólido
- TI Caru: 172.667 ha — verde sólido
- TI Awá: 116.582 ha — verde sólido
- Entorno: marrom/bege (pasto e áreas degradadas)
- Rio Gurupi: linha azul (fronteira MA/PA)
- Municípios: Açailândia, Buriticupu, Santa Luzia marcados
**Referência de estilo**: Global Forest Watch + Kurzgesagt
**Paleta**: Verde-mata #2D6A4F (floresta), Bege #D4C5A9 (desmatado), Terracota #B5533E (invasão), Azul-mar #1B4965 (rios), Creme #FAF3E8 (fundo)
**Tamanho**: Página inteira (23x28cm)

## 2. SVG simplificado

```svg
<svg viewBox="0 0 400 500" xmlns="http://www.w3.org/2000/svg">
  <rect width="400" height="500" fill="#FAF3E8"/>
  <text x="200" y="25" text-anchor="middle" font-family="Source Sans Pro" font-size="13" fill="#2B2B2B">O QUE RESTA DA AMAZÔNIA MARANHENSE</text>
  <!-- Fundo desmatado -->
  <rect x="30" y="40" width="340" height="400" fill="#D4C5A9" rx="5"/>
  <!-- TI Alto Turiaçu -->
  <rect x="50" y="60" width="120" height="150" fill="#2D6A4F" rx="8" opacity="0.85"/>
  <text x="110" y="140" text-anchor="middle" fill="white" font-size="9" font-weight="bold">TI ALTO TURIAÇU</text>
  <text x="110" y="155" text-anchor="middle" fill="white" font-size="7">530.525 ha (Ka'apor)</text>
  <!-- TI Caru -->
  <rect x="180" y="120" width="80" height="100" fill="#2D6A4F" rx="8" opacity="0.85"/>
  <text x="220" y="170" text-anchor="middle" fill="white" font-size="8" font-weight="bold">TI CARU</text>
  <text x="220" y="183" text-anchor="middle" fill="white" font-size="7">172.667 ha</text>
  <!-- TI Awá -->
  <rect x="120" y="230" width="70" height="80" fill="#2D6A4F" rx="8" opacity="0.85"/>
  <text x="155" y="270" text-anchor="middle" fill="white" font-size="8" font-weight="bold">TI AWÁ</text>
  <text x="155" y="283" text-anchor="middle" fill="white" font-size="7">116.582 ha</text>
  <!-- REBIO Gurupi -->
  <rect x="40" y="230" width="70" height="120" fill="#2D6A4F" rx="8" opacity="0.6"/>
  <rect x="40" y="300" width="70" height="50" fill="#B5533E" rx="0" opacity="0.4"/>
  <text x="75" y="280" text-anchor="middle" fill="white" font-size="8" font-weight="bold">REBIO</text>
  <text x="75" y="293" text-anchor="middle" fill="white" font-size="7">GURUPI</text>
  <text x="75" y="330" text-anchor="middle" fill="#B5533E" font-size="6">~30% invadida</text>
  <!-- Rio Gurupi -->
  <line x1="35" y1="40" x2="35" y2="440" stroke="#1B4965" stroke-width="2.5"/>
  <text x="20" y="240" fill="#1B4965" font-size="8" writing-mode="tb">Gurupi</text>
  <!-- Label Pará -->
  <text x="15" y="140" fill="#2B2B2B" font-size="9" font-style="italic">PARÁ</text>
  <!-- Municípios -->
  <circle cx="300" cy="350" r="4" fill="#C23B22"/>
  <text x="310" y="354" fill="#2B2B2B" font-size="7">Açailândia</text>
  <circle cx="270" cy="280" r="3" fill="#C23B22"/>
  <text x="280" y="284" fill="#2B2B2B" font-size="7">Buriticupu</text>
  <!-- Legenda -->
  <rect x="240" y="420" width="10" height="10" fill="#2D6A4F"/>
  <text x="255" y="430" font-size="8" fill="#2B2B2B">Floresta (TI/UC)</text>
  <rect x="240" y="435" width="10" height="10" fill="#D4C5A9"/>
  <text x="255" y="445" font-size="8" fill="#2B2B2B">Desmatado</text>
  <rect x="240" y="450" width="10" height="10" fill="#B5533E" opacity="0.5"/>
  <text x="255" y="460" font-size="8" fill="#2B2B2B">Invadido</text>
  <text x="360" y="490" text-anchor="end" font-size="7" fill="#2B2B2B">Fonte: INPE, MapBiomas, FUNAI</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Stylized satellite-view map of northwestern Maranhão showing deforestation pattern. Large brown/beige area (deforested land) surrounding green blocks (Indigenous Territories and REBIO Gurupi reserve). Green blocks labeled: TI Alto Turiaçu, TI Caru, TI Awá, REBIO Gurupi. Gurupi River as blue line on western border. Contrast between green blocks and surrounding brown should be dramatic and clear. Clean editorial cartographic style. Warm cream background. Style: Global Forest Watch visualization meets Kurzgesagt warmth. Data-rich, no photorealism."
**Estilo**: Mapa de dados satelitais estilizado
**NÃO incluir**: fotografias reais de satélite, excesso de detalhes topográficos
