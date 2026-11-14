"""
mailer.py — SMTP orqali xabar yuborish (parol tiklash kodi)

SMTP sozlamalari .env da bo'lmasa yoki ulanish xato bo'lsa, modul
import bo'lganda xato tashlamaydi: `send_mail` False qaytaradi va
chaqiruvchi foydalanuvchiga "boshqa usulni ishlating" deb aytadi.

Har bir xabar uch matn mavjud: uz / ru / en.
"""
import logging
import smtplib
import ssl
from email.message import EmailMessage
from typing import Optional

from apps.config import (
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_STARTTLS,
    SMTP_USER,
)

log = logging.getLogger("onlineshop.mailer")

# Xabar matnlari: (mavzu, matn)
TEMPLATES = {
    "uz": (
        "OnlineShop — parol tiklash kodi",
        "Salom!\n\nSizning parol tiklash kodingiz: {code}\n\n"
        "Kod {minutes} daqiqa davomida amal qiladi. Agar bu so'rovni siz "
        "qilmagan bo'lsangiz, hech narsa qilmasligingiz mumkin.\n\n"
        "OnlineShop jamoasi",
    ),
    "ru": (
        "OnlineShop — код восстановления пароля",
        "Здравствуйте!\n\nВаш код восстановления пароля: {code}\n\n"
        "Код действителен {minutes} минут. Если вы не запрашивали смену "
        "пароля — просто проигнорируйте это письмо.\n\nКоманда OnlineShop",
    ),
    "en": (
        "OnlineShop — password reset code",
        "Hello!\n\nYour password reset code is: {code}\n\n"
        "The code is valid for {minutes} minutes. If you did not request "
        "this, you can safely ignore this email.\n\nThe OnlineShop team",
    ),
}

SUBJECTS = {
    "uz": "Parol tiklash kodi",
    "ru": "Код восстановления пароля",
    "en": "Password reset code",
}


def smtp_configured() -> bool:
    """SMTP sozlamalari to'liq bormi."""
    return bool(SMTP_HOST and SMTP_USER and SMTP_PASSWORD)


def send_mail(to: str, subject: str, body: str) -> bool:
    """Xabarni yuboradi. Muvaffaqiyat bo'lsa True, xatoda False."""
    if not smtp_configured():
        log.warning("SMTP sozlamalari to'liq emas — xabar yuborilmadi")
        return False

    msg = EmailMessage()
    msg["From"] = SMTP_FROM or SMTP_USER
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    try:
        if SMTP_PORT == 465:
            server: smtplib.SMTP = smtplib.SMTP_SSL(
                SMTP_HOST, SMTP_PORT, timeout=25,
                context=ssl.create_default_context(),
            )
        else:
            server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=25)
            if SMTP_STARTTLS:
                server.starttls(context=ssl.create_default_context())
        with server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        return True
    except Exception as exc:  # noqa: BLE001 — har qanday xato bilan qaytariladi
        log.warning("Email yuborilmadi (%s): %s", to, exc)
        return False


# def send_reset_code(to: str, code: str, lang: str = "uz", minutes: int = 10) -> bool:
#     """Parol tiklash kodini yuboradi."""
#     lang = lang if lang in TEMPLATES else "uz"
#     subject = SUBJECTS[lang]
#     body = TEMPLATES[lang][1].format(code=code, minutes=minutes)
#     return send_mail(to, subject, body)


def send_reset_code(to: str, code: str, lang: str = "uz", minutes: int = 10) -> bool:
    """Parol tiklash kodini yuboradi va terminalga chiqaradi."""
    lang = lang if lang in TEMPLATES else "uz"
    subject = SUBJECTS[lang]
    body = TEMPLATES[lang][1].format(code=code, minutes=minutes)

    # --- TEST UCHUN KODNI TERMINALGA CHIQARISH ---
    print("\n" + "=" * 50)
    print(f"🔑 PAROL TIKLASH KODI (Terminal): {code}")
    print(f"📧 Qabul qiluvchi: {to}")
    print("=" * 50 + "\n")
    # ---------------------------------------------

    # Terminalning o'zida sinash uchun True qaytaradi
    return True

    # Agar keyinchalik haqiqiy emailga jo'natishni xohlasangiz, yuqoridagi 'return True' ni
    # o'chirib, pastdagi izohdan olib tashlaysiz:
    # return send_mail(to, subject, body)