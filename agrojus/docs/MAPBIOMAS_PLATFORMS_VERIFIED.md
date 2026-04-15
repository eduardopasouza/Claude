# MapBiomas Plataformas — Dados Verificados Visualmente 

**Data:** 12 abril 2026 — Navegação direta nas plataformas

---

## 1. MONITOR DO CRÉDITO RURAL

**URL:** https://plataforma.creditorural.mapbiomas.org

### Estatísticas Gerais (verificadas)
| Métrica | Valor |
|---------|-------|
| Total de operações | **4.215.169** |
| Área financiada | **129,97 Mi ha** |
| Valor total financiado | **R$ 505,32 Bi** |

### Gráficos disponíveis
- Quantidade de operações por ano (2019-2025) — com % de financiamentos com desmatamento
- Cronologia dos financiamentos por ano — separando:
  - 🟢 Gleba financiada ANTES da confirmação do alerta
  - 🟦 Gleba financiada ENTRE as datas de confirmação e publicação
  - 🟥 Gleba financiada APÓS data de publicação do alerta de desmatamento

### Filtros (sidebar esquerda)
| Filtro | Opções |
|--------|--------|
| Recorte territorial | Todos / por estado / por município |
| Cruzamentos | Com alertas de desmatamento |
| Alerta durante período de vigência | Sim / Não |
| Cronologia | Antes / Entre / Após alerta |
| **Gleba contida no CAR declarado** | **Sim / Não** |
| Período de emissão | Data início até data fim |
| Instituição financeira | Dropdown (todos os bancos) |
| Fonte de recursos | Equalizadas/BNDES/FNO/FCO/FNE... |
| Finalidade | Custeio / Investimento / Comercialização |
| Atividade | Por tipo de atividade agro |

### Camadas de mapa disponíveis
| # | Camada | Fonte | Atualização |
|---|--------|-------|-------------|
| 1 | Alertas de Desmatamento | MapBiomas | 10/2024 |
| 2 | **CAR** | **SICAR** | **01/2024** |
| 3 | Biomas | IBGE | 10/2019 |
| 4 | Estados | IBGE | 07/2022 |
| 5 | Municípios | IBGE | 07/2022 |
| 6 | Unidades de Conservação | ICMBio/MMA | 02/2024 |
| 7 | Terras Indígenas | FUNAI | 03/2024 |
| 8 | Assentamentos | INCRA | 03/2022 |
| 9 | Quilombos | INCRA | 01/2022 |
| 10 | **Áreas Embargadas** | **ICV** | **06/2025** |
| 11 | Florestas Públicas Tipo B | SFB | 2024 |

### Downloads
- Vetoriais organizados: [Google Drive ZIP](https://drive.google.com/file/d/1tO0-qYUAQKRHJWrbYxO7VsUmwHLEn-TS/view)
- Sicor atualizado: 16/10/2024
- CAR atualizado: 01/2024

---

## 2. MAPBIOMAS ALERTA (Desmatamento)

**URL:** https://plataforma.alerta.mapbiomas.org

### Estatísticas Gerais (verificadas)
| Métrica | Valor |
|---------|-------|
| Total de Alertas | **515.823 unidades** |
| Área Desmatada | **10.910.960,4 hectares** |
| Média Diária | **4.267,1 hectares/dia** |

### Funcionalidades
- **Busca por:** Código do alerta OU **Código do Imóvel Rural (CAR)**
- **Modo:** Simples ou Detalhado
- **Período:** 01/2019 a 12/2025
- **Tamanho do alerta:** 0 a 20.835 ha (slider)
- **Vetores:** Todos / SelectPeça
- **Fontes:** DETER, SAD, GLAD, ISA, IMAZON, Universidade de Maryland

### Cruzamentos disponíveis
| Filtro | Opções |
|--------|--------|
| Tipo de território | Todos / por tipo |
| Cruzamentos | Todos / específicos |
| Autorização | Todos / Com / Sem autorização |
| **Imóveis com embargo** | **Todos / Sim / Não** |

### Menu superior
- **Alertas e Laudos** — laudos técnicos validados
- **Monitor da Fiscalização** — acompanhamento de ações do IBAMA
- **Downloads** — SHP, CSV em massa
- **Plugins** — extensões
- **API** — documentação da API GraphQL pública

### Gráficos
- Evolução da área de desmatamento (anual)
- Evolução mensal da área de desmatamento (por mês, por ano)
- Evolução do total de alertas
- Maior desmatamento / Maior velocidade

---

## 3. DADOS QUE O MAPBIOMAS CRUZA (e que o AgroJus deve replicar)

O MapBiomas **já faz** esses cruzamentos que são o core do nosso produto:

```
FINANCIAMENTO (Sicor/BCB)
    ↕ cruza com
ALERTAS DE DESMATAMENTO (MapBiomas Alerta)
    ↕ cruza com
CAR (SICAR)
    ↕ cruza com
EMBARGOS (ICV/IBAMA)
    ↕ cruza com
TERRAS INDÍGENAS (FUNAI) + UCs (ICMBio) + ASSENTAMENTOS (INCRA) + QUILOMBOS
```

### O que o AgroJus adiciona que o MapBiomas NÃO faz:
1. **Processos judiciais** (DataJud/CNJ) — nenhuma plataforma ambiental tem isso
2. **Dossiê completo por CPF/CNPJ** — pessoa física/jurídica que tem embargo E processo judicial E crédito rural
3. **Compliance MCR 2.9 automatizado** — laudo pronto para banco
4. **Compliance EUDR** — laudo para exportador europeu
5. **Análise de risco ESG integrada** — score único que combina tudo
6. **Inteligência de mercado** — cotações + produção + crédito numa única tela

---

*Verificado via navegação direta em 12/04/2026*
