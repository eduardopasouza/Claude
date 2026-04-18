# Guia dados.gov.br para AgroJus — O que baixar

**Token CKAN já configurado** em `.env` como `DADOS_GOV_TOKEN`.
API base: `https://dados.gov.br/api/publico/`

Este guia lista **os 32 datasets prioritários** do dados.gov.br para o AgroJus, em ordem decrescente de valor.

## Como acessar via API CKAN

```python
import httpx
import os

TOKEN = os.environ["DADOS_GOV_TOKEN"]
BASE = "https://dados.gov.br/api/publico"
HEADERS = {"Authorization": f"Bearer {TOKEN}"}

# Listar recursos de um dataset
r = httpx.get(f"{BASE}/3/action/package_show?id={dataset_id}", headers=HEADERS)

# Baixar um recurso específico
resource_url = r.json()["result"]["resources"][0]["url"]
data = httpx.get(resource_url, headers=HEADERS).content
```

---

## Datasets prioritários (TOP 32)

### 🔴 PRIORIDADE 1 — Dados que populam o AgroJus imediatamente (12 datasets)

#### Crédito Rural
1. **`matriz-de-dados-do-credito-rural`** (BCB)
   - CSV mensal: cada linha = operação SICOR
   - Colunas: CPF/CNPJ cifrado, valor, finalidade, município, cultura, banco
   - Cobertura: 2013+
   - **Uso AgroJus:** complementa nossa `mapbiomas_credito_rural` — permite agregar por município/UF/programa

2. **`dados-sicor-operacoes-de-credito-rural`** (BCB)
   - Mesma base que acima mas com segmentação PRONAF/PRONAMP/FCO/FNE/FNO
   - **Uso:** filtro de linhas de crédito por elegibilidade do imóvel

#### IBAMA (ambiental)
3. **`ibama-quantidade-de-autos-de-infracao`**
   - CSV histórico de todos os autos
   - Colunas: auto nº, data, CPF/CNPJ, UF, municipio, artigo, valor, situação, coordenadas
   - **Uso:** camada `autos_ibama_pontos` (hoje stub) — PRONTA PARA ATIVAR

4. **`ibama-termo-de-embargo`**
   - CSV com todos embargos IBAMA (além dos ICMBio que já temos)
   - **Uso:** extende `environmental_alerts` com embargos IBAMA pontuais

5. **`ibama-cadastro-tecnico-federal-de-atividades-potencialmente-poluidoras-e-ou-utilizadoras-de-recursos-ambientais`**
   - CTF/APP — lista de atividades poluidoras registradas
   - **Uso:** camada `ctf_ibama` (stub) — PRONTA PARA ATIVAR

#### MTE
6. **`relacao-anual-de-informacoes-sociais-rais`**
   - Base RAIS — vínculos trabalhistas
   - **Uso:** cruzamento com CNPJ na análise de imóvel (emprego formal rural)

7. **`cadastro-de-empregadores-que-tenham-submetido-trabalhadores-a-condicoes-analogas-a-de-escravo`**
   - Lista Suja MTE (já temos via CSV parsing, mas aqui é oficial)
   - **Uso:** atualização mensal automática

#### Transparência / CGU
8. **`beneficiarios-do-programa-garantia-safra`**
   - CSV mensal: CPF + municipio + valor pago
   - **Uso:** camada `garantia_safra` (stub) — PRONTA PARA ATIVAR

9. **`cadastro-nacional-de-empresas-inidoneas-e-suspensas-ceis`**
   - CEIS — idêntico ao que obtemos via Portal Transparência
   - **Uso:** backup + validação cruzada

#### INCRA
10. **`sistema-nacional-de-cadastro-rural-sncr`**
    - SNCR — proprietários rurais declarados
    - **Uso:** cruzamento com CAR/CPF

11. **`acervo-fundiario-sigef`**
    - SIGEF Brasil por UF (shapefile + metadados)
    - **Uso:** complementa nossa `sigef_parcelas` (já parcial)

#### MAPA
12. **`estabelecimentos-sob-inspecao-federal-sif`**
    - Frigoríficos SIF habilitados
    - **Uso:** já temos `geo_frigorificos` — esse dataset é a fonte oficial para atualização

---

### 🟡 PRIORIDADE 2 — Enriquece análise agronômica (10 datasets)

13. **`zoneamento-agricola-de-risco-climatico-zarc`** (MAPA)
    - Planilhas por cultura/UF/município com janelas de plantio
    - **Uso:** complementa Embrapa AgroAPI ZARC (oficial em XLS)

14. **`agrofit`** (MAPA)
    - Agrotóxicos registrados — base oficial
    - **Uso:** backup do Embrapa AgroAPI AGROFIT

15. **`producao-agricola-municipal-pam`** (IBGE)
    - PAM em CSV bulk — alternativa ao SIDRA REST
    - **Uso:** população inicial do banco; depois SIDRA para atualizações

16. **`pesquisa-da-pecuaria-municipal-ppm`** (IBGE)
    - PPM em CSV bulk — idem

17. **`censo-agropecuario-2017`** (IBGE)
    - Censo completo por município
    - **Uso:** dimensionamento de estabelecimentos rurais, áreas, trabalhadores

