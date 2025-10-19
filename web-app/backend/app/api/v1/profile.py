#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
API endpoints สำหรับจัดการโปรไฟล์ผู้ใช้งาน
รองรับการอัปโหลดลายเซ็น (PNG format only)
"""

import os
import shutil
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import Optional
from pydantic import BaseModel, EmailStr

from app.core.database import get_db
from app.api.v1.auth import get_current_user
from app.models.user import User
from app.core.config import settings

router = APIRouter()

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    full_name: str
    position: Optional[str]
    phone_number: Optional[str]
    line_id: Optional[str]
    signature_path: Optional[str]
    has_signature: bool

    class Config:
        from_attributes = True

class UpdateProfileRequest(BaseModel):
    full_name: Optional[str] = None
    position: Optional[str] = None
    phone_number: Optional[str] = None
    line_id: Optional[str] = None
    email: Optional[EmailStr] = None

@router.get("/me", response_model=UserProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ดึงข้อมูลโปรไฟล์ของผู้ใช้งานปัจจุบัน
    """
    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        position=current_user.position,
        phone_number=current_user.phone_number,
        line_id=current_user.line_id,
        signature_path=current_user.signature_path,
        has_signature=bool(current_user.signature_path)
    )

@router.put("/me", response_model=UserProfileResponse)
def update_my_profile(
    profile_data: UpdateProfileRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    อัปเดตข้อมูลโปรไฟล์ของผู้ใช้งานปัจจุบัน
    """
    # Update fields if provided
    if profile_data.full_name is not None:
        current_user.full_name = profile_data.full_name
    if profile_data.position is not None:
        current_user.position = profile_data.position
    if profile_data.phone_number is not None:
        current_user.phone_number = profile_data.phone_number
    if profile_data.line_id is not None:
        current_user.line_id = profile_data.line_id
    if profile_data.email is not None:
        # Check if email already exists
        existing_user = db.query(User).filter(
            User.email == profile_data.email,
            User.id != current_user.id
        ).first()
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        current_user.email = profile_data.email

    db.commit()
    db.refresh(current_user)

    return UserProfileResponse(
        id=current_user.id,
        username=current_user.username,
        email=current_user.email,
        full_name=current_user.full_name,
        position=current_user.position,
        phone_number=current_user.phone_number,
        line_id=current_user.line_id,
        signature_path=current_user.signature_path,
        has_signature=bool(current_user.signature_path)
    )

@router.post("/me/signature")
async def upload_signature(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    อัปโหลดไฟล์ลายเซ็น (PNG format only)

    - รองรับเฉพาะไฟล์ .png เท่านั้น
    - ขนาดไฟล์ไม่เกิน 2MB
    - บันทึกไฟล์ใน /app/uploads/signatures/{user_id}.png
    """
    # ตรวจสอบ content type
    if file.content_type != "image/png":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only PNG files are allowed"
        )

    # ตรวจสอบขนาดไฟล์ (ไม่เกิน 2MB)
    MAX_FILE_SIZE = 2 * 1024 * 1024  # 2MB
    contents = await file.read()
    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File size must not exceed 2MB"
        )

    # สร้างโฟลเดอร์สำหรับเก็บลายเซ็น
    signatures_dir = os.path.join(settings.UPLOAD_DIR, "signatures")
    os.makedirs(signatures_dir, exist_ok=True)

    # สร้างชื่อไฟล์ใหม่ (user_id.png)
    filename = f"{current_user.id}.png"
    file_path = os.path.join(signatures_dir, filename)

    # ลบไฟล์เก่าถ้ามี
    if os.path.exists(file_path):
        os.remove(file_path)

    # บันทึกไฟล์ใหม่
    with open(file_path, "wb") as buffer:
        buffer.write(contents)

    # อัปเดต path ใน database
    signature_relative_path = f"signatures/{filename}"
    current_user.signature_path = signature_relative_path
    db.commit()

    return {
        "message": "Signature uploaded successfully",
        "signature_path": signature_relative_path,
        "uploaded_at": datetime.now().isoformat()
    }

@router.delete("/me/signature")
def delete_signature(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    ลบไฟล์ลายเซ็นของผู้ใช้งาน
    """
    if not current_user.signature_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No signature found"
        )

    # ลบไฟล์
    file_path = os.path.join(settings.UPLOAD_DIR, current_user.signature_path)
    if os.path.exists(file_path):
        os.remove(file_path)

    # ลบ path ใน database
    current_user.signature_path = None
    db.commit()

    return {
        "message": "Signature deleted successfully",
        "deleted_at": datetime.now().isoformat()
    }

@router.get("/me/signature")
def get_signature(
    current_user: User = Depends(get_current_user)
):
    """
    ดึงข้อมูล URL ของลายเซ็น
    """
    if not current_user.signature_path:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No signature found"
        )

    return {
        "signature_path": current_user.signature_path,
        "signature_url": f"/uploads/{current_user.signature_path}"
    }
