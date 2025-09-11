#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summons data management for Criminal Case Management System
"""

from .base_data_manager import BaseDataManager
from ..config.settings import SUMMONS_DATA_FILE, CASE_TYPES, PANDAS_AVAILABLE
from ..utils.string_utils import safe_string_conversion, clean_case_type
from ..utils.date_utils import format_thai_date, get_default_appointment_date

if PANDAS_AVAILABLE:
    import pandas as pd


class SummonsDataManager(BaseDataManager):
    """Manager for summons data operations"""
    
    def __init__(self):
        super().__init__(SUMMONS_DATA_FILE)
    
    def get_case_types(self):
        """Get available case types"""
        return CASE_TYPES
    
    def find_related_summons_data(self, complainant_name):
        """Find summons data related to complainant"""
        if not complainant_name or self.data is None:
            return []
        
        try:
            complainant_clean = safe_string_conversion(complainant_name).strip()
            if not complainant_clean:
                return []
            
            # Search in complainant column  
            matches = self.data[
                self.data['ชื่อผู้ร้องทุกข์'].str.contains(complainant_clean, na=False)
            ]
            
            result = []
            for _, row in matches.iterrows():
                summons_info = row.to_dict()
                
                # Add status text based on reply status
                if row.get('ตอบแล้ว', '') == 'TRUE' or '✓' in str(row.get('ตอบแล้ว', '')):
                    summons_info['status_text'] = '✓ ตอบแล้ว'
                else:
                    summons_info['status_text'] = '⏳ ยังไม่ตอบ'
                
                result.append(summons_info)
            
            return result
            
        except Exception as e:
            print(f"Error finding related summons data: {e}")
            return []
    
    def create_empty_summons_data(self):
        """Create empty summons data structure"""
        default_appointment = get_default_appointment_date()
        default_appointment_thai = format_thai_date(default_appointment)
        
        return {
            'เลขที่หนังสือ': '',
            'ลงวันที่': '',
            'เรื่อง': '',
            'ชื่อ ผตห.': '',
            'เลขประจำตัว ปชช. ผตห.': '',
            'ที่อยู่ ผตห.': '',
            'สภ.พื้นที่รับผิดชอบ': '',
            'จังหวัด': '',
            'ประเภทคดี': '',
            'ชื่อผู้ร้องทุกข์': '',
            'วันที่กำหนดพบ': default_appointment_thai,
            'เวลากำหนดพบ': '09.00 น.',
            'สถานที่พบ': 'กองบังคับการปราบปราม',
            'ตอบแล้ว': ''
        }
    
    def save_summons_data(self, summons_data):
        """Save summons data with case type cleaning"""
        try:
            # Clean case type (remove numbers)
            if 'ประเภทคดี' in summons_data:
                summons_data['ประเภทคดี'] = clean_case_type(summons_data['ประเภทคดี'])
            
            # Convert to DataFrame
            df = pd.DataFrame([summons_data])
            
            # Save data
            return self.save_data(df, append=True)
            
        except Exception as e:
            print(f"Error saving summons data: {e}")
            return False