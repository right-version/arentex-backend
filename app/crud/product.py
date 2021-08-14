from typing import List, Optional

from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import Product
from app.schemas import StoreCreate, ProductInDB


def get(db: Session, id: int) -> Optional[ProductInDB]:
    return db.query(Product).get(id)

def get_multi(db: Session, *, skip: int = 0, limit: int = 100) -> Optional[ProductInDB]:
    return db.query(Product).offset(skip).limit(limit).all()

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