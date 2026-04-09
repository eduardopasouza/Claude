"""
Rotas de autenticação.

Suporta dois modos:
- Com PostgreSQL: persistencia real via SQLAlchemy (producao)
- Sem PostgreSQL: fallback in-memory (dev/testes)
"""

import logging
from datetime import datetime, timezone

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional

from app.services.auth import (
    UserRegister, UserLogin, UserProfile, TokenResponse,
    hash_password, verify_password, create_token, decode_token,
    get_plan_limits,
)

logger = logging.getLogger("agrojus.auth")
router = APIRouter()

# --- User storage backend ---

_use_db = False
_memory_store: dict[str, dict] = {}
_user_counter = 0


def _try_init_db():
    """Tenta conectar ao PostgreSQL. Se falhar, usa in-memory."""
    global _use_db
    try:
        from app.models.database import get_engine
        engine = get_engine()
        conn = engine.connect()
        conn.close()
        _use_db = True
        logger.info("Auth using PostgreSQL backend")
    except Exception:
        _use_db = False
        logger.info("Auth using in-memory backend (no DB available)")


_try_init_db()


def _db_find_user(email: str) -> Optional[dict]:
    """Busca usuario no PostgreSQL."""
    from app.models.database import get_session, User
    session = get_session()
    try:
        user = session.query(User).filter(User.email == email).first()
        if user:
            return {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "password_hash": user.password_hash,
                "cpf_cnpj": user.cpf_cnpj,
                "plan": user.plan,
                "reports_used_this_month": user.reports_used_this_month,
                "created_at": user.created_at.isoformat() if user.created_at else "",
            }
        return None
    finally:
        session.close()


def _db_create_user(data: UserRegister) -> dict:
    """Cria usuario no PostgreSQL."""
    from app.models.database import get_session, User
    session = get_session()
    try:
        user = User(
            email=data.email,
            name=data.name,
            password_hash=hash_password(data.password),
            cpf_cnpj=data.cpf_cnpj,
            plan=data.plan,
        )
        session.add(user)
        session.commit()
        session.refresh(user)
        return {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "password_hash": user.password_hash,
            "cpf_cnpj": user.cpf_cnpj,
            "plan": user.plan,
            "reports_used_this_month": user.reports_used_this_month or 0,
            "created_at": user.created_at.isoformat() if user.created_at else "",
        }
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def _mem_find_user(email: str) -> Optional[dict]:
    return _memory_store.get(email)


def _mem_create_user(data: UserRegister) -> dict:
    global _user_counter
    _user_counter += 1
    user = {
        "id": _user_counter,
        "email": data.email,
        "name": data.name,
        "password_hash": hash_password(data.password),
        "cpf_cnpj": data.cpf_cnpj,
        "plan": data.plan,
        "reports_used_this_month": 0,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    _memory_store[data.email] = user
    return user


def find_user(email: str) -> Optional[dict]:
    if _use_db:
        return _db_find_user(email)
    return _mem_find_user(email)


def create_user(data: UserRegister) -> dict:
    if _use_db:
        return _db_create_user(data)
    return _mem_create_user(data)


# --- Dependencies ---

def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """Dependency to extract current user from JWT token."""
    if not authorization:
        return None
    if not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    return decode_token(token)


# --- Routes ---

@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister):
    """Registra um novo usuario."""
    existing = find_user(data.email)
    if existing:
        raise HTTPException(status_code=409, detail="Email ja cadastrado")

    user = create_user(data)
    token = create_token(user["id"], user["email"], user["plan"])

    return TokenResponse(
        access_token=token,
        user=UserProfile(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            cpf_cnpj=user["cpf_cnpj"],
            plan=user["plan"],
            reports_used_this_month=user["reports_used_this_month"],
            created_at=user["created_at"],
        ),
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin):
    """Autentica um usuario e retorna JWT."""
    user = find_user(data.email)
    if not user:
        raise HTTPException(status_code=401, detail="Credenciais invalidas")

    if not verify_password(data.password, user["password_hash"]):
        raise HTTPException(status_code=401, detail="Credenciais invalidas")

    token = create_token(user["id"], user["email"], user["plan"])

    return TokenResponse(
        access_token=token,
        user=UserProfile(
            id=user["id"],
            email=user["email"],
            name=user["name"],
            cpf_cnpj=user["cpf_cnpj"],
            plan=user["plan"],
            reports_used_this_month=user["reports_used_this_month"],
            created_at=user["created_at"],
        ),
    )


@router.get("/me")
async def get_me(user: dict = Depends(get_current_user)):
    """Retorna dados do usuario autenticado."""
    if not user:
        raise HTTPException(status_code=401, detail="Nao autenticado")

    stored = find_user(user.get("email", ""))
    if not stored:
        raise HTTPException(status_code=404, detail="Usuario nao encontrado")

    return UserProfile(
        id=stored["id"],
        email=stored["email"],
        name=stored["name"],
        cpf_cnpj=stored["cpf_cnpj"],
        plan=stored["plan"],
        reports_used_this_month=stored["reports_used_this_month"],
        created_at=stored["created_at"],
    )


@router.get("/plan-limits")
async def plan_limits(user: dict = Depends(get_current_user)):
    """Retorna limites do plano do usuario."""
    plan = user.get("plan", "free") if user else "free"
    return {"plan": plan, "limits": get_plan_limits(plan)}
