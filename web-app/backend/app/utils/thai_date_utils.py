#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Thai date utilities for formatting dates in Buddhist Era (พ.ศ.)
"""

from datetime import datetime, date

def parse_thai_date_to_buddhist_era(thai_date_str):
    """
    Parse Thai date string and return in Buddhist Era format
    Input: "18 ก.ย. 02568 11:20"
    Output: "18 กันยายน 2568"
    """
    if not thai_date_str or thai_date_str.strip() == '':
        return None
    
    try:
        # Thai month abbreviations to full names
        thai_months = {
            'ม.ค.': 'มกราคม', 'ก.พ.': 'กุมภาพันธ์', 'มี.ค.': 'มีนาคม', 'เม.ย.': 'เมษายน',
            'พ.ค.': 'พฤษภาคม', 'มิ.ย.': 'มิถุนายน', 'ก.ค.': 'กรกฎาคม', 'ส.ค.': 'สิงหาคม',
            'ก.ย.': 'กันยายน', 'ต.ค.': 'ตุลาคม', 'พ.ย.': 'พฤศจิกายน', 'ธ.ค.': 'ธันวาคม'
        }
        
        # Parse Thai date format
        parts = thai_date_str.strip().split()
        if len(parts) >= 3:
            day = parts[0]
            thai_month_abbr = parts[1]
            year_with_time = parts[2]
            
            # Extract year (last 4 digits)
            year = year_with_time[-4:]
            
            # Get full month name
            full_month = thai_months.get(thai_month_abbr)
            if full_month:
                return f"{day} {full_month} {year}"
        
        return None
        
    except Exception as e:
        print(f"Error parsing Thai date: {e}")
        return None

def format_date_to_thai_buddhist_era(date_obj):
    """
    Format date object to Thai Buddhist Era format
    Input: datetime.date(2025, 9, 18)
    Output: "18 กันยายน 2568"
    """
    if not date_obj:
        return None
    
    try:
        # Thai month names
        thai_months = [
            'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
            'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
            'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
        ]
        
        # Convert to Buddhist Era
        buddhist_year = date_obj.year + 543
        thai_month = thai_months[date_obj.month - 1]
        
        return f"{date_obj.day} {thai_month} {buddhist_year}"
        
    except Exception as e:
        print(f"Error formatting date to Thai Buddhist Era: {e}")
        return None

def parse_thai_date_to_date_object(thai_date_str):
    """
    Parse Thai date string and return date object
    Input: "18 ก.ย. 02568 11:20"
    Output: datetime.date(2025, 9, 18)
    """
    if not thai_date_str or thai_date_str.strip() == '':
        return None
    
    try:
        # Thai month abbreviations
        thai_months = {
            'ม.ค.': '01', 'ก.พ.': '02', 'มี.ค.': '03', 'เม.ย.': '04',
            'พ.ค.': '05', 'มิ.ย.': '06', 'ก.ค.': '07', 'ส.ค.': '08',
            'ก.ย.': '09', 'ต.ค.': '10', 'พ.ย.': '11', 'ธ.ค.': '12'
        }
        
        # Parse Thai date format
        parts = thai_date_str.strip().split()
        if len(parts) >= 3:
            day = parts[0]
            thai_month_abbr = parts[1]
            year_with_time = parts[2]
            
            # Extract year (last 4 digits)
            year = year_with_time[-4:]
            
            month = thai_months.get(thai_month_abbr)
            if month:
                # Convert Buddhist year to Christian year
                christian_year = int(year) - 543
                return date(christian_year, int(month), int(day))
        
        return None
        
    except Exception as e:
        print(f"Error parsing Thai date to date object: {e}")
        return None