18. **`levantamento-sistematico-da-producao-agricola-lspa`** (IBGE)
    - Estimativas mensais de safra (antes do PAM anual)
    - **Uso:** pontos quentes de produção em tempo quase-real

19. **`estatisticas-de-comercio-exterior-agronegocio`** (MAPA AgroStat)
    - Exportações/importações por produto+país
    - **Uso:** contexto de mercado para commodities

20. **`sigmine-processos-minerarios`** (ANM)
    - Shapefile dos processos minerários
    - **Uso:** camada `sigmine_anm` (stub) — PRONTA PARA ATIVAR

21. **`outorgas-de-direito-de-uso-de-recursos-hidricos`** (ANA)
    - Outorgas + coordenadas + finalidade + vazão
    - **Uso:** camada `ana_outorgas` (stub) — PRONTA PARA ATIVAR

22. **`base-hidrografica-ottocodificada`** (ANA BHO)
    - Shapefile de rios ottocodificados 12 níveis
    - **Uso:** camada `ana_bho` (stub) — PRONTA PARA ATIVAR

---

### 🟢 PRIORIDADE 3 — Valor contextual (10 datasets)

23. **`snv-rodovias-federais`** (DNIT)
    - Shapefile atualizado de rodovias federais
    - **Uso:** atualização da nossa `geo_rodovias_federais`

24. **`malha-ferroviaria`** (ANTT)
    - Shapefile ferrovias — similar atualização

25. **`estabelecimentos-portuarios`** (ANTAQ)
    - Portos + terminais
    - **Uso:** atualização `geo_portos` + ativação de terminais intermodais

26. **`malha-municipal-ibge`** (IBGE)
    - Shapefiles dos 5.570 municípios
    - **Uso:** base para choropleths

27. **`regic-regioes-de-influencia-das-cidades`** (IBGE)
    - Hierarquia urbana 2018
    - **Uso:** camada `ibge_regic_2018` (stub) — PRONTA PARA ATIVAR

28. **`areas-quilombolas`** (INCRA/Palmares)
    - Territórios quilombolas
    - **Uso:** camada `quilombolas_incra` (stub) — PRONTA PARA ATIVAR

29. **`assentamentos-incra`** (INCRA)
    - Projetos de assentamento
    - **Uso:** camada `assentamentos_incra` (stub) — PRONTA PARA ATIVAR

30. **`terras-indigenas-funai`** (FUNAI)
    - Shapefile oficial (temos via WFS, aqui é backup estável)

31. **`empreendimentos-de-geracao-de-energia-eletrica-big`** (ANEEL)
    - Usinas cadastradas (hidro, térmica, solar, eólica)
    - **Uso:** camada `aneel_usinas` (stub) — PRONTA PARA ATIVAR

32. **`linhas-de-transmissao`** (ONS/ANEEL)
    - Shapefile de LTs
    - **Uso:** camada `aneel_linhas_transmissao` (stub) — PRONTA PARA ATIVAR

---

## Próximos passos concretos

### Sprint Dados Gov — 1 (3 dias)
Ativar as 10 camadas marcadas como **"PRONTA PARA ATIVAR"**:
1. IBAMA autos de infração (pontos)
2. IBAMA termo de embargo (pontos + polígonos)
3. IBAMA CTF/APP
4. Garantia-Safra
5. SIGMINE ANM
6. ANA Outorgas
7. ANA BHO
8. Assentamentos INCRA
9. Quilombolas
10. ANEEL usinas + LTs

Cada uma: coletor Python ~100 linhas + ETL para PostGIS + entrada no `LAYER_REGISTRY` backend.

### Sprint Dados Gov — 2 (2 dias)
- Automatizar download incremental mensal via cron
- Versionamento das bases (tracking de mudanças)
- Dashboard admin para status de cada coleta

---

## Como descobrir novos datasets

O dados.gov.br tem **29 temas** (você seguiu vários). Para cada tema, liste datasets:

```bash
curl -H "Authorization: Bearer $DADOS_GOV_TOKEN" \
  "https://dados.gov.br/api/publico/3/action/package_search?fq=groups:meio-ambiente&rows=50"
```

Temas relevantes para AgroJus:
- `agricultura-extrativismo-e-pesca` (48 datasets)
- `meio-ambiente` (95)
- `economia-e-financas` (157 — inclui BCB SICOR)
- `geografia` (42 — IBGE malhas)
- `governo-e-politica` (85 — CGU Transparência)
- `justica-e-legislacao` (35 — DataJud, CNJ)
- `trabalho` (27 — RAIS, Lista Suja MTE)

---

## Conclusão

**O que você seguiu = notificações de atualização.** Os dados baixam via:
1. **API CKAN** (com o token já configurado) — endpoint `package_show` + download do recurso
2. **Download direto** do link de cada recurso (CSV/SHP/JSON)

Os **32 datasets priorizados acima** cobrem tudo que o AgroJus precisa do dados.gov.br. Dos 32, **10 são de ativação imediata** (preenchem camadas stub existentes), **12 são alta prioridade** de integração, e **10 agregam contexto**.
