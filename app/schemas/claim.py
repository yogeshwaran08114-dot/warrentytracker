from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field


class ClaimCreate(BaseModel):
    registration_id: int
    issue_description: str = Field(min_length=5, max_length=5000)


class ClaimUpdate(BaseModel):
    status: str
    admin_remarks: str | None = None


class ClaimResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    registration_id: int
    user_id: int
    issue_description: str
    claim_date: date
    status: str
    admin_remarks: str | None
    updated_at: datetime | None
