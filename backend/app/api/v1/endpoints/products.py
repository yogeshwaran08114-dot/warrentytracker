from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.schemas.common import ApiResponse
from app.schemas.product import ProductCreate, ProductResponse
from app.services import product as service

router = APIRouter()

@router.get("", response_model=ApiResponse[list[ProductResponse]])
def read_products(db: Session = Depends(get_db)):
    return ApiResponse(data=service.list_products(db))

@router.post("", response_model=ApiResponse[ProductResponse], status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=service.create_product(db, data), message="Product created")

@router.get("/{product_id}", response_model=ApiResponse[ProductResponse])
def read_product(product_id: int, db: Session = Depends(get_db)):
    return ApiResponse(data=service.get_product(db, product_id))

@router.put("/{product_id}", response_model=ApiResponse[ProductResponse])
def update_product(product_id: int, data: ProductCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=service.update_product(db, product_id, data), message="Product updated")

@router.delete("/{product_id}", response_model=ApiResponse[None])
def delete_product(product_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    service.delete_product(db, product_id)
    return ApiResponse(data=None, message="Product deleted")
