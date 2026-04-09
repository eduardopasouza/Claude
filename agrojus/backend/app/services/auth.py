"""
Sistema de autenticação JWT para AgroJus.

Suporta registro, login, e proteção de rotas por plano (free/basic/pro/enterprise).
"""

import hashlib
import secrets
from datetime import datetime, timezone, timedelta
from typing import Optional

import jwt
from pydantic import BaseModel, EmailStr, Field

from app.config import settings


JWT_SECRET = settings.jwt_secret
JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_HOURS = 24


class UserRegister(BaseModel):
    email: str
    password: str = Field(min_length=8)
    name: str
    cpf_cnpj: Optional[str] = None
    plan: str = "free"  # free, basic, pro, enterprise


class UserLogin(BaseModel):
    email: str
    password: str


class UserProfile(BaseModel):
    id: int
    email: str
    name: str
    cpf_cnpj: Optional[str] = None
    plan: str
    reports_used_this_month: int = 0
    created_at: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = JWT_EXPIRATION_HOURS * 3600
    user: UserProfile


# Plan limits
PLAN_LIMITS = {
    "free": {"reports_per_month": 3, "searches_per_day": 10, "pdf": False, "monitoring": False, "api": False},
    "basic": {"reports_per_month": 20, "searches_per_day": 50, "pdf": True, "monitoring": False, "api": False},
    "pro": {"reports_per_month": 100, "searches_per_day": 500, "pdf": True, "monitoring": True, "api": False},
    "enterprise": {"reports_per_month": -1, "searches_per_day": -1, "pdf": True, "monitoring": True, "api": True},
}


def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    hashed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return f"{salt}:{hashed.hex()}"


def verify_password(password: str, stored: str) -> bool:
    salt, hashed = stored.split(":")
    check = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
    return check.hex() == hashed


def create_token(user_id: int, email: str, plan: str) -> str:
    payload = {
        "sub": str(user_id),
        "email": email,
        "plan": plan,
        "exp": datetime.now(timezone.utc) + timedelta(hours=JWT_EXPIRATION_HOURS),
        "iat": datetime.now(timezone.utc),
    }
    return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_plan_limits(plan: str) -> dict:
    return PLAN_LIMITS.get(plan, PLAN_LIMITS["free"])


def check_plan_permission(plan: str, feature: str) -> bool:
    limits = get_plan_limits(plan)
    return limits.get(feature, False)
