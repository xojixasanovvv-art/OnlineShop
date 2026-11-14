"""
config.py — loyihaning barcha sozlamalari bitta joyda
.env fayl bo'lsa o'shandan o'qiydi, bo'lmasa default qiymatlar ishlaydi.
Bu fayl TZ 8-bo'lim: SECRET_KEY va DB URL hardcode bo'lmasligi sharti uchun.
"""
import os
import secrets
from pathlib import Path

# .env ni oddiy o'qish (python-dotenv bo'lmasa ham ishlaydi)
def _load_dotenv():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        return
    for line in env_path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        key, value = key.strip(), value.strip().strip('"').strip("'")
        if key not in os.environ:
            os.environ[key] = value

_load_dotenv()

# Asosiy sozlamalar — bularni .env da o'zgartirsa bo'ladi
# Xavfsizlik: repo da ko'rinadigan "namuna" kalitlar bilan ishlash taqiqlanadi.
_DEFAULT_SECRET_KEYS = {
    "",
    "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7",
    "change-me",
    "changeme",
}
APP_ENV: str = os.getenv("APP_ENV", os.getenv("ENV", "development")).strip().lower()
_env_secret = os.getenv("SECRET_KEY", "").strip()

if _env_secret in _DEFAULT_SECRET_KEYS:
    if APP_ENV in {"prod", "production"}:
        raise RuntimeError(
            "SECRET_KEY .env da o'rnatilmagan yoki namuna kalit. "
            "Yangi kalit: python -c \"import secrets; print(secrets.token_hex(32))\""
        )
    print(
        "[SECURITY WARNING] SECRET_KEY .env da o'rnatilmagan — vaqtinchalik "
        "tasodifiy kalit ishlatilmoqda. Server qayta ishga tushganda tokenlar bekor bo'ladi. "
        "Doimiy kalit uchun .env ga SECRET_KEY yozing."
    )
    _env_secret = secrets.token_hex(32)

SECRET_KEY: str = _env_secret
ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_DAYS: int = int(os.getenv("REFRESH_TOKEN_EXPIRE_DAYS", "7"))
DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://postgres:1@localhost:5432/postgres")
# Telegram bot sozlamalari
BOT_TOKEN: str = os.getenv("BOT_TOKEN", "")  # @BotFather dan olingan token
ADMIN_TG_ID: str = os.getenv("ADMIN_TG_ID", "")  # admin telegram chat id (masalan 123456789)
# MinIO S3 sozlamalari
MINIO_ENDPOINT: str = os.getenv("MINIO_ENDPOINT", "")  # masalan localhost:9000 yoki minio:9000 (docker)
MINIO_ACCESS_KEY: str = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY: str = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET: str = os.getenv("MINIO_BUCKET", "onlineshop")
MINIO_SECURE: bool = os.getenv("MINIO_SECURE", "false").lower() == "true"
# Email (SMTP) sozlamalari — parol tiklash kodi yuborish uchun
SMTP_HOST: str = os.getenv("SMTP_HOST", "")
SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER: str = os.getenv("SMTP_USER", "")
SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
SMTP_FROM: str = os.getenv("SMTP_FROM", "") or os.getenv("SMTP_USER", "")
SMTP_STARTTLS: bool = os.getenv("SMTP_STARTTLS", "true").lower() in ("1", "true", "yes")
# Parol tiklash kodi sozlamalari
RESET_CODE_LENGTH: int = int(os.getenv("RESET_CODE_LENGTH", "6"))
RESET_CODE_EXPIRE_MINUTES: int = int(os.getenv("RESET_CODE_EXPIRE_MINUTES", "10"))
RESET_CODE_MAX_ATTEMPTS: int = int(os.getenv("RESET_CODE_MAX_ATTEMPTS", "5"))
