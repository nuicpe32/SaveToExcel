#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Excel Reader - อ่านข้อมูลจากไฟล์ Excel โดยไม่ต้องใช้ pandas
"""

import zipfile
import xml.etree.ElementTree as ET
import os

def read_excel_basic(filename):
    """อ่านข้อมูลพื้นฐานจากไฟล์ Excel"""
    try:
        if not os.path.exists(filename):
            print(f"ไม่พบไฟล์ {filename}")
            return None, None
        
        # ไฟล์ Excel เป็น ZIP file
        with zipfile.ZipFile(filename, 'r') as zip_file:
            # อ่าน shared strings
            shared_strings = []
            try:
                with zip_file.open('xl/sharedStrings.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    # namespace สำหรับ Excel
                    ns = {'ss': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    
                    for si in root.findall('.//ss:si', ns):
                        t = si.find('.//ss:t', ns)
                        if t is not None:
                            shared_strings.append(t.text or '')
                        else:
                            shared_strings.append('')
            except:
                print("ไม่สามารถอ่าน shared strings ได้")
            
            # อ่านข้อมูลจาก worksheet
            try:
                with zip_file.open('xl/worksheets/sheet1.xml') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    
                    ns = {'ss': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
                    
                    rows_data = []
                    for row in root.findall('.//ss:row', ns):
                        row_data = []
                        for cell in row.findall('.//ss:c', ns):
                            value = ""
                            
                            # ตรวจสอบประเภทของ cell
                            t_attr = cell.get('t')
                            v_elem = cell.find('.//ss:v', ns)
                            
                            if v_elem is not None:
                                if t_attr == 's':  # shared string
                                    idx = int(v_elem.text)
                                    if idx < len(shared_strings):
                                        value = shared_strings[idx]
                                else:
                                    value = v_elem.text or ""
                            
                            row_data.append(value)
                        
                        if row_data:  # เพิ่มเฉพาะแถวที่มีข้อมูล
                            rows_data.append(row_data)
                    
                    if rows_data:
                        headers = rows_data[0] if rows_data else []
                        data_rows = rows_data[1:] if len(rows_data) > 1 else []
                        return headers, data_rows
                    
            except Exception as e:
                print(f"ไม่สามารถอ่าน worksheet: {e}")
        
        return None, None
        
    except Exception as e:
        print(f"ไม่สามารถอ่านไฟล์ Excel: {e}")
        return None, None

def display_excel_data(filename):
    """แสดงข้อมูลจากไฟล์ Excel"""
    print(f"=== อ่านข้อมูลจาก {filename} ===")
    
    headers, rows = read_excel_basic(filename)
    
    if headers and rows:
        print(f"จำนวนคอลัมน์: {len(headers)}")
        print(f"จำนวนแถวข้อมูล: {len(rows)}")
        
        print("\n=== หัวข้อคอลัมน์ ===")
        for i, header in enumerate(headers, 1):
            print(f"{i:2d}. {header}")
        
        print(f"\n=== ข้อมูล 5 แถวแรก ===")
        for i, row in enumerate(rows[:5], 1):
            print(f"แถว {i}:")
            for j, (header, value) in enumerate(zip(headers, row)):
                print(f"  {header}: {value}")
            print()
        
        return headers, rows
    else:
        print("ไม่สามารถอ่านข้อมูลได้")
        return None, None

def main():
    """ทดสอบการอ่านไฟล์"""
    filename = "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"
    display_excel_data(filename)

if __name__ == "__main__":
    main()