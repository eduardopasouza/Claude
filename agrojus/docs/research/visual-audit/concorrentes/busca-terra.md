# Busca Terra

- **URL:** https://buscaterra.com.br/
- **Categoria:** concorrente
- **Data auditoria:** 2026-04-17
- **Acesso:** público (institucional); mapa interativo em subdomínio mapas.consultaterra.com.br

## Propósito declarado
"Data and information about rural properties" / "Information is our business". A Busca Terra (também opera como Consulta Terra) posiciona-se como **centralizadora de informação territorial e fundiária rural**, com base de dados geoespacial integrando cartórios, CAR, INCRA e órgãos ambientais para reduzir risco de mercado de terras e apoiar ESG/crédito.

## Layout e navegação
- **Header:** menu horizontal com "HOME | IMÓVEIS RURAIS | GEOPROCESSAMENTO | ABOUT US | CONTACT | PLATAFORMS | More".
- Submenu "IMÓVEIS RURAIS" → "TO VIEW" com 3 sub-itens (avaliação, levantamento, regularização).
- Submenu "PLATAFORMS" → 3 variações de "Pagamento por Serviços Ambientais" + "Mapa Interativo".
- **Hero:** imagem de fundo rural + headline em inglês "data and information about rural properties" + subtítulo "Information is our business" + CTA "👉 Entre em contato".
- **Main:** cartões de serviço (Avaliação, Levantamento, Mapa Interativo, Regularização Fundiária) + seção ESG + trust badges.
- **Footer:** email contato@buscaterra.com.br, redes sociais (Instagram, Facebook, LinkedIn, YouTube, Twitter), links institucionais (About Us, Terms, Privacy, Work with us), copyright 2022 (site parece desatualizado).
- Mapa interativo vive em subdomínio separado (`mapas.consultaterra.com.br`), padrão comum de sites feitos em Wix/Squarespace que hospedam o app web à parte.

## Features principais observadas
- **Avaliação de Imóvel Rural:** laudo de avaliação econômica de propriedade.
- **Levantamento de Imóveis Rurais:** due diligence fundiária (cartório, matrícula, sobreposições).
- **Regularização Fundiária:** apoio a processo de titulação, georreferenciamento INCRA.
- **Mapa Interativo:** ferramenta de consulta geográfica com camadas públicas.
- **Pagamento por Serviços Ambientais (PSA):** três variações de módulo voltado a estruturar projetos de PSA.
- **Geoprocessamento sob demanda.**
- Texto institucional cita banco "centralized, updated, spatialized and georeferenced" e integração com mais de 100 bases públicas (conhecimento externo).

## UX / interações
Site institucional simples, bilíngue truncado (misturando PT e EN). Produto real está no mapa interativo externo — presumível: busca por município/CPF/matrícula → desenha polígono ou clica na propriedade → drawer lateral com dados da matrícula, CAR, sobreposições, PRODES, UCs, TIs. Experiência clássica de "GIS viewer" mais próxima de ferramenta técnica que de produto polido.

## Preço e modelo de negócio
Nenhum preço visível. Modelo é tipicamente serviço + plataforma:
- Projeto de levantamento/regularização por propriedade (preço sob consulta, ~ R$ 2k-15k por imóvel).
- Acesso ao mapa interativo em plano mensal/anual (não detalhado publicamente).
- Consultoria em PSA e créditos ambientais.
Atende cartórios, bancos, produtores e escritórios de advocacia rural.

## Autenticação
Não identificada no fetch. O mapa interativo em subdomínio pode exigir login próprio (email/senha). Sem gov.br.

## Conhecimento externo aplicável
- Busca Terra/Consulta Terra integra mais de 100 bases públicas (CAR, SNCI, INCRA, Sigef, matrículas, PRODES, MapBiomas, UCs, TIs).
- Público-alvo inclui advogados agraristas, cartórios, peritos judiciais, corretores de terras, bancos regionais.
- Diferencial de mercado é a profundidade em **dado fundiário e cartorário** (matrícula + sobreposição), que Agrotools e Serasa tratam de forma mais superficial.
- Site institucional parece pouco mantido (footer 2022) — operação pode estar concentrada no app de mapa.

## Insights para AgroJus
1. **Copiar:** foco em dado cartorário/matrícula + CAR + sobreposição — é exatamente o tipo de conteúdo que o advogado agrarista precisa. AgroJus deve integrar matrícula (SNCI/cartórios) como camada de primeira classe.
2. **Copiar:** separar "mapa interativo" como produto/subdomínio. Dá para lançar `mapa.agrojus.com` antes de ter login complexo no app principal.
3. **Fazer diferente:** Busca Terra mistura serviço (projeto de regularização) com plataforma (mapa). AgroJus deve ser plataforma-first; serviço consultivo opcional.
4. **Copiar:** módulo PSA (Pagamento por Serviços Ambientais) — advogados agraristas lidam com isso em áreas de RL/APP.
5. **Fazer diferente:** UX do Busca Terra aparenta ser de ferramenta técnica crua. AgroJus deve investir em drawer elegante, paleta Forest/Onyx, filtros visíveis, UX premium.
6. **Fazer diferente:** site bilíngue mal-feito prejudica credibilidade. AgroJus deve ser PT-first, bem feito, e inglês apenas se houver plano real de expansão.
7. **Copiar:** menu categorizado por TIPO DE ATIVO (Imóvel Rural) em vez de tipo de dado. Advogado pensa em "a fazenda do Fulano", não em "camada X".

## Gaps vs AgroJus

| Feature concorrente | AgroJus hoje | Prioridade |
|---|---|---|
| 100+ bases públicas integradas | Parcial (~10 conectadas) | ALTA |
| Dado cartorário/matrícula | Não temos ingestão de matrícula | ALTA |
| Módulo de avaliação de imóvel | Não temos | MÉDIA |
| Módulo de regularização fundiária | Não temos workflow | MÉDIA |
| Módulo PSA (serviços ambientais) | Não temos | BAIXA |
| Mapa interativo público | Em construção (Next.js 14) | ALTA |
| Sobdomínio dedicado ao mapa | Não temos, mas estratégia válida | MÉDIA |
| Site bilíngue | Site PT apenas (por design) | BAIXA |
| Due diligence fundiária como fluxo | Não temos | ALTA |
