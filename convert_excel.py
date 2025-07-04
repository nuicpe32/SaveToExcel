#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
สคริปต์แปลงไฟล์ Excel เป็น CSV เพื่อดูข้อมูล
"""

import subprocess
import os
import csv

def convert_excel_to_csv():
    """แปลงไฟล์ Excel เป็น CSV"""
    excel_file = "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx"
    csv_file = "existing_data.csv"
    
    if not os.path.exists(excel_file):
        print(f"ไม่พบไฟล์ {excel_file}")
        return False
    
    try:
        # ใช้ LibreOffice แปลง
        cmd = f'libreoffice --headless --convert-to csv --outdir . "{excel_file}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            # เปลี่ยนชื่อไฟล์ที่แปลงแล้ว
            converted_file = excel_file.replace('.xlsx', '.csv')
            if os.path.exists(converted_file):
                os.rename(converted_file, csv_file)
                print(f"แปลงไฟล์ {excel_file} เป็น {csv_file} สำเร็จ")
                return True
        
        print("ไม่สามารถแปลงด้วย LibreOffice ได้")
        return False
        
    except Exception as e:
        print(f"Error: {e}")
        return False

def read_csv_data():
    """อ่านข้อมูลจาก CSV"""
    csv_file = "existing_data.csv"
    
    if not os.path.exists(csv_file):
        print(f"ไม่พบไฟล์ {csv_file}")
        return None, None
    
    try:
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            data = list(reader)
            
        if data:
            headers = data[0]
            rows = data[1:]
            return headers, rows
        else:
            return None, None
            
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return None, None

def main():
    """ฟังก์ชันหลัก"""
    print("=== แปลงและดูข้อมูลจากไฟล์ Excel ===")
    
    # แปลงไฟล์
    if convert_excel_to_csv():
        # อ่านข้อมูล
        headers, rows = read_csv_data()
        
        if headers and rows:
            print(f"\n=== ข้อมูลในไฟล์ ===")
            print(f"จำนวนคอลัมน์: {len(headers)}")
            print(f"จำนวนแถว: {len(rows)}")
            
            print("\nหัวข้อคอลัมน์:")
            for i, header in enumerate(headers, 1):
                print(f"{i:2d}. {header}")
            
            if rows:
                print(f"\nตัวอย่างข้อมูล (5 แถวแรก):")
                for i, row in enumerate(rows[:5], 1):
                    print(f"แถว {i}: {row}")
        else:
            print("ไม่มีข้อมูลในไฟล์")
    else:
        print("ไม่สามารถแปลงไฟล์ได้")

if __name__ == "__main__":
    main()