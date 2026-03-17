# Visual Briefing — 1.1 "A Encruzilhada: três biomas, dois mundos, um estado"

**Derivado de:** Cap. 01 — A Terra, Tópico 1.1
**Data:** 2026-03-17
**Destinatário:** Designer / Ilustrador
**Contexto:** O Maranhão (329.651 km²) é o único estado brasileiro onde três biomas se encontram. Fica na fronteira entre o Norte (Amazônia) e o Nordeste (Cerrado/Caatinga). Este tópico abre o livro inteiro — os visuais precisam causar impacto imediato e traduzir a ideia central de "encruzilhada".

---

## Asset 1 — Mapa dos 3 Biomas

**Código:** `VIS-1.1-A`
**Prioridade:** Must-have (imagem principal do tópico)

### Formato e Dimensões
- **Tipo:** Página inteira (full page), orientação retrato.
- **Proporção:** Aproximadamente 170 × 240 mm (mancha útil de livro 16 × 23 cm). Prever versão digital em alta resolução (300 dpi, PNG/SVG).
- Deve funcionar também reduzido a 50% para uso em redes sociais.

### Descrição
Mapa do estado do Maranhão preenchido pelas áreas dos três biomas, com a silhueta do estado bem definida. O mapa deve ser limpo, vetorial, com estética inspirada no estúdio **Kurzgesagt** — cores sólidas, formas simplificadas, sem texturas fotográficas, tipografia moderna (sem serifa). Fundo: off-white ou cinza muito claro (#F5F5F0).

### Paleta de Cores

| Bioma     | Cor principal           | Hex sugerido | Área  |
|-----------|-------------------------|--------------|-------|
| Amazônia  | Verde-floresta denso    | #2D6A4F      | 35%   |
| Cerrado   | Ocre / dourado quente   | #D4A843      | 64%   |
| Caatinga  | Terracota / tijolo seco | #C4624A      | 1%    |

- Usar variações de saturação (mais claro no interior, mais escuro nas bordas) para dar profundidade sem perder a limpeza.
- Contorno do estado: linha fina cinza-escuro (#333333), 1 pt.

### Overlay: Amazônia Legal
- Sobrepor ao mapa uma **linha tracejada branca ou cinza-claro** delimitando a área da Amazônia Legal dentro do Maranhão (181 dos 217 municípios — ~79,3% do território, a oeste do meridiano 44°W).
- Legenda da linha: "Amazônia Legal (79,3% do território)".
- A linha deve contrastar com os biomas sem competir visualmente. Sugestão: tracejado 4 px / 4 px, opacidade 70%.

### Rótulos e Textos
- Dentro de cada área de bioma, centralizado:
  - **"CERRADO — 64%"** (tipografia bold, corpo grande)
  - **"AMAZÔNIA — 35%"**
  - **"CAATINGA — 1%"** (corpo menor, com seta indicadora se a faixa for muito estreita no mapa)
- Rodapé do mapa: `Fonte: IBGE — Biomas (2019); Embrapa (2011)`
- Título superior (opcional, se houver espaço): "Três biomas, um estado"

### Referência de Estilo
- **Kurzgesagt — In a Nutshell** (YouTube): mapas vetoriais com gradientes suaves, paleta restrita, labels integrados ao corpo do mapa.
- Referência adicional: mapas do Our World in Data (ourworldindata.org) — clareza informacional acima de tudo.

### Notas Técnicas
- A Caatinga ocupa apenas a faixa leste extrema do estado (divisa com Piauí). É uma fatia muito fina — usar uma seta ou callout para garantir legibilidade.
- A transição Amazônia–Cerrado no centro do estado pode ser indicada por uma faixa de gradiente sutil ou por uma linha de transição rotulada "Mata dos Cocais (transição)".

---

## Asset 2 — Infográfico "O Mapa Dobrado"

**Código:** `VIS-1.1-B`
**Prioridade:** Must-have (imagem de abertura do livro)

### Formato e Dimensões
- **Tipo:** Página dupla (spread) ou página inteira sangrada (full bleed). É a primeira imagem que o leitor vê ao abrir o Capítulo 1.
- **Proporção:** 340 × 240 mm (spread) ou 170 × 240 mm (página inteira). Prever versão quadrada (1:1) para uso digital.

### Descrição Conceitual
Ilustração conceitual que traduz visualmente a metáfora do texto de abertura:

> "Dobre o mapa do Brasil em três. Uma dobra separando a Amazônia. Outra separando o Cerrado. Uma terceira isolando o Nordeste seco. Agora olhe para o ponto onde as três dobras se cruzam. É o Maranhão."

O mapa do Brasil aparece como se fosse uma **folha de papel sendo dobrada fisicamente** em três partes. As dobras criam três "abas" ou painéis:

1. **Aba esquerda (Oeste/Norte):** Amazônia — verde-floresta (#2D6A4F), com ícones sutis de árvores/copa de floresta.
2. **Aba central/sul:** Cerrado — ocre/dourado (#D4A843), com ícones sutis de árvores retorcidas típicas do cerrado.
3. **Aba direita (Leste):** Nordeste seco — terracota (#C4624A), com ícones sutis de cacto/solo rachado.

No **ponto exato onde as três dobras se cruzam**, o estado do Maranhão aparece em destaque — um brilho ou halo sutil ao redor da sua silhueta, como se ali fosse o "eixo" do papel dobrado. Pode haver uma leve sombra de dobra de papel para reforçar a tridimensionalidade.

### Paleta de Cores
- Mesma paleta do Asset 1 (verde-floresta, ocre, terracota).
- Fundo: branco puro ou off-white.
- Sombras da dobra: cinza neutro com baixa opacidade.
- Destaque no Maranhão: borda luminosa branca ou dourada sutil.

### Rótulos e Textos
- Em cada "aba" do mapa dobrado, um rótulo discreto:
  - "AMAZÔNIA"
  - "CERRADO"
  - "NORDESTE SECO"
- No ponto de cruzamento: **"MARANHÃO"** em destaque (bold, corpo maior).
- Não precisa de título — a imagem é autoexplicativa e será acompanhada pelo parágrafo de abertura do texto.

### Referência de Estilo
- Estética de **paper folding / origami infographic** — clean, tridimensional porém flat, com sombras mínimas.
- Referências visuais: ilustrações editoriais da revista *Monocle*, infográficos da *National Geographic* (versão simplificada), ou trabalhos do ilustrador **Malika Favre** (formas planas com sugestão de profundidade).
- Evitar: realismo fotográfico, texturas pesadas, excesso de detalhes cartográficos.

### Notas Técnicas
- A proporção geográfica do Brasil não precisa ser milimetricamente exata — é uma ilustração conceitual, não um mapa técnico. Mas a silhueta deve ser reconhecível.
- As "dobras" devem parecer naturais, como se alguém realmente dobrasse um papel. As linhas de dobra passam aproximadamente pelos limites dos biomas.
- O Maranhão deve ser o ponto focal inequívoco da composição. Considerar usar escala levemente exagerada para o estado.

---

## Asset 3 — Mapa de Localização

**Código:** `VIS-1.1-C`
**Prioridade:** Nice-to-have (pode ser integrado como inset no Asset 1)

### Formato e Dimensões
- **Tipo:** Inline ou quarter-page. Pode funcionar como inset (caixa menor) dentro do Asset 1, no canto inferior direito.
- **Proporção:** ~80 × 80 mm (quadrado ou levemente retrato).

### Descrição
Mapa simplificado do Brasil inteiro, com todos os estados delineados em cinza claro. O Maranhão aparece em destaque (preenchido em cor sólida). Os estados vizinhos relevantes são rotulados:

- **Pará** (a oeste) — pertence à Região Norte.
- **Piauí** (a leste) — pertence à Região Nordeste.
- **Tocantins** (a sudoeste) — pertence à Região Norte.

O objetivo é mostrar visualmente que o Maranhão **fica exatamente na fronteira entre duas macrorregiões** do IBGE (Norte e Nordeste).

### Paleta de Cores

| Elemento                  | Cor                  | Hex sugerido |
|---------------------------|----------------------|--------------|
| Maranhão                  | Destaque forte       | #1B4332      |
| Estados da Região Norte   | Azul-acinzentado     | #A8DADC      |
| Estados da Região Nordeste| Bege/areia           | #E8D5B7      |
| Demais estados            | Cinza muito claro    | #E0E0E0      |
| Contornos                 | Cinza médio          | #999999      |

### Rótulos e Textos
- **"MARANHÃO"** — dentro ou ao lado do estado, bold.
- **"Pará"** — com indicação "(Região Norte)".
- **"Piauí"** — com indicação "(Região Nordeste)".
- **"Tocantins"** — com indicação "(Região Norte)".
- Linha divisória visual ou rótulo indicando: **"Limite Norte / Nordeste"** passando pela fronteira oeste do Maranhão.
- Legenda de cores: "Norte" / "Nordeste" / "Demais regiões".

### Referência de Estilo
- Mapa localizador clássico de atlas ou artigo acadêmico, porém com a mesma linguagem visual limpa dos demais assets.
- Referência: mapas localizadores da Wikipedia em SVG — simples, sem relevo, com foco na informação política/regional.

### Notas Técnicas
- Não incluir relevo, rios ou cidades — é um mapa puramente político/regional.
- Se usado como inset do Asset 1, reduzir para ~60 × 60 mm e eliminar rótulos secundários (manter apenas "MA", "PA", "PI" como siglas).
- Garantir que a diferença cromática entre Região Norte e Região Nordeste seja perceptível mesmo em impressão P&B (usar tons com luminosidade bem diferente).

---

## Diretrizes Gerais (todos os assets)

### Tipografia
- Família sem serifa, geométrica. Sugestões: **Inter**, **DM Sans**, **Outfit** ou **Nunito Sans**.
- Rótulos de mapa: peso medium ou semibold.
- Dados percentuais: peso bold.
- Fontes/créditos: peso regular, corpo reduzido (7–8 pt impresso).

### Entrega
- Formatos: **SVG** (editável) + **PNG 300 dpi** (para diagramação) + **PDF vetorial**.
- Organizar camadas nomeadas (biomas, labels, overlay, fundo).
- Versão light e dark mode para uso digital, se possível.

### Acessibilidade
- Garantir contraste mínimo WCAG AA entre cores de bioma e texto sobreposto.
- Não depender exclusivamente de cor para distinguir os biomas — usar também rótulos textuais e/ou padrões (hachura sutil) como fallback.
- Incluir alt-text sugerido para cada asset (para versão digital/e-book).

### Alt-texts sugeridos
- **Asset 1:** "Mapa do Maranhão dividido em três biomas: Cerrado (64%, em ocre), Amazônia (35%, em verde) e Caatinga (1%, em terracota), com sobreposição da fronteira da Amazônia Legal."
- **Asset 2:** "Ilustração conceitual do mapa do Brasil dobrado em três partes — Amazônia, Cerrado e Nordeste seco — com o ponto de cruzamento das dobras no Maranhão."
- **Asset 3:** "Mapa do Brasil com o Maranhão em destaque, mostrando sua posição entre a Região Norte (Pará, Tocantins) e a Região Nordeste (Piauí)."

---

## Resumo de Prioridades

| Asset                        | Código     | Prioridade  | Formato         |
|------------------------------|------------|-------------|-----------------|
| Mapa dos 3 Biomas            | VIS-1.1-A  | Must-have   | Página inteira  |
| Infográfico "O Mapa Dobrado" | VIS-1.1-B  | Must-have   | Spread / página |
| Mapa de Localização          | VIS-1.1-C  | Nice-to-have| Inline / inset  |
