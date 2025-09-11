#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
String utility functions for Criminal Case Management System
"""


def clean_document_number(doc_number):
    """ทำความสะอาดเลขที่หนังสือ - ลบ .0 ออกจากท้าย"""
    if not doc_number:
        return doc_number
    
    doc_str = str(doc_number).strip()
    if doc_str.endswith('.0'):
        doc_str = doc_str[:-2]  # ลบ .0 ออก
    
    return doc_str


def clean_case_type(case_type_str):
    """ลบหมายเลขออกจากประเภทคดี เช่น "1. ฉ้อโกง" -> "ฉ้อโกง" """
    if not case_type_str:
        return case_type_str
    
    case_type_clean = str(case_type_str).strip()
    # ลบหมายเลขและจุดหน้าข้อความ
    if '. ' in case_type_clean and case_type_clean.split('. ')[0].isdigit():
        case_type_clean = '. '.join(case_type_clean.split('. ')[1:])
    
    return case_type_clean


def safe_string_conversion(value):
    """แปลงค่าเป็น string อย่างปลอดภัย"""
    if value is None or str(value).strip().lower() in ['nan', 'none', '']:
        return ''
    return str(value).strip()