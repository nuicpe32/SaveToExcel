#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check database data for case 1174/2568
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine

def check_database_data():
    """Check database data for case 1174/2568"""
    print("=== Checking Database Data for Case 1174/2568 ===")
    
    try:
        with engine.connect() as conn:
            # 1. Check criminal cases
            print("\n1. Checking criminal cases...")
            result = conn.execute(text("SELECT id, case_number, complainant, case_id FROM criminal_cases WHERE case_number = '1174/2568'"))
            case = result.fetchone()
            
            if case:
                case_id, case_number, complainant, case_id_field = case
                print(f"   ✅ Found case: ID={case_id}, Case Number={case_number}, Complainant='{complainant}', CaseID='{case_id_field}'")
                
                # 2. Check bank accounts by criminal_case_id
                print(f"\n2. Checking bank accounts by criminal_case_id={case_id}...")
                bank_result = conn.execute(text("SELECT COUNT(*) FROM bank_accounts WHERE criminal_case_id = %s"), (case_id,))
                bank_count = bank_result.fetchone()[0]
                print(f"   Bank accounts by criminal_case_id: {bank_count}")
                
                # 3. Check bank accounts by complainant
                print(f"\n3. Checking bank accounts by complainant='{complainant}'...")
                bank_complainant_result = conn.execute(text("SELECT COUNT(*) FROM bank_accounts WHERE complainant = %s"), (complainant,))
                bank_complainant_count = bank_complainant_result.fetchone()[0]
                print(f"   Bank accounts by complainant: {bank_complainant_count}")
                
                if bank_complainant_count > 0:
                    # Show sample bank accounts
                    bank_sample = conn.execute(text("SELECT document_number, complainant, victim_name, reply_status FROM bank_accounts WHERE complainant = %s LIMIT 3"), (complainant,))
                    print("   Sample bank accounts:")
                    for row in bank_sample:
                        print(f"      Doc: {row[0]}, Complainant: {row[1]}, Victim: {row[2]}, Replied: {row[3]}")
                
                # 4. Check suspects by criminal_case_id
                print(f"\n4. Checking suspects by criminal_case_id={case_id}...")
                suspect_result = conn.execute(text("SELECT COUNT(*) FROM suspects WHERE criminal_case_id = %s"), (case_id,))
                suspect_count = suspect_result.fetchone()[0]
                print(f"   Suspects by criminal_case_id: {suspect_count}")
                
                # 5. Check suspects by complainant
                print(f"\n5. Checking suspects by complainant='{complainant}'...")
                suspect_complainant_result = conn.execute(text("SELECT COUNT(*) FROM suspects WHERE complainant = %s"), (complainant,))
                suspect_complainant_count = suspect_complainant_result.fetchone()[0]
                print(f"   Suspects by complainant: {suspect_complainant_count}")
                
                if suspect_complainant_count > 0:
                    # Show sample suspects
                    suspect_sample = conn.execute(text("SELECT document_number, complainant, victim_name, reply_status FROM suspects WHERE complainant = %s LIMIT 3"), (complainant,))
                    print("   Sample suspects:")
                    for row in suspect_sample:
                        print(f"      Doc: {row[0]}, Complainant: {row[1]}, Victim: {row[2]}, Replied: {row[3]}")
                
            else:
                print("   ❌ Case 1174/2568 not found in database")
                
                # Show all available cases
                print("\n   Available cases:")
                all_cases = conn.execute(text("SELECT case_number, complainant FROM criminal_cases ORDER BY case_number LIMIT 10"))
                for row in all_cases:
                    print(f"      {row[0]}: {row[1]}")
                
                # Check if there are any cases with 1174 in the case number
                case_1174_like = conn.execute(text("SELECT case_number, complainant FROM criminal_cases WHERE case_number LIKE '%1174%'"))
                case_1174_like_rows = case_1174_like.fetchall()
                if case_1174_like_rows:
                    print("\n   Cases containing '1174':")
                    for row in case_1174_like_rows:
                        print(f"      {row[0]}: {row[1]}")
                
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_database_data()
