from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductInDB
from app.db.base import get_db
from app.crud import product as crud_product


router = APIRouter()


@router.get("/{id}/", response_model=ProductInDB)
def get_store(
    *,
    db: Session = Depends(get_db),
    id: int = Path(...),
):
    product = crud_product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product is not found")
    return product

@router.get("/", response_model=List[ProductInDB])
def get_stores(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    products = crud_product.get_multi(db, skip=skip, limit=limit)
    return products