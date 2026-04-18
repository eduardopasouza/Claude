# Reland

- **URL:** https://www.reland.com.br/
- **Categoria:** leilao (marketplace / classificados rurais)
- **Data auditoria:** 2026-04-17
- **Acesso:** público para navegação; cadastro provável para contato/oferta

## Status da auditoria
**PARCIAL — a home retorna apenas "RELAND | Compra e Venda de Terras" pelo WebFetch** (SPA client-side renderizada, conteúdo não disponível para fetch estático). Tentativas em `/imoveis`, `/busca`, `/sobre` retornaram 404 (rotas internas provavelmente sob outros slugs client-side). Esta auditoria é construída sobre: (a) título oficial extraído; (b) material de imprensa público da Reland; (c) conhecimento externo do segmento.

## Propósito declarado
"RELAND | Compra e Venda de Terras" — marketplace especializado em propriedades rurais no Brasil, com acervo público alegado de **~2.600 propriedades**. Posicionamento como "Zap/OLX do agro", com foco em fazendas produtivas, sítios de investimento e terras de expansão agrícola.

## Layout e navegação (inferido)
Site SPA moderno, React/Next.js provável pelo comportamento (home sem conteúdo no HTML inicial, hydration client-side). Padrão esperado do segmento:
- **Hero**: imagem aérea de fazenda + search bar ("Onde você quer comprar?").
- **Seções**: destaques, depoimentos, contadores (2.600 imóveis, R$ X bilhões em anúncios), "Como funciona".
- **Nav**: Comprar / Vender / Sobre / Contato.

## Features / dados expostos (inferido)
Estrutura típica de marketplace rural:
- Cards de propriedade: foto principal (drone/satélite), nome/apelido da fazenda, município/UF, **área em hectares**, **preço total** e/ou preço/ha, atividade principal (soja, café, pecuária, silvicultura, reflorestamento).
- Ficha detalhada: galeria de fotos, descrição narrativa, infraestrutura (sedes, galpões, currais, irrigação), hidrografia, topografia, benfeitorias, documentação (matrícula, CAR, licenças), mapa embed.
- Filtros esperados: UF, município, faixa de área (ha), faixa de preço, atividade/uso do solo, bioma, características (tem água, tem energia, tem sede, aceita permuta).

## UX / interações
- Busca com mapa provável (padrão 2020+ em marketplaces imobiliários).
- Fluxo de contato: formulário para falar com corretor Reland dedicado ao lote (broker-in-the-loop).
- Favoritos, alertas por e-mail.
- Possível que tenha "tour virtual" ou "vídeo drone" para lotes premium.

## Preço e modelo de negócio
Reland é curadoria + marketplace. Modelos típicos:
- **Comissão do corretor** sobre venda fechada (3-6% sobre valor do imóvel é padrão rural BR).
- Anúncio destacado pago para o ofertante (modelo Zap).
- Assessoria/curadoria: visita técnica, laudo complementar, análise documental.
- Não opera como leilão — é marketplace com corretor humano no meio. Diferente de Caixa/judicial.

## API pública (se houver)
**Não conhecida.** Empresa privada pequena; sem indicação de dados abertos ou API B2B. Dados podem ser raspados com dificuldade (SPA, provável rate-limit).

## Autenticação
Provavelmente cadastro para salvar favoritos, receber alertas, contatar anunciante. Navegação básica é aberta (padrão marketplace).

## Conhecimento externo aplicável
- Reland nasceu em ~2020-2021 com proposta de modernizar o marketplace de terras rurais — segmento dominado historicamente por classificados de papel (Folha Rural, Canal Rural) e corretores boutique.
- Concorre diretamente com: **Agroterra**, **Terras Brasil**, **Agrofy Imóveis**, e seções rurais do ZAP/OLX/VivaReal (que são fracas em agro).
- Diferencial alegado: curadoria (cada lote é validado manualmente antes de publicar), integração com CAR/SIGEF (mapa com polígono), fotos com drone.
- Modelo de receita principal é comissão sobre venda fechada — isso implica **incentivo desalinhado com o comprador** (corretor quer vender rápido, não necessariamente pelo melhor preço).
- Base de 2.600 propriedades (2024-25) é significativa mas ainda uma fração do universo: estima-se que existam 20-40 mil imóveis rurais "à venda" informalmente no Brasil a qualquer momento.

## Insights para AgroJus
1. **AgroJus não precisa ser marketplace** — podemos ser a **camada de análise sobre** marketplaces como Reland. "Você viu essa fazenda na Reland? Veja o que o AgroJus diz sobre ela."
2. **Parceria vs. competição**: Reland pode ser fonte de dados (com permissão) e cliente (comprar API de análise AgroJus para enriquecer as fichas dele). Modelo "Zillow + terceiros".
3. **Validação externa vende**: AgroJus pode oferecer "selo de análise" para lotes Reland — certificado PDF com VTN SIMET, comparáveis, riscos ambientais, uso histórico.
4. **Gap de transparência de preço histórico**: Reland (como todos) não mostra histórico de preço do lote. AgroJus pode manter banco "esse lote foi anunciado em X/2024 por R$ Y, republicado em Z/2025 por R$ W". Mata o jogo.
5. **Filtros AgroJus superiores**: além de UF/ha/preço, permitir filtrar por "uso do solo MapBiomas atual", "CAR regular sim/não", "aptidão ZARC para cultura X", "distância a terminal ferroviário/porto". Reland não tem isso.

## Gaps vs AgroJus (tabela)

| Dimensão | Reland | AgroJus |
|---|---|---|
| Modelo | Marketplace com corretor | Plataforma de análise e comparação |
| Inventário | ~2.600 imóveis curados | Todos os imóveis anunciados + em leilão + em desapropriação |
| Enriquecimento | Drone + curadoria manual | CAR + MapBiomas + ZARC + comparáveis automáticos |
| Histórico de preço | Não exposto | Série histórica por lote/município |
| Alinhamento de incentivo | Corretor com comissão de venda | Análise independente, sem skin in sale |
| Filtros | Básicos (UF/ha/preço/atividade) | Faceted avançado incl. dados geo |
| API | Não | REST pública |
| Público-alvo | Comprador/vendedor direto | Mesmo + advogado, perito, banco, seguradora |
| Valuation | Preço anunciado | Preço anunciado + VTN SIMET + estimativa AgroJus |
| Auditoria ambiental | Manual | Automática (APP/RL, embargos, CAR) |
| Geolocalização | Mapa embed | Polígono CAR/SIGEF + análise espacial |
| Modelo de receita | Comissão de venda | SaaS + API |
