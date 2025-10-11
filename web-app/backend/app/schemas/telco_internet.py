from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class TelcoInternetBase(BaseModel):
    """Base schema สำหรับ TelcoInternet"""
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

class TelcoInternetCreate(TelcoInternetBase):
    """Schema สำหรับสร้าง TelcoInternet ใหม่"""
    pass

class TelcoInternetUpdate(BaseModel):
    """Schema สำหรับแก้ไข TelcoInternet"""
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

class TelcoInternetResponse(TelcoInternetBase):
    """Schema สำหรับ Response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

