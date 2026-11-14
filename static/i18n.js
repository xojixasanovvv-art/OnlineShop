// i18n.js — 3 tilda (UZ/RU/EN) — data-i18n bilan ishlaydi
const translations = {
  uz: {
    // navbar
    "nav.products": "Mahsulotlar",
    "nav.cart": "Savat",
    "nav.profile": "Profil",
    "nav.admin": "Admin",
    "nav.login": "Kirish",
    "nav.register": "Ro'yxatdan o'tish",
    "nav.logout": "Chiqish",
    // hero
    "hero.eyebrow": "★ Yangi kolleksiya • 2026",
    "hero.title": "Kerakli narsangizni <em>bir joyda</em> toping",
    "hero.desc": "Telefon, aksessuar va minglab mahsulotlar — filtr, qidiruv va tezkor yetkazib berish bilan.",
    "hero.btn": "Xaridni boshlash →",
    "hero.note": "500+ mamnun mijozlar",
    "hero.card_label": "Tez yetkazib berish",
    "hero.card_value": "24 soat ichida",
    "hero.card_desc": "Toshkent bo'ylab bepul yetkazib berish",
    // filter
    "filter.search": "Qidiruv — masalan: iPhone",
    "filter.allCat": "Barcha kategoriyalar",
    "filter.newest": "Yangi birinchi",
    "filter.price": "Narx bo'yicha",
    "filter.desc": "Kamayish",
    "filter.asc": "O'sish",
    "filter.min": "Min narx",
    "filter.max": "Max narx",
    "filter.clear": "Tozalash",
    // products
    "products.title": "Barcha mahsulotlar",
    "products.empty": "Hech narsa topilmadi. Filtrlarni tozalab ko'ring.",
    "products.add": "Savatga +",
    "products.detail": "Batafsil",
    "products.stock": "dona qoldi",
    "products.out": "Tugadi",
    "products.noDesc": "Tavsif yo'q",
    // auth
    "auth.login_title": "Kirish",
    "auth.login_sub": "Hisobingizga kirish uchun ma'lumotlarni kiriting",
    "auth.login_btn": "Kirish",
    "auth.login_noacc": "Hisobingiz yo'qmi?",
    "auth.register_title": "Ro'yxatdan o'tish",
    "auth.register_sub": "Bir necha soniyada hisob yarating",
    "auth.register_btn": "Ro'yxatdan o'tish",
    "auth.hasAcc": "Hisobingiz bormi?",
    "auth.name": "Ism",
    "auth.username": "Username yoki email",
    "forgot.loginHint": "Endi kirish sahifasida username yoki email bilan kiring.",
    "auth.usernamePh": "ake yoki email@onlineshop.uz",
    "auth.email": "Email",
    "auth.password": "Parol",
    "auth.brand_login": "Qaytganingizdan xursandmiz",
    "auth.brand_login_p": "Hisobingizga kiring va buyurtmalaringizni, savatingizni davom ettiring.",
    "auth.brand_reg": "Xarid qilishni hoziroq boshlang",
    "auth.brand_reg_p": "Ro'yxatdan o'ting va minglab mahsulotlarga kirish huquqiga ega bo'ling.",
    // profile
    "profile.title": "Profil",
    "profile.info": "Shaxsiy ma'lumotlar",
    "profile.edit": "Profilni tahrirlash",
    "profile.save": "Saqlash",
    "profile.addrs": "Manzillarim",
    "profile.orders": "Buyurtmalarim",
    "profile.avatar_url": "Avatar URL (ixtiyoriy)",
    "profile.avatar_file": "Yoki fayl yuklash",
    // cart
    "cart.title": "Savat",
    "cart.desc": "Mahsulotlarni tekshiring — keyin to'lov sahifasiga o'ting",
    "cart.clear": "Savatni tozalash",
    "cart.continue": "Savatdan davom etish →",
    "cart.continue_hint": "Davom etish tugmasi sizni to'liq to'lov sahifasiga olib boradi — u yerda buyurtma tekshirilib yaratiladi.",
    "cart.empty": "Savat bo'sh.",
    "cart.toProducts": "Mahsulotlarga qaytish",
    // pay
    "pay.title": "To'lov sahifasi",
    "pay.back": "← Savatga qaytish",
    "pay.desc": "Buyurtmani tekshiring, keyin to'lovni amalga oshiring. 15 daqiqada chek yuklanmasa bekor bo'ladi.",
    "pay.cart": "Savat tarkibi",
    "pay.total": "Jami",
    "pay.orderBtn": "Buyurtma berish — tekshirish bilan →",
    "pay.order_checking": "Tekshirilmoqda...",
    "pay.flash": "DEMO UZCARD / HUMO • FLASHCARD",
    "pay.demo_note": "Demo karta — baza da balans bor, website avtomatik tekshiradi va admin TG ga yuboradi.",
    "pay.upload_title": "Chekni yuklang (screenshot)",
    "pay.upload_desc": "Kartaga pul tashlagach, chek rasmini yuklang. Rasm darhol admin TG ga boradi va demo balans tekshiriladi.",
    "pay.send": "Yuborish",
    "pay.placeholder": "Buyurtma berilgach bu yerda karta va 15 daqiqa taymer chiqadi.",
    // product detail
    "pd.back": "← Barcha mahsulotlar",
    "pd.reviews": "Sharhlar",
    "pd.add_review": "Sharh qoldirish",
    "pd.review_hint": "Faqat sotib olgan foydalanuvchilar sharh qoldira oladi",
    "pd.rating": "Reyting (1-5)",
    "pd.comment": "Izoh",
    "pd.send": "Yuborish",
    "pd.add_to_cart": "Savatga qo'shish 🛒",
    "pd.view_cart": "Savatni ko'rish",
    // admin
    "admin.title": "Admin Panel",
    "admin.only": "faqat admin",
    "admin.users": "Foydalanuvchilar",
    "admin.orders": "Buyurtmalar",
    "admin.revenue": "Jami savdo",
    "admin.products": "Mahsulotlar",
    "admin.categories": "Kategoriyalar",
    "admin.payments": "To'lovlar",
    "admin.newCat": "Yangi kategoriya",
    "admin.newProd": "Yangi mahsulot qo'shish",
    "admin.editProd": "Tahrirlash",
    "admin.ph_title": "iPhone 15 Pro",
    "admin.ph_desc": "Qisqa tavsif",
    "admin.ph_cat_name": "Telefonlar",
    "admin.ph_cat_desc": "Tavsif (ixtiyoriy)",
    "profile.ph_country": "Uzbekistan",
    "profile.ph_city": "Tashkent",
    "profile.ph_street": "Ko'cha",
    "profile.ph_zip": "Pochta indeksi",
    "pd.ph_comment": "Mahsulot haqida fikringiz",
    // footer
    "footer.copy": "© 2026 OnlineShop — FastAPI • SQLModel • JWT",
    // generic
    // wishlist
    "wishlist.nav": "Sevimlilar",
    "wishlist.title": "Sevimlilar",
    "wishlist.desc": "Yurak bosgan mahsulotlaringiz",
    "wishlist.add": "Sevimlilarga qo'shish",
    "wishlist.remove": "Sevimlilardan olib tashlash",
    "wishlist.added": "Sevimlilarga qo'shildi",
    "wishlist.removed": "Sevimlilardan olib tashlandi",
    "wishlist.empty": "Hozircha sevimli mahsulot yo'q. Yurakni bosing!",
    "wishlist.clear": "Tozalash",
    "wishlist.cleared": "Sevimlilar tozalandi",
    "wishlist.confirm_clear": "Barcha sevimlilar o'chirilsinmi?",
    "common.error": "Xatolik",
    "common.network": "Serverga ulanib bolmadi",
    "auth.session_expired": "Sessiya tugadi, qayta kiring",
    "btn.add": "Qo'shish",
    "btn.edit": "Tahrirlash",
    "btn.delete": "O'chirish",
    "btn.save": "Saqlash",
    "btn.cancel": "Bekor",
    "btn.refresh": "Yangilash",
    "common.loading": "Yuklanmoqda...",
    "common.no": "Hozircha yo'q",
    // common
    "common.sum": "so'm",
    "common.pcs": "dona",
    "common.customer": "Xaridor",
    "common.failure": "Xatolik",
    "common.items": "ta",
    "cart.total": "Jami:",
    // admin
    "admin.noCatFirst": "Avval kategoriya qo'shing",
    "admin.noCats": "Kategoriya yo'q",
    "admin.noProds": "Hozircha mahsulot yo'q",
    "admin.noOrders": "Buyurtma yo'q",
    "admin.noUsers": "Foydalanuvchi yo'q",
    "admin.noPays": "To'lov yo'q",
    "admin.noShot": "Screenshot yo'q",
    "admin.nameLbl": "Nomi",
    "admin.descLbl": "Tavsif",
    "admin.priceLbl": "Narxi",
    "admin.stockLbl": "Ombordagi soni",
    "admin.catLbl": "Kategoriya",
    "admin.listTitle": "Mahsulotlar ro'yxati",
    "admin.added": "Qo'shildi",
    "admin.updated": "Yangilandi",
    "admin.editing": "Tahrirlash",
    "admin.statusLbl": "Status",
    // profile
    "profile.noAddr": "Manzil yo'q",
    "profile.noOrders": "Hozircha buyurtma yo'q",
    // product
    "pd.notFound": "Mahsulot topilmadi",
    "pd.noReviews": "Hozircha sharh yo'q",
    "pd.reviewAdded": "Sharh qo'shildi",
    // pay
    "pay.orderWord": "Buyurtma",
    "pay.statusLbl": "Status",
    // order/payment status
    "st.pending": "Kutilmoqda",
    "st.paid": "To'landi",
    "st.shipped": "Yuborilgan",
    "st.delivered": "Yetkazilgan",
    "st.cancelled": "Bekor qilingan",
    "st.verified": "Tasdiqlangan",
    // admin qo'shimcha
    "products.fallback": "Mahsulot",
    "st.expired": "Muddati tugagan",
    "pd.redirecting": "bosh sahifaga o'tkazilmoqda...",
    "pd.addedToCart": "Savatga qo'shildi",
    "profile.savedMsg": "Saqlandi",
    "profile.savedToast": "Profil yangilandi",
    "profile.addrAdded": "Manzil qo'shildi",
    "admin.paymentsTitle": "To'lovlar",
    "admin.demoCards": "Demo kartalar",
    "admin.confirmDelCat": "Kategoriyani o'chirasizmi?",
    "admin.confirmDelProd": "Mahsulotni o'chirasizmi?",
    "admin.newName": "Yangi nom",
    "admin.descOptional": "Tavsif (ixtiyoriy)",
    "admin.imgFail": "Rasm yuklanmadi",
    "admin.deleted": "O'chirildi",
    "admin.roleChanged": "Rol o'zgardi",
    "admin.passUpdated": "Parol yangilandi",
    "admin.statusUpdated": "Status yangilandi",
    "admin.verify": "Tasdiqlash",
    "admin.reject": "Rad etish",
    "admin.verified": "Tasdiqlandi",
    "admin.rejected": "Rad etildi",
    "admin.block": "Bloklash",
    "admin.activate": "Faollashtirish",
    "admin.activeState": "faol",
    "admin.blockedState": "bloklangan",
    "admin.toUser": "→ User",
    "admin.toAdmin": "→ Admin",
    "admin.password": "🔑 Parol",
    "admin.newPassPrompt": "uchun yangi parol (kamida 6 belgi):",
    "admin.expires": "muddati",
    "admin.userWord": "foydalanuvchi",
    "admin.paymentWord": "To'lov",
    // product images
    "pd.imgUrl": "Rasm URL (ixtiyoriy)",
    "pd.imgFile": "Rasm fayl yuklash (ixtiyoriy)",
    "pd.imgHint": "URL yoki fayl — bittasi yetarli. Bo'sh qoldirsa 📦 chiqadi.",
    "forgot.link": "Parolni unutdingizmi?",
    "forgot.title": "Parolni tiklash",
    "forgot.sub": "Emailingizga tiklash kodi yuboramiz",
    "forgot.email": "Email manzili",
    "forgot.send": "Kod yuborish",
    "forgot.sending": "Yuborilmoqda...",
    "forgot.code": "Tiklash kodi",
    "forgot.codeHint": "6 raqamli kodni kiriting",
    "forgot.newPass": "Yangi parol",
    "forgot.confirm": "Parolni tasdiqlash",
    "forgot.reset": "Parolni tiklash",
    "forgot.newPassword": "Yangi parol",
    "forgot.confirmPassword": "Yangi parolni tasdiqlash",
    "forgot.codePlaceholder": "000000",

      // ── server xabarlari (locale/*.json dan) ──
      "username_taken": "Bu username band",
      "email_taken": "Bu email band",
      "wrong_credentials": "Username yoki parol noto'g'ri",
      "account_blocked": "Hisobingiz bloklangan",
      "user_not_found": "Foydalanuvchi topilmadi",
      "admin_required": "Bu amal uchun admin huquqi kerak",
      "category_not_found": "Kategoriya topilmadi",
      "category_name_taken": "Bu kategoriya nomi band",
      "product_not_found": "Mahsulot topilmadi",
      "category_not_exists": "Bunday kategoriya mavjud emas",
      "cart_item_not_found": "Savat elementi topilmadi",
      "not_your_cart": "Bu sizning savatingiz emas",
      "cart_empty": "Savat bo'sh",
      "insufficient_stock": "'{title}' mahsulotidan yetarli qoldiq yo'q",
      "order_not_found": "Buyurtma topilmadi",
      "not_your_order": "Bu sizning buyurtmangiz emas",
      "only_pending_can_cancel": "Faqat 'pending' holatdagi buyurtmani bekor qilish mumkin",
      "only_buyers_can_review": "Faqat sotib olgan foydalanuvchi sharh qoldira oladi",
      "review_not_found": "Sharh topilmadi",
      "not_your_review": "Bu sizning sharhingiz emas",
      "address_not_found": "Manzil topilmadi",
      "not_your_address": "Bu sizning manzilingiz emas",
      "token_invalid": "Token noto'g'ri",
      "token_type_invalid": "Token turi noto'g'ri. Kutilgan: {expected}",
      "token_expired": "Token muddati tugagan",
      "token_invalid_generic": "Token yaroqsiz",
      "card_already_exists": "Bu karta allaqachon bor",
      "only_pending_payment": "Faqat pending buyurtma uchun to'lov mumkin",
      "demo_card_not_found": "Demo karta topilmadi",
      "payment_not_found": "To'lov topilmadi",
      "permission_denied": "Ruxsat yo'q",
      "payment_not_started": "Avval /pay bilan to'lovni boshlang",
      "not_your_payment": "Bu sizning to'lovingiz emas",
      "payment_status_invalid": "To'lov holati {status}, screenshot yuborib bo'lmaydi",
      "payment_expired": "15 daqiqa tugadi, to'lov expired",
      "insufficient_balance": "Demo karta balansi yetarli emas",
      "deleted": "O'chirildi",
      "cart_cleared": "Savat tozalandi",
      "order_cancelled": "Buyurtma bekor qilindi",
      "verified": "Tasdiqlandi ✅",
      "rejected": "Rad etildi",
      "register_success": "Muvaffaqiyatli ro'yxatdan o'tdingiz",
      "review_added": "Sharh qo`shildi",
      "address_added": "Manzil qo'shildi",
      "cannot_block_self": "O'zingizni bloklayolmaysiz",
      "cannot_demote_self": "O'z rolingizni pasaytiraolmaysiz",
      "invalid_input": "Kiritilgan maʼlumot notoʼgʼri",
      "imageUrlNotAllowed": "Rasm URL maydoniga rasm yopishtirib bo‘lmaydi. «Rasm fayl» maydonidan fayl yuklang.",
      "imageUrlTooLong": "Rasm URL juda uzun (2048 belgidan ko‘p).",
      "resetCodeSent": "Agar bu email bazada ro‘yxatda bo‘lsa, tiklash kodi yuborildi.",
      "resetCodeInvalid": "Kod noto‘g‘ri. Yoki urinishlar soni tugab, kod o‘chirildi.",
      "resetCodeExpired": "Kodning muddati tugagan. Yangi kod so‘rang.",
      "passwordChanged": "Parolingiz yangilandi. Endi yangi parol bilan kiring.",
      "resetCodeExpiredShort": "Kod muddati tugadi. Yangi kod so‘rang.",
    "forgot.backToLogin": "Kirish sahifasiga qaytish",
    "forgot.step1": "1-qadam: email",
    "forgot.step2": "2-qadam: kod va yangi parol",
    "forgot.sentTo": "Kod yuborildi:",
    "forgot.resend": "Kodni qayta yuborish",
    "forgot.mismatch": "Parollar mos kelmadi",
    "forgot.passShort": "Parol kamida 6 ta belgidan iborat bo'lsin",
    "forgot.done": "Parol yangilandi. Kirish sahifasiga o'tamiz...",
    "forgot.wait": "Yana {s} soniya kutamiz",
    "forgot.expiresIn": "Kod muddati:",
    "forgot.expired": "Kod muddati tugadi",
    "forgot.expiredHint": "Yangi kod so‘rash uchun yuqoridagi tugmani bosing",
    "forgot.renew": "Yangi kod so‘rash",
    "resetCodeExpiredShort": "Kod muddati tugadi. Yangi kod so‘rang.",
    "forgot.uiError": "Kod yuborildi, lekin sahifada xatolik yuz berdi. Sahifani yangilang.",
  },
  ru: {
    "nav.products": "Товары",
    "nav.cart": "Корзина",
    "nav.profile": "Профиль",
    "nav.admin": "Админ",
    "nav.login": "Войти",
    "nav.register": "Регистрация",
    "nav.logout": "Выйти",
    "hero.eyebrow": "★ Новая коллекция • 2026",
    "hero.title": "Найдите всё <em>в одном месте</em>",
    "hero.desc": "Телефоны, аксессуары и тысячи товаров — с фильтром, поиском и быстрой доставкой.",
    "hero.btn": "Начать покупки →",
    "hero.note": "500+ довольных клиентов",
    "hero.card_label": "Быстрая доставка",
    "hero.card_value": "В течение 24 часов",
    "hero.card_desc": "Бесплатная доставка по Ташкенту",
    "filter.search": "Поиск — например: iPhone",
    "filter.allCat": "Все категории",
    "filter.newest": "Сначала новые",
    "filter.price": "По цене",
    "filter.desc": "Убывание",
    "filter.asc": "Возрастание",
    "filter.min": "Мин цена",
    "filter.max": "Макс цена",
    "filter.clear": "Очистить",
    "products.title": "Все товары",
    "products.empty": "Ничего не найдено. Очистите фильтры.",
    "products.add": "В корзину +",
    "products.detail": "Подробнее",
    "products.stock": "шт осталось",
    "products.out": "Нет в наличии",
    "products.noDesc": "Нет описания",
    "auth.login_title": "Вход",
    "auth.login_sub": "Введите данные для входа",
    "auth.login_btn": "Войти",
    "auth.login_noacc": "Нет аккаунта?",
    "auth.register_title": "Регистрация",
    "auth.register_sub": "Создайте аккаунт за секунды",
    "auth.register_btn": "Зарегистрироваться",
    "auth.hasAcc": "Есть аккаунт?",
    "auth.name": "Имя",
    "auth.username": "Логин или email",
    "forgot.loginHint": "Теперь войдите, указав логин или email.",
    "auth.usernamePh": "ake или email@onlineshop.uz",
    "auth.email": "Email",
    "auth.password": "Пароль",
    "auth.brand_login": "Рады снова видеть вас",
    "auth.brand_login_p": "Войдите и продолжите покупки.",
    "auth.brand_reg": "Начните покупки сейчас",
    "auth.brand_reg_p": "Зарегистрируйтесь и получите доступ к тысячам товаров.",
    "profile.title": "Профиль",
    "profile.info": "Личные данные",
    "profile.edit": "Редактировать профиль",
    "profile.save": "Сохранить",
    "profile.addrs": "Мои адреса",
    "profile.orders": "Мои заказы",
    "profile.avatar_url": "URL аватара (необязательно)",
    "profile.avatar_file": "Или загрузите файл",
    "cart.title": "Корзина",
    "cart.desc": "Проверьте товары — затем перейдите к оплате",
    "cart.clear": "Очистить корзину",
    "cart.continue": "Продолжить →",
    "cart.continue_hint": "Кнопка продолжения ведёт на полную страницу оплаты — заказ создаётся после проверки.",
    "cart.empty": "Корзина пуста.",
    "cart.toProducts": "К товарам",
    "pay.title": "Оплата",
    "pay.back": "← Назад в корзину",
    "pay.desc": "Проверьте заказ, затем оплатите. Если чек не загружен за 15 минут — отменяется.",
    "pay.cart": "Состав корзины",
    "pay.total": "Итого",
    "pay.orderBtn": "Оформить заказ →",
    "pay.order_checking": "Проверка...",
    "pay.flash": "ДЕМО UZCARD / HUMO • FLASHCARD",
    "pay.demo_note": "Демо карта — баланс в базе, сайт проверит автоматически и отправит админу в TG.",
    "pay.upload_title": "Загрузите чек (скриншот)",
    "pay.upload_desc": "После оплаты загрузите фото чека. Фото сразу уйдёт админу в TG и баланс проверится.",
    "pay.send": "Отправить",
    "pay.placeholder": "После заказа здесь появится карта и таймер 15 минут.",
    "pd.back": "← Все товары",
    "pd.reviews": "Отзывы",
    "pd.add_review": "Оставить отзыв",
    "pd.review_hint": "Только купившие могут оставлять отзыв",
    "pd.rating": "Рейтинг (1-5)",
    "pd.comment": "Комментарий",
    "pd.send": "Отправить",
    "pd.add_to_cart": "В корзину 🛒",
    "pd.view_cart": "Корзина",
    "admin.title": "Админ панель",
    "admin.only": "только админ",
    "admin.users": "Пользователи",
    "admin.orders": "Заказы",
    "admin.revenue": "Выручка",
    "admin.products": "Товары",
    "admin.categories": "Категории",
    "admin.payments": "Платежи",
    "admin.newCat": "Новая категория",
    "admin.newProd": "Добавить товар",
    "admin.editProd": "Редактирование",
    "admin.ph_title": "iPhone 15 Pro",
    "admin.ph_desc": "Краткое описание",
    "admin.ph_cat_name": "Телефоны",
    "admin.ph_cat_desc": "Описание (необязательно)",
    "profile.ph_country": "Узбекистан",
    "profile.ph_city": "Ташкент",
    "profile.ph_street": "Улица",
    "profile.ph_zip": "Индекс",
    "pd.ph_comment": "Ваш отзыв о товаре",
    "footer.copy": "© 2026 OnlineShop — FastAPI • SQLModel • JWT",
    // wishlist
    "wishlist.nav": "Избранное",
    "wishlist.title": "Избранное",
    "wishlist.desc": "Товары, которым вы поставили сердечко",
    "wishlist.add": "В избранное",
    "wishlist.remove": "Убрать из избранного",
    "wishlist.added": "Добавлено в избранное",
    "wishlist.removed": "Убрано из избранного",
    "wishlist.empty": "Пока ничего нет. Нажмите на сердечко!",
    "wishlist.clear": "Очистить",
    "wishlist.cleared": "Избранное очищено",
    "wishlist.confirm_clear": "Очистить всё избранное?",
    "common.error": "Ошибка",
    "common.network": "Net svyazi s serverom",
    "auth.session_expired": "Сессия завершилась, войдите снова",
    "btn.add": "Добавить",
    "btn.edit": "Редактировать",
    "btn.delete": "Удалить",
    "btn.save": "Сохранить",
    "btn.cancel": "Отмена",
    "btn.refresh": "Обновить",
    "common.loading": "Загрузка...",
    "common.no": "Пока нет",
    // common
    "common.sum": "сум",
    "common.pcs": "шт",
    "common.customer": "Покупатель",
    "common.failure": "Ошибка",
    "common.items": "шт",
    "cart.total": "Итого:",
    // admin
    "admin.noCatFirst": "Сначала добавьте категорию",
    "admin.noCats": "Категорий нет",
    "admin.noProds": "Товаров пока нет",
    "admin.noOrders": "Заказов нет",
    "admin.noUsers": "Пользователей нет",
    "admin.noPays": "Платежей нет",
    "admin.noShot": "Скриншота нет",
    "admin.nameLbl": "Название",
    "admin.descLbl": "Описание",
    "admin.priceLbl": "Цена",
    "admin.stockLbl": "Кол-во на складе",
    "admin.catLbl": "Категория",
    "admin.listTitle": "Список товаров",
    "admin.added": "Добавлено",
    "admin.updated": "Обновлено",
    "admin.editing": "Редактирование",
    "admin.statusLbl": "Статус",
    // profile
    "profile.noAddr": "Адресов нет",
    "profile.noOrders": "Заказов пока нет",
    // product
    "pd.notFound": "Товар не найден",
    "pd.noReviews": "Отзывов пока нет",
    "pd.reviewAdded": "Отзыв добавлен",
    // pay
    "pay.orderWord": "Заказ",
    "pay.statusLbl": "Статус",
    // order/payment status
    "st.pending": "Ожидает",
    "st.paid": "Оплачен",
    "st.shipped": "Отправлен",
    "st.delivered": "Доставлен",
    "st.cancelled": "Отменён",
    "st.verified": "Подтверждён",
    // admin qo'shimcha
    "products.fallback": "Товар",
    "st.expired": "Срок истёк",
    "pd.redirecting": "перенаправляем на главную...",
    "pd.addedToCart": "Добавлено в корзину",
    "profile.savedMsg": "Сохранено",
    "profile.savedToast": "Профиль обновлён",
    "profile.addrAdded": "Адрес добавлен",
    "admin.paymentsTitle": "Платежи",
    "admin.demoCards": "Демо карты",
    "admin.confirmDelCat": "Удалить категорию?",
    "admin.confirmDelProd": "Удалить товар?",
    "admin.newName": "Новое название",
    "admin.descOptional": "Описание (необязательно)",
    "admin.imgFail": "Изображение не загружено",
    "admin.deleted": "Удалено",
    "admin.roleChanged": "Роль изменена",
    "admin.passUpdated": "Пароль обновлён",
    "admin.statusUpdated": "Статус обновлён",
    "admin.verify": "Подтвердить",
    "admin.reject": "Отклонить",
    "admin.verified": "Подтверждено",
    "admin.rejected": "Отклонено",
    "admin.block": "Заблокировать",
    "admin.activate": "Активировать",
    "admin.activeState": "активен",
    "admin.blockedState": "заблокирован",
    "admin.toUser": "→ Пользователь",
    "admin.toAdmin": "→ Админ",
    "admin.password": "🔑 Пароль",
    "admin.newPassPrompt": "новый пароль (минимум 6 символов):",
    "admin.expires": "до",
    "admin.userWord": "пользователь",
    "admin.paymentWord": "Платёж",
    // product images
    "pd.imgUrl": "URL изображения (необязательно)",
    "pd.imgFile": "Загрузить файл (необязательно)",
    "pd.imgHint": "URL или файл — достаточно одного. Если пусто, будет 📦.",
    "forgot.link": "Забыли пароль?",
    "forgot.title": "Восстановление пароля",
    "forgot.sub": "Отправим код восстановления на ваш email",
    "forgot.email": "Адрес электронной почты",
    "forgot.send": "Отправить код",
    "forgot.sending": "Отправка...",
    "forgot.code": "Код восстановления",
    "forgot.codeHint": "Введите код из 6 цифр",
    "forgot.newPass": "Новый пароль",
    "forgot.confirm": "Подтвердите пароль",
    "forgot.reset": "Сбросить пароль",
    "forgot.newPassword": "Новый пароль",
    "forgot.confirmPassword": "Подтвердите новый пароль",
    "forgot.codePlaceholder": "000000",

      // ── server xabarlari (locale/*.json dan) ──
      "username_taken": "Это имя пользователя занято",
      "email_taken": "Этот email уже занят",
      "wrong_credentials": "Неверный логин или пароль",
      "account_blocked": "Ваш аккаунт заблокирован",
      "user_not_found": "Пользователь не найден",
      "admin_required": "Требуются права администратора",
      "category_not_found": "Категория не найдена",
      "category_name_taken": "Такое имя категории уже занято",
      "product_not_found": "Товар не найден",
      "category_not_exists": "Такой категории не существует",
      "cart_item_not_found": "Элемент корзины не найден",
      "not_your_cart": "Это не ваша корзина",
      "cart_empty": "Корзина пуста",
      "insufficient_stock": "Недостаточно товара '{title}'",
      "order_not_found": "Заказ не найден",
      "not_your_order": "Это не ваш заказ",
      "only_pending_can_cancel": "Можно отменить только заказ в статусе 'pending'",
      "only_buyers_can_review": "Отзыв может оставить только покупатель",
      "review_not_found": "Отзыв не найден",
      "not_your_review": "Это не ваш отзыв",
      "address_not_found": "Адрес не найден",
      "not_your_address": "Это не ваш адрес",
      "token_invalid": "Неверный токен",
      "token_type_invalid": "Неверный тип токена. Ожидался: {expected}",
      "token_expired": "Срок токена истёк",
      "token_invalid_generic": "Недействительный токен",
      "card_already_exists": "Такая карта уже существует",
      "only_pending_payment": "Оплата возможна только для заказа в статусе pending",
      "demo_card_not_found": "Демо карта не найдена",
      "payment_not_found": "Платёж не найден",
      "permission_denied": "Нет доступа",
      "payment_not_started": "Сначала начните оплату через /pay",
      "not_your_payment": "Это не ваш платёж",
      "payment_status_invalid": "Статус платежа {status}, нельзя отправить скриншот",
      "payment_expired": "15 минут истекло, платёж просрочен",
      "insufficient_balance": "Недостаточно средств на демо карте",
      "deleted": "Удалено",
      "cart_cleared": "Корзина очищена",
      "order_cancelled": "Заказ отменён",
      "verified": "Подтверждено ✅",
      "rejected": "Отклонено",
      "register_success": "Успешная регистрация",
      "review_added": "Отзыв добавлен",
      "address_added": "Адрес добавлен",
      "cannot_block_self": "Нельзя заблокировать себя",
      "cannot_demote_self": "Нельзя понизить свою роль",
      "invalid_input": "Введено неверное значение",
      "imageUrlNotAllowed": "Нельзя вставлять изображение в поле URL. Загрузите файл через поле «Файл изображения».",
      "imageUrlTooLong": "URL изображения слишком длинный (более 2048 символов).",
      "resetCodeSent": "Если email зарегистрирован, код восстановления отправлен.",
      "resetCodeInvalid": "Неверный код. Либо попытки исчерпаны и код удалён.",
      "resetCodeExpired": "Срок кода истёк. Запросите новый код.",
      "passwordChanged": "Пароль обновлён. Войдите с новым паролем.",
      "resetCodeExpiredShort": "Срок кода истёк. Запросите новый код.",
    "forgot.backToLogin": "Вернуться ко входу",
    "forgot.step1": "Шаг 1: email",
    "forgot.step2": "Шаг 2: код и новый пароль",
    "forgot.sentTo": "Код отправлен на:",
    "forgot.resend": "Отправить код ещё раз",
    "forgot.mismatch": "Пароли не совпадают",
    "forgot.passShort": "Пароль должен быть не короче 6 символов",
    "forgot.done": "Пароль обновлён. Переходим ко входу...",
    "forgot.wait": "Подождите ещё {s} с",
    "forgot.expiresIn": "Срок кода:",
    "forgot.expired": "Срок кода истёк",
    "forgot.expiredHint": "Нажмите кнопку выше, чтобы запросить новый код",
    "forgot.renew": "Запросить новый код",
    "resetCodeExpiredShort": "Срок кода истёк. Запросите новый код.",
    "forgot.uiError": "Код отправлен, но на странице произошла ошибка. Обновите страницу.",
  },
  en: {
    "nav.products": "Products",
    "nav.cart": "Cart",
    "nav.profile": "Profile",
    "nav.admin": "Admin",
    "nav.login": "Login",
    "nav.register": "Sign up",
    "nav.logout": "Logout",
    "hero.eyebrow": "★ New collection • 2026",
    "hero.title": "Find everything <em>in one place</em>",
    "hero.desc": "Phones, accessories and thousands of products — with filter, search and fast delivery.",
    "hero.btn": "Start shopping →",
    "hero.note": "500+ happy customers",
    "hero.card_label": "Fast delivery",
    "hero.card_value": "Within 24 hours",
    "hero.card_desc": "Free delivery in Tashkent",
    "filter.search": "Search — e.g. iPhone",
    "filter.allCat": "All categories",
    "filter.newest": "Newest first",
    "filter.price": "By price",
    "filter.desc": "Descending",
    "filter.asc": "Ascending",
    "filter.min": "Min price",
    "filter.max": "Max price",
    "filter.clear": "Clear",
    "products.title": "All products",
    "products.empty": "Nothing found. Clear filters.",
    "products.add": "Add to cart +",
    "products.detail": "Details",
    "products.stock": "left",
    "products.out": "Out of stock",
    "products.noDesc": "No description",
    "auth.login_title": "Login",
    "auth.login_sub": "Enter your credentials",
    "auth.login_btn": "Login",
    "auth.login_noacc": "No account?",
    "auth.register_title": "Sign up",
    "auth.register_sub": "Create account in seconds",
    "auth.register_btn": "Sign up",
    "auth.hasAcc": "Have an account?",
    "auth.name": "Name",
    "auth.username": "Username yoki email",
    "forgot.loginHint": "Endi kirish sahifasida username yoki email bilan kiring.",
    "auth.usernamePh": "ake yoki email@onlineshop.uz",
    "auth.email": "Email",
    "auth.password": "Password",
    "auth.brand_login": "Welcome back",
    "auth.brand_login_p": "Login and continue shopping.",
    "auth.brand_reg": "Start shopping now",
    "auth.brand_reg_p": "Sign up and get access to thousands of products.",
    "profile.title": "Profile",
    "profile.info": "Personal info",
    "profile.edit": "Edit profile",
    "profile.save": "Save",
    "profile.addrs": "My addresses",
    "profile.orders": "My orders",
    "profile.avatar_url": "Avatar URL (optional)",
    "profile.avatar_file": "Or upload file",
    "cart.title": "Cart",
    "cart.desc": "Check items — then go to payment",
    "cart.clear": "Clear cart",
    "cart.continue": "Continue →",
    "cart.continue_hint": "Continue leads to full payment page — order is created after verification.",
    "cart.empty": "Cart is empty.",
    "cart.toProducts": "To products",
    "pay.title": "Payment",
    "pay.back": "← Back to cart",
    "pay.desc": "Check order, then pay. If no receipt in 15 min — cancelled.",
    "pay.cart": "Cart contents",
    "pay.total": "Total",
    "pay.orderBtn": "Place order →",
    "pay.order_checking": "Checking...",
    "pay.flash": "DEMO UZCARD / HUMO • FLASHCARD",
    "pay.demo_note": "Demo card — balance in DB, site checks automatically and sends to admin TG.",
    "pay.upload_title": "Upload receipt (screenshot)",
    "pay.upload_desc": "After payment upload receipt photo. It goes to admin TG and balance is checked.",
    "pay.send": "Send",
    "pay.placeholder": "Card and 15 min timer will appear after order.",
    "pd.back": "← All products",
    "pd.reviews": "Reviews",
    "pd.add_review": "Add review",
    "pd.review_hint": "Only buyers can review",
    "pd.rating": "Rating (1-5)",
    "pd.comment": "Comment",
    "pd.send": "Send",
    "pd.add_to_cart": "Add to cart 🛒",
    "pd.view_cart": "View cart",
    "admin.title": "Admin Panel",
    "admin.only": "admin only",
    "admin.users": "Users",
    "admin.orders": "Orders",
    "admin.revenue": "Revenue",
    "admin.products": "Products",
    "admin.categories": "Categories",
    "admin.payments": "Payments",
    "admin.newCat": "New category",
    "admin.newProd": "Add product",
    "admin.editProd": "Edit",
    "admin.ph_title": "iPhone 15 Pro",
    "admin.ph_desc": "Short description",
    "admin.ph_cat_name": "Phones",
    "admin.ph_cat_desc": "Description (optional)",
    "profile.ph_country": "Uzbekistan",
    "profile.ph_city": "Tashkent",
    "profile.ph_street": "Street",
    "profile.ph_zip": "ZIP",
    "pd.ph_comment": "Your comment about product",
    "footer.copy": "© 2026 OnlineShop — FastAPI • SQLModel • JWT",
    // wishlist
    "wishlist.nav": "Wishlist",
    "wishlist.title": "Wishlist",
    "wishlist.desc": "Products you hearted",
    "wishlist.add": "Add to wishlist",
    "wishlist.remove": "Remove from wishlist",
    "wishlist.added": "Added to wishlist",
    "wishlist.removed": "Removed from wishlist",
    "wishlist.empty": "Nothing here yet. Tap the heart!",
    "wishlist.clear": "Clear",
    "wishlist.cleared": "Wishlist cleared",
    "wishlist.confirm_clear": "Clear the whole wishlist?",
    "common.error": "Error",
    "common.network": "Server unreachable",
    "auth.session_expired": "Session expired, please log in again",
    "btn.add": "Add",
    "btn.edit": "Edit",
    "btn.delete": "Delete",
    "btn.save": "Save",
    "btn.cancel": "Cancel",
    "btn.refresh": "Refresh",
    "common.loading": "Loading...",
    "common.no": "Nothing yet",
    // common
    "common.sum": "UZS",
    "common.pcs": "pcs",
    "common.customer": "Customer",
    "common.failure": "Error",
    "common.items": "items",
    "cart.total": "Total:",
    // admin
    "admin.noCatFirst": "Add a category first",
    "admin.noCats": "No categories",
    "admin.noProds": "No products yet",
    "admin.noOrders": "No orders",
    "admin.noUsers": "No users",
    "admin.noPays": "No payments",
    "admin.noShot": "No screenshot",
    "admin.nameLbl": "Name",
    "admin.descLbl": "Description",
    "admin.priceLbl": "Price",
    "admin.stockLbl": "Stock",
    "admin.catLbl": "Category",
    "admin.listTitle": "Product list",
    "admin.added": "Added",
    "admin.updated": "Updated",
    "admin.editing": "Editing",
    "admin.statusLbl": "Status",
    // profile
    "profile.noAddr": "No addresses",
    "profile.noOrders": "No orders yet",
    // product
    "pd.notFound": "Product not found",
    "pd.noReviews": "No reviews yet",
    "pd.reviewAdded": "Review added",
    // pay
    "pay.orderWord": "Order",
    "pay.statusLbl": "Status",
    // order/payment status
    "st.pending": "Pending",
    "st.paid": "Paid",
    "st.shipped": "Shipped",
    "st.delivered": "Delivered",
    "st.cancelled": "Cancelled",
    "st.verified": "Verified",
    // admin extra
    "products.fallback": "Product",
    "st.expired": "Expired",
    "pd.redirecting": "redirecting to home...",
    "pd.addedToCart": "Added to cart",
    "profile.savedMsg": "Saved",
    "profile.savedToast": "Profile updated",
    "profile.addrAdded": "Address added",
    "admin.paymentsTitle": "Payments",
    "admin.demoCards": "Demo cards",
    "admin.confirmDelCat": "Delete this category?",
    "admin.confirmDelProd": "Delete this product?",
    "admin.newName": "New name",
    "admin.descOptional": "Description (optional)",
    "admin.imgFail": "Image upload failed",
    "admin.deleted": "Deleted",
    "admin.roleChanged": "Role changed",
    "admin.passUpdated": "Password updated",
    "admin.statusUpdated": "Status updated",
    "admin.verify": "Verify",
    "admin.reject": "Reject",
    "admin.verified": "Verified",
    "admin.rejected": "Rejected",
    "admin.block": "Block",
    "admin.activate": "Activate",
    "admin.activeState": "active",
    "admin.blockedState": "blocked",
    "admin.toUser": "→ User",
    "admin.toAdmin": "→ Admin",
    "admin.password": "🔑 Password",
    "admin.newPassPrompt": "new password (at least 6 characters):",
    "admin.expires": "expires",
    "admin.userWord": "user",
    "admin.paymentWord": "Payment",
    // product images
    "pd.imgUrl": "Image URL (optional)",
    "pd.imgFile": "Upload image file (optional)",
    "pd.imgHint": "URL or file — one is enough. Empty shows 📦.",
    "forgot.link": "Forgot your password?",
    "forgot.title": "Reset password",
    "forgot.sub": "We'll email you a reset code",
    "forgot.email": "Email address",
    "forgot.send": "Send code",
    "forgot.sending": "Sending...",
    "forgot.code": "Reset code",
    "forgot.codeHint": "Enter the 6-digit code",
    "forgot.newPass": "New password",
    "forgot.confirm": "Confirm password",
    "forgot.reset": "Reset password",
    "forgot.newPassword": "New password",
    "forgot.confirmPassword": "Confirm new password",
    "forgot.codePlaceholder": "000000",

      // ── server xabarlari (locale/*.json dan) ──
      "username_taken": "Username already taken",
      "email_taken": "Email already taken",
      "wrong_credentials": "Wrong username or password",
      "account_blocked": "Your account is blocked",
      "user_not_found": "User not found",
      "admin_required": "Admin privileges required",
      "category_not_found": "Category not found",
      "category_name_taken": "Category name already taken",
      "product_not_found": "Product not found",
      "category_not_exists": "Such category does not exist",
      "cart_item_not_found": "Cart item not found",
      "not_your_cart": "This is not your cart",
      "cart_empty": "Cart is empty",
      "insufficient_stock": "Not enough stock for '{title}'",
      "order_not_found": "Order not found",
      "not_your_order": "This is not your order",
      "only_pending_can_cancel": "Only pending orders can be cancelled",
      "only_buyers_can_review": "Only buyers can leave a review",
      "review_not_found": "Review not found",
      "not_your_review": "This is not your review",
      "address_not_found": "Address not found",
      "not_your_address": "This is not your address",
      "token_invalid": "Invalid token",
      "token_type_invalid": "Invalid token type. Expected: {expected}",
      "token_expired": "Token expired",
      "token_invalid_generic": "Invalid token",
      "card_already_exists": "Card already exists",
      "only_pending_payment": "Payment only for pending orders",
      "demo_card_not_found": "Demo card not found",
      "payment_not_found": "Payment not found",
      "permission_denied": "Permission denied",
      "payment_not_started": "Start payment via /pay first",
      "not_your_payment": "This is not your payment",
      "payment_status_invalid": "Payment status {status}, cannot send screenshot",
      "payment_expired": "15 minutes expired",
      "insufficient_balance": "Insufficient demo card balance",
      "deleted": "Deleted",
      "cart_cleared": "Cart cleared",
      "order_cancelled": "Order cancelled",
      "verified": "Verified ✅",
      "rejected": "Rejected",
      "register_success": "Successfully registered",
      "review_added": "Review added",
      "address_added": "Address added",
      "cannot_block_self": "You cannot block yourself",
      "cannot_demote_self": "You cannot demote yourself",
      "invalid_input": "Invalid value provided",
      "imageUrlNotAllowed": "Do not paste an image into the URL field. Upload a file via the \"Image file\" field.",
      "imageUrlTooLong": "Image URL is too long (over 2048 characters).",
      "resetCodeSent": "If the email is registered, a reset code has been sent.",
      "resetCodeInvalid": "Wrong code. Or attempts ran out and the code was voided.",
      "resetCodeExpired": "The code has expired. Request a new one.",
      "passwordChanged": "Your password has been updated. Sign in with the new one.",
      "resetCodeExpiredShort": "The code has expired. Request a new one.",
    "forgot.backToLogin": "Back to sign in",
    "forgot.step1": "Step 1: email",
    "forgot.step2": "Step 2: code and new password",
    "forgot.sentTo": "Code sent to:",
    "forgot.resend": "Resend code",
    "forgot.mismatch": "Passwords do not match",
    "forgot.passShort": "Password must be at least 6 characters",
    "forgot.done": "Password updated. Redirecting to sign in...",
    "forgot.wait": "Wait {s}s",
    "forgot.expiresIn": "Code expires in:",
    "forgot.expired": "Code expired",
    "forgot.expiredHint": "Press the button above to request a new code",
    "forgot.renew": "Request a new code",
    "resetCodeExpiredShort": "The code has expired. Request a new one.",
    "forgot.uiError": "The code was sent, but the page hit an error. Please refresh.",
  }
};

