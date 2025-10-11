from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class NonBankBase(BaseModel):
    """Base schema สำหรับ NonBank"""
    company_name: str
    company_name_short: Optional[str] = None
    
    # Address
    company_address: Optional[str] = None
    soi: Optional[str] = None
    moo: Optional[str] = None
    road: Optional[str] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    
    # Contact
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Status
    is_active: Optional[bool] = True

class NonBankCreate(NonBankBase):
    """Schema สำหรับสร้าง NonBank ใหม่"""
    pass

class NonBankUpdate(BaseModel):
    """Schema สำหรับแก้ไข NonBank"""
    company_name: Optional[str] = None
    company_name_short: Optional[str] = None
    
    # Address
    company_address: Optional[str] = None
    soi: Optional[str] = None
    moo: Optional[str] = None
    road: Optional[str] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    
    # Contact
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    
    # Status
    is_active: Optional[bool] = None

class NonBankResponse(NonBankBase):
    """Schema สำหรับ Response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

