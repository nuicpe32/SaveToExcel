from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core import get_db
from app.models.non_bank_account import NonBankAccount
from app.models.non_bank import NonBank
from app.models.user import User
from app.schemas.non_bank_account import (
    NonBankAccountCreate,
    NonBankAccountUpdate,
    NonBankAccountResponse,
    NonBankAccountPaginationResponse
)
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=NonBankAccountResponse)
def create_non_bank_account(
    non_bank_account: NonBankAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกผู้ให้บริการ Non-Bank ใหม่"""
    # แปลง schema เป็น dict
    non_bank_data = non_bank_account.dict()

    # Auto-lookup non_bank_id from provider_name
    if non_bank_data.get('provider_name'):
        # ลองหาแบบตรงทั้งหมดก่อน
        non_bank = db.query(NonBank).filter(
            NonBank.company_name == non_bank_data['provider_name']
        ).first()
        
        # ถ้าไม่เจอ ลองหาจาก company_name_short
        if not non_bank:
            non_bank = db.query(NonBank).filter(
                NonBank.company_name_short == non_bank_data['provider_name']
            ).first()
        
        # ถ้ายังไม่เจอ ลองหาแบบ LIKE
        if not non_bank:
            search_pattern = f"%{non_bank_data['provider_name']}%"
            non_bank = db.query(NonBank).filter(
                NonBank.company_name.like(search_pattern)
            ).first()
        
        if non_bank:
            non_bank_data['non_bank_id'] = non_bank.id

    # เพิ่ม created_by
    non_bank_data['created_by'] = current_user.id

    # สร้าง NonBankAccount instance
    db_non_bank_account = NonBankAccount(**non_bank_data)
    db.add(db_non_bank_account)
    db.commit()
    db.refresh(db_non_bank_account)
    return db_non_bank_account

@router.get("/", response_model=NonBankAccountPaginationResponse)
def get_non_bank_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการหมายเรียก Non-Bank ทั้งหมด"""
    total = db.query(NonBankAccount).count()
    non_bank_accounts = db.query(NonBankAccount).offset(skip).limit(limit).all()
    return {
        "items": non_bank_accounts,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{non_bank_account_id}", response_model=NonBankAccountResponse)
def get_non_bank_account(
    non_bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูลหมายเรียก Non-Bank ตาม ID"""
    non_bank_account = db.query(NonBankAccount).filter(
        NonBankAccount.id == non_bank_account_id
    ).first()
    if non_bank_account is None:
        raise HTTPException(status_code=404, detail="Non-bank account not found")
    return non_bank_account

@router.put("/{non_bank_account_id}", response_model=NonBankAccountResponse)
def update_non_bank_account(
    non_bank_account_id: int,
    non_bank_account: NonBankAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """แก้ไขหมายเรียก Non-Bank"""
    db_non_bank_account = db.query(NonBankAccount).filter(
        NonBankAccount.id == non_bank_account_id
    ).first()
    if db_non_bank_account is None:
        raise HTTPException(status_code=404, detail="Non-bank account not found")

    update_data = non_bank_account.dict(exclude_unset=True)

    # Auto-lookup non_bank_id from provider_name if being updated
    if 'provider_name' in update_data and update_data['provider_name']:
        # ลองหาแบบตรงทั้งหมดก่อน
        non_bank = db.query(NonBank).filter(
            NonBank.company_name == update_data['provider_name']
        ).first()
        
        # ถ้าไม่เจอ ลองหาจาก company_name_short
        if not non_bank:
            non_bank = db.query(NonBank).filter(
                NonBank.company_name_short == update_data['provider_name']
            ).first()
        
        # ถ้ายังไม่เจอ ลองหาแบบ LIKE
        if not non_bank:
            search_pattern = f"%{update_data['provider_name']}%"
            non_bank = db.query(NonBank).filter(
                NonBank.company_name.like(search_pattern)
            ).first()
        
        if non_bank:
            update_data['non_bank_id'] = non_bank.id

    for key, value in update_data.items():
        setattr(db_non_bank_account, key, value)

    db.commit()
    db.refresh(db_non_bank_account)
    return db_non_bank_account

@router.delete("/{non_bank_account_id}")
def delete_non_bank_account(
    non_bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ลบหมายเรียก Non-Bank"""
    db_non_bank_account = db.query(NonBankAccount).filter(
        NonBankAccount.id == non_bank_account_id
    ).first()
    if db_non_bank_account is None:
        raise HTTPException(status_code=404, detail="Non-bank account not found")
    
    db.delete(db_non_bank_account)
    db.commit()
    return {"message": "Non-bank account deleted successfully"}

# Endpoint สำหรับดึง non_bank_accounts ของคดี
@router.get("/by-case/{criminal_case_id}", response_model=List[NonBankAccountResponse])
def get_non_bank_accounts_by_case(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการหมายเรียก Non-Bank ของคดี"""
    non_bank_accounts = db.query(NonBankAccount).filter(
        NonBankAccount.criminal_case_id == criminal_case_id
    ).all()
    return non_bank_accounts

