from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List
from app.core import get_db
from app.models import CFR, CriminalCase, User
from app.api.v1.auth import get_current_user
import pandas as pd
import os
from datetime import datetime

router = APIRouter()

@router.post("/upload/{criminal_case_id}")
async def upload_cfr_file(
    criminal_case_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    อัพโหลดไฟล์ CFR และบันทึกข้อมูลลงฐานข้อมูล
    
    Logic:
    - ถ้าชื่อไฟล์ซ้ำ → ลบข้อมูลเดิมทั้งหมดก่อน แล้ว insert ใหม่
    - ถ้าชื่อไฟล์ใหม่ → insert เพิ่ม
    """
    
    # ตรวจสอบว่าคดีมีอยู่จริง
    criminal_case = db.query(CriminalCase).filter(CriminalCase.id == criminal_case_id).first()
    if not criminal_case:
        raise HTTPException(status_code=404, detail="ไม่พบข้อมูลคดี")
    
    # ตรวจสอบว่าเป็นไฟล์ .xlsx
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="รองรับเฉพาะไฟล์ .xlsx เท่านั้น")
    
    try:
        # อ่านไฟล์ Excel
        contents = await file.read()
        
        # Save to temp file
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(contents)
        
        # อ่านข้อมูลด้วย pandas โดยกำหนดให้เลขบัญชีเป็น string เพื่อรักษาเลข 0 หน้า
        df = pd.read_excel(temp_path, dtype=str)
        
        # ลบไฟล์ temp
        os.remove(temp_path)
        
        # ตรวจสอบว่ามีข้อมูลเดิมที่ชื่อไฟล์เดียวกันหรือไม่
        existing_records = db.query(CFR).filter(
            CFR.criminal_case_id == criminal_case_id,
            CFR.filename == file.filename
        ).all()
        
        if existing_records:
            # ลบข้อมูลเดิม
            for record in existing_records:
                db.delete(record)
            db.commit()
        
        # Helper function to safely convert values
        def safe_int(val):
            if pd.isna(val) or val == '' or val == 'nan':
                return None
            try:
                return int(float(str(val)))
            except:
                return None
        
        def safe_float(val):
            if pd.isna(val) or val == '' or val == 'nan':
                return None
            try:
                return float(str(val))
            except:
                return None
        
        def safe_str(val):
            if pd.isna(val) or val == '' or val == 'nan':
                return None
            return str(val).strip()
        
        # Insert ข้อมูลใหม่
        inserted_count = 0
        for _, row in df.iterrows():
            cfr_record = CFR(
                criminal_case_id=criminal_case_id,
                filename=file.filename,
                upload_date=datetime.now(),
                
                # CFR Data
                response_id=safe_int(row['response_id']),
                bank_case_id=safe_str(row['bank_case_id']),
                timestamp_insert=safe_str(row['timestamp_insert']),
                
                # From Account (รักษาเลข 0 หน้า)
                from_bank_code=safe_int(row['from_bank_code']),
                from_bank_short_name=safe_str(row['from_bank_short_name']),
                from_account_no=safe_str(row['from_account_no']),  # รักษาเลข 0
                from_account_name=safe_str(row['from_account_name']),
                
                # To Account (รักษาเลข 0 หน้า)
                to_bank_code=safe_int(row['to_bank_code']),
                to_bank_short_name=safe_str(row['to_bank_short_name']),
                to_bank_branch=safe_str(row['to_bank_branch']),
                to_id_type=safe_str(row['to_id_type']),
                to_id=safe_str(row['to_id']),  # รักษาเลข 0
                first_name=safe_str(row['first_name']),
                last_name=safe_str(row['last_name']),
                phone_number=safe_str(row['phone_number']),  # รักษาเลข 0
                
                # PromptPay (รักษาเลข 0 หน้า)
                promptpay_type=safe_str(row['promptpay_type']),
                promptpay_id=safe_str(row['promptpay_id']),  # รักษาเลข 0
                
                # To Account Details (รักษาเลข 0 หน้า)
                to_account_no=safe_str(row['to_account_no']),  # รักษาเลข 0
                to_account_name=safe_str(row['to_account_name']),
                to_account_status=safe_str(row['to_account_status']),
                to_open_date=safe_str(row['to_open_date']),
                to_close_date=safe_str(row['to_close_date']),
                to_balance=safe_float(row['to_balance']),
                
                # Transfer
                transfer_date=safe_str(row['transfer_date']),
                transfer_channel=safe_str(row['transfer_channel']),
                transfer_channel_detail=safe_str(row['transfer_channel_detail']),
                transfer_time=safe_str(row['transfer_time']),
                transfer_amount=safe_float(row['transfer_amount']),
                transfer_description=safe_str(row['transfer_description']),
                transfer_ref=safe_str(row['transfer_ref']),
                
                created_by=current_user.id
            )
            db.add(cfr_record)
            inserted_count += 1
        
        db.commit()
        
        return {
            "message": "อัพโหลดไฟล์ CFR สำเร็จ",
            "filename": file.filename,
            "records_inserted": inserted_count,
            "records_deleted": len(existing_records) if existing_records else 0
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"เกิดข้อผิดพลาด: {str(e)}")

@router.get("/{criminal_case_id}/files")
def get_cfr_files(
    criminal_case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงรายการไฟล์ CFR ที่อัพโหลดสำหรับคดีนี้"""
    
    files = db.query(
        CFR.filename,
        func.count(CFR.id).label('record_count'),
        func.max(CFR.upload_date).label('last_upload')
    ).filter(
        CFR.criminal_case_id == criminal_case_id
    ).group_by(CFR.filename).all()
    
    return [
        {
            "filename": f.filename,
            "record_count": f.record_count,
            "last_upload": f.last_upload
        }
        for f in files
    ]

@router.get("/{criminal_case_id}/records")
def get_cfr_records(
    criminal_case_id: int,
    filename: str = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ดึงข้อมูล CFR records"""
    
    query = db.query(CFR).filter(CFR.criminal_case_id == criminal_case_id)
    
    if filename:
        query = query.filter(CFR.filename == filename)
    
    records = query.order_by(CFR.transfer_date.desc(), CFR.transfer_time.desc()).offset(skip).limit(limit).all()
    
    return {
        "records": records,
        "total": query.count()
    }

@router.delete("/{criminal_case_id}/file/{filename}")
def delete_cfr_file(
    criminal_case_id: int,
    filename: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """ลบไฟล์ CFR และข้อมูลทั้งหมดของไฟล์นั้น"""
    
    deleted = db.query(CFR).filter(
        CFR.criminal_case_id == criminal_case_id,
        CFR.filename == filename
    ).delete()
    
    db.commit()
    
    return {
        "message": f"ลบไฟล์ {filename} สำเร็จ",
        "records_deleted": deleted
    }

