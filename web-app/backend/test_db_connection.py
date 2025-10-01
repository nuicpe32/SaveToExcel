#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test database connection
"""

import psycopg2
import sys
import os

def test_db_connection():
    """Test database connection"""
    print("🔗 ทดสอบการเชื่อมต่อฐานข้อมูล...")
    
    # Connection parameters
    host = "localhost"
    port = 5432
    database = "criminal_case_db"
    user = "user"
    password = "password"
    
    try:
        # Test connection
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        
        print("✅ เชื่อมต่อสำเร็จ!")
        
        # Get database info
        cur = conn.cursor()
        cur.execute("SELECT version()")
        version = cur.fetchone()[0]
        print(f"📊 PostgreSQL Version: {version}")
        
        cur.execute("SELECT current_database()")
        db_name = cur.fetchone()[0]
        print(f"📊 Database: {db_name}")
        
        cur.execute("SELECT current_user")
        current_user = cur.fetchone()[0]
        print(f"📊 Current User: {current_user}")
        
        # Test tables
        cur.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public' 
            ORDER BY table_name
        """)
        tables = cur.fetchall()
        
        print(f"📋 Tables ({len(tables)}):")
        for table in tables:
            print(f"   - {table[0]}")
        
        cur.close()
        conn.close()
        
        print("\n🎯 ข้อมูลการเชื่อมต่อสำหรับ DBeaver:")
        print(f"   Host: {host}")
        print(f"   Port: {port}")
        print(f"   Database: {database}")
        print(f"   Username: {user}")
        print(f"   Password: {password}")
        
    except Exception as e:
        print(f"❌ เชื่อมต่อไม่สำเร็จ: {e}")
        print("\n🔧 วิธีแก้ไข:")
        print("   1. ตรวจสอบ Docker containers ทำงานอยู่")
        print("   2. รันคำสั่ง: docker-compose up -d")
        print("   3. รอให้ containers เริ่มทำงานเสร็จ")

if __name__ == "__main__":
    test_db_connection()
