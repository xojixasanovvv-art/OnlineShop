# OnlineShop — To'liq Prezentatsiya

## 1. Loyiha haqida
**OnlineShop API** — foydalanuvchi ro'yxatdan o'tib, mahsulotlarni ko'rib, savatga qo'shib, buyurtma va to'lov (15 daq flashcard + screenshot) qila oladigan, admin panel, Telegram bot va 3 tilda (UZ/RU/EN) ishlaydigan real darajadagi e-commerce backend + frontend.

- **Maqsad:** sertifikat himoyasi uchun “real” loyiha — JWT, relatsiyalar, rollar, CRUD, bot, MinIO.
- **Foydalanuvchi rollari:** `user` (xaridor), `admin` (boshqaruv).
- **Asosiy oqim:** `Ro'yxatdan o'tish → Login → Mahsulot tanlash → Savat → /pay-page da Buyurtma (stock tekshiruv) → 15 daq karta flashcard → Chek screenshot → Demo balans tekshiruvi → Admin TG ga xabar → Tasdiq → paid`.

## 2. Texnologiyalar Stack
| Qatlam | Texnologiya | Versiya | Izoh |
|---|---|---|---|
| Backend | **FastAPI** | 0.141.1 | APIRouter, Swagger /docs |
| ORM | **SQLModel** (SQLAlchemy 2.0.52) | 0.0.39 | 12 ta model, Relationship |
| DB | **PostgreSQL** | 15 | psycopg2-binary |
| Auth | **PyJWT** + **bcrypt** | 2.13 / 5.0 | Access 30m, Refresh 7d |
| Validatsiya | **Pydantic** 2.13 + **email-validator** | - | forms.py |
| Server | **Uvicorn** | 0.52.4 | --reload |
| Frontend | **Jinja2** + **Vanilla JS** | 3.1.6 | data-i18n, fetch wrapper |
| Bot | **httpx** | 0.28.1 | Telegram Bot API (sendMessage/sendPhoto) |
| Storage | **MinIO** (S3) | latest | minio-py, docker-compose |
| Konteyner | **Docker Compose** | - | app + db + minio |
| Til | **i18n** | - | backend `locale/*.json`, frontend `static/i18n.js` |

## 3. Loyiha tuzilmasi
```
OnlineShop/
├── apps/
│   ├── config.py          # .env dan SECRET_KEY, DB, BOT_TOKEN, MINIO
│   ├── database.py        # engine, get_session, create_db_and_tables
│   ├── models.py          # 12 model (User..Payment)
│   ├── forms.py           # Pydantic sxemalar
│   ├── i18n.py           # backend t() + get_lang (Accept-Language / ?lang)
│   ├── minio_client.py    # S3 upload/get_url (yangi)
│   ├── bot.py             # Telegram sendOrder/sendPaymentProof
│   └── views/
│       ├── main.py        # FastAPI app, lifespan, include_router
│       ├── auth.py        # /auth/*, avatar file/S3
│       ├── category.py    # /categories CRUD
│       ├── product.py     # /products + /images + /upload (S3)
│       ├── cart.py        # /cart
│       ├── order.py       # POST /orders (stock, tozalash)
│       ├── payment.py     # /orders/{id}/pay + /screenshot (S3) + /admin/payments
│       ├── review.py      # /products/{id}/reviews (faqat sotib olgan)
│       ├── address.py     # /addresses
│       ├── admin.py       # /admin/users, /stats
│       └── pages.py       # /, /login-page, /pay-page, /admin-page
├── locale/                # backend uz.json, ru.json, en.json (detail tarjimalari)
├── static/
│   ├── style.css          # premium editorial (F8F7F4, Fraunces+Inter, 14px radius)
│   ├── i18n.js            # toggle UZ/RU/EN, fetch Accept-Language
│   └── script.js          # navbar, cart badge, toast
├── templates/             # 8 ta Jinja2 sahifa (index, product_detail, cart, pay, profile, admin, login, register)
├── docker-compose.yml     # postgres + minio + app (MinIO bilan)
└── requirements.txt
```

