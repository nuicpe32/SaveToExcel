from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core import get_db
from app.models import Exchange, User
from app.schemas.exchange import ExchangeCreate, ExchangeUpdate, ExchangeResponse
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[ExchangeResponse])
def get_exchanges(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = True,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ดึงรายการผู้ให้บริการ Crypto Exchange ทั้งหมด
    
    Args:
        skip: จำนวนที่ข้าม (สำหรับ pagination)
        limit: จำนวนสูงสุดที่ต้องการ
        active_only: แสดงเฉพาะที่ active (default: True)
    """
    query = db.query(Exchange)
    
    if active_only:
        query = query.filter(Exchange.is_active == True)
    
    exchanges = query.order_by(Exchange.company_name_short).offset(skip).limit(limit).all()
    return exchanges

@router.get("/{exchange_id}", response_model=ExchangeResponse)
def get_exchange(
    exchange_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูล Exchange รายการเดียว"""
    exchange = db.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    return exchange

@router.post("/", response_model=ExchangeResponse, status_code=201)
def create_exchange(
    exchange: ExchangeCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    สร้าง Exchange ใหม่
    
    Note: ต้องมีสิทธิ์ Admin
    """
    # Check if company_name already exists
    existing = db.query(Exchange).filter(Exchange.company_name == exchange.company_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Company name already exists")
    
    db_exchange = Exchange(**exchange.dict())
    db.add(db_exchange)
    db.commit()
    db.refresh(db_exchange)
    return db_exchange

@router.put("/{exchange_id}", response_model=ExchangeResponse)
def update_exchange(
    exchange_id: int,
    exchange: ExchangeUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    แก้ไขข้อมูล Exchange
    
    Note: ต้องมีสิทธิ์ Admin
    """
    db_exchange = db.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not db_exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    
    # Update fields
    update_data = exchange.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_exchange, field, value)
    
    db.commit()
    db.refresh(db_exchange)
    return db_exchange

@router.delete("/{exchange_id}")
def delete_exchange(
    exchange_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    ลบ Exchange
    
    Note: ต้องมีสิทธิ์ Admin
    """
    db_exchange = db.query(Exchange).filter(Exchange.id == exchange_id).first()
    if not db_exchange:
        raise HTTPException(status_code=404, detail="Exchange not found")
    
    db.delete(db_exchange)
    db.commit()
    return {"message": "Exchange deleted successfully"}

