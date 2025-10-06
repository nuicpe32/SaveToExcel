from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime, date

class SuspectBase(BaseModel):
    # Document Information
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Suspect Information
    suspect_name: str
    suspect_id_card: Optional[str] = None
    suspect_address: Optional[str] = None
    
    # Police Station Information
    police_station: Optional[str] = None
    police_province: Optional[str] = None
    police_address: Optional[str] = None


    # Appointment Information
    appointment_date: Optional[date] = None
    appointment_date_thai: Optional[str] = None
    
    # Status
    status: Optional[str] = "pending"
    notes: Optional[str] = None

class SuspectCreate(SuspectBase):
    criminal_case_id: int  # REQUIRED field
    reply_status: Optional[bool] = False

class SuspectUpdate(BaseModel):
    # Document Information
    document_number: Optional[str] = None
    document_date: Optional[date] = None
    
    # Suspect Information
    suspect_name: Optional[str] = None
    suspect_id_card: Optional[str] = None
    suspect_address: Optional[str] = None
    
    # Police Station Information
    police_station: Optional[str] = None
    police_province: Optional[str] = None
    police_address: Optional[str] = None


    # Appointment Information
    appointment_date: Optional[date] = None
    appointment_date_thai: Optional[str] = None
    
    # Status
    status: Optional[str] = None
    notes: Optional[str] = None
    
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

class SuspectResponse(SuspectBase):
    id: int
    criminal_case_id: Optional[int] = None  # Allow null for legacy data
    reply_status: bool = False
    created_at: datetime
    updated_at: Optional[datetime] = None
    created_by: Optional[int] = None
    criminal_case: Optional[CriminalCaseInfo] = None

    class Config:
        from_attributes = True