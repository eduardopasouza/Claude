---
id: VIS-V63-A
verbete: V63
tipo: infografico
posicao: pagina-inteira
---

# Visual V63-A: As tres mesas — ingredientes, tecnicas e fusao

## 1. Briefing para designer
**O que e**: Infografico de pagina inteira mostrando as tres matrizes culinarias do Maranhao. Tres colunas verticais (INDIGENA | AFRICANA | PORTUGUESA), cada uma com: ingredientes-chave (icones ilustrados), tecnicas culinarias, pratos tipicos. No centro-inferior, uma zona de convergencia ("FUSAO") onde os pratos hibridos aparecem — arroz de cuxa, vatapa MA, peixada, tiquira — com setas indicando quais ingredientes vem de qual coluna.
**Dados**: Coluna indigena: mandioca (farinha, tucupi, tapioca, tiquira), peixe, jucara, bacuri, buriti, pimenta. Coluna africana: arroz (Oryza glaberrima), vinagreira/cuxa, dende, quiabo, gergelim, feijao-fradinho. Coluna portuguesa: alho, cebola, coentro, camarao seco, arroz (Oryza sativa), doces conventuais, gado bovino. Zona de fusao: arroz de cuxa (3 setas), vatapa MA, caruru MA, peixada, torta de camarao, jucara com farinha.
**Referencia de estilo**: Infografico editorial tipo National Geographic — ilustrado, nao fotografico. Icones de ingredientes desenhados, nao fotos. Fundo cor Areia (#E8D5B7).
**Paleta**: Terracota (#B5533E) para moldura e titulos. Verde-mata (#2D6A4F) para coluna indigena. Roxo-tambor (#5E3A7E) para coluna africana. Azul-mar (#1B4965) para coluna portuguesa. Ocre (#C8952E) para zona de fusao.
**Tamanho**: Pagina inteira (23x28cm)

## 2. SVG simplificado
**Elementos**: 3 retangulos verticais (colunas) com titulos, lista de ingredientes como texto, zona de convergencia como retangulo horizontal no terco inferior com setas diagonais descendo das colunas
**Layout**: 3 colunas ocupam 2/3 superiores da pagina. Zona de fusao ocupa 1/3 inferior. Setas convergem das 3 colunas para os pratos hibridos.
**Cores**: Verde #2D6A4F, Roxo #5E3A7E, Azul #1B4965, Ocre #C8952E, fundo #E8D5B7

```svg
<svg viewBox="0 0 800 1000" xmlns="http://www.w3.org/2000/svg">
  <rect width="800" height="1000" fill="#E8D5B7"/>
  <!-- Titulo -->
  <text x="400" y="50" text-anchor="middle" font-size="28" fill="#B5533E" font-weight="bold">AS TRES MESAS</text>
  <!-- Coluna Indigena -->
  <rect x="20" y="80" width="240" height="550" rx="10" fill="#2D6A4F" opacity="0.15" stroke="#2D6A4F" stroke-width="2"/>
  <text x="140" y="115" text-anchor="middle" font-size="18" fill="#2D6A4F" font-weight="bold">INDIGENA</text>
  <text x="40" y="150" font-size="13" fill="#2B2B2B">Mandioca (farinha, tucupi,</text>
  <text x="40" y="170" font-size="13" fill="#2B2B2B">tapioca, tiquira)</text>
  <text x="40" y="200" font-size="13" fill="#2B2B2B">Peixe (moquem)</text>
  <text x="40" y="230" font-size="13" fill="#2B2B2B">Jucara / Bacuri / Buriti</text>
  <text x="40" y="260" font-size="13" fill="#2B2B2B">Pimenta</text>
  <text x="40" y="290" font-size="13" fill="#2B2B2B">Mel / Castanhas</text>
  <text x="40" y="330" font-size="14" fill="#2D6A4F" font-weight="bold">Tecnicas:</text>
  <text x="40" y="355" font-size="12" fill="#2B2B2B">Tipiti (prensa de fibra)</text>
  <text x="40" y="375" font-size="12" fill="#2B2B2B">Moquem (assar na folha)</text>
  <text x="40" y="395" font-size="12" fill="#2B2B2B">Forno de barro</text>
  <!-- Coluna Africana -->
  <rect x="280" y="80" width="240" height="550" rx="10" fill="#5E3A7E" opacity="0.15" stroke="#5E3A7E" stroke-width="2"/>
  <text x="400" y="115" text-anchor="middle" font-size="18" fill="#5E3A7E" font-weight="bold">AFRICANA</text>
  <text x="300" y="150" font-size="13" fill="#2B2B2B">Arroz (Oryza glaberrima)</text>
  <text x="300" y="180" font-size="13" fill="#2B2B2B">Vinagreira (cuxa)</text>
  <text x="300" y="210" font-size="13" fill="#2B2B2B">Azeite de dende</text>
  <text x="300" y="240" font-size="13" fill="#2B2B2B">Quiabo</text>
  <text x="300" y="270" font-size="13" fill="#2B2B2B">Gergelim</text>
  <text x="300" y="300" font-size="13" fill="#2B2B2B">Feijao-fradinho</text>
  <text x="300" y="340" font-size="14" fill="#5E3A7E" font-weight="bold">Tecnicas:</text>
  <text x="300" y="365" font-size="12" fill="#2B2B2B">Fritura em oleo vegetal</text>
  <text x="300" y="385" font-size="12" fill="#2B2B2B">Folhas cozidas</text>
  <text x="300" y="405" font-size="12" fill="#2B2B2B">Pilao</text>
  <!-- Coluna Portuguesa -->
  <rect x="540" y="80" width="240" height="550" rx="10" fill="#1B4965" opacity="0.15" stroke="#1B4965" stroke-width="2"/>
  <text x="660" y="115" text-anchor="middle" font-size="18" fill="#1B4965" font-weight="bold">PORTUGUESA</text>
  <text x="560" y="150" font-size="13" fill="#2B2B2B">Alho / Cebola / Coentro</text>
  <text x="560" y="180" font-size="13" fill="#2B2B2B">Arroz (Oryza sativa)</text>
  <text x="560" y="210" font-size="13" fill="#2B2B2B">Camarao seco (salga)</text>
  <text x="560" y="240" font-size="13" fill="#2B2B2B">Gado bovino</text>
  <text x="560" y="270" font-size="13" fill="#2B2B2B">Acucar / Doces conventuais</text>
  <text x="560" y="300" font-size="13" fill="#2B2B2B">Leite / Queijo</text>
  <text x="560" y="340" font-size="14" fill="#1B4965" font-weight="bold">Tecnicas:</text>
  <text x="560" y="365" font-size="12" fill="#2B2B2B">Cozimento lento (ensopado)</text>
  <text x="560" y="385" font-size="12" fill="#2B2B2B">Conserva de sal</text>
  <text x="560" y="405" font-size="12" fill="#2B2B2B">Panificacao / Confeitaria</text>
  <!-- Setas de convergencia -->
  <line x1="140" y1="630" x2="300" y2="720" stroke="#2D6A4F" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="400" y1="630" x2="400" y2="720" stroke="#5E3A7E" stroke-width="2" marker-end="url(#arrow)"/>
  <line x1="660" y1="630" x2="500" y2="720" stroke="#1B4965" stroke-width="2" marker-end="url(#arrow)"/>
  <!-- Zona de fusao -->
  <rect x="100" y="700" width="600" height="250" rx="15" fill="#C8952E" opacity="0.2" stroke="#C8952E" stroke-width="3"/>
  <text x="400" y="740" text-anchor="middle" font-size="22" fill="#C8952E" font-weight="bold">FUSAO: SO NO MARANHAO</text>
  <text x="400" y="780" text-anchor="middle" font-size="15" fill="#2B2B2B" font-weight="bold">Arroz de cuxa</text>
  <text x="400" y="800" text-anchor="middle" font-size="12" fill="#2B2B2B">arroz + vinagreira + camarao seco + gergelim + farinha</text>
  <text x="200" y="840" text-anchor="middle" font-size="14" fill="#2B2B2B">Vatapa MA</text>
  <text x="400" y="840" text-anchor="middle" font-size="14" fill="#2B2B2B">Peixada</text>
  <text x="600" y="840" text-anchor="middle" font-size="14" fill="#2B2B2B">Tiquira</text>
  <text x="200" y="880" text-anchor="middle" font-size="14" fill="#2B2B2B">Caruru MA</text>
  <text x="400" y="880" text-anchor="middle" font-size="14" fill="#2B2B2B">Torta de camarao</text>
  <text x="600" y="880" text-anchor="middle" font-size="14" fill="#2B2B2B">Jucara c/ farinha</text>
  <defs><marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M 0 0 L 10 5 L 0 10 z" fill="#2B2B2B"/></marker></defs>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Editorial infographic illustration of three culinary traditions merging into one. Three columns representing Indigenous (green, showing cassava, fish, jungle fruits), African (purple, showing rice fields, palm oil, hibiscus leaves), and Portuguese (blue, showing garlic, salt cod, sugar) traditions. At the bottom, a large wooden table where all ingredients come together into fusion dishes. Style: warm, hand-illustrated, editorial, watercolor textures. Color palette: terracotta, sage green, deep purple, ocean blue, golden ochre. 23x28cm vertical format. No text. No people."
**Estilo**: Ilustracao editorial aquarelada, tipo revista de gastronomia premium
**Referencia**: Infograficos do New York Times Food section; ilustracoes de Wendy MacNaughton
**NAO incluir**: fotografias, pessoas reconheciveis, logotipos, bandeiras nacionais

---

---
id: VIS-V63-B
verbete: V63
tipo: mapa
posicao: corpo
---

# Visual V63-B: Mapa dos ingredientes — de onde vem cada um

## 1. Briefing para designer
**O que e**: Mapa esquematico do Maranhao mostrando a origem geografica dos ingredientes-chave. Mandioca e frutas nativas (interior/pre-amazonia). Vinagreira (cultivada nas hortas periurbanas de Sao Luis). Camarao (litoral — baias e estuarios). Jucara (matas de varzea do oeste). Bacuri (pre-amazonia oriental). Buriti (cerrado sul). Arroz (varzeas do Itapecuru, Mearim, Pindaré). Gado (sertao sul/leste).
**Dados**: Posicoes aproximadas no mapa do estado. Icones de cada ingrediente na regiao correspondente. Setas mostrando fluxo para Sao Luis (centro de consumo).
**Paleta**: Fundo Areia (#E8D5B7). Mapa em tracos Carvao (#2B2B2B). Icones coloridos conforme matriz: verde (indigena), roxo (africana), azul (portuguesa).
**Tamanho**: Meia pagina

## 2. SVG simplificado
**Elementos**: Contorno do Maranhao, pontos marcados com nome do ingrediente, setas convergindo para Sao Luis
**Layout**: Mapa centralizado, legendas nas margens

## 3. Prompt para IA generativa
**Prompt**: "Hand-drawn illustrated map of Maranhao state, Brazil, showing origins of traditional ingredients. Cassava in the interior, shrimp on the coast, rice in the river valleys, acai/jucara in the western forests, buriti in the southern savanna. Small watercolor icons for each ingredient. Warm color palette, vintage cartography style with modern illustration. Terracotta and ochre tones. No text labels (will be added separately). Vertical orientation."
**Estilo**: Cartografia ilustrada estilo atlas vintage
**Referencia**: Herb Lester Associates travel maps; They Draw & Travel
**NAO incluir**: fronteiras politicas detalhadas, cidades menores, estradas
