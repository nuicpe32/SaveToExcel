from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core import get_db
from app.models import BankAccount, User, Bank
from app.schemas import BankAccountCreate, BankAccountUpdate, BankAccountResponse
from app.api.v1.auth import get_current_user
from app.utils.thai_date_utils import format_date_to_thai_buddhist_era

router = APIRouter()

def generate_document_number(db: Session) -> str:
    current_year = datetime.now().year + 543
    count = db.query(BankAccount).filter(
        BankAccount.document_number.like(f"BA-{current_year}-%")
    ).count()
    return f"BA-{current_year}-{count + 1:04d}"

@router.post("/", response_model=BankAccountResponse)
def create_bank_account(
    bank_account: BankAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # แปลง BankAccountCreate เป็น dict และเตรียมข้อมูล
    bank_data = bank_account.dict()

    # ไม่ต้อง auto-generate document_number
    # ให้ผู้ใช้กรอกเอง หรือเว้นว่างไว้

    # Auto-lookup bank_id from bank_name
    if bank_data.get('bank_name'):
        bank = db.query(Bank).filter(Bank.bank_name == bank_data['bank_name']).first()
        if bank:
            bank_data['bank_id'] = bank.id

    # แปลง document_date เป็น document_date_thai อัตโนมัติ
    if bank_data.get('document_date'):
        bank_data['document_date_thai'] = format_date_to_thai_buddhist_era(bank_data['document_date'])

    # เพิ่ม created_by
    bank_data['created_by'] = current_user.id

    # สร้าง BankAccount instance
    db_bank_account = BankAccount(**bank_data)
    db.add(db_bank_account)
    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account

@router.get("/", response_model=List[BankAccountResponse])
def read_bank_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bank_accounts = db.query(BankAccount).offset(skip).limit(limit).all()
    return bank_accounts

@router.get("/{bank_account_id}", response_model=BankAccountResponse)
def read_bank_account(
    bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")
    return bank_account

@router.put("/{bank_account_id}", response_model=BankAccountResponse)
def update_bank_account(
    bank_account_id: int,
    bank_account: BankAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")

    update_data = bank_account.dict(exclude_unset=True)

    # Auto-lookup bank_id from bank_name if bank_name is being updated
    if 'bank_name' in update_data and update_data['bank_name']:
        bank = db.query(Bank).filter(Bank.bank_name == update_data['bank_name']).first()
        if bank:
            update_data['bank_id'] = bank.id

    # แปลง document_date เป็น document_date_thai อัตโนมัติ
    if 'document_date' in update_data and update_data['document_date']:
        update_data['document_date_thai'] = format_date_to_thai_buddhist_era(update_data['document_date'])

    for key, value in update_data.items():
        setattr(db_bank_account, key, value)

    db.commit()
    db.refresh(db_bank_account)
    return db_bank_account

@router.delete("/{bank_account_id}")
def delete_bank_account(
    bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if db_bank_account is None:
        raise HTTPException(status_code=404, detail="Bank account not found")

    db.delete(db_bank_account)
    db.commit()
    return {"ok": True}