#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Bank data management for Criminal Case Management System
"""

from .base_data_manager import BaseDataManager
from ..config.settings import BANK_DATA_FILE, PANDAS_AVAILABLE
from ..utils.string_utils import safe_string_conversion

if PANDAS_AVAILABLE:
    import pandas as pd


class BankDataManager(BaseDataManager):
    """Manager for bank account data operations"""
    
    def __init__(self):
        super().__init__(BANK_DATA_FILE)
        self.bank_branches = self._load_bank_branches()
    
    def _load_bank_branches(self):
        """Load bank branches data"""
        return [
            "ธนาคารกรุงเทพ สาขาหาดใหญ่",
            "ธนาคารกสิกรไทย สาขาหาดใหญ่",
            "ธนาคารไทยพาณิชย์ สาขาหาดใหญ่",
            "ธนาคารกรุงไทย สาขาหาดใหญ่",
            "ธนาคารทหารไทยธนชาต สาขาหาดใหญ่",
            "ธนาคารกรุงศรีอยุธยา สาขาหาดใหญ่",
            "ธนาคารยูโอบี สาขาหาดใหญ่",
            "ธนาคารซีไอเอ็มบี สาขาหาดใหญ่",
            "ธนาคารแลนด์ แอนด์ เฮ้าส์ สาขาหาดใหญ่",
            "ธนาคารออมสิน สาขาหาดใหญ่",
            "ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร สาขาหาดใหญ่",
            "ธนาคารอิสลามแห่งประเทศไทย สาขาหาดใหญ่"
        ]
    
    def get_bank_branches(self):
        """Get list of bank branches"""
        return self.bank_branches
    
    def find_related_bank_data(self, complainant_name):
        """Find bank accounts related to complainant"""
        if not complainant_name or not self.data is not None:
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
                bank_info = row.to_dict()
                
                # Add status text based on reply status
                if row.get('ตอบแล้ว', '') == 'TRUE' or '✓' in str(row.get('ตอบแล้ว', '')):
                    bank_info['status_text'] = '✓ ตอบแล้ว'
                else:
                    bank_info['status_text'] = '⏳ ยังไม่ตอบ'
                
                result.append(bank_info)
            
            return result
            
        except Exception as e:
            print(f"Error finding related bank data: {e}")
            return []
    
    def get_case_id_from_bank_data(self, complainant_name):
        """Get CaseID from bank data"""
        if not complainant_name or self.data is None:
            return ""
        
        try:
            complainant_clean = safe_string_conversion(complainant_name).strip()
            if not complainant_clean:
                return ""
            
            # Search for matching complainant
            matches = self.data[
                self.data['ชื่อผู้ร้องทุกข์'].str.contains(complainant_clean, na=False)
            ]
            
            if not matches.empty:
                case_id = matches.iloc[0].get('เคสไอดี', '')
                return safe_string_conversion(case_id)
            
            return ""
            
        except Exception as e:
            print(f"Error getting CaseID: {e}")
            return ""
    
    def create_empty_bank_data(self):
        """Create empty bank data structure"""
        return {
            'ลำดับ': '',
            'ชื่อธนาคาร': '',
            'เลขบัญชี': '',
            'เจ้าของบัญชีม้า': '',
            'ชื่อผู้ร้องทุกข์': '',
            'เลขหนังสือ': '',
            'วัน': '',
            'เดือน': '',
            'ปี': '',
            'วันส่ง': '',
            'เดือนส่ง': '',
            'ปีส่ง': '',
            'เวลาส่ง': '',
            'ตอบแล้ว': '',
            'หมายเหตุ': ''
        }
    
    def get_next_order_number(self):
        """Get next order number for new entries"""
        if self.data is None or self.data.empty:
            return 1
        
        try:
            # Get max order number and add 1
            max_order = self.data['ลำดับ'].max()
            return int(max_order) + 1 if pd.notna(max_order) else 1
        except:
            return 1