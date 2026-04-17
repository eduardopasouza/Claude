# MapBiomas Monitor da Mineração

- **URL:** https://plataforma.monitormineracao.mapbiomas.org/
- **Categoria:** mapbiomas (referência de busca por processo + integração multi-fonte)
- **Data auditoria:** 2026-04-17
- **Acesso:** público; aceite de termos via dialog inicial

## Propósito declarado

Mapeamento das áreas de mineração industrial + garimpo (legal/ilegal) no Brasil, integrando:
- **MapBiomas (Coleção 10)** — detecção por satélite
- **SIGMINE** (ANM) — processos minerários ativos
- **Cadastro Mineiro** (dados.gov.br) — titularidade
- **Sistema de Arrecadação ANM** — CFEM

## Layout e navegação

Similar às outras plataformas MapBiomas mas com **dialog de fontes** no primeiro acesso (mostra as 4 fontes integradas com checkbox "Concordo").

**Filtros observados (muito ricos):**
- Bioma (autocomplete)
- UF
- Município
- Substância mineral (provavelmente)
- Titular / CPF / CNPJ
- Status do processo
- **Spinbutton Year** — início e fim (ano numérico)
- **Choose date** — calendário
- **Busca textual**: "Ex: 851145/2021 ou Indústrias..." — permite busca por nº do processo OU por nome do titular
- Botões Resetar / Buscar

**Outras ferramentas:**
- **Lat/Lon inputs** — ir para coordenada específica (centralizar mapa)
- **Lista** (botão) — painel lateral com lista de resultados
- Toolbar com ~15 botões (zoom, régua, opacidade, etc.)
- Dialog "Descartar" para fechar filtros

## Interações

- Dialog inicial obriga aceite antes de usar (termos)
- Filtros compostos — combinação AND entre critérios
- Resultados podem ser listados em painel direito

## API e export

Via seção "Downloads" (padrão MapBiomas).

## Autenticação

Nenhuma para consulta pública. Aceite de termos obrigatório.

## Insights para AgroJus

### Padrões a copiar

1. **Dialog de fontes inicial** — transparência. Mostra ao usuário **quais bases estão sendo cruzadas** com links clicáveis. Para AgroJus: no inspector ou num banner "Fontes consultadas: SICAR, DataJud, DJEN, ANA Outorgas, IBAMA dados abertos..." com checkbox de concordância LGPD no primeiro uso.

2. **Busca textual flexível** — "Ex: 851145/2021 ou Indústrias..." aceita:
   - número do processo
   - nome de titular
   - autocomplete cross-field
   Para AgroJus: unificar OmniSearch (já temos smart search com 12 regex) para operar também em camada ativa — "digite CNPJ e destaca no mapa apenas features associadas a ele".

3. **Input direto de Lat/Lon** — ir para coordenada manualmente. AgroJus ❌.

4. **Spinbutton de ano** (duas entradas: início e fim) — melhor que slider dual para ranges amplos (1985-2024). AgroJus ❌.

5. **Integração multi-fonte explícita** — o site deixa claro que combina MapBiomas + SIGMINE + Cadastro Mineiro + Arrecadação. **AgroJus pode fazer isso mostrando badges**: "Esta feature: MapBiomas Alertas + CAR + DataJud (3 processos vinculados)".

## Gaps vs AgroJus

| Feature Mineração | AgroJus hoje | Prioridade |
|---|---|---|
| Dialog de fontes com termos | ❌ | MÉDIA |
| Busca textual cross-field | ⚠️ smart-search só roteia por tipo | MÉDIA |
| Input lat/lon direto | ❌ | MÉDIA |
| Spinbutton de ano duplo | ❌ | ALTA |
| Badges de fontes por feature | ❌ | BAIXA |
