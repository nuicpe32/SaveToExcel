from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.models.payment_gateway import PaymentGateway
from app.models.user import User
from app.schemas.payment_gateway import (
    PaymentGateway as PaymentGatewaySchema,
    PaymentGatewayCreate,
    PaymentGatewayUpdate
)
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[PaymentGatewaySchema])
def get_payment_gateways(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการ Payment Gateway ทั้งหมด"""
    payment_gateways = db.query(PaymentGateway).filter(
        PaymentGateway.is_active == True
    ).offset(skip).limit(limit).all()
    return payment_gateways

@router.get("/{payment_gateway_id}", response_model=PaymentGatewaySchema)
def get_payment_gateway(
    payment_gateway_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูล Payment Gateway ตาม ID"""
    payment_gateway = db.query(PaymentGateway).filter(
        PaymentGateway.id == payment_gateway_id
    ).first()
    if not payment_gateway:
        raise HTTPException(status_code=404, detail="Payment gateway not found")
    return payment_gateway

@router.post("/", response_model=PaymentGatewaySchema)
def create_payment_gateway(
    payment_gateway: PaymentGatewayCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้าง Payment Gateway ใหม่ (Admin only)"""
    db_payment_gateway = PaymentGateway(**payment_gateway.dict())
    db.add(db_payment_gateway)
    db.commit()
    db.refresh(db_payment_gateway)
    return db_payment_gateway

@router.put("/{payment_gateway_id}", response_model=PaymentGatewaySchema)
def update_payment_gateway(
    payment_gateway_id: int,
    payment_gateway: PaymentGatewayUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """อัพเดท Payment Gateway (Admin only)"""
    db_payment_gateway = db.query(PaymentGateway).filter(
        PaymentGateway.id == payment_gateway_id
    ).first()
    if not db_payment_gateway:
        raise HTTPException(status_code=404, detail="Payment gateway not found")
    
    update_data = payment_gateway.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_payment_gateway, field, value)
    
    db.commit()
    db.refresh(db_payment_gateway)
    return db_payment_gateway

@router.delete("/{payment_gateway_id}")
def delete_payment_gateway(
    payment_gateway_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ลบ Payment Gateway (Admin only)"""
    db_payment_gateway = db.query(PaymentGateway).filter(
        PaymentGateway.id == payment_gateway_id
    ).first()
    if not db_payment_gateway:
        raise HTTPException(status_code=404, detail="Payment gateway not found")
    
    db.delete(db_payment_gateway)
    db.commit()
    return {"message": "Payment gateway deleted successfully"}

