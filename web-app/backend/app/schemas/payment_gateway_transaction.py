from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class PaymentGatewayTransactionBase(BaseModel):
    """Base schema สำหรับรายละเอียดการโอนเงิน Payment Gateway"""
    criminal_case_id: int
    payment_gateway_account_id: int
    
    # บัญชีต้นทาง (FK to banks)
    source_bank_id: Optional[int] = None
    source_account_number: Optional[str] = None
    source_account_name: Optional[str] = None
    
    # บัญชีปลายทาง (FK to banks)
    destination_bank_id: Optional[int] = None
    destination_account_number: Optional[str] = None
    destination_account_name: Optional[str] = None
    
    # ข้อมูลการโอน
    transfer_date: Optional[date] = None
    transfer_time: Optional[str] = None
    transfer_amount: Optional[Decimal] = None
    
    # หมายเหตุ
    note: Optional[str] = None

class PaymentGatewayTransactionCreate(PaymentGatewayTransactionBase):
    """Schema สำหรับสร้างรายละเอียดการโอน"""
    pass

class PaymentGatewayTransactionUpdate(BaseModel):
    """Schema สำหรับอัพเดทรายละเอียดการโอน"""
    source_bank_id: Optional[int] = None
    source_account_number: Optional[str] = None
    source_account_name: Optional[str] = None
    
    destination_bank_id: Optional[int] = None
    destination_account_number: Optional[str] = None
    destination_account_name: Optional[str] = None
    
    transfer_date: Optional[date] = None
    transfer_time: Optional[str] = None
    transfer_amount: Optional[Decimal] = None
    
    note: Optional[str] = None

class PaymentGatewayTransaction(PaymentGatewayTransactionBase):
    """Schema สำหรับแสดงข้อมูลรายละเอียดการโอน"""
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    
    class Config:
        from_attributes = True

