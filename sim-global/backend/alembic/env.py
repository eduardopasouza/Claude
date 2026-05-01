"""Alembic environment para sim-global.

Resolução de URL (em ordem de prioridade):
  1. variável de ambiente SIMGLOBAL_DATABASE_URL
  2. config.yaml na raiz do projeto (persistence.database_url)
  3. fallback de alembic.ini (sqlalchemy.url)
"""
from __future__ import annotations

import os
import sys
from logging.config import fileConfig
from pathlib import Path

from alembic import context
from sqlalchemy import engine_from_config, pool

# Garante que `src/` está em sys.path para importar simglobal.persistence.
HERE = Path(__file__).resolve().parent
SRC_DIR = HERE.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from simglobal.persistence.models import Base  # noqa: E402

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)


def _resolve_database_url() -> str:
    env_url = os.environ.get("SIMGLOBAL_DATABASE_URL")
    if env_url:
        return env_url

    # tenta config.yaml da raiz do projeto
    project_root = HERE.parent.parent  # backend/alembic/.. = backend/.. = raiz
    config_path = project_root / "config.yaml"
    if config_path.exists():
        try:
            import yaml

            data = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            url = data.get("persistence", {}).get("database_url")
            if isinstance(url, str) and url:
                return url
        except Exception:
            pass

    return config.get_main_option("sqlalchemy.url") or "sqlite:///saves/simglobal.db"


target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = _resolve_database_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=url.startswith("sqlite"),
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    url = _resolve_database_url()
    section = config.get_section(config.config_ini_section) or {}
    section["sqlalchemy.url"] = url
    connectable = engine_from_config(
        section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=url.startswith("sqlite"),
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
