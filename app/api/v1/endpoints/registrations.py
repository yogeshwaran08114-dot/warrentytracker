from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.schemas.common import ApiResponse
from app.schemas.registration import RegistrationCreate, RegistrationResponse
from app.services import registration as service

router = APIRouter()

@router.post("", response_model=ApiResponse[RegistrationResponse], status_code=status.HTTP_201_CREATED)
def register_product(data: RegistrationCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ApiResponse(data=service.create_registration(db, user.id, data), message="Product registered")

@router.get("/my", response_model=ApiResponse[list[RegistrationResponse]])
def my_registrations(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ApiResponse(data=service.list_user_registrations(db, user.id))

@router.get("/{registration_id}", response_model=ApiResponse[RegistrationResponse])
def registration_details(registration_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ApiResponse(data=service.get_user_registration(db, user.id, registration_id))