let currentLang = localStorage.getItem('lang') || 'uz';
if(!['uz','ru','en'].includes(currentLang)) currentLang='uz';

// Backend ham shu tilni tushunishi uchun har bir fetch ga header qo'shamiz
// Va 401 qaytganda access token'ni avtomatik yangilab, so'rovni qayta yuboramiz.
const _origFetch = window.fetch.bind(window);
let _refreshing = null;

async function refreshAccessToken(){
  const rt = localStorage.getItem('refresh_token');
  if(!rt) return null;
  if(!_refreshing){
    _refreshing = _origFetch('/auth/refresh', {
      method:'POST',
      headers:{'Content-Type':'application/json'},
      body: JSON.stringify({refresh_token: rt})
    }).then(r => r.ok ? r.json() : null).catch(() => null).finally(() => { _refreshing = null; });
  }
  const data = await _refreshing;
  if(data && data.access_token){
    localStorage.setItem('access_token', data.access_token);
    if(data.refresh_token) localStorage.setItem('refresh_token', data.refresh_token);
    return data.access_token;
  }
  return null;
}

function forceLogout(){
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  if(typeof showToast === 'function') showToast(t('auth.session_expired'), 'error');
  setTimeout(() => location.href = '/login-page', 1200);
}

window.fetch = async function(url, opts = {}){
  opts.headers = opts.headers || {};
  if(opts.headers instanceof Headers){
    opts.headers.set('Accept-Language', currentLang);
  } else {
    opts.headers = {...opts.headers, 'Accept-Language': currentLang};
  }

  const res = await _origFetch(url, opts);

  const isAuthCall = typeof url === 'string' && (url.includes('/auth/refresh') || url.includes('/auth/login'));
  if(res.status === 401 && !isAuthCall && opts.headers.Authorization){
    const fresh = await refreshAccessToken();
    if(!fresh){ forceLogout(); return res; }
    opts.headers = {...opts.headers, 'Authorization': 'Bearer ' + fresh};
    return _origFetch(url, opts);
  }
  return translateServerText(res);
};

