from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostArrestBase(BaseModel):
    suspect_name: str
    id_card_number: Optional[str] = None
    arrest_location: Optional[str] = None
    charge: Optional[str] = None
    case_number: Optional[str] = None
    officer_in_charge: Optional[str] = None
    notes: Optional[str] = None

class PostArrestCreate(PostArrestBase):
    arrest_date: Optional[datetime] = None

class PostArrestUpdate(BaseModel):
    suspect_name: Optional[str] = None
    id_card_number: Optional[str] = None
    arrest_date: Optional[datetime] = None
    arrest_location: Optional[str] = None
    charge: Optional[str] = None
    case_number: Optional[str] = None
    interrogation_completed: Optional[bool] = None
    interrogation_date: Optional[datetime] = None
    prosecutor_submitted: Optional[bool] = None
    prosecutor_submit_date: Optional[datetime] = None
    prosecutor_name: Optional[str] = None
    court_submitted: Optional[bool] = None
    court_submit_date: Optional[datetime] = None
    court_name: Optional[str] = None
    detention_requested: Optional[bool] = None
    detention_approved: Optional[bool] = None
    detention_location: Optional[str] = None
    bail_requested: Optional[bool] = None
    bail_amount: Optional[str] = None
    bail_status: Optional[str] = None
    status: Optional[str] = None
    officer_in_charge: Optional[str] = None
    notes: Optional[str] = None

class PostArrestResponse(PostArrestBase):
    id: int
    arrest_number: str
    arrest_date: Optional[datetime] = None
    interrogation_completed: bool
    interrogation_date: Optional[datetime] = None
    prosecutor_submitted: bool
    prosecutor_submit_date: Optional[datetime] = None
    prosecutor_name: Optional[str] = None
    court_submitted: bool
    court_submit_date: Optional[datetime] = None
    court_name: Optional[str] = None
    detention_requested: bool
    detention_approved: bool
    detention_location: Optional[str] = None
    bail_requested: bool
    bail_amount: Optional[str] = None
    bail_status: Optional[str] = None
    status: str
    created_at: datetime

    class Config:
        from_attributes = True