"""
create_admin.py — admin (superuser) yaratish CLI

Ishlatish:
    python create_admin.py                 # interaktiv (savollab)
    python create_admin.py --username admin --password "KuchliParol123" --email admin@example.com --name "Admin"

Xavfsizlik: parol hech qachon logga yozilmaydi, faqat hash saqlanadi.
"""
import argparse
import getpass
import sys

from sqlmodel import Session, select

from apps.database import engine
from apps.models import User
from apps.utils import hash_password

MIN_PASSWORD_LEN = 8
MAX_PASSWORD_BYTES = 72


def _validate(db: Session, username: str, email: str) -> None:
    if db.exec(select(User).where(User.username == username)).first():
        sys.exit(f"Xatolik: '{username}' username allaqachon band.")
    if db.exec(select(User).where(User.email == email)).first():
        sys.exit(f"Xatolik: '{email}' email allaqachon band.")


def create_admin(name: str, username: str, email: str, password: str, role: str = "admin") -> User:
    if len(password) < MIN_PASSWORD_LEN:
        sys.exit(f"Xatolik: parol kamida {MIN_PASSWORD_LEN} ta belgidan iborat bo'lishi kerak.")
    if len(password.encode("utf-8")) > MAX_PASSWORD_BYTES:
        sys.exit(f"Xatolik: parol {MAX_PASSWORD_BYTES} baytdan uzun bo'lmasligi kerak.")
    if not username.strip() or not email.strip():
        sys.exit("Xatolik: username va email bo'sh bo'lmasligi kerak.")

    with Session(engine) as db:
        _validate(db, username.strip(), email.strip())
        user = User(
            name=name.strip() or username.strip(),
            username=username.strip(),
            email=email.strip(),
            password=hash_password(password),
            role=role,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


def main() -> None:
    p = argparse.ArgumentParser(description="OnlineShop — admin yaratish")
    p.add_argument("--username")
    p.add_argument("--password")
    p.add_argument("--email")
    p.add_argument("--name")
    p.add_argument("--role", default="admin", choices=["admin", "user"])
    args = p.parse_args()

    username = args.username or input("Username: ").strip()
    email = args.email or input("Email: ").strip()
    name = args.name or input("Ism: ").strip()
    # --password berilmasa — kiritish oynasi orqali so'raladi (tarixga yozilmaydi)
    password = args.password or getpass.getpass("Parol: ")
    if not args.password:
        again = getpass.getpass("Parolni yana kiriting: ")
        if password != again:
            sys.exit("Xatolik: parollar mos emas.")

    user = create_admin(name, username, email, password, args.role)
    print(f"Tayyor — rol: {user.role} | username: {user.username} | id: {user.id}")


if __name__ == "__main__":
    main()
