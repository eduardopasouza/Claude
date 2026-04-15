# Inteligência Competitiva e Estratégia de Produto — AgroJus

Pesquisa conduzida em abril de 2026.

---

## O MOMENTO É AGORA: MCR 2.9

As resoluções CMN 5.267/2025 e 5.268/2025, com vigência a partir de
01/04/2026, criaram uma ruptura no mercado de crédito rural:

**O que os bancos agora são OBRIGADOS a verificar antes de liberar crédito:**
- CAR ativo (não cancelado, não suspenso)
- Ausência de supressão de vegetação nativa após 31/07/2019 (via PRODES)
- Georreferenciamento e conformidade territorial
- Imóveis acima de 4 módulos fiscais: obrigatório desde 01/04/2026
- Imóveis menores: obrigatório a partir de 04/01/2027

**BCB já bloqueou mais de R$6 bilhões em operações com irregularidades.**

**IMPLICAÇÃO**: Todo banco e cooperativa do Brasil precisa automatizar
essa verificação. AgroJus pode entregar isso como serviço.

---

## MAPA COMPETITIVO

### Agrotools (agrotools.com.br)
- **Clientes**: McDonald's, Rabobank, Carrefour, Itaú BBA, JBS, Cargill, Sicredi
- **Preço**: Enterprise (R$5K-50K+/mês)
- **Gap**: Inacessível para advogado individual ou banco regional
- **Nosso espaço**: O mercado do meio que a Agrotools não atende

### Registro Rural (registrorural.com.br)
- **Preço**: Gratuito / R$149,90 / R$850/mês
- **Modelo**: Créditos pré-pagos por consulta
- **Gap**: Dados brutos sem análise. Sem score de risco. Sem jurídico
- **Nosso diferencial**: Transformar dados em RISCO e AÇÃO

### Chãozão (chaozao.com.br)
- **Posição**: Líder em anúncios de terras (R$500 bi anunciados)
- **Gap**: Sem due diligence integrada, sem dados ambientais/jurídicos
- **Nosso espaço**: O comprador usa Chãozão para achar, AgroJus para investigar

### AdvLabs (advlabs.com.br)
- **Foco**: Defesa ambiental (IBAMA/ICMBio). IA para teses e petições
- **Modelo**: Assinatura anual + créditos avulsos
- **Gap**: Só ambiental. Sem fundiário, sem trabalhista, sem crédito rural
- **Nosso espaço**: AdvLabs ampliado (ambiental + fundiário + trabalhista + financeiro)

### Docket (docket.com.br)
- **Foco**: OCR de certidões com IA (50+ tipos). Parceira da Agrotools
- **Gap**: Genérico (não especializado em rural). Sem CAR, SIGEF, SNCR
- **Nosso espaço**: OCR especializado para documentos RURAIS

### Traive / Agrolend (crédito rural com IA)
- **Foco**: Motor de risco para fintechs e bancos. Traive: USD 20M série B
- **Gap**: Dados fundiários são insumo, não produto deles
- **Nosso espaço**: Ser o FORNECEDOR de dados que essas fintechs precisam via API

### App "Meu Imóvel Rural" (governo, lançado jul/2025)
- **O que faz**: Unifica SNCR + SIGEF + SICAR para o produtor baixar docs
- **Gap**: Entrega PDFs, não inteligência. Sem análise, sem risco, sem alerta
- **Nosso espaço**: O governo digitalizou o acesso. Nós digitalizamos a ANÁLISE

---

## FEATURES QUE NINGUÉM TEM (nosso fosso competitivo)

### 1. Score MCR 2.9 em Tempo Real
Checklist automatizado para bancos:
- CAR ativo? → SICAR
- PRODES limpo após 31/07/2019? → TerraBrasilis DETER/PRODES
- Georreferenciado no SIGEF? → SIGEF
- Embargo IBAMA? → Dados abertos
- Resultado: APTO / INAPTO / PENDENTE (com justificativa auditável)

