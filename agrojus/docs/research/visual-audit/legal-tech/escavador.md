# Escavador

- **URL:** https://www.escavador.com/
- **Categoria:** legal-tech
- **Data auditoria:** 2026-04-17
- **Acesso:** freemium (pesquisa gratuita limitada; API e monitoramento pagos)

## Status da auditoria

A landing page `https://www.escavador.com/` e `/sobre` responderam HTTP 403 ao WebFetch (proteção anti-bot — provavelmente Cloudflare ou similar). A auditoria foi feita com base em:
- `https://api.escavador.com/` (página institucional da API — respondeu)
- `https://api.escavador.com/v2/docs/` (documentação técnica — respondeu)
- Conhecimento externo marcado na seção própria

## Propósito declarado

Plataforma de **dados jurídicos brasileiros** com cobertura nacional. Tagline da seção API: "Cobertura nacional! Cobrimos todos os tribunais do Brasil" — monitoramento de **+440 sistemas de tribunais** e **+175 diários oficiais**. Posicionamento central: agregador universal de processos (450M+ processos indexados, segundo material público histórico).

## Layout e navegação

Como o site público bloqueou o fetch, este bloco cobre apenas o que aparece no subdomínio da API (`api.escavador.com`), que é minimalista:
- Header simples com logo Escavador + links "Docs", "Central de Ajuda", "Painel", "Tokens", "Callbacks"
- Seções institucionais explicando casos de uso (consulta, monitoramento, integração com CRMs jurídicos)
- Footer com contato e link para suporte (`suporte-api.escavador.com`)

Painel do cliente (inferido pela estrutura da doc): dashboard com abas para **Tokens**, **Callbacks** (webhooks), **Serviços** (pricing por endpoint), **Histórico de consumo**.

## Features principais observadas

Extraídas da documentação v2:

1. **Consulta de processos** por número CNJ, com movimentações, documentos e envolvidos
2. **Busca por OAB** — retorna todos os processos do advogado + resumo
3. **Busca por CPF/CNPJ ou nome** — processos do envolvido + resumo IA
4. **Resumo inteligente** — geração de resumos de processos via IA
5. **Atualização de processos em lote** com status de requisição
6. **Monitoramento** em dois modos:
   - Novos processos (quando a pessoa/empresa aparece em processo novo)
   - Processos específicos (movimentações)
7. **Certificados digitais** — gerenciamento para autenticação em tribunais
8. **Webhooks/callbacks** para eventos: novo processo, atualização concluída, nova movimentação, processo verificado/não encontrado
9. **Listagem de tribunais/sistemas** disponíveis (descoberta de cobertura)
10. **Diários oficiais** — +175 diários monitorados

## UX / interações

Inferido pela API (o painel reflete a mesma estrutura):
- **Busca unificada por identificador** — o mesmo endpoint conceitual atende OAB, CPF, CNPJ e CNJ (discriminação por rota)
- **Paginação dupla**: numerada (`?page=2&per_page=25`) para listas estáveis e cursor (`?cursor=...&limit=25`) para dados dinâmicos (movimentações recentes). Padrão sofisticado.
- **Assinatura de eventos** via callbacks HTTP — UX de "configure a URL e esqueça", típico de SaaS maduro
- **Header de consumo** (`Creditos-Utilizados`) em cada resposta — transparência de custo em tempo real

## Preço e modelo de negócio

- **Sem tabela pública.** Texto da API: "O preço vai depender do serviço utilizado. Cada um dos serviços disponíveis tem seu custo especificado em nossa página de serviços no painel da API."
- Modelo de **crédito por chamada** (cobrança em centavos, exposta no header `Creditos-Utilizados`)
- Recomendação explícita de contato com especialistas para cotação → orientação enterprise
- Freemium na camada de consumidor final (site público permite consulta gratuita limitada — conhecido externamente, não confirmado no fetch)

## API pública (se houver)

**Sim, API v2 madura.** Destaques:

- **Base URL:** `https://api.escavador.com/api/v2`
- **Autenticação:** Personal Access Tokens (PAT) no padrão `Authorization: Bearer {token}`, gerados em `https://api.escavador.com/tokens`
- **Segurança:** HTTPS/TLS 1.2+, revogação imediata, **server-to-server apenas** (documentação avisa explicitamente para não usar em frontend)
- **Rate limit:** 500 req/min global
- **Paginação:** numerada ou cursor, com links `first/last/prev/next` e meta `current_page/total`
- **Webhooks:** configuráveis em `https://api.escavador.com/callbacks`, com token de segurança no header `Authorization` da requisição para validação
- **Módulos:** Processos, Atualização em lote, Monitoramento, Resumo IA, Certificados digitais, Tribunais

