"""
category.py — kategoriyalar CRUD
GET public, POST/PUT/DELETE faqat admin
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from apps.database import get_session
from apps.i18n import get_lang, t
from apps.dependencies import require_admin
from apps.forms import CategoryForm
from apps.models import Category, User

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/")
@router.get("", include_in_schema=False)
def list_categories(session: Session = Depends(get_session)):
    return session.exec(select(Category)).all()


@router.get("/{category_id}")
def get_category(category_id: int, session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    cat = session.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail=t("category_not_found", lang))
    # mahsulotlari bilan birga qaytaramiz (lazy load)
    return cat


@router.post("/", status_code=201)
@router.post("", status_code=201, include_in_schema=False)
def create_category(form: CategoryForm, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    # nom bandmi?
    if session.exec(select(Category).where(Category.name == form.name)).first():
        raise HTTPException(status_code=409, detail=t("category_name_taken", lang))
    cat = Category(name=form.name, description=form.description, parent_id=form.parent_id)
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@router.put("/{category_id}")
def update_category(category_id: int, form: CategoryForm, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    cat = session.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail=t("category_not_found", lang))
    cat.name = form.name
    cat.description = form.description
    cat.parent_id = form.parent_id
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat


@router.delete("/{category_id}")
def delete_category(category_id: int, session: Session = Depends(get_session), admin: User = Depends(require_admin), lang: str = Depends(get_lang)):
    cat = session.get(Category, category_id)
    if not cat:
        raise HTTPException(status_code=404, detail=t("category_not_found", lang))
    session.delete(cat)
    session.commit()
    return {"message": t("deleted", lang)}
