from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PaymentGatewayBase(BaseModel):
    """Base schema สำหรับ Payment Gateway"""
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
    is_active: bool = True

class PaymentGatewayCreate(PaymentGatewayBase):
    """Schema สำหรับสร้าง Payment Gateway ใหม่"""
    pass

class PaymentGatewayUpdate(BaseModel):
    """Schema สำหรับอัพเดท Payment Gateway"""
    company_name: Optional[str] = None
    company_name_short: Optional[str] = None
    company_address: Optional[str] = None
    soi: Optional[str] = None
    moo: Optional[str] = None
    road: Optional[str] = None
    sub_district: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    website: Optional[str] = None
    is_active: Optional[bool] = None

class PaymentGateway(PaymentGatewayBase):
    """Schema สำหรับแสดงข้อมูล Payment Gateway"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

