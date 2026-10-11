from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.deps import Base


class Warranty(Base):
    __tablename__ = "warranties"

    id = Column(Integer, primary_key=True, index=True)

    registration_id = Column(Integer, ForeignKey("registrations.id"), nullable=False, unique=True, index=True)
    warranty_type = Column(String(100))
    warranty_months = Column(Integer, nullable=False)
    terms = Column(Text)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    registration = relationship("Registration", back_populates="warranty")