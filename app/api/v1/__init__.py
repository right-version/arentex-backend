from fastapi import APIRouter

from app.api.v1 import product, store, category, search

api_router = APIRouter()
api_router.include_router(product.router, prefix="/product", tags=["product"])
api_router.include_router(store.router, prefix="/store", tags=["store"])
api_router.include_router(category.router, prefix="/category", tags=["category"])
api_router.include_router(search.router, prefix="/search", tags=["search"])