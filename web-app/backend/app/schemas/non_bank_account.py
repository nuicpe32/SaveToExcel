from pydantic import BaseModel, Field
from typing import Optional
from datetime import date, datetime

# Base Schema
class NonBankAccountBase(BaseModel):
    """Base schema สำหรับ Non-Bank Account"""
    criminal_case_id: int
    non_bank_id: Optional[int] = None
    
    # ข้อมูลเอกสาร
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    document_date_thai: Optional[str] = None
    
    # ข้อมูลผู้ให้บริการและบัญชี
    provider_name: str = Field(..., description="ชื่อผู้ให้บริการ")
    account_number: str = Field(..., description="เลขที่บัญชี/หมายเลขผู้ใช้")
    account_name: Optional[str] = None
    account_owner: Optional[str] = None
    
    # ข้อมูลคดี
    complainant: Optional[str] = None
    victim_name: Optional[str] = None  # deprecated
    case_id: Optional[str] = None
    
    # ช่วงเวลาที่ต้องการข้อมูล
    time_period: Optional[str] = None
    
    # การส่งหมายเรียก
    delivery_date: Optional[date] = None
    delivery_month: Optional[str] = None
    delivery_time: Optional[str] = None
    
    # สถานะ
    reply_status: bool = False
    status: str = "pending"
    
    # การอายัด
    is_frozen: bool = False

# Create Schema
class NonBankAccountCreate(NonBankAccountBase):
    """Schema สำหรับสร้าง Non-Bank Account ใหม่"""
    pass

# Update Schema
class NonBankAccountUpdate(BaseModel):
    """Schema สำหรับแก้ไข Non-Bank Account"""
    non_bank_id: Optional[int] = None
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    document_date_thai: Optional[str] = None
    provider_name: Optional[str] = None
    account_number: Optional[str] = None
    account_name: Optional[str] = None
    account_owner: Optional[str] = None
    complainant: Optional[str] = None
    victim_name: Optional[str] = None
    case_id: Optional[str] = None
    time_period: Optional[str] = None
    delivery_date: Optional[date] = None
    delivery_month: Optional[str] = None
    delivery_time: Optional[str] = None
    reply_status: Optional[bool] = None
    status: Optional[str] = None
    is_frozen: Optional[bool] = None

# Response Schema
class NonBankAccountResponse(NonBankAccountBase):
    """Schema สำหรับ response Non-Bank Account"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None

    class Config:
        from_attributes = True

# Pagination Response
class NonBankAccountPaginationResponse(BaseModel):
    """Schema สำหรับ pagination response"""
    items: list[NonBankAccountResponse]
    total: int
    skip: int
    limit: int

    class Config:
        from_attributes = True

