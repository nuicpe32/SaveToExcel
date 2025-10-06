from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class BankAccountBase(BaseModel):
    # Document Information
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Bank Information
    bank_name: str
    account_number: str
    account_name: str

    # Additional Information
    time_period: Optional[str] = None
    
    # Note: Bank address is retrieved from banks table via bank_id FK
    # No need to store address fields here
    
    # Delivery Information
    delivery_date: Optional[date] = None
    
    # Status and Response
    reply_status: Optional[bool] = False
    days_since_sent: Optional[int] = None
    
    # Additional Information
    notes: Optional[str] = None
    status: Optional[str] = "pending"

class BankAccountCreate(BankAccountBase):
    criminal_case_id: int  # REQUIRED field

class BankAccountUpdate(BaseModel):
    # Document Information
    order_number: Optional[int] = None
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Bank Information
    bank_name: Optional[str] = None
    account_number: Optional[str] = None
    account_name: Optional[str] = None

    # Additional Information
    time_period: Optional[str] = None
    
    # Note: Bank address is retrieved from banks table via bank_id FK
    
    # Delivery Information
    delivery_date: Optional[date] = None
    
    # Status and Response
    reply_status: Optional[bool] = None
    days_since_sent: Optional[int] = None
    
    # Additional Information
    notes: Optional[str] = None
    status: Optional[str] = None
    
    # Foreign Key
    criminal_case_id: Optional[int] = None

class CriminalCaseInfo(BaseModel):
    id: int
    case_id: Optional[str] = None
    case_number: Optional[str] = None
    victim_name: Optional[str] = None
    complainant: Optional[str] = None
    damage_amount: Optional[str] = None

    class Config:
        from_attributes = True

class BankAccountResponse(BankAccountBase):
    id: int
    criminal_case_id: Optional[int] = None  # Allow null for legacy data
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    criminal_case: Optional[CriminalCaseInfo] = None

    class Config:
        from_attributes = True

class BankAccountPaginationResponse(BaseModel):
    items: List[BankAccountResponse]
    total: int
    page: int
    per_page: int
    total_pages: int