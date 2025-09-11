#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Configuration settings for Criminal Case Management System
"""

import os


# Application settings
APP_NAME = "ระบบจัดการคดีอาญา"
APP_NAME_EN = "Criminal Case Management System"
VERSION = "2.3.2"

# File paths
BANK_DATA_FILE = "ข้อมูลเอกสารขอสำเนาบัญชีธนาคาร.xlsx"
SUMMONS_DATA_FILE = "ข้อมูลสำหรับออกหมายเรียกผู้ต้องหา.xlsx"
CRIMINAL_CASES_FILE = "คดีอาญาในความรับผิดชอบ.xlsx"
ARREST_DATA_FILE = "เอกสารหลังการจับกุม.xlsx"

# GUI settings
MAIN_WINDOW_TITLE = f"{APP_NAME} - {APP_NAME_EN}"
DEFAULT_WINDOW_BG = '#f0f0f0'
DETAIL_WINDOW_BG = '#f8f9fa'
DETAIL_WINDOW_WIDTH_PERCENT = 0.4
DETAIL_WINDOW_HEIGHT_PERCENT = 0.7

# Default document settings
DEFAULT_DOCUMENT_PREFIX = "ตช. 0039.52/"
DEFAULT_DELIVERY_TIME = "09.00 น."
DEFAULT_APPOINTMENT_DAYS = 7

# Thai months mapping
THAI_MONTHS = {
    1: "ม.ค.", 2: "ก.พ.", 3: "มี.ค.", 4: "เม.ย.", 5: "พ.ค.", 6: "มิ.ย.",
    7: "ก.ค.", 8: "ส.ค.", 9: "ก.ย.", 10: "ต.ค.", 11: "พ.ย.", 12: "ธ.ค."
}

THAI_MONTHS_FULL = [
    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
    "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม", 
    "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
]

THAI_MONTHS_REVERSE = {
    'ม.ค.': 1, 'ก.พ.': 2, 'มี.ค.': 3, 'เม.ย.': 4, 'พ.ค.': 5, 'มิ.ย.': 6,
    'ก.ค.': 7, 'ส.ค.': 8, 'ก.ย.': 9, 'ต.ค.': 10, 'พ.ย.': 11, 'ธ.ค.': 12
}

# Case types
CASE_TYPES = [
    "1. ฉ้อโกง", "2. ยักยอก", "3. ฟอกเงิน", "4. แข่งรถ", "5. ใช้เอกสารเท็จ",
    "6. ทำร้ายร่างกาย", "7. กรรมสิทธิ์", "8. ข่มขืน", "9. ชิงทรัพย์",
    "10. ลักทรัพย์", "11. โจรกรรม", "12. ทำลายทรัพย์สิน", "13. ปลิดชีวิต",
    "14. พรากผู้เยาว์", "15. หลอกลวง", "16. อื่นๆ"
]

# Colors
COLORS = {
    'primary': '#1f4e79',
    'secondary': '#c55a11', 
    'accent': '#2c5aa0',
    'success': 'green',
    'warning': '#ff9800',
    'error': 'red',
    'text_gray': '#666666',
    'bg_even': '#f8f9fa',
    'bg_odd': '#ffffff',
    'selected': '#e3f2fd',
    'selected_text': '#1565c0'
}

# Font settings
FONTS = {
    'default': ('Segoe UI', 10),
    'heading': ('Segoe UI', 18, 'bold'),
    'subheading': ('Segoe UI', 14, 'bold'),
    'label': ('Segoe UI', 10, 'bold'),
    'small': ('Segoe UI', 9),
    'tree_heading': ('Arial', 10, 'bold')
}

# Check GUI availability
try:
    import tkinter as tk
    import tkinter.ttk as ttk
    from tkinter import messagebox, filedialog
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("Warning: GUI ไม่พร้อมใช้งาน (tkinter ไม่พบ)")

# Check pandas availability 
try:
    import pandas as pd
    PANDAS_AVAILABLE = True
except ImportError:
    PANDAS_AVAILABLE = False
    print("Warning: pandas ไม่พร้อมใช้งาน")

# Check openpyxl availability
try:
    import openpyxl
    OPENPYXL_AVAILABLE = True
except ImportError:
    OPENPYXL_AVAILABLE = False
    print("Warning: openpyxl ไม่พร้อมใช้งาน")