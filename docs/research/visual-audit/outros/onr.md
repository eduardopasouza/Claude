# ONR — Operador Nacional do Registro de Imóveis

- **URL principal tentada:** https://map.onr.org.br/
- **URL alternativa acessada:** https://www.onr.org.br
- **URL adicional tentada:** https://buscaonr.org.br/busca-onr
- **Categoria:** mercado-dados (registro imobiliário)
- **Data auditoria:** 2026-04-17
- **Acesso:** parcialmente público; certidões e buscas detalhadas exigem pagamento e cadastro

## Status da auditoria
- `map.onr.org.br` → **ECONNREFUSED** (domínio de mapa interativo aparentemente offline ou migrado em 04/2026; confirma observação no próprio briefing).
- `www.onr.org.br` → acessível; conteúdo institucional descrito abaixo.
- `buscaonr.org.br` → **ECONNREFUSED**.

A auditoria consolida o que foi extraído do site institucional + conhecimento externo do **SREI (Sistema de Registro Eletrônico de Imóveis)** e da Lei 13.465/2017.

## Propósito declarado
"Instituição oficial encarregada de projetar e implementar o Sistema de Registro Eletrônico de Imóveis (SREI)", criado pela **Lei 13.465/2017**. Missão: viabilizar a **implantação unificada do registro eletrônico**, conectando os ~3.500 Cartórios de Registro de Imóveis (RI) do Brasil num ponto único de acesso digital.

## Layout e navegação
- Visual clean e institucional.
- Paleta azul/branco (autoridade institucional, similar a gov.br sem ser).
- **Service tiles** para os produtos principais.
- Integração com Instagram mostrando iniciativas.
- Botões de download dos apps iOS/Android em destaque.

## Features / dados expostos
Serviços listados:
- **RI Digital** — acesso centralizado aos registros imobiliários eletrônicos.
- **Ofício Eletrônico** — comunicação digital entre cartórios e órgãos públicos (ex.: Judiciário, Receita, INCRA).
- **CNIB 2.0** — Central Nacional de Indisponibilidade de Bens (quando juiz determina indisponibilidade, propaga para todos os RIs).
- **Penhora Online** — plataforma de registro digital de penhora.
- **Apps iOS/Android** — consulta móvel do cidadão.
- **PID — Programa de Inclusão Digital** — digitaliza cartórios menores que ainda operam em papel.

## UX / interações
O serviço público de busca (via `buscaonr.org.br`) permite **buscar pelo nome da pessoa em todos os RIs do Brasil** por uma taxa pequena. Retorna uma **lista de matrículas** potencialmente associadas. Para obter a matrícula em si (certidão), usuário é direcionado ao cartório específico com pagamento adicional.

Fluxo típico:
1. Usuário digita nome/CPF/CNPJ.
2. Sistema varre os RIs integrados (nem todos ainda estão).
3. Retorna ocorrências agrupadas por RI.
4. Usuário escolhe e paga certidão → PDF assinado digitalmente.

## Preço e modelo de negócio
- **Busca por nome**: taxa pequena (R$ 20-50 tipicamente).
- **Certidão individual**: emolumentos cartoriais (R$ 30-100 dependendo da UF).
- **SREI volume/empresarial**: acordos bilaterais para integradores (Serasa, Cenprot, fintechs).

## API pública (se houver)
- **Não há API aberta**. Integração se dá via convênios específicos (SREI-Empresarial). Fintechs e AgTechs acessam mediante contrato.
- Canais B2B: Ofício Eletrônico para órgãos públicos; integrações SOAP/REST privadas para clientes institucionais.

## Autenticação
- Consultas simples: pagamento via boleto/cartão.
- Apps: login gov.br / CPF + senha.
- B2B: tokens contratuais via convênio.

## Conhecimento externo aplicável
- O **registro de imóveis rurais no Brasil é crítico e fragmentado**. Cada matrícula fica num RI específico (cartório da comarca). Mesma fazenda pode ter várias matrículas (desmembramentos).
- O **SREI ainda está em implantação** (2017-2026): nem todos os cartórios estão digitalizados. Interior do país, especialmente Norte/Nordeste, ainda tem muito papel.
- **Buscas por nome** eram historicamente impossíveis (cada cartório respondia isoladamente). O ONR mudou o jogo — agora dá pra saber "Fulano tem imóvel em qual cartório do Brasil?".
- **Cruzamento com CAR/SIGEF/INCRA**: a matrícula do RI traz a descrição do imóvel (Memorial Descritivo). O CAR tem polígono. O SIGEF tem georreferenciamento certificado. **Nem sempre batem** — esse desalinhamento é o grande problema fundiário brasileiro, e AgroJus pode se diferenciar resolvendo.
- O ONR está em sprint de modernização; o site mapa (`map.onr.org.br`) aparentemente saiu do ar em 04/2026 — pode estar sendo migrado para nova versão ou integração maior com SERPRO/GOV.

## Insights para AgroJus
1. **Matrícula é fonte-verdade jurídica**: para valuation rural, o número da matrícula + RI + comarca é obrigatório no laudo. AgroJus deve ter integração direta (via convênio) ou, no mínimo, **link profundo para busca ONR** com CPF/CNPJ pré-preenchido.
2. **Cruzamento matrícula × CAR × SIGEF**: o diamante bruto. Se AgroJus monta base que correlaciona polígono CAR com matrícula ONR e certificação SIGEF, tem ativo único no mercado.
3. **CNIB como red flag**: antes de comprar um imóvel, checar se há indisponibilidade registrada no CNIB é essencial. AgroJus pode consultar (via convênio) e sinalizar automaticamente.
4. **Emolumento embutido no produto**: usuário AgroJus poderia comprar a certidão pelo próprio app, com repasse aos cartórios. Experiência Amazon vs. fricção atual.
5. **Parceria institucional com ONR**: é legítima. ONR busca ampliar uso do SREI. AgroJus traz público qualificado (advogados, peritos, bancos) e dados georreferenciados de volta — ganha-ganha.
6. **Mapa ONR offline é oportunidade**: o "mapa de matrículas" (map.onr.org.br) é conceito que AgroJus pode fazer melhor com CAR + matrícula consolidada.

## Gaps vs AgroJus (tabela)

| Dimensão | ONR | AgroJus |
|---|---|---|
| Escopo | Registro de imóvel (todos os tipos) | Imóvel rural especializado |
| Autoridade | Oficial SREI | Analítica (sem autoridade registral) |
| Cobertura de cartórios | Em implantação; nem todos integrados | Depende de ONR — limitação compartilhada |
| Busca por nome | Sim, nacional unificada | Via link ONR + enriquecimento |
| Cruzamento CAR/SIGEF | Não | Sim, core feature |
| UX | Institucional, serviços tile | Analítica, mapa, laudo |
| Mobile | Apps nativos | Web responsivo + apps futuros |
| API aberta | Não (convênios bilaterais) | REST pública com créditos por chamada |
| Preço | Emolumentos por certidão | SaaS AgroJus + repasse emolumentos |
| Red flags (CNIB, embargos) | Consulta isolada | Cruzado automaticamente com imóvel |
| Público | Cidadão/advogado genérico | Agro + jurídico + financeiro |
