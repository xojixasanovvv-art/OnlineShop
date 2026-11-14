"""
wishlist.py — sevimlilar (yurak)
Foydalanuvchi mahsulotga yurak bosadi, ro'yxat saqlanadi va
alohida sahifada ko'rsatiladi.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from apps.database import get_session
from apps.dependencies import get_current_user
from apps.forms import WishlistForm
from apps.i18n import get_lang, t
from apps.models import Product, User, Wishlist

router = APIRouter(prefix="/wishlist", tags=["Wishlist"])


@router.get("/")
@router.get("", include_in_schema=False)
def get_wishlist(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Foydalanuvchining sevimlilari — mahsulot ma'lumotlari bilan."""
    rows = session.exec(
        select(Wishlist).where(Wishlist.user_id == current_user.id).order_by(Wishlist.created_at.desc())
    ).all()

    items, seen = [], set()
    for row in rows:
        product = session.get(Product, row.product_id)
        if not product or product.id in seen:
            continue
        seen.add(product.id)
        items.append({
            "id": row.id,
            "product_id": product.id,
            "title": product.title,
            "description": product.description,
            "price": product.price,
            "stock": product.stock,
            "image_url": product.images[0].image_url if product.images else None,
            "created_at": row.created_at,
        })
    return {"user_id": current_user.id, "count": len(items), "items": items}


@router.post("/", status_code=201)
@router.post("", status_code=201, include_in_schema=False)
def add_to_wishlist(
    form: WishlistForm,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    lang: str = Depends(get_lang),
):
    """Yurak bosish — mahsulotni sevimlilarga qo'shish (toggle emas, idempotent)."""
    if not session.get(Product, form.product_id):
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))

    existing = session.exec(
        select(Wishlist).where(
            Wishlist.user_id == current_user.id,
            Wishlist.product_id == form.product_id,
        )
    ).first()
    if existing:
        return existing

    item = Wishlist(user_id=current_user.id, product_id=form.product_id)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/{product_id}")
def remove_from_wishlist(
    product_id: int,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    """Yurakni bosib qayta bosish — sevimlilardan olib tashlash."""
    item = session.exec(
        select(Wishlist).where(
            Wishlist.user_id == current_user.id,
            Wishlist.product_id == product_id,
        )
    ).first()
    if not item:
        raise HTTPException(status_code=404, detail="Wishlistda yo'q")
    session.delete(item)
    session.commit()
    return {"deleted": True, "product_id": product_id}


@router.delete("/")
@router.delete("", include_in_schema=False)
def clear_wishlist(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    """Barcha sevimlilarni tozalash."""
    rows = session.exec(select(Wishlist).where(Wishlist.user_id == current_user.id)).all()
    for row in rows:
        session.delete(row)
    session.commit()
    return {"deleted": len(rows)}
