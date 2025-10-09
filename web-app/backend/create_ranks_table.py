#!/usr/bin/env python3
"""
Script to create police ranks master data table
"""

import sys
import os
sys.path.append('/app')

from app.core.database import SessionLocal, engine
from sqlalchemy import text

def create_ranks_table():
    """Create police_ranks table and insert master data"""
    
    db = SessionLocal()
    try:
        # Create table
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS police_ranks (
            id SERIAL PRIMARY KEY,
            rank_full VARCHAR(100) NOT NULL,
            rank_short VARCHAR(20) NOT NULL,
            rank_english VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        db.execute(text(create_table_sql))
        db.commit()
        
        # Insert master data
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
        
        # Clear existing data
        db.execute(text("DELETE FROM police_ranks"))
        
        # Insert new data
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
        
        db.commit()
        print("✅ Police ranks table created and populated successfully!")
        
        # Verify data
        result = db.execute(text("SELECT COUNT(*) FROM police_ranks"))
        count = result.scalar()
        print(f"📊 Total ranks inserted: {count}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_ranks_table()
