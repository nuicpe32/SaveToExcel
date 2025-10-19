from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.charge import Charge
from app.schemas.charge import ChargeCreate, ChargeUpdate, ChargeResponse
from app.api.v1.auth import get_current_user, require_admin
from app.models.user import User

router = APIRouter()

@router.get("/", response_model=List[ChargeResponse])
def get_charges(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all charges (ดึงข้อมูลข้อหาทั้งหมด)
    """
    charges = db.query(Charge).offset(skip).limit(limit).all()
    return charges

@router.get("/{charge_id}", response_model=ChargeResponse)
def get_charge(
    charge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get a specific charge by ID (ดึงข้อมูลข้อหาตาม ID)
    """
    charge = db.query(Charge).filter(Charge.id == charge_id).first()
    if not charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    return charge

@router.post("/", response_model=ChargeResponse, status_code=201)
def create_charge(
    charge: ChargeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Create a new charge (สร้างข้อหาใหม่) - Admin only
    """
    # Check if charge name already exists
    existing_charge = db.query(Charge).filter(
        Charge.charge_name == charge.charge_name
    ).first()
    if existing_charge:
        raise HTTPException(
            status_code=400,
            detail=f"Charge with name '{charge.charge_name}' already exists"
        )
    
    db_charge = Charge(**charge.dict())
    db.add(db_charge)
    db.commit()
    db.refresh(db_charge)
    return db_charge

@router.put("/{charge_id}", response_model=ChargeResponse)
def update_charge(
    charge_id: int,
    charge: ChargeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Update a charge (แก้ไขข้อมูลข้อหา) - Admin only
    """
    db_charge = db.query(Charge).filter(Charge.id == charge_id).first()
    if not db_charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    
    # Check if new charge name already exists (if updating name)
    if charge.charge_name and charge.charge_name != db_charge.charge_name:
        existing_charge = db.query(Charge).filter(
            Charge.charge_name == charge.charge_name
        ).first()
        if existing_charge:
            raise HTTPException(
                status_code=400,
                detail=f"Charge with name '{charge.charge_name}' already exists"
            )
    
    # Update fields
    update_data = charge.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_charge, field, value)
    
    db.commit()
    db.refresh(db_charge)
    return db_charge

@router.delete("/{charge_id}")
def delete_charge(
    charge_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_admin)
):
    """
    Delete a charge (ลบข้อหา) - Admin only
    """
    db_charge = db.query(Charge).filter(Charge.id == charge_id).first()
    if not db_charge:
        raise HTTPException(status_code=404, detail="Charge not found")
    
    # TODO: Check if charge is being used in any criminal cases
    # If relationships exist, prevent deletion or handle cascade
    
    db.delete(db_charge)
    db.commit()
    return {"message": f"Charge '{db_charge.charge_name}' deleted successfully"}

