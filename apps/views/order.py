"""
order.py — buyurtmalar
TZ 5.5: stock tekshiruvi, savatni tozalash, status admin only
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from apps.database import get_session
from apps.dependencies import get_current_user, require_admin
from apps.forms import OrderStatusForm
from apps.i18n import get_lang, t
from apps.models import Cart, CartItem, Order, OrderItem, Product, User

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("/", status_code=201)
@router.post("", status_code=201, include_in_schema=False)
async def create_order(current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    cart = session.exec(select(Cart).where(Cart.user_id == current_user.id)).first()
    if not cart:
        raise HTTPException(status_code=400, detail=t("cart_empty", lang))
    cart_items = session.exec(select(CartItem).where(CartItem.cart_id == cart.id)).all()
    if not cart_items:
        raise HTTPException(status_code=400, detail=t("cart_empty", lang))
    for ci in cart_items:
        prod = session.get(Product, ci.product_id)
        if not prod or prod.stock < ci.quantity:
            raise HTTPException(status_code=400, detail=t("insufficient_stock", lang, title=prod.title if prod else str(ci.product_id)))
    total = 0
    order = Order(user_id=current_user.id, status="pending", total_price=0)
    session.add(order)
    session.commit()
    session.refresh(order)
    for ci in cart_items:
        prod = session.get(Product, ci.product_id)
        oi = OrderItem(order_id=order.id, product_id=prod.id, quantity=ci.quantity, price_at_order=prod.price)
        session.add(oi)
        prod.stock -= ci.quantity
        session.add(prod)
        total += prod.price * ci.quantity
    order.total_price = total
    session.add(order)
    session.commit()
    for ci in cart_items:
        session.delete(ci)
    session.commit()
    session.refresh(order)
    return order


@router.get("/")
@router.get("", include_in_schema=False)
def list_orders(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    if current_user.role == "admin":
        return session.exec(select(Order)).all()
    return session.exec(select(Order).where(Order.user_id == current_user.id)).all()


@router.get("/{order_id}")
def get_order(order_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=t("order_not_found", lang))
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("not_your_order", lang))
    return order


@router.patch("/{order_id}/status")
def update_status(order_id: int, form: OrderStatusForm, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=t("order_not_found", lang))
    order.status = form.status
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


@router.delete("/{order_id}")
def cancel_order(order_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=t("order_not_found", lang))
    if order.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=t("not_your_order", lang))
    if order.status != "pending":
        raise HTTPException(status_code=400, detail=t("only_pending_can_cancel", lang))
    order.status = "cancelled"
    session.add(order)
    session.commit()
    return {"message": t("order_cancelled", lang)}
