# CONAB — Companhia Nacional de Abastecimento

- **URL original:** https://www.conab.gov.br/info-agro/safras
- **URL efetiva (após 301):** https://www.gov.br/conab/pt-br (a página `/info-agro/safras` foi migrada para o domínio gov.br institucional)
- **Categoria:** mercado-dados
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Status da auditoria
A URL fornecida foi **migrada** (301 permanente) para o domínio gov.br institucional. A subpágina específica `/acompanhamento-safra` sob o novo domínio retornou 404 no fetch — a árvore de URLs foi reorganizada. Auditoria consolida: (a) a home gov.br da CONAB que foi acessível; (b) conhecimento externo sobre os produtos CONAB.

## Propósito declarado
CONAB é a companhia federal que executa políticas públicas de abastecimento e informação agrícola. Missão dupla: **operação** (estoques reguladores, PGPM, PAA, leilões de commodities, armazenagem) e **informação** (pesquisas de safra, custos de produção, análise conjuntural).

## Layout e navegação
Padrão **gov.br institucional**:
- Header azul federal com selo, busca, acessibilidade.
- Menu hierárquico: Operações / Notícias / Acesso à Informação / Canais de Comunicação.
- Seções principais do "Atuação":
  - Abastecimento Social (PAA, cestas de alimentos, venda de balcão)
  - Agricultura Familiar
  - Armazenagem (cadastro de armazéns)
  - Comercialização (leilões, apoio de preço)
  - **Informações Agrícolas** (análise de mercado, custos de produção, acompanhamento de safra)
  - Logística
  - Sociobiodiversidade (PGPM-Bio)

## Features / dados expostos
Produtos de dados relevantes da CONAB:
- **Acompanhamento da Safra Brasileira de Grãos** — 12 boletins/ano, PDF + XLSX. Cobre soja, milho 1ª/2ª safra, algodão, arroz, feijão, trigo, sorgo, girassol, canola, etc. Estima área plantada, produção, produtividade por UF e consolidado Brasil.
- **Boletim da Safra de Café** — trimestral (4/ano), arábica + conilon por UF produtora.
- **Boletim de Cana-de-açúcar** — quatrimestral, área + produção + produtividade + destino (açúcar/etanol).
- **Custos de Produção Agrícola** — planilhas detalhadas por cultura + UF + sistema (sequeiro/irrigado, plantio direto/convencional). Composição: insumos, operações, pós-colheita, depreciação, remuneração da terra e capital. **Dado crítico para valuation rural por abordagem de renda.**
- **Estoques Públicos** e **Sisdep** (leilões).
- **Conjuntura agropecuária** mensal.
- **Mapa da cadeia produtiva** e **Portal de Armazenagem** (dashboard Power BI).

## UX / interações
- Downloads de PDFs + XLSX é o fluxo principal.
- Portal Power BI embarcado para armazenagem (diferencial — raro em gov.br).
- Sem search full-text robusto dentro dos boletins.
- Paleta padrão gov.br (azul #1351B4, cinza neutro, branco). Sem identidade própria visual forte.
- Sem gráficos interativos no HTML — só PDFs com figuras estáticas.

## Preço e modelo de negócio
100% gratuito, dado público federal.

## API pública (se houver)
- **dados.gov.br** cataloga datasets CONAB (área/produção/produtividade, custos de produção, estoques). Acesso via CKAN API do dados.gov.br.
- CONAB tem **Portal de Informações Agropecuárias** com alguns endpoints diretos (variam por produto).
- **Power BI** para armazenagem expõe parcialmente via embed mas não tem API REST clara.
- Raspagem dos XLSX é factível e tem formato razoavelmente estável entre edições.

## Autenticação
Consulta pública sem login. Edição/submissão de cadastro de armazém requer gov.br login.

## Conhecimento externo aplicável
- CONAB é **a fonte oficial** de estimativa de safra brasileira, usada por: MAPA, IBGE (para comparar com LSPA), USDA (para benchmarking internacional), traders, bancos, seguradoras, mídia agro.
- **Custos de produção CONAB** é input central na abordagem da renda para valuation rural (NBR 14.653-3): receita bruta esperada (commodity CEPEA × produtividade ZARC) menos custo CONAB = margem bruta que justifica valor da terra.
- Boletins de safra saem com padrão: **10º dia útil de cada mês**. Previsível.
- Historicamente, CONAB e IBGE/LSPA divergem em estimativas de safra — existe triangulação de mercado. AgroJus pode mostrar ambas e divergência.
- Portal Power BI de armazenagem é o mais moderno do conjunto; mostra onde ficam os silos (cooperativas, privados, CONAB) — dado logístico valioso para valuation regional.

## Insights para AgroJus
1. **Custo de produção CONAB como input de valuation**: para cada imóvel, AgroJus pode mostrar automaticamente "Custo de produção da soja em GO (CONAB 2025/26): R$ X/ha. Receita estimada: R$ Y/ha. Margem: R$ Z/ha. Capitalizando a 8% = valor-terra estimado pela renda: R$ W/ha." Isso é a abordagem da renda completa, em segundos.
2. **Estimativa de safra para análise conjuntural**: ao exibir ficha de imóvel em região específica, mostrar "Safra prevista CONAB para o município X: Y sacas de soja" — dá contexto macro imediato.
3. **Ingerir via dados.gov.br**: evita raspagem frágil. CKAN API é pipeline limpo.
4. **Dashboard AgroJus "Brasil Agrícola"**: reempacotar os dados CONAB num mapa nacional interativo (área plantada, produtividade, custo, estoque por UF). O governo não faz isso bem; AgroJus pode ser a versão boa.
5. **PGPM e leilões CONAB**: monitorar leilões públicos da CONAB (ex.: aquisição de arroz, escoamento de estoque) como fonte adicional de preço de referência por cadeia.

## Gaps vs AgroJus (tabela)

| Dimensão | CONAB | AgroJus |
|---|---|---|
| Formato principal | PDF + XLSX | Dashboard interativo + API |
| Granularidade | UF e algumas microrregiões | UF → município → polígono |
| Visualização | Figuras estáticas em PDF | Mapas, gráficos interativos |
| Custo de produção | Planilha por cultura/UF | Aplicado automaticamente ao imóvel georref. |
| Safra | Mensal por boletim | Mensal + comparativo entre boletins |
| Contextualização | Isolada por boletim | Cruzada com CEPEA + ZARC + MapBiomas |
| Atualização | 12 boletins/ano grãos; 4 café | Ingerido via dados.gov.br no dia |
| Público | Agro generalista | + advogado, perito, banco, seguradora |
| API | Via dados.gov.br, irregular | REST consolidada e versionada |
| Laudo | Dado bruto | Capítulo pronto para NBR 14.653 |