// ══ Server xabarlarini avtomatik tarjima qilish ══════════════
// Server t("resetCodeSent", lang) qilib ALMASHGAN matn qaytaradi.
// U matnni kalitga qaytarib, joriy tilga o'girib beramiz — shunda
// login/savat/buyurtma/admin xatolari ham RU/EN da to'g'ri chiqadi.
const API_MSG_KEYS = [
  'username_taken',
  'email_taken',
  'wrong_credentials',
  'account_blocked',
  'user_not_found',
  'admin_required',
  'category_not_found',
  'category_name_taken',
  'product_not_found',
  'category_not_exists',
  'cart_item_not_found',
  'not_your_cart',
  'cart_empty',
  'insufficient_stock',
  'order_not_found',
  'not_your_order',
  'only_pending_can_cancel',
  'only_buyers_can_review',
  'review_not_found',
  'not_your_review',
  'address_not_found',
  'not_your_address',
  'token_invalid',
  'token_type_invalid',
  'token_expired',
  'token_invalid_generic',
  'card_already_exists',
  'only_pending_payment',
  'demo_card_not_found',
  'payment_not_found',
  'permission_denied',
  'payment_not_started',
  'not_your_payment',
  'payment_status_invalid',
  'payment_expired',
  'insufficient_balance',
  'deleted',
  'cart_cleared',
  'order_cancelled',
  'verified',
  'rejected',
  'register_success',
  'review_added',
  'address_added',
  'cannot_block_self',
  'cannot_demote_self',
  'invalid_input',
  'imageUrlNotAllowed',
  'imageUrlTooLong',
  'resetCodeSent',
  'resetCodeInvalid',
  'resetCodeExpired',
  'passwordChanged',
  'resetCodeExpiredShort',
];

