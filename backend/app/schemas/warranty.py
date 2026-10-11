from datetime import date, datetime
from pydantic import BaseModel, ConfigDict


class WarrantyResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    registration_id: int
    warranty_type: str | None
    warranty_months: int
    terms: str | None
    created_at: datetime


class WarrantyStatus(BaseModel):
    registration_id: int
    status: str
    expiry_date: date
