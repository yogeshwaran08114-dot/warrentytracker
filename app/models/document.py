from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.deps import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)

    product_id = Column(
        Integer,
        ForeignKey("products.id"),
        nullable=False,
        index=True
    )

    file_name = Column(String(255), nullable=False)
    file_path = Column(String(500), nullable=False)
    document_type = Column(String(100))
    uploaded_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    product = relationship("Product", back_populates="documents")