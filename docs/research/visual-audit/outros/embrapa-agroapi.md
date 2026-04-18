# Embrapa AgroAPI

- **URL:** https://www.agroapi.cnptia.embrapa.br/portal/
- **Categoria:** mercado-dados (plataforma de APIs agro)
- **Data auditoria:** 2026-04-17
- **Acesso:** cadastro + API key; algumas APIs são pagas por chamada

## Status da auditoria
**PARCIAL — o fetch da home retornou apenas o título "AgroAPI"** (SPA ou render client-side); `/apis` retornou 404. Auditoria feita com conhecimento externo do programa AgroAPI da Embrapa (CNPTIA — Campinas).

## Propósito declarado
AgroAPI é o **hub de APIs da Embrapa** criado para expor, de forma programática, o acervo científico de décadas de pesquisa agronômica brasileira. Modelo de marketplace de APIs desenvolvido pelo CNPTIA (Embrapa Informática Agropecuária, Campinas).

## Layout e navegação (inferido por conhecimento externo)
- **Header** com logo Embrapa, menu: Home / Catálogo / Docs / Preço / Conta.
- **Hero** com proposta de valor: "APIs do agro brasileiro, prontas para seu app".
- **Catálogo** com cards de cada API: ícone, nome, descrição curta, tag de categoria, link para detalhes.
- **Página da API**: descrição, endpoints, parâmetros, exemplos, preço por chamada, link para docs Swagger/OpenAPI.
- Paleta Embrapa: verde institucional (#006B3F) + branco + cinza.

## Features / dados expostos
APIs historicamente publicadas:
- **ZARC Plantio Certo** — Zoneamento Agrícola de Risco Climático. Entrada: município + cultura + solo + data. Saída: janela de plantio recomendada por nível de risco (20%, 30%, 40%). Base regulatória para liberar Proagro/seguro rural.
- **SmartSolos Expert** — classificação automática de solo a partir de análise química/física enviada. Retorna classe taxonômica SiBCS + recomendações.
- **AGROFIT** — banco de agrotóxicos registrados: nome comercial, ingrediente ativo, cultura-alvo, alvo biológico, dosagem. Espelha a base MAPA.
- **SATVeg** — séries temporais de vegetação por pixel MODIS/NDVI, consulta por lat/lon ou polígono.
- **Invernada+** — pastagens tropicais, recomendação de forrageira por região.
- **AgroTagBaaS** — etiquetagem e rastreabilidade de produtos agro.
- **SISLA** — simulador de leite (dieta).
- APIs regionais específicas (café, cana, citros) dependendo do momento.

Cada API típica oferece:
- Endpoints REST (JSON primário)
- Autenticação por **API key** (Bearer token)
- Documentação Swagger
- Playground de teste

## UX / interações
- Cadastro → criar app → gerar API key → consumir endpoints.
- Documentação interativa estilo Postman/Swagger UI.
- Dashboard de consumo (chamadas/mês, cota restante) para o assinante.
- Suporte por ticket/e-mail.

## Preço e modelo de negócio
Modelo **freemium por API**:
- Plano gratuito com quota limitada (ex.: 100 chamadas/mês para ZARC).
- Planos pagos por volume (pay-per-call ou pacote mensal).
- Algumas APIs (AGROFIT) são mais gratuitas por serem dado público; outras (SATVeg, ZARC com detalhes premium) têm cobrança.
- Valores tipicamente R$ 0,10 - R$ 1,00 por chamada em planos básicos.

## API pública (se houver)
É o produto em si — APIs REST com especificação Swagger/OpenAPI. Esse é um dos poucos casos no agro gov.br com **API-first real**.

## Autenticação
- Cadastro do desenvolvedor (e-mail + CPF + dados).
- Criação de aplicação → geração de API key.
- Key passada em header `Authorization: Bearer <key>` ou query param.
- Cotas e rate limits aplicados por key.

## Conhecimento externo aplicável
- AgroAPI é **a aposta da Embrapa para monetizar e distribuir seu acervo científico** em formato moderno. Foi lançado em 2019 e cresceu em importância no ecossistema AgTech.
- **ZARC** é a API mais consumida — regulação Proagro depende dela, então bancos, seguradoras, cooperativas e AgTechs de crédito precisam consultar ZARC antes de liberar operação.
- **SmartSolos**: sensacional para valuation — classificação SiBCS a partir de análise laboratorial, em segundos. Input para aptidão agrícola real (NBR 14.653-3).
- **AGROFIT**: monitora agrotóxicos registrados — útil para due diligence ambiental e de produção.
- **SATVeg**: NDVI temporal — input para avaliar **uso efetivo** do imóvel ao longo do tempo. Cruza com MapBiomas mas em frequência mais alta (8-16 dias vs. anual).
- Dor: Embrapa/CNPTIA tem dificuldade de escala comercial. UX do portal é "acadêmica", onboarding do dev é arrastado, documentação varia em qualidade entre APIs. Muitos times preferem raspar dado bruto.

## Insights para AgroJus
1. **ZARC é must-have**: AgroJus deve consumir a API ZARC para cada imóvel, exibindo "janela de plantio recomendada para soja em X" + "risco climático 20%/30%/40%" por década. Esse dado muda valor de terra.
2. **SmartSolos como serviço premium**: usuário carrega análise de solo → AgroJus envia ao SmartSolos → devolve classe SiBCS + aptidão. Virtualmente gera um capítulo técnico agronômico do laudo.
3. **SATVeg enriquece histórico**: para cada imóvel, plotar NDVI dos últimos 5-10 anos revela se a fazenda foi efetivamente cultivada, abandonada, degradada. Red flag ou green flag automático.
4. **AGROFIT cruza com embargos**: se imóvel tem registro de uso de defensivo proibido, aparece em AGROFIT + IBAMA.
5. **AgroJus vira consumidor power user da Embrapa**: justifica plano empresarial, possível acordo de parceria institucional. Marketing positivo.
6. **Consolidação de API**: AgroJus pode expor para seus clientes uma **API única consolidada** (GET /imovel/{car_id} retornando ZARC + SmartSolos + MapBiomas + CEPEA + SICOR consolidado). Esse empacotamento é valor agregado claro.

## Gaps vs AgroJus (tabela)

| Dimensão | AgroAPI Embrapa | AgroJus |
|---|---|---|
| Produto | Hub de APIs atômicas | Consumidor agregador + interface para humano |
| Público-alvo | Desenvolvedores AgTech | Advogado, perito, banco, investidor (não dev) |
| UX | Portal Swagger / CRUD de keys | Visualização, laudo, mapa |
| Uso de ZARC | Endpoint bruto | Integrado a ficha de imóvel com interpretação |
| SmartSolos | API de classificação | Upload guiado + relatório pronto |
| SATVeg | Série NDVI por pixel | Gráfico NDVI 10 anos + alerta de degradação |
| Preço | Per-call / plano API | SaaS com Embrapa incorporado no custo |
| Docs | Swagger por API | Documentação única, agronômica + jurídica |
| Cobertura | Atômica (uma função por API) | Agregada (imóvel completo em um GET) |
| Parceria estratégica | Potencial cliente power user | — |
