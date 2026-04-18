# SICAR — Sistema de Cadastro Ambiental Rural

- **URL:** https://www.car.gov.br/publico/imoveis/index (redireciona para https://consultapublica.car.gov.br/publico/)
- **Categoria:** fonte-gov
- **Data auditoria:** 2026-04-17
- **Acesso:** público (consulta); login exclusivo para cadastro

## Status da auditoria
A URL original redireciona 302 para `consultapublica.car.gov.br` — que apresentou erro de certificado SSL inválido ao WebFetch ("unable to verify the first certificate"), impedindo a leitura direta da interface de consulta pública. A página raiz `www.car.gov.br` foi auditada em substituição, cobrindo estrutura institucional e navegação de alto nível. As seções "Dados e funcionalidades expostas" abaixo que dependem da consulta em si estão marcadas como **conhecimento externo** (público, mas não auditado nesta sessão).

## Propósito declarado
O SICAR é o sistema nacional de gestão do Cadastro Ambiental Rural (CAR), instituído pela Lei 12.651/2012 (Código Florestal). Registra eletronicamente os imóveis rurais do país, declarando perímetro, áreas de preservação permanente (APP), reserva legal (RL), áreas de uso restrito, áreas consolidadas e remanescentes de vegetação nativa. É base de integração para regularização ambiental (PRA/PRADA) e para fiscalização.

## Layout e navegação
A página institucional `www.car.gov.br` estrutura-se em:

- **Header:** logo SICAR + menu principal ("Início", "Ajuda", "Sobre o CAR", "Central de Conteúdo").
- **Ações frequentes em cards:** "Central do Proprietário/Possuidor", "Baixar Módulo CAR" (aplicativo desktop offline), "Enviar arquivos .CAR", "Retificar cadastros".
- **Bloco de consultas:** link direto para "Consulta Pública" e busca individual por CAR.
- **Suporte:** assistente virtual, FAQ, contatos por órgão estadual competente.
- **Footer:** redes sociais (Facebook, Twitter, YouTube, SoundCloud) e recomendação de navegadores (Chrome, Firefox, IE9+) — assinatura visual de portal governamental legado.

A consulta pública em si está em subdomínio separado (`consultapublica.car.gov.br`), desacoplando o front institucional do front de dados — padrão comum em portais governamentais brasileiros.

## Dados e funcionalidades expostas
**Conhecimento externo aplicável (não auditado):**
- Consulta por código do CAR, município, estado ou demarcação em mapa interativo (Google Maps embutido com camadas WMS).
- Visualização individual da poligonal do imóvel com APP, RL, áreas consolidadas sobrepostas.
- Status do cadastro: Ativo / Pendente / Cancelado / Suspenso.
- Emissão de "Demonstrativo da Situação das Informações Declaradas" em PDF para qualquer imóvel publicamente consultado.
- Downloads em massa por estado/município (shapefile zipado) na Central de Downloads do SFB.

## UX / interações (consulta, busca, filtros, download)
Página institucional usa padrão **cards grandes com ícones** para ações primárias — baixa densidade informacional, foco em direcionar o cidadão a uma de quatro jornadas (cadastrar, consultar, retificar, baixar módulo).

Busca na consulta pública (conhecimento externo): formulário com drill-down geográfico (UF → Município) + input de código CAR. Resultado é mapa com poligonal destacada e painel lateral com atributos.

## API pública (endpoints, auth, formatos)
Não há menção a API pública ou webservices na página auditada. O Serviço Florestal Brasileiro publica, fora deste portal, uma Central de Downloads com shapefiles consolidados por UF em `https://www.car.gov.br/publico/municipios/downloads`. **Não existe endpoint oficial JSON/REST para consulta por imóvel** (conhecimento externo) — integrações terceirizadas (MapBiomas, AgroTools) fazem scraping ou usam shapefiles baixados.

## Rate limits / cotas conhecidas
Não declarados na interface. Conhecimento externo: downloads em massa por UF são disponibilizados mensalmente em ZIP único, e a consulta pública aplica CAPTCHA para individualizar buscas — limita scraping.

## Autenticação
- **Consulta pública:** sem login. CAPTCHA antes de exibir poligonal individual.
- **Cadastro/retificação:** login SICAR via CPF/CNPJ + senha própria (sistema anterior ao gov.br). A Central do Proprietário/Possuidor exige autenticação específica.
- Não integra gov.br no front institucional.

## Conhecimento externo aplicável
- Base do CAR é referência para ações possessórias e ambientais: a sobreposição de poligonais declaradas é litígio frequente.
- Shapefiles oficiais por UF têm atraso de 1-3 meses vs. base interna do SFB.
- Poligonais são **declaratórias** — não substituem matrícula e podem conter sobreposições, autodeclarações falsas ou desatualizadas.
- Integração com SIGEF/INCRA é assimétrica: CAR é declaratório, SIGEF é certificação georreferenciada.

## Insights para AgroJus (o que podemos reaproveitar visualmente)
1. **Cards grandes com ícone + verbo** para ações primárias (consultar, cadastrar, baixar, retificar) — o usuário rural/advogado está acostumado a esse padrão.
2. **Subdomínio para consulta pública** separado do institucional — AgroJus pode seguir o mesmo split (site marketing vs. app data).
3. **Demonstrativo PDF** é o "artefato final" esperado pelo advogado em consultas. AgroJus deve gerar relatório PDF com poligonal + atributos, não apenas JSON.
4. **Drill-down UF → Município** é o padrão geográfico esperado — manter esse fluxo em filtros do AgroJus.
5. **Visual legado** (IE9, Google Maps embutido): AgroJus pode diferenciar com Mapbox/MapLibre e dark mode moderno sem perder familiaridade.

## Gaps vs AgroJus (tabela)

| Dimensão | SICAR | AgroJus (alvo) |
|---|---|---|
| API REST | Ausente | JSON/REST documentada (OpenAPI) |
| Sobreposição automática | Manual, 1 imóvel por vez | Cross-layer CAR × SIGEF × MapBiomas × ANM |
| Dark mode | Não | Sim (Forest/Onyx) |
| Autenticação | Login SICAR próprio | gov.br + OAuth |
| Rate limit declarado | Oculto (CAPTCHA) | Documentado (tier free/pro) |
| Exportação em lote | Shapefile UF mensal | GeoJSON/CSV/Parquet por filtro |
| Histórico temporal | Não | MapBiomas Alerta integrado |
| Busca por CPF/CNPJ do proprietário | Não pública | Core do AgroJus (cruzamento possessório) |
| Atributos APP/RL | Exibidos | Exibidos + risco calculado |
| Contraditório automático | Ausente | Detecção de sobreposições e divergências |
