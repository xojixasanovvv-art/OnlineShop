# OnlineShop API — Onlayn Do'kon Backend

To'liq funksional REST API + chiroyli frontend, JWT (Access+Refresh), 13 model, bot, MinIO S3, 3 til.

## Texnologiyalar
FastAPI 0.141, SQLModel 0.0.39, PostgreSQL 15, PyJWT 2.13, bcrypt 5.0, Uvicorn, Jinja2, httpx, MinIO 7.2.5, Docker Compose.

## Loyiha tuzilmasi
```
apps/
  config.py, database.py, models.py (13), forms.py, i18n.py, minio_client.py, bot.py
  views/auth, category, product, cart, order, payment, review, address, admin, wishlist, pages
templates/ (8 sahifa), static/style.css, static/i18n.js
locale/uz|ru|en.json (backend), PRESENTATION.md
```

## O'rnatish

```bash
cp .env.example .env  # BOT_TOKEN, ADMIN_TG_ID, MINIO_* ni to'ldiring
pip install -r requirements.txt
# yoki docker
docker-compose up --build  # http://127.0.0.1:8000/docs, minio http://localhost:9001
```

Local (docker siz):
```bash
uvicorn apps.views.main:app --reload
# admin yaratish
make admin  # yoki python create_admin.py
# test
pytest  # (qo'shilsa)
```

## .env.example
```
SECRET_KEY=...
DATABASE_URL=postgresql://postgres:1@localhost:5432/postgres
BOT_TOKEN=877...  # @BotFather
ADMIN_TG_ID=590...
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin
MINIO_BUCKET=onlineshop
```

## Email (parol tiklash kodi) sozlash

Gmail oddiy akkaunt paroli bilan SMTP'ga ruxsat bermaydi. Kerak:

1. `myaccount.google.com` → **Security** → **2-Step Verification** yoqiladi.
2. **App Passwords** → yangi parol yaratiladi (16 belgi).
3. `.env` ga yoziladi:
   ```
   SMTP_HOST=smtp.gmail.com
   SMTP_PORT=587
   SMTP_USER=sizning@gmail.com
   SMTP_PASSWORD=app-password-16-belgi
   SMTP_FROM=sizning@gmail.com   # SMTP_USER bilan bir xil bo'lsin
   SMTP_STARTTLS=true
   ```
4. Tekshirish: `python check_email.py` (yoki `make check-email`) — test xat yuboradi.
   Faqat loginni tekshirish: `python check_email.py --login-only`.

## Xavfsizlik qoidalari
- `.env` dagi `SECRET_KEY` bo'sh yoki namuna bo'lsa, dev rejimida vaqtinchalik tasodifiy kalit ishlatiladi; `APP_ENV=production` bo'lsa ilova ishga tushmaydi.
- Parol 8–72 bayt oralig'ida bo'lishi shart (bcrypt chegarasi).
- Yuklanadigan rasmlar faqat JPEG/PNG/WEBP/GIF (magic-bytes bo'yicha tekshiriladi): avatar/mahsulot 5 MB, to'lov cheki 10 MB.
- Foydalanuvchi kiritgan matn frontendda `innerHTML` ga qo'yishdan oldin `esc()` / `safeUrl()` orqali tozalanadi (`static/script.js`).

## API Endpointlar (Swagger /docs)
- Auth: `POST /auth/register`, `POST /auth/login`, `POST /auth/refresh`, `GET /auth/me`, `PATCH /auth/me`, `POST /auth/avatar`
- Category: `GET /categories`, `GET /{id}`, `POST/PUT/DELETE (admin)`
- Product: `GET /products?search&category_id&min/max_price&page&limit&sort_by&order`, `GET /{id}`, `POST/PUT/DELETE (admin)`, `POST /{id}/images`, `POST /{id}/upload`
- Cart: `GET /cart`, `POST /cart/items`, `PATCH /cart/items/{id}`, `DELETE /cart/items/{id}`, `DELETE /cart/clear`
- Order: `POST /orders`, `GET /orders`, `GET /{id}`, `PATCH /{id}/status (admin)`, `DELETE /{id}`
- Payment: `POST /orders/{id}/pay` (15m flashcard), `POST /orders/{id}/pay/screenshot`, `GET /orders/{id}/payment`, `GET /admin/payments`
- Review: `POST /products/{id}/reviews`, `GET /products/{id}/reviews`, `DELETE /reviews/{id}`
- Address: `GET/POST/PUT/DELETE /addresses`
- Wishlist: `GET /wishlist`, `POST /wishlist`, `DELETE /wishlist/{product_id}`
- Admin: `GET /admin/users`, `PATCH /admin/users/{id}/toggle-active`, `GET /admin/stats`
- Pages: `/`, `/login-page`, `/register-page`, `/cart-page`, `/pay-page`, `/wishlist-page`, `/product/{id}`, `/profile-page`, `/admin-page`

Barcha himoyalangan endpoint `Authorization: Bearer <access_token>` va `Accept-Language: uz|ru|en` header bilan.

## Frontend
`templates/base.html` navbar UZ/RU/EN toggle (`localStorage.lang`), `static/i18n.js` + `static/style.css` premium (`F8F7F4` + `Fraunces/Inter`).

## MinIO
`docker-compose.yml` da `minio:minio` `9000/9001`, bucket `onlineshop` public. `apps/minio_client.py` fallback `static/media`.

## Bot
`apps/bot.py` `httpx` `sendPhoto` file bilan, `ADMIN_TG_ID` ga order + to'lov cheki. Token bo'sh bo'lsa demo log.

## Litsenziya
MIT
