"""Carrega config.yaml da raiz do projeto + overrides via env vars."""
from __future__ import annotations

import os
from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class ServerConfig(BaseModel):
    host: str = "127.0.0.1"
    port: int = 8000
    open_browser: bool = True


class AgentConfig(BaseModel):
    model: str = "claude-opus-4-7"
    max_retries_validation: int = 3
    oauth_token_env: str = "CLAUDE_CODE_OAUTH_TOKEN"


class ConsolidatorConfig(BaseModel):
    threshold: int = 20


class PersistenceConfig(BaseModel):
    database_url: str = "sqlite:///saves/simglobal.db"
    echo_sql: bool = False


class AssetsConfig(BaseModel):
    flags_dir: str = "data/catalog/flags"
    portraits_dir: str = "data/catalog/portraits"
    map_dir: str = "data/map"


class AppConfig(BaseModel):
    server: ServerConfig = Field(default_factory=ServerConfig)
    agent: AgentConfig = Field(default_factory=AgentConfig)
    consolidator: ConsolidatorConfig = Field(default_factory=ConsolidatorConfig)
    persistence: PersistenceConfig = Field(default_factory=PersistenceConfig)
    assets: AssetsConfig = Field(default_factory=AssetsConfig)


def project_root() -> Path:
    """Raiz do sim-global onde estão data/, examples/, config.yaml.

    Em ambiente de dev (instalação editable, src layout), calcula
    subindo a partir deste arquivo. Em container/serverless onde o
    pacote é instalado em site-packages, o cálculo fura — então
    respeitamos a env var SIMGLOBAL_PROJECT_ROOT quando definida
    (Dockerfile/Fly seta para /app; Vercel para o caminho do
    deployment).

    Layout dev: .../sim-global/backend/src/simglobal/config.py
    parents[0]=simglobal/, [1]=src/, [2]=backend/, [3]=sim-global/.
    """
    env = os.getenv("SIMGLOBAL_PROJECT_ROOT")
    if env:
        return Path(env)
    return Path(__file__).resolve().parents[3]


def _apply_env_overrides(cfg: AppConfig) -> AppConfig:
    """Permite que variáveis de ambiente sobrescrevam config.yaml.

    Útil em deploy cloud (Fly.io, Render, Heroku) onde config é
    versionado mas valores específicos do host vêm de env.
    """
    if v := os.getenv("SIMGLOBAL_HOST"):
        cfg.server.host = v
    if v := os.getenv("SIMGLOBAL_PORT") or os.getenv("PORT"):
        try:
            cfg.server.port = int(v)
        except ValueError:
            pass
    if v := os.getenv("SIMGLOBAL_OPEN_BROWSER"):
        cfg.server.open_browser = v.lower() in {"1", "true", "yes", "on"}
    if v := os.getenv("SIMGLOBAL_DATABASE_URL"):
        cfg.persistence.database_url = v
    if v := os.getenv("SIMGLOBAL_MODEL"):
        cfg.agent.model = v
    if v := os.getenv("SIMGLOBAL_CONSOLIDATOR_THRESHOLD"):
        try:
            cfg.consolidator.threshold = int(v)
        except ValueError:
            pass
    return cfg


def load_config(path: Path | None = None) -> AppConfig:
    if path is None:
        path = project_root() / "config.yaml"
    if path.exists():
        raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        cfg = AppConfig.model_validate(raw)
    else:
        cfg = AppConfig()
    return _apply_env_overrides(cfg)
