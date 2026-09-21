from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.schemas.category import CategoryCreate, CategoryResponse
from app.schemas.common import ApiResponse
from app.services import category as service

router = APIRouter()

@router.get("", response_model=ApiResponse[list[CategoryResponse]])
def read_categories(db: Session = Depends(get_db)):
    return ApiResponse(data=service.list_categories(db))

@router.post("", response_model=ApiResponse[CategoryResponse], status_code=status.HTTP_201_CREATED)
def create_category(data: CategoryCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=service.create_category(db, data), message="Category created")


@router.put("/{category_id}", response_model=ApiResponse[CategoryResponse])
def update_category(category_id: int, data: CategoryCreate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=service.update_category(db, category_id, data), message="Category updated")


@router.delete("/{category_id}", response_model=ApiResponse[None])
def delete_category(category_id: int, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    service.delete_category(db, category_id)
    return ApiResponse(data=None, message="Category deleted")