## 4. Ma'lumotlar bazasi — 12 model (`apps/models.py:15`)
1. **User** `id, name, username unique, email unique, password hash, role, is_active, created_at, avatar_url`
2. **Category** `id, name unique, description, parent_id self-ref`
3. **Product** `id, title, description, price, stock, category_id, created_at` + `images, reviews`
4. **ProductImage** `id, image_url (S3 /static/media), product_id`
5. **Cart** `id, user_id unique`
6. **CartItem** `id, cart_id, product_id, quantity`
7. **Order** `id, user_id, status pending|paid|shipped|delivered|cancelled, total_price, created_at`
8. **OrderItem** `id, order_id, product_id, quantity, price_at_order`
9. **Review** `id, user_id, product_id, rating 1-5, comment, created_at`
10. **Address** `id, user_id, country, city, street, zip_code`
11. **DemoCard** `id, card_number unique, card_holder, balance, is_active` — to'lov tekshiruvi uchun
12. **Payment** `id, order_id unique, user_id, demo_card_id, amount, status pending|verified|expired|rejected, screenshot_url (S3), expires_at +15m`

Relatsiyalar `Relationship(cascade_delete=True)` bilan, `Field(index=True)` optimizatsiya.

## 5. API — 35+ endpoint (Swagger /docs)
- **Auth** `POST /auth/register (409)`, `POST /auth/login (401)`, `POST /auth/refresh`, `GET /auth/me`, `PATCH /auth/me`, `POST /auth/avatar` (file/S3) — `apps/views/auth.py:20`
- **Category** `GET /categories, GET /{id}, POST/PUT/DELETE (admin)` — `category.py:17`
- **Product** `GET /products?search&category_id&min/max_price&page&limit&sort_by&order`, `GET /{id}`, `POST/PUT/DELETE (admin)`, `POST /{id}/images`, `POST /{id}/upload` (S3) — `product.py:34`
- **Cart** `GET /cart, POST /cart/items, PATCH /cart/items/{id}, DELETE /cart/items/{id}, DELETE /cart/clear` — `cart.py:17`
- **Order** `POST /orders` (stock tekshiruvi, savat tozalash, TG pending emas), `GET /orders, GET /{id}, PATCH /{id}/status (admin), DELETE /{id}` — `order.py:17`
- **Payment** `POST /orders/{id}/pay (15m flashcard)`, `POST /{id}/pay/screenshot (S3 + TG file)`, `GET /orders/{id}/payment`, `GET /admin/payments`, `POST /admin/payments/{id}/verify|reject` — `payment.py:17`
- **Review** `POST /products/{id}/reviews (faqat sotib olgan)`, `GET /reviews, DELETE /reviews/{id}` — `review.py:17`
- **Address** `GET/POST/PUT/DELETE /addresses` — `address.py:17`
- **Admin** `GET /admin/users, PATCH /toggle-active, GET /admin/stats` — `admin.py:17`
- **Pages** `GET /, /login-page, /register-page, /profile-page, /cart-page, /pay-page (full pay), /product/{id}, /admin-page` — `pages.py:12`

Barcha himoyalangan endpoint `HTTPBearer` + `get_current_user` + `require_admin (403)`, `t(key, lang)` orqali `Accept-Language: uz|ru|en` yoki `?lang` bo'yicha `locale/*.json` dan tarjima.

## 6. Frontend — premium, toggle 3 til
- **Dizayn:** `static/style.css:1` `F8F7F4 / 0F1215 / 8B95A5 / E6E8EB`, `Fraunces 600` + `Inter`, `14px` radius, `74px` blur navbar, hero `58px` editorial + `hero-visual` rasm overlay, card `272px` hover `-4px + scale 1.04`, `fadeIn` stagger, `14px` form `focus 3px` ring — bachkana yashil/emoji yo'q.
- **i18n:** `static/i18n.js:1` `translations{uz,ru,en} 113 kalit`, `data-i18n` + `data-i18n-placeholder`, `localStorage.lang`, `setLang()` + `window.fetch` wrap `Accept-Language: currentLang` ni backendga yuboradi, `navbar UZ/RU/EN` toggle `active` qora pill.
- **Sahifalar:** `index` filter/search/sort/pagination, `product_detail` rasm+sharx, `cart` faqat ko'rish + `Savatdan davom etish → /pay-page`, `pay` flashcard `flashcard-new` gradient + chip + `Copy` + `15:00` `pulse` + screenshot preview, `profile` avatar file/URL preview, `admin` 4 tab + stats.

