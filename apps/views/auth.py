"""
auth.py — autentifikatsiya moduli
TZ 5.1: register, login, refresh, me (GET+PATCH)
Har bir endpoint tushunarli, ixcham va xavfsiz yozilgan.
"""
import hashlib
import logging
import os
import secrets
import uuid
from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session, select
from sqlalchemy import func

from apps.config import (
    SECRET_KEY,
    RESET_CODE_EXPIRE_MINUTES,
    RESET_CODE_LENGTH,
    RESET_CODE_MAX_ATTEMPTS,
)
from apps.database import get_session
from apps.dependencies import get_current_user
from apps.forms import (
    RegisterForm, LoginForm, Token, RefreshTokenRequest, ProfileResponse,
    ProfileUpdateForm, ForgotPasswordForm, ResetPasswordCodeForm,
)
from apps.i18n import get_lang, t
from apps.mailer import send_reset_code
from apps.models import User, PasswordResetToken
from apps.uploads import MAX_IMAGE_BYTES, read_image
from apps.utils import hash_password, check_password, create_access_and_refresh_tokens, verify_token

log = logging.getLogger("onlineshop.auth")

router = APIRouter(tags=["Auth"])


# ── Ro'yxatdan o'tish ──────────────────────────
@router.post("/auth/register", status_code=201)
@router.post("/user/register", status_code=201, include_in_schema=False)
def register(form: RegisterForm, session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    # username va emailni normalizatsiya qilamiz (bo'sh joy + harf)
    username = form.username.strip().lower()
    email = str(form.email).strip().lower()
    # username bandmi? (katta-kichik harfga sezgir)
    if session.exec(select(User).where(func.lower(User.username) == username)).first():
        raise HTTPException(status_code=409, detail=t("username_taken", lang))
    # email bandmi?
    if session.exec(select(User).where(func.lower(User.email) == email)).first():
        raise HTTPException(status_code=409, detail=t("email_taken", lang))
    user = User(
        name=form.name.strip(),
        username=username,
        email=email,
        password=hash_password(form.password),
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return {"message": t("register_success", lang), "user_id": user.id}


# ── Login ─────────────────────────────────────
@router.post("/auth/login", response_model=Token)
@router.post("/user/login", response_model=Token, include_in_schema=False)
def login(form: LoginForm, session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    # username yoki email — ikkalasi ham ishlaydi
    # (parol tiklash email orqali o'tgani uchun login ham emailni qabul qilishi kerak)
    login_id = form.username.strip()
    # username va email ikkalasi ham katta-kichik harfga sezgir emas
    user = session.exec(
        select(User).where(func.lower(User.username) == login_id.lower())
    ).first()
    if not user:
        user = session.exec(
            select(User).where(func.lower(User.email) == login_id.lower())
        ).first()
    if not user or not check_password(form.password, user.password):
        raise HTTPException(status_code=401, detail=t("wrong_credentials", lang))
    if not user.is_active:
        raise HTTPException(status_code=403, detail=t("account_blocked", lang))
    access, refresh = create_access_and_refresh_tokens(user.username)
    return Token(access_token=access, refresh_token=refresh)


# ── Refresh ───────────────────────────────────
@router.post("/auth/refresh", response_model=Token)
@router.post("/refresh", response_model=Token, include_in_schema=False)
def refresh_token(body: RefreshTokenRequest, lang: str = Depends(get_lang)):
    username = verify_token(body.refresh_token, token_type="refresh", lang=lang)
    access, refresh = create_access_and_refresh_tokens(username)
    return Token(access_token=access, refresh_token=refresh)


# ── Hozirgi foydalanuvchi (me) ─────────────────
def _profile(user: User) -> ProfileResponse:
    return ProfileResponse(
        id=user.id,
        name=user.name,
        username=user.username,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
        avatar_url=user.avatar_url,
        created_at=user.created_at,
    )


@router.get("/auth/me", response_model=ProfileResponse)
@router.get("/user/get/me", response_model=ProfileResponse, include_in_schema=False)
def read_me(user: User = Depends(get_current_user)):
    """Joriy kirgan foydalanuvchi ma'lumotlari (parol hash qaytarilmaydi)."""
    return _profile(user)


@router.patch("/auth/me", response_model=ProfileResponse)
@router.patch("/user/update/me", response_model=ProfileResponse, include_in_schema=False)
def update_me(
    form: ProfileUpdateForm,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
    lang: str = Depends(get_lang),
):
    """Ism, email yoki avatar URL'ni yangilaydi. Username o'zgartirilmaydi."""
    if form.name is not None:
        name = form.name.strip()
        if not name:
            raise HTTPException(status_code=400, detail=t("invalid_input", lang))
        user.name = name

    if form.email is not None:
        email = str(form.email).strip().lower()
        taken = session.exec(select(User).where(User.email == email)).first()
        if taken and taken.id != user.id:
            raise HTTPException(status_code=409, detail=t("email_taken", lang))
        user.email = email

    if form.avatar_url is not None:
        user.avatar_url = form.avatar_url.strip() or None

    session.add(user)
    session.commit()
    session.refresh(user)
    return _profile(user)


# ── Avatar yuklash ─────────────────────────────
AVATAR_DIR = "static/media/avatars"


@router.post("/auth/avatar", response_model=ProfileResponse)
@router.post("/user/avatar", response_model=ProfileResponse, include_in_schema=False)
def upload_avatar(
    file: UploadFile = File(...),
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
):
    """Avatar rasmini yuklaydi (5 MB gacha, faqat haqiqiy rasm formatlari)."""
    # Format va hajm fayl mazmuni bo'yicha tekshiriladi (kengaytmaga ishonmaymiz).
    data, _mime, ext = read_image(file, MAX_IMAGE_BYTES, lang)

    os.makedirs(AVATAR_DIR, exist_ok=True)
    filename = f"{user.id}_{uuid.uuid4().hex}{ext}"
    path = os.path.join(AVATAR_DIR, filename)
    with open(path, "wb") as fh:
        fh.write(data)

    user.avatar_url = f"/static/media/avatars/{filename}"
    session.add(user)
    session.commit()
    session.refresh(user)
    return _profile(user)


# ── Parol tiklash: email orqali kod ───────────
# Kodlar sha256 bilan saqlanadi. "Tuz" qismi SECRET_KEY dan keladi —
# bu parol tiklash kodlarini tokenlar (JWT)dan ajratib turadi.
CODE_SALT = hashlib.sha256(f"reset-code::{SECRET_KEY}".encode()).hexdigest()


def _hash_code(code: str) -> str:
    """Kodni sha256 ko'rinishida saqlaymiz (oddiy matnda saqlanmaydi)."""
    return hashlib.sha256(f"{CODE_SALT}:{code}".encode()).hexdigest()


def _new_code() -> str:
    return "".join(secrets.choice("0123456789") for _ in range(RESET_CODE_LENGTH))


@router.post("/auth/forgot-password")
@router.post("/user/forgot-password", include_in_schema=False)
def forgot_password(
    form: ForgotPasswordForm,
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
):
    """Emailga 6 raqamli tiklash kodi yuboradi.

    Xavfsizlik: javob har doim bir xil — foydalanuvchi mavjudligini
    oshkor qilmaydi.
    """
    email = str(form.email).strip().lower()
    user = session.exec(select(User).where(User.email == email)).first()

    if user:
        # eski kodlarni bekor qilamiz
        for old in session.exec(
            select(PasswordResetToken).where(PasswordResetToken.user_id == user.id)
        ).all():
            old.used = True
            session.add(old)

        code = _new_code()
        row = PasswordResetToken(
            token=_hash_code(code),
            user_id=user.id,
            expires_at=datetime.utcnow() + timedelta(minutes=RESET_CODE_EXPIRE_MINUTES),
        )
        session.add(row)
        session.commit()

        if not send_reset_code(
            user.email, code, lang=lang, minutes=RESET_CODE_EXPIRE_MINUTES
        ):
            log.error("Tiklash kodi yuborilmadi: %s", user.email)

    # har doim bir xil javob
    return {"message": t("resetCodeSent", lang)}


@router.post("/auth/reset-password")
@router.post("/user/reset-password", include_in_schema=False)
def reset_password(
    form: ResetPasswordCodeForm,
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
):
    """Kodni tekshirib, parolni yangilaydi."""
    email = str(form.email).strip().lower()
    user = session.exec(select(User).where(User.email == email)).first()
    if not user:
        raise HTTPException(status_code=400, detail=t("resetCodeInvalid", lang))

    now = datetime.utcnow()
    rows = session.exec(
        select(PasswordResetToken)
        .where(PasswordResetToken.user_id == user.id)
        .order_by(PasswordResetToken.id.desc())
    ).all()

    # hali ishlatilmagan va muddati o'tmagan kodlar
    valid = [r for r in rows if not r.used and r.expires_at > now]
    if not valid:
        raise HTTPException(status_code=400, detail=t("resetCodeExpired", lang))

    digest = _hash_code(form.code)
    match = next((r for r in valid if secrets.compare_digest(r.token, digest)), None)
    if not match:
        # noto'g'ri kod: urinishni hisoblaymiz, chegaradan o'tsa kod o'ldiriladi
        for r in valid:
            r.attempts += 1
            if r.attempts >= RESET_CODE_MAX_ATTEMPTS:
                r.used = True
            session.add(r)
        session.commit()
        raise HTTPException(status_code=400, detail=t("resetCodeInvalid", lang))

    match.used = True
    user.password = hash_password(form.new_password)
    session.add(user)
    session.add(match)
    session.commit()
    return {"message": t("passwordChanged", lang)}
