from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from app.core import get_db
from app.models import Suspect, User
from app.schemas import SuspectCreate, SuspectUpdate, SuspectResponse
from app.api.v1.auth import get_current_user

router = APIRouter()

def generate_document_number(db: Session) -> str:
    current_year = datetime.now().year + 543
    count = db.query(Suspect).filter(
        Suspect.document_number.like(f"SUS-{current_year}-%")
    ).count()
    return f"SUS-{current_year}-{count + 1:04d}"

@router.post("/", response_model=SuspectResponse)
def create_suspect(
    suspect: SuspectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Generate document number if not provided
    document_number = suspect.document_number or generate_document_number(db)
    
    # Create suspect data without document_number to avoid duplicate
    suspect_data = suspect.dict()
    suspect_data.pop('document_number', None)  # Remove document_number if exists
    
    db_suspect = Suspect(
        **suspect_data,
        document_number=document_number,
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
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    suspects = db.query(Suspect).options(joinedload(Suspect.criminal_case)).offset(skip).limit(limit).all()
    return suspects

@router.get("/{suspect_id}", response_model=SuspectResponse)
def read_suspect(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    suspect = db.query(Suspect).options(joinedload(Suspect.criminal_case)).filter(Suspect.id == suspect_id).first()
    if suspect is None:
        raise HTTPException(status_code=404, detail="Suspect not found")
    return suspect

@router.put("/{suspect_id}", response_model=SuspectResponse)
def update_suspect(
    suspect_id: int,
    suspect: SuspectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if db_suspect is None:
        raise HTTPException(status_code=404, detail="Suspect not found")

    for key, value in suspect.dict(exclude_unset=True).items():
        setattr(db_suspect, key, value)

    db.commit()
    db.refresh(db_suspect)
    return db_suspect

@router.delete("/{suspect_id}")
def delete_suspect(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if db_suspect is None:
        raise HTTPException(status_code=404, detail="Suspect not found")

    db.delete(db_suspect)
    db.commit()
    return {"ok": True}