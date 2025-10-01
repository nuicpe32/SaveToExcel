#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Date utility functions for Criminal Case Management System
"""

from datetime import datetime, date
from typing import Optional, Tuple

def calculate_case_age(complaint_date: Optional[date]) -> Tuple[int, int]:
    """
    Calculate case age in months and days
    Returns (months, days)
    """
    if not complaint_date:
        return 0, 0
    
    today = date.today()
    
    # Calculate total days difference
    total_days = (today - complaint_date).days
    
    # Calculate months and remaining days
    months = total_days // 30  # Approximate months
    days = total_days % 30     # Remaining days
    
    return months, days

def format_case_age(complaint_date: Optional[date]) -> str:
    """
    Format case age as "X เดือน Y วัน"
    """
    months, days = calculate_case_age(complaint_date)
    
    if months == 0 and days == 0:
        return "0 วัน"
    elif months == 0:
        return f"{days} วัน"
    elif days == 0:
        return f"{months} เดือน"
    else:
        return f"{months} เดือน {days} วัน"

def is_case_over_6_months(complaint_date: Optional[date]) -> bool:
    """
    Check if case is over 6 months old
    """
    months, _ = calculate_case_age(complaint_date)
    return months >= 6

def calculate_days_since_sent(document_date: Optional[date]) -> int:
    """
    Calculate days since document was sent
    """
    if not document_date:
        return 0
    
    today = date.today()
    return (today - document_date).days

def format_days_since_sent(document_date: Optional[date]) -> str:
    """
    Format days since sent as "X วัน" or "X เดือน Y วัน"
    """
    days = calculate_days_since_sent(document_date)
    
    if days == 0:
        return "0 วัน"
    elif days < 30:
        return f"{days} วัน"
    else:
        months = days // 30
        remaining_days = days % 30
        if remaining_days == 0:
            return f"{months} เดือน"
        else:
            return f"{months} เดือน {remaining_days} วัน"
