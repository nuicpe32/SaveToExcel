#!/usr/bin/env python3
"""
Migration: Add banks table and normalize bank_accounts
- Create banks table from Excel master data
- Add bank_id foreign key to bank_accounts
- Migrate existing data
- Remove redundant columns from bank_accounts
"""

import pandas as pd
import psycopg2
from psycopg2.extras import RealDictCursor
import sys

# Database connection
import os
DB_CONFIG = {
    'host': os.getenv('DATABASE_HOST', 'criminal-case-db'),
    'port': 5432,
    'database': 'criminal_case_db',
    'user': 'user',
    'password': 'password'
}

# Excel file path
EXCEL_PATH = '/app/bank_master_data.xlsx'

# Bank name normalization mapping
BANK_NAME_MAPPING = {
    'กสิกรไทย': 'กสิกรไทย',
    'ไทยพาณิชย์': 'ไทยพาณิชย์',
    'ทหารไทยธนชาต': 'ทหารไทยธนชาต',
    'ทหารไทยธนชาต ': 'ทหารไทยธนชาต',
    'ยูโอบี': 'ยูโอบี',
    'กรุงเทพ': 'กรุงเทพ',
    'กรุงศรีอยุธยา': 'กรุงศรีอยุธยา',
    'กรุงศรีอยุธยา ': 'กรุงศรีอยุธยา',
    'ออมสิน': 'ออมสิน',
    'กรุงไทย': 'กรุงไทย',
    'ซีไอเอ็มบี': 'ซีไอเอ็มบีไทย',
    'ซีไอเอ็มบี ไทย': 'ซีไอเอ็มบีไทย',
    'ซีไอเอ็มบี ไทย ': 'ซีไอเอ็มบีไทย',
    'ซีไอเอ็มบีไทย': 'ซีไอเอ็มบีไทย',
    'อาคารสงเคราะห์': 'อาคารสงเคราะห์',
    'แลนด์ แอนด์ เฮ้าส์': 'แลนด์แอนด์เฮ้าส์',
    'แลนด์แอนด์เฮ้าส์': 'แลนด์แอนด์เฮ้าส์',
    'เพื่อการเกษตรและสหกรณ์การเกษตร (ธ.ก.ส.)': 'เพื่อการเกษตรและสหกรณ์การเกษตร (ธ.ก.ส.)',
    'เกียรตินาคินภัทร': 'เกียรตินาคินภัทร',
}

def normalize_bank_name(name):
    """Normalize bank name (trim spaces, map to standard name)"""
    if pd.isna(name) or str(name).strip() == 'nan':
        return None
    name = str(name).strip()
    return BANK_NAME_MAPPING.get(name, name)

