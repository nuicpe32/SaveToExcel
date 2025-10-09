from pydantic import BaseModel, EmailStr, validator
from typing import List, Optional
from datetime import datetime

class UserRegistrationBase(BaseModel):
    # Police information
    rank_id: int
    full_name: str
    position: Optional[str] = None
    email: EmailStr
    phone_number: Optional[str] = None
    line_id: Optional[str] = None
    
    # Role selection (multiple roles as checkboxes)
    role_ids: List[int]
    
    # Account credentials
    username: str
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('รหัสผ่านต้องมีอย่างน้อย 6 ตัวอักษร')
        return v
    
    @validator('username')
    def validate_username(cls, v):
        if len(v) < 3:
            raise ValueError('ชื่อผู้ใช้ต้องมีอย่างน้อย 3 ตัวอักษร')
        return v

class UserRegistrationCreate(UserRegistrationBase):
    pass

class PoliceRankResponse(BaseModel):
    id: int
    rank_full: str
    rank_short: str
    rank_english: str
    
    class Config:
        from_attributes = True

class UserRoleResponse(BaseModel):
    id: int
    role_name: str
    role_display: str
    role_description: Optional[str] = None
    
    class Config:
        from_attributes = True

class UserRegistrationResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    position: Optional[str] = None
    phone_number: Optional[str] = None
    line_id: Optional[str] = None
    is_active: bool
    is_approved: bool
    created_at: datetime
    rank: Optional[PoliceRankResponse] = None
    role: Optional[UserRoleResponse] = None
    role_mappings: List[dict] = []
    
    class Config:
        from_attributes = True
