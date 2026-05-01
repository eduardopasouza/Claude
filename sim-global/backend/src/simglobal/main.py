"""FastAPI app do sim-global. Serve frontend + API JSON."""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from simengine.engine import check_state_invariants
from simengine.schemas import GameState

from . import __version__
from .config import load_config
from .state_loader import list_examples, load_example


def create_app() -> FastAPI:
    cfg = load_config()
    app = FastAPI(
        title="sim-global",
        version=__version__,
        description="Simulador histórico-estratégico turn-based local.",
    )

    web_dir = Path(__file__).parent / "web"
    static_dir = web_dir / "static"
    templates_dir = web_dir / "templates"

    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    templates = Jinja2Templates(directory=str(templates_dir))

    # Estado em memória — fase pré-SQLite. Apenas o cenário-piloto.
    state_cache: dict[str, GameState] = {}

    def _get_state(name: str) -> GameState:
        if name not in state_cache:
            state_cache[name] = load_example(name)
        return state_cache[name]

    # ---------- páginas ----------

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> HTMLResponse:
        examples = list_examples()
        active = examples[0] if examples else None
        state = _get_state(active) if active else None
        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "examples": examples,
                "active": active,
                "state": state,
                "version": __version__,
                "model": cfg.agent.model,
            },
        )

    # ---------- API JSON ----------

    @app.get("/api/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "version": __version__}

    @app.get("/api/examples")
    def api_examples() -> list[str]:
        return list_examples()

    @app.get("/api/state/{name}")
    def api_state(name: str) -> JSONResponse:
        try:
            state = _get_state(name)
        except FileNotFoundError as exc:
            raise HTTPException(404, f"cenário não encontrado: {name}") from exc
        violations = check_state_invariants(state)
        return JSONResponse(
            {
                "campaign": name,
                "state": state.model_dump(mode="json"),
                "invariant_violations": violations,
            }
        )

    return app


app = create_app()
