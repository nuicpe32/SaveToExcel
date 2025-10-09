from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

class PoliceRankInfo(BaseModel):
    id: int
    rank_short: str
    rank_full: str
    rank_english: str
    
    class Config:
        from_attributes = True

class CaseOwnerInfo(BaseModel):
    id: int
    full_name: str
    rank: Optional[PoliceRankInfo] = None
    
    class Config:
        from_attributes = True

class CriminalCaseBase(BaseModel):
    case_number: Optional[str] = None  # Will be auto-generated if not provided
    case_id: Optional[str] = None
    status: Optional[str] = "ระหว่างสอบสวน"

    complainant: Optional[str] = None

    case_type: Optional[str] = None  # ประเภทคดี
    damage_amount: Optional[str] = None

    complaint_date: Optional[date] = None
    incident_date: Optional[date] = None

    court_name: Optional[str] = None  # เขตอำนาจศาล
    
    # Virtual fields (computed at runtime, not in database)
    complaint_date_thai: Optional[str] = None
    incident_date_thai: Optional[str] = None

class CriminalCaseCreate(BaseModel):
    case_number: str  # REQUIRED - user must provide
    case_id: str  # REQUIRED - user must provide
    status: str
    complainant: str  # Required
    complaint_date: date  # Required
    case_type: Optional[str] = None  # ประเภทคดี
    damage_amount: Optional[str] = None
    incident_date: Optional[date] = None
    court_name: Optional[str] = None

class CriminalCaseUpdate(BaseModel):
    case_id: Optional[str] = None
    status: Optional[str] = None
    complainant: Optional[str] = None
    case_type: Optional[str] = None  # ประเภทคดี
    damage_amount: Optional[str] = None
    complaint_date: Optional[date] = None
    incident_date: Optional[date] = None
    court_name: Optional[str] = None
    last_update_date: Optional[datetime] = None

class CriminalCaseResponse(CriminalCaseBase):
    id: int
    last_update_date: Optional[date] = None
    created_at: datetime
    bank_accounts_count: Optional[str] = "0/0"
    suspects_count: Optional[str] = "0/0"
    row_class: Optional[str] = ""
    row_style: Optional[dict] = {}
    owner_id: Optional[int] = None
    owner: Optional[CaseOwnerInfo] = None

    class Config:
        from_attributes = True