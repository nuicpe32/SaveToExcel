from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core import get_db
from app.models.bank_account import BankAccount
from app.models.criminal_case import CriminalCase
from app.schemas.bank_account import BankAccountCreate, BankAccountUpdate, BankAccountResponse
from app.api.v1.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=BankAccountResponse)
def create_bank_account(
    bank_account: BankAccountCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new bank account record"""
    
    # Validate criminal case exists
    if bank_account.criminal_case_id:
        criminal_case = db.query(CriminalCase).filter(CriminalCase.id == bank_account.criminal_case_id).first()
        if not criminal_case:
            raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # Create bank account
    db_bank_account = BankAccount(
        **bank_account.dict(),
        created_by=current_user.id
    )
    
    db.add(db_bank_account)
    db.commit()
    db.refresh(db_bank_account)
    
    return db_bank_account

@router.get("/", response_model=List[BankAccountResponse])
def read_bank_accounts(
    skip: int = 0,
    limit: int = 100,
    criminal_case_id: Optional[int] = Query(None, description="Filter by criminal case ID"),
    reply_status: Optional[bool] = Query(None, description="Filter by reply status"),
    status: Optional[str] = Query(None, description="Filter by status"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get bank accounts with filtering options"""
    
    query = db.query(BankAccount)
    
    # Apply filters
    if criminal_case_id:
        query = query.filter(BankAccount.criminal_case_id == criminal_case_id)
    
    if reply_status is not None:
        query = query.filter(BankAccount.reply_status == reply_status)
    
    if status:
        query = query.filter(BankAccount.status == status)
    
    bank_accounts = query.offset(skip).limit(limit).all()
    return bank_accounts

@router.get("/{bank_account_id}", response_model=BankAccountResponse)
def read_bank_account(
    bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific bank account by ID"""
    
    bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if not bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    return bank_account

@router.put("/{bank_account_id}", response_model=BankAccountResponse)
def update_bank_account(
    bank_account_id: int,
    bank_account_update: BankAccountUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a bank account record"""
    
    db_bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if not db_bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    # Validate criminal case exists if provided
    if bank_account_update.criminal_case_id:
        criminal_case = db.query(CriminalCase).filter(CriminalCase.id == bank_account_update.criminal_case_id).first()
        if not criminal_case:
            raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # Update fields
    update_data = bank_account_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_bank_account, field, value)
    
    db.commit()
    db.refresh(db_bank_account)
    
    return db_bank_account

@router.delete("/{bank_account_id}")
def delete_bank_account(
    bank_account_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a bank account record"""
    
    db_bank_account = db.query(BankAccount).filter(BankAccount.id == bank_account_id).first()
    if not db_bank_account:
        raise HTTPException(status_code=404, detail="Bank account not found")
    
    db.delete(db_bank_account)
    db.commit()
    
    return {"message": "Bank account deleted successfully"}

@router.get("/criminal-case/{criminal_case_id}", response_model=List[BankAccountResponse])
def get_bank_accounts_by_criminal_case(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all bank accounts for a specific criminal case"""
    
    # Validate criminal case exists
    criminal_case = db.query(CriminalCase).filter(CriminalCase.id == criminal_case_id).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    bank_accounts = db.query(BankAccount).filter(
        BankAccount.criminal_case_id == criminal_case_id
    ).all()
    
    return bank_accounts
