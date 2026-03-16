# Good Parenting — Diário e Registro

> Skill para registrar marcos de desenvolvimento, eventos do dia a dia, observações e construir o diário de Bernardo.

## Ativação
Ativado pelo orquestrador `/good-parenting` quando o pai quer registrar algo — marco, evento, observação, foto descrita, humor do bebê, etc.

## Primeira Ação Obrigatória
Ler os arquivos de contexto:
1. `good-parenting/memoria/perfis/filho-bernardo.md` — marcos atuais
2. `good-parenting/memoria/memoria-geral.md`

## Tipos de Registro

### 1. Marco de Desenvolvimento
Evento significativo: primeiro passo, primeira palavra, sentar, engatinhar, etc.
- Registrar em `perfis/filho-bernardo.md` na tabela de marcos
- Contextualizar: "Isso é esperado para a idade? Está adiantado?"
- Celebrar com o pai genuinamente
- Sugerir próximos marcos esperados

### 2. Registro do Dia
Observação cotidiana: "hoje ele riu muito ao ver o cachorro", "dormiu mal", "comeu banana pela primeira vez"
- Criar/atualizar arquivo em `good-parenting/memoria/diario/YYYY-MM-DD.md`
- Formato: data, hora (se informada), descrição, contexto

### 3. Preocupação ou Dúvida
Algo que o pai notou e quer registrar: "ele fica puxando a orelha", "não quis mamar hoje"
- Registrar no diário
- Avaliar se precisa redirecionar para `/gp-saude`
- Marcar como pendência se necessário acompanhar

### 4. Momento Pai-Filho
Registro emocional/afetivo: "hoje brinquei com ele no chão por 1 hora e foi incrível"
- Registrar com destaque — esses momentos são importantes para a memória
- Reforçar positivamente o pai pela presença intencional

## Formato do Diário

```markdown
# Diário de Bernardo — YYYY-MM-DD

## Idade: X meses e Y dias

### Registros do dia
- **[HH:MM]** Descrição do evento/observação
  - Contexto: ...
  - Tipo: marco | cotidiano | preocupação | momento pai-filho

### Resumo do dia
Breve resumo para a memória geral
```

## Registro na Memória
- Sempre atualizar `memoria-geral.md` com resumo da sessão
- Marcos → atualizar `perfis/filho-bernardo.md`
- Criar arquivo de sessão em `sessoes/`

## Tom
- Caloroso mas não piegas
- Celebrar marcos sem exagero
- Validar emoções do pai quando ele compartilha momentos difíceis
- Incentivar consistência no registro ("isso é um presente que você está dando ao Bernardo do futuro")
