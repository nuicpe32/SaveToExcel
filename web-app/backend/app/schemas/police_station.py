from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PoliceStationBase(BaseModel):
    station_name: str
    station_code: Optional[str] = None
    province: str
    district: Optional[str] = None
    subdistrict: Optional[str] = None
    address: Optional[str] = None
    postal_code: Optional[str] = None
    phone: Optional[str] = None
    subdistricts_covered: Optional[str] = None

class PoliceStationCreate(PoliceStationBase):
    pass

class PoliceStationUpdate(PoliceStationBase):
    pass

class PoliceStationResponse(PoliceStationBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class PoliceStationSearchRequest(BaseModel):
    address: str  # ที่อยู่ผู้ต้องหา

class PoliceStationSearchResponse(BaseModel):
    exact_match: Optional[PoliceStationResponse] = None  # สถานีที่ตรงตำบล
    province_matches: list[PoliceStationResponse] = []  # สถานีในจังหวัดเดียวกัน
    district_matches: list[PoliceStationResponse] = []  # สถานีในอำเภอเดียวกัน
    has_incomplete_address: bool = False  # มีสถานีที่ไม่มีเลขที่ในที่อยู่
    warning_message: Optional[str] = None  # ข้อความแจ้งเตือน
