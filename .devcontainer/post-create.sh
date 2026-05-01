#!/usr/bin/env bash
# post-create: roda UMA vez quando o Codespace é criado.
# Instala dependências e prepara o ambiente.
set -euo pipefail

echo "→ instalando dependências do sim-global…"
cd "$(dirname "$0")/../sim-global/backend"
pip install --upgrade pip --quiet
pip install -e ".[dev,agent]" --quiet

echo "→ criando saves/ e validando estado inicial…"
cd ..
mkdir -p saves
python -m simengine.scripts.validate_state \
  examples/brasil-vargas-1930/initial_state.json

echo
echo "✓ ambiente pronto. O app vai subir automaticamente quando o"
echo "  Codespace iniciar (post-start.sh)."
echo
echo "  → Sem CLAUDE_CODE_OAUTH_TOKEN: app sobe em modo LEITURA"
echo "    (mapa, painéis navegáveis; /turn /advise /dm = 503)."
echo
echo "  → Para ativar o motor narrativo Claude Opus 4.7:"
echo "    1. Em outro terminal local SEU, rode:"
echo "         claude setup-token"
echo "    2. Copie o token impresso."
echo "    3. Adicione como secret do Codespace:"
echo "         https://github.com/settings/codespaces"
echo "       Nome: CLAUDE_CODE_OAUTH_TOKEN"
echo "    4. Reinicie este Codespace (… → Rebuild)."
