#!/usr/bin/env python3
"""
Test PostgreSQL Connection
รันไฟล์นี้เพื่อทดสอบการเชื่อมต่อ database
"""

import sys

try:
    import psycopg2
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False
    print("⚠ psycopg2 not installed, trying alternative...")

if HAS_PSYCOPG2:
    # Test with psycopg2
    configs = [
        {
            'name': 'User: user / Password: password123',
            'host': 'localhost',
            'port': 5432,
            'database': 'criminal_case_db',
            'user': 'user',
            'password': 'password123'
        },
        {
            'name': 'User: dbuser / Password: dbpass123',
            'host': 'localhost',
            'port': 5432,
            'database': 'criminal_case_db',
            'user': 'dbuser',
            'password': 'dbpass123'
        }
    ]

    for config in configs:
        print(f"\n{'='*60}")
        print(f"Testing: {config['name']}")
        print('='*60)

        try:
            conn = psycopg2.connect(
                host=config['host'],
                port=config['port'],
                database=config['database'],
                user=config['user'],
                password=config['password'],
                connect_timeout=5
            )

            cur = conn.cursor()
            cur.execute("SELECT version();")
            version = cur.fetchone()[0]

            cur.execute("SELECT current_user, current_database();")
            user, db = cur.fetchone()

            cur.execute("SELECT COUNT(*) FROM pg_tables WHERE schemaname = 'public';")
            table_count = cur.fetchone()[0]

            print(f"✅ SUCCESS!")
            print(f"   User: {user}")
            print(f"   Database: {db}")
            print(f"   Tables: {table_count}")
            print(f"   Version: {version[:50]}...")
            print(f"\n   ใช้ใน DBeaver:")
            print(f"   Username: {config['user']}")
            print(f"   Password: {config['password']}")

            cur.close()
            conn.close()

            break  # If successful, no need to test other config

        except Exception as e:
            print(f"❌ FAILED: {str(e)}")
            continue
else:
    # Fallback: Use urllib to test TCP connection
    import socket

    print("\n" + "="*60)
    print("Testing TCP Connection (psycopg2 not available)")
    print("="*60)

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)
        result = sock.connect_ex(('localhost', 5432))
        sock.close()

        if result == 0:
            print("✅ Port 5432 is OPEN - PostgreSQL is running")
            print("\nInstall psycopg2 to test authentication:")
            print("   pip install psycopg2-binary")
        else:
            print("❌ Port 5432 is CLOSED - PostgreSQL not accessible")
            print("   Check if Docker container is running:")
            print("   docker ps | grep criminal-case-db")

    except Exception as e:
        print(f"❌ Connection test failed: {str(e)}")

print("\n" + "="*60)
print("Test Complete")
print("="*60 + "\n")
