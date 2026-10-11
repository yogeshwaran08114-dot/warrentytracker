from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.deps import get_current_admin, get_db
from app.schemas.claim import ClaimResponse, ClaimUpdate
from app.schemas.common import ApiResponse
from app.schemas.registration import RegistrationResponse
from app.services import claim as claim_service
from app.services import registration as registration_service
from app.schemas.warranty import WarrantyResponse
from app.models.registration import Registration
from app.models.warranty import Warranty

router = APIRouter()

@router.get("/registrations", response_model=ApiResponse[list[RegistrationResponse]])
def all_registrations(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=db.query(Registration).all())

@router.get("/warranties", response_model=ApiResponse[list[WarrantyResponse]])
def all_warranties(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=db.query(Warranty).all())

@router.get("/claims", response_model=ApiResponse[list[ClaimResponse]])
def all_claims(db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=claim_service.list_claims(db))

@router.put("/claims/{claim_id}", response_model=ApiResponse[ClaimResponse])
def change_claim(claim_id: int, data: ClaimUpdate, db: Session = Depends(get_db), _=Depends(get_current_admin)):
    return ApiResponse(data=claim_service.update_claim(db, claim_id, data), message="Claim updated")
