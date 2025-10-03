#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Show complete database structure
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from app.core.database import engine

def show_database_structure():
    """Show complete database structure"""
    print("=" * 80)
    print("🗄️  โครงสร้างฐานข้อมูลทั้งหมด")
    print("=" * 80)
    
    try:
        with engine.connect() as conn:
            # 1. List all tables
            print("\n📋 รายการตารางทั้งหมด:")
            result = conn.execute(text("""
                SELECT table_name, table_type 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            for row in result:
                print(f"   • {row[0]} ({row[1]})")
            
            # 2. Show detailed structure for each table
            tables = ['criminal_cases', 'bank_accounts', 'suspects', 'post_arrests', 'users']
            
            for table_name in tables:
                print(f"\n{'=' * 60}")
                print(f"📊 ตาราง: {table_name.upper()}")
                print(f"{'=' * 60}")
                
                # Get column information
                result = conn.execute(text("""
                    SELECT 
                        column_name, 
                        data_type, 
                        is_nullable,
                        column_default,
                        character_maximum_length
                    FROM information_schema.columns 
                    WHERE table_name = %s 
                    ORDER BY ordinal_position
                """), (table_name,))
                
                columns = result.fetchall()
                if columns:
                    print(f"📝 คอลัมน์ ({len(columns)} คอลัมน์):")
                    for col in columns:
                        col_name, data_type, nullable, default, max_length = col
                        nullable_str = "NULL" if nullable == "YES" else "NOT NULL"
                        length_str = f"({max_length})" if max_length else ""
                        default_str = f" DEFAULT {default}" if default else ""
                        print(f"   • {col_name}: {data_type}{length_str} {nullable_str}{default_str}")
                    
                    # Get primary key
                    result = conn.execute(text("""
                        SELECT column_name 
                        FROM information_schema.key_column_usage 
                        WHERE table_name = %s AND constraint_name LIKE '%_pkey'
                    """), (table_name,))
                    pk_columns = [row[0] for row in result.fetchall()]
                    if pk_columns:
                        print(f"🔑 Primary Key: {', '.join(pk_columns)}")
                    
                    # Get foreign keys
                    result = conn.execute(text("""
                        SELECT 
                            column_name, 
                            constraint_name,
                            (SELECT table_name FROM information_schema.constraint_column_usage 
                             WHERE constraint_name = tc.constraint_name) as referenced_table,
                            (SELECT column_name FROM information_schema.constraint_column_usage 
                             WHERE constraint_name = tc.constraint_name) as referenced_column
                        FROM information_schema.table_constraints tc
                        JOIN information_schema.key_column_usage kcu 
                            ON tc.constraint_name = kcu.constraint_name
                        WHERE tc.table_name = %s AND tc.constraint_type = 'FOREIGN KEY'
                    """), (table_name,))
                    fk_columns = result.fetchall()
                    if fk_columns:
                        print(f"🔗 Foreign Keys:")
                        for fk in fk_columns:
                            print(f"   • {fk[0]} → {fk[2]}.{fk[3]}")
                    
                    # Get indexes
                    result = conn.execute(text("""
                        SELECT indexname, indexdef 
                        FROM pg_indexes 
                        WHERE tablename = %s
                        ORDER BY indexname
                    """), (table_name,))
                    indexes = result.fetchall()
                    if indexes:
                        print(f"📇 Indexes ({len(indexes)} indexes):")
                        for idx in indexes:
                            print(f"   • {idx[0]}")
                    
                    # Get row count
                    result = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}"))
                    row_count = result.fetchone()[0]
                    print(f"📊 จำนวนแถว: {row_count:,} แถว")
                    
                    # Show sample data (first 3 rows)
                    if row_count > 0:
                        result = conn.execute(text(f"SELECT * FROM {table_name} LIMIT 3"))
                        sample_data = result.fetchall()
                        if sample_data:
                            print(f"📋 ตัวอย่างข้อมูล (3 แถวแรก):")
                            for i, row in enumerate(sample_data, 1):
                                print(f"   {i}. {dict(row)}")
                else:
                    print(f"❌ ไม่พบตาราง {table_name}")
            
            # 3. Show relationships summary
            print(f"\n{'=' * 60}")
            print("🔗 สรุปความสัมพันธ์ระหว่างตาราง")
            print(f"{'=' * 60}")
            
            result = conn.execute(text("""
                SELECT 
                    tc.table_name as from_table, 
                    kcu.column_name as from_column,
                    ccu.table_name as to_table,
                    ccu.column_name as to_column,
                    tc.constraint_name
                FROM information_schema.table_constraints tc
                JOIN information_schema.key_column_usage kcu 
                    ON tc.constraint_name = kcu.constraint_name
                JOIN information_schema.constraint_column_usage ccu 
                    ON tc.constraint_name = ccu.constraint_name
                WHERE tc.constraint_type = 'FOREIGN KEY'
                ORDER BY tc.table_name, kcu.column_name
            """))
            
            relationships = result.fetchall()
            if relationships:
                for rel in relationships:
                    print(f"   {rel[0]}.{rel[1]} → {rel[2]}.{rel[3]}")
            else:
                print("   ไม่พบ Foreign Key relationships")
            
            # 4. Show data linking statistics
            print(f"\n{'=' * 60}")
            print("📈 สถิติการเชื่อมโยงข้อมูล")
            print(f"{'=' * 60}")
            
            # Criminal cases
            result = conn.execute(text("SELECT COUNT(*) FROM criminal_cases"))
            criminal_count = result.fetchone()[0]
            print(f"📋 Criminal Cases: {criminal_count:,} คดี")
            
            # Bank accounts linking
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(criminal_case_id) as linked_by_fk,
                    COUNT(*) - COUNT(criminal_case_id) as unlinked
                FROM bank_accounts
            """))
            bank_stats = result.fetchone()
            print(f"🏦 Bank Accounts: {bank_stats[0]:,} บัญชี (เชื่อมโยง: {bank_stats[1]:,}, ไม่เชื่อมโยง: {bank_stats[2]:,})")
            
            # Suspects linking
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(criminal_case_id) as linked_by_fk,
                    COUNT(*) - COUNT(criminal_case_id) as unlinked
                FROM suspects
            """))
            suspect_stats = result.fetchone()
            print(f"👤 Suspects: {suspect_stats[0]:,} คน (เชื่อมโยง: {suspect_stats[1]:,}, ไม่เชื่อมโยง: {suspect_stats[2]:,})")
            
            # Post arrests linking
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) as total,
                    COUNT(criminal_case_id) as linked_by_fk,
                    COUNT(*) - COUNT(criminal_case_id) as unlinked
                FROM post_arrests
            """))
            post_arrest_stats = result.fetchone()
            print(f"🚔 Post Arrests: {post_arrest_stats[0]:,} รายการ (เชื่อมโยง: {post_arrest_stats[1]:,}, ไม่เชื่อมโยง: {post_arrest_stats[2]:,})")
            
            print(f"\n{'=' * 80}")
            print("✅ แสดงโครงสร้างฐานข้อมูลเสร็จสิ้น")
            print(f"{'=' * 80}")
            
    except Exception as e:
        print(f"❌ เกิดข้อผิดพลาด: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    show_database_structure()
