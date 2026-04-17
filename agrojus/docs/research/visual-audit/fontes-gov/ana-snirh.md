# Hidroweb / SNIRH — Agência Nacional de Águas

- **URL:** https://www.snirh.gov.br/hidroweb
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Status da auditoria
A página é renderizada por JavaScript (Angular/SPA) e o WebFetch recebeu apenas o `<title>HIDROWEB</title>` sem o conteúdo dinâmico. Não foi possível observar diretamente a UI. As seções a seguir são majoritariamente **conhecimento externo** baseado no sistema público e documentado da ANA, marcado explicitamente onde relevante.

## Propósito declarado
Conhecimento externo: o Hidroweb é o sistema público de informações hidrológicas da Agência Nacional de Águas e Saneamento Básico (ANA), integrado ao SNIRH (Sistema Nacional de Informações sobre Recursos Hídricos). Disponibiliza dados históricos e em tempo quase-real de estações da Rede Hidrometeorológica Nacional: séries pluviométricas, fluviométricas, sedimentométricas e de qualidade de água.

## Layout e navegação
**Conhecimento externo:**
- Header com logo ANA/gov.br + menu: "Apresentação", "Mapa", "Estações", "Dados", "Séries", "Telemetria", "Sobre", "Ajuda".
- Mapa interativo (Leaflet) com clusters de estações — cores por tipo (pluviométrica, fluviométrica, qualidade).
- Sidebar de filtros: UF, município, bacia, sub-bacia, responsável (ANA/CPRM/ANEEL/INMET/estadual), tipo, período.
- Detalhe da estação: metadados + botão "Download dados" + gráfico de séries temporais.

## Dados e funcionalidades expostas
**Conhecimento externo:**
- ~22.000 estações cadastradas (ativas e desativadas).
- Séries diárias e horárias (onde telemetria existe).
- Variáveis: chuva, cota, vazão, sedimentos suspensos, qualidade (OD, pH, turbidez, etc.).
- Dados consolidados com responsável pelo dado (ANA gerencia rede, operadores variam).

## UX / interações (consulta, busca, filtros, download)
**Conhecimento externo:**
- Busca por código de estação (8 dígitos) ou por nome.
- Filtros geográficos em cascata.
- Download em **ZIP contendo .MDB (Access) ou .CSV** — formato MDB é legado mas persiste por compatibilidade com softwares de hidrologia (HIDRO, MGB).
- Gráficos de série temporal navegáveis com zoom.
- Exportação de séries em CSV individualmente por variável.

## API pública (endpoints, auth, formatos)
**Conhecimento externo:**
- **Web service SOAP legado** em `http://telemetriaws1.ana.gov.br/ServiceANA.asmx` — endpoints como `HidroEstacoes`, `HidroSerieHistorica`, `DadosHidrometeorologicos`.
- **API REST nova** em processo de lançamento pela ANA (acompanhar `dadosabertos.ana.gov.br`).
- **CKAN "Dados Abertos ANA"** (`dadosabertos.ana.gov.br`) distribui snapshots CSV/shapefile.
- Sem OpenAPI/Swagger consolidado para o SOAP legado.

## Rate limits / cotas conhecidas
Não declarados publicamente. Web service SOAP historicamente sofre com timeouts em queries extensas — boa prática: paginação por estação/ano.

## Autenticação
- Consulta web e download: **público**.
- Web service SOAP: **anônimo**.
- Sem integração gov.br até a última verificação pública.

## Conhecimento externo aplicável
- Séries hidrológicas são **prova técnica** em ações de desastre climático, responsabilidade de barragens, outorga de uso de água, e hoje em litígios agroclimáticos (seca, estiagem, enchente) em que o produtor alega força maior.
- Telemetria em tempo real está em `https://www.ana.gov.br/sar0/Home` (SAR — Sistema de Acompanhamento de Reservatórios).
- ANA é peça-chave em disputas de outorga de água para irrigação — AgroJus precisa cruzar com CNARH (cadastro de usuários de água) e outorga federal/estadual.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Mapa primeiro, busca depois** — Hidroweb abre direto no mapa de estações. AgroJus pode seguir o mesmo padrão para consultas geoespaciais (imóvel-first UX).
2. **Formatos legados (.MDB) coexistem com CSV** — público técnico brasileiro ainda usa Access para hidrologia. AgroJus pode oferecer CSV como primário mas manter SHP/DBF para compatibilidade.
3. **SOAP legado** segue servido — AgroJus deve **não** depender de SOAP, mas documentar como seu cliente consome e traduz.
4. **Código padronizado 8 dígitos** para estações é tipo de identificador que AgroJus pode emular (código estável por feature).
5. **Série temporal com gráfico zoomável** é a killer feature — AgroJus deve oferecer gráfico similar para histórico MapBiomas, desmatamento, precipitação no imóvel.

## Gaps vs AgroJus (tabela)

| Dimensão | Hidroweb | AgroJus (alvo) |
|---|---|---|
| Interface | SPA Angular legada | Next.js + mapa moderno |
| Dados primários | Séries hidrometeorológicas | Multi-domínio (CAR, SIGEF, embargos, clima) |
| API | SOAP legado | REST OpenAPI |
| Formato de download | ZIP/MDB/CSV | CSV/Parquet/GeoJSON |
| Rate limit | Não declarado | Declarado por tier |
| Visualização temporal | Gráfico de série | Série + mapa + timeline MapBiomas |
| Cruzamento com imóvel | Manual | Automático (estações próximas ao polígono) |
| Alerta de evento extremo | Não | Webhook (chuva/estiagem anômala) |
| Autenticação | Anônima | gov.br + token |
| Linkagem a outorga | Parcial (SAR separado) | Integrada (outorga + uso + série) |
| Laudo automático de seca/enchente | Não | Gerado por AgroJus |
| Dados em tempo real | Parcial (SAR à parte) | Integrado |
