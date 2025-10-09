#!/usr/bin/env python3
"""
Script to create user_roles table for storing multiple roles per user
"""

import sys
import os
sys.path.append('/app')

from app.core.database import SessionLocal, engine
from sqlalchemy import text

def create_user_roles_table():
    """Create user_roles table for storing multiple roles per user"""
    
    db = SessionLocal()
    try:
        print("🔧 Creating user_roles table...")
        
        # Create table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS user_roles_mapping (
            id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
            role_id INTEGER NOT NULL REFERENCES user_roles(id) ON DELETE CASCADE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            UNIQUE(user_id, role_id)
        );
        """
        
        db.execute(text(create_table_sql))
        db.commit()
        
        print("✅ User roles mapping table created successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_user_roles_table()
