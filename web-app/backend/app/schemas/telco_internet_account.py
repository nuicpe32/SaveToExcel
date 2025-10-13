from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class TelcoInternetAccountBase(BaseModel):
    # Document Information
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Telco Internet Information
    provider_name: str      # ชื่อผู้ให้บริการ (บังคับ)
    ip_address: str         # IP Address (บังคับ)

    # Additional Information
    datetime_used: Optional[datetime] = None  # วันเวลาที่ใช้งาน
    
    # Delivery Information
    delivery_date: Optional[date] = None  # กำหนดให้ส่งเอกสาร
    
    # Status and Response
    reply_status: Optional[bool] = False
    days_since_sent: Optional[int] = None
    
    # Additional Information
    notes: Optional[str] = None
    status: Optional[str] = "pending"

class TelcoInternetAccountCreate(TelcoInternetAccountBase):
    criminal_case_id: int  # REQUIRED field
    telco_internet_id: Optional[int] = None  # FK to telco_internet table

class TelcoInternetAccountUpdate(BaseModel):
    # Document Information
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Telco Internet Information
    provider_name: Optional[str] = None
    ip_address: Optional[str] = None

    # Additional Information
    datetime_used: Optional[datetime] = None
    
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
    telco_internet_id: Optional[int] = None

class CriminalCaseInfo(BaseModel):
    id: int
    case_id: Optional[str] = None
    case_number: Optional[str] = None
    complainant: Optional[str] = None

    class Config:
        from_attributes = True

class TelcoInternetInfo(BaseModel):
    id: int
    company_name: str
    company_name_short: Optional[str] = None

    class Config:
        from_attributes = True

class TelcoInternetAccountResponse(TelcoInternetAccountBase):
    id: int
    criminal_case_id: Optional[int] = None
    telco_internet_id: Optional[int] = None
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    criminal_case: Optional[CriminalCaseInfo] = None
    telco_internet: Optional[TelcoInternetInfo] = None

    class Config:
        from_attributes = True

class TelcoInternetAccountPaginationResponse(BaseModel):
    items: List[TelcoInternetAccountResponse]
    total: int
    page: int
    per_page: int
    total_pages: int

