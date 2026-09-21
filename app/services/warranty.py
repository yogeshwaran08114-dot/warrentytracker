from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.registration import Registration


def get_warranty(db: Session, user_id: int, registration_id: int):
    registration = db.query(Registration).filter(Registration.id == registration_id, Registration.user_id == user_id).first()
    if not registration or not registration.warranty:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Warranty not found")
    return registration.warranty


def get_status(db: Session, user_id: int, registration_id: int):
    registration = db.query(Registration).filter(Registration.id == registration_id, Registration.user_id == user_id).first()
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    return {"registration_id": registration.id, "status": "ACTIVE" if date.today() <= registration.warranty_expiry_date else "EXPIRED", "expiry_date": registration.warranty_expiry_date}
