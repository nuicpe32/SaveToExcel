from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ========================================
# Bureau Schemas
# ========================================

class BureauBase(BaseModel):
    name_full: str
    name_short: str
    is_active: Optional[bool] = True

class BureauCreate(BureauBase):
    pass

class BureauUpdate(BaseModel):
    name_full: Optional[str] = None
    name_short: Optional[str] = None
    is_active: Optional[bool] = None

class BureauResponse(BureauBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ========================================
# Division Schemas
# ========================================

class DivisionBase(BaseModel):
    bureau_id: int
    name_full: str
    name_short: str
    is_active: Optional[bool] = True

class DivisionCreate(DivisionBase):
    pass

class DivisionUpdate(BaseModel):
    bureau_id: Optional[int] = None
    name_full: Optional[str] = None
    name_short: Optional[str] = None
    is_active: Optional[bool] = None

class DivisionResponse(DivisionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ========================================
# Supervision Schemas
# ========================================

class SupervisionBase(BaseModel):
    division_id: int
    name_full: str
    name_short: str
    is_active: Optional[bool] = True

class SupervisionCreate(SupervisionBase):
    pass

class SupervisionUpdate(BaseModel):
    division_id: Optional[int] = None
    name_full: Optional[str] = None
    name_short: Optional[str] = None
    is_active: Optional[bool] = None

class SupervisionResponse(SupervisionBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

# ========================================
# Organization Tree Schema (สำหรับแสดงโครงสร้าง)
# ========================================

class SupervisionWithStats(SupervisionResponse):
    """Supervision พร้อมสถิติผู้ใช้"""
    user_count: int = 0

class DivisionWithSupervisions(DivisionResponse):
    """Division พร้อม Supervisions"""
    supervisions: List[SupervisionWithStats] = []
    user_count: int = 0

class BureauWithDivisions(BureauResponse):
    """Bureau พร้อม Divisions และ Supervisions"""
    divisions: List[DivisionWithSupervisions] = []
    user_count: int = 0

class OrganizationTree(BaseModel):
    """โครงสร้างหน่วยงานทั้งหมดแบบต้นไม้"""
    bureaus: List[BureauWithDivisions]
    total_users: int
    active_organizations: int
    inactive_organizations: int

