#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
วิเคราะห์ข้อมูลธนาคารจากไฟล์เดิม
"""

import zipfile
import xml.etree.ElementTree as ET
from collections import defaultdict

def read_excel_data():
    """อ่านข้อมูลจากไฟล์ Excel"""
    filename = "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"
    
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
                    headers = rows_data[0]
                    data_rows = rows_data[1:]
                    return headers, data_rows
        
        return None, None
    except Exception as e:
        print(f"Error: {e}")
        return None, None

def analyze_bank_data():
    """วิเคราะห์ข้อมูลธนาคาร"""
    headers, rows = read_excel_data()
    
    if not headers or not rows:
        print("ไม่สามารถอ่านข้อมูลได้")
        return
    
    # หาตำแหน่งคอลัมน์ที่ต้องการ
    bank_branch_col = -1
    bank_name_col = -1
    address_col = -1
    soi_col = -1
    moo_col = -1
    tambon_col = -1
    amphoe_col = -1
    road_col = -1
    province_col = -1
    postal_col = -1
    
    for i, header in enumerate(headers):
        if 'ธนาคารสาขา' in header:
            bank_branch_col = i
        elif 'ชื่อธนาคาร' in header:
            bank_name_col = i
        elif 'ที่อยู่ธนาคาร' in header:
            address_col = i
        elif 'ซอย' in header:
            soi_col = i
        elif 'หมู่' in header:
            moo_col = i
        elif 'ตำบล' in header or 'แขวง' in header:
            tambon_col = i
        elif 'อำเภอ' in header or 'เขต' in header:
            amphoe_col = i
        elif 'ถนน' in header:
            road_col = i
        elif 'จังหวัด' in header:
            province_col = i
        elif 'รหัสไปรษณี' in header:
            postal_col = i
    
    # เก็บข้อมูลธนาคาร
    bank_branches = set()
    bank_names = set()
    bank_address_map = {}
    
    for row in rows:
        if len(row) > max(bank_branch_col, bank_name_col, address_col):
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
                if address_col >= 0 and len(row) > address_col:
                    address_data['address'] = row[address_col] or ""
                if soi_col >= 0 and len(row) > soi_col:
                    address_data['soi'] = row[soi_col] or ""
                if moo_col >= 0 and len(row) > moo_col:
                    address_data['moo'] = row[moo_col] or ""
                if tambon_col >= 0 and len(row) > tambon_col:
                    address_data['tambon'] = row[tambon_col] or ""
                if amphoe_col >= 0 and len(row) > amphoe_col:
                    address_data['amphoe'] = row[amphoe_col] or ""
                if road_col >= 0 and len(row) > road_col:
                    address_data['road'] = row[road_col] or ""
                if province_col >= 0 and len(row) > province_col:
                    address_data['province'] = row[province_col] or ""
                if postal_col >= 0 and len(row) > postal_col:
                    address_data['postal'] = row[postal_col] or ""
                
                bank_address_map[key] = address_data
    
    # แสดงผลการวิเคราะห์
    print("="*80)
    print("📊 การวิเคราะห์ข้อมูลธนาคารจากไฟล์เดิม")
    print("="*80)
    
    print(f"\n🏦 ธนาคารสาขา ({len(bank_branches)} รายการ):")
    for i, branch in enumerate(sorted(bank_branches), 1):
        print(f"  {i:2d}. {branch}")
    
    print(f"\n🏛️ ชื่อธนาคาร ({len(bank_names)} รายการ):")
    for i, name in enumerate(sorted(bank_names), 1):
        print(f"  {i:2d}. {name}")
    
    print(f"\n📍 ตัวอย่างการ mapping ที่อยู่ (5 รายการแรก):")
    count = 0
    for key, addr in bank_address_map.items():
        if count >= 5:
            break
        bank_branch, bank_name = key.split('|')
        print(f"\n  🔹 {bank_branch} | {bank_name}")
        print(f"     ที่อยู่: {addr.get('address', '')}")
        print(f"     ถนน: {addr.get('road', '')}")
        print(f"     ตำบล/แขวง: {addr.get('tambon', '')}")
        print(f"     อำเภอ/เขต: {addr.get('amphoe', '')}")
        print(f"     จังหวัด: {addr.get('province', '')}")
        print(f"     รหัสไปรษณี: {addr.get('postal', '')}")
        count += 1
    
    # บันทึกข้อมูลลงไฟล์ JSON
    import json
    
    bank_data = {
        'bank_branches': sorted(list(bank_branches)),
        'bank_names': sorted(list(bank_names)),
        'address_mapping': bank_address_map
    }
    
    with open('bank_data.json', 'w', encoding='utf-8') as f:
        json.dump(bank_data, f, ensure_ascii=False, indent=2)
    
    print(f"\n💾 บันทึกข้อมูลลงไฟล์ bank_data.json แล้ว")
    print(f"📊 สรุป: {len(bank_branches)} สาขา, {len(bank_names)} ธนาคาร, {len(bank_address_map)} การ mapping")

if __name__ == "__main__":
    analyze_bank_data()