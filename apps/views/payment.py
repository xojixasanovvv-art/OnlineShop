"""
payment.py — flashcard + 15 min + screenshot + demo karta tekshiruvi + TG bot + MinIO
"""
import os
import uuid
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlmodel import Session, select
from apps.bot import send_payment_proof, send_payment_verified
from apps.database import get_session
from apps.dependencies import get_current_user, require_admin
from apps.i18n import get_lang, t
from apps.minio_client import upload_bytes
from apps.models import Order, User, DemoCard, Payment
from apps.uploads import MAX_SCREENSHOT_BYTES, validate_image

router = APIRouter(tags=["Payments"])

def ensure_demo_cards(session: Session):
    if session.exec(select(DemoCard)).first():
        return
    cards = [
        DemoCard(card_number="8600 1234 5678 9012", card_holder="OnlineShop Demo", balance=50_000_000),
        DemoCard(card_number="8600 1111 2222 3333", card_holder="Demo UzCard", balance=20_000_000),
        DemoCard(card_number="8600 9999 8888 7777", card_holder="Demo Humo", balance=5_000_000),
    ]
    for c in cards:
        session.add(c)
    session.commit()

@router.get("/payments/cards")
def list_demo_cards(session: Session = Depends(get_session)):
    ensure_demo_cards(session)
    return session.exec(select(DemoCard).where(DemoCard.is_active==True)).all()

@router.post("/payments/cards", status_code=201)
def create_demo_card(card_number: str, balance: float = 10_000_000, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    if session.exec(select(DemoCard).where(DemoCard.card_number==card_number)).first():
        raise HTTPException(status_code=409, detail=t("card_already_exists", lang))
    card = DemoCard(card_number=card_number, balance=balance)
    session.add(card)
    session.commit()
    session.refresh(card)
    return card

@router.post("/orders/{order_id}/pay")
async def create_payment(order_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user), lang: str = Depends(get_lang)):
    order = session.get(Order, order_id)
    if not order:
        raise HTTPException(status_code=404, detail=t("order_not_found", lang))
    if order.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("not_your_order", lang))
    if order.status != "pending":
        raise HTTPException(status_code=400, detail=t("only_pending_payment", lang))
    existing = session.exec(select(Payment).where(Payment.order_id==order_id)).first()
    if existing:
        if existing.expires_at > datetime.utcnow() and existing.status=="pending":
            card = session.get(DemoCard, existing.demo_card_id)
            return {"payment_id": existing.id, "card_number": card.card_number, "card_holder": card.card_holder, "amount": existing.amount, "expires_at": existing.expires_at, "status": existing.status}
        else:
            session.delete(existing)
            session.commit()
    ensure_demo_cards(session)
    card = session.exec(select(DemoCard).where(DemoCard.is_active==True).order_by(DemoCard.balance.desc())).first()
    if not card:
        raise HTTPException(status_code=500, detail=t("demo_card_not_found", lang))
    expires = datetime.utcnow() + timedelta(minutes=15)
    payment = Payment(order_id=order.id, user_id=current_user.id, demo_card_id=card.id, amount=order.total_price, status="pending", expires_at=expires)
    session.add(payment)
    session.commit()
    session.refresh(payment)
    return {"payment_id": payment.id, "card_number": card.card_number, "card_holder": card.card_holder, "amount": payment.amount, "expires_at": payment.expires_at, "status": payment.status, "message": "15 daqiqa ichida to'lang"}

@router.get("/orders/{order_id}/payment")
def get_payment(order_id: int, session: Session = Depends(get_session), current_user: User = Depends(get_current_user), lang: str = Depends(get_lang)):
    payment = session.exec(select(Payment).where(Payment.order_id==order_id)).first()
    if not payment:
        raise HTTPException(status_code=404, detail=t("payment_not_found", lang))
    order = session.get(Order, order_id)
    if payment.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("permission_denied", lang))
    if payment.status=="pending" and payment.expires_at < datetime.utcnow():
        payment.status="expired"
        session.add(payment)
        session.commit()
        session.refresh(payment)
    card = session.get(DemoCard, payment.demo_card_id)
    return {"id": payment.id, "order_id": payment.order_id, "amount": payment.amount, "status": payment.status, "card_number": card.card_number if card else None, "card_holder": card.card_holder if card else None, "expires_at": payment.expires_at, "screenshot_url": payment.screenshot_url, "created_at": payment.created_at}

