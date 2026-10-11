from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.core.deps import get_current_user, get_db
from app.schemas.claim import ClaimCreate, ClaimResponse
from app.schemas.common import ApiResponse
from app.services import claim as service

router = APIRouter()

@router.post("", response_model=ApiResponse[ClaimResponse], status_code=status.HTTP_201_CREATED)
def create_claim(data: ClaimCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ApiResponse(data=service.create_claim(db, user.id, data), message="Claim submitted")

@router.get("/my", response_model=ApiResponse[list[ClaimResponse]])
def my_claims(db: Session = Depends(get_db), user=Depends(get_current_user)):
    return ApiResponse(data=service.list_user_claims(db, user.id))
