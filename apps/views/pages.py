"""
pages.py — HTML sahifalar (Jinja2)
Frontend chiroyli va responsive
"""
from fastapi import APIRouter, Request

from apps.views.main import templates

from apps.config import RESET_CODE_EXPIRE_MINUTES

router = APIRouter(tags=["Pages"])


@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse(request, "index.html")


@router.get("/register-page")
async def register_page(request: Request):
    return templates.TemplateResponse(request, "register.html")


@router.get("/login-page")
async def login_page(request: Request):
    return templates.TemplateResponse(request, "login.html")


@router.get("/forgot-password-page")
async def forgot_password_page(request: Request):
    return templates.TemplateResponse(
        request,
        "forgot_password.html",
        {"reset_expire_minutes": RESET_CODE_EXPIRE_MINUTES},
    )


@router.get("/profile-page")
async def profile_page(request: Request):
    return templates.TemplateResponse(request, "profile.html")


@router.get("/cart-page")
async def cart_page(request: Request):
    return templates.TemplateResponse(request, "cart.html")


@router.get("/pay-page")
async def pay_page(request: Request):
    return templates.TemplateResponse(request, "pay.html")


@router.get("/product/{product_id}")
async def product_detail_page(request: Request, product_id: int):
    return templates.TemplateResponse(request, "product_detail.html", {"product_id": product_id})


@router.get("/admin-page")
async def admin_page(request: Request):
    return templates.TemplateResponse(request, "admin.html")


@router.get("/wishlist-page")
async def wishlist_page(request: Request):
    return templates.TemplateResponse(request, "wishlist.html")
