"""
models.py — TZ 4-bo'limdagi 10 ta jadval
Har bir modelda Relationship() bilan bog'lanishlar to'liq yozilgan.
Nomlar TZ ga 100% mos, tushunarli kommentlar bilan.
"""
from datetime import datetime
from typing import Optional

from sqlalchemy import UniqueConstraint
from sqlmodel import SQLModel, Field, Relationship


# ─────────────────────────────────────────────
# 1. User
# ─────────────────────────────────────────────
class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    username: str = Field(unique=True, nullable=False, index=True)
    email: str = Field(unique=True, nullable=False, index=True)
    password: str  # bcrypt hash saqlanadi, hech qachon plain-text emas
    role: str = Field(default="user")  # "user" | "admin"
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    avatar_url: Optional[str] = Field(default=None, description="Profil rasmi URL")

    # teskari bog'lanishlar (ixtiyoriy, lekin qulay)
    carts: list["Cart"] = Relationship(back_populates="user")
    orders: list["Order"] = Relationship(back_populates="user")
    reviews: list["Review"] = Relationship(back_populates="user")
    addresses: list["Address"] = Relationship(back_populates="user")
    reset_tokens: list["PasswordResetToken"] = Relationship(back_populates="user")


# ─────────────────────────────────────────────
# 2. Category — self-referencing parent_id bilan
# ─────────────────────────────────────────────
class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False, index=True)
    description: Optional[str] = Field(default=None)
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id")

    products: list["Product"] = Relationship(back_populates="category")


# ─────────────────────────────────────────────
# 3. Product
# ─────────────────────────────────────────────
class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    description: Optional[str] = Field(default=None)
    price: float = Field(ge=0)
    stock: int = Field(default=0, ge=0)
    category_id: int = Field(foreign_key="categories.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    category: "Category" = Relationship(back_populates="products")
    images: list["ProductImage"] = Relationship(back_populates="product", cascade_delete=True)
    reviews: list["Review"] = Relationship(back_populates="product")


# ─────────────────────────────────────────────
# 4. ProductImage
# ─────────────────────────────────────────────
class ProductImage(SQLModel, table=True):
    __tablename__ = "productImages"

    id: Optional[int] = Field(default=None, primary_key=True)
    image_url: str
    product_id: int = Field(foreign_key="products.id", index=True)

    product: Product = Relationship(back_populates="images")


# ─────────────────────────────────────────────
# 5. Cart — har bir userga bitta savat (unique user_id)
# ─────────────────────────────────────────────
class Cart(SQLModel, table=True):
    __tablename__ = "carts"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", unique=True, index=True)

    user: User = Relationship(back_populates="carts")
    items: list["CartItem"] = Relationship(back_populates="cart", cascade_delete=True)


# ─────────────────────────────────────────────
# 6. CartItem
# ─────────────────────────────────────────────
class CartItem(SQLModel, table=True):
    __tablename__ = "cartItems"

    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int = Field(default=1, ge=1)
    cart_id: int = Field(foreign_key="carts.id", index=True)
    product_id: int = Field(foreign_key="products.id", index=True)

    cart: Cart = Relationship(back_populates="items")
    product: Product = Relationship()


# ─────────────────────────────────────────────
# 7. Order
# ─────────────────────────────────────────────
class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: Optional[int] = Field(default=None, primary_key=True)
    status: str = Field(default="pending")  # pending | paid | shipped | delivered | cancelled
    total_price: float = Field(default=0, ge=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="users.id", index=True)

    user: User = Relationship(back_populates="orders")
    items: list["OrderItem"] = Relationship(back_populates="order", cascade_delete=True)


# ─────────────────────────────────────────────
# 8. OrderItem
# ─────────────────────────────────────────────
class OrderItem(SQLModel, table=True):
    __tablename__ = "orderItems"

    id: Optional[int] = Field(default=None, primary_key=True)
    quantity: int = Field(ge=1)
    price_at_order: float = Field(ge=0)
    order_id: int = Field(foreign_key="orders.id", index=True)
    product_id: int = Field(foreign_key="products.id")

    order: Order = Relationship(back_populates="items")
    product: Product = Relationship()


# ─────────────────────────────────────────────
# 9. Review
# ─────────────────────────────────────────────
class Review(SQLModel, table=True):
    __tablename__ = "reviews"

    id: Optional[int] = Field(default=None, primary_key=True)
    rating: int = Field(ge=1, le=5)
    comment: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    user_id: int = Field(foreign_key="users.id", index=True)
    product_id: int = Field(foreign_key="products.id", index=True)

    user: User = Relationship(back_populates="reviews")
    product: Product = Relationship(back_populates="reviews")


# ─────────────────────────────────────────────
# 10. Address
# ─────────────────────────────────────────────
class Address(SQLModel, table=True):
    __tablename__ = "addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    country: str
    city: str
    street: str
    zip_code: str
    user_id: int = Field(foreign_key="users.id", index=True)

    user: User = Relationship(back_populates="addresses")


# ─────────────────────────────────────────────
# 11. DemoCard — vaqtinchalik demo karta (pul tekshirish uchun)
# ─────────────────────────────────────────────
class DemoCard(SQLModel, table=True):
    __tablename__ = "demo_cards"

    id: Optional[int] = Field(default=None, primary_key=True)
    card_number: str = Field(unique=True, index=True)  # 8600 1234 5678 9012
    card_holder: str = Field(default="Demo Card")
    balance: float = Field(default=10_000_000, ge=0)  # so'mda
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


# ─────────────────────────────────────────────
# 12. Payment — buyurtma to'lovi (flashcard + screenshot)
# ─────────────────────────────────────────────
class Payment(SQLModel, table=True):
    __tablename__ = "payments"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", unique=True, index=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    demo_card_id: int = Field(foreign_key="demo_cards.id")
    amount: float = Field(ge=0)
    status: str = Field(default="pending")  # pending | verified | expired | rejected
    screenshot_url: Optional[str] = Field(default=None)
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow())
    created_at: datetime = Field(default_factory=datetime.utcnow)

    order: Order = Relationship()
    user: User = Relationship()
    demo_card: DemoCard = Relationship()


# ─────────────────────────────────────────────
# 13. Wishlist — sevimlilar (yurak)
# ─────────────────────────────────────────────
class Wishlist(SQLModel, table=True):
    __tablename__ = "wishlists"
    __table_args__ = (UniqueConstraint("user_id", "product_id", name="uq_wishlist_user_product"),)

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id", index=True)
    product_id: int = Field(foreign_key="products.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: User = Relationship()
    product: Product = Relationship()


# ─────────────────────────────────────────────


# ─────────────────────────────────────────────
# PasswordResetToken — email orqali parol tiklash kodi
# Kod sha256 ko'rinishida saqlanadi (ochiq matnda emas)
# ─────────────────────────────────────────────
class PasswordResetToken(SQLModel, table=True):
    __tablename__ = "password_reset_tokens"

    id: Optional[int] = Field(default=None, primary_key=True)
    token: str = Field(index=True, nullable=False)  # sha256 hex
    user_id: int = Field(foreign_key="users.id", index=True, nullable=False)
    expires_at: datetime = Field(nullable=False)
    used: bool = Field(default=False)
    attempts: int = Field(default=0)  # noto'g'ri kod kiritilgan urinishlar
    created_at: datetime = Field(default_factory=datetime.utcnow)

    user: "User" = Relationship(back_populates="reset_tokens")
