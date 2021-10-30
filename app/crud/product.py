from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from app.models import Product
from app.schemas import StoreCreate, ProductInDB


def get(db: Session, id: int) -> Optional[ProductInDB]:
    return db.query(Product).get(id)

# TODO: запилить динамические фильтры
def get_multi(
    db: Session, 
    *, skip: int = 0, 
    limit: int = 100,
    category: Optional[int] = None,
    subcategory: Optional[int] = None,
    store: Optional[int] = None,
    max_price: Optional[int] = None,
    min_price: Optional[int] = None
) -> Optional[ProductInDB]:
    query = db.query(Product)
    if category:
        query = query.filter(Product.category_id == category)
    if subcategory:
        query = query.filter(Product.subcategory_id == subcategory)
    if store:
        query = query.filter(Product.store_id == store)
    if max_price:
        query = query.filter(Product.price <= max_price)
    if min_price:
        query = query.filter(Product.price >= min_price)
    total = query.count()
    return total, query.offset(skip).limit(limit).all()


# def post(db: Session, payload: StoreCreate) -> Optional[StoreInDB]:
#     exists = db.query(Store).filter_by(title=payload.title).first() is not None
#     if exists:
#         return None
#     else:
#         obj_in_data = jsonable_encoder(payload)
#         store = Store(**obj_in_data)
#         db.add(store)
#         db.commit()
#         db.refresh(store)
#         return store