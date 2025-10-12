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
@router.get("/by-case/{criminal_case_id}")
def get_non_bank_accounts_by_case(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการหมายเรียก Non-Bank ของคดี"""
    non_bank_accounts = db.query(NonBankAccount).filter(
        NonBankAccount.criminal_case_id == criminal_case_id
    ).all()
    
    # เพิ่ม provider_name จาก relationship
    result = []
    for account in non_bank_accounts:
        account_dict = {
            'id': account.id,
            'non_bank_id': account.non_bank_id,
            'document_number': account.document_number,
            'document_date': account.document_date,
            'account_number': account.account_number,
            'account_name': account.account_name,
            'time_period': account.time_period,
            'delivery_date': account.delivery_date,
            'reply_status': account.reply_status,
            'status': account.status,
            'created_at': account.created_at,
            'updated_at': account.updated_at,
            'created_by': account.created_by,
        }
        
        # เพิ่ม provider_name จาก non_banks table
        if account.non_bank_id:
            non_bank = db.query(NonBank).filter(NonBank.id == account.non_bank_id).first()
            if non_bank:
                account_dict['provider_name'] = non_bank.company_name
        
        result.append(account_dict)
    
    return result

