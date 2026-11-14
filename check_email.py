"""
check_email.py — SMTP sozlamalarini tekshirish va test xat yuborish.

Ishlatish:
    python check_email.py                # SMTP_USER ga test xat yuboradi
    python check_email.py siz@mail.com   # ko'rsatilgan manzilga yuboradi
    python check_email.py --login-only   # faqat login tekshiriladi (xat yuborilmaydi)

Parol hech qachon ekranga chiqarilmaydi.
"""
import argparse
import smtplib
import ssl
import sys
from email.message import EmailMessage

from apps.config import (
    SMTP_FROM,
    SMTP_HOST,
    SMTP_PASSWORD,
    SMTP_PORT,
    SMTP_STARTTLS,
    SMTP_USER,
)


def _mask(value: str) -> str:
    if not value:
        return "(bo'sh)"
    name, _, domain = value.partition("@")
    return f"{name[:2]}***@{domain}" if domain else f"{value[:2]}***"


def _connect():
    if SMTP_PORT == 465:
        return smtplib.SMTP_SSL(
            SMTP_HOST, SMTP_PORT, timeout=25, context=ssl.create_default_context()
        )
    server = smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=25)
    server.ehlo()
    if SMTP_STARTTLS:
        server.starttls(context=ssl.create_default_context())
        server.ehlo()
    return server


def _explain(exc: Exception) -> list[str]:
    """Keng tarqalgan Gmail/SMTP xatolarini o'zbekcha tushuntiradi."""
    text = str(exc)
    name = type(exc).__name__
    if isinstance(exc, smtplib.SMTPAuthenticationError) or "535" in text or "534" in text:
        return [
            "Gmail login rad etdi (535/534).",
            "Gmail uchun oddiy parol EMAS, App Password kerak:",
            "  1) myaccount.google.com → Security → 2-Step Verification ni yoqing.",
            "  2) App Passwords → yangi ilova paroli yarating (16 belgi).",
            "  3) .env: SMTP_PASSWORD=<16 belgili kod> (bo'shliqlarsiz).",
        ]
    if name == "SMTPServerDisconnected":
        return [
            "Gmail ulanishni yopdi — bu ko'pincha noto'g'ri parol yoki App Password",
            "ishlatilmaganini bildiradi.",
            "  1) 2-Step Verification yoqilganini tekshiring.",
            "  2) 16 belgili App Password yarating va .env ga yozing.",
            "  3) Agar parolni ko'chirganda bo'shliqlar tushgan bo'lsa, ularni olib tashlang.",
        ]
    if "550" in text or "5.7.1" in text:
        return [
            "From manzili Gmail tomonidan ruxsat etilmagan (550 5.7.1).",
            f"SMTP_FROM ({_mask(SMTP_FROM or SMTP_USER)}) va SMTP_USER ({_mask(SMTP_USER)})",
            "bir xil bo'lishi kerak (yoki Gmail'da 'Send mail as' sifatida tasdiqlangan bo'lsin).",
        ]
    if "timed out" in text.lower() or "timeout" in text.lower():
        return [
            "Serverga ulanish vaqti tugadi.",
            "Internet, firewall yoki provayderning 587-portni bloklanishini tekshiring.",
            "Muqobil: SMTP_PORT=465 (SSL) qilib ko'ring.",
        ]
    return ["Kutilmagan xato. Yuqoridagi xato matnini tekshiring."]


def main() -> None:
    parser = argparse.ArgumentParser(description="SMTP tekshiruvi")
    parser.add_argument("to", nargs="?", default=SMTP_USER, help="Qabul qiluvchi email")
    parser.add_argument("--login-only", action="store_true", help="Faqat login tekshirish")
    args = parser.parse_args()

    print("── SMTP sozlamalari ─────────────────────────")
    print("HOST      :", SMTP_HOST or "(bo'sh)")
    print("PORT      :", SMTP_PORT, "| STARTTLS:", SMTP_STARTTLS)
    print("USER      :", _mask(SMTP_USER))
    print("FROM      :", _mask(SMTP_FROM or SMTP_USER))
    print("PASSWORD  :", f"{len(SMTP_PASSWORD)} belgi" if SMTP_PASSWORD else "(bo'sh)")
    if not SMTP_HOST or not SMTP_USER or not SMTP_PASSWORD:
        print("\n❌ SMTP_HOST / SMTP_USER / SMTP_PASSWORD .env da to'liq emas.")
        sys.exit(1)
    if (SMTP_FROM or SMTP_USER).lower() != SMTP_USER.lower():
        print("\n⚠️  SMTP_FROM va SMTP_USER har xil — Gmail buni rad etishi mumkin.")
        print("    .env da SMTP_FROM ni SMTP_USER bilan bir xil qiling.")

    print("\n── Ulanish ──────────────────────────────────")
    try:
        server = _connect()
        print("✅ TLS ulanish OK")
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Ulanish xatosi: {type(exc).__name__}: {exc}")
        for line in _explain(exc):
            print("  ", line)
        sys.exit(1)

    try:
        # Gmail App Password ba'zan bo'shliqlar bilan ko'chiriladi — ularni olib tashlaymiz.
        server.login(SMTP_USER, SMTP_PASSWORD.replace(" ", ""))
        print("✅ Login OK")
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Login xatosi: {type(exc).__name__}: {exc}")
        for line in _explain(exc):
            print("  ", line)
        try:
            server.quit()
        except Exception:  # noqa: BLE001
            pass
        sys.exit(1)

    if args.login_only:
        print("\nLogin-only rejim: xat yuborilmadi.")
        server.quit()
        return

    print("\n── Test xat ─────────────────────────────────")
    msg = EmailMessage()
    msg["From"] = SMTP_FROM or SMTP_USER
    msg["To"] = args.to
    msg["Subject"] = "OnlineShop — SMTP test"
    msg.set_content(
        "Bu OnlineShop ilovasidan yuborilgan test xat.\n"
        "Agar buni ko'rsangiz, email sozlamalari to'g'ri ishlayapti."
    )
    try:
        server.send_message(msg)
        print(f"✅ Test xat yuborildi: {_mask(args.to)}")
        print("   Gmail'da 'Spam' papkasini ham tekshiring.")
    except Exception as exc:  # noqa: BLE001
        print(f"❌ Yuborish xatosi: {type(exc).__name__}: {exc}")
        for line in _explain(exc):
            print("  ", line)
        sys.exit(1)
    finally:
        try:
            server.quit()
        except Exception:  # noqa: BLE001
            pass


if __name__ == "__main__":
    main()
