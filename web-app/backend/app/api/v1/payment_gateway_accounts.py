from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core import get_db
from app.models.payment_gateway_account import PaymentGatewayAccount
from app.models.payment_gateway import PaymentGateway
from app.models.user import User
from app.schemas.payment_gateway_account import (
    PaymentGatewayAccountCreate,
    PaymentGatewayAccountUpdate,
    PaymentGatewayAccountResponse,
    PaymentGatewayAccountPaginationResponse
)
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=PaymentGatewayAccountResponse)
def create_payment_gateway_account(
    payment_gateway_account: PaymentGatewayAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างหมายเรียกผู้ให้บริการ Payment Gateway ใหม่"""
    # แปลง schema เป็น dict
    pg_account_data = payment_gateway_account.dict()
    
    # เพิ่ม created_by
    pg_account_data['created_by'] = current_user.id

    # สร้าง PaymentGatewayAccount instance
    db_pg_account = PaymentGatewayAccount(**pg_account_data)
    db.add(db_pg_account)
    db.commit()
    db.refresh(db_pg_account)
    return db_pg_account

@router.get("/", response_model=PaymentGatewayAccountPaginationResponse)
def get_payment_gateway_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการหมายเรียก Payment Gateway ทั้งหมด"""
    total = db.query(PaymentGatewayAccount).count()
    pg_accounts = db.query(PaymentGatewayAccount).offset(skip).limit(limit).all()
    return {
        "items": pg_accounts,
        "total": total,
        "skip": skip,
        "limit": limit
    }

@router.get("/{payment_gateway_account_id}", response_model=PaymentGatewayAccountResponse)
def get_payment_gateway_account(
    payment_gateway_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูลหมายเรียก Payment Gateway ตาม ID"""
    pg_account = db.query(PaymentGatewayAccount).filter(
        PaymentGatewayAccount.id == payment_gateway_account_id
    ).first()
    if pg_account is None:
        raise HTTPException(status_code=404, detail="Payment gateway account not found")
    return pg_account

@router.put("/{payment_gateway_account_id}", response_model=PaymentGatewayAccountResponse)
def update_payment_gateway_account(
    payment_gateway_account_id: int,
    payment_gateway_account: PaymentGatewayAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """แก้ไขหมายเรียก Payment Gateway"""
    db_pg_account = db.query(PaymentGatewayAccount).filter(
        PaymentGatewayAccount.id == payment_gateway_account_id
    ).first()
    if db_pg_account is None:
        raise HTTPException(status_code=404, detail="Payment gateway account not found")

    update_data = payment_gateway_account.dict(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_pg_account, key, value)

    db.commit()
    db.refresh(db_pg_account)
    return db_pg_account

@router.delete("/{payment_gateway_account_id}")
def delete_payment_gateway_account(
    payment_gateway_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ลบหมายเรียก Payment Gateway"""
    db_pg_account = db.query(PaymentGatewayAccount).filter(
        PaymentGatewayAccount.id == payment_gateway_account_id
    ).first()
    if db_pg_account is None:
        raise HTTPException(status_code=404, detail="Payment gateway account not found")

    # ลบ transactions ที่เกี่ยวข้องก่อน (explicit delete)
    from app.models.payment_gateway_transaction import PaymentGatewayTransaction
    db.query(PaymentGatewayTransaction).filter(
        PaymentGatewayTransaction.payment_gateway_account_id == payment_gateway_account_id
    ).delete(synchronize_session=False)

    db.delete(db_pg_account)
    db.commit()
    return {"message": "Payment gateway account deleted successfully"}

# Endpoint สำหรับดึง payment_gateway_accounts ของคดี
@router.get("/by-case/{criminal_case_id}")
def get_payment_gateway_accounts_by_case(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการหมายเรียก Payment Gateway ของคดี"""
    pg_accounts = db.query(PaymentGatewayAccount).filter(
        PaymentGatewayAccount.criminal_case_id == criminal_case_id
    ).all()
    
    # เพิ่ม provider_name จาก relationship
    result = []
    for account in pg_accounts:
        account_dict = {
            'id': account.id,
            'payment_gateway_id': account.payment_gateway_id,
            'bank_id': account.bank_id,
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
        
        # เพิ่ม provider_name จาก payment_gateways table
        if account.payment_gateway_id:
            pg = db.query(PaymentGateway).filter(PaymentGateway.id == account.payment_gateway_id).first()
            if pg:
                account_dict['provider_name'] = pg.company_name
        
        # เพิ่ม bank_name จาก banks table
        if account.bank_id:
            from app.models.bank import Bank
            bank = db.query(Bank).filter(Bank.id == account.bank_id).first()
            if bank:
                account_dict['bank_name'] = bank.bank_name
        
        result.append(account_dict)
    
    return result

