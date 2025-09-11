#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Criminal cases data management for Criminal Case Management System
"""

from .base_data_manager import BaseDataManager
from .bank_data_manager import BankDataManager
from .summons_data_manager import SummonsDataManager
from ..config.settings import CRIMINAL_CASES_FILE, PANDAS_AVAILABLE
from ..utils.date_utils import is_case_over_6_months
from ..utils.string_utils import safe_string_conversion

if PANDAS_AVAILABLE:
    import pandas as pd


class CriminalDataManager(BaseDataManager):
    """Manager for criminal cases data operations"""
    
    def __init__(self):
        super().__init__(CRIMINAL_CASES_FILE)
        self.bank_manager = BankDataManager()
        self.summons_manager = SummonsDataManager()
    
    def load_with_related_data(self):
        """Load criminal data along with related bank and summons data"""
        if not self.load_data():
            return False
        
        # Load related data
        self.bank_manager.load_data()
        self.summons_manager.load_data()
        
        return True
    
    def get_bank_accounts_count(self, complainant_name):
        """นับจำนวนบัญชีธนาคารที่เกี่ยวข้องและจำนวนที่ตอบกลับแล้ว"""
        if not complainant_name or str(complainant_name).strip() == '':
            return "0/0"
        
        try:
            bank_data = self.bank_manager.find_related_bank_data(complainant_name)
            if not bank_data:
                return "0/0"
            
            total_accounts = len(bank_data)
            replied_accounts = 0
            
            for bank in bank_data:
                status_text = bank.get('status_text', '')
                if '✓' in status_text or 'ตอบแล้ว' in status_text:
                    replied_accounts += 1
            
            return f"{total_accounts}/{replied_accounts}"
            
        except Exception as e:
            print(f"Error calculating bank accounts count: {e}")
            return "0/0"
    
    def get_suspects_count(self, complainant_name):
        """นับจำนวนผู้ต้องหาที่เกี่ยวข้องและจำนวนที่ตอบกลับแล้ว"""
        if not complainant_name or str(complainant_name).strip() == '':
            return "0/0"
        
        try:
            summons_data = self.summons_manager.find_related_summons_data(complainant_name)
            if not summons_data:
                return "0/0"
            
            total_suspects = len(summons_data)
            replied_suspects = 0
            
            for summons in summons_data:
                status_text = summons.get('status_text', '')
                if '✓' in status_text or 'ตอบแล้ว' in status_text:
                    replied_suspects += 1
            
            return f"{total_suspects}/{replied_suspects}"
            
        except Exception as e:
            print(f"Error calculating suspects count: {e}")
            return "0/0"
    
    def get_case_statistics(self):
        """Get case statistics including 6-month old cases"""
        if self.data is None:
            return "ไม่มีข้อมูล"
        
        try:
            total_cases = len(self.data)
            
            # Count cases with status "ระหว่างสอบสวน"
            investigating_cases = self.data[
                self.data['สถานะคดี'] == 'ระหว่างสอบสวน'
            ]
            investigating_count = len(investigating_cases)
            
            # Count cases over 6 months (only investigating cases)
            over_6_months_count = 0
            for _, case in investigating_cases.iterrows():
                complaint_date = case.get('วันที่/เวลา รับคำร้องทุกข์', '')
                if is_case_over_6_months(complaint_date):
                    over_6_months_count += 1
            
            # Count completed cases
            completed_count = total_cases - investigating_count
            
            return f"จำนวนคดีทั้งหมด {total_cases} | กำลังดำเนินการ {investigating_count} | เกิน 6 เดือน {over_6_months_count} | จำหน่ายแล้ว {completed_count}"
            
        except Exception as e:
            print(f"Error calculating statistics: {e}")
            return "เกิดข้อผิดพลาดในการคำนวณสถิติ"
    
    def is_case_older_than_6_months(self, date_string):
        """ตรวจสอบว่าคดีอายุเกิน 6 เดือนหรือไม่"""
        return is_case_over_6_months(date_string)
    
    def has_all_banks_replied(self, complainant_name):
        """Check if all bank accounts have replied"""
        bank_count_str = self.get_bank_accounts_count(complainant_name)
        if '/' not in bank_count_str:
            return False
        
        try:
            total, replied = bank_count_str.split('/')
            return int(total) > 0 and int(total) == int(replied)
        except:
            return False
    
    def get_case_tags_and_colors(self, case_row):
        """Get tags and colors for case row display"""
        tags = ['evenrow']
        
        # Check if case is over 6 months and investigating
        status = safe_string_conversion(case_row.get('สถานะคดี', ''))
        complaint_date = case_row.get('วันที่/เวลา รับคำร้องทุกข์', '')
        
        if (status == 'ระหว่างสอบสวน' and 
            self.is_case_older_than_6_months(complaint_date)):
            tags.append('over_6_months')
        
        # Check if all banks replied and status is investigating
        complainant_name = case_row.get('ชื่อผู้ร้องทุกข์', '')
        if (status == 'ระหว่างสอบสวน' and 
            self.has_all_banks_replied(complainant_name)):
            tags.append('all_banks_replied')
        
        return tags