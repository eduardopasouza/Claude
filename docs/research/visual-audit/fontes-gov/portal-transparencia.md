# Portal da Transparência (CGU) — API de Dados

- **URL:** https://portaldatransparencia.gov.br/api-de-dados
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (token gratuito exigido)

## Propósito declarado
Plataforma da Controladoria-Geral da União (CGU) para acesso programático a dados de transparência federal — permite consumir, via REST, informações que seriam navegadas manualmente no portal web. A API substitui o scraping e garante contrato estável para integrações.

## Layout e navegação
- **Menu principal:** "Consultas Detalhadas", "Painel Gráfico", "Sobre o Portal", "Controle Social", "Aprenda Mais".
- **Breadcrumb** visível nas páginas internas — padrão gov.br clássico.
- **Footer:** redes sociais, links secundários, avisos legais (LGPD, LAI).
- Página `/api-de-dados` funciona como hub: apresenta lista de endpoints agrupada por domínio + links para playground Swagger e exemplos em código.

## Dados e funcionalidades expostas
Endpoints REST por domínio (relevantes para AgroJus em negrito):
- **Garantia-Safra** (seguro agrícola familiar)
- **CEIS** — Cadastro de Empresas Inidôneas e Suspensas
- **CNEP** — Cadastro Nacional de Empresas Punidas
- **CEPIM** — entidades sem fins lucrativos impedidas
- **CEAF** — expulsões da administração federal
- Bolsa Família, PETI, Seguro Defeso (benefícios sociais)
- Contratos e Convênios do Executivo Federal
- Despesas Públicas, Licitações Federais, Notas Fiscais Eletrônicas
- Servidores Federais, Viagens a Serviço

Todos acessíveis por GET com filtros (CPF/CNPJ, município, ano/mês, órgão).

## UX / interações (consulta, busca, filtros, download)
- Página web expõe **Swagger/Redoc** — playground para testar endpoint sem escrever código.
- Exemplos de consumo em **JavaScript, Java, PHP, .NET** com código copiável.
- Paginação padrão via parâmetros `pagina` e `tamanhoPagina`.
- Download bruto em CSV disponível separadamente na seção "Dados Abertos" (não na API).

## API pública (endpoints, auth, formatos)
- **Arquitetura:** REST sobre HTTPS.
- **Formato:** JSON (primário); algumas rotas respondem XML por negociação de conteúdo.
- **Base URL histórica:** `http://api.portaldatransparencia.gov.br/` (migrada para HTTPS).
- **Autenticação:** token emitido após cadastro de e-mail. Token enviado no header `chave-api-dados`.
- **Documentação Swagger:** disponível na própria página `/swagger-ui/index.html`.

## Rate limits / cotas conhecidas
**Declarados explicitamente na UI:**
- **90 requisições/minuto** entre 06:00 e 23:59
- **300 requisições/minuto** entre 00:00 e 05:59

Estratégia comum: agendar cargas pesadas para madrugada. Excesso retorna HTTP 429.

## Autenticação
- Cadastro gratuito com e-mail → token permanente.
- Token enviado no header HTTP `chave-api-dados`.
- **Não integra gov.br** — autenticação é independente (anterior à política unificada).
- Sem OAuth; sem refresh token; token único por conta.

## Conhecimento externo aplicável
- CEIS/CNEP são fontes **obrigatórias** em due diligence de contratação pública e em defesas possessórias com réu pessoa jurídica.
- Garantia-Safra é diretamente relevante para AgroJus — cruza CPF de produtor rural com benefício pago, relevante em ações possessórias e ambientais que envolvem agricultor familiar.
- Base é atualizada mensalmente (com defasagem típica de 30-60 dias).
- Dataset CSV bruto está em `dadosabertos.gov.br` (CKAN) — rota alternativa para cargas massivas.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Token por e-mail** é o padrão gov low-friction — AgroJus pode oferecer tier público idêntico (e-mail → token) antes de exigir gov.br.
2. **Rate limits declarados upfront** (90/min diurno, 300/min madrugada) são a expectativa do usuário gov — AgroJus deve tornar limites visíveis na doc (evitar "403 mistério").
3. **Swagger embutido** com botão "Try it out" é o gold standard que o desenvolvedor brasileiro espera.
4. **Exemplos em 4+ linguagens** (JS, Java, PHP, .NET) — AgroJus deve cobrir pelo menos JS, Python, cURL.
5. **Janela noturna de maior cota** cria padrão cultural de batch jobs noturnos — AgroJus pode seguir mesmo padrão para cargas pesadas.
6. **Header `chave-api-dados`** é o naming convention brasileiro — considerar aceitar além de `Authorization: Bearer`.

## Gaps vs AgroJus (tabela)

| Dimensão | Portal Transparência | AgroJus (alvo) |
|---|---|---|
| Arquitetura | REST simples | REST + GraphQL (opcional) |
| Autenticação | Token único | Token + OAuth gov.br |
| Rate limit | 90-300 req/min | Tiered (free/pro/enterprise) com burst |
| Formato | JSON/XML | JSON + GeoJSON + Parquet |
| Dados geoespaciais | Ausentes | Core |
| Cruzamento entre datasets | Manual | Automatizado (SQL/federação) |
| Swagger | Sim | Sim + exemplos live |
| Webhooks/eventos | Não | Sim (atualização CAR, alerta MapBiomas) |
| Histórico versionado | Não explicitado | Snapshots datados |
| SDK oficial | Não | Python + TS |
| Relatório PDF | Não | Sim (AgroJus gera laudo) |
| Dashboard pré-pronto | Painel Gráfico estático | Dashboards personalizáveis |
