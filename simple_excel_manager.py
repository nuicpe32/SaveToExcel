#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple Excel Data Manager - เวอร์ชันง่าย
โปรแกรม GUI สำหรับจัดการข้อมูล Excel
"""

import os
import sys
import csv
import json
import zipfile
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import calendar

# ฟังก์ชันสำหรับแปลงวันที่เป็นรูปแบบไทย
def format_thai_date(date_obj):
    """แปลงวันที่เป็นรูปแบบไทย เช่น 23 พ.ค. 68"""
    thai_months = {
        1: "ม.ค.", 2: "ก.พ.", 3: "มี.ค.", 4: "เม.ย.", 5: "พ.ค.", 6: "มิ.ย.",
        7: "ก.ค.", 8: "ส.ค.", 9: "ก.ย.", 10: "ต.ค.", 11: "พ.ย.", 12: "ธ.ค."
    }
    
    day = date_obj.day
    month = thai_months[date_obj.month]
    year = (date_obj.year + 543) % 100  # แปลงเป็น พ.ศ. และเอาแค่ 2 หลัก
    
    return f"{day} {month} {year:02d}"

def get_default_appointment_date():
    """ได้วันที่กำหนดพบเริ่มต้น (วันปัจจุบัน + 7 วัน)"""
    return datetime.now() + timedelta(days=7)


# ตรวจสอบและติดตั้ง dependencies
def check_and_install_deps():
    """ตรวจสอบและติดตั้ง dependencies"""
    missing_packages = []
    
    try:
        import pandas
    except ImportError:
        missing_packages.append("pandas")
    
    try:
        import openpyxl
    except ImportError:
        missing_packages.append("openpyxl")
    
    try:
        import tkinter
    except ImportError:
        missing_packages.append("python3-tk")
    
    try:
        import requests
    except ImportError:
        missing_packages.append("requests")
    
    if missing_packages:
        print("กำลังติดตั้งแพ็กเกจที่จำเป็น...")
        os.system("python3 install_dependencies.py")
        return False
    
    return True

# Import หลังจากตรวจสอบ dependencies
try:
    import tkinter as tk
    from tkinter import ttk, messagebox, filedialog
    import pandas as pd
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False
    print("ไม่สามารถใช้ GUI ได้ กรุณาติดตั้ง dependencies")

class SimpleExcelManager:
    def __init__(self):
        # ไฟล์ Excel สำหรับข้อมูลธนาคาร
        self.excel_file = os.path.join(os.getcwd(), "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx")
        self.data = None  # จะเป็น DataFrame หรือ dict ขึ้นอยู่กับว่ามี pandas หรือไม่
        self.data_rows = []  # สำหรับเก็บข้อมูลแบบ list
        self.data_headers = []  # สำหรับเก็บหัวข้อ
        
        # ไฟล์ Excel สำหรับข้อมูลหมายเรียกผู้ต้องหา
        self.summons_file = os.path.join(os.getcwd(), "ข้อมูลสำหรับออกหมายเรียกผู้ต้องหา.xlsx")
        self.summons_data = None
        self.summons_data_rows = []
        self.summons_data_headers = []
        
        self.use_pandas = False
        
        # โหลดข้อมูลธนาคาร
        self.bank_data = {}
        self.load_bank_data()
        
        # ตรวจสอบว่ามี pandas หรือไม่
        try:
            import pandas as pd
            self.use_pandas = True
            self.data = pd.DataFrame()
        except ImportError:
            self.use_pandas = False
            print("ทำงานโดยไม่ใช้ pandas")
        
        # โหลดข้อมูลไม่ว่า GUI จะพร้อมหรือไม่
        self.load_data()  # โหลดข้อมูลธนาคาร
        self.load_summons_data()  # โหลดข้อมูลหมายเรียก
        
        if GUI_AVAILABLE:
            self.create_gui()
        else:
            print("GUI ไม่พร้อมใช้งาน")
    
    def load_bank_data(self):
        """โหลดข้อมูลธนาคารจากไฟล์ JSON หรือสร้างใหม่"""
        try:
            if os.path.exists('bank_data.json'):
                with open('bank_data.json', 'r', encoding='utf-8') as f:
                    self.bank_data = json.load(f)
            else:
                # สร้างข้อมูลธนาคารจากไฟล์ Excel
                self.extract_bank_data()
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการโหลดข้อมูลธนาคาร: {e}")
            self.bank_data = {
                'bank_branches': [],
                'bank_names': [],
                'address_mapping': {}
            }
    
    def extract_bank_data(self):
        """สร้างข้อมูลธนาคารจากไฟล์ Excel"""
        try:
            headers, rows = self.read_excel_direct()
            if not headers or not rows:
                return
            
            # หาตำแหน่งคอลัมน์
            bank_branch_col = -1
            bank_name_col = -1
            address_col = -1
            
            for i, header in enumerate(headers):
                if 'ธนาคารสาขา' in header:
                    bank_branch_col = i
                elif 'ชื่อธนาคาร' in header:
                    bank_name_col = i
                elif 'ที่อยู่ธนาคาร' in header:
                    address_col = i
            
            bank_branches = set()
            bank_names = set()
            address_mapping = {}
            
            for row in rows:
                if len(row) > max(bank_branch_col, bank_name_col):
                    bank_branch = row[bank_branch_col] if bank_branch_col >= 0 else ""
                    bank_name = row[bank_name_col] if bank_name_col >= 0 else ""
                    
                    if bank_branch and bank_branch.strip():
                        bank_branches.add(bank_branch.strip())
                    if bank_name and bank_name.strip():
                        bank_names.add(bank_name.strip())
                    
                    # สร้าง mapping ของที่อยู่
                    if bank_branch and bank_name:
                        key = f"{bank_branch}|{bank_name}"
                        address_data = {}
                        
                        # เก็บข้อมูลที่อยู่ทั้งหมด
                        address_fields = ['ที่อยู่ธนาคาร', 'ซอย', 'หมู่', 'ตำบล/แขวง', 'อำเภอ/เขต', 'ถนน', 'จังหวัด', 'รหัสไปรษณี']
                        for field in address_fields:
                            col_idx = -1
                            for i, header in enumerate(headers):
                                if field in header:
                                    col_idx = i
                                    break
                            if col_idx >= 0 and len(row) > col_idx:
                                address_data[field] = row[col_idx] or ""
                        
                        address_mapping[key] = address_data
            
            self.bank_data = {
                'bank_branches': sorted(list(bank_branches)),
                'bank_names': sorted(list(bank_names)),
                'address_mapping': address_mapping
            }
            
            # บันทึกลงไฟล์
            with open('bank_data.json', 'w', encoding='utf-8') as f:
                json.dump(self.bank_data, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            print(f"Error extracting bank data: {e}")
            self.bank_data = {
                'bank_branches': [],
                'bank_names': [],
                'address_mapping': {}
            }
    
    def create_gui(self):
        """สร้าง GUI"""
        self.root = tk.Tk()
        self.root.title("Excel Data Manager - จัดการข้อมูล Excel")
        self.root.geometry("1200x800")
        self.root.configure(bg='#f0f0f0')
        
        # ธีมสีสวย
        style = ttk.Style()
        style.theme_use('clam')
        
        # สร้าง main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # หัวข้อ
        title_label = ttk.Label(main_frame, text="ระบบจัดการข้อมูล Excel", 
                               font=('Arial', 18, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # สร้าง notebook สำหรับแท็บ
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill='both', expand=True)
        
        # แท็บกรอกข้อมูล
        self.create_input_tab()
        
        # แท็บดูข้อมูล
        self.create_view_tab()
        
        # แท็บหมายเรียกผู้ต้องหา
        self.create_summons_input_tab()
        
        # แท็บดูข้อมูลหมายเรียก
        self.create_summons_view_tab()
    
    def create_input_tab(self):
        """สร้างแท็บกรอกข้อมูล"""
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="🏦 ข้อมูลบัญชีธนาคาร")
        
        # สร้าง scrollable frame
        canvas = tk.Canvas(input_frame)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # หัวข้อ
        title = ttk.Label(scrollable_frame, text="เพิ่มข้อมูลใหม่", 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=20)
        
        # ฟิลด์กรอกข้อมูล
        self.entries = {}
        fields = [
            ("ลำดับ", "order_no"),
            ("เลขหนังสือ", "document_no"),
            ("วัน", "day"),
            ("เดือน", "month"),
            ("ปี", "year"),
            ("ธนาคารสาขา", "bank_branch"),
            ("ผู้เสียหาย", "victim"),
            ("เคสไอดี", "case_id"),
            ("เจ้าของบัญชีม้า", "account_owner_horse"),
            ("ชื่อธนาคาร", "bank_name"),
            ("เลขบัญชี", "account_no"),
            ("ชื่อบัญชี", "account_name"),
            ("ช่วงเวลา", "time_period"),
            ("ที่อยู่ธนาคาร", "bank_address"),
            ("ซอย", "soi"),
            ("หมู่", "moo"),
            ("ตำบล/แขวง", "tambon_khwaeng"),
            ("อำเภอ/เขต", "amphoe_khet"),
            ("ถนน", "road"),
            ("จังหวัด", "province"),
            ("รหัสไปรษณี", "postal_code"),
            ("วันนัดส่ง", "delivery_day"),
            ("เดือนส่ง", "delivery_month"),
            ("เวลาส่ง", "delivery_time")
        ]
        
        # จัดกลุ่มฟิลด์
        groups = [
            ("📋 ข้อมูลหนังสือ", [
                ("ลำดับ", "order_no", "auto"),
                ("เลขหนังสือ", "document_no", "entry"),
                ("วัน", "day", "auto"),
                ("เดือน", "month", "month_dropdown"),
                ("ปี", "year", "auto")
            ]),
            ("🏦 ข้อมูลธนาคาร", [
                ("ธนาคารสาขา", "bank_branch", "dropdown"),
                ("ชื่อธนาคาร", "bank_name", "dropdown"),
                ("เลขบัญชี", "account_no", "entry"),
                ("ชื่อบัญชี", "account_name", "entry"),
                ("เจ้าของบัญชีม้า", "account_owner_horse", "linked"),
                ("ช่วงเวลา", "time_period", "entry")
            ]),
            ("👤 ข้อมูลผู้เกี่ยวข้อง", [
                ("ผู้เสียหาย", "victim", "entry"),
                ("เคสไอดี", "case_id", "entry")
            ]),
            ("📍 ที่อยู่ธนาคาร", [
                ("ที่อยู่ธนาคาร", "bank_address", "auto"),
                ("ซอย", "soi", "auto"),
                ("หมู่", "moo", "auto"),
                ("ตำบล/แขวง", "tambon_khwaeng", "auto"),
                ("อำเภอ/เขต", "amphoe_khet", "auto"),
                ("ถนน", "road", "auto"),
                ("จังหวัด", "province", "auto"),
                ("รหัสไปรษณี", "postal_code", "auto")
            ]),
            ("📅 ข้อมูลการส่ง", [
                ("วันนัดส่ง", "delivery_day", "entry"),
                ("เดือนส่ง", "delivery_month", "month_dropdown"),
                ("เวลาส่ง", "delivery_time", "entry")
            ])
        ]
        
        for group_title, group_fields in groups:
            # หัวข้อกลุ่ม
            group_label = ttk.Label(scrollable_frame, text=group_title, 
                                   font=('Arial', 12, 'bold'))
            group_label.pack(pady=(20, 10))
            
            # สร้างเฟรมสำหรับกลุ่ม
            group_frame = ttk.LabelFrame(scrollable_frame, text="", padding=15)
            group_frame.pack(fill='x', padx=30, pady=(0, 10))
            
            for label_text, key, field_type in group_fields:
                field_frame = ttk.Frame(group_frame)
                field_frame.pack(fill='x', pady=3)
                
                label = ttk.Label(field_frame, text=label_text, width=18, font=('Arial', 10))
                label.pack(side='left', padx=(0, 10))
                
                # สร้าง widget ตามประเภท
                if field_type == "dropdown":
                    entry = ttk.Combobox(field_frame, width=47, font=('Arial', 10), state="readonly")
                    if key == "bank_branch":
                        entry['values'] = self.bank_data.get('bank_branches', [])
                        entry.bind('<<ComboboxSelected>>', self.on_bank_selection)
                    elif key == "bank_name":
                        entry['values'] = self.bank_data.get('bank_names', [])
                        entry.bind('<<ComboboxSelected>>', self.on_bank_selection)
                elif field_type == "month_dropdown":
                    entry = ttk.Combobox(field_frame, width=47, font=('Arial', 10), state="readonly")
                    thai_months = [
                        "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
                        "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
                        "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
                    ]
                    entry['values'] = thai_months
                elif field_type == "text":
                    entry = tk.Text(field_frame, height=3, width=50, font=('Arial', 10))
                elif field_type == "auto":
                    entry = ttk.Entry(field_frame, width=50, font=('Arial', 10))
                    if key in ['bank_address', 'soi', 'moo', 'tambon_khwaeng', 'amphoe_khet', 'road', 'province', 'postal_code']:
                        entry.config(state='readonly')
                elif field_type == "linked":
                    entry = ttk.Entry(field_frame, width=50, font=('Arial', 10))
                    # ربطกับ account_name
                    if key == "account_owner_horse":
                        entry.bind('<KeyRelease>', lambda e: self.sync_account_names())
                else:  # entry
                    entry = ttk.Entry(field_frame, width=50, font=('Arial', 10))
                    if key == "account_name":
                        entry.bind('<KeyRelease>', lambda e: self.sync_account_names())
                    elif key == "document_no":
                        # ใส่ค่าเริ่มต้นสำหรับเลขที่หนังสือ
                        entry.insert(0, "ตช. 0039.52/")
                    elif key == "delivery_day":
                        # ใส่วันนัดส่งเป็นวันปัจจุบัน + 7 วัน
                        delivery_date = datetime.now() + timedelta(days=7)
                        entry.insert(0, str(delivery_date.day))
                    elif key == "delivery_time":
                        # ใส่เวลาส่งเป็น 09.00 น.
                        entry.insert(0, "09.00 น.")
                
                entry.pack(side='left', fill='x', expand=True)
                self.entries[key] = entry
        
        # ตั้งค่าข้อมูลอัตโนมัติ
        self.set_automatic_values()
        
        # ปุ่มจัดการ
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=30)
        
        save_btn = ttk.Button(button_frame, text="💾 บันทึก", 
                             command=self.save_data)
        save_btn.pack(side='left', padx=10)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ ล้างข้อมูล", 
                              command=self.clear_entries)
        clear_btn.pack(side='left', padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def set_automatic_values(self):
        """ตั้งค่าข้อมูลอัตโนมัติ"""
        # ลำดับอัตโนมัติ
        next_order = self.get_next_order_number()
        if 'order_no' in self.entries:
            self.entries['order_no'].delete(0, tk.END)
            self.entries['order_no'].insert(0, str(next_order))
            self.entries['order_no'].config(state='readonly')
        
        # วันที่ปัจจุบัน (ตามรูปแบบไฟล์เดิม)
        now = datetime.now()
        thai_months = {
            1: "มกราคม", 2: "กุมภาพันธ์", 3: "มีนาคม", 4: "เมษายน",
            5: "พฤษภาคม", 6: "มิถุนายน", 7: "กรกฎาคม", 8: "สิงหาคม",
            9: "กันยายน", 10: "ตุลาคม", 11: "พฤศจิกายน", 12: "ธันวาคม"
        }
        
        current_day = str(now.day)
        current_month = thai_months[now.month]
        current_year = str(now.year + 543)  # พ.ศ. เช่น 2567
        
        # ตั้งค่าข้อมูลวันที่อัตโนมัติ
        
        if 'day' in self.entries:
            self.entries['day'].delete(0, tk.END)
            self.entries['day'].insert(0, current_day)
            self.entries['day'].config(state='readonly')
        
        if 'month' in self.entries:
            self.entries['month'].set(current_month)
        
        if 'year' in self.entries:
            self.entries['year'].delete(0, tk.END)
            self.entries['year'].insert(0, current_year)
            self.entries['year'].config(state='readonly')
        
        # ตั้งค่าเดือนส่งเป็นเดือนถัดไป
        next_month_index = now.month % 12 + 1
        next_month = thai_months[next_month_index]
        if 'delivery_month' in self.entries:
            self.entries['delivery_month'].set(next_month)
    
    def get_next_order_number(self):
        """หาลำดับถัดไปจากข้อมูลที่โหลดมา"""
        max_order = 0
        
        try:
            if self.use_pandas and self.data is not None and not self.data.empty:
                # ใช้ pandas
                for val in self.data.iloc[:, 0]:  # คอลัมน์แรก (ลำดับ)
                    try:
                        order_num = int(str(val).strip())
                        if order_num > max_order:
                            max_order = order_num
                    except:
                        pass
            elif self.data_rows:
                # ไม่ใช้ pandas
                for row in self.data_rows:
                    if row and len(row) > 0:
                        try:
                            order_num = int(str(row[0]).strip())
                            if order_num > max_order:
                                max_order = order_num
                        except:
                            pass
            else:
                # ถ้าไม่มีข้อมูล ลองอ่านจากไฟล์โดยตรง
                headers, rows = self.read_excel_direct()
                if rows:
                    for row in rows:
                        if row and len(row) > 0:
                            try:
                                order_num = int(str(row[0]).strip())
                                if order_num > max_order:
                                    max_order = order_num
                            except:
                                pass
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการหาลำดับถัดไป: {e}")
        
        next_order = max_order + 1
        # ค้นหาลำดับถัดไป
        return next_order
    
    def on_bank_selection(self, event=None):
        """จัดการเมื่อเลือกธนาคาร"""
        try:
            bank_branch = self.entries['bank_branch'].get()
            bank_name = self.entries['bank_name'].get()
            
            if bank_branch and bank_name:
                key = f"{bank_branch}|{bank_name}"
                address_data = self.bank_data.get('address_mapping', {}).get(key, {})
                
                # อัพเดทฟิลด์ที่อยู่
                address_fields = {
                    'bank_address': 'ที่อยู่ธนาคาร',
                    'soi': 'ซอย',
                    'moo': 'หมู่',
                    'tambon_khwaeng': 'ตำบล/แขวง',
                    'amphoe_khet': 'อำเภอ/เขต',
                    'road': 'ถนน',
                    'province': 'จังหวัด',
                    'postal_code': 'รหัสไปรษณี'
                }
                
                for field_key, address_key in address_fields.items():
                    if field_key in self.entries:
                        widget = self.entries[field_key]
                        widget.config(state='normal')
                        widget.delete(0, tk.END)
                        value = address_data.get(address_key, '')
                        widget.insert(0, value)
                        widget.config(state='readonly')
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเลือกธนาคาร: {e}")
    
    def sync_account_names(self):
        """ซิงค์ชื่อบัญชีกับเจ้าของบัญชีม้า"""
        try:
            account_name = self.entries['account_name'].get()
            self.entries['account_owner_horse'].delete(0, tk.END)
            self.entries['account_owner_horse'].insert(0, account_name)
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการซิงค์ชื่อบัญชี: {e}")
    
    def create_view_tab(self):
        """สร้างแท็บดูข้อมูล"""
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="📊 ดูข้อมูลบัญชีธนาคาร")
        
        # หัวข้อและปุ่ม
        top_frame = ttk.Frame(view_frame)
        top_frame.pack(fill='x', padx=20, pady=10)
        
        title = ttk.Label(top_frame, text="ข้อมูลทั้งหมด", 
                         font=('Arial', 16, 'bold'))
        title.pack(side='left')
        
        # ปุ่มจัดการ
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side='right')
        
        ttk.Button(btn_frame, text="🔄 รีเฟรช", 
                  command=self.refresh_data).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="✏️ แก้ไข", 
                  command=self.edit_selected).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="🗑️ ลบ", 
                  command=self.delete_selected).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="📋 คัดลอก", 
                  command=self.copy_selected).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="💾 บันทึก Excel", 
                  command=self.save_excel).pack(side='left', padx=2)
        
        # ตารางข้อมูล
        tree_frame = ttk.Frame(view_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview
        self.tree = ttk.Treeview(tree_frame)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", 
                                   command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", 
                                   command=self.tree.xview)
        
        self.tree.configure(yscrollcommand=v_scrollbar.set,
                           xscrollcommand=h_scrollbar.set)
        
        # Pack scrollbars และ treeview
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)
    
    def load_data(self):
        """โหลดข้อมูลจากไฟล์ Excel"""
        try:
            if os.path.exists(self.excel_file):
                if self.use_pandas:
                    try:
                        # ใช้ pandas
                        import pandas as pd
                        self.data = pd.read_excel(self.excel_file)
                        print(f"โหลดข้อมูล {len(self.data)} แถว จากไฟล์ Excel (pandas)")
                        
                    except Exception as pandas_error:
                        print(f"ไม่สามารถใช้ pandas อ่านไฟล์: {pandas_error}")
                        self.load_data_direct()
                else:
                    # ไม่มี pandas ใช้วิธีอื่น
                    self.load_data_direct()
            else:
                # สร้างข้อมูลเปล่า
                self.create_empty_data()
            
            # อัพเดทตารางแสดงผล
            if GUI_AVAILABLE and hasattr(self, 'tree'):
                self.update_treeview()
            
        except Exception as e:
            if GUI_AVAILABLE:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดข้อมูล: {str(e)}")
            print(f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
    
    def load_summons_data(self):
        """โหลดข้อมูลหมายเรียกผู้ต้องหาจากไฟล์ Excel"""
        try:
            if os.path.exists(self.summons_file):
                if self.use_pandas:
                    try:
                        # ใช้ pandas
                        import pandas as pd
                        self.summons_data = pd.read_excel(self.summons_file)
                        print(f"โหลดข้อมูลหมายเรียก {len(self.summons_data)} แถว จากไฟล์ Excel (pandas)")
                        
                    except Exception as pandas_error:
                        print(f"ไม่สามารถใช้ pandas อ่านไฟล์หมายเรียก: {pandas_error}")
                        self.load_summons_data_direct()
                else:
                    # ไม่มี pandas ใช้วิธีอื่น
                    self.load_summons_data_direct()
            else:
                # สร้างข้อมูลเปล่าสำหรับหมายเรียก
                self.create_empty_summons_data()
            
            # อัพเดทตารางแสดงผล
            if GUI_AVAILABLE and hasattr(self, 'summons_tree'):
                self.update_summons_treeview()
            
        except Exception as e:
            if GUI_AVAILABLE:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถโหลดข้อมูลหมายเรียก: {str(e)}")
            print(f"เกิดข้อผิดพลาดในการโหลดข้อมูลหมายเรียก: {e}")
    
    def load_summons_data_direct(self):
        """โหลดข้อมูลหมายเรียกโดยไม่ใช้ pandas"""
        try:
            headers, rows = self.read_excel_direct(self.summons_file)
            if headers and rows:
                self.summons_data_headers = headers
                self.summons_data_rows = rows
                
                if self.use_pandas:
                    import pandas as pd
                    self.summons_data = pd.DataFrame(rows, columns=headers)
                
                print(f"โหลดข้อมูลหมายเรียก {len(rows)} แถว จากไฟล์ Excel (direct)")
            else:
                self.create_empty_summons_data()
                
        except Exception as e:
            print(f"ไม่สามารถอ่านไฟล์หมายเรียก Excel โดยตรง: {e}")
            self.create_empty_summons_data()
    
    def create_empty_summons_data(self):
        """สร้างข้อมูลเปล่าสำหรับหมายเรียก"""
        columns = [
            "เลขที่หนังสือ", "ลงวันที่", "ชื่อ ผตห.", "เลขประจำตัว ปชช. ผตห.", 
            "สภ.พื้นที่รับผิดชอบ", "จังหวัด สภ.พื้นที่รับผิดชอบ", "ชื่อผู้เสียหาย", 
            "ประเภทคดี", "ความเสียหาย", "เลขเคสไอดี", "ที่อยู่ ผตห.", 
            "กำหนดให้มาพบ", "ที่อยู่ สภ. พื้นที่รับผิดชอบ"
        ]
        
        self.summons_data_headers = columns
        self.summons_data_rows = []
        
        if self.use_pandas:
            import pandas as pd
            self.summons_data = pd.DataFrame(columns=columns)
            
        print("สร้างไฟล์ข้อมูลหมายเรียกใหม่")
    
    def load_data_direct(self):
        """โหลดข้อมูลโดยไม่ใช้ pandas"""
        try:
            headers, rows = self.read_excel_direct()
            if headers and rows:
                self.data_headers = headers
                self.data_rows = rows
                
                if self.use_pandas:
                    import pandas as pd
                    self.data = pd.DataFrame(rows, columns=headers)
                
                print(f"โหลดข้อมูล {len(rows)} แถว จากไฟล์ Excel (direct)")
            else:
                self.create_empty_data()
                
        except Exception as e:
            print(f"ไม่สามารถอ่านไฟล์ Excel โดยตรง: {e}")
            self.create_empty_data()
    
    def read_excel_direct(self, file_path=None):
        """อ่านไฟล์ Excel โดยตรงโดยไม่ใช้ pandas"""
        if file_path is None:
            file_path = self.excel_file
            
        try:
            with zipfile.ZipFile(file_path, 'r') as zip_file:
                # อ่าน shared strings
                shared_strings = []
                try:
                    with zip_file.open('xl/sharedStrings.xml') as f:
                        tree = ET.parse(f)
                        root = tree.getroot()
                        
                        ns = {'ss': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                        
                        for si in root.findall('.//ss:si', ns):
                            t = si.find('.//ss:t', ns)
                            if t is not None:
                                shared_strings.append(t.text or '')
                            else:
                                shared_strings.append('')
                except:
                    pass
                
                # อ่านข้อมูลจาก worksheet
                with zip_file.open('xl/worksheets/sheet1.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    ns = {'ss': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    
                    rows_data = []
                    for row in root.findall('.//ss:row', ns):
                        row_data = []
                        for cell in row.findall('.//ss:c', ns):
                            value = ""
                            
                            t_attr = cell.get('t')
                            v_elem = cell.find('.//ss:v', ns)
                            
                            if v_elem is not None:
                                if t_attr == 's':  # shared string
                                    try:
                                        idx = int(v_elem.text)
                                        if idx < len(shared_strings):
                                            value = shared_strings[idx]
                                    except:
                                        value = v_elem.text or ""
                                else:
                                    value = v_elem.text or ""
                            
                            row_data.append(value)
                        
                        if row_data:
                            rows_data.append(row_data)
                    
                    if rows_data:
                        headers = rows_data[0] if rows_data else []
                        data_rows = rows_data[1:] if len(rows_data) > 1 else []
                        return headers, data_rows
            
            return None, None
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการอ่าน Excel โดยตรง: {e}")
            return None, None
    
    def create_empty_data(self):
        """สร้างข้อมูลเปล่า (ตามโครงสร้างไฟล์เดิม)"""
        columns = ["ลำดับ", "เลขหนังสือ", "วัน", "เดือน ", "ปี ", "ธนาคารสาขา", 
                  "ผู้เสียหาย", "เคสไอดี", "เจ้าของบัญชีม้า", "ชื่อธนาคาร", "เลขบัญชี", 
                  "ชื่อบัญชี", "ช่วงเวลา", "ที่อยู่ธนาคาร", "ซอย", "หมู่", "ตำบล/แขวง", 
                  "อำเภอ/เขต", "ถนน", "จังหวัด", "รหัสไปรษณี", "วันนัดส่ง", "เดือนส่ง ", "เวลาส่ง"]
        
        self.data_headers = columns
        self.data_rows = []
        
        if self.use_pandas:
            import pandas as pd
            self.data = pd.DataFrame(columns=columns)
            
        print("สร้างไฟล์ข้อมูลใหม่")
    
    def convert_excel_to_csv(self):
        """แปลงไฟล์ Excel เป็น CSV"""
        try:
            import subprocess
            csv_file = "temp_data.csv"
            cmd = f'libreoffice --headless --convert-to csv --outdir . "{self.excel_file}"'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            if result.returncode == 0:
                converted_file = self.excel_file.replace('.xlsx', '.csv')
                if os.path.exists(converted_file):
                    os.rename(converted_file, csv_file)
                    return True
            return False
        except:
            return False
    
    def load_from_csv(self):
        """โหลดข้อมูลจาก CSV"""
        csv_file = "temp_data.csv"
        try:
            import csv
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                data = list(reader)
                
            if data:
                headers = data[0]
                rows = data[1:]
                
                # สร้าง DataFrame จากข้อมูล CSV
                import pandas as pd
                self.data = pd.DataFrame(rows, columns=headers)
                print(f"โหลดข้อมูล {len(rows)} แถว จาก CSV")
                
                # ลบไฟล์ชั่วคราว
                os.remove(csv_file)
            else:
                self.create_empty_dataframe()
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการโหลด CSV: {e}")
            self.create_empty_dataframe()
    
    def filter_display_columns(self, columns, data_rows):
        """กรองคอลัมน์ที่จะแสดง - ซ่อนคอลัมน์ภาษาอังกฤษและคอลัมน์ว่าง"""
        if not columns:
            return []
        
        display_columns = []
        
        for i, col in enumerate(columns):
            # ตรวจสอบว่าเป็นคอลัมน์ภาษาไทยและมีข้อมูล
            is_thai_column = self.is_thai_column(col)
            has_data = self.column_has_data(i, data_rows)
            
            # แสดงเฉพาะคอลัมน์ภาษาไทยที่มีข้อมูล
            if is_thai_column and has_data:
                display_columns.append(col)
        
        return display_columns
    
    def is_thai_column(self, column_name):
        """ตรวจสอบว่าชื่อคอลัมน์เป็นภาษาไทยหรือไม่"""
        if not column_name or not isinstance(column_name, str):
            return False
        
        # รายการคอลัมน์ภาษาไทยที่ต้องการ
        thai_columns = [
            'ลำดับ', 'เลขหนังสือ', 'วัน', 'เดือน', 'ปี', 'ธนาคารสาขา',
            'ผู้เสียหาย', 'เคสไอดี', 'เจ้าของบัญชีม้า', 'ชื่อธนาคาร', 'เลขบัญชี',
            'ชื่อบัญชี', 'ช่วงเวลา', 'ที่อยู่ธนาคาร', 'ซอย', 'หมู่', 'ตำบล/แขวง',
            'อำเภอ/เขต', 'ถนน', 'จังหวัด', 'รหัสไปรษณีย์', 'วันนัดส่ง', 'เดือนส่ง', 'เวลาส่ง'
        ]
        
        # ตรวจสอบว่าชื่อคอลัมน์ตรงกับรายการหรือไม่ (รวมทั้งช่องว่างด้วย)
        column_clean = column_name.strip()
        for thai_col in thai_columns:
            if thai_col in column_clean:
                return True
        
        return False
    
    def column_has_data(self, column_index, data_rows):
        """ตรวจสอบว่าคอลัมน์มีข้อมูลหรือไม่"""
        if not data_rows or column_index < 0:
            return False
        
        # ตรวจสอบอย่างน้อย 5 แถวแรกเพื่อดูว่ามีข้อมูลหรือไม่
        sample_size = min(5, len(data_rows))
        
        for i, row in enumerate(data_rows[:sample_size]):
            if column_index < len(row):
                value = str(row[column_index]).strip()
                if value and value != '' and value.lower() != 'nan' and value != 'None':
                    return True
        
        return False
    
    def update_treeview(self):
        """อัพเดทตารางแสดงข้อมูล"""
        if not GUI_AVAILABLE:
            return
            
        # ล้างข้อมูลเก่า
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # ตรวจสอบว่ามีข้อมูลหรือไม่
        if self.use_pandas:
            if self.data is None or self.data.empty:
                return
            columns = list(self.data.columns)
            data_rows = self.data.values.tolist()
        else:
            if not self.data_headers or not self.data_rows:
                return
            columns = self.data_headers
            data_rows = self.data_rows
        
        # กรองคอลัมน์ที่จะแสดง (เฉพาะคอลัมน์ที่มีข้อมูลและเป็นภาษาไทย)
        display_columns = self.filter_display_columns(columns, data_rows)
        
        # ตั้งค่าคอลัมน์
        self.tree['columns'] = display_columns
        self.tree['show'] = 'headings'
        
        # ตั้งค่าหัวข้อ
        for col in display_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=80)
        
        # กำหนดสีสำหรับแถวที่ตอบกลับแล้ว
        self.tree.tag_configure('replied', foreground='green')
        
        # เพิ่มข้อมูล (เฉพาะคอลัมน์ที่เลือกแสดง)
        column_indices = [columns.index(col) for col in display_columns if col in columns]
        
        for row in data_rows:
            if self.use_pandas:
                try:
                    import pandas as pd
                    full_values = [str(val) if pd.notna(val) else "" for val in row]
                except:
                    full_values = [str(val) if val else "" for val in row]
            else:
                full_values = [str(val) if val else "" for val in row]
            
            # เลือกเฉพาะคอลัมน์ที่ต้องแสดง
            filtered_values = []
            for i in column_indices:
                if i < len(full_values):
                    filtered_values.append(full_values[i])
                else:
                    filtered_values.append("")
            
            # ตรวจสอบว่าแถวนี้ตอบกลับแล้วหรือไม่
            tags = ()
            if "ตอบกลับ" in columns:
                replied_index = columns.index("ตอบกลับ")
                if replied_index < len(full_values) and str(full_values[replied_index]).strip().upper() == "X":
                    tags = ('replied',)
            
            self.tree.insert('', 'end', values=filtered_values, tags=tags)
    
    def save_data(self):
        """บันทึกข้อมูลใหม่ลงไฟล์เดิม"""
        try:
            # รวบรวมข้อมูลจากฟอร์ม
            form_data = {}
            for key, widget in self.entries.items():
                if isinstance(widget, tk.Text):
                    value = widget.get("1.0", tk.END).strip()
                elif isinstance(widget, ttk.Combobox):
                    value = widget.get().strip()
                else:
                    value = widget.get().strip()
                form_data[key] = value
            
            # แมพข้อมูลกับคอลัมน์ไฟล์เดิม (ตรงตามชื่อคอลัมน์ที่มีช่องว่าง)
            column_mapping = {
                'order_no': 'ลำดับ',
                'document_no': 'เลขหนังสือ',
                'day': 'วัน',
                'month': 'เดือน ',  # มีช่องว่าง
                'year': 'ปี ',      # มีช่องว่าง
                'bank_branch': 'ธนาคารสาขา',
                'victim': 'ผู้เสียหาย',
                'case_id': 'เคสไอดี',
                'account_owner_horse': 'เจ้าของบัญชีม้า',
                'bank_name': 'ชื่อธนาคาร',
                'account_no': 'เลขบัญชี',
                'account_name': 'ชื่อบัญชี',
                'time_period': 'ช่วงเวลา',
                'bank_address': 'ที่อยู่ธนาคาร',
                'soi': 'ซอย',
                'moo': 'หมู่',
                'tambon_khwaeng': 'ตำบล/แขวง',
                'amphoe_khet': 'อำเภอ/เขต',
                'road': 'ถนน',
                'province': 'จังหวัด',
                'postal_code': 'รหัสไปรษณี',
                'delivery_day': 'วันนัดส่ง',
                'delivery_month': 'เดือนส่ง ',  # มีช่องว่าง
                'delivery_time': 'เวลาส่ง'
            }
            
            # สร้างแถวข้อมูลใหม่ตามโครงสร้างไฟล์เดิม
            if self.use_pandas and self.data is not None:
                # ใช้ pandas
                excel_columns = list(self.data.columns)
                new_row_data = {}
                
                for form_key, excel_col in column_mapping.items():
                    if excel_col in excel_columns:
                        new_row_data[excel_col] = form_data.get(form_key, '')
                
                # เพิ่มข้อมูลใหม่
                import pandas as pd
                new_row = pd.DataFrame([new_row_data])
                self.data = pd.concat([self.data, new_row], ignore_index=True)
                
                # บันทึกลงไฟล์ Excel ทันที
                self.data.to_excel(self.excel_file, index=False)
                
            else:
                # ไม่ใช้ pandas - ใช้วิธีอื่น
                if self.data_headers:
                    new_row = []
                    for header in self.data_headers:
                        # หาข้อมูลที่ตรงกับหัวข้อ
                        value = ''
                        for form_key, excel_col in column_mapping.items():
                            if excel_col == header:
                                value = form_data.get(form_key, '')
                                break
                        new_row.append(value)
                    
                    # เพิ่มข้อมูลใหม่
                    self.data_rows.append(new_row)
                    
                    # บันทึกลงไฟล์ Excel ด้วยวิธีพิเศษ
                    self.save_to_excel_direct()
            
            # รีโหลดข้อมูลและอัพเดทตาราง
            self.load_data()
            
            # ล้างฟิลด์และตั้งค่าใหม่
            self.clear_entries()
            
            messagebox.showinfo("สำเร็จ", f"บันทึกข้อมูลลงไฟล์ {self.excel_file} เรียบร้อย")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกข้อมูล: {str(e)}")
            print(f"รายละเอียดข้อผิดพลาดการบันทึก: {e}")
    
    def save_to_excel_direct(self):
        """บันทึกข้อมูลลงไฟล์ Excel โดยตรง (ไม่ใช้ pandas)"""
        try:
            # ใช้ Excel writer ที่เขียนเอง
            success = self.write_excel_file(self.excel_file, self.data_headers, self.data_rows)
            
            if not success:
                # ถ้าไม่สำเร็จ ลองใช้วิธี CSV + LibreOffice
                self.fallback_csv_method()
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการบันทึก Excel: {e}")
            self.fallback_csv_method()
    
    def write_excel_file(self, filename, headers, data_rows):
        """เขียนไฟล์ Excel โดยตรง"""
        try:
            import shutil
            from datetime import datetime
            
            # สร้างไฟล์ Excel ใหม่
            temp_dir = "temp_excel"
            if os.path.exists(temp_dir):
                shutil.rmtree(temp_dir)
            os.makedirs(temp_dir)
            
            # สร้างโครงสร้างไฟล์ Excel
            self.create_excel_structure(temp_dir, headers, data_rows)
            
            # สำรองไฟล์เดิม
            if os.path.exists(filename):
                backup_file = f"{filename}.backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
                shutil.copy2(filename, backup_file)
                print(f"สำรองไฟล์เดิมไว้ที่ {backup_file}")
            
            # บีบอัดเป็นไฟล์ .xlsx
            with zipfile.ZipFile(filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(temp_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arc_path = os.path.relpath(file_path, temp_dir)
                        zipf.write(file_path, arc_path)
            
            # ลบโฟลเดอร์ชั่วคราว
            shutil.rmtree(temp_dir)
            
            print(f"เขียนข้อมูลลงไฟล์ {filename} สำเร็จ ({len(data_rows)} แถว)")
            return True
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการเขียนไฟล์ Excel: {e}")
            return False
    
    def create_excel_structure(self, temp_dir, headers, data_rows):
        """สร้างโครงสร้างไฟล์ Excel"""
        import shutil
        from datetime import datetime
        
        # สร้างโฟลเดอร์
        os.makedirs(os.path.join(temp_dir, "_rels"))
        os.makedirs(os.path.join(temp_dir, "docProps"))
        os.makedirs(os.path.join(temp_dir, "xl"))
        os.makedirs(os.path.join(temp_dir, "xl", "_rels"))
        os.makedirs(os.path.join(temp_dir, "xl", "worksheets"))
        
        # สร้างไฟล์ XML ต่างๆ
        self.create_content_types(temp_dir)
        self.create_relationships(temp_dir)
        self.create_doc_props(temp_dir)
        self.create_shared_strings_file(temp_dir, headers, data_rows)
        self.create_worksheet_file(temp_dir, headers, data_rows)
        self.create_workbook_file(temp_dir)
    
    def create_content_types(self, temp_dir):
        """สร้าง [Content_Types].xml"""
        content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
<Default Extension="xml" ContentType="application/xml"/>
<Override PartName="/xl/workbook.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet.main+xml"/>
<Override PartName="/xl/worksheets/sheet1.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.worksheet+xml"/>
<Override PartName="/xl/sharedStrings.xml" ContentType="application/vnd.openxmlformats-officedocument.spreadsheetml.sharedStrings+xml"/>
<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>
<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>
</Types>'''
        
        with open(os.path.join(temp_dir, "[Content_Types].xml"), 'w', encoding='utf-8') as f:
            f.write(content)
    
    def create_relationships(self, temp_dir):
        """สร้างไฟล์ relationships"""
        # _rels/.rels
        rels_content = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="xl/workbook.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>
<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>
</Relationships>'''
        
        with open(os.path.join(temp_dir, "_rels", ".rels"), 'w', encoding='utf-8') as f:
            f.write(rels_content)
        
        # xl/_rels/workbook.xml.rels
        workbook_rels = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/worksheet" Target="worksheets/sheet1.xml"/>
<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/sharedStrings" Target="sharedStrings.xml"/>
</Relationships>'''
        
        with open(os.path.join(temp_dir, "xl", "_rels", "workbook.xml.rels"), 'w', encoding='utf-8') as f:
            f.write(workbook_rels)
    
    def create_doc_props(self, temp_dir):
        """สร้างไฟล์ document properties"""
        from datetime import datetime
        
        # docProps/app.xml
        app_props = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties" xmlns:vt="http://schemas.openxmlformats.org/officeDocument/2006/docPropsVTypes">
<Application>Excel Data Manager</Application>
<ScaleCrop>false</ScaleCrop>
<SharedDoc>false</SharedDoc>
<HyperlinksChanged>false</HyperlinksChanged>
<AppVersion>1.0</AppVersion>
</Properties>'''
        
        with open(os.path.join(temp_dir, "docProps", "app.xml"), 'w', encoding='utf-8') as f:
            f.write(app_props)
        
        # docProps/core.xml
        now = datetime.now().isoformat()
        core_props = f'''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" xmlns:dc="http://purl.org/dc/elements/1.1/" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dcmitype="http://purl.org/dc/dcmitype/" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">
<dc:creator>Excel Data Manager</dc:creator>
<dcterms:created xsi:type="dcterms:W3CDTF">{now}</dcterms:created>
<dcterms:modified xsi:type="dcterms:W3CDTF">{now}</dcterms:modified>
</cp:coreProperties>'''
        
        with open(os.path.join(temp_dir, "docProps", "core.xml"), 'w', encoding='utf-8') as f:
            f.write(core_props)
    
    def create_shared_strings_file(self, temp_dir, headers, data_rows):
        """สร้างไฟล์ shared strings"""
        all_strings = set()
        
        # รวบรวม string ทั้งหมด
        for header in headers:
            if isinstance(header, str) and header.strip():
                all_strings.add(header.strip())
        
        for row in data_rows:
            for cell in row:
                if isinstance(cell, str) and cell.strip():
                    all_strings.add(cell.strip())
        
        self.string_list = sorted(list(all_strings))
        self.string_map = {s: i for i, s in enumerate(self.string_list)}
        
        # สร้าง XML
        root = ET.Element("sst")
        root.set("xmlns", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")
        root.set("count", str(len(self.string_list)))
        root.set("uniqueCount", str(len(self.string_list)))
        
        for string_val in self.string_list:
            si = ET.SubElement(root, "si")
            t = ET.SubElement(si, "t")
            t.text = string_val
        
        # เขียนไฟล์
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        tree.write(os.path.join(temp_dir, "xl", "sharedStrings.xml"), 
                   encoding='utf-8', xml_declaration=True)
    
    def create_worksheet_file(self, temp_dir, headers, data_rows):
        """สร้าง worksheet"""
        root = ET.Element("worksheet")
        root.set("xmlns", "http://schemas.openxmlformats.org/spreadsheetml/2006/main")
        
        sheet_data = ET.SubElement(root, "sheetData")
        
        # หัวข้อ
        header_row = ET.SubElement(sheet_data, "row")
        header_row.set("r", "1")
        
        for col_idx, header in enumerate(headers, 1):
            cell = ET.SubElement(header_row, "c")
            col_letter = chr(64 + col_idx) if col_idx <= 26 else f"A{chr(64 + col_idx - 26)}"
            cell.set("r", f"{col_letter}1")
            cell.set("t", "s")  # string type
            
            v = ET.SubElement(cell, "v")
            v.text = str(self.string_map.get(header.strip(), 0))
        
        # ข้อมูล
        for row_idx, row_data in enumerate(data_rows, 2):
            row_elem = ET.SubElement(sheet_data, "row")
            row_elem.set("r", str(row_idx))
            
            for col_idx, cell_value in enumerate(row_data, 1):
                cell = ET.SubElement(row_elem, "c")
                col_letter = chr(64 + col_idx) if col_idx <= 26 else f"A{chr(64 + col_idx - 26)}"
                cell_ref = f"{col_letter}{row_idx}"
                cell.set("r", cell_ref)
                
                if isinstance(cell_value, str) and cell_value.strip():
                    cell.set("t", "s")  # string
                    v = ET.SubElement(cell, "v")
                    v.text = str(self.string_map.get(cell_value.strip(), 0))
                else:
                    # ลองเป็นตัวเลข
                    try:
                        float(str(cell_value))
                        v = ET.SubElement(cell, "v")
                        v.text = str(cell_value)
                    except:
                        if str(cell_value).strip():
                            cell.set("t", "s")
                            v = ET.SubElement(cell, "v")
                            v.text = str(self.string_map.get(str(cell_value).strip(), 0))
        
        # เขียนไฟล์
        tree = ET.ElementTree(root)
        ET.indent(tree, space="  ", level=0)
        tree.write(os.path.join(temp_dir, "xl", "worksheets", "sheet1.xml"), 
                   encoding='utf-8', xml_declaration=True)
    
    def create_workbook_file(self, temp_dir):
        """สร้าง workbook"""
        workbook_xml = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<workbook xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main" xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
<sheets>
<sheet name="Sheet1" sheetId="1" r:id="rId1"/>
</sheets>
</workbook>'''
        
        with open(os.path.join(temp_dir, "xl", "workbook.xml"), 'w', encoding='utf-8') as f:
            f.write(workbook_xml)
    
    def fallback_csv_method(self):
        """วิธีสำรองใช้ CSV"""
        try:
            csv_temp = "temp_save.csv"
            import csv
            
            with open(csv_temp, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(self.data_headers)
                writer.writerows(self.data_rows)
            
            print(f"บันทึกข้อมูลเป็น CSV: {csv_temp}")
            print("กรุณาเปิดไฟล์ CSV ใน Excel และบันทึกเป็น .xlsx")
            
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการสำรอง CSV: {e}")
    
    def clear_entries(self):
        """ล้างข้อมูลในฟิลด์"""
        for key, widget in self.entries.items():
            try:
                # ปลดล็อกฟิลด์ที่เป็น readonly ชั่วคราว
                if hasattr(widget, 'config'):
                    widget.config(state='normal')
                
                if isinstance(widget, tk.Text):
                    widget.delete("1.0", tk.END)
                elif isinstance(widget, ttk.Combobox):
                    widget.set('')
                else:
                    widget.delete(0, tk.END)
            except:
                pass
        
        # ตั้งค่าข้อมูลอัตโนมัติใหม่
        self.set_automatic_values()
    
    def refresh_data(self):
        """รีเฟรชข้อมูล"""
        self.load_data()
        messagebox.showinfo("สำเร็จ", "รีเฟรชข้อมูลเรียบร้อย")
    
    def edit_selected(self):
        """แก้ไขข้อมูลที่เลือก"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกข้อมูลที่ต้องการแก้ไข")
            return
        
        # หาข้อมูลที่เลือก
        item = self.tree.item(selection[0])
        displayed_values = item['values']
        row_index = self.tree.index(selection[0])
        
        # เตรียมข้อมูลแถวที่แก้ไขจากข้อมูลจริง
        if self.use_pandas and self.data is not None:
            all_columns = list(self.data.columns)
            all_data_rows = self.data.values.tolist()
        else:
            all_columns = self.data_headers
            all_data_rows = self.data_rows
        
        # หาข้อมูลแถวที่แก้ไขจากข้อมูลจริง
        if row_index < len(all_data_rows):
            full_row_data = all_data_rows[row_index]
        else:
            messagebox.showerror("ข้อผิดพลาด", "ไม่พบข้อมูลแถวที่ต้องการแก้ไข")
            return
        
        # สร้างหน้าต่างแก้ไข
        edit_window = tk.Toplevel(self.root)
        edit_window.title("แก้ไขข้อมูล")
        edit_window.geometry("700x600")
        edit_window.resizable(True, True)
        
        # สร้าง main frame และ scrollable area
        main_frame = ttk.Frame(edit_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # สร้าง canvas และ scrollbar
        canvas = tk.Canvas(main_frame, bg="white")
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        # ตั้งค่า scroll region
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # เพิ่ม scrollable frame ลงใน canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # เพิ่มการสนับสนุน mouse wheel
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # หัวข้อ
        title_label = ttk.Label(scrollable_frame, text="แก้ไขข้อมูล", font=('Arial', 16, 'bold'))
        title_label.pack(pady=(10, 20))
        
        # ฟิลด์แก้ไข
        edit_entries = {}
        
        for i, col in enumerate(all_columns):
            # ตรวจสอบว่าเป็นคอลัมน์ภาษาไทยหรือไม่
            if not self.is_thai_column(col):
                continue  # ข้ามคอลัมน์ภาษาอังกฤษ
            
            # เอาข้อมูลจากแถวเต็ม
            if i < len(full_row_data):
                value = full_row_data[i]
            else:
                value = ""
            
            # สร้าง frame สำหรับแต่ละฟิลด์
            field_frame = ttk.Frame(scrollable_frame)
            field_frame.pack(fill='x', padx=20, pady=5)
            
            # Label
            label = ttk.Label(field_frame, text=col, width=18, font=('Arial', 10))
            label.pack(side='left', padx=(0, 10))
            
            # สร้าง widget ตามประเภทของฟิลด์
            if col in ['ที่อยู่ธนาคาร', 'ผู้เสียหาย']:
                # Text widget สำหรับข้อความยาว
                entry = tk.Text(field_frame, height=3, width=50, font=('Arial', 10), wrap=tk.WORD)
                entry.insert("1.0", str(value) if value else "")
            elif col in ['เดือน', 'เดือนส่ง']:
                # Combobox สำหรับฟิลด์เดือน
                entry = ttk.Combobox(field_frame, width=47, font=('Arial', 10), state="readonly")
                thai_months = [
                    "มกราคม", "กุมภาพันธ์", "มีนาคม", "เมษายน",
                    "พฤษภาคม", "มิถุนายน", "กรกฎาคม", "สิงหาคม",
                    "กันยายน", "ตุลาคม", "พฤศจิกายน", "ธันวาคม"
                ]
                entry['values'] = thai_months
                if str(value) in thai_months:
                    entry.set(str(value))
                else:
                    entry.set("")  # ไม่ตั้งค่าเริ่มต้น
            else:
                # Entry widget สำหรับฟิลด์ปกติ
                entry = ttk.Entry(field_frame, width=50, font=('Arial', 10))
                entry.insert(0, str(value) if value else "")
            
            entry.pack(side='left', fill='x', expand=True)
            edit_entries[col] = entry
        
        # สร้าง frame สำหรับปุ่ม (นอก scrollable area)
        button_main_frame = ttk.Frame(edit_window)
        button_main_frame.pack(side="bottom", fill="x", padx=10, pady=10)
        
        # เพิ่ม checkbox สำหรับ "ตอบกลับ"
        replied_frame = ttk.Frame(button_main_frame)
        replied_frame.pack(pady=5)
        
        replied_var = tk.BooleanVar()
        # ตรวจสอบสถานะปัจจุบันจากคอลัมน์ "ตอบกลับ" หากมี
        replied_status = ""
        if "ตอบกลับ" in all_columns:
            replied_col_index = all_columns.index("ตอบกลับ")
            if replied_col_index < len(full_row_data):
                replied_status = str(full_row_data[replied_col_index]) if full_row_data[replied_col_index] else ""
        
        replied_var.set(replied_status.strip().upper() == "X")
        
        replied_checkbox = ttk.Checkbutton(
            replied_frame, 
            text="รับได้ข้อมูลตอบกลับแล้ว", 
            variable=replied_var,
            style="TCheckbutton"
        )
        replied_checkbox.pack(pady=5)
        
        # ปุ่มบันทึกและยกเลิก
        btn_frame = ttk.Frame(button_main_frame)
        btn_frame.pack(pady=10)
        
        def save_edit():
            try:
                # อัพเดทข้อมูล
                for col, entry in edit_entries.items():
                    if isinstance(entry, tk.Text):
                        value = entry.get("1.0", tk.END).strip()
                    elif isinstance(entry, ttk.Combobox):
                        value = entry.get().strip()
                    else:
                        value = entry.get().strip()
                    
                    # อัพเดทข้อมูลในโครงสร้างข้อมูล
                    if self.use_pandas and self.data is not None:
                        self.data.at[row_index, col] = value
                    else:
                        # อัพเดทใน data_rows
                        col_index = all_columns.index(col) if col in all_columns else -1
                        if col_index >= 0 and row_index < len(self.data_rows):
                            if col_index < len(self.data_rows[row_index]):
                                self.data_rows[row_index][col_index] = value
                            else:
                                # ขยาย list ถ้าจำเป็น
                                while len(self.data_rows[row_index]) <= col_index:
                                    self.data_rows[row_index].append("")
                                self.data_rows[row_index][col_index] = value
                
                # จัดการคอลัมน์ "ตอบกลับ"
                replied_value = "X" if replied_var.get() else ""
                
                if self.use_pandas and self.data is not None:
                    # เพิ่มคอลัมน์ "ตอบกลับ" ถ้ายังไม่มี
                    if "ตอบกลับ" not in self.data.columns:
                        self.data["ตอบกลับ"] = ""
                    self.data.at[row_index, "ตอบกลับ"] = replied_value
                else:
                    # เพิ่มคอลัมน์ "ตอบกลับ" ถ้ายังไม่มี
                    if "ตอบกลับ" not in all_columns:
                        all_columns.append("ตอบกลับ")
                        self.data_headers.append("ตอบกลับ")
                        # เพิ่มคอลัมน์ว่างให้ทุกแถว
                        for i in range(len(self.data_rows)):
                            self.data_rows[i].append("")
                    
                    # อัพเดทค่า "ตอบกลับ" ในแถวนี้
                    replied_col_index = all_columns.index("ตอบกลับ")
                    if replied_col_index < len(self.data_rows[row_index]):
                        self.data_rows[row_index][replied_col_index] = replied_value
                    else:
                        # ขยาย list ถ้าจำเป็น
                        while len(self.data_rows[row_index]) <= replied_col_index:
                            self.data_rows[row_index].append("")
                        self.data_rows[row_index][replied_col_index] = replied_value
                
                # บันทึกลงไฟล์
                if self.use_pandas and self.data is not None:
                    self.data.to_excel(self.excel_file, index=False)
                else:
                    # ใช้วิธีบันทึกโดยตรง
                    self.save_to_excel_direct()
                
                # อัพเดทตาราง
                self.update_treeview()
                
                edit_window.destroy()
                messagebox.showinfo("สำเร็จ", "แก้ไขข้อมูลเรียบร้อย")
                
            except Exception as e:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถแก้ไขข้อมูล: {str(e)}")
                print(f"รายละเอียดข้อผิดพลาดการแก้ไข: {e}")
        
        # ปุ่มบันทึกและยกเลิก
        save_btn = ttk.Button(btn_frame, text="💾 บันทึกการแก้ไข", command=save_edit)
        save_btn.pack(side='left', padx=15)
        
        cancel_btn = ttk.Button(btn_frame, text="❌ ยกเลิก", command=edit_window.destroy)
        cancel_btn.pack(side='left', padx=15)
        
        # Pack canvas และ scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # ตั้งค่า focus ที่หน้าต่าง
        edit_window.focus_set()
        
        # ปรับขนาด canvas เมื่อ content เปลี่ยนแปลง
        def update_scroll_region():
            canvas.update_idletasks()
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        edit_window.after(100, update_scroll_region)
    
    def delete_selected(self):
        """ลบข้อมูลที่เลือก"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกข้อมูลที่ต้องการลบ")
            return
        
        if messagebox.askyesno("ยืนยัน", "คุณต้องการลบข้อมูลนี้หรือไม่?"):
            try:
                row_index = self.tree.index(selection[0])
                self.data = self.data.drop(self.data.index[row_index]).reset_index(drop=True)
                
                # บันทึกลงไฟล์
                self.data.to_excel(self.excel_file, index=False)
                
                # อัพเดทตาราง
                self.update_treeview()
                
                messagebox.showinfo("สำเร็จ", "ลบข้อมูลเรียบร้อย")
                
            except Exception as e:
                messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถลบข้อมูล: {str(e)}")
    
    def copy_selected(self):
        """คัดลอกข้อมูลที่เลือก"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("คำเตือน", "กรุณาเลือกข้อมูลที่ต้องการคัดลอก")
            return
        
        try:
            row_index = self.tree.index(selection[0])
            row_data = self.data.iloc[row_index].copy()
            
            # เพิ่มข้อมูลที่คัดลอก
            new_row = pd.DataFrame([row_data])
            self.data = pd.concat([self.data, new_row], ignore_index=True)
            
            # บันทึกลงไฟล์
            self.data.to_excel(self.excel_file, index=False)
            
            # อัพเดทตาราง
            self.update_treeview()
            
            messagebox.showinfo("สำเร็จ", "คัดลอกข้อมูลเรียบร้อย")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถคัดลอกข้อมูล: {str(e)}")
    
    def save_excel(self):
        """บันทึกไฟล์ Excel"""
        try:
            # บันทึกลงไฟล์ที่กำหนดโดยตรง
            filename = "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"
            
            # บันทึกไฟล์โดยไม่ถามยืนยัน (overwrite if exists)
            self.data.to_excel(filename, index=False)
            messagebox.showinfo("สำเร็จ", f"บันทึกไฟล์ {filename} เรียบร้อย")
                
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกไฟล์: {str(e)}")
    
    def run(self):
        """เริ่มต้นโปรแกรม"""
        if GUI_AVAILABLE:
            self.root.mainloop()

    def create_summons_input_tab(self):
        """สร้างแท็บกรอกข้อมูลหมายเรียกผู้ต้องหา"""
        input_frame = ttk.Frame(self.notebook)
        self.notebook.add(input_frame, text="👤 ข้อมูล ผตห.")
        
        # สร้าง scrollable frame
        canvas = tk.Canvas(input_frame)
        scrollbar = ttk.Scrollbar(input_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # หัวข้อ
        title = ttk.Label(scrollable_frame, text="เพิ่มข้อมูลหมายเรียกผู้ต้องหา", 
                         font=('Arial', 16, 'bold'))
        title.pack(pady=20)
        
        # ฟิลด์กรอกข้อมูลหมายเรียก
        self.summons_entries = {}
        
        # จัดกลุ่มฟิลด์
        groups = [
            ("📜 ข้อมูลหนังสือ", [
                ("เลขที่หนังสือ", "doc_number", "entry"),
                ("ลงวันที่", "doc_date", "date"),
            ]),
            ("👤 ข้อมูลผู้ต้องหา", [
                ("ชื่อ ผตห.", "suspect_name", "entry"),
                ("เลขประจำตัว ปชช. ผตห.", "suspect_id", "entry"),
                ("ที่อยู่ ผตห.", "suspect_address", "text"),
            ]),
            ("🏢 ข้อมูลสถานีตำรวจ", [
                ("สภ.พื้นที่รับผิดชอบ", "police_station", "entry"),
                ("จังหวัด สภ.พื้นที่รับผิดชอบ", "police_province", "entry"),
                ("ที่อยู่ สภ. พื้นที่รับผิดชอบ", "police_address", "text"),
            ]),
            ("⚖️ ข้อมูลคดี", [
                ("ชื่อผู้เสียหาย", "victim_name", "entry"),
                ("ประเภทคดี", "case_type", "dropdown"),
                ("ความเสียหาย", "damage_amount", "entry"),
                ("เลขเคสไอดี", "case_id", "entry"),
            ]),
            ("📅 ข้อมูลการนัดหมาย", [
                ("กำหนดให้มาพบ", "appointment_date", "date"),
            ])
        ]
        
        for group_title, group_fields in groups:
            # หัวข้อกลุ่ม
            group_label = ttk.Label(scrollable_frame, text=group_title, 
                                   font=('Arial', 12, 'bold'))
            group_label.pack(pady=(20, 10))
            
            # สร้างเฟรมสำหรับกลุ่ม
            group_frame = ttk.LabelFrame(scrollable_frame, text="", padding=15)
            group_frame.pack(fill='x', padx=30, pady=(0, 10))
            
            for label_text, key, field_type in group_fields:
                field_frame = ttk.Frame(group_frame)
                field_frame.pack(fill='x', pady=3)
                
                label = ttk.Label(field_frame, text=label_text, width=18, font=('Arial', 10))
                label.pack(side='left', padx=(0, 10))
                
                # สร้าง widget ตามประเภท
                if field_type == "text":
                    entry = tk.Text(field_frame, height=3, width=50, font=('Arial', 10))
                elif field_type == "date":
                    # ใช้ entry ธรรมดาสำหรับวันที่
                    entry = ttk.Entry(field_frame, width=50, font=('Arial', 10))
                    if key == "doc_date":
                        # ตั้งค่าวันที่ปัจจุบัน
                        from datetime import datetime
                        today = datetime.now().strftime("%d/%m/%Y")
                        entry.insert(0, today)
                    elif key == "appointment_date":
                        # ตั้งค่าวันที่กำหนดพบเป็นวันปัจจุบัน + 7 วัน ในรูปแบบไทย
                        default_date = get_default_appointment_date()
                        thai_formatted_date = format_thai_date(default_date)
                        entry.insert(0, thai_formatted_date)
                elif field_type == "dropdown":
                    entry = ttk.Combobox(field_frame, width=47, font=('Arial', 10), state="readonly")
                    if key == "case_type":
                        # รายการประเภทคดี
                        case_types = [
                            "1.คดีไม่เข้า พรก.",
                            "2.หลอกลวงซื้อขายสินค้าหรือบริการ ที่ไม่มีลักษณะเป็นขบวนการ",
                            "3.หลอกลวงเป็นบุคคลอื่นเพื่อยืมเงิน",
                            "4.หลอกลวงให้รักแล้วโอนเงิน (Romance Scam)",
                            "5.หลอกลวงให้โอนเงินเพื่อรับรางวัลหรือวัตถุประสงค์อื่นๆ",
                            "6.หลอกลวงให้กู้เงินอันมีลักษณะฉ้อโกง กรรโชก หรือรีดเอาทรัพย์",
                            "7.หลอกลวงให้โอนเงินเพื่อทำงานหารายได้พิเศษ",
                            "8.ข่มขู่ทางโทรศัพท์ให้เกิดความกลัวแล้วหลอกให้โอนเงิน",
                            "9.หลอกลวงให้ติดตั้งโปรแกรมควบคุมระบบในเครื่องโทรศัพท์",
                            "10.กระทำต่อระบบหรือข้อมูลคอมพิวเตอร์โดยผิดกฎหมาย (Hacking) เพื่อฉ้อโกง กรรโชก หรือรีดเอาทรัพย์",
                            "11.เข้ารหัสข้อมูลคอมพิวเตอร์ของผู้อื่นโดยมิชอบเพื่อกรรโชก หรือรีดเอาทรัพย์ (Ransomware)",
                            "12. หลอกลวงให้ลงทุนผ่านระบบคอมพิวเตอร์",
                            "13.หลอกลวงเกี่ยวกับสินทรัพย์ดิจิทัล",
                            "14.หลอกลวงซื้อขายสินค้าหรือบริการ ที่มีลักษณะเป็นขบวนการ",
                            "15.หลอกลวงให้ลงทุนที่เป็นความผิดตาม พ.ร.ก.กู้ยืมเงินฯ",
                            "16.คดีอาชญากรรมทางเทคโนโลยีทางลักษณะอื่นๆ"
                        ]
                        entry['values'] = case_types
                else:  # entry
                    entry = ttk.Entry(field_frame, width=50, font=('Arial', 10))
                    if key == "doc_number":
                        # ใส่ค่าเริ่มต้นสำหรับเลขที่หนังสือ
                        entry.insert(0, "ตช. 0039.52/")
                
                entry.pack(side='left', fill='x', expand=True)
                self.summons_entries[key] = entry
        
        # ปุ่มจัดการ
        button_frame = ttk.Frame(scrollable_frame)
        button_frame.pack(pady=30)
        
        save_btn = ttk.Button(button_frame, text="💾 บันทึกข้อมูลหมายเรียก", 
                             command=self.save_summons_data)
        save_btn.pack(side='left', padx=10)
        
        police_search_btn = ttk.Button(button_frame, text="🔍 ค้นหาข้อมูลสถานีตำรวจ", 
                                     command=self.search_police_station)
        police_search_btn.pack(side='left', padx=10)
        
        clear_btn = ttk.Button(button_frame, text="🗑️ ล้างข้อมูล", 
                              command=self.clear_summons_entries)
        clear_btn.pack(side='left', padx=10)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def create_summons_view_tab(self):
        """สร้างแท็บดูข้อมูลหมายเรียกผู้ต้องหา"""
        view_frame = ttk.Frame(self.notebook)
        self.notebook.add(view_frame, text="👁️ ดูข้อมูล ผตห.")
        
        # หัวข้อและปุ่ม
        top_frame = ttk.Frame(view_frame)
        top_frame.pack(fill='x', padx=20, pady=10)
        
        title = ttk.Label(top_frame, text="ข้อมูลหมายเรียกผู้ต้องหาทั้งหมด", 
                         font=('Arial', 16, 'bold'))
        title.pack(side='left')
        
        # ปุ่มจัดการ
        btn_frame = ttk.Frame(top_frame)
        btn_frame.pack(side='right')
        
        ttk.Button(btn_frame, text="🔄 รีเฟรช", 
                  command=self.refresh_summons_data).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="✏️ แก้ไข", 
                  command=self.edit_summons_selected).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="🗑️ ลบ", 
                  command=self.delete_summons_selected).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="📋 คัดลอก", 
                  command=self.copy_summons_selected).pack(side='left', padx=2)
        ttk.Button(btn_frame, text="💾 บันทึก Excel", 
                  command=self.save_summons_excel).pack(side='left', padx=2)
        
        # ตารางข้อมูล
        tree_frame = ttk.Frame(view_frame)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # Treeview สำหรับหมายเรียก
        self.summons_tree = ttk.Treeview(tree_frame)
        
        # Scrollbars
        summons_v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", 
                                           command=self.summons_tree.yview)
        summons_h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", 
                                           command=self.summons_tree.xview)
        
        self.summons_tree.configure(yscrollcommand=summons_v_scrollbar.set,
                                   xscrollcommand=summons_h_scrollbar.set)
        
        # Pack scrollbars และ treeview
        summons_v_scrollbar.pack(side="right", fill="y")
        summons_h_scrollbar.pack(side="bottom", fill="x")
        self.summons_tree.pack(fill="both", expand=True)
        
        # โหลดและแสดงข้อมูลจากไฟล์ Excel ทันที
        self.update_summons_treeview()
    
    def update_summons_treeview(self):
        """อัพเดทตารางแสดงข้อมูลหมายเรียก"""
        if not GUI_AVAILABLE or not hasattr(self, 'summons_tree'):
            return
            
        # ล้างข้อมูลเก่า
        for item in self.summons_tree.get_children():
            self.summons_tree.delete(item)
        
        # ตรวจสอบว่ามีข้อมูลหรือไม่
        if self.use_pandas:
            if self.summons_data is None or self.summons_data.empty:
                return
            columns = list(self.summons_data.columns)
            data_rows = self.summons_data.values.tolist()
        else:
            if not self.summons_data_headers or not self.summons_data_rows:
                return
            columns = self.summons_data_headers
            data_rows = self.summons_data_rows
        
        # ตั้งค่าคอลัมน์
        self.summons_tree['columns'] = columns
        self.summons_tree['show'] = 'headings'
        
        # ตั้งค่าหัวข้อ
        for col in columns:
            self.summons_tree.heading(col, text=col)
            self.summons_tree.column(col, width=120, minwidth=80)
        
        # กำหนดสีสำหรับแถวที่ตอบกลับแล้ว
        self.summons_tree.tag_configure('replied', foreground='green')
        
        # เพิ่มข้อมูล
        for row in data_rows:
            if self.use_pandas:
                try:
                    import pandas as pd
                    values = [str(val) if pd.notna(val) else "" for val in row]
                except:
                    values = [str(val) if val else "" for val in row]
            else:
                values = [str(val) if val else "" for val in row]
            
            # ตรวจสอบว่าแถวนี้ตอบกลับแล้วหรือไม่
            tags = ()
            if "ตอบกลับ" in columns:
                replied_index = columns.index("ตอบกลับ")
                if replied_index < len(values) and str(values[replied_index]).strip().upper() == "X":
                    tags = ('replied',)
            
            self.summons_tree.insert('', 'end', values=values, tags=tags)
    
    def save_summons_data(self):
        """บันทึกข้อมูลหมายเรียกใหม่ลงไฟล์เดิม"""
        try:
            # รวบรวมข้อมูลจากฟอร์ม
            form_data = {}
            for key, widget in self.summons_entries.items():
                if isinstance(widget, tk.Text):
                    value = widget.get("1.0", tk.END).strip()
                else:
                    value = widget.get().strip()
                form_data[key] = value
            
            # แมพข้อมูลกับคอลัมน์ไฟล์เดิม
            column_mapping = {
                'doc_number': 'เลขที่หนังสือ',
                'doc_date': 'ลงวันที่',
                'suspect_name': 'ชื่อ ผตห.',
                'suspect_id': 'เลขประจำตัว ปชช. ผตห.',
                'police_station': 'สภ.พื้นที่รับผิดชอบ',
                'police_province': 'จังหวัด สภ.พื้นที่รับผิดชอบ',
                'victim_name': 'ชื่อผู้เสียหาย',
                'case_type': 'ประเภทคดี',
                'damage_amount': 'ความเสียหาย',
                'case_id': 'เลขเคสไอดี',
                'suspect_address': 'ที่อยู่ ผตห.',
                'appointment_date': 'กำหนดให้มาพบ',
                'police_address': 'ที่อยู่ สภ. พื้นที่รับผิดชอบ'
            }
            
            # สร้างแถวข้อมูลใหม่ตามโครงสร้างไฟล์เดิม
            if self.use_pandas and self.summons_data is not None:
                # ใช้ pandas
                excel_columns = list(self.summons_data.columns)
                new_row_data = {}
                
                for form_key, excel_col in column_mapping.items():
                    if excel_col in excel_columns:
                        value = form_data.get(form_key, '')
                        # ลบตัวเลขลำดับออกจากประเภทคดี
                        if form_key == 'case_type' and value:
                            # ลบตัวเลขและจุดออกจากหน้าข้อความ เช่น "1.คดีไม่เข้า พรก." -> "คดีไม่เข้า พรก."
                            import re
                            value = re.sub(r'^\d+\.', '', value).strip()
                        new_row_data[excel_col] = value
                
                # เพิ่มข้อมูลใหม่
                import pandas as pd
                new_row = pd.DataFrame([new_row_data])
                self.summons_data = pd.concat([self.summons_data, new_row], ignore_index=True)
                
                # บันทึกลงไฟล์ Excel ทันที
                self.summons_data.to_excel(self.summons_file, index=False)
                
            else:
                # ไม่ใช้ pandas - ใช้วิธีอื่น
                if self.summons_data_headers:
                    new_row = []
                    for header in self.summons_data_headers:
                        # หาข้อมูลที่ตรงกับหัวข้อ
                        value = ''
                        for form_key, excel_col in column_mapping.items():
                            if excel_col == header:
                                value = form_data.get(form_key, '')
                                # ลบตัวเลขลำดับออกจากประเภทคดี
                                if form_key == 'case_type' and value:
                                    # ลบตัวเลขและจุดออกจากหน้าข้อความ เช่น "1.คดีไม่เข้า พรก." -> "คดีไม่เข้า พรก."
                                    import re
                                    value = re.sub(r'^\d+\.', '', value).strip()
                                break
                        new_row.append(value)
                    
                    # เพิ่มข้อมูลใหม่
                    self.summons_data_rows.append(new_row)
                    
                    # บันทึกลงไฟล์ Excel ด้วยวิธีพิเศษ
                    self.save_summons_to_excel_direct()
            
            # รีโหลดข้อมูลและอัพเดทตาราง
            self.load_summons_data()
            
            # ล้างฟิลด์และตั้งค่าใหม่
            self.clear_summons_entries()
            
            messagebox.showinfo("สำเร็จ", f"บันทึกข้อมูลหมายเรียกลงไฟล์ {self.summons_file} เรียบร้อย")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกข้อมูลหมายเรียก: {str(e)}")
            print(f"รายละเอียดข้อผิดพลาดการบันทึกหมายเรียก: {e}")
    
    def save_summons_to_excel_direct(self):
        """บันทึกข้อมูลหมายเรียกลงไฟล์ Excel โดยตรง (ไม่ใช้ pandas)"""
        try:
            # ใช้ Excel writer ที่เขียนเอง
            success = self.write_excel_file(self.summons_file, self.summons_data_headers, self.summons_data_rows)
            
            if not success:
                # ถ้าไม่สำเร็จ ลองใช้วิธี CSV + LibreOffice
                print("ลองใช้วิธี CSV สำรองสำหรับหมายเรียก")
                
        except Exception as e:
            print(f"เกิดข้อผิดพลาดในการบันทึกหมายเรียก Excel: {e}")
    
    def clear_summons_entries(self):
        """ล้างฟิลด์ข้อมูลหมายเรียก"""
        for key, widget in self.summons_entries.items():
            if isinstance(widget, tk.Text):
                widget.delete("1.0", tk.END)
            else:
                widget.delete(0, tk.END)
                # ตั้งค่าวันที่ใหม่สำหรับฟิลด์วันที่
                if key in ["doc_date", "appointment_date"]:
                    from datetime import datetime
                    today = datetime.now().strftime("%d/%m/%Y")
                    widget.insert(0, today)
    
    def search_police_station(self):
        """ค้นหาข้อมูลสถานีตำรวจจากที่อยู่ผู้ต้องหา"""
        try:
            # ตรวจสอบว่ามีการกรอกที่อยู่ผู้ต้องหาหรือไม่
            if 'suspect_address' not in self.summons_entries:
                messagebox.showwarning("คำเตือน", "ไม่พบช่องที่อยู่ผู้ต้องหา")
                return
            
            suspect_address_widget = self.summons_entries['suspect_address']
            if isinstance(suspect_address_widget, tk.Text):
                suspect_address = suspect_address_widget.get("1.0", tk.END).strip()
            else:
                suspect_address = suspect_address_widget.get().strip()
            
            if not suspect_address:
                messagebox.showwarning("คำเตือน", "กรุณากรอกที่อยู่ของผู้ต้องหาก่อนค้นหาสถานีตำรวจ")
                return
            
            # แสดง loading message
            if GUI_AVAILABLE:
                # สร้างหน้าต่าง loading
                loading_window = tk.Toplevel()
                loading_window.title("กำลังค้นหา...")
                loading_window.geometry("300x100")
                loading_window.resizable(False, False)
                loading_window.transient(self.root)
                loading_window.grab_set()
                
                # จัดให้อยู่กึ่งกลางหน้าจอ
                loading_window.update_idletasks()
                x = (loading_window.winfo_screenwidth() // 2) - (300 // 2)
                y = (loading_window.winfo_screenheight() // 2) - (100 // 2)
                loading_window.geometry(f"300x100+{x}+{y}")
                
                loading_label = ttk.Label(loading_window, text="🔍 กำลังค้นหาสถานีตำรวจ...", 
                                        font=('Arial', 12))
                loading_label.pack(expand=True)
                
                # อัพเดท GUI
                loading_window.update()
            
            print(f"กำลังค้นหาสถานีตำรวจสำหรับที่อยู่: {suspect_address}")
            
            # ขั้นตอน 1: Geocoding ที่อยู่
            location_data = geocode_address(suspect_address)
            
            if not location_data:
                if GUI_AVAILABLE:
                    loading_window.destroy()
                messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถหาตำแหน่งของที่อยู่ที่ระบุได้\nกรุณาตรวจสอบความถูกต้องของที่อยู่")
                return
            
            print(f"พบตำแหน่ง: {location_data['lat']}, {location_data['lon']}")
            
            # ขั้นตอน 2: ค้นหาสถานีตำรวจใกล้เคียง
            stations = find_nearby_police_stations(location_data['lat'], location_data['lon'])
            
            if GUI_AVAILABLE:
                loading_window.destroy()
            
            if not stations:
                messagebox.showwarning("ไม่พบข้อมูล", "ไม่พบสถานีตำรวจในพื้นที่ใกล้เคียง\nกรุณาเพิ่มข้อมูลด้วยตนเอง")
                return
            
            # ขั้นตอน 3: แสดงผลและให้เลือก
            self.show_police_station_selection(stations, location_data.get('province'))
            
        except Exception as e:
            if GUI_AVAILABLE and 'loading_window' in locals():
                loading_window.destroy()
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการค้นหา: {str(e)}")
            print(f"Error in search_police_station: {e}")
    
    def show_police_station_selection(self, stations, province):
        """แสดงหน้าต่างให้เลือกสถานีตำรวจ"""
        if not GUI_AVAILABLE:
            return
            
        # สร้างหน้าต่างเลือกสถานีตำรวจ
        selection_window = tk.Toplevel()
        selection_window.title("เลือกสถานีตำรวจ")
        selection_window.geometry("600x400")
        selection_window.resizable(True, True)
        selection_window.transient(self.root)
        selection_window.grab_set()
        
        # จัดให้อยู่กึ่งกลางหน้าจอ
        selection_window.update_idletasks()
        x = (selection_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (selection_window.winfo_screenheight() // 2) - (400 // 2)
        selection_window.geometry(f"600x400+{x}+{y}")
        
        # หัวข้อ
        title_label = ttk.Label(selection_window, text="เลือกสถานีตำรวจที่ใกล้ที่สุด", 
                               font=('Arial', 14, 'bold'))
        title_label.pack(pady=10)
        
        # ตารางแสดงสถานีตำรวจ
        tree_frame = ttk.Frame(selection_window)
        tree_frame.pack(fill='both', expand=True, padx=20, pady=10)
        
        # สร้าง Treeview
        columns = ('ชื่อสถานี', 'ระยะทาง (กม.)')
        tree = ttk.Treeview(tree_frame, columns=columns, show='headings', height=8)
        
        # กำหนดหัวข้อ
        tree.heading('ชื่อสถานี', text='ชื่อสถานี')
        tree.heading('ระยะทาง (กม.)', text='ระยะทาง (กม.)')
        
        # กำหนดความกว้างคอลัมน์
        tree.column('ชื่อสถานี', width=400)
        tree.column('ระยะทาง (กม.)', width=150)
        
        # เพิ่มข้อมูลสถานีตำรวจ
        for i, station in enumerate(stations):
            distance_km = round(station['distance'] / 1000, 2)
            tree.insert('', 'end', values=(station['name'], f"{distance_km} กม."))
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        tree.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')
        
        # ปุ่มจัดการ
        button_frame = ttk.Frame(selection_window)
        button_frame.pack(pady=20)
        
        def select_station():
            selection = tree.selection()
            if not selection:
                messagebox.showwarning("คำเตือน", "กรุณาเลือกสถานีตำรวจ")
                return
            
            # หาข้อมูลสถานีที่เลือก
            selected_index = tree.index(selection[0])
            selected_station = stations[selected_index]
            
            # กรอกข้อมูลลงในฟอร์ม
            self.fill_police_station_data(selected_station, province)
            
            selection_window.destroy()
            messagebox.showinfo("สำเร็จ", "กรอกข้อมูลสถานีตำรวจเรียบร้อย")
        
        select_btn = ttk.Button(button_frame, text="✅ เลือกสถานีนี้", command=select_station)
        select_btn.pack(side='left', padx=10)
        
        cancel_btn = ttk.Button(button_frame, text="❌ ยกเลิก", command=selection_window.destroy)
        cancel_btn.pack(side='left', padx=10)
        
        # เลือกแถวแรกโดยอัตโนมัติ
        if tree.get_children():
            tree.selection_set(tree.get_children()[0])
            tree.focus(tree.get_children()[0])
    
    def fill_police_station_data(self, station, province):
        """กรอกข้อมูลสถานีตำรวจลงในฟอร์ม"""
        try:
            # กรอกชื่อสถานีตำรวจ
            if 'police_station' in self.summons_entries:
                police_station_widget = self.summons_entries['police_station']
                police_station_widget.delete(0, tk.END)
                police_station_widget.insert(0, station['name'])
            
            # กรอกจังหวัด
            if 'police_province' in self.summons_entries and province:
                police_province_widget = self.summons_entries['police_province']
                police_province_widget.delete(0, tk.END)
                police_province_widget.insert(0, province)
            
            # ค้นหาและกรอกที่อยู่สถานีตำรวจ
            if 'police_address' in self.summons_entries:
                station_address = get_police_station_address(station['name'], province or 'ไม่ระบุ')
                police_address_widget = self.summons_entries['police_address']
                
                if isinstance(police_address_widget, tk.Text):
                    police_address_widget.delete("1.0", tk.END)
                    police_address_widget.insert("1.0", station_address)
                else:
                    police_address_widget.delete(0, tk.END)
                    police_address_widget.insert(0, station_address)
            
            print(f"กรอกข้อมูลสถานีตำรวจ: {station['name']} ในจังหวัด{province}")
            
        except Exception as e:
            print(f"Error filling police station data: {e}")
            messagebox.showerror("ข้อผิดพลาด", f"เกิดข้อผิดพลาดในการกรอกข้อมูล: {str(e)}")
    
    # เพิ่มฟังก์ชันอื่นๆ สำหรับหมายเรียก
    def refresh_summons_data(self):
        """รีเฟรชข้อมูลหมายเรียก"""
        self.load_summons_data()
    
    def edit_summons_selected(self):
        """แก้ไขข้อมูลหมายเรียกที่เลือก"""
        try:
            if not hasattr(self, 'summons_tree'):
                return
                
            selected_item = self.summons_tree.selection()
            if not selected_item:
                messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกข้อมูลที่ต้องการแก้ไข")
                return
            
            # ดึงข้อมูลที่เลือก
            row_values = self.summons_tree.item(selected_item[0])['values']
            
            # สร้างหน้าต่างแก้ไข
            edit_window = tk.Toplevel(self.root)
            edit_window.title("แก้ไขข้อมูลหมายเรียกผู้ต้องหา")
            edit_window.geometry("700x600")
            edit_window.resizable(True, True)
            
            # สร้าง main frame
            main_frame = ttk.Frame(edit_window)
            main_frame.pack(fill='both', expand=True, padx=10, pady=10)
            
            # สร้าง canvas สำหรับ scroll
            canvas = tk.Canvas(main_frame)
            scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
            scrollable_frame = ttk.Frame(canvas)
            
            scrollable_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
            
            canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
            canvas.configure(yscrollcommand=scrollbar.set)
            
            # หัวข้อ
            title_label = ttk.Label(scrollable_frame, text="แก้ไขข้อมูลหมายเรียกผู้ต้องหา", 
                                   font=('Arial', 14, 'bold'))
            title_label.pack(pady=10)
            
            # สร้างฟิลด์แก้ไข
            edit_entries = {}
            
            # รายการคอลัมน์และชื่อฟิลด์
            column_field_mapping = {
                'เลขที่หนังสือ': ('doc_number', 'entry'),
                'ลงวันที่': ('doc_date', 'entry'),
                'ชื่อ ผตห.': ('suspect_name', 'entry'),
                'เลขประจำตัว ปชช. ผตห.': ('suspect_id', 'entry'),
                'สภ.พื้นที่รับผิดชอบ': ('police_station', 'entry'),
                'จังหวัด สภ.พื้นที่รับผิดชอบ': ('police_province', 'entry'),
                'ชื่อผู้เสียหาย': ('victim_name', 'entry'),
                'ประเภทคดี': ('case_type', 'dropdown'),
                'ความเสียหาย': ('damage_amount', 'entry'),
                'เลขเคสไอดี': ('case_id', 'entry'),
                'ที่อยู่ ผตห.': ('suspect_address', 'text'),
                'กำหนดให้มาพบ': ('appointment_date', 'entry'),
                'ที่อยู่ สภ. พื้นที่รับผิดชอบ': ('police_address', 'text')
            }
            
            # สร้างฟิลด์สำหรับแต่ละคอลัมน์
            columns = self.summons_data_headers if not self.use_pandas else list(self.summons_data.columns)
            
            for i, column in enumerate(columns):
                if column in column_field_mapping:
                    field_key, field_type = column_field_mapping[column]
                    
                    field_frame = ttk.Frame(scrollable_frame)
                    field_frame.pack(fill='x', padx=20, pady=3)
                    
                    label = ttk.Label(field_frame, text=column, width=25, font=('Arial', 10))
                    label.pack(side='left', padx=(0, 10))
                    
                    if field_type == 'text':
                        entry = tk.Text(field_frame, height=3, width=50, font=('Arial', 10))
                    elif field_type == 'dropdown':
                        entry = ttk.Combobox(field_frame, width=47, font=('Arial', 10), state="readonly")
                        if field_key == 'case_type':
                            # รายการประเภทคดี
                            case_types = [
                                "1.คดีไม่เข้า พรก.",
                                "2.หลอกลวงซื้อขายสินค้าหรือบริการ ที่ไม่มีลักษณะเป็นขบวนการ",
                                "3.หลอกลวงเป็นบุคคลอื่นเพื่อยืมเงิน",
                                "4.หลอกลวงให้รักแล้วโอนเงิน (Romance Scam)",
                                "5.หลอกลวงให้โอนเงินเพื่อรับรางวัลหรือวัตถุประสงค์อื่นๆ",
                                "6.หลอกลวงให้กู้เงินอันมีลักษณะฉ้อโกง กรรโชก หรือรีดเอาทรัพย์",
                                "7.หลอกลวงให้โอนเงินเพื่อทำงานหารายได้พิเศษ",
                                "8.ข่มขู่ทางโทรศัพท์ให้เกิดความกลัวแล้วหลอกให้โอนเงิน",
                                "9.หลอกลวงให้ติดตั้งโปรแกรมควบคุมระบบในเครื่องโทรศัพท์",
                                "10.กระทำต่อระบบหรือข้อมูลคอมพิวเตอร์โดยผิดกฎหมาย (Hacking) เพื่อฉ้อโกง กรรโชก หรือรีดเอาทรัพย์",
                                "11.เข้ารหัสข้อมูลคอมพิวเตอร์ของผู้อื่นโดยมิชอบเพื่อกรรโชก หรือรีดเอาทรัพย์ (Ransomware)",
                                "12. หลอกลวงให้ลงทุนผ่านระบบคอมพิวเตอร์",
                                "13.หลอกลวงเกี่ยวกับสินทรัพย์ดิจิทัล",
                                "14.หลอกลวงซื้อขายสินค้าหรือบริการ ที่มีลักษณะเป็นขบวนการ",
                                "15.หลอกลวงให้ลงทุนที่เป็นความผิดตาม พ.ร.ก.กู้ยืมเงินฯ",
                                "16.คดีอาชญากรรมทางเทคโนโลยีทางลักษณะอื่นๆ"
                            ]
                            entry['values'] = case_types
                    else:
                        entry = ttk.Entry(field_frame, width=50, font=('Arial', 10))
                    
                    entry.pack(side='left', fill='x', expand=True)
                    
                    # ใส่ค่าเดิม
                    if i < len(row_values):
                        if field_type == 'text':
                            entry.insert("1.0", str(row_values[i]))
                        elif field_type == 'dropdown':
                            # สำหรับ dropdown ใช้ set()
                            entry.set(str(row_values[i]))
                        else:
                            # ตรวจสอบว่าเป็นช่องกำหนดให้มาพบหรือไม่
                            if field_key == 'appointment_date' and (not row_values[i] or str(row_values[i]).strip() == '' or str(row_values[i]) == 'nan'):
                                # ใส่ค่าเริ่มต้นเป็นวันปัจจุบัน + 7 วัน ในรูปแบบไทย
                                default_date = get_default_appointment_date()
                                thai_formatted_date = format_thai_date(default_date)
                                entry.insert(0, thai_formatted_date)
                            else:
                                entry.insert(0, str(row_values[i]))
                    else:
                        # กรณีไม่มีข้อมูลเดิม
                        if field_key == 'appointment_date':
                            # ใส่ค่าเริ่มต้นเป็นวันปัจจุบัน + 7 วัน ในรูปแบบไทย
                            default_date = get_default_appointment_date()
                            thai_formatted_date = format_thai_date(default_date)
                            if field_type == 'text':
                                entry.insert("1.0", thai_formatted_date)
                            else:
                                entry.insert(0, thai_formatted_date)
                    
                    edit_entries[field_key] = entry
            
            # Frame สำหรับปุ่ม (อยู่นอก scrollable area)
            button_main_frame = ttk.Frame(main_frame)
            button_main_frame.pack(side='bottom', fill='x', pady=(15, 0))
            
            # เพิ่ม checkbox สำหรับ "ตอบกลับ"
            replied_frame = ttk.Frame(button_main_frame)
            replied_frame.pack(pady=5)
            
            replied_var = tk.BooleanVar()
            # ตรวจสอบสถานะปัจจุบันจากคอลัมน์ "ตอบกลับ" หากมี
            replied_status = ""
            if "ตอบกลับ" in columns:
                replied_col_index = columns.index("ตอบกลับ")
                if replied_col_index < len(row_values):
                    replied_status = str(row_values[replied_col_index]) if row_values[replied_col_index] else ""
            
            replied_var.set(replied_status.strip().upper() == "X")
            
            replied_checkbox = ttk.Checkbutton(
                replied_frame, 
                text="ได้รับข้อมูลตอบกลับแล้ว", 
                variable=replied_var,
                style="TCheckbutton"
            )
            replied_checkbox.pack(pady=5)
            
            btn_frame = ttk.Frame(button_main_frame)
            btn_frame.pack()
            
            def save_changes():
                try:
                    # อัพเดทข้อมูล
                    selected_index = self.summons_tree.index(selected_item[0])
                    
                    # รวบรวมข้อมูลใหม่
                    updated_values = []
                    for column in columns:
                        if column in column_field_mapping:
                            field_key, field_type = column_field_mapping[column]
                            if field_key in edit_entries:
                                widget = edit_entries[field_key]
                                if field_type == 'text':
                                    value = widget.get("1.0", tk.END).strip()
                                else:
                                    value = widget.get().strip()
                                # ลบตัวเลขลำดับออกจากประเภทคดี
                                if field_key == 'case_type' and value:
                                    # ลบตัวเลขและจุดออกจากหน้าข้อความ เช่น "1.คดีไม่เข้า พรก." -> "คดีไม่เข้า พรก."
                                    import re
                                    value = re.sub(r'^\d+\.', '', value).strip()
                                updated_values.append(value)
                            else:
                                updated_values.append("")
                        else:
                            updated_values.append("")
                    
                    # จัดการคอลัมน์ "ตอบกลับ"
                    replied_value = "X" if replied_var.get() else ""
                    
                    # เพิ่มคอลัมน์ "ตอบกลับ" ถ้ายังไม่มี
                    if "ตอบกลับ" not in columns:
                        columns.append("ตอบกลับ")
                        if hasattr(self, 'summons_data_headers'):
                            self.summons_data_headers.append("ตอบกลับ")
                        updated_values.append(replied_value)
                        
                        # เพิ่มคอลัมน์ว่างให้ทุกแถวที่มีอยู่
                        if self.use_pandas and self.summons_data is not None:
                            self.summons_data["ตอบกลับ"] = ""
                        else:
                            for i in range(len(self.summons_data_rows)):
                                self.summons_data_rows[i].append("")
                    else:
                        # อัพเดทค่า "ตอบกลับ" ในตำแหน่งที่ถูกต้อง
                        replied_col_index = columns.index("ตอบกลับ")
                        if replied_col_index < len(updated_values):
                            updated_values[replied_col_index] = replied_value
                        else:
                            # ขยาง list ถ้าจำเป็น
                            while len(updated_values) <= replied_col_index:
                                updated_values.append("")
                            updated_values[replied_col_index] = replied_value
                    
                    # อัพเดทข้อมูลในโครงสร้าง
                    if self.use_pandas and self.summons_data is not None:
                        # อัพเดท DataFrame
                        for i, column in enumerate(columns):
                            if i < len(updated_values):
                                self.summons_data.iloc[selected_index, i] = updated_values[i]
                        
                        # บันทึกลงไฟล์
                        self.summons_data.to_excel(self.summons_file, index=False)
                    else:
                        # อัพเดทข้อมูลแบบไม่ใช้ pandas
                        if selected_index < len(self.summons_data_rows):
                            self.summons_data_rows[selected_index] = updated_values
                            # บันทึกลงไฟล์
                            self.save_summons_to_excel_direct()
                    
                    # รีเฟรชตาราง
                    self.update_summons_treeview()
                    edit_window.destroy()
                    messagebox.showinfo("สำเร็จ", "แก้ไขข้อมูลหมายเรียกเรียบร้อย")
                    
                except Exception as e:
                    messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถแก้ไขข้อมูล: {str(e)}")
            
            # ปุ่มบันทึกและยกเลิก
            save_btn = ttk.Button(btn_frame, text="💾 บันทึกการแก้ไข", command=save_changes)
            save_btn.pack(side='left', padx=10)
            
            cancel_btn = ttk.Button(btn_frame, text="❌ ยกเลิก", command=edit_window.destroy)
            cancel_btn.pack(side='left', padx=10)
            
            # Pack canvas และ scrollbar
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # รองรับ mouse wheel
            def _on_mousewheel(event):
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            canvas.bind_all("<MouseWheel>", _on_mousewheel)
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถเปิดหน้าต่างแก้ไข: {str(e)}")
    
    def delete_summons_selected(self):
        """ลบข้อมูลหมายเรียกที่เลือก"""
        try:
            if not hasattr(self, 'summons_tree'):
                return
                
            selected_item = self.summons_tree.selection()
            if not selected_item:
                messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกข้อมูลที่ต้องการลบ")
                return
            
            # ยืนยันการลบ
            result = messagebox.askyesno("ยืนยันการลบ", 
                                       "คุณต้องการลบข้อมูลหมายเรียกนี้หรือไม่?\nการดำเนินการนี้ไม่สามารถยกเลิกได้")
            if not result:
                return
            
            # หาตำแหน่งของข้อมูลที่เลือก
            selected_index = self.summons_tree.index(selected_item[0])
            
            # ลบข้อมูล
            if self.use_pandas and self.summons_data is not None:
                # ใช้ pandas
                self.summons_data = self.summons_data.drop(self.summons_data.index[selected_index]).reset_index(drop=True)
                
                # บันทึกลงไฟล์
                self.summons_data.to_excel(self.summons_file, index=False)
            else:
                # ไม่ใช้ pandas
                if selected_index < len(self.summons_data_rows):
                    del self.summons_data_rows[selected_index]
                    
                    # บันทึกลงไฟล์
                    self.save_summons_to_excel_direct()
            
            # รีเฟรชตาราง
            self.update_summons_treeview()
            messagebox.showinfo("สำเร็จ", "ลบข้อมูลหมายเรียกเรียบร้อย")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถลบข้อมูล: {str(e)}")
    
    def copy_summons_selected(self):
        """คัดลอกข้อมูลหมายเรียกที่เลือก"""
        try:
            if not hasattr(self, 'summons_tree'):
                return
                
            selected_item = self.summons_tree.selection()
            if not selected_item:
                messagebox.showwarning("แจ้งเตือน", "กรุณาเลือกข้อมูลที่ต้องการคัดลอก")
                return
            
            # ดึงข้อมูลที่เลือก
            row_values = self.summons_tree.item(selected_item[0])['values']
            
            # สร้างข้อมูลใหม่ (คัดลอก)
            new_row = list(row_values)
            
            # เพิ่มข้อมูลใหม่
            if self.use_pandas and self.summons_data is not None:
                # ใช้ pandas
                columns = list(self.summons_data.columns)
                new_row_dict = {}
                
                for i, column in enumerate(columns):
                    if i < len(new_row):
                        new_row_dict[column] = new_row[i]
                    else:
                        new_row_dict[column] = ""
                
                # เพิ่มข้อมูลใหม่
                import pandas as pd
                new_row_df = pd.DataFrame([new_row_dict])
                self.summons_data = pd.concat([self.summons_data, new_row_df], ignore_index=True)
                
                # บันทึกลงไฟล์
                self.summons_data.to_excel(self.summons_file, index=False)
            else:
                # ไม่ใช้ pandas
                # เพิ่มข้อมูลใหม่
                self.summons_data_rows.append(new_row)
                
                # บันทึกลงไฟล์
                self.save_summons_to_excel_direct()
            
            # รีเฟรชตาราง
            self.update_summons_treeview()
            messagebox.showinfo("สำเร็จ", "คัดลอกข้อมูลหมายเรียกเรียบร้อย")
            
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถคัดลอกข้อมูล: {str(e)}")
    
    def save_summons_excel(self):
        """บันทึกข้อมูลหมายเรียกลง Excel"""
        try:
            # บันทึกลงไฟล์ ข้อมูลสำหรับออกหมายเรียกผู้ต้องหา.xlsx ใน path ปัจจุบัน
            filename = os.path.join(os.getcwd(), "ข้อมูลสำหรับออกหมายเรียกผู้ต้องหา.xlsx")
            
            if filename:
                if self.use_pandas and self.summons_data is not None:
                    # ใช้ pandas
                    self.summons_data.to_excel(filename, index=False)
                else:
                    # ไม่ใช้ pandas - ใช้วิธีเขียน Excel ด้วยตนเอง
                    success = self.write_excel_file(filename, self.summons_data_headers, self.summons_data_rows)
                    if not success:
                        messagebox.showerror("ข้อผิดพลาด", "ไม่สามารถบันทึกไฟล์ Excel ได้")
                        return
                
                messagebox.showinfo("สำเร็จ", f"บันทึกไฟล์ข้อมูลหมายเรียก {filename} เรียบร้อย")
                
        except Exception as e:
            messagebox.showerror("ข้อผิดพลาด", f"ไม่สามารถบันทึกไฟล์: {str(e)}")

def main():
    """ฟังก์ชันหลัก"""
    print("=== Excel Data Manager ===")
    
    if not GUI_AVAILABLE:
        print("⚠️  GUI ไม่พร้อมใช้งาน - รันในโหมด Command Line")
        print("กรุณาติดตั้ง dependencies สำหรับ GUI:")
        print("python3 install_dependencies.py")
        print("หรือติดตั้งแบบแยก: pip install pandas openpyxl")
        print()
    
    app = SimpleExcelManager()
    if GUI_AVAILABLE:
        app.run()
    else:
        print("โปรแกรมเริ่มต้นแล้ว - ข้อมูลจะถูกโหลดในพื้นหลัง")
        print("สามารถใช้งานผ่าน GUI ได้เมื่อติดตั้ง dependencies เรียบร้อยแล้ว")

if __name__ == "__main__":
    main()