// matn -> kalit (har til uchun teskari indeks)
const API_MSG_INDEX = {};
for (const lang of ['uz', 'ru', 'en']) {
  API_MSG_INDEX[lang] = {};
  for (const k of API_MSG_KEYS) {
    const txt = translations[lang][k];
    if (typeof txt === 'string' && txt) {
      // {placeholder} li kalitlarni indekslamaymiz — ular to'ldirilgan holda keladi
      if (!txt.includes('{')) API_MSG_INDEX[lang][txt] = k;
    }
  }
}

// server matnidan kalitni topadi (i18n.js:xxx kabi) — aks holda null
function apiKeyOf(text) {
  if (typeof text !== 'string' || !text) return null;
  for (const l of ['uz', 'ru', 'en']) {
    const k = API_MSG_INDEX[l][text];
    if (k) return k;
  }
  return null;
}

// server matnini joriy tilga o'giradi; o'zgarmasa null qaytaradi
function apiTranslate(text, lang) {
  if (typeof text !== 'string' || !text) return null;
  const from = API_MSG_INDEX[lang] || {};
  // 1) joriy tilda allaqon shunday yozilganmi
  if (from[text]) return null;
  // 2) boshqa tilda yozilganmi -> kalitni topamiz
  for (const l of ['uz', 'ru', 'en']) {
    if (l === lang) continue;
    const k = API_MSG_INDEX[l][text];
    if (k && translations[lang][k] && !translations[lang][k].includes('{')) {
      return translations[lang][k];
    }
  }
  return null;
}

