from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core import get_db
from app.models.suspect import Suspect
from app.models.criminal_case import CriminalCase
from app.schemas.suspect import SuspectCreate, SuspectUpdate, SuspectResponse
from app.api.v1.auth import get_current_user
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=SuspectResponse)
def create_suspect(
    suspect: SuspectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new suspect record"""
    
    # Validate criminal case exists
    if suspect.criminal_case_id:
        criminal_case = db.query(CriminalCase).filter(CriminalCase.id == suspect.criminal_case_id).first()
        if not criminal_case:
            raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # Create suspect
    db_suspect = Suspect(
        **suspect.dict(),
        created_by=current_user.id
    )
    
    db.add(db_suspect)
    db.commit()
    db.refresh(db_suspect)
    
    return db_suspect

@router.get("/", response_model=List[SuspectResponse])
def read_suspects(
    skip: int = 0,
    limit: int = 100,
    criminal_case_id: Optional[int] = Query(None, description="Filter by criminal case ID"),
    status: Optional[str] = Query(None, description="Filter by status"),
    case_type: Optional[str] = Query(None, description="Filter by case type"),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get suspects with filtering options"""
    
    query = db.query(Suspect)
    
    # Apply filters
    if criminal_case_id:
        query = query.filter(Suspect.criminal_case_id == criminal_case_id)
    
    if status:
        query = query.filter(Suspect.status == status)
    
    if case_type:
        query = query.filter(Suspect.case_type == case_type)
    
    suspects = query.offset(skip).limit(limit).all()
    return suspects

@router.get("/{suspect_id}", response_model=SuspectResponse)
def read_suspect(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific suspect by ID"""
    
    suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")
    
    return suspect

@router.put("/{suspect_id}", response_model=SuspectResponse)
def update_suspect(
    suspect_id: int,
    suspect_update: SuspectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a suspect record"""
    
    db_suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not db_suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")
    
    # Validate criminal case exists if provided
    if suspect_update.criminal_case_id:
        criminal_case = db.query(CriminalCase).filter(CriminalCase.id == suspect_update.criminal_case_id).first()
        if not criminal_case:
            raise HTTPException(status_code=404, detail="Criminal case not found")
    
    # Update fields
    update_data = suspect_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_suspect, field, value)
    
    db.commit()
    db.refresh(db_suspect)
    
    return db_suspect

@router.delete("/{suspect_id}")
def delete_suspect(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a suspect record"""
    
    db_suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not db_suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")
    
    db.delete(db_suspect)
    db.commit()
    
    return {"message": "Suspect deleted successfully"}

@router.get("/criminal-case/{criminal_case_id}", response_model=List[SuspectResponse])
def get_suspects_by_criminal_case(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all suspects for a specific criminal case"""
    
    # Validate criminal case exists
    criminal_case = db.query(CriminalCase).filter(CriminalCase.id == criminal_case_id).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="Criminal case not found")
    
    suspects = db.query(Suspect).filter(
        Suspect.criminal_case_id == criminal_case_id
    ).all()
    
    return suspects
