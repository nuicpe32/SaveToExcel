#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Utility functions for computing virtual fields
(fields that don't exist in database but computed at runtime)
"""

from datetime import date
from typing import Optional
from sqlalchemy.orm import Session
from app.models import BankAccount, Suspect

def format_thai_date(date_obj: Optional[date]) -> Optional[str]:
    """
    แปลงวันที่เป็นรูปแบบภาษาไทย พ.ศ.
    
    Args:
        date_obj: วันที่ในรูปแบบ date object
    
    Returns:
        str: วันที่ในรูปแบบไทย เช่น "15 มกราคม 2568"
        None: ถ้าไม่มีวันที่
    """
    if not date_obj:
        return None
    
    thai_months = [
        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
        "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
        "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
    ]
    
    day = date_obj.day
    month = thai_months[date_obj.month - 1]
    year = date_obj.year + 543  # แปลง ค.ศ. เป็น พ.ศ.
    
    return f"{day} {month} {year}"


def format_thai_date_short(date_obj: Optional[date]) -> Optional[str]:
    """
    แปลงวันที่เป็นรูปแบบภาษาไทยแบบสั้น
    
    Args:
        date_obj: วันที่ในรูปแบบ date object
    
    Returns:
        str: วันที่ในรูปแบบไทยสั้น เช่น "15 ม.ค. 68"
        None: ถ้าไม่มีวันที่
    """
    if not date_obj:
        return None
    
    thai_months_short = [
        "ม.ค.", "ก.พ.", "มี.ค.", "เม.ย.",
        "พ.ค.", "มิ.ย.", "ก.ค.", "ส.ค.",
        "ก.ย.", "ต.ค.", "พ.ย.", "ธ.ค."
    ]
    
    day = date_obj.day
    month = thai_months_short[date_obj.month - 1]
    year = str(date_obj.year + 543)[-2:]  # เอา 2 หลักท้าย
    
    return f"{day} {month} {year}"


def get_bank_accounts_count(db: Session, case_id: int) -> str:
    """
    คำนวณจำนวนบัญชีธนาคารและจำนวนที่ตอบกลับแล้ว
    
    Args:
        db: Database session
        case_id: ID ของคดี
    
    Returns:
        str: รูปแบบ "ทั้งหมด/ตอบกลับแล้ว" เช่น "10/5"
    """
    total = db.query(BankAccount).filter(
        BankAccount.criminal_case_id == case_id
    ).count()
    
    replied = db.query(BankAccount).filter(
        BankAccount.criminal_case_id == case_id,
        BankAccount.reply_status == True
    ).count()
    
    return f"{total}/{replied}"


def get_suspects_count(db: Session, case_id: int) -> str:
    """
    คำนวณจำนวนผู้ต้องหาและจำนวนที่มาตามนัดแล้ว
    
    Args:
        db: Database session
        case_id: ID ของคดี
    
    Returns:
        str: รูปแบบ "ทั้งหมด/มาตามนัดแล้ว" เช่น "8/3"
    """
    total = db.query(Suspect).filter(
        Suspect.criminal_case_id == case_id
    ).count()
    
    replied = db.query(Suspect).filter(
        Suspect.criminal_case_id == case_id,
        Suspect.reply_status == True
    ).count()
    
    return f"{total}/{replied}"


def calculate_age_in_months(complaint_date: Optional[date]) -> Optional[int]:
    """
    คำนวณอายุคดีเป็นเดือน
    
    Args:
        complaint_date: วันที่รับคำกล่าวหา
    
    Returns:
        int: อายุคดีเป็นเดือน
        None: ถ้าไม่มีวันที่
    """
    if not complaint_date:
        return None
    
    from datetime import datetime
    today = datetime.now().date()
    
    # คำนวณความแตกต่างเป็นเดือน
    months = (today.year - complaint_date.year) * 12 + (today.month - complaint_date.month)
    
    # ถ้าวันของเดือนปัจจุบันน้อยกว่าวันที่รับคำกล่าวหา ให้ลบ 1 เดือน
    if today.day < complaint_date.day:
        months -= 1
    
    return max(0, months)  # ไม่ให้เป็นค่าติดลบ


def is_over_six_months(complaint_date: Optional[date]) -> Optional[str]:
    """
    ตรวจสอบว่าคดีมีอายุเกิน 6 เดือนหรือไม่
    
    Args:
        complaint_date: วันที่รับคำกล่าวหา
    
    Returns:
        str: "เกิน 6 เดือน" หรือ "ไม่เกิน 6 เดือน"
        None: ถ้าไม่มีวันที่
    """
    if not complaint_date:
        return None
    
    age_months = calculate_age_in_months(complaint_date)
    
    if age_months is None:
        return None
    
    return "เกิน 6 เดือน" if age_months > 6 else "ไม่เกิน 6 เดือน"

