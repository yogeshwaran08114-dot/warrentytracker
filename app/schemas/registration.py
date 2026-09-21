from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field
from app.schemas.product import ProductResponse


class RegistrationCreate(BaseModel):
    product_id: int
    serial_number: str = Field(min_length=1, max_length=255)
    purchase_date: date


class RegistrationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    product: ProductResponse
    serial_number: str
    purchase_date: date
    warranty_start_date: date
    warranty_expiry_date: date
    created_at: datetime
