#!/usr/bin/env python3
"""
Script to check admin user data
"""

import sys
import os
sys.path.append('/app')

from app.core.database import SessionLocal
from sqlalchemy import text

def check_admin_user():
    """Check admin user data"""
    
    db = SessionLocal()
    try:
        print("🔍 Checking admin user data...")
        
        # Check admin user
        user_result = db.execute(text("SELECT username, email, is_approved, role_id FROM users WHERE username = 'admin'"))
        user = user_result.fetchone()
        
        if user:
            print(f"✅ Admin user found:")
            print(f"   Username: {user[0]}")
            print(f"   Email: {user[1]}")
            print(f"   Approved: {user[2]}")
            print(f"   Role ID: {user[3]}")
            
            # Check role data
            if user[3]:
                role_result = db.execute(text("SELECT role_name, role_display FROM user_roles WHERE id = :role_id"), {"role_id": user[3]})
                role = role_result.fetchone()
                if role:
                    print(f"   Role: {role[0]} ({role[1]})")
                else:
                    print("   ❌ Role not found")
            
            # Check rank data
            rank_result = db.execute(text("SELECT rank_short, rank_full FROM police_ranks WHERE id = (SELECT rank_id FROM users WHERE username = 'admin')"))
            rank = rank_result.fetchone()
            if rank:
                print(f"   Rank: {rank[0]} ({rank[1]})")
            else:
                print("   ❌ Rank not found")
        else:
            print("❌ Admin user not found")
            
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin_user()
