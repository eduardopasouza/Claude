# RAMT — Relatório de Análise de Mercados de Terras (INCRA)

- **URL:** https://www.gov.br/incra/pt-br/assuntos/governanca-fundiaria/relatorio-de-analise-de-mercados-de-terras
- **Categoria:** valuation
- **Data auditoria:** 2026-04-17
- **Acesso:** público, sem cadastro

## Propósito declarado
Disponibilizar o **Relatório de Análise de Mercados de Terras (RAMT)**, peça oficial do INCRA com análises regionalizadas de preços e dinâmica do mercado fundiário. É o documento-base para:
- Decisões de desapropriação (apoia o valor do VTN/VTI).
- Planejamento de reforma agrária.
- Diagnóstico de valorização regional ("MATOPIBA", "oeste baiano", "fronteira agrícola do Cerrado").
- Subsídio para perícia judicial em ações possessórias e desapropriatórias.

## Layout e navegação
- **Header gov.br padrão**: barra azul institucional, busca, menu hambúrguer, links de acessibilidade (alto contraste, tamanho de fonte, libras).
- **Breadcrumb**: Página Inicial > Assuntos > Governança Fundiária > RAMT.
- **Menu lateral esquerdo**: índice navegável com os 27 estados (Acre → Tocantins), cada um é um link para subpágina dedicada do tipo `/relatorio-de-analise-de-mercados-de-terras/[estado]`.
- **Corpo principal**: texto introdutório curto + lista de UFs. Não há dashboard, mapa nacional nem tabela comparativa.
- **Tags temáticas** ao final: "Imóvel rural", "RAMT", "Planilha de Preços Referenciais de Terra".
- **Botões de compartilhamento social** (Facebook, Twitter, LinkedIn, WhatsApp).
- **Footer gov.br**: menção genérica a "Dados Abertos" sem link direto para o RAMT.

## Features / dados expostos
- A página-raiz é **índice de estados**, não dashboard. Zero gráfico, zero tabela, zero mapa renderizado inline.
- Os PDFs do RAMT ficam em subpáginas por UF. Usuário precisa: clicar no estado → chegar na subpágina → baixar PDF.
- **Não há filtro por ano** na home; é preciso entrar em cada UF e ver quais ciclos estão disponíveis (tipicamente 2015, 2017, 2019, 2021, 2023...).
- Metodologia vive num link separado ("Introdução - RAMT") em vez de resumida ao lado dos dados.

## UX / interações
- **Modelo "biblioteca digital gov.br"**: páginas de conteúdo estático com listas de links; nada de interatividade.
- Tipografia Rawline, paleta azul #1351B4, botões sólidos. Acessibilidade AA.
- **Fricção alta** para o usuário que quer comparar estados: precisa abrir 27 abas e baixar 27 PDFs para ter visão nacional.
- Sem search interno, sem filtros temporais, sem preview de PDF.

## Preço e modelo de negócio
Gratuito, conteúdo oficial federal.

## API pública (se houver)
**Não documentada.** Os PDFs ficam em paths estáveis `/governanca-fundiaria/relatorio-de-analise-de-mercados-de-terras/[estado]`, então é possível fazer raspagem previsível. Não há JSON/REST oficial.
Possibilidade de catalogação no **dados.gov.br**, mas não foi verificado link direto a partir desta página.

## Autenticação
Nenhuma — leitura é 100% pública.

## Conhecimento externo aplicável
- O RAMT é o **relatório narrativo** do INCRA; o SIMET é a **base numérica** (VTN por município). Os dois andam juntos: RAMT cita, comenta e contextualiza os dados do SIMET.
- Cada edição estadual do RAMT tipicamente tem: introdução metodológica, cenário econômico regional, mapa de mesorregiões, tabelas de VTN por aptidão, análise de tendência (série 10 anos), comentário qualitativo sobre drivers de valorização.
- **Defasagem editorial** é marcante: muitos estados têm RAMT mais recente de 2021/22; em abril/2026 isso significa dados já envelhecidos em 3-4 anos em regiões de alta dinâmica (MT, BA, MA, TO).
- Para peritos e advogados, o RAMT é **citação obrigatória** em laudo de desapropriação, mesmo quando insuficiente — porque STJ/STF esperam ancoragem oficial.

## Insights para AgroJus
1. **Concentração e acesso**: AgroJus pode ingerir os 27 PDFs do RAMT + SIMET e servir num único dashboard nacional com mapa-coroplético de VTN por município, filtro temporal e comparação estado-a-estado. **Isso o próprio INCRA não oferece.**
2. **"RAMT AgroJus"**: geração automatizada de relatório estilo RAMT por município/mesorregião sob demanda, usando: SIMET + comparáveis (leilões, anúncios) + MapBiomas (uso/cobertura) + CEPEA (preços de commodities da região) + Conab (custos de produção). Um perito economiza dias.
3. **Citar RAMT inline**: o laudo gerado pelo AgroJus cita o RAMT oficial parágrafo-a-parágrafo, criando defensibilidade judicial imediata.
4. **Sinalização de defasagem**: quando RAMT disponível é de 2021 e AgroJus tem dados até março/2026, mostrar "RAMT oficial: 2021 | Atualização AgroJus: mensal | Discrepância detectada: +X%". Esse alerta converte.
5. **Série histórica navegável**: AgroJus pode acumular RAMTs antigos e plotar linha histórica por UF — visualização que o gov.br não entrega.

## Gaps vs AgroJus (tabela)

| Dimensão | RAMT (gov.br) | AgroJus |
|---|---|---|
| Formato primário | PDF estático por UF | Dashboard interativo + PDF exportável |
| Navegação | Lista de 27 estados, sem mapa | Mapa nacional + drill-down município/polígono |
| Atualização | Ciclos de 2-4 anos | Mensal |
| Filtros | Nenhum (só estado) | Ano, UF, bioma, aptidão, uso do solo, range de área |
| Visualizações | PDF com gráficos estáticos | Gráficos interativos, séries temporais, mapas |
| Metodologia | Documento separado | Exposta inline com tooltips e código aberto |
| Citabilidade | Fonte oficial, alta autoridade | Cita RAMT + agrega atualização |
| Busca | Sem search | Full-text + filtros |
| API | Não tem | REST + GeoJSON |
| Custo | Gratuito | Freemium (visualização grátis, laudo pago) |
| Público-alvo | Peritos, advogados, acadêmicos | Mesmo público + bancos, seguradoras, investidores |
| Exportação | PDF | PDF laudo + XLSX + JSON + link compartilhável |
