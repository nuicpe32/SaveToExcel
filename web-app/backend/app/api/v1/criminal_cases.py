from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime, timedelta
from app.core import get_db
from app.models import CriminalCase, User, BankAccount, Suspect
from app.schemas import CriminalCaseCreate, CriminalCaseUpdate, CriminalCaseResponse, BankAccountResponse, SuspectResponse
from app.api.v1.auth import get_current_user
from app.utils.string_utils import safe_string_conversion, name_contains, clean_name_for_matching
from app.utils.case_styling import get_case_row_class, get_case_row_style
from app.utils.case_number_generator import generate_case_number, validate_case_number
from app.utils.virtual_fields import format_thai_date, get_bank_accounts_count, get_suspects_count

router = APIRouter()

@router.post("/", response_model=CriminalCaseResponse, status_code=201)
def create_criminal_case(
    criminal_case: CriminalCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case_data = criminal_case.dict()

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
        created_by=current_user.id,
        owner_id=current_user.id  # Set owner to the creator
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    # Compute virtual fields
    complaint_date_thai = format_thai_date(db_case.complaint_date)
    incident_date_thai = format_thai_date(db_case.incident_date)
    bank_accounts_count = get_bank_accounts_count(db, db_case.id)
    suspects_count = get_suspects_count(db, db_case.id)

    # Add row styling
    complaint_date_str = complaint_date_thai or str(db_case.complaint_date) if db_case.complaint_date else ''
    row_class = get_case_row_class(db_case.status, complaint_date_str, bank_accounts_count)
    row_style = get_case_row_style(db_case.status, complaint_date_str, bank_accounts_count)

    # Create response with virtual fields
    response = CriminalCaseResponse.from_orm(db_case)
    response.complaint_date_thai = complaint_date_thai
    response.incident_date_thai = incident_date_thai
    response.bank_accounts_count = bank_accounts_count
    response.suspects_count = suspects_count
    response.row_class = row_class
    response.row_style = row_style

    return response

# get_bank_accounts_count() moved to app.utils.virtual_fields

def get_case_id_from_related_data(db: Session, case_id: int) -> str:
    """Get CaseID from the criminal case itself"""
    try:
        # Get the case directly by ID
        case = db.query(CriminalCase).options(
        joinedload(CriminalCase.owner).joinedload(User.rank)
    ).filter(CriminalCase.id == case_id).first()
        if case and case.case_id:
            return case.case_id
        return ""
    except Exception as e:
        print(f"Error getting CaseID: {e}")
        return ""

# get_suspects_count() moved to app.utils.virtual_fields

@router.get("/", response_model=List[CriminalCaseResponse])
def read_criminal_cases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Build query based on user role
    query = db.query(CriminalCase).options(
        joinedload(CriminalCase.owner).joinedload(User.rank)
    )
    
    # If user is not admin, filter by owner_id
    if not current_user.role or current_user.role.role_name != "admin":
        query = query.filter(CriminalCase.owner_id == current_user.id)
    
    cases = query.order_by(CriminalCase.complaint_date.desc()).offset(skip).limit(limit).all()

    # Add virtual fields to each case
    response_cases = []
    for case in cases:
        # Compute virtual fields
        complaint_date_thai = format_thai_date(case.complaint_date)
        incident_date_thai = format_thai_date(case.incident_date)
        bank_accounts_count = get_bank_accounts_count(db, case.id)
        suspects_count = get_suspects_count(db, case.id)

        # Add row styling information
        complaint_date_str = complaint_date_thai or str(case.complaint_date) if case.complaint_date else ''
        row_class = get_case_row_class(case.status, complaint_date_str, bank_accounts_count)
        row_style = get_case_row_style(case.status, complaint_date_str, bank_accounts_count)

        # Create response with virtual fields
        response = CriminalCaseResponse.from_orm(case)
        response.complaint_date_thai = complaint_date_thai
        response.incident_date_thai = incident_date_thai
        response.bank_accounts_count = bank_accounts_count
        response.suspects_count = suspects_count
        response.row_class = row_class
        response.row_style = row_style
        
        response_cases.append(response)

    return response_cases

@router.get("/aging", response_model=List[CriminalCaseResponse])
def read_aging_cases(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    six_months_ago = datetime.now() - timedelta(days=180)
    
    # Build query based on user role
    query = db.query(CriminalCase).options(
        joinedload(CriminalCase.owner).joinedload(User.rank)
    ).filter(
        CriminalCase.case_date < six_months_ago.date(),
        CriminalCase.status == "active"
    )
    
    # If user is not admin, filter by owner_id
    if not current_user.role or current_user.role.role_name != "admin":
        query = query.filter(CriminalCase.owner_id == current_user.id)
    
    cases = query.all()
    return cases

@router.get("/{case_id}", response_model=CriminalCaseResponse)
def read_criminal_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case = db.query(CriminalCase).options(
        joinedload(CriminalCase.owner).joinedload(User.rank)
    ).filter(CriminalCase.id == case_id).first()
    if case is None:
        raise HTTPException(status_code=404, detail="Case not found")

    # Compute virtual fields
    complaint_date_thai = format_thai_date(case.complaint_date)
    incident_date_thai = format_thai_date(case.incident_date)
    bank_accounts_count = get_bank_accounts_count(db, case.id)
    suspects_count = get_suspects_count(db, case.id)

    # Add row styling
    complaint_date_str = complaint_date_thai or str(case.complaint_date) if case.complaint_date else ''
    row_class = get_case_row_class(case.status, complaint_date_str, bank_accounts_count)
    row_style = get_case_row_style(case.status, complaint_date_str, bank_accounts_count)

    # Create response with virtual fields
    response = CriminalCaseResponse.from_orm(case)
    response.complaint_date_thai = complaint_date_thai
    response.incident_date_thai = incident_date_thai
    response.bank_accounts_count = bank_accounts_count
    response.suspects_count = suspects_count
    response.row_class = row_class
    response.row_style = row_style

    return response


@router.get("/{case_id}/bank-accounts", response_model=List[BankAccountResponse])
def get_case_bank_accounts(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get bank accounts related to a specific criminal case"""
    # Get the criminal case
    case = db.query(CriminalCase).options(
        joinedload(CriminalCase.owner).joinedload(User.rank)
    ).filter(CriminalCase.id == case_id).first()
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
    case = db.query(CriminalCase).options(
        joinedload(CriminalCase.owner).joinedload(User.rank)
    ).filter(CriminalCase.id == case_id).first()
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
    
    try:
        db.commit()
        db.refresh(db_case)

        # Compute virtual fields
        complaint_date_thai = format_thai_date(db_case.complaint_date)
        incident_date_thai = format_thai_date(db_case.incident_date)
        bank_accounts_count = get_bank_accounts_count(db, db_case.id)
        suspects_count = get_suspects_count(db, db_case.id)

        # Add row styling
        complaint_date_str = complaint_date_thai or str(db_case.complaint_date) if db_case.complaint_date else ''
        row_class = get_case_row_class(db_case.status, complaint_date_str, bank_accounts_count)
        row_style = get_case_row_style(db_case.status, complaint_date_str, bank_accounts_count)

        # Create response with virtual fields
        response = CriminalCaseResponse.from_orm(db_case)
        response.complaint_date_thai = complaint_date_thai
        response.incident_date_thai = incident_date_thai
        response.bank_accounts_count = bank_accounts_count
        response.suspects_count = suspects_count
        response.row_class = row_class
        response.row_style = row_style

        return response
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