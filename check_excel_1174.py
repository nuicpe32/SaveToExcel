#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check Excel data for case 1174/2568
"""

import pandas as pd
import os

def check_excel_data():
    """Check Excel data for case 1174/2568"""
    excel_dir = "Xlsx"
    
    print("=== Checking Excel Data for Case 1174/2568 ===")
    
    # 1. Check criminal cases file
    print("\n1. Checking criminal cases file...")
    try:
        criminal_file = os.path.join(excel_dir, "export_คดีอาญาในความรับผิดชอบ.xlsx")
        if os.path.exists(criminal_file):
            df = pd.read_excel(criminal_file)
            print(f"   File: {criminal_file}")
            print(f"   Total rows: {len(df)}")
            print(f"   Columns: {list(df.columns)}")
            
            # Look for case 1174
            case_1174 = df[df.iloc[:, 2].astype(str).str.contains('1174', na=False)]
            if len(case_1174) > 0:
                print(f"   ✅ Found case 1174/2568:")
                row = case_1174.iloc[0]
                print(f"      Case Number: {row.iloc[2]}")
                print(f"      Complainant: {row.iloc[5]}")
                print(f"      Status: {row.iloc[3]}")
            else:
                print(f"   ❌ Case 1174/2568 not found")
                
                # Show sample data
                print("   Sample cases:")
                for i in range(min(5, len(df))):
                    case_num = df.iloc[i, 2] if len(df.columns) > 2 else 'N/A'
                    complainant = df.iloc[i, 5] if len(df.columns) > 5 else 'N/A'
                    print(f"      {i+1}. {case_num}: {complainant}")
        else:
            print(f"   ❌ File not found: {criminal_file}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 2. Check bank accounts file
    print("\n2. Checking bank accounts file...")
    try:
        bank_file = os.path.join(excel_dir, "หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx")
        if os.path.exists(bank_file):
            df = pd.read_excel(bank_file)
            print(f"   File: {bank_file}")
            print(f"   Total rows: {len(df)}")
            print(f"   Columns: {list(df.columns)}")
            
            # Look for case 1174 in any column
            case_1174_found = False
            for col_idx in range(min(5, len(df.columns))):
                case_1174 = df[df.iloc[:, col_idx].astype(str).str.contains('1174', na=False)]
                if len(case_1174) > 0:
                    print(f"   ✅ Found bank accounts for case 1174 in column {col_idx}:")
                    for idx, row in case_1174.iterrows():
                        print(f"      Row {idx}: {dict(row)}")
                    case_1174_found = True
                    break
            
            if not case_1174_found:
                print(f"   ❌ No bank accounts found for case 1174")
                
                # Show sample data
                print("   Sample bank accounts:")
                for i in range(min(3, len(df))):
                    row_data = {}
                    for j in range(min(5, len(df.columns))):
                        row_data[df.columns[j]] = df.iloc[i, j]
                    print(f"      {i+1}. {row_data}")
        else:
            print(f"   ❌ File not found: {bank_file}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # 3. Check suspects file
    print("\n3. Checking suspects file...")
    try:
        suspect_file = os.path.join(excel_dir, "ข้อมูลสำหรับออกหมายเรียกผู้ต้องหา.xlsx")
        if os.path.exists(suspect_file):
            df = pd.read_excel(suspect_file)
            print(f"   File: {suspect_file}")
            print(f"   Total rows: {len(df)}")
            print(f"   Columns: {list(df.columns)}")
            
            # Look for case 1174 in any column
            case_1174_found = False
            for col_idx in range(min(5, len(df.columns))):
                case_1174 = df[df.iloc[:, col_idx].astype(str).str.contains('1174', na=False)]
                if len(case_1174) > 0:
                    print(f"   ✅ Found suspects for case 1174 in column {col_idx}:")
                    for idx, row in case_1174.iterrows():
                        print(f"      Row {idx}: {dict(row)}")
                    case_1174_found = True
                    break
            
            if not case_1174_found:
                print(f"   ❌ No suspects found for case 1174")
                
                # Show sample data
                print("   Sample suspects:")
                for i in range(min(3, len(df))):
                    row_data = {}
                    for j in range(min(5, len(df.columns))):
                        row_data[df.columns[j]] = df.iloc[i, j]
                    print(f"      {i+1}. {row_data}")
        else:
            print(f"   ❌ File not found: {suspect_file}")
    except Exception as e:
        print(f"   ❌ Error: {e}")

if __name__ == "__main__":
    check_excel_data()
