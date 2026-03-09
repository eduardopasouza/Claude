# Maranhão Book Plugin

Plugin para orquestrar a redação colaborativa do livro sobre o Maranhão usando agentes especializados.

## Estrutura

```
maranhao-book-plugin/
├── skills/          # Skills especializadas (pesquisa, redação, revisão, etc.)
├── agents/          # Configurações de agentes por tópico/função
├── references/      # Referências bibliográficas e fontes
├── drafts/          # Rascunhos e versões dos capítulos
└── config/          # Configurações do plugin e do projeto
```

## Fluxo de Trabalho

1. **Importar** contexto do projeto da Manus AI (ver `PROMPT_MANUS_EXPORT.md`)
2. **Configurar** agentes especializados por tópico/capítulo
3. **Delegar** redação via skills com instruções específicas
4. **Revisar** e integrar os outputs dos agentes
5. **Compilar** o livro final

## Status

- [ ] Exportação de dados da Manus AI
- [ ] Definição da estrutura de capítulos
- [ ] Configuração dos agentes
- [ ] Redação dos capítulos
- [ ] Revisão e edição
- [ ] Compilação final
