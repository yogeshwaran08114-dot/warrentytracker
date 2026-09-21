import calendar
from datetime import date
from fastapi import HTTPException, status
from sqlalchemy.orm import Session, joinedload
from app.models.product import Product
from app.models.registration import Registration
from app.models.warranty import Warranty
from app.schemas.registration import RegistrationCreate


def add_months(value: date, months: int) -> date:
    month_index = value.month - 1 + months
    year = value.year + month_index // 12
    month = month_index % 12 + 1
    day = min(value.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def create_registration(db: Session, user_id: int, data: RegistrationCreate):
    product = db.query(Product).filter(Product.id == data.product_id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    if db.query(Registration).filter(Registration.serial_number == data.serial_number).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Serial number already registered")
    expiry = add_months(data.purchase_date, product.default_warranty_months)
    registration = Registration(user_id=user_id, product_id=product.id, serial_number=data.serial_number,
                                purchase_date=data.purchase_date, warranty_start_date=data.purchase_date,
                                warranty_expiry_date=expiry)
    registration.warranty = Warranty(registration=registration, warranty_type="Manufacturer",
                                     warranty_months=product.default_warranty_months,
                                     terms="See manufacturer terms")
    db.add(registration)
    db.commit()
    return db.query(Registration).options(joinedload(Registration.product)).filter(Registration.id == registration.id).one()


def list_user_registrations(db: Session, user_id: int):
    return db.query(Registration).options(joinedload(Registration.product)).filter(Registration.user_id == user_id).all()


def get_user_registration(db: Session, user_id: int, registration_id: int):
    registration = db.query(Registration).options(joinedload(Registration.product)).filter(
        Registration.id == registration_id, Registration.user_id == user_id).first()
    if not registration:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found")
    return registration
