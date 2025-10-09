from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload
from typing import List
from datetime import datetime
from app.core import get_db
from app.models import User, PoliceRank, UserRole, UserRoleMapping
from app.schemas.user_registration import UserRegistrationResponse, PoliceRankResponse, UserRoleResponse
from app.api.v1.auth import get_current_user
from app.core.security import verify_password

router = APIRouter()

def check_admin_permission(current_user: User = Depends(get_current_user)):
    """Check if current user has admin permission"""
    if not current_user.role or current_user.role.role_name != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="ไม่มีสิทธิ์เข้าถึง"
        )
    return current_user

def format_user_response(user: User) -> dict:
    """Format user response with proper role_mappings"""
    user_dict = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "position": user.position,
        "phone_number": user.phone_number,
        "line_id": user.line_id,
        "is_active": user.is_active,
        "is_approved": user.is_approved,
        "failed_login_attempts": user.failed_login_attempts,
        "locked_until": user.locked_until,
        "created_at": user.created_at,
        "approved_at": user.approved_at,
        "rank": None,
        "role": None,
        "role_mappings": []
    }
    
    if user.rank:
        user_dict["rank"] = {
            "id": user.rank.id,
            "rank_short": user.rank.rank_short,
            "rank_full": user.rank.rank_full,
            "rank_english": user.rank.rank_english
        }
    
    if user.role:
        user_dict["role"] = {
            "id": user.role.id,
            "role_name": user.role.role_name,
            "role_display": user.role.role_display,
            "role_description": user.role.role_description
        }
    
    if user.role_mappings:
        user_dict["role_mappings"] = [
            {
                "id": mapping.role.id,
                "role_name": mapping.role.role_name,
                "role_display": mapping.role.role_display,
                "role_description": mapping.role.role_description
            }
            for mapping in user.role_mappings
        ]
    
    return user_dict

@router.get("/pending-users", response_model=List[UserRegistrationResponse])
def get_pending_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(check_admin_permission)
):
    """Get all users pending approval"""
    users = db.query(User).options(
        joinedload(User.rank),
        joinedload(User.role),
        joinedload(User.role_mappings).joinedload(UserRoleMapping.role)
    ).filter(
        User.is_approved == False
    ).order_by(User.created_at.desc()).all()
    
    return [format_user_response(user) for user in users]

@router.post("/approve-user/{user_id}")
def approve_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(check_admin_permission)
):
    """Approve a user registration"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบผู้ใช้"
        )
    
    if user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ผู้ใช้นี้ได้รับการอนุมัติแล้ว"
        )
    
    # Approve user
    user.is_approved = True
    user.is_active = True
    user.approved_at = datetime.utcnow()
    user.approved_by = admin_user.id
    
    db.commit()
    
    return {"message": "อนุมัติผู้ใช้เรียบร้อยแล้ว"}

@router.post("/reject-user/{user_id}")
def reject_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(check_admin_permission)
):
    """Reject a user registration"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบผู้ใช้"
        )
    
    if user.is_approved:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ผู้ใช้นี้ได้รับการอนุมัติแล้ว"
        )
    
    # Delete user (reject)
    db.delete(user)
    db.commit()
    
    return {"message": "ปฏิเสธการสมัครสมาชิกเรียบร้อยแล้ว"}

@router.get("/all-users", response_model=List[UserRegistrationResponse])
def get_all_users(
    db: Session = Depends(get_db),
    admin_user: User = Depends(check_admin_permission)
):
    """Get all users (admin only)"""
    users = db.query(User).options(
        joinedload(User.rank),
        joinedload(User.role),
        joinedload(User.role_mappings).joinedload(UserRoleMapping.role)
    ).order_by(User.created_at.desc()).all()
    
    return [format_user_response(user) for user in users]

@router.post("/unlock-user/{user_id}")
def unlock_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(check_admin_permission)
):
    """Unlock a locked user account"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบผู้ใช้"
        )
    
    # Unlock user
    user.failed_login_attempts = 0
    user.locked_until = None
    
    db.commit()
    
    return {"message": "ปลดล็อคผู้ใช้เรียบร้อยแล้ว"}

@router.post("/deactivate-user/{user_id}")
def deactivate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(check_admin_permission)
):
    """Deactivate a user account"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบผู้ใช้"
        )
    
    if user.id == admin_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="ไม่สามารถปิดใช้งานบัญชีตัวเองได้"
        )
    
    # Deactivate user
    user.is_active = False
    
    db.commit()
    
    return {"message": "ปิดใช้งานผู้ใช้เรียบร้อยแล้ว"}

@router.post("/activate-user/{user_id}")
def activate_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin_user: User = Depends(check_admin_permission)
):
    """Activate a user account"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="ไม่พบผู้ใช้"
        )
    
    # Activate user
    user.is_active = True
    
    db.commit()
    
    return {"message": "เปิดใช้งานผู้ใช้เรียบร้อยแล้ว"}
