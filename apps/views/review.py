"""
review.py — sharhlar
TZ 5.6: faqat sotib olgan foydalanuvchi sharh qoldira oladi
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from apps.database import get_session
from apps.dependencies import get_current_user
from apps.forms import ReviewForm
from apps.i18n import get_lang, t
from apps.models import Review, Product, Order, OrderItem, User

router = APIRouter(tags=["Reviews"])


@router.post("/products/{product_id}/reviews", status_code=201)
def create_review(product_id: int, form: ReviewForm, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    if not session.get(Product, product_id):
        raise HTTPException(status_code=404, detail=t("product_not_found", lang))
    orders = session.exec(select(Order).where(Order.user_id == current_user.id, Order.status != "cancelled")).all()
    has_bought = False
    for o in orders:
        items = session.exec(select(OrderItem).where(OrderItem.order_id == o.id, OrderItem.product_id == product_id)).first()
        if items:
            has_bought = True
            break
    if not has_bought:
        raise HTTPException(status_code=403, detail=t("only_buyers_can_review", lang))
    review = Review(rating=form.rating, comment=form.comment, user_id=current_user.id, product_id=product_id)
    session.add(review)
    session.commit()
    session.refresh(review)
    return review


@router.get("/products/{product_id}/reviews")
def list_reviews(product_id: int, session: Session = Depends(get_session)):
    return session.exec(select(Review).where(Review.product_id == product_id)).all()


@router.delete("/reviews/{review_id}")
def delete_review(review_id: int, current_user: User = Depends(get_current_user), session: Session = Depends(get_session), lang: str = Depends(get_lang)):
    review = session.get(Review, review_id)
    if not review:
        raise HTTPException(status_code=404, detail=t("review_not_found", lang))
    if review.user_id != current_user.id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail=t("not_your_review", lang))
    session.delete(review)
    session.commit()
    return {"message": t("deleted", lang)}
