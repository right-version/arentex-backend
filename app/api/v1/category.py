from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from sqlalchemy.orm import Session

from app.models import Category
from app.schemas import CategoryInDB
from app.db.base import get_db


router = APIRouter()


@router.get("/", response_model=List[CategoryInDB])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories