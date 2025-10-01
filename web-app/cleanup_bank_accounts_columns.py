#!/usr/bin/env python3
"""
Migration: Remove redundant bank-related columns from bank_accounts table
After normalizing to banks table, these columns are no longer needed:
- bank_address, soi, moo, road, sub_district, district, province, postal_code
- bank_branch (we only send to headquarters now)
"""

import psycopg2
import sys

DB_CONFIG = {
    'host': 'criminal-case-db',
    'port': 5432,
    'database': 'criminal_case_db',
    'user': 'user',
    'password': 'password'
}

COLUMNS_TO_DROP = [
    'bank_address',
    'soi',
    'moo',
    'road',
    'sub_district',
    'district',
    'province',
    'postal_code',
    'bank_branch'  # No longer needed - send to headquarters only
]

def main():
    print("=" * 80)
    print("CLEANUP BANK_ACCOUNTS TABLE - REMOVE REDUNDANT COLUMNS")
    print("=" * 80)

    try:
        # Connect to database
        print("\n1. Connecting to database...")
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        print("   ✓ Connected successfully")

        # Check current columns
        print("\n2. Checking current columns in bank_accounts...")
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'bank_accounts'
            ORDER BY ordinal_position
        """)
        columns = cur.fetchall()
        print(f"   Current columns: {len(columns)}")

        existing_columns = [col[0] for col in columns]
        columns_to_drop = [col for col in COLUMNS_TO_DROP if col in existing_columns]

        if not columns_to_drop:
            print("\n   ℹ️ No columns to drop (already cleaned up)")
            return

        print(f"\n   Columns to be dropped: {', '.join(columns_to_drop)}")

        # Drop columns
        print("\n3. Dropping redundant columns...")
        for col in columns_to_drop:
            try:
                print(f"   Dropping column: {col}")
                cur.execute(f"ALTER TABLE bank_accounts DROP COLUMN IF EXISTS {col}")
                conn.commit()
                print(f"   ✓ Dropped: {col}")
            except Exception as e:
                print(f"   ✗ Error dropping {col}: {e}")
                conn.rollback()

        # Verify final structure
        print("\n4. Verifying final structure...")
        cur.execute("""
            SELECT column_name, data_type
            FROM information_schema.columns
            WHERE table_name = 'bank_accounts'
            ORDER BY ordinal_position
        """)
        final_columns = cur.fetchall()

        print(f"\n   Final column count: {len(final_columns)}")
        print("\n   Remaining columns:")
        for col_name, col_type in final_columns:
            print(f"   - {col_name} ({col_type})")

        # Check bank_id foreign key
        print("\n5. Verifying bank_id foreign key...")
        cur.execute("""
            SELECT COUNT(*) as total,
                   COUNT(bank_id) as with_bank_id,
                   COUNT(*) - COUNT(bank_id) as without_bank_id
            FROM bank_accounts
        """)
        stats = cur.fetchone()
        print(f"   Total records: {stats[0]}")
        print(f"   With bank_id: {stats[1]}")
        print(f"   Without bank_id: {stats[2]}")

        print("\n" + "=" * 80)
        print("CLEANUP COMPLETED SUCCESSFULLY")
        print("=" * 80)
        print("\nNext steps:")
        print("1. Update Backend model: remove dropped columns from BankAccount model")
        print("2. Update Backend schema: remove fields from BankAccountCreate/Update schemas")
        print("3. Update Frontend forms: remove bank address and branch fields")
        print("4. Restart backend service")

        cur.close()
        conn.close()

    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == '__main__':
    main()
