from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime, timedelta
from app.core import get_db
from app.models import CriminalCase, User, BankAccount, Suspect
from app.schemas import CriminalCaseCreate, CriminalCaseUpdate, CriminalCaseResponse, BankAccountResponse, SuspectResponse
from app.api.v1.auth import get_current_user
from app.utils.string_utils import safe_string_conversion, name_contains, clean_name_for_matching
from app.utils.case_styling import get_case_row_class, get_case_row_style
from app.utils.case_number_generator import generate_case_number, validate_case_number

router = APIRouter()

@router.post("/", response_model=CriminalCaseResponse, status_code=201)
def create_criminal_case(
    criminal_case: CriminalCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Auto-generate case_number if not provided
    case_data = criminal_case.dict()
    if not case_data.get('case_number'):
        case_data['case_number'] = generate_case_number(db)

    # Validate case_number format
    if not validate_case_number(case_data['case_number']):
        raise HTTPException(status_code=400, detail="Invalid case number format. Expected: {number}/{year}")

    # Check if case_number already exists
    db_case = db.query(CriminalCase).filter(CriminalCase.case_number == case_data['case_number']).first()
    if db_case:
        raise HTTPException(status_code=400, detail=f"Case number {case_data['case_number']} already exists")

    db_case = CriminalCase(
        **case_data,
        last_update_date=datetime.now(),
        created_by=current_user.id
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    # Add related data counts using case ID
    db_case.bank_accounts_count = get_bank_accounts_count(db, db_case.id)
    db_case.suspects_count = get_suspects_count(db, db_case.id)
    # case_id field is already set from form data

    # Add row styling
    complaint_date_str = db_case.complaint_date_thai or str(db_case.complaint_date) if db_case.complaint_date else ''
    db_case.row_class = get_case_row_class(db_case.status, complaint_date_str, db_case.bank_accounts_count)
    db_case.row_style = get_case_row_style(db_case.status, complaint_date_str, db_case.bank_accounts_count)

    return db_case

def get_bank_accounts_count(db: Session, case_id: int) -> str:
    """Calculate bank accounts count and replied count for a criminal case"""
    try:
        # Use FK relationship only
        matching_accounts = db.query(BankAccount).filter(
            BankAccount.criminal_case_id == case_id
        ).all()

        if not matching_accounts:
            return "0/0"

        total_accounts = len(matching_accounts)
        replied_accounts = sum(1 for account in matching_accounts if account.reply_status)

        return f"{total_accounts}/{replied_accounts}"

    except Exception as e:
        print(f"Error calculating bank accounts count: {e}")
        return "0/0"

def get_case_id_from_related_data(db: Session, case_id: int) -> str:
    """Get CaseID from the criminal case itself"""
    try:
        # Get the case directly by ID
        case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
        if case and case.case_id:
            return case.case_id
        return ""
    except Exception as e:
        print(f"Error getting CaseID: {e}")
        return ""

def get_suspects_count(db: Session, case_id: int) -> str:
    """Calculate suspects count and replied count for a criminal case"""
    try:
        # Use FK relationship only
        matching_suspects = db.query(Suspect).filter(
            Suspect.criminal_case_id == case_id
        ).all()

        if not matching_suspects:
            return "0/0"

        total_suspects = len(matching_suspects)
        # For suspects, check reply_status field (X means replied, False/None means not replied)
        replied_suspects = sum(1 for suspect in matching_suspects if suspect.reply_status)

        return f"{total_suspects}/{replied_suspects}"

    except Exception as e:
        print(f"Error calculating suspects count: {e}")
        return "0/0"

@router.get("/", response_model=List[CriminalCaseResponse])
def read_criminal_cases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    cases = db.query(CriminalCase).order_by(CriminalCase.complaint_date.desc()).offset(skip).limit(limit).all()

    # Add related data counts to each case
    for case in cases:
        case.bank_accounts_count = get_bank_accounts_count(db, case.id)
        case.suspects_count = get_suspects_count(db, case.id)
        # case_id is already in the database

        # Add row styling information
        complaint_date_str = case.complaint_date_thai or str(case.complaint_date) if case.complaint_date else ''
        case.row_class = get_case_row_class(case.status, complaint_date_str, case.bank_accounts_count)
        case.row_style = get_case_row_style(case.status, complaint_date_str, case.bank_accounts_count)

    return cases

@router.get("/aging", response_model=List[CriminalCaseResponse])
def read_aging_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    six_months_ago = datetime.now() - timedelta(days=180)
    cases = db.query(CriminalCase).filter(
        CriminalCase.case_date < six_months_ago.date(),
        CriminalCase.status == "active"
    ).all()
    return cases

@router.get("/{case_id}", response_model=CriminalCaseResponse)
def read_criminal_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    # Add related data counts using case ID
    case.bank_accounts_count = get_bank_accounts_count(db, case.id)
    case.suspects_count = get_suspects_count(db, case.id)
    # case_id is already in the database

    # Add row styling
    complaint_date_str = case.complaint_date_thai or str(case.complaint_date) if case.complaint_date else ''
    case.row_class = get_case_row_class(case.status, complaint_date_str, case.bank_accounts_count)
    case.row_style = get_case_row_style(case.status, complaint_date_str, case.bank_accounts_count)

    return case

@router.put("/{case_id}", response_model=CriminalCaseResponse)
def update_criminal_case(
    case_id: int,
    criminal_case: CriminalCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    for key, value in criminal_case.dict(exclude_unset=True).items():
        setattr(db_case, key, value)

    db_case.last_update_date = datetime.now()
    
    # Update Thai date fields if complaint_date is updated
    if 'complaint_date' in criminal_case.dict(exclude_unset=True) and db_case.complaint_date:
        from app.services.data_migration import DataMigration
        migration = DataMigration()
        db_case.complaint_date_thai = migration._format_thai_date(db_case.complaint_date)
    
    if 'incident_date' in criminal_case.dict(exclude_unset=True) and db_case.incident_date:
        from app.services.data_migration import DataMigration
        migration = DataMigration()
        db_case.incident_date_thai = migration._format_thai_date(db_case.incident_date)
    
    db.commit()
    db.refresh(db_case)

    # Add related data counts using case ID
    db_case.bank_accounts_count = get_bank_accounts_count(db, db_case.id)
    db_case.suspects_count = get_suspects_count(db, db_case.id)
    # case_id is already in the database

    # Add row styling
    complaint_date_str = db_case.complaint_date_thai or str(db_case.complaint_date) if db_case.complaint_date else ''
    db_case.row_class = get_case_row_class(db_case.status, complaint_date_str, db_case.bank_accounts_count)
    db_case.row_style = get_case_row_style(db_case.status, complaint_date_str, db_case.bank_accounts_count)

    return db_case

@router.delete("/{case_id}")
def delete_criminal_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if db_case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    db.delete(db_case)
    db.commit()
    return {"ok": True}

@router.get("/{case_id}/bank-accounts", response_model=List[BankAccountResponse])
def get_case_bank_accounts(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get bank accounts related to a specific criminal case"""
    # Get the criminal case
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    try:
        # Use FK relationship only
        bank_accounts = db.query(BankAccount).filter(
            BankAccount.criminal_case_id == case_id
        ).all()

        return bank_accounts

    except Exception as e:
        print(f"Error getting case bank accounts: {e}")
        return []

@router.get("/{case_id}/suspects", response_model=List[SuspectResponse])
def get_case_suspects(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get suspects related to a specific criminal case"""
    # Get the criminal case
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    try:
        # Use FK relationship only
        suspects = db.query(Suspect).filter(
            Suspect.criminal_case_id == case_id
        ).all()

        return suspects

    except Exception as e:
        print(f"Error getting case suspects: {e}")
        return []

@router.put("/{case_id}", response_model=CriminalCaseResponse)
def update_criminal_case(
    case_id: int,
    criminal_case: CriminalCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # Update fields
    update_data = criminal_case.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_case, field, value)
    
    # Update Thai date fields if complaint_date is updated
    if 'complaint_date' in update_data and db_case.complaint_date:
        from app.services.data_migration import DataMigration
        migration = DataMigration()
        db_case.complaint_date_thai = migration._format_thai_date(db_case.complaint_date)
    
    if 'incident_date' in update_data and db_case.incident_date:
        from app.services.data_migration import DataMigration
        migration = DataMigration()
        db_case.incident_date_thai = migration._format_thai_date(db_case.incident_date)
    
    try:
        db.commit()
        db.refresh(db_case)

        # Add related data counts using case ID
        db_case.bank_accounts_count = get_bank_accounts_count(db, db_case.id)
        db_case.suspects_count = get_suspects_count(db, db_case.id)
        # case_id is already in the database

        # Add row styling
        complaint_date_str = db_case.complaint_date_thai or str(db_case.complaint_date) if db_case.complaint_date else ''
        db_case.row_class = get_case_row_class(db_case.status, complaint_date_str, db_case.bank_accounts_count)
        db_case.row_style = get_case_row_style(db_case.status, complaint_date_str, db_case.bank_accounts_count)

        return db_case
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating criminal case: {str(e)}")

@router.delete("/{case_id}")
def delete_criminal_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not db_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    try:
        db.delete(db_case)
        db.commit()
        return {"ok": True}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting criminal case: {str(e)}")