def main():
    print("=" * 80)
    print("BANK MASTER DATA MIGRATION")
    print("=" * 80)

    try:
        # Connect to database
        print("\n1. Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor(cursor_factory=RealDictCursor)
        print("   ✓ Connected successfully")

        # Load Excel data
        print("\n2. Loading bank master data from Excel...")
        df = pd.read_excel(EXCEL_PATH)
        print(f"   ✓ Loaded {len(df)} banks from Excel")

        # Create banks table
        print("\n3. Creating banks table...")
        cur.execute("""
            CREATE TABLE IF NOT EXISTS banks (
                id SERIAL PRIMARY KEY,
                bank_name VARCHAR(255) NOT NULL UNIQUE,
                bank_address VARCHAR(500),
                soi VARCHAR(100),
                moo VARCHAR(50),
                road VARCHAR(100),
                sub_district VARCHAR(100),
                district VARCHAR(100),
                province VARCHAR(100),
                postal_code VARCHAR(10),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        print("   ✓ Banks table created")

        # Insert bank master data
        print("\n4. Inserting bank master data...")
        inserted_count = 0
        for idx, row in df.iterrows():
            bank_name = normalize_bank_name(row['ชื่อธนาคาร'])
            if not bank_name:
                continue

            try:
                cur.execute("""
                    INSERT INTO banks (
                        bank_name, bank_address, soi, moo, road,
                        sub_district, district, province, postal_code
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (bank_name) DO NOTHING
                """, (
                    bank_name,
                    row['ที่อยู่ธนาคาร'],
                    row['ซอย'] if row['ซอย'] != '-' else None,
                    row['หมู่'] if row['หมู่'] != '-' else None,
                    row['ถนน'],
                    row['ตำบล/แขวง'],
                    row['อำเภอ/เขต'],
                    row['จังหวัด'],
                    str(row['รหัสไปรษณี'])
                ))
                inserted_count += 1
                print(f"   ✓ Inserted: {bank_name}")
            except Exception as e:
                print(f"   ✗ Error inserting {bank_name}: {e}")

        conn.commit()
        print(f"\n   ✓ Total inserted: {inserted_count} banks")

        # Add bank_id column to bank_accounts
        print("\n5. Adding bank_id column to bank_accounts...")
        cur.execute("""
            ALTER TABLE bank_accounts
            ADD COLUMN IF NOT EXISTS bank_id INTEGER REFERENCES banks(id)
        """)
        conn.commit()
        print("   ✓ Column added")

        # Update bank_id for existing records
        print("\n6. Mapping existing bank_accounts to banks table...")
        cur.execute("SELECT id, bank_name FROM bank_accounts WHERE bank_name IS NOT NULL")
        accounts = cur.fetchall()

        matched_count = 0
        unmatched_count = 0
        null_count = 0
        unmatched_banks = set()

        for account in accounts:
            account_id = account['id']
            bank_name_raw = account['bank_name']

            if pd.isna(bank_name_raw) or str(bank_name_raw).strip() == 'nan':
                null_count += 1
                continue

            bank_name = normalize_bank_name(bank_name_raw)
            if not bank_name:
                null_count += 1
                continue

            # Find bank in banks table
            cur.execute("SELECT id FROM banks WHERE bank_name = %s", (bank_name,))
            bank = cur.fetchone()

            if bank:
                # Update bank_id
                cur.execute(
                    "UPDATE bank_accounts SET bank_id = %s WHERE id = %s",
                    (bank['id'], account_id)
                )
                matched_count += 1
            else:
                unmatched_count += 1
                unmatched_banks.add(bank_name_raw)
                print(f"   ⚠ Unmatched: '{bank_name_raw}' -> normalized: '{bank_name}'")

        conn.commit()

        print(f"\n   Results:")
        print(f"   ✓ Matched and updated: {matched_count} records")
        print(f"   ⚠ Unmatched (set to NULL): {unmatched_count} records")
        print(f"   ⚠ NULL/NaN values: {null_count} records")

        if unmatched_banks:
            print(f"\n   Unmatched bank names:")
            for bank in sorted(unmatched_banks):
                print(f"   - '{bank}'")

        # Show current status
        print("\n7. Current status:")
        cur.execute("""
            SELECT
                COUNT(*) as total,
                COUNT(bank_id) as with_bank_id,
                COUNT(*) - COUNT(bank_id) as without_bank_id
            FROM bank_accounts
        """)
        status = cur.fetchone()
        print(f"   Total records: {status['total']}")
        print(f"   With bank_id: {status['with_bank_id']}")
        print(f"   Without bank_id: {status['without_bank_id']}")

        # Optional: Remove old columns (commented out for safety)
        print("\n8. Cleanup old columns (SKIPPED for safety)")
        print("   The following columns can be removed manually after verification:")
        print("   - bank_address, soi, moo, road, sub_district, district, province, postal_code")
        print("\n   To remove them, run:")
        print("   ALTER TABLE bank_accounts DROP COLUMN bank_address, DROP COLUMN soi, ...")

        print("\n" + "=" * 80)
        print("MIGRATION COMPLETED SUCCESSFULLY")
        print("=" * 80)

        cur.close()
        conn.close()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
