"""
forms.py — Pydantic So'rov/Javob sxemalari
Har bir modul uchun alohida sxema, validatsiya bilan.
TZ 5-bo'limdagi barcha maydonlar qamrab olingan.
"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


# ── Auth ──────────────────────────────────────
# bcrypt faqat 72 baytgacha parolni qabul qiladi.
MAX_PASSWORD_BYTES = 72
USERNAME_PATTERN = r"^[A-Za-z0-9_.-]{3,32}$"


def _validate_password(v: str) -> str:
    """Parol bo'sh emasligi va bcrypt limitiga sig'ishini tekshiradi."""
    if not v or not v.strip():
        raise ValueError("Parol bo'sh bo'lmasligi kerak")
    if len(v.encode("utf-8")) > MAX_PASSWORD_BYTES:
        raise ValueError("Parol 72 baytdan uzun bo'lmasligi kerak")
    return v


class RegisterForm(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    username: str = Field(min_length=3, max_length=32, pattern=USERNAME_PATTERN)
    email: EmailStr
    password: str = Field(min_length=8, max_length=72)

    @field_validator("name")
    @classmethod
    def name_not_blank(cls, v):
        if not v.strip():
            raise ValueError("Ism bo'sh bo'lmasligi kerak")
        return v

    @field_validator("password")
    @classmethod
    def password_valid(cls, v):
        return _validate_password(v)


class LoginForm(BaseModel):
    username: str = Field(min_length=1, max_length=255)
    password: str = Field(min_length=1, max_length=255)


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class ProfileResponse(BaseModel):
    id: int
    name: str
    username: str
    email: str
    role: str
    is_active: bool
    avatar_url: Optional[str] = None
    created_at: Optional[datetime] = None


class ProfileUpdateForm(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    email: Optional[EmailStr] = None
    avatar_url: Optional[str] = Field(default=None, max_length=2048)


# ── Category ──────────────────────────────────
class CategoryForm(BaseModel):
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    parent_id: Optional[int] = None


# ── Product ───────────────────────────────────
class ProductForm(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    stock: int = 0
    category_id: int
    image_url: Optional[str] = None  # ixtiyoriy — bir vaqtning o'zida rasm qo'shish uchun

    @field_validator("price")
    @classmethod
    def price_positive(cls, v):
        if v < 0:
            raise ValueError("Narx manfiy bo'lishi mumkin emas")
        return v


class ProductImageForm(BaseModel):
    image_url: str


# ── Cart ──────────────────────────────────────
class CartItemForm(BaseModel):
    product_id: int
    quantity: int = 1

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v):
        if v < 1:
            raise ValueError("Miqdor kamida 1 bo'lishi kerak")
        return v


class CartItemUpdateForm(BaseModel):
    quantity: int

    @field_validator("quantity")
    @classmethod
    def qty_positive(cls, v):
        if v < 1:
            raise ValueError("Miqdor kamida 1 bo'lishi kerak")
        return v


# ── Order ─────────────────────────────────────
class OrderStatusForm(BaseModel):
    status: str

    @field_validator("status")
    @classmethod
    def status_allowed(cls, v):
        allowed = {"pending", "paid", "shipped", "delivered", "cancelled"}
        if v not in allowed:
            raise ValueError(f"Status {allowed} lardan biri bo'lishi kerak")
        return v


# ── Review ────────────────────────────────────
class ReviewForm(BaseModel):
    rating: int
    comment: Optional[str] = None

    @field_validator("rating")
    @classmethod
    def rating_range(cls, v):
        if not 1 <= v <= 5:
            raise ValueError("Reyting 1 dan 5 gacha bo'lishi kerak")
        return v


# ── Address ───────────────────────────────────
class AddressForm(BaseModel):
    country: str
    city: str
    street: str
    zip_code: str


# ── Wishlist ──────────────────────────────────
class WishlistForm(BaseModel):
    product_id: int


# ── Parol tiklash (email orqali kod) ──────────
class ForgotPasswordForm(BaseModel):
    """Kod yuborish uchun emailni oladi."""

    email: EmailStr


class ResetPasswordCodeForm(BaseModel):
    """Kodni tekshirib, yangi parol o'rnatadi."""

    email: EmailStr
    code: str = Field(min_length=4, max_length=10)
    new_password: str = Field(min_length=8, max_length=72)
    confirm_password: str = Field(min_length=8, max_length=72)

    @field_validator("code")
    @classmethod
    def code_digits(cls, v):
        v = v.strip()
        if not v.isdigit():
            raise ValueError("Kod faqat raqamlardan iborat bo'lishi kerak")
        return v

    @field_validator("new_password", "confirm_password")
    @classmethod
    def password_not_blank(cls, v):
        return _validate_password(v)

    @field_validator("confirm_password")
    @classmethod
    def passwords_match(cls, v, info):
        new = info.data.get("new_password")
        if new and v != new:
            raise ValueError("Parollar mos kelmadi")
        return v

