from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core import get_db
from app.models import Bureau, Division, Supervision, User
from app.schemas.organization import (
    BureauResponse, BureauUpdate,
    DivisionResponse, DivisionUpdate,
    SupervisionResponse, SupervisionUpdate,
    OrganizationTree, BureauWithDivisions, DivisionWithSupervisions, SupervisionWithStats
)
from app.api.v1.auth import get_current_user

router = APIRouter()

# ========================================
# Bureaus Endpoints
# ========================================

@router.get("/bureaus", response_model=List[BureauResponse])
def get_bureaus(
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการ Bureau ทั้งหมด"""
    query = db.query(Bureau)
    if active_only:
        query = query.filter(Bureau.is_active == True)
    return query.order_by(Bureau.name_short).all()

@router.put("/bureaus/{bureau_id}", response_model=BureauResponse)
def update_bureau(
    bureau_id: int,
    bureau: BureauUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """อัพเดต Bureau (เปิด/ปิดสิทธิ์)"""
    db_bureau = db.query(Bureau).filter(Bureau.id == bureau_id).first()
    if not db_bureau:
        raise HTTPException(status_code=404, detail="Bureau not found")
    
    update_data = bureau.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bureau, field, value)
    
    db.commit()
    db.refresh(db_bureau)
    return db_bureau

# ========================================
# Divisions Endpoints
# ========================================

@router.get("/divisions", response_model=List[DivisionResponse])
def get_divisions(
    bureau_id: Optional[int] = None,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการ Division (สามารถกรองตาม bureau_id)"""
    query = db.query(Division)
    
    if bureau_id:
        query = query.filter(Division.bureau_id == bureau_id)
    
    if active_only:
        query = query.filter(Division.is_active == True)
    
    return query.order_by(Division.id).all()

@router.put("/divisions/{division_id}", response_model=DivisionResponse)
def update_division(
    division_id: int,
    division: DivisionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """อัพเดต Division (เปิด/ปิดสิทธิ์)"""
    db_division = db.query(Division).filter(Division.id == division_id).first()
    if not db_division:
        raise HTTPException(status_code=404, detail="Division not found")
    
    update_data = division.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_division, field, value)
    
    db.commit()
    db.refresh(db_division)
    return db_division

# ========================================
# Supervisions Endpoints
# ========================================

@router.get("/supervisions", response_model=List[SupervisionResponse])
def get_supervisions(
    division_id: Optional[int] = None,
    active_only: bool = False,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการ Supervision (สามารถกรองตาม division_id)"""
    query = db.query(Supervision)
    
    if division_id:
        query = query.filter(Supervision.division_id == division_id)
    
    if active_only:
        query = query.filter(Supervision.is_active == True)
    
    return query.order_by(Supervision.id).all()

@router.put("/supervisions/{supervision_id}", response_model=SupervisionResponse)
def update_supervision(
    supervision_id: int,
    supervision: SupervisionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """อัพเดต Supervision (เปิด/ปิดสิทธิ์)"""
    db_supervision = db.query(Supervision).filter(Supervision.id == supervision_id).first()
    if not db_supervision:
        raise HTTPException(status_code=404, detail="Supervision not found")
    
    update_data = supervision.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_supervision, field, value)
    
    db.commit()
    db.refresh(db_supervision)
    return db_supervision

# ========================================
# Organization Tree Endpoint
# ========================================

@router.get("/tree", response_model=OrganizationTree)
def get_organization_tree(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงโครงสร้างหน่วยงานทั้งหมดแบบต้นไม้ พร้อมสถิติ"""
    
    bureaus = db.query(Bureau).order_by(Bureau.name_short).all()
    
    result_bureaus = []
    total_users = 0
    active_count = 0
    inactive_count = 0
    
    for bureau in bureaus:
        # นับ users ใน bureau
        bureau_user_count = db.query(User).filter(User.bureau_id == bureau.id).count()
        total_users += bureau_user_count
        
        if bureau.is_active:
            active_count += 1
        else:
            inactive_count += 1
        
        # ดึง divisions
        divisions = db.query(Division).filter(Division.bureau_id == bureau.id).order_by(Division.id).all()
        result_divisions = []
        
        for division in divisions:
            division_user_count = db.query(User).filter(User.division_id == division.id).count()
            
            if division.is_active:
                active_count += 1
            else:
                inactive_count += 1
            
            # ดึง supervisions
            supervisions = db.query(Supervision).filter(Supervision.division_id == division.id).order_by(Supervision.id).all()
            result_supervisions = []
            
            for supervision in supervisions:
                supervision_user_count = db.query(User).filter(User.supervision_id == supervision.id).count()
                
                if supervision.is_active:
                    active_count += 1
                else:
                    inactive_count += 1
                
                result_supervisions.append(
                    SupervisionWithStats(
                        **supervision.__dict__,
                        user_count=supervision_user_count
                    )
                )
            
            result_divisions.append(
                DivisionWithSupervisions(
                    **division.__dict__,
                    supervisions=result_supervisions,
                    user_count=division_user_count
                )
            )
        
        result_bureaus.append(
            BureauWithDivisions(
                **bureau.__dict__,
                divisions=result_divisions,
                user_count=bureau_user_count
            )
        )
    
    return OrganizationTree(
        bureaus=result_bureaus,
        total_users=total_users,
        active_organizations=active_count,
        inactive_organizations=inactive_count
    )

