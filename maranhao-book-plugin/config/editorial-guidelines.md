# Diretrizes Editoriais — Livro sobre o Maranhão

## 1. Princípios Fundamentais

### Tom e Voz
- **Narrativo-ensaístico**: combinar fluidez narrativa com rigor informativo
- **Acessível sem ser superficial**: o leitor comum deve compreender, o especialista deve encontrar substância
- **Afetivo mas não ufanista**: celebrar sem idealizar, apontar problemas sem demonizar
- **Em primeira pessoa quando experiencial, em terceira quando analítico**

### Perspectiva
- Priorizar vozes maranhenses: escritores, pesquisadores, artistas, moradores
- Dar protagonismo a comunidades tradicionais (quilombolas, indígenas, quebradeiras de coco)
- Evitar o olhar colonizador ou exotizante
- Contextualizar o Maranhão dentro do Brasil e do mundo, não como periferia

### Linguagem
- Português brasileiro padrão com naturalidade
- Incorporar termos regionais com explicação contextual (sem necessidade de aspas excessivas)
- Evitar jargão acadêmico desnecessário
- Usar notas de rodapé para aprofundamentos, não para informações essenciais

## 2. Padrões de Redação

### Estrutura de Capítulo
```
- Epígrafe (citação relevante de autor maranhense ou sobre o Maranhão)
- Abertura narrativa (cena, anedota ou imagem que introduz o tema)
- Desenvolvimento (3-5 seções com subtítulos)
- Fechamento reflexivo (conexão com o presente ou com temas do livro)
- Notas e referências do capítulo
```

### Extensão por Capítulo
- Mínimo: 15 páginas (~6.000 palavras)
- Máximo: 30 páginas (~12.000 palavras)
- Ideal: 20-25 páginas (~8.000-10.000 palavras)

### Citações e Referências
- Formato ABNT para referências bibliográficas
- Citações diretas com aspas e referência completa
- Citações longas (>3 linhas) em bloco recuado
- Fontes orais indicadas com nome, contexto e data quando possível

## 3. Regras de Pesquisa

### Fontes Obrigatórias por Tipo de Conteúdo
| Tipo de Conteúdo | Fontes Mínimas |
|---|---|
| Dados históricos | 2 fontes acadêmicas + 1 fonte primária |
| Dados estatísticos | IBGE, IPEA ou órgão oficial equivalente |
| Informações culturais | 1 pesquisador local + 1 fonte etnográfica |
| Biografias | 2 fontes independentes |
| Dados ambientais | ICMBio, INPE ou órgão ambiental competente |

### Verificação
- Todo dado numérico deve ter fonte verificável
- Datas históricas devem ser cruzadas com pelo menos 2 fontes
- Relatos orais devem ser identificados como tal
- Evitar Wikipedia como fonte final (usar como ponto de partida)

## 4. Sensibilidades Editoriais

### Temas que Exigem Cuidado Especial
- **Escravidão**: tratar com a gravidade devida, sem espetacularizar o sofrimento
- **Comunidades quilombolas**: respeitar autodeterminação, evitar paternalismo
- **Povos indígenas**: usar etnônimos corretos, reconhecer diversidade entre povos
- **Religiosidade afro-brasileira**: tratar com respeito, evitar folclorização
- **Desigualdade social**: apresentar dados sem revitimizar populações
- **Política local**: manter equilíbrio, evitar partidarismo

### Terminologia Preferida
- "Escravizado" (não "escravo")
- "Povos indígenas" ou "povos originários" (não "índios")
- "Comunidades quilombolas" (não "remanescentes de quilombos" salvo contexto legal)
- "Tambor de Mina" (não "macumba" ou termos pejorativos)
- "Maranhense" (não "maranho" ou formas pejorativas)

## 5. Formatação

### Markdown de Produção
- Cada capítulo em arquivo `.md` separado
- Nome do arquivo: `cap-XX-titulo-slug.md`
- Imagens referenciadas com placeholder: `![Descrição](img/cap-XX-nome.jpg)`
- Notas de rodapé usando sintaxe `[^1]`

### Metadados por Arquivo
```yaml
---
capitulo: X
titulo: "Título do Capítulo"
parte: "Nome da Parte"
status: rascunho | revisao | aprovado | final
versao: 1.0
agente: nome-do-agente
data_criacao: YYYY-MM-DD
data_revisao: YYYY-MM-DD
palavras: XXXX
---
```
