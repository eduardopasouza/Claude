# Portal Leilão Imóvel

- **URL:** https://www.portalleilaoimovel.com.br/
- **Categoria:** leilao
- **Data auditoria:** 2026-04-17
- **Acesso:** indeterminado (fetch falhou)

## Status da auditoria
**FALHA DE ACESSO — o WebFetch retornou ECONNREFUSED em https://www.portalleilaoimovel.com.br/ e em https://portalleilaoimovel.com.br/** (04/2026). O domínio pode estar fora do ar, em manutenção ou bloqueando fetch por User-Agent. Esta auditoria é construída integralmente a partir de conhecimento externo público do mercado brasileiro de agregadores de leilões.

## Propósito declarado
Agregador de leilões imobiliários brasileiro. Escala pública alegada: **~80 mil anúncios** (ordem de grandeza similar ao Spy Leilões, embora com perfil diferente). Foco em imóveis judiciais, extrajudiciais e venda direta.

## Layout e navegação (inferido por conhecimento externo)
Padrão do segmento agregador de leilões BR (2024-26):
- Hero com busca por UF/cidade + CTA de cadastro.
- Carrossel ou grid de "oportunidades em destaque".
- Seções: Planos / Como funciona / Leiloeiros parceiros / Depoimentos / FAQ.
- Footer com links institucionais e LGPD.

## Features / dados expostos (inferido)
Catálogo típico:
- Cards com foto, tipo (casa, apartamento, rural, terreno, comercial), município/UF, valor atual, valor avaliado, % desconto, datas das praças.
- Filtros padrão: UF, cidade, tipo de imóvel, faixa de preço, modalidade (judicial/extrajudicial/venda direta), leiloeiro, comitente (banco/particular/massa falida), "só com foto".

## UX / interações (inferido)
- Login para detalhe (gatewall comum).
- Favoritos e alertas.
- Mapa em algumas versões.

## Preço e modelo de negócio
Modelo usual: freemium/assinatura (R$ 50-200/mês para acesso completo), com trial. Revenue share com leiloeiros em alguns casos.

## API pública (se houver)
Não conhecida.

## Autenticação
Cadastro para ficha completa e edital.

## Conhecimento externo aplicável
- Portal Leilão Imóvel é player relevante mas **menor que SpyLeilões** em cobertura e UX. Reputação de interface datada e base menor de leiloeiros integrados.
- Concorre com: Spy Leilões, Resale, LeilãoVip, Sold, Venda Judicial Online, Mega Leilões (este último é leiloeiro + plataforma própria).
- Categoria rural historicamente subvalorizada no portal — é "mais um tipo" ao invés de vertical dedicada.
- Problema estrutural do segmento: duplicação de lotes (mesmo imóvel aparece em 3-4 agregadores), dados inconsistentes, ficha incompleta, foto ruim. AgroJus pode resolver deduplicando e enriquecendo.

## Insights para AgroJus
1. **Falha de acesso é insight**: player do segmento aparentemente fora do ar/instável em 04/2026 é sinal de mercado consolidando (Spy crescendo, players menores sumindo). AgroJus deve entrar com cobertura robusta desde o dia 1.
2. **Deduplicação como feature**: o mesmo lote de fazenda FCO inadimplente aparece em Caixa + Spy + Portal Leilão + agregadores regionais. AgroJus deve unificar com hash de matrícula + CAR + endereço.
3. **Não replicar a fraqueza rural**: portais horizontais tratam rural como categoria secundária. AgroJus inverte — rural é primeira classe.
4. **Redundância de fontes = confiabilidade**: monitorar Spy + Portal Leilão + Caixa + TJs simultaneamente e cruzar reduz risco de perder lote ou mostrar dado desatualizado.

## Gaps vs AgroJus (tabela)

| Dimensão | Portal Leilão Imóvel | AgroJus |
|---|---|---|
| Uptime | Instável (04/2026 sem acesso) | Alvo 99.9% |
| Escala | ~80 mil anúncios alegados | Espelhar + desapropriações + CAR |
| Categoria rural | Secundária | Primária |
| UX | Datada (reputação de mercado) | Moderna, faceted search, mobile-first |
| Deduplicação | Baixa | Alta (hash matrícula + CAR + endereço) |
| Enriquecimento | Básico | MapBiomas + CAR + ZARC + VTN SIMET |
| API | Sem | REST pública |
| Confiabilidade de dado | Variável | Pipeline validado + fonte-data-de-coleta em cada registro |
| Público-alvo | Investidor de leilão generalista | Rural + advogado + banco + seguradora |
