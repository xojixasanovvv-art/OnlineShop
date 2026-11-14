"""
address.py — manzillar
Foydalanuvchi faqat o'z manzilini ko'ra/o'zgartira oladi
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from apps.database import get_session
from apps.dependencies import get_current_user
from apps.forms import AddressForm
from apps.i18n import get_lang, t
from apps.models import Address, User

router = APIRouter(prefix="/addresses", tags=["Addresses"])


@router.get("/")
@router.get("", include_in_schema=False)
def list_addresses(current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    return session.exec(select(Address).where(Address.user_id == current_user.id)).all()


@router.post("/", status_code=201)
@router.post("", status_code=201, include_in_schema=False)
def create_address(form: AddressForm, current_user: User = Depends(get_current_user), session: Session = Depends(get_session)):
    addr = Address(**form.model_dump(), user_id=current_user.id)
    session.add(addr)
    session.commit()
    session.refresh(addr)
    return addr


@router.put("/{address_id}")
def update_address(address_id: int, form: AddressForm, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    addr = session.get(Address, address_id)
    if not addr:
        raise HTTPException(status_code=404, detail=t("address_not_found", lang))
    if addr.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=t("not_your_address", lang))
    for k, v in form.model_dump().items():
        setattr(addr, k, v)
    session.add(addr)
    session.commit()
    session.refresh(addr)
    return addr


@router.delete("/{address_id}")
def delete_address(address_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    addr = session.get(Address, address_id)
    if not addr:
        raise HTTPException(status_code=404, detail=t("address_not_found", lang))
    if addr.user_id != current_user.id:
        raise HTTPException(status_code=403, detail=t("not_your_address", lang))
    session.delete(addr)
    session.commit()
    return {"message": t("deleted", lang)}
