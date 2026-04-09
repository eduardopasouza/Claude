"""Rotas de autenticação."""

from fastapi import APIRouter, HTTPException, Depends, Header
from typing import Optional

from app.services.auth import (
    UserRegister, UserLogin, UserProfile, TokenResponse,
    hash_password, verify_password, create_token, decode_token,
    get_plan_limits,
)

router = APIRouter()

# In-memory user store (production: database)
_users_db: dict[str, dict] = {}
_user_counter = 0


def get_current_user(authorization: Optional[str] = Header(None)) -> Optional[dict]:
    """Dependency to extract current user from JWT token."""
    if not authorization:
        return None
    if not authorization.startswith("Bearer "):
        return None
    token = authorization[7:]
    payload = decode_token(token)
    return payload


@router.post("/register", response_model=TokenResponse)
async def register(data: UserRegister):
    """Registra um novo usuário."""
    global _user_counter

    if data.email in _users_db:
        raise HTTPException(status_code=409, detail="Email ja cadastrado")

    _user_counter += 1
    user_id = _user_counter

    _users_db[data.email] = {
        "id": user_id,
        "email": data.email,
        "name": data.name,
        "password_hash": hash_password(data.password),
        "cpf_cnpj": data.cpf_cnpj,
        "plan": data.plan,
        "reports_used_this_month": 0,
        "created_at": "2026-04-09T00:00:00Z",
    }

    token = create_token(user_id, data.email, data.plan)
    user = _users_db[data.email]

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
    """Autentica um usuário e retorna JWT."""
    user = _users_db.get(data.email)
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
    """Retorna dados do usuário autenticado."""
    if not user:
        raise HTTPException(status_code=401, detail="Nao autenticado")

    email = user.get("email")
    stored = _users_db.get(email)
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
    """Retorna limites do plano do usuário."""
    plan = user.get("plan", "free") if user else "free"
    return {"plan": plan, "limits": get_plan_limits(plan)}
