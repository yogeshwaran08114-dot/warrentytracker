from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.deps import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    registration_id = Column(Integer, ForeignKey("registrations.id"), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    issue_description = Column(Text, nullable=False)
    claim_date = Column(Date, nullable=False, server_default=func.current_date())
    status = Column(String(30), nullable=False, default="Pending")
    admin_remarks = Column(Text)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    registration = relationship("Registration", back_populates="claims")
    user = relationship("User", back_populates="claims")
