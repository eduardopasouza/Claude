---
id: VIS-V38-A
verbete: V38
tipo: infografico
posicao: corpo
---

# Visual V38-A: O caminho do grao — da Africa ao cuxa

## 1. Briefing para designer

**O que e**: Infografico de pagina inteira que mostra a jornada do arroz: da domesticacao na Africa Ocidental ate o prato de cuxa na mesa maranhense. Combina mapa de rotas com desdobramento dos ingredientes africanos.

**Dados**:
- Oryza glaberrima: domesticada no delta do Niger, 3.500-2.500 a.C.
- Rota: Guine-Bissau (portos de Bissau e Cacheu) → Sao Luis do Maranhao
- 88% dos escravizados do MA vieram da Alta Guine
- Grupo principal: Balanta (rizicultores)
- Arroz = principal exportacao do MA entre 1760-1778
- Ingredientes africanos do cuxa: vinagreira (Hibiscus sabdariffa), gergelim (Sesamum indicum), camarao seco (tecnica de conservacao)
- Unico ingrediente nao-africano: farinha de mandioca (indigena)

**Referencia de estilo**: Infografico editorial, estilo National Geographic / The New York Times — limpo, elegante, com camadas de informacao. Mapa estilizado (nao cartografico puro). Icones de ingredientes em estilo botanico simplificado.

**Paleta**:
- Fundo: creme #FAF3E8
- Rotas/setas: roxo-tambor #5E3A7E
- Destaque Africa: verde-mata #2D6A4F
- Destaque Maranhao: terracota #B5533E
- Textos: carvao #2B2B2B
- Icones de ingredientes: ocre #C8952E

**Tamanho**: Pagina inteira (23x28cm)

## 2. SVG simplificado

**Elementos**:
- Mapa esquematico do Atlantico com contornos da Africa Ocidental e Nordeste do Brasil
- Ponto de origem: delta do Niger (circulo pulsante) com label "Oryza glaberrima — 3.500 a.C."
- Ponto intermediario: costa da Guine-Bissau (Bissau/Cacheu) com label "88% dos escravizados"
- Seta curva cruzando Atlantico ate Sao Luis
- Ponto de chegada: Sao Luis com label "Maior exportador de arroz, 1760-1778"
- Abaixo do mapa: 4 icones em linha horizontal representando os ingredientes do cuxa
  - Vinagreira (folha estilizada) — label "AFRICA"
  - Gergelim (semente) — label "AFRICA"
  - Camarao seco (camarao) — label "AFRICA"
  - Farinha de mandioca (raiz) — label "INDIGENA"
- Abaixo dos icones: seta convergindo para um prato de arroz de cuxa estilizado
- Titulo: "O CAMINHO DO GRAO"

**Layout**: Vertical. Mapa ocupa 60% superior. Ingredientes e prato ocupam 40% inferior.

**Cores**: roxo-tambor para rotas, verde-mata para Africa, terracota para MA, ocre para icones

