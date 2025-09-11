#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Arrest data management for Criminal Case Management System
"""

from .base_data_manager import BaseDataManager
from ..config.settings import ARREST_DATA_FILE, PANDAS_AVAILABLE

if PANDAS_AVAILABLE:
    import pandas as pd


class ArrestDataManager(BaseDataManager):
    """Manager for arrest data operations"""
    
    def __init__(self):
        super().__init__(ARREST_DATA_FILE)
        self.arrest_headers = [
            "คดีอาญาที่", "ผู้กล่าวหา", "ชื่อผู้ต้องหา", "อายุ", "สัญชาติ", "ที่อยุ่", "เลข ปชช", "อาชีพ",
            "ศาล", "เลขหมาย", "ลงหมาย", "วันยื่นคำร้อง", "เดือนยื่น", "ปียื่น", "วันที่จับ ", "เวลาจับ",
            "สถานที่จับ", "ผู้นำจับ", "พยาน1", "พยาน2", "หมายเหตุ", "ข้อหา", "ที่เกิดเหตุในคดี",
            "ความเสียหาย", "ข้อเท็จจริง", "ผลการดำเนินคดี", "วันที่ส่งผู้ต้องหา", "เวลาส่งผู้ต้องหา",
            "หน่วยงานที่ส่ง", "ผู้รับส่ง", "วันที่ออกหมายจับ", "คำสั่งศาล", "เลขที่คำสั่ง", "วันที่คำสั่ง",
            "หมายเหตุศาล", "ข้อหาที่ตั้ง", "ผลคำพิพากษา", "วันที่พิพากษา", "หมายเหตุการพิพากษา", 
            "สถานะคดี", "ผู้จัดทำเอกสาร", "วันที่จัดทำเอกสาร", "หมายเหตุเพิ่มเติม"
        ]
    
    def get_arrest_headers(self):
        """Get arrest data column headers"""
        return self.arrest_headers
    
    def create_empty_arrest_data(self):
        """Create empty arrest data structure"""
        return {header: '' for header in self.arrest_headers}
    
    def get_arrest_field_groups(self):
        """Get organized field groups for arrest form"""
        return [
            ("⚖️ ข้อมูลคดีและผู้กล่าวหา", [
                ("คดีอาญาที่", "case_criminal_no", "entry"),
                ("ผู้กล่าวหา", "accuser", "entry"),
                ("ที่เกิดเหตุในคดี", "crime_scene", "text"),
                ("ความเสียหาย", "damage_amount", "entry")
            ]),
            ("👤 ข้อมูลผู้ต้องหา", [
                ("ชื่อผู้ต้องหา", "suspect_name", "entry"),
                ("อายุ", "age", "entry"),
                ("สัญชาติ", "nationality", "entry"),
                ("ที่อยู่", "address", "text"),
                ("เลขบัตรประชาชน", "id_card", "entry"),
                ("อาชีพ", "occupation", "entry")
            ]),
            ("📋 ข้อมูลหมายจับ", [
                ("ศาล", "court", "entry"),
                ("เลขหมายจับ", "warrant_no", "entry"),
                ("วันที่ออกหมาย", "warrant_date", "entry"),
                ("ลงหมาย", "warrant_issued", "entry")
            ]),
            ("📝 ข้อมูลคำร้อง", [
                ("วันยื่นคำร้อง", "petition_day", "entry"),
                ("เดือนยื่น", "petition_month", "entry"),
                ("ปียื่น", "petition_year", "entry")
            ]),
            ("🚔 ข้อมูลการจับกุม", [
                ("วันที่จับ", "arrest_date", "entry"),
                ("เวลาจับ", "arrest_time", "entry"),
                ("สถานที่จับ", "arrest_location", "text"),
                ("ผู้นำจับ", "arresting_officer", "entry"),
                ("พยาน 1", "witness_1", "entry"),
                ("พยาน 2", "witness_2", "entry")
            ]),
            ("⚖️ ข้อหาและข้อเท็จจริง", [
                ("ข้อหา", "charges", "text"),
                ("ข้อเท็จจริง", "facts", "text")
            ]),
            ("📤 การส่งตัวผู้ต้องหา", [
                ("วันที่ส่งผู้ต้องหา", "transfer_date", "entry"),
                ("เวลาส่งผู้ต้องหา", "transfer_time", "entry"),
                ("หน่วยงานที่ส่ง", "transfer_agency", "entry"),
                ("ผู้รับส่ง", "receiver", "entry")
            ]),
            ("⚖️ คำสั่งศาลและผลคดี", [
                ("คำสั่งศาล", "court_order", "text"),
                ("เลขที่คำสั่ง", "order_no", "entry"),
                ("วันที่คำสั่ง", "order_date", "entry"),
                ("ผลการดำเนินคดี", "case_result", "text"),
                ("ผลคำพิพากษา", "judgment", "text"),
                ("วันที่พิพากษา", "judgment_date", "entry")
            ]),
            ("📝 หมายเหตุและข้อมูลเพิ่มเติม", [
                ("หมายเหตุ", "notes", "text"),
                ("หมายเหตุศาล", "court_notes", "text"),
                ("หมายเหตุการพิพากษา", "judgment_notes", "text"),
                ("สถานะคดี", "case_status", "entry"),
                ("ผู้จัดทำเอกสาร", "document_creator", "entry"),
                ("วันที่จัดทำเอกสาร", "document_date", "entry"),
                ("หมายเหตุเพิ่มเติม", "additional_notes", "text")
            ])
        ]
    
    def get_key_mapping(self):
        """Get mapping between form keys and Excel columns"""
        return {
            'case_criminal_no': 'คดีอาญาที่',
            'accuser': 'ผู้กล่าวหา',
            'crime_scene': 'ที่เกิดเหตุในคดี',
            'damage_amount': 'ความเสียหาย',
            'suspect_name': 'ชื่อผู้ต้องหา',
            'age': 'อายุ',
            'nationality': 'สัญชาติ',
            'address': 'ที่อยุ่',
            'id_card': 'เลข ปชช',
            'occupation': 'อาชีพ',
            'court': 'ศาล',
            'warrant_no': 'เลขหมาย',
            'warrant_date': 'วันที่ออกหมายจับ',
            'warrant_issued': 'ลงหมาย',
            'petition_day': 'วันยื่นคำร้อง',
            'petition_month': 'เดือนยื่น',
            'petition_year': 'ปียื่น',
            'arrest_date': 'วันที่จับ ',
            'arrest_time': 'เวลาจับ',
            'arrest_location': 'สถานที่จับ',
            'arresting_officer': 'ผู้นำจับ',
            'witness_1': 'พยาน1',
            'witness_2': 'พยาน2',
            'charges': 'ข้อหา',
            'facts': 'ข้อเท็จจริง',
            'transfer_date': 'วันที่ส่งผู้ต้องหา',
            'transfer_time': 'เวลาส่งผู้ต้องหา',
            'transfer_agency': 'หน่วยงานที่ส่ง',
            'receiver': 'ผู้รับส่ง',
            'court_order': 'คำสั่งศาล',
            'order_no': 'เลขที่คำสั่ง',
            'order_date': 'วันที่คำสั่ง',
            'case_result': 'ผลการดำเนินคดี',
            'judgment': 'ผลคำพิพากษา',
            'judgment_date': 'วันที่พิพากษา',
            'notes': 'หมายเหตุ',
            'court_notes': 'หมายเหตุศาล',
            'judgment_notes': 'หมายเหตุการพิพากษา',
            'case_status': 'สถานะคดี',
            'document_creator': 'ผู้จัดทำเอกสาร',
            'document_date': 'วันที่จัดทำเอกสาร',
            'additional_notes': 'หมายเหตุเพิ่มเติม'
        }