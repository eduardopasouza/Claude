# MapBiomas Monitor do Fogo

- **URL:** https://plataforma.monitorfogo.mapbiomas.org/
- **Categoria:** mapbiomas
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Status da auditoria

**Página não renderizou conteúdo via automação** — provavelmente SPA com carregamento pesado de raster via WebGL/MapLibre que não completa o bootstrap sem interação humana. Tanto `claude-in-chrome` quanto `WebFetch` retornaram HTML vazio.

## Inferências baseadas em conhecimento (MapBiomas suite)

Seguindo o padrão das outras 5 plataformas MapBiomas já auditadas, o Monitor do Fogo provavelmente oferece:

### Layout esperado (baseado em padrões observados)

- **Árvore temática lateral esquerda** semelhante ao Brasil/Cobertura
- **Abas** Filtros / Camadas / Mapa base (padrão Crédito Rural e Recuperação)
- **Mapa Leaflet ou MapLibre** centralizado
- **Dashboard inferior** com estatísticas agregadas

### Camadas típicas do módulo Fogo (cruzamento com Brasil/Cobertura)

- **Anual** — cicatrizes de fogo por ano (desde 1985)
- **Mensal** — cicatrizes mês-a-mês (desde ~2019 com Sentinel)
- **Acumulado** — total histórico
- **Frequência** — nº de vezes que o pixel queimou em X anos
- **Ano do último fogo**
- **Tamanho da cicatriz** — classes de área (pequena/média/grande)

### Filtros esperados

- Bioma, UF, município
- Range temporal (ano inicial e final)
- Tipo de cobertura afetada (floresta, savana, pastagem, agricultura)

### Origem dos dados

- Satélites MODIS + VIIRS + Landsat + Sentinel
- Classificação supervisionada MapBiomas

## Conhecimento externo aplicável

- **Google Earth Engine assets:** `projects/mapbiomas-public/assets/brazil/fire/collection3/`
- **Cicatrizes mensais** desde 2019
- **Cicatrizes anuais** 1985-presente
- Cruzamento automático com cobertura de terra → permite responder "quanto de cana queimou em 2024?"

## Insights para AgroJus

### Aplicação jurídica

Fogo é **prova pericial** em casos de:
- Auto de infração IBAMA por incêndio em APP/RL (art. 41 Lei 9.605/98)
- Defesa de autuações com alegação de fogo natural vs antrópico
- Comprovação de PRAD com histórico de fogo

**Para AgroJus:**
1. Camada MapBiomas Fogo deve estar no mapa quando integrada (layer `mapbiomas_fogo` já catalogada como `comingSoon` em `layers-catalog.ts`).
2. No inspector de uma feature PRODES/DETER, cruzar com histórico de fogo do MapBiomas para aquele polígono.
3. Gerar laudo técnico "Histórico de fogo no imóvel CAR X" via Earth Engine para anexar em defesa.

## Ações para reauditar este site

- [ ] Acesso manual via browser do usuário (Eduardo) + captura de screenshots
- [ ] Ou usar Playwright headless com `waitForSelector` em uma SPA-aware
- [ ] Ou consumir a API/GEE assets diretamente (sem passar pela SPA)

## Próxima iteração

Quando integração Earth Engine desbloqueada (GCP Project ID já configurado), implementar módulo direto baseado nos assets GEE do MapBiomas Fogo, sem depender do site.