### 2. Detector de Inconsistências CAR × SIGEF × Matrícula
- Área no CAR ≠ área no SIGEF ≠ área na matrícula = ALERTA
- Sobreposição com outros imóveis, TI, UC
- 139,6 milhões de hectares com sobreposição no CAR (dado real)
- Nenhum concorrente faz isso automaticamente

### 3. OCR Especializado para Documentos Rurais
Treinar modelos para ler:
- Matrícula de imóvel rural (área, confrontantes, ônus, averbações)
- CCIR (módulos fiscais, fração mínima, código do imóvel)
- CAR Demonstrativo (APP, RL, uso consolidado, passivo)
- Laudo SIGEF (vértices, memorial descritivo)

### 4. Cadeia Dominial Digital
Reconstituir histórico de titularidade:
- Quem eram os donos anteriores
- Quando venderam, por quanto
- Se há litígios históricos
- Alimentado por OCR de matrículas + SNCR histórico

### 5. Dashboard de Carteira para Bancos
Banco cadastra sua carteira de financiamentos → recebe alertas quando
qualquer imóvel muda: novo embargo, desmatamento, CAR cancelado,
novo processo judicial.

### 6. Valuation Rural por IA
Modelo preditivo baseado em:
- Produtividade por município (IBGE PAM)
- Tipo de solo (EMBRAPA)
- Bioma, distância de infraestrutura
- Transações históricas
- Output: valor estimado/ha com intervalo de confiança

### 7. Assistente Jurídico AgroJus (LLM especializado)
Fine-tuned em legislação agrária, ambiental, decisões STJ/STF,
regulamentações BACEN/CMN, INs IBAMA, instruções INCRA.

---

## MODELO DE MONETIZAÇÃO REFINADO

### Tier 1 — Freemium (aquisição de tráfego)
- Semáforo básico do imóvel (CAR ativo? SIGEF certificado?)
- 3 relatórios/mês grátis
- Notícias e cotações
- **Objetivo**: viralização e captação

### Tier 2 — Individual (R$149-299/mês)
- Advogados, produtores, corretores, consultores
- Relatórios ilimitados
- OCR de documentos (20/mês)
- Monitor de legislação
- Painel de saúde (3 imóveis)

### Tier 3 — Profissional (R$699-1.490/mês)
- Escritórios (5 usuários), cooperativas
- OCR ilimitado
- Detector de inconsistências
- Cadeia dominial
- Valuation automatizado
- API (500 req/mês)
- Monitoramento (50 imóveis)

### Tier 4 — Enterprise (R$5.000-50.000/mês)
- Bancos, seguradoras, tradings
- API ilimitada
- Score MCR 2.9
- Dashboard de carteira
- White-label
- SLA dedicado

### Pay-per-report (avulso)
- Due Diligence Completa: R$89-199/imóvel
- Laudo de Valuation: R$149-299/imóvel
- Cadeia dominial: R$49-99/matrícula

### API B2B (maior potencial de receita)
- R$2-15 por imóvel verificado
- Centenas de milhares de operações de crédito rural/ano no Brasil

---

## DESIGN DE EXPERIÊNCIA

### O imóvel como entidade central
Tudo gira em torno do imóvel (como uma ação na bolsa).
O usuário "segue" imóveis. Recebe alertas quando algo muda.

### Semáforo de saúde
Cada imóvel: 🟢 Regular | 🟡 Atenção | 🔴 Crítico
Um clique → resumo. Dois cliques → dossiê completo.

### Mapa como navegação principal
O mapa É o produto, não um acessório.
Usuário localiza, não preenche formulário.

### Alertas proativos = reengajamento
O app avisa, o usuário não precisa lembrar de entrar.
Cada alerta = razão para abrir o site.

### Exportação multi-formato
PDF (relatório) + Shapefile (perito) + KML (Google Earth) +
Excel (analista) + Link compartilhável (cliente)
