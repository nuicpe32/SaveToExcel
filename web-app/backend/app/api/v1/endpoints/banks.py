from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core import get_db
from app.api.v1.auth import get_current_user
from app.models.bank import Bank
from app.schemas.bank import Bank as BankSchema, BankCreate, BankUpdate

router = APIRouter()


@router.get("/", response_model=List[BankSchema])
def get_banks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    """Get all banks"""
    banks = db.query(Bank).order_by(Bank.bank_name).offset(skip).limit(limit).all()
    return banks


@router.get("/{bank_id}", response_model=BankSchema)
def get_bank(
    bank_id: int,
    db: Session = Depends(get_db)
):
    """Get bank by ID"""
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")
    return bank


@router.post("/", response_model=BankSchema)
def create_bank(
    bank_in: BankCreate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Create new bank (admin only)"""
    # Check if bank already exists
    existing = db.query(Bank).filter(Bank.bank_name == bank_in.bank_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Bank with this name already exists")

    bank = Bank(**bank_in.model_dump())
    db.add(bank)
    db.commit()
    db.refresh(bank)
    return bank


@router.put("/{bank_id}", response_model=BankSchema)
def update_bank(
    bank_id: int,
    bank_in: BankUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Update bank (admin only)"""
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    update_data = bank_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(bank, field, value)

    db.commit()
    db.refresh(bank)
    return bank


@router.delete("/{bank_id}")
def delete_bank(
    bank_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    """Delete bank (admin only)"""
    bank = db.query(Bank).filter(Bank.id == bank_id).first()
    if not bank:
        raise HTTPException(status_code=404, detail="Bank not found")

    # Check if bank is being used
    if bank.bank_accounts:
        raise HTTPException(
            status_code=400,
            detail=f"Cannot delete bank. It is referenced by {len(bank.bank_accounts)} bank account(s)"
        )

    db.delete(bank)
    db.commit()
    return {"message": "Bank deleted successfully"}
