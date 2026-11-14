"""
product.py — mahsulotlar + MinIO
GET /products -> filter, search, pagination, sort + rasmlar bilan
POST/PUT/DELETE va images — faqat admin, MinIO S3 fallback static/media
"""
import os
import uuid
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, UploadFile, File
from sqlmodel import Session, select

from apps.database import get_session
from apps.dependencies import require_admin
from apps.forms import ProductForm, ProductImageForm
from apps.i18n import get_lang, t
from apps.minio_client import upload_bytes
from apps.models import Product, ProductImage, Category, User
from apps.uploads import MAX_IMAGE_BYTES, read_image

router = APIRouter(prefix="/products", tags=["Products"])

# "Rasm URL" maydoni faqat havolalarni qabul qiladi. data: URI (base64 rasm)
# yozilsa, u ba'zan qirqilib qoladi va brauzerda rasm chiqmaydi — shuning uchun
# rad etiladi. Rasmiy fayl "Rasm fayl" maydonidan yuklanadi (/upload).
MAX_IMAGE_URL_LEN = 2048


def clean_image_url(url: Optional[str], lang: str) -> Optional[str]:
    """Rasm URL'ini tekshiradi: bo'sh, data: URI va juda uzun qiymatlarni rad etadi."""
    if url is None:
        return None
    url = str(url).strip()
    if not url:
        return None
    if url.lower().startswith("data:"):
        raise HTTPException(
            status_code=400,
            detail=t("imageUrlNotAllowed", lang),
        )
    # Faqat http(s) yoki nisbiy yo'l. javascript:, vbscript: kabi sxemalar rad etiladi.
    scheme = url.split(":", 1)[0].lower() if ":" in url.split("/", 1)[0] else ""
    if scheme and scheme not in {"http", "https"}:
        raise HTTPException(status_code=400, detail=t("imageUrlNotAllowed", lang))
    if len(url) > MAX_IMAGE_URL_LEN:
        raise HTTPException(status_code=400, detail=t("imageUrlTooLong", lang))
    return url


def _product_with_images(session: Session, product: Product) -> dict:
    images = session.exec(
        select(ProductImage)
        .where(ProductImage.product_id == product.id)
        .order_by(ProductImage.id)
    ).all()
    data = product.model_dump()
    cat = session.get(Category, product.category_id)
    data["category"] = {"id": cat.id, "name": cat.name} if cat else None
    data["images"] = [img.model_dump() for img in images]
    data["image_url"] = images[0].image_url if images else None
    return data


@router.get("/")
@router.get("", include_in_schema=False)
def list_products(
    session: Session = Depends(get_session),
    category_id: Optional[int] = Query(default=None),
    min_price: Optional[float] = Query(default=None, ge=0),
    max_price: Optional[float] = Query(default=None, ge=0),
    search: Optional[str] = Query(default=None),
    page: int = Query(default=1, ge=1),
    limit: int = Query(default=10, ge=1, le=100),
    sort_by: str = Query(default="created_at"),
    order: str = Query(default="desc"),
):
    query = select(Product)
    if category_id is not None:
        query = query.where(Product.category_id == category_id)
    if min_price is not None:
        query = query.where(Product.price >= min_price)
    if max_price is not None:
        query = query.where(Product.price <= max_price)
    if search:
        query = query.where(Product.title.ilike(f"%{search}%"))
    sort_field = Product.price if sort_by == "price" else Product.created_at
    query = query.order_by(sort_field.desc() if order == "desc" else sort_field.asc())
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)
    products = session.exec(query).all()
    return [_product_with_images(session, p) for p in products]


@router.get("/{product_id}")
def get_product(product_id: int, session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))
    return _product_with_images(session, product)


@router.post("/", status_code=201)
@router.post("", status_code=201, include_in_schema=False)
def create_product(form: ProductForm, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    if not session.get(Category, form.category_id):
        raise HTTPException(status_code=404, detail=t("category_not_exists", lang))
    image_url = clean_image_url(form.image_url, lang)
    data = form.model_dump(exclude={"image_url"})
    product = Product(**data)
    session.add(product)
    session.commit()
    session.refresh(product)
    if image_url:
        img = ProductImage(image_url=image_url, product_id=product.id)
        session.add(img)
        session.commit()
    return _product_with_images(session, product)


@router.put("/{product_id}")
def update_product(product_id: int, form: ProductForm, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))
    image_url = clean_image_url(form.image_url, lang)
    for key, val in form.model_dump(exclude={"image_url"}).items():
        setattr(product, key, val)
    session.add(product)
    session.commit()
    if image_url:
        img = ProductImage(image_url=image_url, product_id=product.id)
        session.add(img)
        session.commit()
    session.refresh(product)
    return _product_with_images(session, product)


@router.delete("/{product_id}")
def delete_product(product_id: int, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))
    for img in session.exec(select(ProductImage).where(ProductImage.product_id == product_id)).all():
        session.delete(img)
    session.delete(product)
    session.commit()
    return {"message": t("deleted", lang)}


@router.post("/{product_id}/images", status_code=201)
def add_product_image(product_id: int, form: ProductImageForm, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    if not session.get(Product, product_id):
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))
    image_url = clean_image_url(form.image_url, lang)
    if not image_url:
        raise HTTPException(status_code=400, detail=t("invalid_input", lang))
    image = ProductImage(image_url=image_url, product_id=product_id)
    session.add(image)
    session.commit()
    session.refresh(image)
    return image


@router.post("/{product_id}/upload", status_code=201)
def upload_product_image(product_id: int, file: UploadFile = File(...), session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    if not session.get(Product, product_id):
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))
    # Format va hajm fayl mazmuni bo'yicha tekshiriladi (kengaytmaga ishonmaymiz).
    data, mime, ext = read_image(file, MAX_IMAGE_BYTES, lang)
    key = f"products/{product_id}_{uuid.uuid4().hex}{ext}"
    # MinIO ga urinish, fallback static/media
    url = upload_bytes(data, key, content_type=mime)
    if not url:
        media_dir = os.path.join("static", "media")
        os.makedirs(media_dir, exist_ok=True)
        filename = f"{product_id}_{uuid.uuid4().hex}{ext}"
        path = os.path.join(media_dir, filename)
        with open(path, "wb") as f:
            f.write(data)
        url = f"/static/media/{filename}"
    img = ProductImage(image_url=url, product_id=product_id)
    session.add(img)
    session.commit()
    session.refresh(img)
    return img
