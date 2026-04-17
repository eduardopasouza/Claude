# Agrotools

- **URL:** https://agrotools.com.br/
- **Categoria:** concorrente
- **Data auditoria:** 2026-04-17
- **Acesso:** público (institucional); ATMarket e produto em portais separados

## Propósito declarado
"Conectamos territórios com negócios para apoiar a tomada de decisão." A Agrotools se posiciona como plataforma de geointeligência para o agronegócio que entrega compliance ambiental, análise de risco e rastreabilidade de cadeia produtiva, conectando produtores a compradores, financiadores e seguradoras.

## Layout e navegação
- **Header:** duas camadas de menu. Primária: "Conteúdos | Soluções | Blog | Carreira | Sobre | Materiais | ATMarket". Secundária (hover/secundário): "Sobre | Soluções | Carreira | Conteúdos | Blog | Na mídia | Cases | ATMarket". Toggle de idioma PT/EN/ES.
- **Hero:** headline "Os melhores insights sobre o agro agora em suas mãos!" + subtítulo sobre territórios e decisão + CTA "Entenda melhor" (scrolla para soluções).
- **Main:** grid de 6 verticais de solução, cada uma com SVG ilustrativo e texto. Depois seção por persona (comprador, financiador, vendedor). Seção de cases e mídia.
- **Footer:** telefone +55 11 3045-6636, escritórios (São José dos Campos HQ, SP, Parque Tecnológico), redes sociais (Facebook, Instagram, LinkedIn).
- ATMarket é sub-portal separado (atmarket.agrotools.com.br) — provável marketplace/B2B interno.

## Features principais observadas
- **Financiamento rural:** análise de risco do produtor em "poucos segundos" para bancos/cooperativas.
- **Eficiência de vendas:** inteligência geográfica para segmentar mercado (ex.: revendas de insumos).
- **ESG compliance:** verificação de origem de matéria-prima / desmatamento / sobreposição com UCs e TIs.
- **Inteligência de supply chain:** rastreabilidade da cadeia (grãos, carne, fibra).
- **Seguro Rural:** avaliação de risco para seguradoras.
- **Proteção de Marca:** aparente monitoramento para empresas que querem garantir que fornecedores não desmatam.
- Conhecimento externo: catálogo de 1.300+ camadas GIS internas, cobrindo CAR, embargos, UCs, TIs, MapBiomas, PRODES, DETER, propriedades, climatologia, solo.

## UX / interações
Site vitrine institucional — não expõe o produto. O produto real é entregue via painel web customizado por cliente enterprise (contratos anuais), típica venda consultiva B2B. Não há screenshots reais de mapa/dashboard no site — apenas placeholders SVG, o que reforça postura "premium enterprise, não se mostra para qualquer um". Fluxo do visitante: hero → solução → formulário de contato comercial → demo agendada com SDR.

## Preço e modelo de negócio
Nenhum preço visível. Conhecimento externo: contratos enterprise em torno de R$ 50 mil/mês, dimensionados por número de CPFs/CNPJs/fazendas consultadas e camadas liberadas. Clientes: tradings (Cargill, Bunge), bancos, frigoríficos, seguradoras. Modelo é SaaS + consultoria + API (ATMarket pode ser o marketplace de dados/API).

## Autenticação
Nenhum login visível no site institucional. ATMarket aparentemente tem portal próprio com autenticação pelo domínio atmarket.agrotools.com.br. Produto principal é entregue por painel whitelabel ou via API ao sistema do cliente.

## Conhecimento externo aplicável
- Agrotools é a líder histórica de geoinformação para o agro brasileiro (fundada em São José dos Campos, ecossistema INPE).
- 1.300+ camadas GIS, integração com Planet, Sentinel, MapBiomas, CAR, Ibama, ICMBio, Funai, INCRA.
- Clientes: Cargill, Bunge, Minerva, Marfrig, BNDES, Banco do Brasil, Itaú Agro.
- Forte em compliance antidesmatamento (pré-EUDR) e due diligence de fornecedor.
- Equipe técnica pesada em sensoriamento remoto, não em software product.

## Insights para AgroJus
1. **Fazer diferente:** Agrotools vende PARA o comprador/financiador/segurador da cadeia. AgroJus deve vender para o advogado do produtor — quem defende o lado oposto das acusações de desmatamento/irregularidade que a Agrotools produz.
2. **Copiar:** catálogo modular por "solução" (Financiamento, ESG, Seguro, Supply, Proteção de Marca). AgroJus pode ter módulos verticais por problema jurídico (Embargo, Multa, Crédito negado, Desapropriação).
3. **Copiar:** integração massiva de camadas GIS como diferencial. AgroJus já tem MapBiomas+CAR+BigQuery; precisa expor isso visualmente no produto.
4. **Fazer diferente:** Agrotools esconde o produto (placeholders SVG). AgroJus deve ter screenshots reais e demo ao vivo — advogado não compra sem ver.
5. **Copiar:** arquitetura de personas no marketing (comprador/financiador/segurador/vendedor). AgroJus pode espelhar (advogado / produtor / banco rural / perito).
6. **Fazer diferente:** Agrotools é opaca em preço (enterprise R$ 50k/mês). AgroJus deve ter tier PRO R$ 299-999/mês e tier Enterprise com preço sob consulta — democratiza acesso.
7. **Copiar:** ATMarket como marketplace sub-domínio — dá para criar "AgroJus Precedentes" ou "AgroJus Dados" como sub-portais independentes.
8. **Fazer diferente:** Agrotools é eng-forward sem UX. AgroJus deve ser UX-forward: mapa click-to-drawer, filtros visíveis, paleta dark Forest/Onyx.

## Gaps vs AgroJus

| Feature concorrente | AgroJus hoje | Prioridade |
|---|---|---|
| 1.300+ camadas GIS | ~20 camadas MapBiomas+BigQuery+EE | ALTA (expandir catálogo) |
| Análise de risco de produtor (seg/fin) | Não temos scoring | MÉDIA |
| Compliance ESG antidesmatamento | Temos dados; falta produto empacotado | ALTA |
| Rastreabilidade supply chain | Não temos | BAIXA |
| Catálogo enterprise com SLA e API | Parcial | MÉDIA |
| Multi-idioma (PT/EN/ES) | Só PT | BAIXA |
| Marketplace de dados (ATMarket) | Não temos | BAIXA (futuro) |
| Preço enterprise opaco | AgroJus deve ter preço visível | ALTA (diferencial) |
| Posicionamento pró-acusador | AgroJus é pró-defesa | ALTA (posicionamento) |
