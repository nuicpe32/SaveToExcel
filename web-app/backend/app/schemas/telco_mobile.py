from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TelcoMobileBase(BaseModel):
    """Base schema สำหรับ TelcoMobile"""
    company_name: str
    company_name_short: Optional[str] = None
    
    # Address
    building_name: Optional[str] = None
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

class TelcoMobileCreate(TelcoMobileBase):
    """Schema สำหรับสร้าง TelcoMobile ใหม่"""
    pass

class TelcoMobileUpdate(BaseModel):
    """Schema สำหรับแก้ไข TelcoMobile"""
    company_name: Optional[str] = None
    company_name_short: Optional[str] = None
    
    # Address
    building_name: Optional[str] = None
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

class TelcoMobileResponse(TelcoMobileBase):
    """Schema สำหรับ Response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

