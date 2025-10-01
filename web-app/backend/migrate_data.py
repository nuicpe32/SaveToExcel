#!/usr/bin/env python3
"""
Data Migration Script
ย้ายข้อมูลจาก Excel files ไป PostgreSQL database

Usage:
    python migrate_data.py --all
    python migrate_data.py --banks
    python migrate_data.py --suspects
    python migrate_data.py --cases
    python migrate_data.py --arrests
"""

import sys
import argparse
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from app.services.data_migration import DataMigration
from app.core.database import Base, engine


def init_database():
    print("🔧 กำลังสร้างตารางในฐานข้อมูล...")
    Base.metadata.create_all(bind=engine)
    print("✅ สร้างตารางเสร็จสิ้น\n")


def main():
    parser = argparse.ArgumentParser(description='Data Migration Tool')
    parser.add_argument('--all', action='store_true', help='ย้ายข้อมูลทั้งหมด')
    parser.add_argument('--banks', action='store_true', help='ย้ายข้อมูลบัญชีธนาคาร')
    parser.add_argument('--suspects', action='store_true', help='ย้ายข้อมูลหมายเรียกผู้ต้องหา')
    parser.add_argument('--cases', action='store_true', help='ย้ายข้อมูลคดีอาญา')
    parser.add_argument('--arrests', action='store_true', help='ย้ายข้อมูลหลังการจับกุม')
    parser.add_argument('--init', action='store_true', help='สร้างตารางในฐานข้อมูลก่อน')
    parser.add_argument('--excel-dir', type=str, default='../../Xlsx', help='path to Excel files directory')

    args = parser.parse_args()

    if args.init:
        init_database()

    migrator = DataMigration(excel_dir=args.excel_dir)

    if args.all:
        migrator.migrate_all()
    else:
        if args.banks:
            migrator.migrate_bank_accounts()
        if args.suspects:
            migrator.migrate_suspects()
        if args.cases:
            migrator.migrate_criminal_cases()
        if args.arrests:
            migrator.migrate_post_arrests()

        if not any([args.banks, args.suspects, args.cases, args.arrests]):
            print("❌ กรุณาระบุ option อย่างน้อย 1 ตัว หรือใช้ --all")
            print("ใช้ --help เพื่อดูวิธีใช้งาน")
            sys.exit(1)


if __name__ == "__main__":
    main()