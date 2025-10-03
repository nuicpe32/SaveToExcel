#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
String utility functions for Criminal Case Management System
"""

import re


def safe_string_conversion(value):
    """แปลงค่าเป็น string อย่างปลอดภัย"""
    if value is None or str(value).strip().lower() in ['nan', 'none', '']:
        return ''
    return str(value).strip()


def clean_name_for_matching(name):
    """ทำความสะอาดชื่อสำหรับการเปรียบเทียบ - ลบคำนำหน้าและช่องว่าง"""
    if not name:
        return ''
    
    name_clean = safe_string_conversion(name)
    
    # ลบหมายเลขและเครื่องหมาย เช่น "1) " ก่อน
    name_clean = re.sub(r'^\d+\)\s*', '', name_clean)
    
    # ลบคำนำหน้า
    prefixes = ['นาย', 'นาง', 'นางสาว', 'น.ส.', 'เด็กชาย', 'เด็กหญิง', 'ด.ช.', 'ด.ญ.']
    for prefix in prefixes:
        if name_clean.startswith(prefix):
            name_clean = name_clean[len(prefix):].strip()
    
    # ลบช่องว่างส่วนเกิน
    name_clean = ' '.join(name_clean.split())
    
    return name_clean


def names_match(name1, name2):
    """เปรียบเทียบชื่อสองชื่อว่าตรงกันหรือไม่ (ไม่สนใจคำนำหน้า)"""
    if not name1 or not name2:
        return False
    
    clean1 = clean_name_for_matching(name1)
    clean2 = clean_name_for_matching(name2)
    
    # เปรียบเทียบแบบ case-insensitive
    return clean1.lower() == clean2.lower()


def name_contains(target_name, search_name):
    """ตรวจสอบว่า target_name มี search_name อยู่หรือไม่ (ไม่สนใจคำนำหน้า)"""
    if not target_name or not search_name:
        return False
    
    clean_target = clean_name_for_matching(target_name)
    clean_search = clean_name_for_matching(search_name)
    
    # เปรียบเทียบแบบ case-insensitive และ partial match
    return clean_search.lower() in clean_target.lower()
