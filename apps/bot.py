"""
bot.py — Telegram bot orqali admin ga xabar yuborish
Faqat requests/httpx ishlatiladi, qo'shimcha kutubxona kerak emas.
BOT_TOKEN va ADMIN_TG_ID .env dan olinadi.
Website savatdan buyurtma berganda va to'lov screenshot yuborilganda
admin_id ga xabar boradi.
"""
import httpx
from apps.config import BOT_TOKEN, ADMIN_TG_ID

API = f"https://api.telegram.org/bot{BOT_TOKEN}" if BOT_TOKEN else None


async def _tg_request(method: str, payload: dict):
    if not BOT_TOKEN or not ADMIN_TG_ID:
        # .env da token yo'q bo'lsa logga chiqaramiz, xatolik bermaymiz (demo rejim)
        print(f"[BOT DEMO] {method} -> admin {ADMIN_TG_ID}: {payload.get('text') or payload.get('caption','')[:200]}")
        return None
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.post(f"{API}/{method}", json=payload)
            # r.json() da ok boolean
            if r.status_code != 200:
                print(f"[BOT ERROR] {r.text}")
            return r.json()
    except Exception as e:
        print(f"[BOT ERROR] {e}")
        return None


async def send_order_notification(order, user, items: list):
    """Savatdan buyurtma yaratilganda admin ga yuboriladi"""
    text = (
        f"🛒 *Yangi buyurtma!* #{order.id}\n"
        f"👤 {user.name} (@{user.username}) • {user.email}\n"
        f"💰 Jami: {order.total_price:,.0f} so'm\n"
        f"📦 Mahsulotlar:\n"
    )
    for it in items:
        text += f"  • {it['title']} ×{it['quantity']} = {it['total']:,.0f} so'm\n"
    text += f"\nStatus: {order.status} • /orders/{order.id}"
    if not ADMIN_TG_ID or not BOT_TOKEN:
        print(f"[BOT DEMO] Order #{order.id} -> admin {ADMIN_TG_ID or 'NOT_SET'}: {text[:500]}")
        return
    await _tg_request("sendMessage", {
        "chat_id": ADMIN_TG_ID,
        "text": text,
        "parse_mode": "Markdown"
    })


async def send_payment_proof(payment, order, user, screenshot_url: str | None = None):
    """User screenshot yuklaganda admin ga yuboriladi, 15 min ichida — rasm fayl bo'lib yuboriladi (localhost URL Telegram ko'ra olmaydi)"""
    import os
    caption = (
        f"💳 *To'lov cheki* #{payment.id}\n"
        f"Buyurtma #{order.id} • {order.total_price:,.0f} so'm\n"
        f"👤 {user.name} (@{user.username})\n"
        f"Karta: {payment.demo_card.card_number if hasattr(payment,'demo_card') and payment.demo_card else payment.demo_card_id}\n"
        f"Status: {payment.status}\n"
    )
    if screenshot_url and screenshot_url.startswith("/static/"):
        file_path = screenshot_url.lstrip("/")
        if os.path.exists(file_path):
            if not BOT_TOKEN or not ADMIN_TG_ID:
                print(f"[BOT DEMO] sendPhoto file {file_path} -> admin {ADMIN_TG_ID or 'NOT_SET'}: {caption[:200]}")
                return None
            try:
                async with httpx.AsyncClient(timeout=15) as client:
                    with open(file_path, "rb") as f:
                        files = {"photo": (os.path.basename(file_path), f, "image/jpeg")}
                        data = {"chat_id": ADMIN_TG_ID, "caption": caption, "parse_mode": "Markdown"}
                        r = await client.post(f"{API}/sendPhoto", data=data, files=files)
                        if r.status_code != 200:
                            print(f"[BOT ERROR] sendPhoto file {r.text}")
                        else:
                            print(f"[BOT] screenshot yuborildi #{payment.id}")
                        return r.json() if r.status_code==200 else None
            except Exception as e:
                print(f"[BOT ERROR] sendPhoto file {e}")
                return None
        # fayl topilmasa URL fallback
    if screenshot_url:
        # http URL bo'lsa yoki lokal fayl topilmasa — URL bilan yuborish (demo)
        photo_url = screenshot_url if screenshot_url.startswith("http") else f"http://127.0.0.1:8000{screenshot_url}"
        return await _tg_request("sendPhoto", {
            "chat_id": ADMIN_TG_ID,
            "photo": photo_url,
            "caption": caption,
            "parse_mode": "Markdown"
        })
    else:
        return await _tg_request("sendMessage", {
            "chat_id": ADMIN_TG_ID,
            "text": caption,
            "parse_mode": "Markdown"
        })


async def send_payment_verified(payment, order):
    """Pul tushgani tasdiqlanganda admin ga yakuniy xabar"""
    text = f"✅ *To'lov tasdiqlandi!* Buyurtma #{order.id} • {payment.amount:,.0f} so'm • Payment #{payment.id} ✅\nDemo karta balansi yangilandi."
    await _tg_request("sendMessage", {
        "chat_id": ADMIN_TG_ID,
        "text": text,
        "parse_mode": "Markdown"
    })
