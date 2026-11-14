"""
utils.py — parol va JWT bilan ishlash
Barcha maxfiy qiymatlar apps.config dan olinadi (hardcode yo'q)
"""
from datetime import datetime, timedelta
from typing import Optional

import bcrypt
import jwt
from fastapi import HTTPException
from starlette import status

from apps.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from apps.i18n import t as tr


# ── Parol ─────────────────────────────────────
# bcrypt 72 baytdan uzun parolni qabul qilmaydi (ValueError beradi).
MAX_PASSWORD_BYTES = 72


def hash_password(password: str) -> str:
    """Oddiy parolni bcrypt bilan hash qiladi"""
    raw = password.encode("utf-8")
    if not password.strip():
        raise ValueError("Parol bo'sh bo'lmasligi kerak")
    if len(raw) > MAX_PASSWORD_BYTES:
        raise ValueError("Parol 72 baytdan uzun bo'lmasligi kerak")
    return bcrypt.hashpw(raw, bcrypt.gensalt()).decode()


def check_password(password: str, hashed_password: str) -> bool:
    """Kiritilgan parol hash bilan mosligini tekshiradi.

    Buzilgan/limitdan uzun parol 500 emas, oddiy "mos emas" javobini beradi.
    """
    try:
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode())
    except (ValueError, TypeError):
        return False


# ── Token yaratish ────────────────────────────
def create_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def create_access_and_refresh_tokens(username: str) -> tuple[str, str]:
    """Login/register dan keyin ikkita token qaytaradi"""
    access = create_token(
        {"sub": username, "type": "access"},
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    refresh = create_token(
        {"sub": username, "type": "refresh"},
        timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    )
    return access, refresh


# ── Token tekshirish ──────────────────────────
def verify_token(token: str, token_type: str = "access", lang: str = "uz") -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        ttype: str = payload.get("type")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=tr("token_invalid", lang))
        if ttype != token_type:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=tr("token_type_invalid", lang, expected=token_type),
            )
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=tr("token_expired", lang))
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=tr("token_invalid_generic", lang))