// JSON yukida ishlaydi: {detail}, {message}, 422 uchun [{msg}] massivi
function translatePayload(data) {
  let changed = false;
  const fix = obj => {
    for (const f of ['detail', 'message', 'msg']) {
      if (typeof obj[f] === 'string') {
        const tr = apiTranslate(obj[f], currentLang);
        if (tr) { obj[f] = tr; changed = true; }
      }
    }
    return changed;
  };
  if (Array.isArray(data)) {
    data.forEach(it => { if (it && typeof it === 'object') fix(it); });
  } else if (data && typeof data === 'object') {
    fix(data);
  }
  return changed;
}

async function translateServerText(res) {
  const ct = res.headers.get('content-type') || '';
  if (!ct.includes('json')) return res;
  let data;
  try { data = await res.clone().json(); } catch (e) { return res; }
  if (!translatePayload(data)) return res;
  return new Response(JSON.stringify(data), {
    status: res.status,
    statusText: res.statusText,
    headers: { 'Content-Type': 'application/json' }
  });
}

function t(key){
  return (translations[currentLang] && translations[currentLang][key]) || (translations['uz'][key] || key);
}

const LOCALE_MAP = { uz: 'uz-UZ', ru: 'ru-RU', en: 'en-US' };
const CURRENCY_MAP = { uz: "so'm", ru: 'сум', en: 'UZS' };

