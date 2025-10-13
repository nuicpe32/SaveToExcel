from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class TelcoMobileAccountBase(BaseModel):
    # Document Information
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Telco Information
    provider_name: str  # ชื่อผู้ให้บริการ (บังคับ)
    phone_number: str   # หมายเลขโทรศัพท์ (บังคับ)

    # Additional Information
    time_period: Optional[str] = None  # ช่วงเวลาที่ขอข้อมูล
    
    # Delivery Information
    delivery_date: Optional[date] = None  # กำหนดให้ส่งเอกสาร
    
    # Status and Response
    reply_status: Optional[bool] = False
    days_since_sent: Optional[int] = None
    
    # Additional Information
    notes: Optional[str] = None
    status: Optional[str] = "pending"

class TelcoMobileAccountCreate(TelcoMobileAccountBase):
    criminal_case_id: int  # REQUIRED field
    telco_mobile_id: Optional[int] = None  # FK to telco_mobile table

class TelcoMobileAccountUpdate(BaseModel):
    # Document Information
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Telco Information
    provider_name: Optional[str] = None
    phone_number: Optional[str] = None

    # Additional Information
    time_period: Optional[str] = None
    
    # Delivery Information
    delivery_date: Optional[date] = None
    
    # Status and Response
    reply_status: Optional[bool] = None
    days_since_sent: Optional[int] = None
    
    # Additional Information
    notes: Optional[str] = None
    status: Optional[str] = None
    
    # Foreign Keys
    criminal_case_id: Optional[int] = None
    telco_mobile_id: Optional[int] = None

class CriminalCaseInfo(BaseModel):
    id: int
    case_id: Optional[str] = None
    case_number: Optional[str] = None
    complainant: Optional[str] = None

    class Config:
        from_attributes = True

class TelcoMobileInfo(BaseModel):
    id: int
    company_name: str
    company_name_short: Optional[str] = None

    class Config:
        from_attributes = True

class TelcoMobileAccountResponse(TelcoMobileAccountBase):
    id: int
    criminal_case_id: Optional[int] = None
    telco_mobile_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    criminal_case: Optional[CriminalCaseInfo] = None
    telco_mobile: Optional[TelcoMobileInfo] = None

    class Config:
        from_attributes = True

class TelcoMobileAccountPaginationResponse(BaseModel):
    items: List[TelcoMobileAccountResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

