"""
database.py — DB bilan ishlash uchun yagona joy
- engine bitta joyda yaratiladi (DRY)
- get_session() — har bir endpoint uchun dependency
- create_db_and_tables() — jadvallarni yaratish
"""
from sqlmodel import SQLModel, Session, create_engine

from apps.config import DATABASE_URL

# echo=False — SQL loglarni konsolga chiqarmaydi (toza bo'lishi uchun)
engine = create_engine(DATABASE_URL, echo=False)


def get_session():
    """FastAPI dependency: har bir so'rov uchun alohida Session"""
    with Session(engine) as session:
        yield session


def create_db_and_tables():
    """Dastur ishga tushganda barcha jadvallarni yaratadi"""
    import apps.models  # noqa: F401 — modellarni import qilish shart
    SQLModel.metadata.create_all(engine)
