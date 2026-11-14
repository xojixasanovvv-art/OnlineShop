"""
dependencies.py — himoyalangan endpointlar uchun umumiy dependency lar
DRY: har bir views faylida bir xil kodni takrorlamaslik uchun
"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlmodel import Session, select

from apps.database import get_session
from apps.i18n import get_lang, t
from apps.models import User
from apps.utils import verify_token

security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
) -> User:
    """Token orqali hozirgi userni qaytaradi. Token yo'q/eski bo'lsa 401"""
    username = verify_token(credentials.credentials, token_type="access", lang=lang)
    user = session.exec(select(User).where(User.username == username)).first()
    if not user:
        raise HTTPException(status_code=404, detail=t("user_not_found", lang))
    if not user.is_active:
        raise HTTPException(status_code=403, detail=t("account_blocked", lang))
    return user


def require_admin(
    current_user: User = Depends(get_current_user),
    lang: str = Depends(get_lang),
) -> User:
    """Faqat admin o'ta oladi, bo'lmasa 403"""
    if current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("admin_required", lang))
    return current_user
