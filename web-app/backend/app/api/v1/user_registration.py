from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.core import get_db
from app.models import User, PoliceRank, UserRole, UserRoleMapping
from app.schemas.user_registration import (
    UserRegistrationCreate, 
    UserRegistrationResponse,
    PoliceRankResponse,
    UserRoleResponse
)
from app.core.security import get_password_hash

router = APIRouter()

@router.get("/ranks", response_model=List[PoliceRankResponse])
def get_police_ranks(db: Session = Depends(get_db)):
    """Get all police ranks for registration form"""
    ranks = db.query(PoliceRank).order_by(PoliceRank.id).all()
    return ranks

@router.get("/roles", response_model=List[UserRoleResponse])
def get_user_roles(db: Session = Depends(get_db)):
    """Get all user roles for registration form"""
    roles = db.query(UserRole).filter(UserRole.is_active == True).order_by(UserRole.id).all()
    return roles

@router.post("/register", response_model=UserRegistrationResponse)
def register_user(
    user_data: UserRegistrationCreate,
    db: Session = Depends(get_db)
):
    """Register a new user (requires admin approval)"""
    
    # Check if username already exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ชื่อผู้ใช้นี้มีอยู่แล้ว"
        )
    
    # Check if email already exists
    existing_email = db.query(User).filter(User.email == user_data.email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="อีเมลนี้มีอยู่แล้ว"
        )
    
    # Validate rank exists
    rank = db.query(PoliceRank).filter(PoliceRank.id == user_data.rank_id).first()
    if not rank:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ยศที่เลือกไม่ถูกต้อง"
        )
    
    # Validate roles exist and get the first one (primary role)
    if not user_data.role_ids:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ต้องเลือกสิทธิ์อย่างน้อย 1 สิทธิ์"
        )
    
    primary_role = db.query(UserRole).filter(UserRole.id == user_data.role_ids[0]).first()
    if not primary_role:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="สิทธิ์ที่เลือกไม่ถูกต้อง"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        rank_id=user_data.rank_id,
        full_name=user_data.full_name,
        position=user_data.position,
        phone_number=user_data.phone_number,
        line_id=user_data.line_id,
        role_id=primary_role.id,  # Use first role as primary
        is_active=False,  # Requires admin approval
        is_approved=False,
        failed_login_attempts=0
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    # Add role mappings for all selected roles
    for role_id in user_data.role_ids:
        role_mapping = UserRoleMapping(
            user_id=new_user.id,
            role_id=role_id
        )
        db.add(role_mapping)
    
    db.commit()
    
    return new_user

@router.get("/check-username/{username}")
def check_username_availability(username: str, db: Session = Depends(get_db)):
    """Check if username is available"""
    existing_user = db.query(User).filter(User.username == username).first()
    return {"available": existing_user is None}

@router.get("/check-email/{email}")
def check_email_availability(email: str, db: Session = Depends(get_db)):
    """Check if email is available"""
    existing_user = db.query(User).filter(User.email == email).first()
    return {"available": existing_user is None}
