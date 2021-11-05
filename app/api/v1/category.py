from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy import func, text
from sqlalchemy.orm import Session

from app.models import Category, Product
from app.schemas import CategoryInDB
from app.db.base import get_db


router = APIRouter()


# @router.get("/", response_model=List[CategoryInDB])
# def get_categories(db: Session = Depends(get_db)):
#     categories = db.query(Category).all()
#     return categories


@router.get("/", response_model=List[CategoryInDB])
def get_top_categories(db: Session = Depends(get_db)):
    categories = (
        db.query(Category, func.count(Product.category_id).label("total"))
        .outerjoin(Product)
        .group_by(Category)
        .order_by(text("total DESC"))
        .all()
    )
    categories = [c[0] for c in categories]
    return categories
