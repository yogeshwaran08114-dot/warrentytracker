from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.deps import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)

    product_name = Column(String(255), nullable=False)
    brand = Column(String(255), nullable=False)
    model_number = Column(String(255), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False, index=True)
    default_warranty_months = Column(Integer, nullable=False, default=12)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    category = relationship("Category", back_populates="products")
    registrations = relationship("Registration", back_populates="product", cascade="all, delete-orphan")