from fastapi import APIRouter
from app.api.v1.endpoints import auth, users, categories, products, registrations, warranties, claims, admin

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(categories.router, prefix="/categories", tags=["categories"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(registrations.router, prefix="/registrations", tags=["registrations"])
api_router.include_router(warranties.router, prefix="/warranties", tags=["warranties"])
api_router.include_router(claims.router, prefix="/claims", tags=["claims"])
api_router.include_router(admin.router, prefix="/admin", tags=["admin"])
