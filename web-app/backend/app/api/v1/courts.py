from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core import get_db
from app.models import Court, User
from app.schemas import CourtCreate, CourtUpdate, Court as CourtSchema
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.get("/", response_model=List[CourtSchema])
def get_courts(
    skip: int = 0,
    limit: int = 300,
    court_type: Optional[str] = Query(None, description="Filter by court type"),
    region: Optional[str] = Query(None, description="Filter by region"),
    province: Optional[str] = Query(None, description="Filter by province"),
    search: Optional[str] = Query(None, description="Search by court name"),
    db: Session = Depends(get_db)
):
    """Get list of courts with optional filters (public endpoint - no auth required)"""
    query = db.query(Court)

    if court_type:
        query = query.filter(Court.court_type == court_type)

    if region:
        query = query.filter(Court.region == region)

    if province:
        query = query.filter(Court.province == province)

    if search:
        query = query.filter(Court.court_name.ilike(f"%{search}%"))

    courts = query.offset(skip).limit(limit).all()
    return courts

@router.get("/types")
def get_court_types(
    db: Session = Depends(get_db)
):
    """Get list of unique court types (public endpoint - no auth required)"""
    court_types = db.query(Court.court_type).distinct().filter(Court.court_type.isnot(None)).all()
    return {"court_types": [ct[0] for ct in court_types]}

@router.get("/regions")
def get_court_regions(
    db: Session = Depends(get_db)
):
    """Get list of unique regions (public endpoint - no auth required)"""
    regions = db.query(Court.region).distinct().filter(Court.region.isnot(None)).all()
    return {"regions": [r[0] for r in regions]}

@router.get("/provinces")
def get_court_provinces(
    db: Session = Depends(get_db)
):
    """Get list of unique provinces (public endpoint - no auth required)"""
    provinces = db.query(Court.province).distinct().filter(Court.province.isnot(None)).all()
    return {"provinces": sorted([p[0] for p in provinces])}

@router.get("/{court_id}", response_model=CourtSchema)
def get_court(
    court_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific court by ID"""
    court = db.query(Court).filter(Court.id == court_id).first()
    if court is None:
        raise HTTPException(status_code=404, detail="Court not found")
    return court

@router.post("/", response_model=CourtSchema)
def create_court(
    court: CourtCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new court (admin only)"""
    # Check if court name already exists
    existing = db.query(Court).filter(Court.court_name == court.court_name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Court name already exists")

    db_court = Court(**court.dict())
    db.add(db_court)
    db.commit()
    db.refresh(db_court)
    return db_court

@router.put("/{court_id}", response_model=CourtSchema)
def update_court(
    court_id: int,
    court: CourtUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update a court (admin only)"""
    db_court = db.query(Court).filter(Court.id == court_id).first()
    if db_court is None:
        raise HTTPException(status_code=404, detail="Court not found")

    update_data = court.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_court, key, value)

    db.commit()
    db.refresh(db_court)
    return db_court

@router.delete("/{court_id}")
def delete_court(
    court_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete a court (admin only)"""
    db_court = db.query(Court).filter(Court.id == court_id).first()
    if db_court is None:
        raise HTTPException(status_code=404, detail="Court not found")

    db.delete(db_court)
    db.commit()
    return {"message": "Court deleted successfully"}
