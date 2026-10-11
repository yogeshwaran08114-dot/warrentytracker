from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.deps import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), unique=True, nullable=False)
    description = Column(String(500))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    products = relationship("Product", back_populates="category")
