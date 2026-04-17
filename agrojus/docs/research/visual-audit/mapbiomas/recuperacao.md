# MapBiomas Monitor da Recuperação

- **URL:** https://plataforma.recuperacao.mapbiomas.org/
- **Categoria:** mapbiomas (referência de vegetação secundária / restauração)
- **Data auditoria:** 2026-04-17
- **Acesso:** público

## Propósito declarado

Monitor de áreas de **recuperação de vegetação nativa**: regeneração natural e restauração ativa. Calcula idade da vegetação secundária (anos desde abandono/plantio), ganho e perda.

## Layout e navegação

**Estrutura tab-based idêntica à do Crédito Rural**, com 3 abas:
- Filtros / Camadas / Mapa base

Header:
- **Destaques** (editorial)
- **API** (link para `/api-docs` — **API documentada publicamente!**)

## Filtros observados

- Todos (autocomplete bioma/uf/municipio)
- **Switch toggle** (provável: restauração ativa vs regeneração natural)
- **Range duplo 2000-2025** — anos início/fim (slider)
- **Busca por código de embargo**: placeholder `br-emb-00000000`
- **Busca por código CAR**: placeholder `TO-0000000-000000000000000`
- 5 comboboxes "Escolha uma opção" encadeados (provavelmente: UF → município → bioma → classe → categoria)
- Resetar / Buscar

**Facet de destaque:** consulta **CAR + Embargo** lado a lado — mesmo painel aceita os 2 identificadores. **Muito relevante para AgroJus.**

## Dois identificadores no mesmo painel

O filtro principal oferece campos separados para:
1. **Embargo IBAMA** (br-emb-XXXXXXXX)
2. **Código CAR** (UF-0000000-...)

Mostra que a UX **assume que o usuário típico tem ambos os identificadores** e quer cruzar. Isso é exatamente o caso de uso de advogado/compliance.

## API documentada

**Link direto para `/api-docs`** no header. Outros MapBiomas não têm isso tão explícito. Sugere que a Recuperação é **API-first** — ideal para integração.

## Link "Destaques"

PDF Factsheet: https://brasil.mapbiomas.org/wp-content/uploads/sites/4/2025/10/Factsheet-Monitor_de_Recuperacao_22.10_v3.pdf — documentação resumida em 1 página.

## Insights para AgroJus

### Padrões a copiar

1. **Painel de filtros com múltiplos identificadores lado a lado** — embargo + CAR num único panel. Para AgroJus, permitir busca simultânea por:
   - CAR
   - CNPJ
   - Número CNJ
   - Auto IBAMA
   - Código de alerta MapBiomas
   - Número SIGEF
   
   Todos numa mesma tela, cada um num campo com placeholder mostrando formato esperado.

2. **Switch on/off prominente** — toggle de destaque para separar modos diferentes de visualização (aqui: regeneração vs restauração). Para AgroJus: "Mostrar apenas imóveis com alerta ativo", "Incluir fazendas arquivadas".

3. **API documentada no header** — deixar explícito que existe API pública. No AgroJus isso será um diferencial comercial (API enterprise como camada de monetização).

4. **Factsheet PDF linkado** — documentação curta em 1 página explicando a plataforma. Para AgroJus: "Sobre o AgroJus" no header com download do factsheet comercial.

5. **Range slider de anos 2000-2025** — similar ao alerta mas mais compacto (só anos, não meses).

### UX de combos encadeados

Os 5 comboboxes "Escolha uma opção" provavelmente se encadeiam (escolher UF restringe municípios, etc.). AgroJus deve ter o mesmo para filtros geográficos.

## Gaps vs AgroJus

| Feature Recuperação | AgroJus hoje | Prioridade |
|---|---|---|
| Múltiplos identificadores em painel | ⚠️ só OmniSearch único | ALTA |
| Switch on/off prominente | ❌ | MÉDIA |
| API docs no header | ⚠️ temos /docs Swagger mas não linkado | BAIXA |
| Factsheet PDF 1 página | ❌ | BAIXA |
| Combos encadeados | ❌ | ALTA |
