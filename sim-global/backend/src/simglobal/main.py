"""FastAPI app do sim-global. Serve frontend + API JSON."""
from __future__ import annotations

import logging
import os
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from . import __version__
from .config import load_config, project_root
from .persistence import (
    CampaignAlreadyExistsError,
    export_game_state,
    get_session,
    import_game_state,
    init_db,
    list_campaigns,
    make_engine,
    make_session_factory,
)
from .routes import api_router
from .state_loader import load_example, list_examples

logger = logging.getLogger(__name__)


def _resolve_db_url(url: str) -> str:
    """Garante que o diretório do SQLite existe e resolve URL relativa."""
    if url.startswith("sqlite:///") and not url.startswith("sqlite:////"):
        # Relativa à raiz do projeto.
        rel = url.replace("sqlite:///", "", 1)
        abs_path = (project_root() / rel).resolve()
        abs_path.parent.mkdir(parents=True, exist_ok=True)
        return f"sqlite:///{abs_path}"
    if url.startswith("sqlite:////"):
        # Absoluta (e.g. sqlite:////data/saves/simglobal.db em volume Fly).
        abs_path = Path("/" + url.split("sqlite:////", 1)[1])
        abs_path.parent.mkdir(parents=True, exist_ok=True)
    return url


def _try_make_agent_runner(model: str, token_env: str):
    """Inicializa AgentRunner se SDK + token disponíveis. Caso contrário None."""
    if not os.getenv(token_env):
        logger.info("agent: %s ausente; rotas LLM retornarão 503", token_env)
        return None
    try:
        from .agent import AgentRunner

        runner = AgentRunner(model=model, token_env=token_env)
        logger.info("agent: AgentRunner pronto (modelo=%s)", model)
        return runner
    except ImportError as exc:
        logger.warning("agent: SDK não instalado (%s)", exc)
        return None


def _autoseed_example(session_factory, example_name: str = "brasil-vargas-1930") -> None:
    """Importa o cenário-piloto se DB ainda não tem nenhuma campanha."""
    with session_factory() as session:
        if list_campaigns(session):
            return
        try:
            state = load_example(example_name)
        except FileNotFoundError:
            logger.warning("autoseed: exemplo %s ausente", example_name)
            return
        try:
            import_game_state(session, example_name, state)
            session.commit()
            logger.info("autoseed: %s importado", example_name)
        except CampaignAlreadyExistsError:
            session.rollback()


def create_app() -> FastAPI:
    cfg = load_config()

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        url = _resolve_db_url(cfg.persistence.database_url)
        engine = make_engine(url, echo=cfg.persistence.echo_sql)
        init_db(engine)
        session_factory = make_session_factory(engine)
        _autoseed_example(session_factory)
        app.state.engine = engine
        app.state.session_factory = session_factory
        app.state.agent_runner = _try_make_agent_runner(
            cfg.agent.model, cfg.agent.oauth_token_env
        )
        try:
            yield
        finally:
            engine.dispose()

    app = FastAPI(
        title="sim-global",
        version=__version__,
        description="Simulador histórico-estratégico turn-based local.",
        lifespan=lifespan,
    )

    web_dir = Path(__file__).parent / "web"
    static_dir = web_dir / "static"
    templates_dir = web_dir / "templates"

    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    # Servir mapa SVG e bandeiras a partir do diretório data/.
    data_dir = project_root() / "data"
    if data_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(data_dir)), name="assets")

    templates = Jinja2Templates(directory=str(templates_dir))
    app.include_router(api_router)

    @app.get("/", response_class=HTMLResponse)
    def index(request: Request) -> HTMLResponse:
        examples = list_examples()
        active = None
        state = None
        # Tenta carregar a primeira campanha do DB.
        with request.app.state.session_factory() as session:
            campaigns = list_campaigns(session)
            if campaigns:
                active = campaigns[0].name
                try:
                    state = export_game_state(session, active)
                except Exception:
                    state = None
        # Fallback: carrega exemplo direto do disco.
        if state is None:
            active = examples[0] if examples else None
            state = load_example(active) if active else None

        return templates.TemplateResponse(
            request=request,
            name="index.html",
            context={
                "examples": examples,
                "active": active,
                "state": state,
                "version": __version__,
                "model": cfg.agent.model,
                "agent_ready": request.app.state.agent_runner is not None,
            },
        )

    @app.get("/api/health")
    def health() -> dict[str, object]:
        return {
            "status": "ok",
            "version": __version__,
            "agent_ready": getattr(app.state, "agent_runner", None) is not None,
        }

    return app


app = create_app()
