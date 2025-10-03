#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Relink data using Foreign Key relationships only
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine, SessionLocal
from app.models.criminal_case import CriminalCase
from app.models.bank_account import BankAccount
from app.models.suspect import Suspect
from app.models.post_arrest import PostArrest

def relink_data_fk_only():
    """Relink data using Foreign Key relationships only"""
    print("=" * 80)
    print("🔗 เชื่อมโยงข้อมูลใหม่โดยใช้ Foreign Key เท่านั้น")
    print("=" * 80)
    
    db = SessionLocal()
    
    try:
        # 1. Get all criminal cases
        print("\n1. โหลดข้อมูลคดีอาญา...")
        criminal_cases = db.query(CriminalCase).all()
        print(f"   พบคดีอาญา {len(criminal_cases)} คดี")
        
        # 2. Create mapping by case_number for linking
        case_number_to_id = {}
        for case in criminal_cases:
            if case.case_number:
                case_number_to_id[case.case_number] = case.id
        
        print(f"   สร้าง mapping สำหรับ {len(case_number_to_id)} เลขที่คดี")
        
        # 3. Link bank accounts by case_number matching
        print("\n2. เชื่อมโยงบัญชีธนาคาร...")
        bank_accounts = db.query(BankAccount).filter(BankAccount.criminal_case_id.is_(None)).all()
        linked_banks = 0
        
        for account in bank_accounts:
            # Try to find matching criminal case by various methods
            matching_case_id = None
            
            # Method 1: Check if document_number contains case number
            if account.document_number:
                for case_number, case_id in case_number_to_id.items():
                    if case_number in str(account.document_number):
                        matching_case_id = case_id
                        break
            
            if matching_case_id:
                account.criminal_case_id = matching_case_id
                linked_banks += 1
        
        db.commit()
        print(f"   ✅ เชื่อมโยงบัญชีธนาคาร {linked_banks} บัญชี")
        
        # 4. Link suspects by case_number matching
        print("\n3. เชื่อมโยงผู้ต้องหา...")
        suspects = db.query(Suspect).filter(Suspect.criminal_case_id.is_(None)).all()
        linked_suspects = 0
        
        for suspect in suspects:
            # Try to find matching criminal case by various methods
            matching_case_id = None
            
            # Method 1: Check if document_number contains case number
            if suspect.document_number:
                for case_number, case_id in case_number_to_id.items():
                    if case_number in str(suspect.document_number):
                        matching_case_id = case_id
                        break
            
            if matching_case_id:
                suspect.criminal_case_id = matching_case_id
                linked_suspects += 1
        
        db.commit()
        print(f"   ✅ เชื่อมโยงผู้ต้องหา {linked_suspects} คน")
        
        # 5. Link post arrests by case_number matching
        print("\n4. เชื่อมโยงข้อมูลหลังการจับกุม...")
        post_arrests = db.query(PostArrest).filter(PostArrest.criminal_case_id.is_(None)).all()
        linked_post_arrests = 0
        
        for post_arrest in post_arrests:
            # Try to find matching criminal case by suspect name or other fields
            matching_case_id = None
            
            # Method 1: Check if warrant_number contains case number
            if post_arrest.warrant_number:
                for case_number, case_id in case_number_to_id.items():
                    if case_number in str(post_arrest.warrant_number):
                        matching_case_id = case_id
                        break
            
            if matching_case_id:
                post_arrest.criminal_case_id = matching_case_id
                linked_post_arrests += 1
        
        db.commit()
        print(f"   ✅ เชื่อมโยงข้อมูลหลังการจับกุม {linked_post_arrests} รายการ")
        
        # 6. Check case 1174/2568 specifically
        print("\n5. ตรวจสอบคดี 1174/2568...")
        case_1174 = db.query(CriminalCase).filter(CriminalCase.case_number == '1174/2568').first()
        if case_1174:
            print(f"   ✅ พบคดี: ID={case_1174.id}, Case Number={case_1174.case_number}, Complainant='{case_1174.complainant}'")
            
            # Count linked bank accounts
            bank_count = db.query(BankAccount).filter(BankAccount.criminal_case_id == case_1174.id).count()
            print(f"   🏦 บัญชีธนาคารที่เชื่อมโยง: {bank_count}")
            
            # Count linked suspects
            suspect_count = db.query(Suspect).filter(Suspect.criminal_case_id == case_1174.id).count()
            print(f"   👤 ผู้ต้องหาที่เชื่อมโยง: {suspect_count}")
            
            # Show sample bank accounts
            if bank_count > 0:
                sample_banks = db.query(BankAccount).filter(BankAccount.criminal_case_id == case_1174.id).limit(3).all()
                print("   📋 ตัวอย่างบัญชีธนาคาร:")
                for bank in sample_banks:
                    print(f"      - Doc: {bank.document_number}, Bank: {bank.bank_name}, Account: {bank.account_number}")
            
            # Show sample suspects
            if suspect_count > 0:
                sample_suspects = db.query(Suspect).filter(Suspect.criminal_case_id == case_1174.id).limit(3).all()
                print("   📋 ตัวอย่างผู้ต้องหา:")
                for suspect in sample_suspects:
                    print(f"      - Doc: {suspect.document_number}, Name: {suspect.suspect_name}")
        else:
            print("   ❌ ไม่พบคดี 1174/2568")
        
        # 7. Show final statistics
        print("\n6. สถิติสุดท้าย:")
        result = conn.execute(text("SELECT COUNT(*) FROM criminal_cases"))
        print(f"   📋 Criminal Cases: {result.fetchone()[0]:,} คดี")
        
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(criminal_case_id) as linked,
                COUNT(*) - COUNT(criminal_case_id) as unlinked
            FROM bank_accounts
        """))
        bank_stats = result.fetchone()
        print(f"   🏦 Bank Accounts: {bank_stats[0]:,} บัญชี (เชื่อมโยง: {bank_stats[1]:,}, ไม่เชื่อมโยง: {bank_stats[2]:,})")
        
        result = conn.execute(text("""
            SELECT 
                COUNT(*) as total,
                COUNT(criminal_case_id) as linked,
                COUNT(*) - COUNT(criminal_case_id) as unlinked
            FROM suspects
        """))
        suspect_stats = result.fetchone()
        print(f"   👤 Suspects: {suspect_stats[0]:,} คน (เชื่อมโยง: {suspect_stats[1]:,}, ไม่เชื่อมโยง: {suspect_stats[2]:,})")
        
        print(f"\n{'=' * 80}")
        print("✅ เชื่อมโยงข้อมูลเสร็จสิ้น!")
        print(f"{'=' * 80}")
        
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    relink_data_fk_only()
