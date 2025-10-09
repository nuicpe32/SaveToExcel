#!/usr/bin/env python3
"""
Script to setup user system with master data and admin user
"""

import sys
import os
sys.path.append('/app')

from app.core.database import SessionLocal, engine
from app.models import User, PoliceRank, UserRole
from app.core.security import get_password_hash
from sqlalchemy import text
from datetime import datetime

def setup_user_system():
    """Setup user system with master data and admin user"""
    
    db = SessionLocal()
    try:
        print("🚀 Setting up user system...")
        
        # 1. Create police ranks table and data
        print("📋 Creating police ranks...")
        create_ranks_table_sql = """
        CREATE TABLE IF NOT EXISTS police_ranks (
            id SERIAL PRIMARY KEY,
            rank_full VARCHAR(100) NOT NULL,
            rank_short VARCHAR(20) NOT NULL,
            rank_english VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute(text(create_ranks_table_sql))
        
        # Insert police ranks data
        ranks_data = [
            ("พลตำรวจเอก", "พล.ต.อ.", "Police General"),
            ("พลตำรวจโท", "พล.ต.ท.", "Police Lieutenant General"),
            ("พลตำรวจตรี", "พล.ต.ต.", "Police Major General"),
            ("พันตำรวจเอก", "พ.ต.อ.", "Police Colonel"),
            ("พันตำรวจโท", "พ.ต.ท.", "Police Lieutenant Colonel"),
            ("พันตำรวจตรี", "พ.ต.ต.", "Police Major"),
            ("ร้อยตำรวจเอก", "ร.ต.อ.", "Police Captain"),
            ("ร้อยตำรวจโท", "ร.ต.ท.", "Police Lieutenant"),
            ("ร้อยตำรวจตรี", "ร.ต.ต.", "Police Sub-Lieutenant"),
            ("ดาบตำรวจ", "ด.ต.", "Police Senior Sergeant Major"),
            ("จ่าสิบตำรวจ", "จ.ส.ต.", "Police Sergeant Major"),
            ("สิบตำรวจเอก", "ส.ต.อ.", "Police Sergeant"),
            ("สิบตำรวจโท", "ส.ต.ท.", "Police Corporal"),
            ("สิบตำรวจตรี", "ส.ต.ต.", "Police Lance Corporal")
        ]
        
        db.execute(text("DELETE FROM police_ranks"))
        for rank_full, rank_short, rank_english in ranks_data:
            insert_sql = """
            INSERT INTO police_ranks (rank_full, rank_short, rank_english)
            VALUES (:rank_full, :rank_short, :rank_english)
            """
            db.execute(text(insert_sql), {
                "rank_full": rank_full,
                "rank_short": rank_short,
                "rank_english": rank_english
            })
        
        # 2. Create user roles table and data
        print("👥 Creating user roles...")
        create_roles_table_sql = """
        CREATE TABLE IF NOT EXISTS user_roles (
            id SERIAL PRIMARY KEY,
            role_name VARCHAR(50) NOT NULL UNIQUE,
            role_display VARCHAR(50) NOT NULL,
            role_description TEXT,
            is_active BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        db.execute(text(create_roles_table_sql))
        
        # Insert user roles data
        roles_data = [
            ("admin", "แอดมิน", "ผู้ดูแลระบบ"),
            ("investigator", "พนักงานสอบสวน", "เจ้าหน้าที่สอบสวนคดี"),
            ("detective", "เจ้าหน้าที่สืบสวน", "เจ้าหน้าที่สืบสวนข้อมูล"),
            ("clerk", "เจ้าหน้าที่ธุรการ", "เจ้าหน้าที่งานธุรการ"),
            ("supervisor", "ผู้บังคับบัญชา", "ผู้บังคับบัญชาระดับสูง")
        ]
        
        db.execute(text("DELETE FROM user_roles"))
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
        
        # 3. Update users table structure
        print("🔧 Updating users table...")
        
        # Add new columns to users table
        alter_users_sql = """
        ALTER TABLE users 
        ADD COLUMN IF NOT EXISTS rank_id INTEGER REFERENCES police_ranks(id),
        ADD COLUMN IF NOT EXISTS position VARCHAR(255),
        ADD COLUMN IF NOT EXISTS phone_number VARCHAR(20),
        ADD COLUMN IF NOT EXISTS line_id VARCHAR(100),
        ADD COLUMN IF NOT EXISTS role_id INTEGER REFERENCES user_roles(id),
        ADD COLUMN IF NOT EXISTS is_approved BOOLEAN DEFAULT FALSE,
        ADD COLUMN IF NOT EXISTS failed_login_attempts INTEGER DEFAULT 0,
        ADD COLUMN IF NOT EXISTS locked_until TIMESTAMP,
        ADD COLUMN IF NOT EXISTS approved_at TIMESTAMP,
        ADD COLUMN IF NOT EXISTS approved_by INTEGER REFERENCES users(id);
        """
        db.execute(text(alter_users_sql))
        
        # 4. Update existing admin user
        print("👤 Updating admin user...")
        
        # Get admin role ID
        admin_role_result = db.execute(text("SELECT id FROM user_roles WHERE role_name = 'admin'"))
        admin_role_id = admin_role_result.scalar()
        
        # Get highest rank ID (พล.ต.อ.)
        highest_rank_result = db.execute(text("SELECT id FROM police_ranks WHERE rank_short = 'พล.ต.อ.'"))
        highest_rank_id = highest_rank_result.scalar()
        
        # Update admin user
        update_admin_sql = """
        UPDATE users 
        SET rank_id = :rank_id,
            role_id = :role_id,
            is_active = TRUE,
            is_approved = TRUE,
            approved_at = CURRENT_TIMESTAMP
        WHERE username = 'admin'
        """
        db.execute(text(update_admin_sql), {
            "rank_id": highest_rank_id,
            "role_id": admin_role_id
        })
        
        db.commit()
        print("✅ User system setup completed successfully!")
        
        # Verify setup
        ranks_count = db.execute(text("SELECT COUNT(*) FROM police_ranks")).scalar()
        roles_count = db.execute(text("SELECT COUNT(*) FROM user_roles")).scalar()
        admin_user = db.execute(text("SELECT username, is_approved FROM users WHERE username = 'admin'")).fetchone()
        
        print(f"📊 Police ranks created: {ranks_count}")
        print(f"📊 User roles created: {roles_count}")
        if admin_user:
            print(f"👤 Admin user status: {admin_user[0]} - Approved: {admin_user[1]}")
        else:
            print("👤 Admin user not found")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    setup_user_system()
