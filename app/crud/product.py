from typing import List, Optional

from numpy import show_config

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
    min_price: Optional[int] = None,
    title: Optional[str] = None,
    sort: Optional[str] = None
) -> Optional[ProductInDB]:
    query = db.query(Product)
    if category:
        query = query.filter(Product.category_id == category)
    if title:
        search = "%{}%".format(title)
        query = query.filter(Product.title.ilike(search))
    if subcategory:
        query = query.filter(Product.subcategory_id == subcategory)
    if store:
        query = query.filter(Product.store_id == store)
    
    products = query.all()
    if products:
        total_max_price = max(products, key=lambda x: x.price)
        total_max_price = total_max_price.price if total_max_price else 0
        total_min_price = min(products, key=lambda x: x.price)
        total_min_price = total_min_price.price if total_min_price else 0
    else:
        total_max_price = 0
        total_min_price = 0
    
    if max_price:
        query = query.filter(Product.price <= max_price)
    if min_price:
        query = query.filter(Product.price >= min_price)
    if sort:
        if sort == "new":
            query = query.order_by(Product.date.desc())
        elif sort == "old":
            query = query.order_by(Product.date.asc())
        elif sort == "expensive":
            query = query.order_by(Product.price.desc())
        elif sort == "cheap":
            query = query.order_by(Product.price.asc())
        elif sort == "popular":
            query = query.order_by(Product.popularity.desc())
    total = query.count()
    return total, total_max_price, total_min_price, query.offset(skip).limit(limit).all()


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