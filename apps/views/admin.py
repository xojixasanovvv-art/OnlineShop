"""
admin.py — TZ 5.8 bonus admin panel API
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field, field_validator
from sqlmodel import Session, select

from apps.database import get_session
from apps.dependencies import require_admin
from apps.i18n import get_lang, t
from apps.models import Order, User
from apps.utils import hash_password

router = APIRouter(prefix="/admin", tags=["Admin"])


class PasswordUpdate(BaseModel):
    """Parol JSON body orqali yuboriladi (URL/logda ko'rinmasligi uchun)."""

    new_password: str = Field(..., min_length=8, max_length=72)

    @field_validator("new_password")
    @classmethod
    def password_valid(cls, v):
        if not v.strip():
            raise ValueError("Parol bo'sh bo'lmasligi kerak")
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Parol 72 baytdan uzun bo'lmasligi kerak")
        return v


def _safe(user: User) -> dict:
    """Parol HASHI hech qachon mijozga yuborilmaydi."""
    return {
        "id": user.id,
        "name": user.name,
        "username": user.username,
        "email": user.email,
        "role": user.role,
        "is_active": user.is_active,
        "avatar_url": user.avatar_url,
        "created_at": user.created_at,
    }


@router.get("/users")
def list_users(session: Session = Depends(get_session), admin: User = Depends(require_admin)):
    return [_safe(u) for u in session.exec(select(User)).all()]


@router.patch("/users/{user_id}/toggle-active")
def toggle_user_active(user_id: int, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=t("user_not_found", lang))
    if user.id == admin.id:
        raise HTTPException(status_code=400, detail=t("cannot_block_self", lang))
    user.is_active = not user.is_active
    session.add(user)
    session.commit()
    session.refresh(user)
    return _safe(user)


@router.patch("/users/{user_id}/role")
def change_user_role(
    user_id: int,
    role: str,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin),
    lang: str = Depends(get_lang),
):
    """Foydalanuvchini admin yoki user qilish."""
    if role not in ("user", "admin"):
        raise HTTPException(status_code=400, detail="Role faqat 'user' yoki 'admin' bo'lishi kerak")
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail=t("user_not_found", lang))
    if user.id == admin.id and role != "admin":
        raise HTTPException(status_code=400, detail=t("cannot_demote_self", lang))
    user.role = role
    session.add(user)
    session.commit()
    session.refresh(user)
    return _safe(user)


@router.patch("/users/{user_id}/password")
def set_user_password(
    user_id: int,
    payload: PasswordUpdate,
    session: Session = Depends(get_session),
    admin: User = Depends(require_admin),
):
    """Admin foydalanuvchi uchun yangi parol belgilaydi (parol unutgan bo'lsa)."""
    new_password = payload.new_password
    user = session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Foydalanuvchi topilmadi")
    user.password = hash_password(new_password)
    session.add(user)
    session.commit()
    return {"message": "Parol yangilandi", "user_id": user.id}


@router.get("/stats")
def get_stats(session: Session = Depends(get_session), admin: User = Depends(require_admin)):
    total_orders = len(session.exec(select(Order)).all())
    total_revenue = sum(o.total_price for o in session.exec(select(Order).where(Order.status != "cancelled")).all())
    total_users = len(session.exec(select(User)).all())
    return {"total_users": total_users, "total_orders": total_orders, "total_revenue": total_revenue}
