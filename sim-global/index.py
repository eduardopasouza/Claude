"""Vercel-detected FastAPI entrypoint.

Vercel reconhece automaticamente um arquivo `index.py` (entre outros)
na raiz do projeto Python e expõe seu `app` ASGI. Este módulo:
- prepara sys.path para que `simglobal` seja importável de
  backend/src/simglobal sem instalar como pacote;
- configura DB para /tmp (único caminho gravável em serverless);
- desativa autoboot do browser e o Agent SDK (que não roda em
  serverless por depender de subprocess CLI);
- importa a FastAPI app criada pelo factory `create_app`.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_BACKEND_SRC = _HERE / "backend" / "src"
if str(_BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(_BACKEND_SRC))

os.environ.setdefault("SIMGLOBAL_HOST", "0.0.0.0")
os.environ.setdefault("SIMGLOBAL_OPEN_BROWSER", "0")
os.environ.setdefault("SIMGLOBAL_DATABASE_URL", "sqlite:////tmp/simglobal.db")

from simglobal.main import create_app  # noqa: E402

app = create_app()
