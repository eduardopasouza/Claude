"""simengine — motor determinístico para os simuladores em sim/.

Este pacote é chamado pelos Skills via Bash. Não faz chamadas de LLM:
toda criatividade narrativa é responsabilidade dos Skills carregados
pelo Claude Code. simengine cuida de schemas, validação e aplicação
determinística de deltas.
"""

__version__ = "0.1.0"
