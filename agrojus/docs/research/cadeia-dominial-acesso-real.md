# Cadeia Dominial e Matrículas — Realidade do Acesso no Brasil

**Nota:** este documento corrige uma classificação errada anterior.
Matrícula e cadeia dominial **não são camadas geoespaciais de acesso público**
— precisam ser tratadas como análise documental paga/on-demand, não como
polígonos coloridos no mapa.

## 1. Como matrícula realmente funciona no Brasil

A **matrícula imobiliária** é mantida em um dos ~3.400 **Cartórios de Registro de Imóveis (CRIs)** espalhados pelo país. Cada CRI tem sua própria base, escritura própria, e (em muitos casos) sistema informatizado próprio. **Não existe base federal unificada aberta.**

O **ONR (Operador Nacional de Registros de Imóveis)** foi criado pela Lei 11.977/2009 + Provimento CNJ 47/2015 + Provimento 65/2017 para ser um **hub nacional**. Mas:

- **Não é acesso gratuito.** Cobrança por consulta via Central Nacional de Registros (R$ 15-80 por consulta dependendo do CRI).
- **Retorno é PDF ou texto de matrícula**, não geometria.
- **API existe mas restrita** a cartórios e conveniados (bancos grandes, Poder Judiciário). Terceiros precisam passar por intermediários como **InfoSimples** (R$ 0,10-0,50/consulta) ou **CartoReg**, **Registralize**, **CRIDIG**.

**Cadeia dominial** = sequência de transmissões de um imóvel (comprador 1 → comprador 2 → ... → dono atual). Só é reconstruída manualmente lendo matrícula por matrícula. Isso demanda:
1. Uma matrícula inicial por imóvel
2. Acompanhar as averbações (cada averbação pode apontar para outra matrícula)
3. Ir para trás até origem do imóvel

Custa caro e é trabalho humano especializado. Um advogado leva 2-8 horas por imóvel.

## 2. O que AgroJus pode e não pode fazer

### ❌ Não pode:
- Mostrar "camada de matrículas" no mapa
- Baixar bulk de matrículas de um estado
- Integrar gratuitamente com o ONR

### ✅ Pode:
1. **Consulta on-demand paga (InfoSimples)** — na ficha `/imoveis/[car]`, aba "Cadeia Dominial" tem um botão "Consultar agora (R$ 0,50)" que aciona o InfoSimples pelo CPF/CNPJ cadastrado → sistema retorna PDF da matrícula e cobra do saldo do usuário.
2. **Upload de PDF de matrícula + OCR + NLP** — usuário traz o documento próprio (já obtido pelo cartório), AgroJus extrai dados estruturados (proprietário atual, histórico, gravames, georreferenciamento se houver) e **monta a cadeia dominial estruturada**.
3. **Colar texto livre da matrícula** — para quem tem teor digital, cola no sistema que parseia com LLM.
4. **Cruzamento com CAR/SIGEF/ICMBio/DataJud** — uma vez estruturada, a matrícula vira chave para todas as outras consultas do AgroJus.
5. **Armazenamento seguro** — AgroJus guarda o histórico de matrículas já processadas para aquele imóvel. Se alguém refaz a consulta depois, usa o cache local (LGPD-compliant, com consentimento do titular).

### Tratamento no produto

A camada **"Cartório (ONR)"** foi removida do catálogo de camadas de mapa (commit atual). O tratamento cartorial fica em:

**Tela `/imoveis/[car]` — aba "Cadeia Dominial":**
```
┌──────────────────────────────────────────────┐
│  Cadeia Dominial                              │
│  ────────────────                            │
│  [🔒 Nenhuma matrícula cadastrada]           │
│                                                │
│  Opções para começar:                         │
│  ┌────────────────────────────────────────┐  │
│  │ 📄 Upload de PDF da matrícula          │  │
│  │    OCR + parse automático              │  │
│  │    Grátis                               │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ ✏️ Colar teor da matrícula (texto)     │  │
│  │    Parse LLM                            │  │
│  │    Grátis                               │  │
│  └────────────────────────────────────────┘  │
│  ┌────────────────────────────────────────┐  │
│  │ 💳 Consultar via InfoSimples           │  │
│  │    R$ 0,50 por consulta                │  │
│  │    Retorno: PDF + parse automático     │  │
│  └────────────────────────────────────────┘  │
└──────────────────────────────────────────────┘
```

Depois que o usuário faz qualquer uma das 3 opções, a cadeia dominial é estruturada e o AgroJus mostra:
- Proprietário atual
- Histórico de aquisições (timeline)
- Averbações (gravames, hipotecas, servidões)
- Cruzamento com partes de processos judiciais (via DataJud)
- Cruzamento com CPF/CNPJ em embargos IBAMA/ICMBio
- Cruzamento com CAR cadastrado

**Isso é análise documental profunda — não camada de mapa.**

## 3. Fontes alternativas (cartoriais secundárias)

Para **alguns dados** é possível obter gratuitamente em fontes paralelas:

| Dado | Fonte gratuita | Observação |
|---|---|---|
| Proprietário atual (público PJ) | Receita Federal CNPJ (BrasilAPI) | Só CNPJ, não o imóvel |
| CCIR/Cadastro Rural INCRA | SNCR (login gov.br) | Indica proprietário declarado |
| SIGEF (parcelas certificadas) | INCRA público | Alguns imóveis têm SIGEF vinculado, traz titular |
| Protestos/Tabelionatos de Protesto | CENPROT | Não é matrícula, mas indica gravame |
| Imóveis da União | SPU | Terras federais identificadas |
| Indisponibilidade de Bens | CNIB (CNJ) | Lista de imóveis bloqueados judicialmente |

Nenhum desses é matrícula completa. Servem como **triangulação secundária** para confirmar quem é dono aproximadamente — útil quando o cliente ainda não trouxe a matrícula oficial.

## 4. Custo estimado de integração InfoSimples

- Cadastro: gratuito
- **Matrícula RGI digital**: ~R$ 0,10-0,50/consulta
- Repasse ao cliente final: a decidir (AgroJus pode absorver no plano Enterprise ou cobrar R$ 1-2)
- SLA: 95% dos CRIs respondem em segundos; alguns CRIs menores demoram horas

**Recomendação comercial:**
- Plano Free: 0 consultas/mês (exige upgrade)
- Plano Pro: 10 consultas/mês inclusas + R$ 1,50 excedente
- Plano Enterprise: ilimitado

## 5. Correção no catálogo de camadas

O tema **"Cartório (ONR)"** foi removido de `layers-catalog.ts`. As 3 entradas (matrículas, cadeia dominial, averbações) estavam classificadas como stubs a serem ativadas, o que era enganoso.

A nota ficou no arquivo apontando para este documento e indicando onde o tratamento cartorial realmente acontece (ficha do imóvel com opções paga/upload/texto).

## 6. Conclusão

AgroJus **pode** oferecer análise de cadeia dominial — mas como **análise documental paga/assistida**, não como camada de mapa pública. O pipeline é:

```
Input (PDF upload | texto colado | consulta paga)
   ↓
OCR + NLP parse
   ↓
Estrutura: {proprietário, histórico, averbações, gravames}
   ↓
Cruzamento: CAR + CNPJ + DataJud + IBAMA + CNIB
   ↓
Exibe na ficha do imóvel (aba Cadeia Dominial)
   ↓
Export: PDF laudo "Análise de Cadeia Dominial"
```

Esse pipeline é **mais valioso** que uma camada de mapa, porque entrega análise contextual + cruzamentos. É o que advogado/comprador realmente precisa antes de fechar negócio.
