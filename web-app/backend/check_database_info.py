#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Check database information and connection details
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text, create_engine
from app.core.database import engine, settings

def check_database_info():
    """Check database information and connection details"""
    print("=" * 80)
    print("🗄️  ข้อมูลฐานข้อมูลและรายละเอียดการเชื่อมต่อ")
    print("=" * 80)
    
    # 1. Show connection details from settings
    print("\n📋 ข้อมูลการเชื่อมต่อ:")
    print(f"   DATABASE_URL: {settings.DATABASE_URL}")
    
    # Parse DATABASE_URL
    if settings.DATABASE_URL.startswith('postgresql://'):
        url_parts = settings.DATABASE_URL.replace('postgresql://', '').split('/')
        if len(url_parts) >= 2:
            user_pass = url_parts[0].split('@')
            if len(user_pass) >= 2:
                user_info = user_pass[0].split(':')
                host_port = user_pass[1].split(':')
                
                username = user_info[0] if user_info else 'unknown'
                password = user_info[1] if len(user_info) > 1 else 'unknown'
                host = host_port[0] if host_port else 'unknown'
                port = host_port[1] if len(host_port) > 1 else '5432'
                database = url_parts[1] if url_parts[1] else 'unknown'
                
                print(f"   Host: {host}")
                print(f"   Port: {port}")
                print(f"   Database: {database}")
                print(f"   Username: {username}")
                print(f"   Password: {password}")
    
    # 2. Test connection
    print("\n🔗 ทดสอบการเชื่อมต่อ:")
    try:
        with engine.connect() as conn:
            result = conn.execute(text("SELECT version()"))
            version = result.fetchone()[0]
            print(f"   ✅ เชื่อมต่อสำเร็จ!")
            print(f"   PostgreSQL Version: {version}")
            
            # 3. Check database name
            result = conn.execute(text("SELECT current_database()"))
            db_name = result.fetchone()[0]
            print(f"   Database Name: {db_name}")
            
            # 4. Check tables
            print("\n📊 ตารางในฐานข้อมูล:")
            result = conn.execute(text("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]
            
            if tables:
                for table in tables:
                    print(f"   📋 {table}")
                    
                    # Count rows
                    try:
                        result = conn.execute(text(f"SELECT COUNT(*) FROM {table}"))
                        count = result.fetchone()[0]
                        print(f"      └─ {count:,} แถว")
                    except Exception as e:
                        print(f"      └─ Error counting: {e}")
            else:
                print("   ❌ ไม่พบตารางใดๆ")
            
            # 5. Check specific case 1174/2568
            print("\n🔍 ตรวจสอบคดี 1174/2568:")
            try:
                result = conn.execute(text("SELECT COUNT(*) FROM criminal_cases WHERE case_number = '1174/2568'"))
                count = result.fetchone()[0]
                if count > 0:
                    print(f"   ✅ พบคดี 1174/2568 ในฐานข้อมูล")
                    
                    # Get case details
                    result = conn.execute(text("SELECT id, case_number, complainant FROM criminal_cases WHERE case_number = '1174/2568'"))
                    case = result.fetchone()
                    if case:
                        print(f"      ID: {case[0]}")
                        print(f"      Case Number: {case[1]}")
                        print(f"      Complainant: {case[2]}")
                        
                        # Check linked data
                        result = conn.execute(text("SELECT COUNT(*) FROM bank_accounts WHERE criminal_case_id = %s"), (case[0],))
                        bank_count = result.fetchone()[0]
                        print(f"      Linked Bank Accounts: {bank_count}")
                        
                        result = conn.execute(text("SELECT COUNT(*) FROM suspects WHERE criminal_case_id = %s"), (case[0],))
                        suspect_count = result.fetchone()[0]
                        print(f"      Linked Suspects: {suspect_count}")
                else:
                    print(f"   ❌ ไม่พบคดี 1174/2568 ในฐานข้อมูล")
                    
                    # Show available cases
                    result = conn.execute(text("SELECT case_number, complainant FROM criminal_cases LIMIT 5"))
                    cases = result.fetchall()
                    if cases:
                        print("   📋 คดีที่มีอยู่:")
                        for case in cases:
                            print(f"      - {case[0]}: {case[1]}")
            except Exception as e:
                print(f"   ❌ Error checking case 1174/2568: {e}")
                
    except Exception as e:
        print(f"   ❌ เชื่อมต่อไม่สำเร็จ: {e}")
        print(f"   Error details: {type(e).__name__}")
    
    # 6. Show connection summary for external tools
    print(f"\n{'=' * 80}")
    print("🔧 ข้อมูลการเชื่อมต่อสำหรับ Database Browser:")
    print(f"{'=' * 80}")
    print("Host: localhost")
    print("Port: 5432")
    print(f"Database: criminal_case_db")
    print(f"Username: user")
    print(f"Password: password")
    print("\n💡 หมายเหตุ:")
    print("   - ใช้ข้อมูลนี้ในการเชื่อมต่อจากโปรแกรม Database Browser")
    print("   - ตรวจสอบว่า Docker containers กำลังทำงานอยู่")
    print("   - รันคำสั่ง: docker-compose up -d")
    
    print(f"\n{'=' * 80}")

if __name__ == "__main__":
    check_database_info()
