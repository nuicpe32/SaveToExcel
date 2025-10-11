from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core import get_db
from app.models import NonBank, User
from app.schemas.non_bank import NonBankCreate, NonBankUpdate, NonBankResponse
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[NonBankResponse])
def get_non_banks(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ดึงรายการบริษัท Non-Bank ทั้งหมด
    
    Args:
        skip: จำนวนที่ข้าม (สำหรับ pagination)
        limit: จำนวนสูงสุดที่ต้องการ
        active_only: แสดงเฉพาะที่ active (default: True)
    """
    query = db.query(NonBank)
    
    if active_only:
        query = query.filter(NonBank.is_active == True)
    
    non_banks = query.order_by(NonBank.company_name_short).offset(skip).limit(limit).all()
    return non_banks

@router.get("/{non_bank_id}", response_model=NonBankResponse)
def get_non_bank(
    non_bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูลบริษัท Non-Bank รายการเดียว"""
    non_bank = db.query(NonBank).filter(NonBank.id == non_bank_id).first()
    if not non_bank:
        raise HTTPException(status_code=404, detail="Non-Bank company not found")
    return non_bank

@router.post("/", response_model=NonBankResponse, status_code=201)
def create_non_bank(
    non_bank: NonBankCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    สร้างบริษัท Non-Bank ใหม่
    
    Note: ต้องมีสิทธิ์ Admin
    """
    # Check if company_name already exists
    existing = db.query(NonBank).filter(NonBank.company_name == non_bank.company_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company name already exists")
    
    db_non_bank = NonBank(**non_bank.dict())
    db.add(db_non_bank)
    db.commit()
    db.refresh(db_non_bank)
    return db_non_bank

@router.put("/{non_bank_id}", response_model=NonBankResponse)
def update_non_bank(
    non_bank_id: int,
    non_bank: NonBankUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    แก้ไขข้อมูลบริษัท Non-Bank
    
    Note: ต้องมีสิทธิ์ Admin
    """
    db_non_bank = db.query(NonBank).filter(NonBank.id == non_bank_id).first()
    if not db_non_bank:
        raise HTTPException(status_code=404, detail="Non-Bank company not found")
    
    # Update fields
    update_data = non_bank.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_non_bank, field, value)
    
    db.commit()
    db.refresh(db_non_bank)
    return db_non_bank

@router.delete("/{non_bank_id}")
def delete_non_bank(
    non_bank_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ลบบริษัท Non-Bank
    
    Note: ต้องมีสิทธิ์ Admin
    """
    db_non_bank = db.query(NonBank).filter(NonBank.id == non_bank_id).first()
    if not db_non_bank:
        raise HTTPException(status_code=404, detail="Non-Bank company not found")
    
    db.delete(db_non_bank)
    db.commit()
    return {"message": "Non-Bank company deleted successfully"}