```svg
<svg viewBox="0 0 460 640" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="460" height="640" fill="#FAF3E8"/>

  <!-- Titulo -->
  <text x="230" y="35" text-anchor="middle" font-family="serif" font-size="18" font-weight="bold" fill="#2B2B2B">O CAMINHO DO GRAO</text>

  <!-- Africa esquematica -->
  <ellipse cx="310" cy="180" rx="80" ry="120" fill="none" stroke="#2D6A4F" stroke-width="2" opacity="0.3"/>
  <text x="310" y="120" text-anchor="middle" font-size="10" fill="#2D6A4F">AFRICA OCIDENTAL</text>

  <!-- Delta do Niger -->
  <circle cx="300" cy="155" r="6" fill="#2D6A4F"/>
  <text x="310" y="148" font-size="8" fill="#2B2B2B">Delta do Niger</text>
  <text x="310" y="158" font-size="7" fill="#5E3A7E">Oryza glaberrima — 3.500 a.C.</text>

  <!-- Guine-Bissau -->
  <circle cx="270" cy="175" r="8" fill="#5E3A7E"/>
  <text x="240" y="192" font-size="8" fill="#2B2B2B">Bissau/Cacheu</text>
  <text x="240" y="202" font-size="7" fill="#5E3A7E">88% dos escravizados</text>

  <!-- Brasil esquematico -->
  <ellipse cx="140" cy="220" rx="60" ry="90" fill="none" stroke="#B5533E" stroke-width="2" opacity="0.3"/>
  <text x="140" y="160" text-anchor="middle" font-size="10" fill="#B5533E">MARANHAO</text>

  <!-- Sao Luis -->
  <circle cx="155" cy="190" r="8" fill="#B5533E"/>
  <text x="100" y="185" font-size="8" fill="#2B2B2B">Sao Luis</text>
  <text x="80" y="195" font-size="7" fill="#B5533E">Maior exportador, 1760-1778</text>

  <!-- Rota atlantica -->
  <path d="M 268 180 Q 210 140 160 188" fill="none" stroke="#5E3A7E" stroke-width="3" stroke-dasharray="8,4" marker-end="url(#arrow)"/>
  <defs>
    <marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" markerHeight="6" orient="auto">
      <path d="M 0 0 L 10 5 L 0 10 z" fill="#5E3A7E"/>
    </marker>
  </defs>
  <text x="210" y="155" text-anchor="middle" font-size="8" fill="#5E3A7E" font-style="italic">Atlantico</text>

  <!-- Separador -->
  <line x1="40" y1="340" x2="420" y2="340" stroke="#C8952E" stroke-width="1" opacity="0.5"/>
  <text x="230" y="365" text-anchor="middle" font-size="12" font-weight="bold" fill="#2B2B2B">INGREDIENTES DO CUXA</text>

  <!-- Ingredientes -->
  <!-- Vinagreira -->
  <circle cx="80" cy="420" r="28" fill="#2D6A4F" opacity="0.15"/>
  <text x="80" y="418" text-anchor="middle" font-size="20">🌿</text>
  <text x="80" y="458" text-anchor="middle" font-size="9" font-weight="bold" fill="#2B2B2B">Vinagreira</text>
  <text x="80" y="470" text-anchor="middle" font-size="8" fill="#5E3A7E">AFRICA</text>

  <!-- Gergelim -->
  <circle cx="180" cy="420" r="28" fill="#C8952E" opacity="0.15"/>
  <text x="180" y="418" text-anchor="middle" font-size="20">🌾</text>
  <text x="180" y="458" text-anchor="middle" font-size="9" font-weight="bold" fill="#2B2B2B">Gergelim</text>
  <text x="180" y="470" text-anchor="middle" font-size="8" fill="#5E3A7E">AFRICA</text>

  <!-- Camarao -->
  <circle cx="280" cy="420" r="28" fill="#B5533E" opacity="0.15"/>
  <text x="280" y="418" text-anchor="middle" font-size="20">🦐</text>
  <text x="280" y="458" text-anchor="middle" font-size="9" font-weight="bold" fill="#2B2B2B">Camarao seco</text>
  <text x="280" y="470" text-anchor="middle" font-size="8" fill="#5E3A7E">AFRICA</text>

  <!-- Farinha -->
  <circle cx="380" cy="420" r="28" fill="#E8D5B7" opacity="0.5"/>
  <text x="380" y="418" text-anchor="middle" font-size="20">🌱</text>
  <text x="380" y="458" text-anchor="middle" font-size="9" font-weight="bold" fill="#2B2B2B">Farinha seca</text>
  <text x="380" y="470" text-anchor="middle" font-size="8" fill="#2D6A4F">INDIGENA</text>

  <!-- Setas convergentes -->
  <line x1="80" y1="485" x2="230" y2="540" stroke="#C8952E" stroke-width="1.5"/>
  <line x1="180" y1="485" x2="230" y2="540" stroke="#C8952E" stroke-width="1.5"/>
  <line x1="280" y1="485" x2="230" y2="540" stroke="#C8952E" stroke-width="1.5"/>
  <line x1="380" y1="485" x2="230" y2="540" stroke="#C8952E" stroke-width="1.5"/>

  <!-- Prato final -->
  <ellipse cx="230" cy="570" rx="60" ry="25" fill="#5E3A7E" opacity="0.1" stroke="#5E3A7E" stroke-width="2"/>
  <text x="230" y="575" text-anchor="middle" font-size="14" font-weight="bold" fill="#5E3A7E">ARROZ DE CUXA</text>

  <!-- Rodape -->
  <text x="230" y="620" text-anchor="middle" font-size="8" fill="#2B2B2B" font-style="italic">Fontes: Carney (2001), Cascudo (1967), Hawthorne (2010)</text>
</svg>
```

## 3. Prompt para IA generativa

**Prompt**: "Editorial infographic showing the journey of rice from West Africa to Brazilian cuisine. Top section: stylized map of the Atlantic Ocean with West Africa (Guinea-Bissau highlighted) and northeastern Brazil (Maranhao highlighted), connected by a sweeping purple arrow across the ocean. Bottom section: four botanical-style illustrations of ingredients (hibiscus/sorrel leaves, sesame seeds, dried shrimp, cassava flour) converging into a beautiful plate of green rice dish. Color palette: deep purple #5E3A7E, forest green #2D6A4F, terracotta #B5533E, ochre #C8952E, cream background #FAF3E8. Style: clean editorial design, National Geographic meets food magazine, elegant serif typography, no photorealism — illustrated and diagrammatic."

**Estilo**: Infografico editorial ilustrado, tipografia serifada elegante
**Referencia**: National Geographic infographics, NYT cooking visual essays
**NAO incluir**: fotografias realistas, clipart, elementos cartoonescos, emojis no design final
