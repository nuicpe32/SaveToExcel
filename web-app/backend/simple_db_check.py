#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simple database structure check
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine

def simple_db_check():
    """Simple database check"""
    print("=== Database Structure Check ===")
    
    try:
        with engine.connect() as conn:
            # 1. List tables
            print("\n1. Tables:")
            result = conn.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name"))
            for row in result:
                print(f"   - {row[0]}")
            
            # 2. Check criminal_cases structure
            print("\n2. Criminal Cases Columns:")
            result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'criminal_cases' ORDER BY ordinal_position"))
            for row in result:
                print(f"   - {row[0]}: {row[1]}")
            
            # 3. Check bank_accounts structure
            print("\n3. Bank Accounts Columns:")
            result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'bank_accounts' ORDER BY ordinal_position"))
            for row in result:
                print(f"   - {row[0]}: {row[1]}")
            
            # 4. Check suspects structure
            print("\n4. Suspects Columns:")
            result = conn.execute(text("SELECT column_name, data_type FROM information_schema.columns WHERE table_name = 'suspects' ORDER BY ordinal_position"))
            for row in result:
                print(f"   - {row[0]}: {row[1]}")
            
            # 5. Check foreign keys
            print("\n5. Foreign Keys:")
            result = conn.execute(text("""
                SELECT 
                    tc.table_name, 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu ON ccu.constraint_name = tc.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY' AND tc.table_name IN ('bank_accounts', 'suspects')
            """))
            for row in result:
                print(f"   - {row[0]}.{row[1]} -> {row[2]}.{row[3]}")
            
            # 6. Check data counts
            print("\n6. Data Counts:")
            result = conn.execute(text("SELECT COUNT(*) FROM criminal_cases"))
            print(f"   - Criminal Cases: {result.fetchone()[0]}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM bank_accounts"))
            print(f"   - Bank Accounts: {result.fetchone()[0]}")
            
            result = conn.execute(text("SELECT COUNT(*) FROM suspects"))
            print(f"   - Suspects: {result.fetchone()[0]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    simple_db_check()
