from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class PoliceRankInfo(BaseModel):
    id: int
    rank_short: str
    rank_full: str
    rank_english: str

    class Config:
        from_attributes = True

class UserRoleInfo(BaseModel):
    id: int
    role_name: str
    role_display: str
    role_description: Optional[str] = None

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    is_approved: bool
    position: Optional[str] = None
    phone_number: Optional[str] = None
    line_id: Optional[str] = None
    rank: Optional[PoliceRankInfo] = None
    role: Optional[UserRoleInfo] = None
    created_at: datetime

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None