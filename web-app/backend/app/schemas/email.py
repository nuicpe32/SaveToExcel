from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class EmailSendRequest(BaseModel):
    """Request schema สำหรับส่งหมายเรียกทางอีเมล์"""
    account_type: str  # 'non_bank', 'payment_gateway', 'telco_mobile', 'telco_internet', 'bank'
    account_id: int
    recipient_email: EmailStr
    document_type: str = 'summons'  # 'summons' or 'envelope'
    freeze_account: bool = False  # True = อายัดบัญชี, False = ไม่อายัดบัญชี

class EmailSendResponse(BaseModel):
    """Response schema หลังจากส่งอีเมล์"""
    status: str  # 'sent', 'failed', 'pending'
    message: str
    email_log_id: Optional[int] = None
    sent_at: Optional[datetime] = None
    pdf_filename: Optional[str] = None

class EmailLogResponse(BaseModel):
    """Response schema สำหรับประวัติการส่งอีเมล์"""
    id: int
    account_type: str
    account_id: int
    criminal_case_id: int
    recipient_email: str
    subject: str
    document_type: str
    status: str
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int
    opened_count: int
    created_at: datetime
    pdf_filename: Optional[str] = None

    class Config:
        from_attributes = True

class EmailHistoryResponse(BaseModel):
    """Response schema สำหรับประวัติการส่งอีเมล์ทั้งหมด"""
    total: int
    emails: list[EmailLogResponse]
