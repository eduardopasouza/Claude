# Jusbrasil

- **URL:** https://www.jusbrasil.com.br/
- **Categoria:** legal-tech
- **Data auditoria:** 2026-04-17
- **Acesso:** freemium (consulta pública indexada; Jusbrasil Pro / Advogados é pago)

## Status da auditoria

**Fetch bloqueado.** Todos os endpoints testados retornaram HTTP 403:
- `https://www.jusbrasil.com.br/`
- `https://www.jusbrasil.com.br/home`
- `https://www.jusbrasil.com.br/sobre`
- `https://advogados.jusbrasil.com.br/`
- `https://ajuda.jusbrasil.com.br/`
- `https://empresas.jusbrasil.com.br/`

A infraestrutura Jusbrasil usa WAF agressivo que bloqueia crawlers não-autenticados. **Todo o conteúdo abaixo é conhecimento externo explicitamente marcado** — não foi validado nesta auditoria por WebFetch. Recomendação: validar posteriormente via navegação manual ou captura de screenshots.

## Propósito declarado

*(conhecimento externo)*

Portal jurídico generalista brasileiro, posicionado como o maior agregador público de conteúdo jurídico indexado do país. Tagline histórica: "Conectando pessoas e a Justiça". Serve três públicos:

1. **Cidadão comum** — busca informações sobre direitos, modelos de petição, advogados
2. **Advogado** — plataforma Jusbrasil Advogados (perfil público, captação, monitoramento)
3. **Empresa** — Jusbrasil Empresas (gestão de processos, BI jurídico)

## Layout e navegação

*(conhecimento externo, não verificado)*

- **Header:** logo + search bar central ampla + CTA "Entrar" / "Cadastrar"
- **Hero:** campo de busca dominante (tipo Google), com placeholder rotativo ("busque por processo, artigo, advogado")
- **Seções abaixo do fold:** cards de jurisprudência em destaque, artigos da comunidade, diários mais consultados, listas de advogados
- **Footer:** extensivo, com links para tribunais, estados, áreas do direito, SEO-oriented
- **Navegação principal:** "Jurisprudência", "Diários", "Artigos", "Modelos", "Advogados", "Notícias"

## Features principais observadas

*(conhecimento externo)*

1. **Busca unificada** — aceita texto livre, nome, número CNJ, OAB, CPF/CNPJ; roteia para a vertical certa
2. **Jurisprudência indexada** — decisões de TJs, TRFs, STJ, STF, com filtros por tribunal/relator/data
3. **Modelos de peças** — templates de petição, contestação, recurso (área paga)
4. **Comunidade / Artigos** — advogados publicam conteúdo SEO para captar clientes
5. **Diários oficiais** — indexação de publicações, feed pesquisável
6. **Perfil público de advogado** — página com bio, artigos, áreas de atuação, avaliações
7. **Monitoramento de processos** — alertas de movimentação (Jusbrasil Pro)
8. **Jusbrasil IA** — assistente jurídico lançado recentemente para resumir e redigir
9. **Captação de clientes** — "Consulta Jurídica" conecta cidadãos a advogados
10. **Dashboard de processos** — no plano Pro, painel com casos ativos, prazos, publicações

## UX / interações

*(conhecimento externo)*

- **Resultados em lista densa** com snippet destacando o termo buscado
- **Filtros laterais** tipo facetas (tribunal, tipo de documento, data)
- **Timeline de movimentações** no detalhe do processo, com badges coloridos por tipo
- **Cards de advogado** com foto, OAB, áreas, botão "Falar com advogado"
- **Painéis pagos** têm sidebar esquerda com "Meus processos", "Publicações", "Alertas"
- **Notificações por email** em digest diário com novas movimentações
- **Push no app mobile** (iOS/Android) para alertas urgentes

## Preço e modelo de negócio

*(conhecimento externo, valores aproximados; validar antes de citar)*

- **Jusbrasil Pro (consumidor):** faixa R$ 29-79/mês, acesso premium a jurisprudência e alertas
- **Jusbrasil Advogados:** plano mensal com perfil destacado, captação de leads, monitoramento
- **Jusbrasil Empresas:** enterprise, pricing sob cotação, inclui BI, API, integrações
- **Receita publicitária** pesada (Ads em páginas de jurisprudência e perfis gratuitos)
- Modelo híbrido: **SEO + freemium + marketplace de advogados**

