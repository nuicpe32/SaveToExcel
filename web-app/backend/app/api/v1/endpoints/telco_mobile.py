from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core import get_db
from app.models import TelcoMobile, User
from app.schemas.telco_mobile import TelcoMobileCreate, TelcoMobileUpdate, TelcoMobileResponse
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[TelcoMobileResponse])
def get_telco_mobiles(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ดึงรายการผู้ให้บริการเครือข่ายมือถือทั้งหมด
    
    Args:
        skip: จำนวนที่ข้าม (สำหรับ pagination)
        limit: จำนวนสูงสุดที่ต้องการ
        active_only: แสดงเฉพาะที่ active (default: True)
    """
    query = db.query(TelcoMobile)
    
    if active_only:
        query = query.filter(TelcoMobile.is_active == True)
    
    telcos = query.order_by(TelcoMobile.company_name_short).offset(skip).limit(limit).all()
    return telcos

@router.get("/{telco_id}", response_model=TelcoMobileResponse)
def get_telco_mobile(
    telco_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูลผู้ให้บริการรายการเดียว"""
    telco = db.query(TelcoMobile).filter(TelcoMobile.id == telco_id).first()
    if not telco:
        raise HTTPException(status_code=404, detail="Telco Mobile company not found")
    return telco

@router.post("/", response_model=TelcoMobileResponse, status_code=201)
def create_telco_mobile(
    telco: TelcoMobileCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    สร้างผู้ให้บริการใหม่
    
    Note: ต้องมีสิทธิ์ Admin
    """
    # Check if company_name already exists
    existing = db.query(TelcoMobile).filter(TelcoMobile.company_name == telco.company_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company name already exists")
    
    db_telco = TelcoMobile(**telco.dict())
    db.add(db_telco)
    db.commit()
    db.refresh(db_telco)
    return db_telco

@router.put("/{telco_id}", response_model=TelcoMobileResponse)
def update_telco_mobile(
    telco_id: int,
    telco: TelcoMobileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    แก้ไขข้อมูลผู้ให้บริการ
    
    Note: ต้องมีสิทธิ์ Admin
    """
    db_telco = db.query(TelcoMobile).filter(TelcoMobile.id == telco_id).first()
    if not db_telco:
        raise HTTPException(status_code=404, detail="Telco Mobile company not found")
    
    # Update fields
    update_data = telco.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_telco, field, value)
    
    db.commit()
    db.refresh(db_telco)
    return db_telco

@router.delete("/{telco_id}")
def delete_telco_mobile(
    telco_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ลบผู้ให้บริการ
    
    Note: ต้องมีสิทธิ์ Admin
    """
    db_telco = db.query(TelcoMobile).filter(TelcoMobile.id == telco_id).first()
    if not db_telco:
        raise HTTPException(status_code=404, detail="Telco Mobile company not found")
    
    db.delete(db_telco)
    db.commit()
    return {"message": "Telco Mobile company deleted successfully"}

