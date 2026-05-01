"""Carrega config.yaml da raiz do projeto."""
from __future__ import annotations

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
    """Raiz do sim-global (sobe a partir deste arquivo).

    Layout: .../sim-global/backend/src/simglobal/config.py
    parents[0]=simglobal/, [1]=src/, [2]=backend/, [3]=sim-global/.
    """
    return Path(__file__).resolve().parents[3]


def load_config(path: Path | None = None) -> AppConfig:
    if path is None:
        path = project_root() / "config.yaml"
    if not path.exists():
        return AppConfig()
    raw = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return AppConfig.model_validate(raw)
