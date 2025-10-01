#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Clean database structure by removing redundant columns
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine

def clean_database_structure():
    """Clean database structure by removing redundant columns"""
    print("=" * 80)
    print("🧹 ทำความสะอาดโครงสร้างฐานข้อมูล")
    print("=" * 80)
    
    try:
        with engine.connect() as conn:
            # 1. Move data from redundant columns to criminal_cases before dropping
            print("\n1. ย้ายข้อมูลจากคอลัมน์ซ้ำซ้อนไปยัง criminal_cases...")
            
            # Move victim_name from bank_accounts to criminal_cases
            print("   📋 ย้าย victim_name จาก bank_accounts...")
            conn.execute(text("""
                UPDATE criminal_cases 
                SET victim_name = ba.victim_name
                FROM bank_accounts ba 
                WHERE criminal_cases.id = ba.criminal_case_id 
                AND criminal_cases.victim_name IS NULL 
                AND ba.victim_name IS NOT NULL
            """))
            
            # Move victim_name from suspects to criminal_cases
            print("   📋 ย้าย victim_name จาก suspects...")
            conn.execute(text("""
                UPDATE criminal_cases 
                SET victim_name = s.victim_name
                FROM suspects s 
                WHERE criminal_cases.id = s.criminal_case_id 
                AND criminal_cases.victim_name IS NULL 
                AND s.victim_name IS NOT NULL
            """))
            
            # Move case_number from post_arrests to criminal_cases (if needed)
            print("   📋 ย้าย case_number จาก post_arrests...")
            conn.execute(text("""
                UPDATE criminal_cases 
                SET case_number = pa.case_number
                FROM post_arrests pa 
                WHERE criminal_cases.id = pa.criminal_case_id 
                AND criminal_cases.case_number IS NULL 
                AND pa.case_number IS NOT NULL
            """))
            
            # Move accuser_name from post_arrests to criminal_cases
            print("   📋 ย้าย accuser_name จาก post_arrests...")
            conn.execute(text("""
                UPDATE criminal_cases 
                SET complainant = pa.accuser_name
                FROM post_arrests pa 
                WHERE criminal_cases.id = pa.criminal_case_id 
                AND criminal_cases.complainant IS NULL 
                AND pa.accuser_name IS NOT NULL
            """))
            
            # Move crime_scene from post_arrests to criminal_cases
            print("   📋 ย้าย crime_scene จาก post_arrests...")
            conn.execute(text("""
                UPDATE criminal_cases 
                SET case_scene = pa.crime_scene
                FROM post_arrests pa 
                WHERE criminal_cases.id = pa.criminal_case_id 
                AND criminal_cases.case_scene IS NULL 
                AND pa.crime_scene IS NOT NULL
            """))
            
            # Move damage_amount from post_arrests to criminal_cases
            print("   📋 ย้าย damage_amount จาก post_arrests...")
            conn.execute(text("""
                UPDATE criminal_cases 
                SET damage_amount = pa.damage_amount
                FROM post_arrests pa 
                WHERE criminal_cases.id = pa.criminal_case_id 
                AND criminal_cases.damage_amount IS NULL 
                AND pa.damage_amount IS NOT NULL
            """))
            
            conn.commit()
            print("   ✅ ย้ายข้อมูลเสร็จสิ้น")
            
            # 2. Drop redundant columns
            print("\n2. ลบคอลัมน์ซ้ำซ้อน...")
            
            # Drop columns from bank_accounts
            print("   🗑️ ลบคอลัมน์จาก bank_accounts...")
            try:
                conn.execute(text("ALTER TABLE bank_accounts DROP COLUMN IF EXISTS complainant"))
                print("      ✅ ลบ complainant จาก bank_accounts")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ complainant จาก bank_accounts: {e}")
            
            try:
                conn.execute(text("ALTER TABLE bank_accounts DROP COLUMN IF EXISTS victim_name"))
                print("      ✅ ลบ victim_name จาก bank_accounts")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ victim_name จาก bank_accounts: {e}")
            
            # Drop columns from suspects
            print("   🗑️ ลบคอลัมน์จาก suspects...")
            try:
                conn.execute(text("ALTER TABLE suspects DROP COLUMN IF EXISTS complainant"))
                print("      ✅ ลบ complainant จาก suspects")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ complainant จาก suspects: {e}")
            
            try:
                conn.execute(text("ALTER TABLE suspects DROP COLUMN IF EXISTS victim_name"))
                print("      ✅ ลบ victim_name จาก suspects")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ victim_name จาก suspects: {e}")
            
            # Drop columns from post_arrests
            print("   🗑️ ลบคอลัมน์จาก post_arrests...")
            try:
                conn.execute(text("ALTER TABLE post_arrests DROP COLUMN IF EXISTS case_number"))
                print("      ✅ ลบ case_number จาก post_arrests")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ case_number จาก post_arrests: {e}")
            
            try:
                conn.execute(text("ALTER TABLE post_arrests DROP COLUMN IF EXISTS accuser_name"))
                print("      ✅ ลบ accuser_name จาก post_arrests")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ accuser_name จาก post_arrests: {e}")
            
            try:
                conn.execute(text("ALTER TABLE post_arrests DROP COLUMN IF EXISTS crime_scene"))
                print("      ✅ ลบ crime_scene จาก post_arrests")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ crime_scene จาก post_arrests: {e}")
            
            try:
                conn.execute(text("ALTER TABLE post_arrests DROP COLUMN IF EXISTS damage_amount"))
                print("      ✅ ลบ damage_amount จาก post_arrests")
            except Exception as e:
                print(f"      ⚠️ ไม่สามารถลบ damage_amount จาก post_arrests: {e}")
            
            conn.commit()
            print("   ✅ ลบคอลัมน์เสร็จสิ้น")
            
            # 3. Update models to reflect the changes
            print("\n3. อัพเดท Models...")
            print("   ⚠️ ต้องอัพเดท Models ด้วยตนเอง:")
            print("      - ลบ complainant, victim_name จาก BankAccount model")
            print("      - ลบ complainant, victim_name จาก Suspect model")
            print("      - ลบ case_number, accuser_name, crime_scene, damage_amount จาก PostArrest model")
            
            # 4. Update API logic
            print("\n4. อัพเดท API Logic...")
            print("   ⚠️ ต้องอัพเดท API Logic ด้วยตนเอง:")
            print("      - ลบ logic ที่ใช้ complainant matching")
            print("      - ใช้เฉพาะ Foreign Key relationships")
            
            # 5. Show final statistics
            print("\n5. สถิติสุดท้าย:")
            result = conn.execute(text("SELECT COUNT(*) FROM criminal_cases"))
            print(f"   📋 Criminal Cases: {result.fetchone()[0]:,} คดี")
            
            result = conn.execute(text("SELECT COUNT(*) FROM bank_accounts"))
            print(f"   🏦 Bank Accounts: {result.fetchone()[0]:,} บัญชี")
            
            result = conn.execute(text("SELECT COUNT(*) FROM suspects"))
            print(f"   👤 Suspects: {result.fetchone()[0]:,} คน")
            
            result = conn.execute(text("SELECT COUNT(*) FROM post_arrests"))
            print(f"   🚔 Post Arrests: {result.fetchone()[0]:,} รายการ")
            
            print(f"\n{'=' * 80}")
            print("✅ ทำความสะอาดโครงสร้างฐานข้อมูลเสร็จสิ้น!")
            print("⚠️  ต้องอัพเดท Models และ API Logic ด้วยตนเอง")
            print(f"{'=' * 80}")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()
        conn.rollback()

if __name__ == "__main__":
    clean_database_structure()
