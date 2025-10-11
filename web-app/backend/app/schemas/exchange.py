from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class ExchangeBase(BaseModel):
    """Base schema สำหรับ Exchange"""
    company_name: str
    company_name_short: Optional[str] = None
    company_name_alt: Optional[str] = None
    
    # Address
    building_name: Optional[str] = None
    company_address: Optional[str] = None
    floor: Optional[str] = None
    unit: Optional[str] = None
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
    
    # License
    license_number: Optional[str] = None
    license_date: Optional[date] = None
    
    # Status
    is_active: Optional[bool] = True

class ExchangeCreate(ExchangeBase):
    """Schema สำหรับสร้าง Exchange ใหม่"""
    pass

class ExchangeUpdate(BaseModel):
    """Schema สำหรับแก้ไข Exchange"""
    company_name: Optional[str] = None
    company_name_short: Optional[str] = None
    company_name_alt: Optional[str] = None
    
    # Address
    building_name: Optional[str] = None
    company_address: Optional[str] = None
    floor: Optional[str] = None
    unit: Optional[str] = None
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
    
    # License
    license_number: Optional[str] = None
    license_date: Optional[date] = None
    
    # Status
    is_active: Optional[bool] = None

class ExchangeResponse(ExchangeBase):
    """Schema สำหรับ Response"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

