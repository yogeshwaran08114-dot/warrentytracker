from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.deps import Base


class Registration(Base):
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    serial_number = Column(String(255), nullable=False, index=True)
    purchase_date = Column(Date, nullable=False)
    warranty_start_date = Column(Date, nullable=False)
    warranty_expiry_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="registrations")
    product = relationship("Product", back_populates="registrations")
    warranty = relationship("Warranty", back_populates="registration", uselist=False, cascade="all, delete-orphan")
    claims = relationship("Claim", back_populates="registration", cascade="all, delete-orphan")
