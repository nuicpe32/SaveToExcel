from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from app.core.database import get_db
from app.models.telco_mobile_account import TelcoMobileAccount
from app.models.telco_mobile import TelcoMobile
from app.models.user import User
from app.models.criminal_case import CriminalCase
from app.schemas.telco_mobile_account import (
    TelcoMobileAccountCreate, 
    TelcoMobileAccountUpdate, 
    TelcoMobileAccountResponse, 
    TelcoMobileAccountPaginationResponse
)
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=TelcoMobileAccountResponse)
def create_telco_mobile_account(
    telco_account: TelcoMobileAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """สร้างข้อมูลหมายเลขโทรศัพท์ใหม่"""
    telco_data = telco_account.dict()

    # Auto-lookup telco_mobile_id from provider_name
    if telco_data.get('provider_name'):
        # ลองหาแบบตรงทั้งหมดก่อน (company_name_short)
        telco = db.query(TelcoMobile).filter(
            TelcoMobile.company_name_short == telco_data['provider_name']
        ).first()
        
        # ถ้าไม่เจอ ลองหาจาก company_name
        if not telco:
            telco = db.query(TelcoMobile).filter(
                TelcoMobile.company_name == telco_data['provider_name']
            ).first()
        
        # ถ้ายังไม่เจอ ลองหาแบบ LIKE
        if not telco:
            provider_search = f"%{telco_data['provider_name']}%"
            telco = db.query(TelcoMobile).filter(
                TelcoMobile.company_name.like(provider_search)
            ).first()
        
        if telco:
            telco_data['telco_mobile_id'] = telco.id

    # เพิ่ม created_by
    telco_data['created_by'] = current_user.id

    # สร้าง TelcoMobileAccount instance
    db_telco_account = TelcoMobileAccount(**telco_data)
    db.add(db_telco_account)
    db.commit()
    db.refresh(db_telco_account)
    return db_telco_account

@router.get("/", response_model=TelcoMobileAccountPaginationResponse)
def read_telco_mobile_accounts(
    page: int = 1,
    per_page: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการข้อมูลหมายเลขโทรศัพท์ทั้งหมด"""
    # คำนวณ offset
    skip = (page - 1) * per_page
    
    # สร้าง base query ที่กรองข้อมูลที่มีเลขที่หนังสือและลงวันที่
    base_query = db.query(TelcoMobileAccount).filter(
        TelcoMobileAccount.document_number.isnot(None),
        TelcoMobileAccount.document_number != '',
        TelcoMobileAccount.document_date.isnot(None)
    )
    
    # If user is not admin, filter by criminal case owner
    if not current_user.role or current_user.role.role_name != "admin":
        base_query = base_query.join(CriminalCase).filter(
            CriminalCase.owner_id == current_user.id
        )
    
    # นับจำนวนทั้งหมด
    total = base_query.count()
    
    # ดึงข้อมูลตาม pagination พร้อมข้อมูล criminal_case และ telco_mobile
    telco_accounts = base_query.options(
        joinedload(TelcoMobileAccount.criminal_case),
        joinedload(TelcoMobileAccount.telco_mobile)
    ).order_by(TelcoMobileAccount.document_date.desc()).offset(skip).limit(per_page).all()
    
    # คำนวณจำนวนหน้า
    total_pages = (total + per_page - 1) // per_page
    
    return TelcoMobileAccountPaginationResponse(
        items=telco_accounts,
        total=total,
        page=page,
        per_page=per_page,
        total_pages=total_pages
    )

@router.get("/by-case/{criminal_case_id}", response_model=List[TelcoMobileAccountResponse])
def read_telco_mobile_accounts_by_case(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการหมายเลขโทรศัพท์ตามคดี"""
    telco_accounts = db.query(TelcoMobileAccount).options(
        joinedload(TelcoMobileAccount.criminal_case),
        joinedload(TelcoMobileAccount.telco_mobile)
    ).filter(
        TelcoMobileAccount.criminal_case_id == criminal_case_id
    ).order_by(TelcoMobileAccount.document_date.desc()).all()
    
    return telco_accounts

@router.get("/{telco_account_id}", response_model=TelcoMobileAccountResponse)
def read_telco_mobile_account(
    telco_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูลหมายเลขโทรศัพท์ตาม ID"""
    telco_account = db.query(TelcoMobileAccount).options(
        joinedload(TelcoMobileAccount.criminal_case),
        joinedload(TelcoMobileAccount.telco_mobile)
    ).filter(TelcoMobileAccount.id == telco_account_id).first()
    
    if telco_account is None:
        raise HTTPException(status_code=404, detail="Telco mobile account not found")
    return telco_account

@router.put("/{telco_account_id}", response_model=TelcoMobileAccountResponse)
def update_telco_mobile_account(
    telco_account_id: int,
    telco_account: TelcoMobileAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """แก้ไขข้อมูลหมายเลขโทรศัพท์"""
    db_telco_account = db.query(TelcoMobileAccount).filter(
        TelcoMobileAccount.id == telco_account_id
    ).first()
    
    if db_telco_account is None:
        raise HTTPException(status_code=404, detail="Telco mobile account not found")

    update_data = telco_account.dict(exclude_unset=True)

    # Auto-lookup telco_mobile_id from provider_name if being updated
    if 'provider_name' in update_data and update_data['provider_name']:
        # ลองหาแบบตรงทั้งหมดก่อน (company_name_short)
        telco = db.query(TelcoMobile).filter(
            TelcoMobile.company_name_short == update_data['provider_name']
        ).first()
        
        # ถ้าไม่เจอ ลองหาจาก company_name
        if not telco:
            telco = db.query(TelcoMobile).filter(
                TelcoMobile.company_name == update_data['provider_name']
            ).first()
        
        # ถ้ายังไม่เจอ ลองหาแบบ LIKE
        if not telco:
            provider_search = f"%{update_data['provider_name']}%"
            telco = db.query(TelcoMobile).filter(
                TelcoMobile.company_name.like(provider_search)
            ).first()
        
        if telco:
            update_data['telco_mobile_id'] = telco.id

    for key, value in update_data.items():
        setattr(db_telco_account, key, value)

    db.commit()
    db.refresh(db_telco_account)
    return db_telco_account

@router.delete("/{telco_account_id}")
def delete_telco_mobile_account(
    telco_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ลบข้อมูลหมายเลขโทรศัพท์"""
    db_telco_account = db.query(TelcoMobileAccount).filter(
        TelcoMobileAccount.id == telco_account_id
    ).first()
    
    if db_telco_account is None:
        raise HTTPException(status_code=404, detail="Telco mobile account not found")

    db.delete(db_telco_account)
    db.commit()
    return {"message": "Telco mobile account deleted successfully"}

