---
id: VIS-V35-A
verbete: V35
tipo: mapa
posicao: pagina-inteira
---

# Visual V35-A: Mapa das comunidades quilombolas do Maranhao

## 1. Briefing para designer
**O que e**: Mapa do Maranhao mostrando a distribuicao geografica das comunidades quilombolas, com concentracao visivel nas tres regioes principais: Baixada Maranhense, Vale do Itapecuru e Alcantara. Visual principal do verbete, pagina inteira.
**Dados**:
- Total: 1.152 comunidades certificadas (Fundacao Palmares, 2024)
- Concentracao 1: Baixada Maranhense (Pinheiro, Viana, Santa Helena, Penalva) — quilombos da agua
- Concentracao 2: Vale do Itapecuru (Itapecuru-Mirim, Codo, Caxias) — quilombos das antigas fazendas
- Concentracao 3: Alcantara (200+ comunidades) — maior adensamento do Brasil
- Comunidades em destaque: Frechal (Mirinzal), Jamary dos Pretos, Damazio, Alcantara
- Rios principais como eixo: Itapecuru, Mearim, Pindare, Turiacu
- CLA (Centro de Lancamento de Alcantara) marcado como zona de conflito
**Referencia de estilo**: Mapa tematico editorial — pontos/clusters representando comunidades, rios em destaque, zonas de concentracao em halo colorido
**Paleta**: Roxo-tambor (#5E3A7E) para comunidades quilombolas, Azul-rio (#1B4F72) para hidrografia, Terracota (#BA4A00) para zona de conflito CLA, Dourado-babacu (#D4AC0D) para destaques/rotulos
**Tamanho**: Pagina inteira (23x28 cm)

## 2. SVG simplificado
**Elementos**:
- Contorno do estado do Maranhao com rios principais
- Clusters de pontos roxos nas tres zonas de concentracao
- Pontos dispersos no restante do estado
- Destaque para Frechal, Alcantara (com icone de conflito CLA)
- Legenda com dados numericos
**Layout**: Vertical, norte para cima, legenda lateral direita

```svg
<svg viewBox="0 0 600 700" xmlns="http://www.w3.org/2000/svg">
  <!-- Fundo -->
  <rect width="600" height="700" fill="#F5F5DC" opacity="0.3"/>

  <!-- Contorno MA (simplificado) -->
  <path d="M150,100 L350,80 L450,120 L500,200 L480,350 L450,450 L400,550 L300,600 L200,580 L150,500 L120,400 L100,300 L110,200 Z" fill="#F5F5DC" stroke="#1C1C1C" stroke-width="2"/>

  <!-- Rios principais -->
  <path d="M250,150 L280,250 L300,350 L310,450 L320,550" fill="none" stroke="#1B4F72" stroke-width="2" opacity="0.6"/>
  <text x="325" y="400" fill="#1B4F72" font-size="9" transform="rotate(10,325,400)">Itapecuru</text>

  <path d="M200,180 L220,280 L230,380 L240,480" fill="none" stroke="#1B4F72" stroke-width="2" opacity="0.6"/>
  <text x="245" y="340" fill="#1B4F72" font-size="9" transform="rotate(8,245,340)">Mearim</text>

  <path d="M170,200 L180,300 L185,400" fill="none" stroke="#1B4F72" stroke-width="2" opacity="0.5"/>
  <text x="190" y="310" fill="#1B4F72" font-size="8">Pindare</text>

  <!-- Zona 1: Alcantara (200+) -->
  <circle cx="220" cy="140" r="35" fill="#5E3A7E" opacity="0.2"/>
  <circle cx="210" cy="130" r="3" fill="#5E3A7E"/>
  <circle cx="220" cy="135" r="3" fill="#5E3A7E"/>
  <circle cx="230" cy="140" r="3" fill="#5E3A7E"/>
  <circle cx="215" cy="145" r="3" fill="#5E3A7E"/>
  <circle cx="225" cy="150" r="3" fill="#5E3A7E"/>
  <circle cx="235" cy="133" r="3" fill="#5E3A7E"/>
  <circle cx="205" cy="140" r="3" fill="#5E3A7E"/>
  <text x="195" y="175" fill="#5E3A7E" font-size="10" font-weight="bold">Alcantara (200+)</text>

  <!-- CLA zona de conflito -->
  <rect x="225" y="120" width="20" height="15" fill="#BA4A00" opacity="0.3" stroke="#BA4A00" stroke-dasharray="3,2"/>
  <text x="247" y="130" fill="#BA4A00" font-size="7">CLA</text>

  <!-- Zona 2: Baixada Maranhense -->
  <circle cx="175" cy="250" r="40" fill="#5E3A7E" opacity="0.15"/>
  <circle cx="160" cy="240" r="3" fill="#5E3A7E"/>
  <circle cx="170" cy="250" r="3" fill="#5E3A7E"/>
  <circle cx="180" cy="245" r="3" fill="#5E3A7E"/>
  <circle cx="165" cy="260" r="3" fill="#5E3A7E"/>
  <circle cx="185" cy="255" r="3" fill="#5E3A7E"/>
  <circle cx="175" cy="265" r="3" fill="#5E3A7E"/>
  <text x="140" y="300" fill="#5E3A7E" font-size="10" font-weight="bold">Baixada Maranhense</text>

  <!-- Frechal destaque -->
  <circle cx="155" cy="230" r="5" fill="#D4AC0D" stroke="#5E3A7E" stroke-width="1.5"/>
  <text x="110" y="225" fill="#D4AC0D" font-size="8" font-weight="bold">Frechal</text>

  <!-- Zona 3: Vale do Itapecuru -->
  <circle cx="320" cy="350" r="45" fill="#5E3A7E" opacity="0.15"/>
  <circle cx="300" cy="340" r="3" fill="#5E3A7E"/>
  <circle cx="310" cy="350" r="3" fill="#5E3A7E"/>
  <circle cx="320" cy="345" r="3" fill="#5E3A7E"/>
  <circle cx="330" cy="355" r="3" fill="#5E3A7E"/>
  <circle cx="315" cy="365" r="3" fill="#5E3A7E"/>
  <circle cx="335" cy="340" r="3" fill="#5E3A7E"/>
  <text x="280" y="400" fill="#5E3A7E" font-size="10" font-weight="bold">Vale do Itapecuru</text>

  <!-- Pontos dispersos (outras regioes) -->
  <circle cx="350" cy="250" r="2" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="400" cy="300" r="2" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="380" cy="420" r="2" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="250" cy="450" r="2" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="300" cy="500" r="2" fill="#5E3A7E" opacity="0.5"/>
  <circle cx="200" cy="400" r="2" fill="#5E3A7E" opacity="0.5"/>

  <!-- Sao Luis -->
  <circle cx="240" cy="115" r="5" fill="#1C1C1C"/>
  <text x="248" y="112" fill="#1C1C1C" font-size="9" font-weight="bold">Sao Luis</text>

  <!-- Titulo -->
  <text x="30" y="40" fill="#1C1C1C" font-size="16" font-weight="bold">Comunidades quilombolas do Maranhao</text>
  <text x="30" y="58" fill="#5E3A7E" font-size="11">1.152 certificadas — 1o lugar no Brasil</text>

  <!-- Legenda -->
  <rect x="430" y="500" width="150" height="120" fill="white" opacity="0.8" rx="5"/>
  <circle cx="445" cy="520" r="4" fill="#5E3A7E"/>
  <text x="455" y="524" fill="#1C1C1C" font-size="9">Comunidade quilombola</text>
  <circle cx="445" cy="540" r="4" fill="#D4AC0D" stroke="#5E3A7E" stroke-width="1"/>
  <text x="455" y="544" fill="#1C1C1C" font-size="9">Destaque (Frechal)</text>
  <rect x="440" y="554" width="10" height="8" fill="#BA4A00" opacity="0.3" stroke="#BA4A00" stroke-dasharray="2,1"/>
  <text x="455" y="562" fill="#1C1C1C" font-size="9">Zona de conflito (CLA)</text>
  <line x1="440" y1="578" x2="450" y2="578" stroke="#1B4F72" stroke-width="2"/>
  <text x="455" y="582" fill="#1C1C1C" font-size="9">Rios principais</text>
  <text x="435" y="608" fill="#999" font-size="7">Fonte: Fund. Palmares, 2024</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Thematic map of Maranhao state, Brazil, showing distribution of quilombo communities. Deep purple (#5E3A7E) dots clustered in three main areas: Alcantara coast (200+ communities, densest cluster), Baixada Maranhense lowlands (central-west, around lakes and wetlands), and Itapecuru River valley (central-east, along river). Rivers shown in navy blue. One golden dot marking Frechal quilombo as pioneer. Small red-orange zone near Alcantara marking space launch center conflict. Clean cartographic style, parchment-toned background, modern editorial infographic. Total: 1,152 certified communities. Legend in corner."
**Estilo**: Cartografia tematica editorial — entre mapa e infografico
**Referencia**: Mapas do INCRA sobre comunidades quilombolas; Atlas Social do Maranhao
**NAO incluir**: Texto definitivo em ingles (sera em portugues pelo designer), fronteiras municipais detalhadas

---

---
id: VIS-V35-B
verbete: V35
tipo: infografico
posicao: meia-pagina
---

# Visual V35-B: A distancia entre certificacao e titulacao

## 1. Briefing para designer
**O que e**: Infografico mostrando o abismo entre comunidades certificadas e comunidades tituladas no Maranhao. Funil visual: 1.152 entram no topo (certificacao), menos de 10% saem na base (titulacao). Meia pagina.
**Dados**:
- 1.152 comunidades certificadas (FCP, 2024)
- Processo: autoidentificacao → certificacao (Palmares) → laudo antropologico (INCRA) → levantamento fundiario → contestacoes → titulacao
- Resultado: ~10% com titulo definitivo
- Tempo medio estimado: 10-20 anos por processo
**Referencia de estilo**: Funil/pipeline com etapas, mostrando perda em cada fase
**Paleta**: Roxo-tambor (#5E3A7E) para quilombos, Cinza (#999) para burocracia, Vermelho (#BA4A00) para gargalo/contestacoes, Dourado (#D4AC0D) para as que chegam ao titulo
**Tamanho**: Meia pagina (~11x14 cm)

## 2. SVG simplificado
**Elementos**: Funil vertical — topo largo (1.152 certificadas), estreitando em cada etapa burocratica, base estreita (~10% tituladas). Etapas rotuladas na lateral. Setas indicando contestacoes judiciais como ponto de perda.
**Layout**: Vertical, leitura de cima para baixo

## 3. Prompt para IA generativa
**Prompt**: "Clean infographic showing a funnel/pipeline of quilombo land titling process in Maranhao, Brazil. Top of funnel: wide bar in deep purple showing 1,152 certified communities. Middle stages narrowing: anthropological report, land survey, legal challenges (shown in red as bottleneck). Bottom of funnel: thin golden bar showing approximately 10% with definitive title. Each stage labeled with text. Style: modern editorial infographic, minimal colors (purple, gray, red, gold on cream background). Data annotation: '1988: Constitution promised. 2024: most still waiting.'"
**Estilo**: Infografico editorial moderno — funil de conversao adaptado
**NAO incluir**: Texto em ingles definitivo, imagens de pessoas

---

---
id: VIS-V35-C
verbete: V35
tipo: foto-editorial
posicao: corpo
---

# Visual V35-C: Sugestao de fotografia — vida quilombola

## 1. Briefing para designer / editor de foto
**O que e**: Fotografia editorial mostrando vida cotidiana em comunidade quilombola do Maranhao — nao evento cultural, nao pose, nao folclore. O cotidiano: roca, quebra de coco, canoa, escola. Meia pagina ou terco de pagina.
**Orientacao**:
- Priorizar fotografias que mostrem atividade produtiva (quebra de babacu, pesca, roça)
- Evitar cliches: nada de "sorriso de pobreza", nada de "autenticidade exotica"
- Ideal: mulher quebrando coco babacu, ou canoa em lago da Baixada, ou roda de Tambor de Crioula em contexto comunitario (nao palco)
- Credito obrigatorio ao fotografo
**Paleta**: Tons naturais — verde-mata, marrom-terra, azul-agua. Acento roxo-tambor na diagramacao
**Tamanho**: Meia pagina (~11x14 cm) ou faixa horizontal

## 2. Fontes de imagem sugeridas
- Acervo INCRA (imagens de titulacao e comunidades)
- Acervo MIQCB (quebradeiras de coco quilombolas)
- Fotografos maranhenses: buscar creditos locais
- Banco de imagens: evitar — preferir fotografias autorais

## 3. Prompt para IA generativa (referencia, NAO substituicao de foto real)
**Prompt**: "Documentary-style photograph of daily life in a quilombo community in Maranhao, Brazil. A woman breaking babassu coconuts under a palm-leaf shelter, surrounded by children playing nearby. Background shows tropical wetland landscape with palm trees and a small lake. Golden afternoon light. Style: photojournalistic, warm tones, dignified portrayal of rural life. NOT posed, NOT touristic, NOT folkloric."
**NOTA**: Este prompt e apenas referencia visual para o designer. A imagem final DEVE ser fotografia real, creditada, de comunidade quilombola do Maranhao. IA generativa nao substitui fotografia documental neste caso.
