# DJEN — Diário da Justiça Eletrônico Nacional (Comunica PJe)

- **URL:** https://comunica.pje.jus.br/
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (consulta); API pública com requisição direta

## Status da auditoria
O endpoint principal do Comunica PJe rejeitou WebFetch retornando conteúdo insuficiente (o SPA renderiza em JS) e o endpoint de API retornou HTTP 403 (provavelmente por falta de user-agent válido ou exigência de header específico). Descrevo abaixo com base em conhecimento público documentado da Resolução CNJ 455/2022 e da wiki técnica do projeto, marcando o que é **conhecimento externo**.

## Propósito declarado
Portal e API do Diário da Justiça Eletrônico Nacional, instituído pela Resolução CNJ 455/2022 como diário unificado nacional, substituindo os diários individuais de cada tribunal. Concentra publicações, intimações e comunicações processuais de todos os tribunais aderentes.

## Layout e navegação
**Conhecimento externo:**
- Página inicial: formulário de busca com filtros OAB, número de processo CNJ, nome das partes, data, tribunal.
- Resultado em cards/lista com: data da publicação, tribunal, processo, trecho da publicação + botão "Visualizar íntegra" (PDF) e "Copiar link".
- Menu superior: "Início", "Sobre", "Ajuda", "Acesso restrito" (para tribunais).
- Footer com marca CNJ/PJe.

## Dados e funcionalidades expostas
**Conhecimento externo:**
- Publicações oficiais de tribunais federais e estaduais integrados (adesão progressiva iniciada em 2023-2024).
- Cada publicação contém: data de disponibilização, data de publicação (útil para contagem de prazo), órgão julgador, classe, processo CNJ, partes, advogados, trecho e PDF íntegra.
- Busca por **nome do advogado + OAB** é o caso de uso primário.

## UX / interações (consulta, busca, filtros, download)
**Conhecimento externo:**
- Busca com autocomplete para tribunal.
- Filtro por intervalo de datas.
- Exportação CSV de resultados (limitada em quantidade).
- PDF íntegra da publicação para download.
- Paginação clássica.

## API pública (endpoints, auth, formatos)
**Conhecimento externo:**
- Base: `https://comunicaapi.pje.jus.br/api/v1/comunicacao`.
- **Método:** GET com query params.
- **Parâmetros:** `numeroOab`, `ufOab`, `nomeAdvogado`, `numeroProcesso`, `dataDisponibilizacaoInicio`, `dataDisponibilizacaoFim`, `orgaoId`, `itensPorPagina`, `pagina`.
- **Formato:** JSON (`items[]` + paginação).
- **Autenticação:** pública, sem chave aparente (mas com proteções anti-abuso — 403 para bots sem UA adequado).
- Documentação oficial é escassa; integradores consultam via engenharia reversa ou fóruns.

## Rate limits / cotas conhecidas
Não declarados. Comportamento típico: 403/429 para requisições rápidas sem UA de navegador. Janela de dias consultável tem limite implícito (poucos dias por chamada) — integradores paginam por janela de tempo.

## Autenticação
- Consulta pública: anônima.
- API: não exige token, mas exige user-agent "browser-like".
- Sem integração gov.br na consulta.

## Conhecimento externo aplicável
- DJEN é **a fonte primária de prazos** no Judiciário atual — substitui DJEs estaduais progressivamente.
- Advogados monitoram DJEN por OAB — é o core do pipeline de prazos processuais.
- Dado cruza com DataJud (metadados) + movimentações de processo.
- Regra de prazo: disponibilização → publicação (1 dia útil) → contagem a partir do dia útil seguinte à publicação.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Busca por OAB** é o form-factor esperado do advogado — AgroJus deve ter "painel do advogado" centrado em OAB.
2. **Card de publicação com data disponibilização + data publicação** é o layout consolidado. AgroJus deve preservar ambas (são legalmente distintas).
3. **Link direto para PDF íntegra** é a prova documental — AgroJus precisa armazenar/cache PDFs para rastreabilidade.
4. **API GET simples com query string** é acessível — AgroJus pode oferecer endpoint similar de "últimas publicações por advogado".
5. **Resolução CNJ 455/2022 como base legal** é a narrativa de confiabilidade — citar normativa em cada módulo.
6. **Webhook por OAB** é o feature matador que falta no DJEN — AgroJus pode oferecer push realtime ao advogado.

## Gaps vs AgroJus (tabela)

| Dimensão | DJEN | AgroJus (alvo) |
|---|---|---|
| Propósito | Diário oficial unificado | Painel do advogado (prazos + insights) |
| API | GET JSON simples | REST + webhook + push mobile |
| Autenticação | Anônima | gov.br + token + OAuth por OAB |
| Rate limit | Opaco | Por tier |
| Filtros | OAB, processo, data | OAB + caso AgroJus + cliente + matéria |
| Alerta push | Não | Sim (app + e-mail + WhatsApp) |
| Cálculo de prazo | Manual | Automático (considerando feriado + suspensão) |
| Cruzamento com caso | Manual | Automático (FIRAC + DJEN) |
| Armazenamento íntegra | Link ao PDF | Cache permanente + OCR |
| Extração de trecho relevante | Não | NLP (intimação, decisão, sentença) |
| Histórico temporal do advogado | Não | Timeline |
| Exportação | CSV limitado | CSV/Parquet/PDF relatório |
