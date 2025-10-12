from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.non_bank_transaction import NonBankTransaction
from app.models.user import User
from app.schemas.non_bank_transaction import (
    NonBankTransaction as NonBankTransactionSchema,
    NonBankTransactionCreate,
    NonBankTransactionUpdate
)
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[NonBankTransactionSchema])
def get_non_bank_transactions(
    non_bank_account_id: int = None,
    criminal_case_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ดึงรายการธุรกรรม Non-Bank
    - สามารถกรองตาม non_bank_account_id หรือ criminal_case_id
    """
    query = db.query(NonBankTransaction)
    
    if non_bank_account_id:
        query = query.filter(NonBankTransaction.non_bank_account_id == non_bank_account_id)
    
    if criminal_case_id:
        query = query.filter(NonBankTransaction.criminal_case_id == criminal_case_id)
    
    transactions = query.order_by(NonBankTransaction.transfer_date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=NonBankTransactionSchema)
def get_non_bank_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูลธุรกรรม Non-Bank ตาม ID"""
    transaction = db.query(NonBankTransaction).filter(NonBankTransaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=NonBankTransactionSchema)
def create_non_bank_transaction(
    transaction: NonBankTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างธุรกรรม Non-Bank ใหม่"""
    db_transaction = NonBankTransaction(
        **transaction.dict(),
        created_by=current_user.id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.put("/{transaction_id}", response_model=NonBankTransactionSchema)
def update_non_bank_transaction(
    transaction_id: int,
    transaction: NonBankTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """อัพเดทธุรกรรม Non-Bank"""
    db_transaction = db.query(NonBankTransaction).filter(NonBankTransaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    # Update fields
    update_data = transaction.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_transaction, field, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.delete("/{transaction_id}")
def delete_non_bank_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ลบธุรกรรม Non-Bank"""
    db_transaction = db.query(NonBankTransaction).filter(NonBankTransaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

