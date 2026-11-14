"""
main.py — FastAPI ilovasining kirish nuqtasi
Barcha routerlar shu yerda yig'iladi (APIRouter, DRY prinsipi)
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from apps.database import create_db_and_tables

app = FastAPI(
    title="OnlineShop API",
    description="TZ bo'yicha to'liq OnlineShop backend — JWT, Cart, Order, Review, Address",
    version="1.0.0",
)

# static va templates — frontend uchun
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/health")
async def health_check():
    return {
        "status": "ok",
        "message": "OnlineShop API ishlayapti"
    }

@app.middleware("http")
async def security_headers(request, call_next):
    """Barcha javoblarga asosiy xavfsizlik headerlarini qo'shadi."""
    response = await call_next(request)
    response.headers.setdefault("X-Content-Type-Options", "nosniff")
    response.headers.setdefault("X-Frame-Options", "DENY")
    response.headers.setdefault("Referrer-Policy", "strict-origin-when-cross-origin")
    response.headers.setdefault(
        "Permissions-Policy", "geolocation=(), microphone=(), camera=()"
    )
    return response

# DB jadvallarini ishga tushganda yaratish + MinIO bucket
@app.on_event("startup")
def on_startup():
    create_db_and_tables()
    try:
        from apps.minio_client import ensure_bucket
        ensure_bucket()
    except Exception as e:
        print(f"[MinIO] startup bucket ensure failed: {e}")

# ── Routerlarni ulash ───────────────────────────
# Har bir modul APIRouter bilan yozilgan, bu TZ 8-bo'lim talabi
from apps.views import auth, category, product, cart, order, review, address, pages, admin, payment, wishlist  # noqa

app.include_router(auth.router)
app.include_router(category.router)
app.include_router(product.router)
app.include_router(cart.router)
app.include_router(order.router)
# app.include_router(review.router)
app.include_router(review.router)
app.include_router(address.router)
app.include_router(admin.router)
app.include_router(payment.router)
app.include_router(wishlist.router)
app.include_router(pages.router)
