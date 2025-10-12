from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# Base Schema
class PaymentGatewayAccountBase(BaseModel):
    """Base schema สำหรับ Payment Gateway Account"""
    criminal_case_id: int
    payment_gateway_id: Optional[int] = None
    bank_id: Optional[int] = None  # ธนาคารที่เปิดบัญชี
    
    # ข้อมูลเอกสาร
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # ข้อมูลบัญชี
    account_number: str = Field(..., description="เลขที่บัญชี/หมายเลขผู้ใช้")
    account_name: Optional[str] = None
    
    # ช่วงเวลาที่ต้องการข้อมูล
    time_period: Optional[str] = None
    
    # การส่งหมายเรียก
    delivery_date: Optional[date] = None
    
    # สถานะ
    reply_status: bool = False
    status: str = "pending"

# Create Schema
class PaymentGatewayAccountCreate(PaymentGatewayAccountBase):
    """Schema สำหรับสร้าง Payment Gateway Account ใหม่"""
    pass

# Update Schema
class PaymentGatewayAccountUpdate(BaseModel):
    """Schema สำหรับแก้ไข Payment Gateway Account"""
    payment_gateway_id: Optional[int] = None
    bank_id: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    account_number: Optional[str] = None
    account_name: Optional[str] = None
    time_period: Optional[str] = None
    delivery_date: Optional[date] = None
    reply_status: Optional[bool] = None
    status: Optional[str] = None

# Response Schema
class PaymentGatewayAccountResponse(PaymentGatewayAccountBase):
    """Schema สำหรับ response Payment Gateway Account"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None

    class Config:
        from_attributes = True

# Pagination Response
class PaymentGatewayAccountPaginationResponse(BaseModel):
    """Schema สำหรับ pagination response"""
    items: list[PaymentGatewayAccountResponse]
    total: int
    skip: int
    limit: int

    class Config:
        from_attributes = True