// Raqamni joriy tilda formatlash (1000 -> 1 000 / 1 000 / 1,000)
function fmt(n, decimals){
  const num = Number(n || 0);
  return num.toLocaleString(LOCALE_MAP[currentLang] || 'uz-UZ', {
    minimumFractionDigits: decimals || 0,
    maximumFractionDigits: decimals || 0
  });
}

// Narxni valyuta bilan formatlash
function cur(n){
  return fmt(n) + ' ' + t('common.sum');
}

// Sana formatini joriy tilda o'zgartirish
function fmtDate(d, withTime){
  if(!d) return '';
  const date = new Date(d);
  if(isNaN(date)) return String(d);
  return date.toLocaleString(LOCALE_MAP[currentLang] || 'uz-UZ',
    withTime === false ? { dateStyle: 'medium' } : { dateStyle: 'medium', timeStyle: 'short' });
}

function applyI18n(){
  document.documentElement.lang = currentLang;
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    const key=el.getAttribute('data-i18n');
    const val=t(key);
    if(val.includes('<em>') || val.includes('<')) el.innerHTML=val;
    else el.textContent=val;
  });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el=>{
    const key=el.getAttribute('data-i18n-placeholder');
    el.placeholder=t(key);
  });
  document.querySelectorAll('[data-i18n-value]').forEach(el=>{
    el.value=t(el.getAttribute('data-i18n-value'));
  });
  // active lang button
  document.querySelectorAll('.lang-btn').forEach(b=>{
    b.classList.toggle('active', b.dataset.lang===currentLang);
  });
  localStorage.setItem('lang', currentLang);
}

// Buyurtma/to'lov holatini tarjima qilish
function stLabel(s){ return t('st.' + s); }

// Til almashganda sahifadagi dinamik kontentni qayta chizish uchun ro'yxat
window.__i18nRerender = [];
function onLangChange(fn){
  if(typeof fn === 'function') window.__i18nRerender.push(fn);
}

function setLang(lang){
  if(!['uz','ru','en'].includes(lang)) return;
  currentLang = lang;
  applyI18n();
  // Barcha dinamik qismlarni qayta chizish (savatlar, wishlist, admin, profil ...)
  window.__i18nRerender.forEach(fn => { try{ fn(); }catch(e){ console.error(e); } });
  if(typeof loadProducts === 'function' && document.getElementById('products-list')) loadProducts();
  document.dispatchEvent(new CustomEvent('langchange', { detail: { lang } }));
}

document.addEventListener('DOMContentLoaded', ()=>{
  applyI18n();
  document.querySelectorAll('.lang-btn').forEach(b=>{
    b.addEventListener('click', ()=> setLang(b.dataset.lang));
  });
  if(currentLang !== 'uz'){
    window.__i18nRerender.forEach(fn => { try{ fn(); }catch(e){ console.error(e); } });
  }
});
