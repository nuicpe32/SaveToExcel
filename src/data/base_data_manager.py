#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Base data manager for handling Excel file operations
"""

import os
from ..config.settings import PANDAS_AVAILABLE, OPENPYXL_AVAILABLE

if PANDAS_AVAILABLE:
    import pandas as pd
if OPENPYXL_AVAILABLE:
    import openpyxl


class BaseDataManager:
    """Base class for data management operations"""
    
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = None
        self.headers = []
    
    def file_exists(self):
        """Check if the Excel file exists"""
        return os.path.exists(self.file_path)
    
    def load_data(self):
        """Load data from Excel file"""
        if not PANDAS_AVAILABLE:
            print(f"Error: pandas ไม่พร้อมใช้งาน - ไม่สามารถโหลดไฟล์ {self.file_path}")
            return None
        
        try:
            if self.file_exists():
                self.data = pd.read_excel(self.file_path)
                self.headers = list(self.data.columns)
                print(f"โหลดข้อมูล {self.file_path} สำเร็จ: {len(self.data)} แถว")
                return self.data
            else:
                print(f"ไม่พบไฟล์ {self.file_path}")
                return None
        except Exception as e:
            print(f"Error loading {self.file_path}: {e}")
            return None
    
    def save_data(self, data, append=False):
        """Save data to Excel file"""
        if not PANDAS_AVAILABLE or not OPENPYXL_AVAILABLE:
            print("Error: pandas หรือ openpyxl ไม่พร้อมใช้งาน")
            return False
        
        try:
            if append and self.file_exists():
                # Append to existing file
                existing_data = pd.read_excel(self.file_path)
                combined_data = pd.concat([existing_data, data], ignore_index=True)
                combined_data.to_excel(self.file_path, index=False)
            else:
                # Create new file or overwrite
                data.to_excel(self.file_path, index=False)
            
            print(f"บันทึกไฟล์ {self.file_path} สำเร็จ")
            return True
        except Exception as e:
            print(f"Error saving {self.file_path}: {e}")
            return False
    
    def get_data_count(self):
        """Get number of rows in data"""
        if self.data is not None:
            return len(self.data)
        return 0
    
    def get_headers(self):
        """Get column headers"""
        return self.headers
    
    def search_data(self, search_column, search_value, exact_match=False):
        """Search data by column value"""
        if self.data is None:
            return []
        
        try:
            if exact_match:
                matches = self.data[self.data[search_column] == search_value]
            else:
                matches = self.data[self.data[search_column].str.contains(str(search_value), na=False)]
            
            return matches.to_dict('records') if not matches.empty else []
        except Exception as e:
            print(f"Error searching data: {e}")
            return []