from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, ARRAY, JSON, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.functions import func

import random

from app.db.base import Base

class Store(Base):
    __tablename__ = "stores"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, unique=True, index=True)
    description = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    address = Column(String, nullable=True)
    coordinates = Column(String, nullable=True)
    url = Column(String, nullable=True)

    products = relationship("Product", back_populates="store")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    products = relationship("Product", back_populates="category")
    subcategories = relationship("Subcategory", back_populates="category")


class Subcategory(Base):
    __tablename__ = "subcategories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"))

    category = relationship("Category", back_populates="subcategories")
    products = relationship("Product", back_populates="subcategory")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    images = Column(ARRAY(String))
    thumbnail = Column(String, nullable=True)
    date = Column(DateTime, default=func.now())
    popularity = Column(Float, default=0.0)
    specifications = Column(JSON, default={})
    
    store_id = Column(Integer, ForeignKey("stores.id"))
    store = relationship("Store", back_populates="products")

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="products")

    subcategory_id = Column(Integer, ForeignKey("subcategories.id"))
    subcategory = relationship("Subcategory", back_populates="products")