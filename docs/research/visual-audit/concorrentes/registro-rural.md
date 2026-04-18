# Registro Rural

- **URL:** https://www.registrorural.com.br/
- **Categoria:** concorrente
- **Data auditoria:** 2026-04-17
- **Acesso:** público para cadastro; app logado com planos pagos

## Status da auditoria
WebFetch retornou **403 Forbidden** em todas as tentativas (raiz e `/planos`), provavelmente por bloqueio de user-agent ou WAF (Cloudflare/Akamai). O conteúdo abaixo é composto por **conhecimento externo**, explicitamente marcado. Recomenda-se captura manual via navegador + screenshot para revalidar literalidade antes de virar decisão de produto.

## Propósito declarado (conhecimento externo)
Registro Rural se apresenta como a **maior base privada de CARs do Brasil** (16M+ propriedades mapeadas), oferecendo consulta, análise e monitoramento de propriedades rurais para produtores, consultores, bancos e escritórios de advocacia. Posicionamento central: "todo o Brasil rural em um só lugar".

## Layout e navegação (conhecimento externo)
Estrutura típica observada historicamente:
- **Header:** logo Registro Rural + menu "Home / Produtos / Planos / Mapa / Blog / Entrar / Cadastre-se".
- **Hero:** headline destacando "16 milhões de propriedades no mapa" + CTA "Experimente grátis" / "Ver planos".
- **Main:** seções por persona (Produtor / Consultor / Banco / Advogado) + demonstração de mapa + depoimentos.
- **Footer:** institucional, LGPD, redes sociais.
- Não verificado no fetch atual — MARCADO COMO INFERIDO.

## Features principais observadas (conhecimento externo)
- **Mapa interativo do Brasil rural** com 16M+ CARs ingeridos do SICAR.
- **Busca por CPF, CNPJ, nome, município, código CAR.**
- **Camadas sobrepostas:** SICAR, embargos Ibama, UCs, TIs, assentamentos INCRA, PRODES, DETER, matrículas (conforme plano).
- **Consulta de sobreposição** entre polígono e bases ambientais/fundiárias.
- **Monitoramento de alertas** (desmatamento, sobreposição, embargo) na carteira do usuário.
- **Relatório técnico** exportável por propriedade (PDF com evidência geoespacial).
- **Marketplace/diretório** de propriedades (possível, usado para compra/venda de terras).
- **API** em planos superiores.

## UX / interações (conhecimento externo)
Fluxo: cadastro (email) → onboarding com seleção de perfil → dashboard com mapa central + barra de busca → clicar propriedade → drawer lateral com dados CAR + camadas + botões "Gerar relatório" e "Salvar em pasta". Em planos pagos, área "Meus CARs" com monitoramento. Marketing e blog fortes para SEO em termos como "consultar CAR grátis", "ver CAR de um CPF", "como consultar CAR de um vizinho".

## Preço e modelo de negócio (conhecimento externo)
Modelo **freemium + SaaS mensal**:
- **Free:** consulta limitada ao mapa público.
- **Plano pago a partir de ~R$ 149/mês** (referenciado publicamente) com camadas premium, relatórios e monitoramento.
- Planos superiores (Profissional / Consultor / Enterprise) com API, maior volume de consultas e integração.
- Diferencial do mercado: **preço acessível e autoatendimento**, enquanto concorrentes (Agrotools, Serasa) são enterprise opacos.

## Autenticação (conhecimento externo)
- **Cadastro por email + senha**, com trial gratuito.
- Sem login gov.br.
- Áreas pagas exigem assinatura ativa.

## Conhecimento externo aplicável
- Registro Rural é o concorrente MAIS PRÓXIMO do AgroJus em modelo de negócio (freemium, PT, self-service, advogados/consultores pequenos).
- Força comercial vem de SEO pesado em termos de consulta CAR (principal funil).
- Stack aparente é SPA moderna (provavelmente React/Next com mapa via Mapbox GL ou Leaflet).
- Base de dados: ingere CAR do SICAR + embargos + UCs + matrículas públicas.
- Ponto fraco conhecido: sem IA generativa, sem pipeline jurídico (só mostra dado, não gera peça nem ajuda em defesa).
- Público: consultor ambiental, corretor de terras, produtor, advogado agrarista; grandes escritórios não adotam como única ferramenta.

## Insights para AgroJus
1. **Copiar:** modelo **freemium + preço acessível (~R$ 149/mês)**. É a faixa certa para advogado solo/boutique — AgroJus pode precificar próximo disso no tier inicial e cobrar mais pelos módulos de IA/redação.
2. **Copiar:** **SEO pesado em consulta CAR** — é funil barato. AgroJus deve ter páginas públicas "consultar CAR por CPF", "CAR do município X", "imóveis rurais em Y".
3. **Copiar:** mapa-central-primeiro no produto. Usuário entra e vê o Brasil rural; filtros/busca orbitam o mapa. Confirma o direcionamento do AgroJus Forest/Onyx.
4. **Copiar:** onboarding por perfil (produtor / consultor / banco / advogado) mudando o que aparece no dashboard.
5. **Fazer diferente:** Registro Rural ENTREGA DADO. AgroJus deve ENTREGAR DECISÃO — "aqui está o dado + aqui está o risco jurídico + aqui está a minuta de defesa". Dado é commodity, decisão+peça é valor.
6. **Fazer diferente:** Registro Rural não tem IA generativa. AgroJus tem mIA — vira moat imediato.
7. **Copiar:** relatório PDF exportável por propriedade como entregável-chave. Advogado adora algo anexável.
8. **Fazer diferente:** Registro Rural atende o ato de consultar. AgroJus atende a jornada completa (consultar → defender → monitorar → peticionar).
9. **Copiar:** volume de CARs como métrica de vaidade (16M). AgroJus pode usar "X mil fazendas indexadas + Y camadas conectadas + Z precedentes".

## Gaps vs AgroJus

| Feature concorrente | AgroJus hoje | Prioridade |
|---|---|---|
| 16M+ CARs indexados | Parcial (ingestão CAR limitada) | ALTA |
| Mapa central no produto | Em construção (Next.js 14) | ALTA |
| Freemium R$149/mês self-service | Sem billing | ALTA |
| Relatório PDF por propriedade | Não temos gerador | ALTA |
| Monitoramento de carteira | Roadmap | ALTA |
| Busca por CPF/CNPJ/nome | Parcial | ALTA |
| SEO orgânico em consulta CAR | Não temos | ALTA |
| Onboarding por perfil | Não temos | MÉDIA |
| API em plano enterprise | Não temos | MÉDIA |
| Camada fundiária (matrícula) | Não temos | ALTA |
| IA generativa de defesa | Temos (mIA) | ALTA (diferencial) |
| Pipeline jurídico end-to-end | Temos (mIA) | ALTA (diferencial) |
