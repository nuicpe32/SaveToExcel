#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relink bank accounts and suspects to criminal cases
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine, SessionLocal
from app.models.criminal_case import CriminalCase
from app.models.bank_account import BankAccount
from app.models.suspect import Suspect

def clean_name(name):
    """Clean name for matching"""
    if not name:
        return ""
    # Remove common prefixes
    prefixes = ['นาย', 'นาง', 'น.ส.', 'นางสาว', 'ด.ช.', 'ด.ญ.']
    name_cleaned = name.strip()
    for prefix in prefixes:
        if name_cleaned.startswith(prefix):
            name_cleaned = name_cleaned[len(prefix):].strip()
    # Remove spaces and dots
    return name_cleaned.replace(' ', '').replace('.', '')

def relink_data():
    """Relink bank accounts and suspects to criminal cases"""
    print("=== Relinking Data ===")
    
    db = SessionLocal()
    
    try:
        # 1. Get all criminal cases
        print("\n1. Loading criminal cases...")
        criminal_cases = db.query(CriminalCase).all()
        print(f"   Found {len(criminal_cases)} criminal cases")
        
        # Create a mapping of cleaned complainant names to case IDs
        complainant_to_case = {}
        for case in criminal_cases:
            if case.complainant:
                cleaned_name = clean_name(case.complainant)
                if cleaned_name not in complainant_to_case:
                    complainant_to_case[cleaned_name] = []
                complainant_to_case[cleaned_name].append(case)
        
        print(f"   Created mapping for {len(complainant_to_case)} unique complainants")
        
        # 2. Link bank accounts
        print("\n2. Linking bank accounts...")
        bank_accounts = db.query(BankAccount).all()
        linked_banks = 0
        
        for account in bank_accounts:
            if account.complainant:
                cleaned_name = clean_name(account.complainant)
                
                # Try exact match first
                if cleaned_name in complainant_to_case:
                    cases = complainant_to_case[cleaned_name]
                    account.criminal_case_id = cases[0].id
                    linked_banks += 1
                else:
                    # Try partial match
                    for key, cases in complainant_to_case.items():
                        if cleaned_name in key or key in cleaned_name:
                            account.criminal_case_id = cases[0].id
                            linked_banks += 1
                            break
        
        db.commit()
        print(f"   ✅ Linked {linked_banks} bank accounts")
        
        # 3. Link suspects
        print("\n3. Linking suspects...")
        suspects = db.query(Suspect).all()
        linked_suspects = 0
        
        for suspect in suspects:
            complainant = suspect.complainant or suspect.victim_name
            if complainant:
                cleaned_name = clean_name(complainant)
                
                # Try exact match first
                if cleaned_name in complainant_to_case:
                    cases = complainant_to_case[cleaned_name]
                    suspect.criminal_case_id = cases[0].id
                    linked_suspects += 1
                else:
                    # Try partial match
                    for key, cases in complainant_to_case.items():
                        if cleaned_name in key or key in cleaned_name:
                            suspect.criminal_case_id = cases[0].id
                            linked_suspects += 1
                            break
        
        db.commit()
        print(f"   ✅ Linked {linked_suspects} suspects")
        
        # 4. Check case 1174/2568
        print("\n4. Checking case 1174/2568...")
        case_1174 = db.query(CriminalCase).filter(CriminalCase.case_number == '1174/2568').first()
        if case_1174:
            print(f"   ✅ Found case: ID={case_1174.id}, Complainant='{case_1174.complainant}'")
            
            # Count linked bank accounts
            bank_count = db.query(BankAccount).filter(BankAccount.criminal_case_id == case_1174.id).count()
            print(f"   Bank accounts linked by criminal_case_id: {bank_count}")
            
            # Count linked suspects
            suspect_count = db.query(Suspect).filter(Suspect.criminal_case_id == case_1174.id).count()
            print(f"   Suspects linked by criminal_case_id: {suspect_count}")
            
            # Count by complainant
            bank_count_by_complainant = db.query(BankAccount).filter(BankAccount.complainant == case_1174.complainant).count()
            print(f"   Bank accounts by complainant: {bank_count_by_complainant}")
            
            suspect_count_by_complainant = db.query(Suspect).filter(Suspect.complainant == case_1174.complainant).count()
            print(f"   Suspects by complainant: {suspect_count_by_complainant}")
        else:
            print("   ❌ Case 1174/2568 not found")
        
        print("\n✅ Relinking completed!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    relink_data()
