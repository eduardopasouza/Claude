---
id: VIS-V82-A
verbete: V82
tipo: infografico
posicao: pagina-inteira
---

# Visual V82-A: Timeline dos quatro ciclos economicos

## 1. Briefing para designer
**O que e**: Timeline horizontal mostrando os quatro grandes ciclos economicos do Maranhao do seculo XVII ao XXI, com ciclos menores abaixo. Eixo temporal na base, com grossura da barra proporcional ao impacto economico.
**Dados**: Drogas do sertao (1620-1780), Algodao (1780-1870), Arroz (1770-1888), Ferro/Soja (1985-presente). Menores: Cana (1620-presente, fina), Babacu (1900-presente), Pecuaria (1950-presente).
**Paleta**: Ocre #C8952E dominante. Dourado para periodos de auge, cinza para declinio, vermelho para momentos de crise.
**Tamanho**: Pagina inteira (23x28cm landscape)
**Referencia**: Estilo National Geographic timelines, clean, tipografia moderna.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 1200 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Eixo temporal -->
  <line x1="50" y1="350" x2="1150" y2="350" stroke="#2B2B2B" stroke-width="2"/>
  <!-- Marcas seculares -->
  <text x="150" y="380" fill="#666" font-size="14">1600</text>
  <text x="350" y="380" fill="#666" font-size="14">1700</text>
  <text x="550" y="380" fill="#666" font-size="14">1800</text>
  <text x="750" y="380" fill="#666" font-size="14">1900</text>
  <text x="950" y="380" fill="#666" font-size="14">2000</text>
  <!-- Drogas do sertao -->
  <rect x="170" y="200" width="280" height="60" rx="5" fill="#C8952E" opacity="0.7"/>
  <text x="200" y="235" fill="white" font-size="13" font-weight="bold">Drogas do Sertao</text>
  <!-- Algodao -->
  <rect x="430" y="140" width="220" height="80" rx="5" fill="#D4A843"/>
  <text x="470" y="185" fill="white" font-size="13" font-weight="bold">Algodao</text>
  <!-- Arroz -->
  <rect x="410" y="230" width="230" height="50" rx="5" fill="#A67B2E" opacity="0.8"/>
  <text x="470" y="260" fill="white" font-size="13" font-weight="bold">Arroz</text>
  <!-- Ferro/Soja -->
  <rect x="850" y="140" width="280" height="80" rx="5" fill="#8B0000"/>
  <text x="900" y="185" fill="white" font-size="13" font-weight="bold">Ferro + Soja</text>
  <!-- Babacu (menor) -->
  <rect x="700" y="300" width="350" height="25" rx="3" fill="#2D6A4F" opacity="0.6"/>
  <text x="820" y="317" fill="white" font-size="11">Babacu</text>
  <!-- Legenda -->
  <text x="50" y="450" fill="#333" font-size="12">Grossura = impacto economico relativo</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt (Midjourney/DALL-E)**:
"Elegant horizontal timeline infographic showing four economic cycles of Maranhao Brazil, spanning 1600-2025. Left to right: tropical forest products (green, jungle motifs), cotton (white fibers, Manchester factories), rice (golden paddies), iron ore and soybeans (red rust, modern port). Each era connected by a fading arrow. Below main timeline, smaller bars for minor cycles: babassu palm, sugarcane, cattle. Color palette: ochre #C8952E, gold, dark red, forest green. Clean modern design, National Geographic editorial style, white background, no text overlay. --ar 16:9 --v 6"

**NAO incluir**: Rostos, bandeiras, logotipos, textos embutidos.

---

---
id: VIS-V82-B
verbete: V82
tipo: infografico
posicao: meia-pagina
---

# Visual V82-B: O que ficou de cada ciclo

## 1. Briefing para designer
**O que e**: Quatro colunas comparativas — cada uma representando um ciclo. Embaixo de cada coluna: "O que ficou". Contraste visual entre a riqueza gerada e o legado.
**Dados**: Drogas → floresta devastada. Algodao → casaroes em ruina. Arroz → tecnica apagada. Ferro/Soja → cerrado desmatado + CFEM irrisoria.
**Paleta**: Dourado na parte superior (riqueza), cinza/preto na inferior (legado).
**Tamanho**: Meia pagina.

## 2. SVG esquematico

```svg
<svg viewBox="0 0 800 400" xmlns="http://www.w3.org/2000/svg">
  <!-- Colunas -->
  <rect x="50" y="50" width="150" height="120" fill="#C8952E" rx="5"/>
  <text x="75" y="110" fill="white" font-size="12" font-weight="bold">Drogas do Sertao</text>
  <rect x="50" y="180" width="150" height="80" fill="#555" rx="5"/>
  <text x="60" y="220" fill="white" font-size="10">Floresta devastada</text>

  <rect x="230" y="30" width="150" height="140" fill="#D4A843" rx="5"/>
  <text x="270" y="100" fill="white" font-size="12" font-weight="bold">Algodao</text>
  <rect x="230" y="180" width="150" height="80" fill="#555" rx="5"/>
  <text x="240" y="220" fill="white" font-size="10">Casaroes em ruina</text>

  <rect x="410" y="40" width="150" height="130" fill="#A67B2E" rx="5"/>
  <text x="460" y="105" fill="white" font-size="12" font-weight="bold">Arroz</text>
  <rect x="410" y="180" width="150" height="80" fill="#555" rx="5"/>
  <text x="420" y="220" fill="white" font-size="10">Tecnica apagada</text>

  <rect x="590" y="20" width="150" height="150" fill="#8B0000" rx="5"/>
  <text x="615" y="95" fill="white" font-size="12" font-weight="bold">Ferro/Soja</text>
  <rect x="590" y="180" width="150" height="80" fill="#555" rx="5"/>
  <text x="600" y="215" fill="white" font-size="10">Cerrado desmatado</text>
  <text x="600" y="235" fill="white" font-size="10">CFEM irrisoria</text>

  <!-- Labels -->
  <text x="350" y="30" fill="#C8952E" font-size="14" font-weight="bold">RIQUEZA GERADA</text>
  <text x="350" y="290" fill="#555" font-size="14" font-weight="bold">O QUE FICOU</text>
</svg>
```

## 3. Prompt de IA generativa

**Prompt**: "Four columns infographic comparing extraction cycles: tropical forest products, cotton bales, rice paddies, iron ore train. Top half shows wealth (golden tones, abundance). Bottom half shows legacy (grey tones, ruins, deforestation). Split design, contrast between prosperity and aftermath. Ochre and grey palette, editorial style, clean layout. --ar 4:3 --v 6"

**NAO incluir**: Rostos, bandeiras, textos embutidos.
