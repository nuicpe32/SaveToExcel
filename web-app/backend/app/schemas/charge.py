from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ChargeBase(BaseModel):
    charge_name: str  # ชื่อข้อหา
    charge_description: str  # ข้อหา (รายละเอียดเต็ม)
    related_laws: str  # กฎหมายที่เกี่ยวข้อง
    penalty: str  # อัตราโทษ

class ChargeCreate(ChargeBase):
    pass

class ChargeUpdate(BaseModel):
    charge_name: Optional[str] = None
    charge_description: Optional[str] = None
    related_laws: Optional[str] = None
    penalty: Optional[str] = None

class ChargeResponse(ChargeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True
