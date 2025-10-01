from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core import get_db
from app.models import PostArrest, User
from app.schemas import PostArrestCreate, PostArrestUpdate, PostArrestResponse
from app.api.v1.auth import get_current_user

router = APIRouter()

def generate_arrest_number(db: Session) -> str:
    current_year = datetime.now().year + 543
    count = db.query(PostArrest).filter(
        PostArrest.arrest_number.like(f"AR-{current_year}-%")
    ).count()
    return f"AR-{current_year}-{count + 1:04d}"

@router.post("/", response_model=PostArrestResponse)
def create_post_arrest(
    post_arrest: PostArrestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    arrest_number = generate_arrest_number(db)
    db_arrest = PostArrest(
        **post_arrest.dict(),
        arrest_number=arrest_number,
        created_by=current_user.id
    )
    db.add(db_arrest)
    db.commit()
    db.refresh(db_arrest)
    return db_arrest

@router.get("/", response_model=List[PostArrestResponse])
def read_post_arrests(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    arrests = db.query(PostArrest).offset(skip).limit(limit).all()
    return arrests

@router.get("/{arrest_id}", response_model=PostArrestResponse)
def read_post_arrest(
    arrest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    arrest = db.query(PostArrest).filter(PostArrest.id == arrest_id).first()
    if arrest is None:
        raise HTTPException(status_code=404, detail="Arrest record not found")
    return arrest

@router.put("/{arrest_id}", response_model=PostArrestResponse)
def update_post_arrest(
    arrest_id: int,
    post_arrest: PostArrestUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_arrest = db.query(PostArrest).filter(PostArrest.id == arrest_id).first()
    if db_arrest is None:
        raise HTTPException(status_code=404, detail="Arrest record not found")

    for key, value in post_arrest.dict(exclude_unset=True).items():
        setattr(db_arrest, key, value)

    db.commit()
    db.refresh(db_arrest)
    return db_arrest

@router.delete("/{arrest_id}")
def delete_post_arrest(
    arrest_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_arrest = db.query(PostArrest).filter(PostArrest.id == arrest_id).first()
    if db_arrest is None:
        raise HTTPException(status_code=404, detail="Arrest record not found")

    db.delete(db_arrest)
    db.commit()
    return {"ok": True}