@router.post("/orders/{order_id}/pay/screenshot")
async def upload_screenshot(order_id: int, file: UploadFile = File(...), session: Session = Depends(get_session), current_user: User = Depends(get_current_user), lang: str = Depends(get_lang)):
    payment = session.exec(select(Payment).where(Payment.order_id==order_id)).first()
    if not payment:
        raise HTTPException(status_code=404, detail=t("payment_not_started", lang))
    if payment.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=t("not_your_payment", lang))
    if payment.status != "pending":
        raise HTTPException(status_code=400, detail=t("payment_status_invalid", lang, status=payment.status))
    if payment.expires_at < datetime.utcnow():
        payment.status="expired"
        session.add(payment)
        session.commit()
        raise HTTPException(status_code=400, detail=t("payment_expired", lang))
    # Chek ham faqat haqiqiy rasm bo'lishi va hajm chegarasiga sig'ishi kerak.
    data = await file.read(MAX_SCREENSHOT_BYTES + 1)
    mime, ext = validate_image(data, MAX_SCREENSHOT_BYTES, lang)
    key = f"payments/{order_id}_{uuid.uuid4().hex}{ext}"
    url = upload_bytes(data, key, content_type=mime)
    if not url:
        os.makedirs("static/media/payments", exist_ok=True)
        filename = f"{order_id}_{uuid.uuid4().hex}{ext}"
        path = os.path.join("static/media/payments", filename)
        with open(path, "wb") as f:
            f.write(data)
        url = f"/static/media/payments/{filename}"
    payment.screenshot_url = url
    session.add(payment)
    session.commit()
    session.refresh(payment)
    order = session.get(Order, order_id)
    card = session.get(DemoCard, payment.demo_card_id)
    payment.demo_card = card
    await send_payment_proof(payment, order, current_user, payment.screenshot_url)
    if card.balance >= payment.amount:
        card.balance -= payment.amount
        payment.status = "verified"
        order.status = "paid"
        session.add(card)
        session.add(payment)
        session.add(order)
        session.commit()
        await send_payment_verified(payment, order)
        return {"message": "Chek yuklandi va to'lov tasdiqlandi ✅", "payment": get_payment(order_id, session, current_user, lang), "verified": True}
    else:
        return {"message": "Chek yuklandi, admin tekshiradi ⏳", "payment": get_payment(order_id, session, current_user, lang), "verified": False}

@router.get("/admin/payments")
def list_payments(session: Session = Depends(get_session), admin: User = Depends(require_admin)):
    return session.exec(select(Payment).order_by(Payment.created_at.desc())).all()

@router.post("/admin/payments/{payment_id}/verify")
async def admin_verify(payment_id: int, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail=t("payment_not_found", lang))
    if payment.status == "verified":
        return {"message": t("verified", lang)}
    order = session.get(Order, payment.order_id)
    card = session.get(DemoCard, payment.demo_card_id)
    if card.balance < payment.amount:
        raise HTTPException(status_code=400, detail=t("insufficient_balance", lang))
    card.balance -= payment.amount
    payment.status = "verified"
    order.status = "paid"
    session.add(card); session.add(payment); session.add(order)
    session.commit()
    await send_payment_verified(payment, order)
    return {"message": t("verified", lang), "payment_id": payment.id}

@router.post("/admin/payments/{payment_id}/reject")
def admin_reject(payment_id: int, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    payment = session.get(Payment, payment_id)
    if not payment:
        raise HTTPException(status_code=404, detail=t("payment_not_found", lang))
    payment.status = "rejected"
    session.add(payment)
    session.commit()
    return {"message": t("rejected", lang)}
