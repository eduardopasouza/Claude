# Intima.ai

- **URL:** https://intima.ai/
- **Categoria:** legal-tech
- **Data auditoria:** 2026-04-17
- **Acesso:** pago (com possível trial; sem preços públicos)

## Status da auditoria

**Fetch parcial.** O site é SPA (React/Next, renderização cliente) e o WebFetch captura apenas o shell HTML. Resultados:
- `https://intima.ai/` → apenas retorna o headline "API para automatização de serviços dos sistemas judiciais eletrônicos (PJe, PROJUDI, e-SAJ, e-PROC)" e referência a widget Intercom; sem detalhes de features, layout ou preço
- `https://intima.ai/precos`, `/planos`, `/api`, `/docs` → 404
- `https://developers.intima.ai/`, `https://docs.intima.ai/`, `https://api.intima.ai/docs` → ECONNREFUSED (subdomínios inexistentes)

Conclusão: o WebFetch não consegue extrair a landing renderizada. Conteúdo principal abaixo vem de **conhecimento externo explicitamente marcado**; apenas o headline está confirmado por fetch.

## Propósito declarado

**Confirmado por fetch:** *"API para automatização de serviços dos sistemas judiciais eletrônicos (PJe, PROJUDI, e-SAJ, e-PROC)"*.

Posicionamento: infraestrutura de automação judicial para advogados e escritórios, reduzindo trabalho manual de login, navegação e download/upload nos sistemas de tribunal.

## Layout e navegação

**Não capturável por fetch** (SPA). Inferência baseada em conhecimento externo (marcada abaixo).

## Features principais observadas

*(headline confirmado; demais itens = conhecimento externo)*

Sistemas suportados (confirmados no headline):
1. **PJe** (Processo Judicial Eletrônico — Justiça do Trabalho, Federal, alguns estaduais)
2. **PROJUDI** (vários estaduais)
3. **e-SAJ** (TJSP e outros)
4. **e-PROC** (TRF4, TRF2 e alguns estaduais)

Automações típicas da categoria (inferência):
- Download automático de intimações e publicações
- Peticionamento eletrônico programático
- Monitoramento de movimentações processuais
- Upload de documentos em lote
- Consulta de andamento
- Extração de autos completos

## UX / interações

*(conhecimento externo)*

- Painel web centralizando publicações/intimações de múltiplos sistemas
- Lista unificada de intimações com origem (PJe, e-SAJ, etc.) sinalizada como badge
- Fluxo de "protocolar petição" abstraindo os cliques do PJe
- Notificações quando chega publicação nova

## Preço e modelo de negócio

*(conhecimento externo; preços não verificados)*

- Cobrança por **volume de automações/créditos**, tipicamente (modelo comum do setor)
- Planos por faixa de advogados/escritórios
- Sem pricing público; venda consultiva

## API pública (se houver)

*(conhecimento externo, não verificado nesta auditoria)*

Intima.ai se posiciona explicitamente como **API-first** — o próprio nome de domínio e tagline reforçam. Subdomínios testados não responderam, mas historicamente a documentação fica em `docs.intima.ai` ou similar (URL exata precisa ser verificada pelo usuário).

Recursos esperados na API (padrão do setor):
- Endpoint para cadastrar certificado A1 do advogado
- Endpoint para consultar publicações/intimações
- Endpoint para peticionar (upload de documento + metadados)
- Webhooks para nova publicação

## Autenticação

*(conhecimento externo)*

- **Certificado digital A1** é o pivô: cliente carrega o `.pfx` + senha, a plataforma usa como proxy para autenticar nos sistemas judiciais
- **Token/API key** da plataforma para chamadas de aplicação
- Diferença crítica vs. Judit/Escavador: Intima.ai **atua em nome do advogado** nos sistemas reais, não apenas consulta dados

## Conhecimento externo aplicável

> *Tudo nesta seção é inferência não validada pelo fetch; marcar como não-confirmado.*

- Intima.ai é referência brasileira em **RPA judicial as-a-service**: substitui robôs locais que advogados montavam com Selenium
- Nicho específico: escritórios que peticionam em volume (trabalhista, consumidor) e precisam automatizar fluxo repetitivo
- Concorrentes diretos: Legal One (Thomson), Aurum (RobotAdv), Projuris (automação)
- Caso de uso típico: *"toda manhã às 7h, baixar todas as intimações de todos os meus processos em PJe e e-SAJ e me enviar um digest"*
- Diferencial crítico: suporta **peticionamento** (ação de escrita), não apenas leitura — isso implica cofre de certificado e responsabilidade técnica/jurídica maior
- Risco conhecido do setor: tribunais mudam leiaute de portal, automação quebra; Intima.ai provavelmente oferece SLA para reparar

## Insights para AgroJus (pelo menos 5 concretos)

1. **Painel unificado multi-sistema:** se AgroJus algum dia integrar além do DJEN (ex: ler diretamente TJMA, TRF1, etc.), adotar o padrão "origem como badge" — cada publicação mostra de onde veio, e o advogado não precisa se preocupar com qual sistema consultou.

2. **Cofre de certificado A1 é feature premium:** não é nosso foco agora, mas é o bilhete de entrada para peticionamento. Se o AgroJus quiser virar plataforma de *ação* (não só *observação*), vai precisar.

3. **Separação "leitura" vs "escrita":** Intima.ai é caro porque faz escrita (peticionar). AgroJus é barato porque só lê (DJEN público). Podemos posicionar explicitamente: "leitura premium, escrita sob roadmap". Define expectativas.

4. **Webhook de "nova publicação" como output:** Intima.ai provavelmente emite eventos via webhook. Nosso diferencial pode ser *receber* webhooks de Intima.ai e unificar no painel AgroJus — integração em vez de competição.

5. **Digest matinal programável:** advogados esperam "chegar às 7h da manhã e ter tudo pronto". Feature importante no `/publicacoes`: agendamento de resumo diário por email com hora configurável.

6. **Padronização de metadados entre sistemas:** se juntarmos dados de PJe e e-SAJ, os schemas divergem. Intima.ai já fez esse trabalho (provavelmente). AgroJus, ao expandir, vai enfrentar o mesmo. Copiar os campos normalizados deles é atalho.

7. **Posicionamento "API-first" é vendável:** Intima.ai dobra a aposta em desenvolvedores. AgroJus pode publicar OpenAPI spec desde cedo — atrai integradores.

## Gaps vs AgroJus (tabela markdown)

| Aspecto | Intima.ai | AgroJus (atual) | Gap / Oportunidade |
|---|---|---|---|
| Cobertura de sistemas | PJe, Projudi, e-SAJ, e-Proc | Apenas DJEN (feed agregado) | Expansão futura para portais individuais |
| Automação (escrita) | Peticiona, faz upload | Não faz | Fora do roadmap próximo |
| Certificado A1 | Cofre gerenciado | Não | Só se pivotarmos para escrita |
| API-first | Posicionamento central | Interno (Supabase) | Publicar OpenAPI versionada |
| Monitoramento | Sim, core | Sim (DJEN) | Paridade parcial |
| Digest matinal | Provável | Não implementado | Feature low-hanging |
| Preço | Alto (automação + SLA) | Barato (leitura) | Posicionar como camada leitura acessível |
| Multi-sistema unificado | Sim | Só DJEN | Longo prazo |
| Foco setorial | Horizontal (qualquer área) | Agro/ambiental | Diferencial de nicho |
| Widget de suporte | Intercom (confirmado) | ? | Adotar chat embedded para enterprise |
