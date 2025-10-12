from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.payment_gateway_transaction import PaymentGatewayTransaction
from app.models.user import User
from app.schemas.payment_gateway_transaction import (
    PaymentGatewayTransaction as PaymentGatewayTransactionSchema,
    PaymentGatewayTransactionCreate,
    PaymentGatewayTransactionUpdate
)
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PaymentGatewayTransactionSchema])
def get_payment_gateway_transactions(
    payment_gateway_account_id: int = None,
    criminal_case_id: int = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ดึงรายการธุรกรรม Payment Gateway
    - สามารถกรองตาม payment_gateway_account_id หรือ criminal_case_id
    """
    query = db.query(PaymentGatewayTransaction)
    
    if payment_gateway_account_id:
        query = query.filter(PaymentGatewayTransaction.payment_gateway_account_id == payment_gateway_account_id)
    
    if criminal_case_id:
        query = query.filter(PaymentGatewayTransaction.criminal_case_id == criminal_case_id)
    
    transactions = query.order_by(PaymentGatewayTransaction.transfer_date.desc()).offset(skip).limit(limit).all()
    return transactions

@router.get("/{transaction_id}", response_model=PaymentGatewayTransactionSchema)
def get_payment_gateway_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูลธุรกรรม Payment Gateway ตาม ID"""
    transaction = db.query(PaymentGatewayTransaction).filter(PaymentGatewayTransaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@router.post("/", response_model=PaymentGatewayTransactionSchema)
def create_payment_gateway_transaction(
    transaction: PaymentGatewayTransactionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างธุรกรรม Payment Gateway ใหม่"""
    db_transaction = PaymentGatewayTransaction(
        **transaction.dict(),
        created_by=current_user.id
    )
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@router.put("/{transaction_id}", response_model=PaymentGatewayTransactionSchema)
def update_payment_gateway_transaction(
    transaction_id: int,
    transaction: PaymentGatewayTransactionUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """อัพเดทธุรกรรม Payment Gateway"""
    db_transaction = db.query(PaymentGatewayTransaction).filter(PaymentGatewayTransaction.id == transaction_id).first()
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
def delete_payment_gateway_transaction(
    transaction_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ลบธุรกรรม Payment Gateway"""
    db_transaction = db.query(PaymentGatewayTransaction).filter(PaymentGatewayTransaction.id == transaction_id).first()
    if not db_transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(db_transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

