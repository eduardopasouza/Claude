"""Entrypoint serverless para Vercel.

Vercel detecta 'app' como ASGI handler. Este módulo:
- prepara sys.path para que `simglobal` seja importável (o pacote
  vive em ../backend/src/simglobal);
- configura DB para /tmp (único lugar gravável em serverless);
- desativa autostart do browser e o Agent SDK (que não roda em
  serverless por depender de subprocess CLI);
- importa a FastAPI app criada pelo factory.
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Permite importar simglobal sem instalar como pacote.
_HERE = Path(__file__).resolve().parent
_BACKEND_SRC = _HERE.parent / "backend" / "src"
if str(_BACKEND_SRC) not in sys.path:
    sys.path.insert(0, str(_BACKEND_SRC))

# Defaults para serverless.
os.environ.setdefault("SIMGLOBAL_HOST", "0.0.0.0")
os.environ.setdefault("SIMGLOBAL_OPEN_BROWSER", "0")
os.environ.setdefault("SIMGLOBAL_DATABASE_URL", "sqlite:////tmp/simglobal.db")

from simglobal.main import create_app  # noqa: E402

app = create_app()
