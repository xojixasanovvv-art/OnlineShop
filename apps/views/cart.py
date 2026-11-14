"""
cart.py — savat
TZ 5.4 dagi barcha endpointlar, PATCH fix va clear qo'shildi
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from apps.database import get_session
from apps.dependencies import get_current_user
from apps.forms import CartItemForm, CartItemUpdateForm
from apps.i18n import get_lang, t
from apps.models import Cart, CartItem, Product, User

router = APIRouter(prefix="/cart", tags=["Cart"])


def _get_or_create_cart(session: Session, user_id: int) -> Cart:
    cart = session.exec(select(Cart).where(Cart.user_id == user_id)).first()
    if not cart:
        cart = Cart(user_id=user_id)
        session.add(cart)
        session.commit()
        session.refresh(cart)
    return cart


@router.get("/")
@router.get("", include_in_schema=False)
def get_cart(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    cart = _get_or_create_cart(session, current_user.id)
    items = session.exec(select(CartItem).where(CartItem.cart_id == cart.id)).all()
    return {"cart_id": cart.id, "user_id": current_user.id, "items": items}


@router.post("/items", status_code=201)
def add_to_cart(form: CartItemForm, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    if not session.get(Product, form.product_id):
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))
    cart = _get_or_create_cart(session, current_user.id)
    existing = session.exec(select(CartItem).where(CartItem.cart_id == cart.id, CartItem.product_id == form.product_id)).first()
    if existing:
        existing.quantity += form.quantity
        session.add(existing)
        session.commit()
        session.refresh(existing)
        return existing
    item = CartItem(cart_id=cart.id, product_id=form.product_id, quantity=form.quantity)
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.patch("/items/{item_id}")
@router.put("/items/{item_id}", include_in_schema=False)
def update_cart_item(item_id: int, form: CartItemUpdateForm, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    item = session.get(CartItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=t("cart_item_not_found", lang))
    cart = session.get(Cart, item.cart_id)
    if cart.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=t("not_your_cart", lang))
    item.quantity = form.quantity
    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@router.delete("/items/{item_id}")
def delete_cart_item(item_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    item = session.get(CartItem, item_id)
    if not item:
        raise HTTPException(status_code=404, detail=t("cart_item_not_found", lang))
    cart = session.get(Cart, item.cart_id)
    if cart.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=t("not_your_cart", lang))
    session.delete(item)
    session.commit()
    return {"message": t("deleted", lang)}


@router.delete("/clear")
def clear_cart(current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    cart = session.exec(select(Cart).where(Cart.user_id == current_user.id)).first()
    if not cart:
        return {"message": t("cart_empty", lang)}
    items = session.exec(select(CartItem).where(CartItem.cart_id == cart.id)).all()
    for it in items:
        session.delete(it)
    session.commit()
    return {"message": t("cart_cleared", lang)}
