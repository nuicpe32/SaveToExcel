#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Case styling utilities for criminal cases
"""

from datetime import datetime, timedelta
import re

def is_case_over_6_months(complaint_date_str):
    """ตรวจสอบว่าคดีเก่ากว่า 6 เดือนหรือไม่"""
    if not complaint_date_str or str(complaint_date_str).strip() == '' or str(complaint_date_str).strip() == 'nan':
        return False
    
    try:
        date_str = str(complaint_date_str).strip()
        
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
        print(f"Error parsing date {complaint_date_str}: {e}")
        return False
    
    return False

def has_all_banks_replied(bank_accounts_count_str):
    """Check if all bank accounts have replied"""
    if not bank_accounts_count_str or '/' not in bank_accounts_count_str:
        return False
    
    try:
        total, replied = bank_accounts_count_str.split('/')
        return int(total) > 0 and int(total) == int(replied)
    except:
        return False

def get_case_row_class(status, complaint_date_str, bank_accounts_count_str):
    """Get CSS class for case row based on Windows app logic"""
    classes = []
    
    # Check if case is over 6 months and investigating
    if (status == 'ระหว่างสอบสวน' and 
        is_case_over_6_months(complaint_date_str)):
        classes.append('over-six-months')
    
    # Check if all banks replied and status is investigating
    if (status == 'ระหว่างสอบสวน' and 
        has_all_banks_replied(bank_accounts_count_str)):
        classes.append('all-banks-replied')
    
    return ' '.join(classes) if classes else ''

def get_case_row_style(status, complaint_date_str, bank_accounts_count_str):
    """Get inline style for case row based on Windows app logic"""
    is_over_6_months = (status == 'ระหว่างสอบสวน' and 
                       is_case_over_6_months(complaint_date_str))
    all_banks_replied = (status == 'ระหว่างสอบสวน' and 
                        has_all_banks_replied(bank_accounts_count_str))
    
    if is_over_6_months and all_banks_replied:
        # Light blue background
        return {'backgroundColor': '#e6f3ff'}
    elif is_over_6_months:
        # Light orange background
        return {'backgroundColor': '#fff2e6'}
    elif all_banks_replied:
        # Light green background
        return {'backgroundColor': '#f6ffed'}
    else:
        # Default background
        return {}
