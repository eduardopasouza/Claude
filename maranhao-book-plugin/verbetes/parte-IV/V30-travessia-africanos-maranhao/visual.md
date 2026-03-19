---
id: VIS-V30-A
verbete: V30
tipo: mapa
posicao: página-inteira
---

# Visual V30-A: Mapa das rotas do tráfico atlântico para o Maranhão

## 1. Briefing para designer
**O que é**: Mapa do Atlântico mostrando as três rotas do tráfico de escravizados para o Maranhão — Alta Guiné como principal (88%), Golfo do Benin como secundária, Angola como minoritária (12%). Visual principal do verbete, página inteira.
**Dados**:
- Rota principal: Bissau/Cacheu → São Luís (seta grossa, 88% do fluxo)
- Rota secundária: Costa da Mina (Golfo do Benin) → São Luís (seta média, pós-1810)
- Rota terciária: Luanda/Benguela → São Luís (seta fina, 12%)
- Rota triangular: Lisboa → Guiné → São Luís → Lisboa (linha pontilhada)
- Portos de embarque: Bissau, Cacheu, Cabo Verde (entreposto), Elmina, Luanda, Benguela
- Porto de desembarque: São Luís
- Dados nos tooltips: 114.000 total (1755-1820); 20,22% mortalidade; ~3 semanas de travessia
**Referência de estilo**: Mapas do Trans-Atlantic Slave Trade Database (slavevoyages.org) — setas proporcionais ao volume, estilo cartográfico limpo
**Paleta**: Azul-mar (#1B4F72) para oceano, Terracota (#BA4A00) para costa africana, Dourado-babaçu (#D4AC0D) para rotas/setas, Preto-mangue (#1C1C1C) para texto
**Tamanho**: Página inteira (23×28 cm)

## 2. SVG simplificado
**Elementos**:
- Contornos simplificados da costa ocidental africana e costa nordeste brasileira
- 3 setas curvas cruzando o Atlântico (espessura proporcional ao volume)
- Pontos marcando portos de embarque e desembarque
- Legendas com dados
**Layout**: Horizontal, África à direita, Brasil à esquerda, Atlântico no centro

```svg
<svg viewBox="0 0 800 500" xmlns="http://www.w3.org/2000/svg">
  <!-- Oceano -->
  <rect width="800" height="500" fill="#1B4F72" opacity="0.15"/>

  <!-- Costa africana (simplificada) -->
  <path d="M550,50 L580,100 L600,150 L590,200 L610,250 L620,300 L600,350 L580,400 L560,450" fill="none" stroke="#BA4A00" stroke-width="3"/>

  <!-- Costa brasileira (simplificada) -->
  <path d="M200,80 L180,120 L160,180 L140,250 L150,320 L170,380 L200,440" fill="none" stroke="#1E8449" stroke-width="3"/>

  <!-- Rota principal: Alta Guiné → São Luís (88%) -->
  <path d="M570,160 C400,100 300,120 190,150" fill="none" stroke="#D4AC0D" stroke-width="6" opacity="0.9"/>
  <text x="380" y="100" fill="#D4AC0D" font-size="12" font-weight="bold">88% — Alta Guiné</text>

  <!-- Rota secundária: Golfo do Benin → São Luís -->
  <path d="M600,250 C420,200 300,180 190,155" fill="none" stroke="#D4AC0D" stroke-width="3" opacity="0.6"/>
  <text x="400" y="210" fill="#D4AC0D" font-size="10">Golfo do Benin (pós-1810)</text>

  <!-- Rota terciária: Angola → São Luís (12%) -->
  <path d="M580,380 C400,350 280,280 185,170" fill="none" stroke="#D4AC0D" stroke-width="1.5" opacity="0.4"/>
  <text x="380" y="340" fill="#D4AC0D" font-size="10">12% — Angola</text>

  <!-- Rota triangular Lisboa (pontilhada) -->
  <path d="M500,50 L570,150" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>
  <path d="M190,150 L500,50" fill="none" stroke="#999" stroke-width="1" stroke-dasharray="5,5"/>

  <!-- Portos de embarque -->
  <circle cx="570" cy="155" r="5" fill="#BA4A00"/>
  <text x="580" y="150" fill="#BA4A00" font-size="9">Bissau</text>
  <circle cx="565" cy="140" r="4" fill="#BA4A00"/>
  <text x="575" y="135" fill="#BA4A00" font-size="9">Cacheu</text>
  <circle cx="600" cy="245" r="4" fill="#BA4A00"/>
  <text x="610" y="240" fill="#BA4A00" font-size="9">Costa da Mina</text>
  <circle cx="585" cy="370" r="4" fill="#BA4A00"/>
  <text x="595" y="365" fill="#BA4A00" font-size="9">Luanda</text>

  <!-- Porto de desembarque -->
  <circle cx="188" cy="152" r="6" fill="#1E8449"/>
  <text x="130" y="148" fill="#1E8449" font-size="10" font-weight="bold">São Luís</text>

  <!-- Lisboa -->
  <circle cx="500" cy="50" r="4" fill="#999"/>
  <text x="510" y="47" fill="#999" font-size="9">Lisboa</text>

  <!-- Dados -->
  <text x="20" y="30" fill="#1C1C1C" font-size="14" font-weight="bold">Rotas do tráfico para o Maranhão</text>
  <text x="20" y="470" fill="#1C1C1C" font-size="10">114.000 africanos (1755-1820) · Mortalidade: 20% · Travessia: ~3 semanas</text>
</svg>
```

## 3. Prompt para IA generativa
**Prompt**: "Historical map of Atlantic slave trade routes to Maranhão, Brazil. Dark blue Atlantic Ocean. Western African coast on the right showing ports of Bissau, Cacheu (Guinea-Bissau), Gold Coast (Gulf of Benin), and Luanda (Angola). Brazilian northeast coast on the left showing São Luís as main disembarkation port. Three curved golden arrows crossing the Atlantic: one very thick from Guinea-Bissau (88% of traffic), one medium from Gulf of Benin, one thin from Angola (12%). Triangular route shown with dotted line: Lisbon to Guinea to São Luís to Lisbon. Clean cartographic style, parchment-like background, aged map aesthetic but with modern data visualization. Color palette: deep navy ocean, terracotta for African coast, golden arrows, dark green for Brazilian coast."
**Estilo**: Cartografia histórica com dados modernos — estilo entre mapa antigo e infográfico
**Referência**: Mapas do slavevoyages.org; mapas coloniais portugueses
**NÃO incluir**: Texto definitivo em inglês (será em português pelo designer), imagens de violência

---

---
id: VIS-V30-B
verbete: V30
tipo: infográfico
posicao: meia-página
---

# Visual V30-B: Transformação demográfica — antes e depois de Pombal

## 1. Briefing para designer
**O que é**: Infográfico mostrando a transformação demográfica do Maranhão causada pelo tráfico escravista — de 34 africanos/ano (pré-1755) a 55,3% da população escravizada (1821). Meia página.
**Dados**:
- Pré-1755: 34 escravos/ano, economia indígena-mestiça
- 1755-1778: Companhia ativa. 31.317 embarcados, 24.985 sobreviventes
- 1788-1842: 77.083 escravos (boom algodoeiro)
- 1821: 152.893 pop. total → 84.534 escravizados (55,3%)
- Vale do Itapecuru: até 80% "de cor"
**Referência de estilo**: Gráfico de barras empilhadas + timeline, estilo editorial limpo
**Paleta**: Terracota (#BA4A00) para população escravizada, Branco-areia (#F5F5DC) para população livre, Dourado (#D4AC0D) para marcos temporais
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**: Timeline horizontal (1680-1850), barras verticais empilhadas em 4-5 pontos temporais mostrando proporção livre/escravizada, marcos textuais (Companhia 1755, Abolição indígena, boom algodão, pico 1821)
**Layout**: Horizontal, leitura esquerda-direita

## 3. Prompt para IA generativa
**Prompt**: "Clean infographic showing demographic transformation of Maranhão, Brazil from 1680 to 1850. Horizontal timeline. Stacked bar chart at key dates showing proportion of enslaved (terracotta color) vs free population (cream/beige). Key milestones marked: 1755 (Pombal's Company created), 1778 (Company dissolved), 1821 (peak: 55.3% enslaved). Small text labels. Before 1755: tiny bars. After 1755: dramatic growth. Modern editorial infographic style, clean typography, minimal color palette: terracotta, cream, dark text."
**Estilo**: Infográfico editorial moderno
**NÃO incluir**: Imagens de pessoas, texto final em inglês

---

---
id: VIS-V30-C
verbete: V30
tipo: mapa
posicao: corpo
---

# Visual V30-C: Origens étnicas na costa africana

## 1. Briefing para designer
**O que é**: Mapa da costa ocidental africana mostrando as regiões de origem dos escravizados que vieram para o Maranhão, com etnias principais e legados culturais associados. Meia página.
**Dados**:
- Alta Guiné (Bissau/Cacheu): Balanta, Bijago, Papel, Mandinga, Fula → Legado: arroz, bolsas de mandinga, islã
- Golfo do Benin (Costa da Mina): Jeje (Fon), Nagô (Iorubá), Mina → Legado: Tambor de Mina, Casa das Minas
- África Central (Angola/Congo): Banto genérico → Legado: Tambor de Crioula, Terecô
**Referência de estilo**: Mapa étnico/cultural, estilo National Geographic — regiões coloridas com ícones dos legados
**Paleta**: Verde-mangue (#1E8449) para Alta Guiné, Dourado (#D4AC0D) para Golfo do Benin, Terracota (#BA4A00) para Angola/Congo
**Tamanho**: Meia página (~11×14 cm)

## 2. SVG simplificado
**Elementos**: Costa africana ocidental com 3 regiões coloridas, nomes de etnias dentro de cada região, setas/ícones conectando a legados culturais no canto
**Layout**: Vertical (norte a sul), com sidebar de legados

## 3. Prompt para IA generativa
**Prompt**: "Map of West African coast showing three source regions of enslaved Africans brought to Maranhão, Brazil. Upper Guinea (Guinea-Bissau area) in green with ethnic labels: Balanta, Mandinga, Bijago, Fula. Gulf of Benin (Ghana-Benin-Nigeria) in golden with labels: Jeje/Fon, Nago/Yoruba. Central Africa (Angola-Congo) in terracotta with label: Bantu groups. Each region connected by arrow to cultural legacy icon: rice grain for Guinea, drum for Benin (Tambor de Mina), dancing figure for Angola (Tambor de Crioula). Clean cartographic style, educational, colorful but restrained."
**Estilo**: Cartografia educacional moderna
**NÃO incluir**: Fronteiras nacionais modernas (anacronismo), texto final
