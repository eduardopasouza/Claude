# INMET — Instituto Nacional de Meteorologia

- **URL:** https://portal.inmet.gov.br/
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Propósito declarado
"Instituto Nacional de Meteorologia" — vinculado ao Ministério da Agricultura e Pecuária, presta serviços de previsão do tempo, monitoramento climático e meteorologia aplicada à agricultura. Mantém a Rede de Estações Meteorológicas Automáticas (EMA) e Convencionais (EMC) que é a base oficial de dados climáticos do país.

## Layout e navegação
**Menu principal observado:**
- **Tempo:** previsões, análise sinótica, mapas de precipitação, extremos, radar.
- **Clima:** previsão climática, monitoramento, normais climatológicas.
- **Dados Meteorológicos:** banco de dados (BDMEP), catálogo de estações, histórico.
- **Satélites:** imagens GOES.
- **Previsão Numérica:** produtos de modelos.
- **Sisdagro:** monitoramento agrometeorológico (crítico para AgroJus).
- **Publicações:** boletins, notas técnicas.

Layout: header gov.br + tiles grandes de produto (tempo, clima, satélite), com forte componente visual de mapas como preview na home. Identidade é institucional clássica (azul, logo INMET + gov.br).

## Dados e funcionalidades expostas
- **Previsão por capital** (cards grandes com ícones do tempo).
- **Mapas:** condições atuais, anomalias, risco de geada, precipitação acumulada.
- **Gráficos e cartas climatológicas.**
- **Boletins por e-mail** e alertas.
- **Estações:** automáticas (horária, em tempo quase real) + convencionais (diária, com controle de qualidade).
- **BDMEP:** Banco de Dados Meteorológicos para Ensino e Pesquisa — download histórico.
- **Sisdagro:** produtos agrometeorológicos (balanço hídrico, janela de plantio, risco climático por cultura).

## UX / interações (consulta, busca, filtros, download)
- Seleção de estação via mapa ou dropdown UF → Estação.
- Janela de data para extração.
- Exportação CSV do BDMEP (por estação, período, variável).
- **Alert-AS** — feed RSS de alertas meteorológicos.
- Gráficos interativos de série temporal.

## API pública (endpoints, auth, formatos)
- **Base:** `https://apitempo.inmet.gov.br/` (dados históricos e estações).
- **Alert-AS RSS:** feed de alertas meteorológicos em XML/RSS.
- **Formato:** JSON para a API tempo.
- Endpoints conhecidos (conhecimento externo):
  - `/estacoes/T` — estações automáticas
  - `/estacao/{data_inicio}/{data_fim}/{codigo}` — série horária
  - `/estacao/diaria/{data_inicio}/{data_fim}/{codigo}` — série diária
  - `/condicao/capitais/{data}` — condição atual nas capitais
- Documentação Swagger/OpenAPI **não disponível oficialmente** — integradores usam engenharia reversa.

## Rate limits / cotas conhecidas
Não declarados. Historicamente a API tem latência alta e timeouts em queries largas — boa prática: paginar por estação e mês.

## Autenticação
- Pública, sem login.
- Sem token.
- Sem gov.br.

## Conhecimento externo aplicável
- Série INMET é **prova oficial** de evento climático em ação de força maior, seguro agrícola, Pronaf, Garantia-Safra e responsabilidade civil por barragem.
- Sisdagro é relevante para AgroJus: calcula balanço hídrico por cultura e localização — evidência em defesa de produtor.
- Dados são auditáveis: BDMEP tem controle de qualidade formal.
- Normais climatológicas 1991-2020 são a referência oficial para comparação de "ano atípico".
- Cobertura de estações é heterogênea: adensada no Sudeste/Sul, rarefeita no Norte/interior do NE.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Tiles de produto grandes** na home do INMET funcionam porque meteorologia é visual — AgroJus pode aplicar o mesmo padrão para "Dashboards" (Imóvel, Caso, Cliente, Jurisprudência).
2. **Mapa primeiro** é cultura do usuário gov em dados geoespaciais — AgroJus deve manter mapa central em toda tela de imóvel.
3. **Sisdagro como produto derivado** mostra que o usuário aprecia **análise pronta** (risco de geada, janela de plantio) e não só dado cru — AgroJus deve oferecer "indicadores calculados" (risco ambiental, risco possessório, risco minerário).
4. **Alert-AS via RSS** é o feed gov mais antigo que ainda funciona — AgroJus pode oferecer RSS por advogado/caso para integração com leitores.
5. **Sem Swagger** é gap que AgroJus deve evitar — documentar OpenAPI desde dia 1.
6. **Normais climatológicas** dão baseline para laudo — AgroJus deve incorporar normais do INMET em relatórios de seca/enchente.

## Gaps vs AgroJus (tabela)

| Dimensão | INMET | AgroJus (alvo) |
|---|---|---|
| Dados | Meteorologia/clima | Multi-domínio (inclui INMET via ingestão) |
| API | REST JSON sem Swagger | REST + Swagger + MCP |
| Autenticação | Anônima | gov.br + token |
| Rate limit | Opaco | Declarado |
| Alertas | RSS Alert-AS | Webhook + push + e-mail por imóvel |
| Cruzamento imóvel × clima | Manual | Automático (estações próximas + interpolação) |
| Laudo climático | Boletim PDF genérico | Laudo individualizado por imóvel/período |
| Sisdagro | Produto gov isolado | Agrometeorologia integrada ao caso |
| Cobertura geográfica | Heterogênea | Fallback para MERGE/CHIRPS (grade) |
| Histórico | BDMEP CSV | Parquet + BigQuery queryable |
| Visualização | Gráficos estáticos | Gráficos interativos + timeline |
| Interface | Portal legado | SPA moderna |
