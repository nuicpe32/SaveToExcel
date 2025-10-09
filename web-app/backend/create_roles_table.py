#!/usr/bin/env python3
"""
Script to create user roles master data table
"""

import sys
import os
sys.path.append('/app')

from app.core.database import SessionLocal, engine
from sqlalchemy import text

def create_roles_table():
    """Create user_roles table and insert master data"""
    
    db = SessionLocal()
    try:
        # Create table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS user_roles (
            id SERIAL PRIMARY KEY,
            role_name VARCHAR(50) NOT NULL UNIQUE,
            role_description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        db.execute(text(create_table_sql))
        db.commit()
        
        # Insert master data
        roles_data = [
            ("admin", "แอดมิน", "ผู้ดูแลระบบ"),
            ("investigator", "พนักงานสอบสวน", "เจ้าหน้าที่สอบสวนคดี"),
            ("detective", "เจ้าหน้าที่สืบสวน", "เจ้าหน้าที่สืบสวนข้อมูล"),
            ("clerk", "เจ้าหน้าที่ธุรการ", "เจ้าหน้าที่งานธุรการ"),
            ("supervisor", "ผู้บังคับบัญชา", "ผู้บังคับบัญชาระดับสูง")
        ]
        
        # Clear existing data
        db.execute(text("DELETE FROM user_roles"))
        
        # Insert new data
        for role_name, role_display, role_description in roles_data:
            insert_sql = """
            INSERT INTO user_roles (role_name, role_display, role_description)
            VALUES (:role_name, :role_display, :role_description)
            """
            db.execute(text(insert_sql), {
                "role_name": role_name,
                "role_display": role_display,
                "role_description": role_description
            })
        
        db.commit()
        print("✅ User roles table created and populated successfully!")
        
        # Verify data
        result = db.execute(text("SELECT COUNT(*) FROM user_roles"))
        count = result.scalar()
        print(f"📊 Total roles inserted: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_roles_table()
