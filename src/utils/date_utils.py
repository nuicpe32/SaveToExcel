#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date utility functions for Criminal Case Management System
"""

from datetime import datetime, timedelta
import re


def format_thai_date(date_obj):
    """แปลงวันที่เป็นรูปแบบไทย เช่น 23 พ.ค. 68"""
    thai_months = {
        1: "ม.ค.", 2: "ก.พ.", 3: "มี.ค.", 4: "เม.ย.", 5: "พ.ค.", 6: "มิ.ย.",
        7: "ก.ค.", 8: "ส.ค.", 9: "ก.ย.", 10: "ต.ค.", 11: "พ.ย.", 12: "ธ.ค."
    }
    
    day = date_obj.day
    month = thai_months[date_obj.month]
    year = (date_obj.year + 543) % 100  # แปลงเป็น พ.ศ. และเอาแค่ 2 หลัก
    
    return f"{day} {month} {year:02d}"


def get_default_appointment_date():
    """ได้วันที่กำหนดพบเริ่มต้น (วันปัจจุบัน + 7 วัน)"""
    return datetime.now() + timedelta(days=7)


def is_case_over_6_months(date_str):
    """ตรวจสอบว่าคดีเก่ากว่า 6 เดือนหรือไม่"""
    if not date_str or str(date_str).strip() == '' or str(date_str).strip() == 'nan':
        return False
    
    try:
        date_str = str(date_str).strip()
        
        # รูปแบบวันที่ไทย: "01 ก.ย. 02568 11:17"
        thai_months = {
            'ม.ค.': 1, 'ก.พ.': 2, 'มี.ค.': 3, 'เม.ย.': 4, 'พ.ค.': 5, 'มิ.ย.': 6,
            'ก.ค.': 7, 'ส.ค.': 8, 'ก.ย.': 9, 'ต.ค.': 10, 'พ.ย.': 11, 'ธ.ค.': 12
        }
        
        # แยกส่วนประกอบของวันที่
        pattern = r'(\d{1,2})\s+([^\s]+)\s+(\d{4,5})'
        match = re.search(pattern, date_str)
        
        if match:
            day = int(match.group(1))
            month_thai = match.group(2)
            year = int(match.group(3))
            
            # แปลงเดือนไทยเป็นหมายเลข
            month = thai_months.get(month_thai, None)
            if not month:
                return False
            
            # แปลงปี พ.ศ. เป็น ค.ศ.
            if year > 2500:
                year -= 543
            
            # สร้างวันที่
            case_date = datetime(year, month, day)
            
            # คำนวณความต่างเป็นเดือน
            current_date = datetime.now()
            months_diff = (current_date.year - case_date.year) * 12 + (current_date.month - case_date.month)
            
            return months_diff >= 6
            
    except Exception as e:
        print(f"Error parsing date {date_str}: {e}")
        return False
    
    return False


def calculate_days_since_document(doc_date_str):
    """คำนวณจำนวนวันตั้งแต่วันที่ลงหนังสือจนถึงปัจจุบัน"""
    if not doc_date_str or str(doc_date_str).strip() == '' or str(doc_date_str).strip() == 'nan':
        return 0
    
    try:
        date_str = str(doc_date_str).strip()
        
        # รูปแบบวันที่ไทย
        thai_months = {
            'ม.ค.': 1, 'ก.พ.': 2, 'มี.ค.': 3, 'เม.ย.': 4, 'พ.ค.': 5, 'มิ.ย.': 6,
            'ก.ค.': 7, 'ส.ค.': 8, 'ก.ย.': 9, 'ต.ค.': 10, 'พ.ย.': 11, 'ธ.ค.': 12
        }
        
        # แยกส่วนประกอบของวันที่
        pattern = r'(\d{1,2})\s+([^\s]+)\s+(\d{4,5})'
        match = re.search(pattern, date_str)
        
        if match:
            day = int(match.group(1))
            month_thai = match.group(2)
            year = int(match.group(3))
            
            # แปลงเดือนไทยเป็นหมายเลข
            month = thai_months.get(month_thai, None)
            if not month:
                return 0
            
            # แปลงปี พ.ศ. เป็น ค.ศ.
            if year > 2500:
                year -= 543
            
            # สร้างวันที่
            doc_date = datetime(year, month, day)
            
            # คำนวณความต่างเป็นวัน
            current_date = datetime.now()
            days_diff = (current_date - doc_date).days
            
            return days_diff
            
    except Exception as e:
        print(f"Error calculating days since document {doc_date_str}: {e}")
        return 0
    
    return 0