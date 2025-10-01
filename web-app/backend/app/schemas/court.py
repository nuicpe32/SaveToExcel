from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CourtBase(BaseModel):
    court_name: str
    court_type: Optional[str] = None
    region: Optional[str] = None
    province: Optional[str] = None


class CourtCreate(CourtBase):
    pass


class CourtUpdate(BaseModel):
    court_name: Optional[str] = None
    court_type: Optional[str] = None
    region: Optional[str] = None
    province: Optional[str] = None


class Court(CourtBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
