from pydantic import BaseModel, EmailStr, Field, ConfigDict, model_validator
from datetime import datetime
from typing import Optional


class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None
    mobile_number: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=128)
    confirm_password: str = Field(..., min_length=8, max_length=128)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self


class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    mobile_number: Optional[str] = None


class UserInDB(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    is_verified: bool
    role: str
    created_at: datetime
    updated_at: Optional[datetime] = None


class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    role: str
    created_at: datetime
