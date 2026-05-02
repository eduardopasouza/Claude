"""Entry point: `python -m simglobal` sobe FastAPI e abre browser."""
from __future__ import annotations

import threading
import time
import webbrowser

import uvicorn

from .config import load_config


def _open_browser_when_ready(url: str, delay: float = 1.5) -> None:
    def _later() -> None:
        time.sleep(delay)
        webbrowser.open(url)

    threading.Thread(target=_later, daemon=True).start()


def main() -> None:
    cfg = load_config()
    url = f"http://{cfg.server.host}:{cfg.server.port}"
    if cfg.server.open_browser:
        _open_browser_when_ready(url)
    print(f"\n  sim-global servindo em {url}\n")
    uvicorn.run(
        "simglobal.main:app",
        host=cfg.server.host,
        port=cfg.server.port,
        reload=False,
        log_level="info",
    )


if __name__ == "__main__":
    main()
