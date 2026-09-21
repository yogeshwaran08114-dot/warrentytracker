from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.schemas.common import ApiResponse
from app.schemas.warranty import WarrantyResponse, WarrantyStatus
from app.services import warranty as service

router = APIRouter()

@router.get("/{registration_id}", response_model=ApiResponse[WarrantyResponse])
def warranty_details(registration_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ApiResponse(data=service.get_warranty(db, user.id, registration_id))

@router.get("/{registration_id}/status", response_model=ApiResponse[WarrantyStatus])
def warranty_status(registration_id: int, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ApiResponse(data=service.get_status(db, user.id, registration_id))
