#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Demo: แสดงวิธีการทำงานของโปรแกรม Excel Data Manager
"""

import os
import zipfile
import xml.etree.ElementTree as ET

class ExcelDataDemo:
    def __init__(self):
        self.excel_file = "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"
        self.data_headers = []
        self.data_rows = []
        
    def read_excel_direct(self):
        """อ่านไฟล์ Excel โดยตรง"""
        try:
            with zipfile.ZipFile(self.excel_file, 'r') as zip_file:
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
                                if t_attr == 's':
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
                        self.data_headers = rows_data[0] if rows_data else []
                        self.data_rows = rows_data[1:] if len(rows_data) > 1 else []
                        return True
            
            return False
        except Exception as e:
            print(f"Error reading Excel: {e}")
            return False
    
    def display_summary(self):
        """แสดงสรุปข้อมูล"""
        print("="*80)
        print("🔥 EXCEL DATA MANAGER - แสดงข้อมูลจากไฟล์ Excel")
        print("="*80)
        
        if not self.data_headers or not self.data_rows:
            print("❌ ไม่มีข้อมูลให้แสดง")
            return
        
        print(f"📊 สถิติข้อมูล:")
        print(f"   • จำนวนคอลัมน์: {len(self.data_headers)}")
        print(f"   • จำนวนแถวข้อมูล: {len(self.data_rows)}")
        
        print(f"\n📋 ฟิลด์ทั้งหมด:")
        for i, header in enumerate(self.data_headers, 1):
            print(f"   {i:2d}. {header}")
        
        print(f"\n📈 ข้อมูลล่าสุด 5 แถว:")
        key_cols = [0, 1, 6, 9, 11]  # ลำดับ, เลขหนังสือ, ผู้เสียหาย, ชื่อธนาคาร, ชื่อบัญชี
        
        # แสดงหัวข้อ
        for col_idx in key_cols:
            if col_idx < len(self.data_headers):
                print(f"{self.data_headers[col_idx]:<20}", end=" | ")
        print()
        print("-" * 110)
        
        # แสดงข้อมูล 5 แถวล่าสุด
        recent_rows = self.data_rows[-5:] if len(self.data_rows) >= 5 else self.data_rows
        for row in recent_rows:
            for col_idx in key_cols:
                if col_idx < len(row):
                    value = str(row[col_idx])[:18]
                    print(f"{value:<20}", end=" | ")
            print()
    
    def simulate_gui_features(self):
        """จำลองฟีเจอร์ GUI"""
        print(f"\n🎯 ฟีเจอร์ที่พร้อมใช้งานใน GUI:")
        
        features = [
            "✅ แสดงข้อมูลทั้งหมด 269 แถว ในตาราง",
            "✅ กรอกข้อมูลใหม่ด้วยฟอร์มที่จัดกลุ่มเป็นหมวดหมู่",
            "✅ แก้ไขข้อมูลโดยเลือกแถวและคลิกปุ่มแก้ไข",
            "✅ ลบข้อมูลที่ไม่ต้องการ",
            "✅ คัดลอกแถวข้อมูลเพื่อสร้างรายการใหม่",
            "✅ บันทึกข้อมูลใหม่ต่อจากแถวเดิม (แถวที่ 270, 271, ...)",
            "✅ ส่งออกข้อมูลเป็นไฟล์ Excel ใหม่",
            "✅ ลำดับสร้างอัตโนมัติ (ต่อจาก 269)",
            "✅ หน้าจอทันสมัย เรียบง่าย ใช้งานง่าย"
        ]
        
        for feature in features:
            print(f"   {feature}")
        
        print(f"\n💡 วิธีเปิดใช้งาน:")
        print(f"   1. ติดตั้ง dependencies: python3 install_dependencies.py")
        print(f"   2. รันโปรแกรม: python3 simple_excel_manager.py")
        print(f"   3. ใช้งานผ่าน GUI ที่แสดงข้อมูลทั้งหมดทันที")
        
        print(f"\n🔧 โครงสร้างข้อมูลที่รองรับ:")
        groups = [
            ("📋 ข้อมูลหนังสือ", ["ลำดับ", "เลขหนังสือ", "วัน", "เดือน", "ปี"]),
            ("🏦 ข้อมูลธนาคาร", ["ธนาคารสาขา", "ชื่อธนาคาร", "เลขบัญชี", "ชื่อบัญชี", "เจ้าของบัญชีม้า"]),
            ("👤 ข้อมูลผู้เกี่ยวข้อง", ["ผู้เสียหาย", "เคสไอดี", "ช่วงเวลา"]),
            ("📍 ที่อยู่ธนาคาร", ["ที่อยู่ธนาคาร", "ซอย", "หมู่", "ตำบล/แขวง", "อำเภอ/เขต", "ถนน", "จังหวัด", "รหัสไปรษณี"]),
            ("📅 ข้อมูลการส่ง", ["วันนัดส่ง", "เดือนส่ง", "เวลาส่ง"])
        ]
        
        for group_name, fields in groups:
            print(f"\n   {group_name}")
            for field in fields:
                print(f"     • {field}")

def main():
    """ฟังก์ชันหลัก"""
    demo = ExcelDataDemo()
    
    if demo.read_excel_direct():
        demo.display_summary()
        demo.simulate_gui_features()
    else:
        print("❌ ไม่สามารถอ่านไฟล์ Excel ได้")

if __name__ == "__main__":
    main()