## Autenticação

- **Painel do cliente:** login convencional (email/senha) — não confirmado por fetch, inferido
- **API:** Personal Access Token (PAT) Bearer. Sem OAuth aparente. Token gerado no painel.
- **Certificados digitais:** gerenciados pela plataforma para autenticar acesso a sistemas de tribunal que exigem A1/A3 — feature rara.

## Conhecimento externo aplicável

> *Marcado como conhecimento externo, não confirmado no fetch desta auditoria.*

- Escavador historicamente publicou ter **450M+ processos indexados** e atua desde ~2014
- Landing pública (`www.escavador.com`) oferece campo de busca universal central (nome, CPF, CNPJ, OAB, nº processo) — padrão "single search bar" estilo Google
- Resultados de pessoa costumam incluir: dados cadastrais, vínculos societários, processos como parte/advogado, endereços, citações em diários
- Perfis de advogado têm página pública SEO-friendly com lista de processos (útil para ranking)
- Tier "Premium" para usuários finais custa historicamente faixa de R$ 40-90/mês
- Há produto paralelo **Escavador Jurimetria** focado em estatística processual
- Integração com CRMs jurídicos (CP-Pro, ADVBOX, Projuris) via API é caso de uso promovido

## Insights para AgroJus (pelo menos 5 concretos)

1. **Single search bar polimórfica:** o mesmo campo aceita OAB, CPF, CNPJ, nome, número CNJ — roteamento por regex/heurística. Nosso `/publicacoes` pode ter um search único que reconhece automaticamente o tipo (OAB → filtro por advogado, CNJ → filtro por processo, CPF/CNPJ → filtro por parte).
2. **Paginação cursor para feeds dinâmicos:** DJEN é um feed que muda constantemente. Trocar paginação numerada por cursor evita duplicatas/perdas quando novas publicações entram no topo. Escavador distingue os dois casos explicitamente.
3. **Webhook pattern com token de validação:** callback HTTP com `Authorization` header próprio — padrão a adotar no AgroJus quando formos emitir eventos de novas publicações para escritórios integrados.
4. **Transparência de custo inline:** header `Creditos-Utilizados` em cada resposta. Podemos adicionar header `X-AgroJus-Cost-Cents` para consultas pagas, ou um badge no painel mostrando "esta consulta custou R$ 0,12".
5. **Resumo IA como feature tier-2:** Escavador vende "resumo inteligente" como produto dentro da consulta. AgroJus pode empacotar resumos de publicações DJEN (intimação, decisão, despacho) com um botão "Resumir" que chama Claude/GPT e salva o output para reuso (cache).
6. **Separação clara "monitorar novos" vs "monitorar existentes":** dois modos distintos de assinatura. No `/publicacoes` podemos oferecer: (a) alertar quando advogado X aparecer em publicação nova, (b) alertar quando processo Y tiver movimento. São telas e fluxos diferentes.
7. **Dashboard de consumo/histórico:** espaço de "Histórico de consumo" com saldo e extrato. Mesmo sem cobrança de créditos, podemos oferecer ao usuário um timeline de suas próprias consultas recentes — reutilização e auditoria.

## Gaps vs AgroJus (tabela markdown)

| Aspecto | Escavador | AgroJus (atual) | Gap / Oportunidade |
|---|---|---|---|
| Cobertura de processos | +440 sistemas, +175 diários | DJEN (feed público) | Expandir ingestão para TJs individuais |
| API pública | PAT Bearer, webhooks, rate limit 500/min | Endpoints Supabase diretos | Montar API pública versionada com PAT |
| Monitoramento | Novos + existentes, duas telas | Painel único de publicações | Criar dois modos explícitos de alerta |
| Resumo IA | Endpoint dedicado | Não tem | Botão "Resumir publicação" com LLM |
| Paginação | Cursor + numerada | Numerada (presumido) | Implementar cursor para feed DJEN |
| Certificado digital | Gerenciado pela plataforma | Fora do escopo | Não urgente — foco é consulta, não peticionamento |
| Transparência de custo | Header por resposta | N/A | Útil quando/se houver cobrança |
| Busca polimórfica | Single bar aceita OAB/CPF/CNPJ/CNJ | Filtros separados (inferido) | Search bar unificada com detecção automática |
| Integração CRM | Promovida, documentada | Não comunicada | Listar integrações possíveis (Projuris, ADVBOX) |
| Callbacks/webhooks | Sim, com validação por token | Não implementado | Oferecer webhooks para clientes enterprise |