## 7. Telegram bot — `apps/bot.py:1`
- `BOT_TOKEN=8774562050:AAEi...` + `ADMIN_TG_ID=5903694556` `.env:6` da.
- `POST /orders/` endi darhol yubormaydi (user talabi) — faqat `POST /orders/{id}/pay/screenshot` da `send_payment_proof()` `sendPhoto` **fayl** (`open(static/media/payments/xxx.jpg)`) bilan yuboriladi, `DemoCard.balance >= amount` bo'lsa avtomatik `verified` va `send_payment_verified()`. Avval `curl getMe` → `onlineshop247bot` tasdiqlandi, `chat not found` uchun admin `/start` bosishi kerak. Token bo'sh bo'lsa `[BOT DEMO]` console.

## 8. MinIO — S3 Object Storage (yangi)
- **Nima uchun:** `static/media` o'rniga cheksiz, konteynerda yo'qolmaydigan, presigned URL, public bucket.
- **Sozlama:** `.env` `MINIO_ENDPOINT=localhost:9000`, `MINIO_ACCESS_KEY=minioadmin`, `MINIO_SECRET_KEY=minioadmin`, `MINIO_BUCKET=onlineshop`, `MINIO_SECURE=false`.
- **Kli ent:** `apps/minio_client.py` `Minio(...)`, `ensure_bucket()`, `upload_file(file, key) -> url`, `get_presigned_url()`. `requirements.txt` `minio`.
- **Docker:** `docker-compose.yml` `minio:minio` `9000:9000 9001:9001` + `mc` bucket create, `app` `depends_on: minio` va `MINIO_ENDPOINT=minio:9000`.
- **Integratsiya:** `product.py` `/upload`, `auth.py` `/avatar`, `payment.py` `/screenshot` avval `MinIO` ga urinadi, `MINIO_ENDPOINT` bo'sh yoki xato bo'lsa fallback `static/media` ga saqlaydi — shuning uchun ham `GET /static/...` ham `S3 URL` ham ishlaydi. Admin TG ga yuborishda ham S3 URL yoki lokal fayl bo'lsa `open()` bilan yuboriladi.

## 9. Multilanguage — backend + frontend
- **Backend:** `apps/i18n.py` `get_lang(Request, ?lang)` → `Accept-Language` header, `t(key, lang)` `locale/*.json` dan. Barcha `detail` lar `t("username_taken", lang)` kabi. Frontend toggle `Accept-Language` header yuboradi, `TestClient` `Accept-Language: ru → Неверный логин...` tasdiqlandi.
- **Frontend:** yuqoridagi `i18n.js` toggle.

## 10. Ishga tushirish
```bash
cp .env.example .env  # BOT_TOKEN, ADMIN_TG_ID, MINIO_* ni to'ldiring
pip install -r requirements.txt
# yoki docker
docker-compose up --build
# local
uvicorn apps.views.main:app --reload  # http://127.0.0.1:8000/docs, /admin-page (admin/admin123)
```
MinIO console `http://localhost:9001` (minioadmin/minioadmin), bucket `onlineshop` public.

## 11. Xulosa
Loyiha TZ 10 model + JWT + rol + 35+ endpoint + bot + 15 daq to'lov + 3 til + MinIO + Docker bilan to'liq “real” e-commerce. Kod DRY (APIRouter, get_session, i18n), Swagger da har endpoint `TRY`, frontend premium va responsive, TG xabarlar faqat screenshot dan keyin, MinIO bilan rasm yo'qolmaydi.