## API pública (se houver)

*(conhecimento externo)*

Não há API pública aberta documentada. Jusbrasil Empresas oferece integrações sob contrato (webhooks, export), mas sem portal de desenvolvedor público.

## Autenticação

*(conhecimento externo)*

- Email/senha convencional
- Login social (Google, Facebook)
- OAB não é usada como identificador principal, mas é verificável no cadastro de advogado
- Plano Advogados exige validação de OAB ativa

## Conhecimento externo aplicável

Toda a auditoria deste arquivo é conhecimento externo. Fontes:
- Uso público histórico da plataforma (Jusbrasil é referência obrigatória no mercado brasileiro)
- Jusbrasil é conhecido por:
  - **SEO agressivo** — domina resultados Google para "jurisprudência + tema"
  - **Polêmicas recorrentes de privacidade** — exposição de processos com dados pessoais
  - **Lançamento de Jusbrasil IA em 2024-2025** — assistente LLM integrado
  - **M&A histórico** — comprou Jurídico Certo, outros
- Os valores de preço e features específicas **precisam ser validados** antes de usar em material de marketing comparativo

## Insights para AgroJus (pelo menos 5 concretos)

1. **SEO-first architecture:** cada processo, cada decisão, cada advogado tem URL pública amigável e indexável. AgroJus pode seguir padrão `/processo/{cnj}`, `/advogado/{oab}`, `/publicacao/{id}` com metadados ricos para captar tráfego orgânico no nicho agro/ambiental.
2. **Digest por email:** resumo diário agregando novas publicações dos clientes do advogado é UX estabelecido no mercado. Nosso `/publicacoes` deve ter um "Enviar resumo diário para meu email" como toggle simples no perfil.
3. **Facetas laterais:** filtros como sidebar esquerda (tribunal, data, tipo de documento, parte) é padrão consolidado. Se `/publicacoes` hoje tem filtros no topo, considerar versão sidebar para telas largas.
4. **Snippet com termo destacado:** cada resultado mostra 2-3 linhas de contexto com a query em negrito. Apostar em `<mark>` ou similar no feed DJEN.
5. **Perfil público do advogado:** mesmo sem ser marketplace, um `/advogado/{oab}` público SEO-friendly ajuda cobranças indiretas (advogado descobre AgroJus pesquisando o próprio nome).
6. **Badges coloridos na timeline:** Jusbrasil usa cores distintas para tipos de movimentação (intimação, decisão, sentença, despacho). Aplicar no feed DJEN com legenda fixa.
7. **App mobile com push:** advogados respondem mais rápido a push do que email. Considerar PWA com notificações para publicações críticas (prazo fatal detectado).
8. **Assistente IA integrado:** Jusbrasil adicionou LLM como feature tier superior. No AgroJus, oferecer "Resumir esta publicação" / "Explicar em linguagem simples" é diferencial de menor atrito.

## Gaps vs AgroJus (tabela markdown)

| Aspecto | Jusbrasil | AgroJus (atual) | Gap / Oportunidade |
|---|---|---|---|
| Escala de conteúdo | Bilhões de docs indexados | Feed DJEN focado | Não competir em volume — vencer em nicho agro/ambiental |
| SEO | Agressivo, domina Google | Não priorizado | URLs públicas, sitemap, OG tags por processo |
| Multi-público | 3 personas (cidadão/advogado/empresa) | Só advogado | Manter foco, não diversificar cedo |
| Marketplace de advogados | Sim, core do modelo | Não | Não replicar — diferenciar por análise de dados agro |
| App mobile | iOS + Android nativo | Web only (inferido) | PWA com push pode preceder app nativo |
| Comunidade / Artigos | Sim, grande acervo UGC | Não | Considerar newsletter/blog curado de agro-ambiental |
| IA integrada | Jusbrasil IA lançada | N/A | Prioritário — LLM resumindo publicações |
| Digest por email | Padrão | Não implementado | Feature low-hanging, alto engajamento |
| Badges de movimentação | Cores por tipo | Inferido básico | Formalizar legenda visual |
| Privacidade / LGPD | Polêmico | Oportunidade | Venda "privacy-first" como diferencial (agro tem dados sensíveis) |
