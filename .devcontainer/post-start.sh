#!/usr/bin/env bash
# post-start: roda toda vez que o Codespace inicia.
# Sobe o servidor sim-global em background e imprime a URL pública
# que o Codespace expõe automaticamente na porta 8000.
set -euo pipefail

cd "$(dirname "$0")/../sim-global"

# Garante que saves/ existe (volume em /tmp não persiste, mas no
# Codespace o filesystem do workspace persiste entre starts).
mkdir -p saves

echo
echo "================================================================"
echo "  sim-global"
echo "================================================================"
if [ -n "${CLAUDE_CODE_OAUTH_TOKEN:-}" ]; then
  echo "  ✓ token OAuth detectado — modo COMPLETO (Claude Opus 4.7)"
else
  echo "  ⚠ sem CLAUDE_CODE_OAUTH_TOKEN — modo LEITURA"
  echo "    /turn, /advise, /dm vão retornar 503."
  echo "    Veja .devcontainer/post-create.sh para instruções."
fi
echo
echo "  Subindo em http://0.0.0.0:8000…"
echo "  No painel 'PORTS' do VS Code, clique no globo da porta 8000"
echo "  para abrir a URL pública no seu navegador."
echo "================================================================"
echo

# Sobe em background, log em saves/server.log
nohup python -m simglobal > saves/server.log 2>&1 &
echo "PID: $!"
sleep 1
echo "Logs: tail -f sim-global/saves/server.log"
