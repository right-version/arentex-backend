from app.models.models import Store, Subcategory
from typing import List, Optional, Any

from pydantic import BaseModel


class StoreBase(BaseModel):
    title: str
    description: str
    phone: Optional[str] = None
    address: Optional[str] = None
    coordinates: Optional[str] = None
    url: Optional[str] = None


class StoreCreate(StoreBase):
    pass


class StoreInDB(StoreBase):
    id: int

    class Config:
        orm_mode = True


class CategoryBase(BaseModel):
    name: str


class CategoryInDB(CategoryBase):
    id: int

    class Config:
        orm_mode = True


class SubcategoryBase(BaseModel):
    name: str


class SubcategoryInDB(SubcategoryBase):
    id: int

    class Config:
        orm_mode = True
        

class ProductBase(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    images: list[str]
    thumbnail: Optional[str] = None
    specifications: Optional[Any] = None
    store_id: int
    category: CategoryInDB
    subcategory: SubcategoryInDB


class ProductCreate(ProductBase):
    pass


class ProductInDB(ProductBase):
    id: int

    class Config:
        orm_mode = True


# class UserBase(BaseModel):
#     email: str


# class UserCreate(UserBase):
#     password: str


# class User(UserBase):
#     id: int
#     is_active: bool
#     items: List[Item] = []

#     class Config:
#         orm_mode = True