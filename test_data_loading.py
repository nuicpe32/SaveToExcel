#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ทดสอบการโหลดข้อมูลจากไฟล์ Excel
"""

import os
import sys
import zipfile
import xml.etree.ElementTree as ET

def read_excel_direct(filename):
    """อ่านไฟล์ Excel โดยตรง"""
    try:
        with zipfile.ZipFile(filename, 'r') as zip_file:
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
        print(f"Error reading Excel directly: {e}")
        return None, None

def test_simple_data_display():
    """ทดสอบการแสดงข้อมูลแบบง่าย"""
    filename = "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"
    
    print("=== ทดสอบการโหลดข้อมูลสำหรับ GUI ===")
    
    if not os.path.exists(filename):
        print(f"ไม่พบไฟล์ {filename}")
        return
    
    headers, rows = read_excel_direct(filename)
    
    if headers and rows:
        print(f"✅ โหลดข้อมูลสำเร็จ")
        print(f"   - จำนวนคอลัมน์: {len(headers)}")
        print(f"   - จำนวนแถว: {len(rows)}")
        
        # แสดงหัวข้อ 10 คอลัมน์แรก
        print("\n📋 หัวข้อคอลัมน์ (10 คอลัมน์แรก):")
        for i, header in enumerate(headers[:10], 1):
            print(f"   {i:2d}. {header}")
        
        if len(headers) > 10:
            print(f"   ... และอีก {len(headers) - 10} คอลัมน์")
        
        # แสดงข้อมูล 3 แถวแรก (บางคอลัมน์)
        print(f"\n📊 ตัวอย่างข้อมูล (3 แถวแรก):")
        key_columns = [0, 1, 6, 9, 10, 11]  # ลำดับ, เลขหนังสือ, ผู้เสียหาย, ชื่อธนาคาร, เลขบัญชี, ชื่อบัญชี
        
        for col_idx in key_columns:
            if col_idx < len(headers):
                print(f"   {headers[col_idx]:<20}", end=" | ")
        print()
        print("   " + "-" * 100)
        
        for i, row in enumerate(rows[:3], 1):
            print(f"{i:2d}:", end=" ")
            for col_idx in key_columns:
                if col_idx < len(row):
                    value = str(row[col_idx])[:18]  # จำกัดความยาว
                    print(f"{value:<20}", end=" | ")
            print()
        
        print(f"\n✨ พร้อมสำหรับแสดงใน GUI")
        return True
    else:
        print("❌ ไม่สามารถโหลดข้อมูลได้")
        return False

if __name__ == "__main__":
    test_simple_data_display()