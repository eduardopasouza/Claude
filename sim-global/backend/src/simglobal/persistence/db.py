"""Engine SQLAlchemy + factory de Session + helpers de bootstrap.

`init_db(engine)` cria todas as tabelas a partir de Base.metadata —
útil em dev/teste rápidos. Em produção, usar Alembic
(`alembic upgrade head`).
"""
from __future__ import annotations

from contextlib import contextmanager
from typing import Iterator

from sqlalchemy import Engine, create_engine
from sqlalchemy.orm import Session, sessionmaker

from .models import Base


def make_engine(database_url: str, *, echo: bool = False) -> Engine:
    """Cria um Engine SQLAlchemy.

    Para SQLite, ativa `check_same_thread=False` quando o URL é
    in-memory ou uma string compartilhada — facilita o uso em testes
    com fixtures de pytest.
    """
    connect_args: dict[str, object] = {}
    if database_url.startswith("sqlite"):
        connect_args["check_same_thread"] = False
    return create_engine(database_url, echo=echo, connect_args=connect_args, future=True)


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Factory de Session vinculada ao engine."""
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


def init_db(engine: Engine) -> None:
    """Cria todas as tabelas conhecidas. Idempotente."""
    Base.metadata.create_all(engine)


def drop_db(engine: Engine) -> None:
    """Apaga todas as tabelas conhecidas. Útil em cleanup de testes."""
    Base.metadata.drop_all(engine)


@contextmanager
def get_session(session_factory: sessionmaker[Session]) -> Iterator[Session]:
    """Context manager com commit/rollback automático."""
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
