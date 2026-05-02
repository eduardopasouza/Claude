# Flag asset sources — sim-global

Bandeiras nacionais para o cenário Brasil/1930. Catálogo gerado em 2026-05-01.

## Egress note

A sandbox de execução bloqueia `upload.wikimedia.org`,
`commons.wikimedia.org` e `*.wikipedia.org` (resposta HTTP 403 com header
`x-block-reason: hostname_blocked`). As URLs canônicas do Wikimedia Commons
solicitadas no briefing **não puderam ser baixadas diretamente**. Para os 11
países, foram baixados os arquivos SVG correspondentes a partir do mirror PD
[`hampusborgos/country-flags`](https://github.com/hampusborgos/country-flags),
que re-hospeda os SVGs de bandeira nacionais do Wikimedia Commons sob a mesma
licença de domínio público. Esse mirror só contém a variante **atual** de cada
bandeira, então as variantes historicamente específicas pedidas no briefing
ficaram **PENDENTE** — listadas abaixo para download manual posterior.

## Catálogo

### Brasil (BRA)

- Caminho local: `data/catalog/flags/BRA.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/br.svg`
- Licença: Public Domain (mirror PD do Wikimedia Commons).
- Período coberto pelo arquivo baixado: bandeira atual (1992–presente). Os 26
  estados da bandeira atual diferem dos 21 da bandeira de 1889–1960, mas a
  composição visual é equivalente para uso em UI em escala pequena.
- **PENDENTE — variante histórica 1889-1960:**
  `https://upload.wikimedia.org/wikipedia/commons/0/05/Flag_of_Brazil_%281889-1960%29.svg`
  (egress bloqueia upload.wikimedia.org). Era a bandeira em uso durante toda a
  Era Vargas (1930-1945).

### Argentina (ARG)

- Caminho local: `data/catalog/flags/ARG.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/ar.svg`
- Licença: Public Domain.
- Período: bandeira atual; design oficialmente inalterado desde 1818 (com Sol
  de Mayo). Válida para 1930.
- URL Wikimedia original solicitada (PENDENTE no acesso direto):
  `https://upload.wikimedia.org/wikipedia/commons/1/1a/Flag_of_Argentina.svg`

### Uruguai (URY)

- Caminho local: `data/catalog/flags/URY.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/uy.svg`
- Licença: Public Domain.
- Período: design oficial desde 1830, inalterado. Válida para 1930.
- URL Wikimedia original (PENDENTE no acesso direto):
  `https://upload.wikimedia.org/wikipedia/commons/f/fe/Flag_of_Uruguay.svg`

### Paraguai (PRY)

- Caminho local: `data/catalog/flags/PRY.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/py.svg`
- Licença: Public Domain.
- Período: bandeira atual (proporções padronizadas em 2013), mas o desenho é
  do século XIX e estava em uso em 1930 com proporções ligeiramente diferentes.
- URL Wikimedia original (PENDENTE no acesso direto):
  `https://upload.wikimedia.org/wikipedia/commons/2/27/Flag_of_Paraguay.svg`

### Chile (CHL)

- Caminho local: `data/catalog/flags/CHL.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/cl.svg`
- Licença: Public Domain.
- Período: design oficial desde 1817, inalterado. Válida para 1930.
- URL Wikimedia original (PENDENTE no acesso direto):
  `https://upload.wikimedia.org/wikipedia/commons/7/78/Flag_of_Chile.svg`

### Bolívia (BOL)

- Caminho local: `data/catalog/flags/BOL.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/bo.svg`
- Licença: Public Domain.
- Período: bandeira de Estado (com brasão) atual; o desenho do brasão usado em
  1930 difere ligeiramente. Suficiente para UI.
- URL Wikimedia original (PENDENTE no acesso direto):
  `https://upload.wikimedia.org/wikipedia/commons/4/48/Flag_of_Bolivia.svg`

### Estados Unidos (USA)

- Caminho local: `data/catalog/flags/USA.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/us.svg`
- Licença: Public Domain.
- Período: bandeira atual de 50 estrelas (1960–presente). **Não corresponde
  ao período Vargas:** em 1930 estava em uso a bandeira de 48 estrelas
  (1912-1959).
- **PENDENTE — variante historicamente correta (48 estrelas):**
  `https://upload.wikimedia.org/wikipedia/commons/9/97/US_flag_48_stars.svg`
  (egress bloqueia upload.wikimedia.org).

### Reino Unido (GBR)

- Caminho local: `data/catalog/flags/GBR.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/gb.svg`
- Licença: Public Domain.
- Período: Union Jack atual; desenho inalterado desde 1801. Válida para 1930.
- URL Wikimedia original (PENDENTE no acesso direto):
  `https://upload.wikimedia.org/wikipedia/commons/a/ae/Flag_of_the_United_Kingdom.svg`

### Alemanha (DEU)

- Caminho local: `data/catalog/flags/DEU.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/de.svg`
- Licença: Public Domain.
- Período: tricolor atual (preto-vermelho-dourado), República Federal
  1949–presente. **Não corresponde ao período Vargas:** em 1930 a Alemanha de
  Weimar usava o tricolor preto-vermelho-dourado também (até 1933), depois o
  Reich nazista usou a bandeira da suástica (1935-1945) e, em transição
  1933-1935, uma combinação. Política do mirror omite bandeiras nazistas.
- **PENDENTE — variantes historicamente corretas:**
  - Weimar tardia / 1933-1935 transição preto-branco-vermelho:
    `https://upload.wikimedia.org/wikipedia/commons/1/1b/Flag_of_the_German_Empire.svg`
  - Reich 1935-1945 (suástica):
    `https://upload.wikimedia.org/wikipedia/commons/6/61/Flag_of_the_German_Reich_%281935%E2%80%931945%29.svg`
  Ambas pendentes por egress bloqueado. **Decisão de produto recomendada:**
  para um jogo histórico do período Vargas, considerar usar a variante
  preto-branco-vermelho (Reich/Weimar tardia), evitando iconografia nazista
  explícita. A inclusão da suástica é bloqueada por algumas plataformas e
  pode requerer decisão editorial.

### Itália (ITA)

- Caminho local: `data/catalog/flags/ITA.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/it.svg`
- Licença: Public Domain.
- Período: tricolor verde-branco-vermelho atual (República Italiana
  1948–presente). **Não corresponde ao período Vargas:** em 1930, sob o
  Reino da Itália (governo Mussolini), o tricolor incluía o brasão da Casa
  de Saboia centralizado.
- **PENDENTE — variante historicamente correta (Reino com brasão de Saboia,
  1861-1946):**
  `https://upload.wikimedia.org/wikipedia/commons/d/d6/Flag_of_Italy_%281861%E2%80%931946%29_crowned.svg`
  (egress bloqueia upload.wikimedia.org).

### Japão (JPN)

- Caminho local: `data/catalog/flags/JPN.svg`
- Baixado de: `https://raw.githubusercontent.com/hampusborgos/country-flags/main/svg/jp.svg`
- Licença: Public Domain.
- Período: Hinomaru, em uso desde 1870 (proporções e tom de vermelho
  padronizados em 1999, mas visualmente equivalente). Válida para 1930.
- URL Wikimedia original (PENDENTE no acesso direto):
  `https://upload.wikimedia.org/wikipedia/commons/9/9e/Flag_of_Japan.svg`

## Resumo

- 11/11 bandeiras baixadas como SVG válidos (todas parseiam por
  `xml.etree.ElementTree`).
- 7 bandeiras (ARG, URY, PRY, CHL, BOL, GBR, JPN) representam adequadamente
  o período Vargas — desenhos não mudaram entre 1930 e hoje.
- 4 bandeiras (BRA, USA, DEU, ITA) baixadas são variantes **modernas** que
  diferem da iconografia de 1930. Substituições históricas estão como
  PENDENTE acima e podem ser refeitas manualmente assim que houver acesso a
  `upload.wikimedia.org`.
