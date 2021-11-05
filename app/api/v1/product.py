from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import ProductInDB, ProductPaginationPage
from app.db.base import get_db
from app.crud import product as crud_product


router = APIRouter()


@router.get("/{id}/", response_model=ProductInDB)
def get_product(
    *,
    db: Session = Depends(get_db),
    id: int = Path(...),
):
    product = crud_product.get(db=db, id=id)
    if not product:
        raise HTTPException(status_code=404, detail="Product is not found")
    return product

# @router.get("/", response_model=List[ProductInDB])
@router.get("/", response_model=ProductPaginationPage)
def get_products(
    db: Session = Depends(get_db), 
    skip: int = 0, 
    limit: int = 10,
    category: Optional[int] = None,
    subcategory: Optional[int] = None,
    store: Optional[int] = None,
    max_price: Optional[int] = None,
    min_price: Optional[int] = None,
    search: Optional[str] = None
): 
    total, products = crud_product.get_multi(
        db, 
        skip=skip, 
        limit=limit,
        category=category,
        subcategory=subcategory,
        store=store,
        max_price=max_price,
        min_price=min_price,
        title=search
    )

    if products:
        max_price = max(products, key=lambda x: x.price)
        max_price = max_price.price
        min_price = min(products, key=lambda x: x.price)
        min_price = min_price.price
    else:
        max_price = 0
        min_price = 0

    response = {
        "items": products,
        "total": total,
        "skip": skip,
        "limit": limit,
        "max_price": max_price,
        "min_price": min_price
    }
    return response