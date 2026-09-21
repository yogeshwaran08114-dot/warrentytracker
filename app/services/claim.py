from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.claim import Claim
from app.models.registration import Registration
from app.schemas.claim import ClaimCreate, ClaimUpdate

VALID_STATUSES = {"Pending", "Approved", "Rejected", "Completed"}


def create_claim(db: Session, user_id: int, data: ClaimCreate):
    registration = db.query(Registration).filter(Registration.id == data.registration_id, Registration.user_id == user_id).first()
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    claim = Claim(registration_id=registration.id, user_id=user_id, issue_description=data.issue_description)
    db.add(claim)
    db.commit()
    db.refresh(claim)
    return claim


def list_user_claims(db: Session, user_id: int):
    return db.query(Claim).filter(Claim.user_id == user_id).order_by(Claim.claim_date.desc()).all()


def list_claims(db: Session):
    return db.query(Claim).order_by(Claim.claim_date.desc()).all()


def update_claim(db: Session, claim_id: int, data: ClaimUpdate):
    if data.status not in VALID_STATUSES:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Invalid claim status")
    claim = db.query(Claim).filter(Claim.id == claim_id).first()
    if not claim:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Claim not found")
    claim.status = data.status
    claim.admin_remarks = data.admin_remarks
    db.commit()
    db.refresh(claim)
    return claim
