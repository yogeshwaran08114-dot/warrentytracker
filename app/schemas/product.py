from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProductCreate(BaseModel):
    product_name: str = Field(min_length=1, max_length=255)
    brand: str = Field(min_length=1, max_length=255)
    model_number: str = Field(min_length=1, max_length=255)
    category_id: int
    default_warranty_months: int = Field(gt=0, le=120)


class ProductResponse(ProductCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    created_at: datetime
