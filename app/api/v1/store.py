from typing import List

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app.models import Store
from app.schemas import StoreCreate, StoreInDB
from app.db.base import get_db
from app.crud import store as crud_store


router = APIRouter()

@router.get("/{id}/", response_model=StoreInDB)
def get_store(
    *,
    db: Session = Depends(get_db),
    id: int = Path(...),
):
    store = crud_store.get(db=db, id=id)
    if not store:
        raise HTTPException(status_code=404, detail="Store is not found")
    return store

@router.get("/")
def get_stores(db: Session = Depends(get_db), skip: int = 0, limit: int = 10):
    stores = crud_store.get_multi(db, skip=skip, limit=limit)
    return stores

@router.post("/", response_model=StoreInDB, status_code=201)
def create_store(*, db: Session = Depends(get_db), payload: StoreCreate):
    store = crud_store.post(db=db, payload=payload)
    if not store:
        raise HTTPException(status_code=409, detail="Store aleready exists")
    return store