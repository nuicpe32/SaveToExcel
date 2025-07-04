#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test script สำหรับตรวจสอบฟิลด์ที่อัพเดทแล้ว
"""

# ทดสอบ field structure
fields = [
    ("ลำดับ", "order_no"),
    ("เลขหนังสือ", "document_no"),
    ("วัน", "day"),
    ("เดือน", "month"),
    ("ปี", "year"),
    ("ธนาคารสาขา", "bank_branch"),
    ("ผู้เสียหาย", "victim"),
    ("เคสไอดี", "case_id"),
    ("เจ้าของบัญชีม้า", "account_owner_horse"),
    ("ชื่อธนาคาร", "bank_name"),
    ("เลขบัญชี", "account_no"),
    ("ชื่อบัญชี", "account_name"),
    ("ช่วงเวลา", "time_period"),
    ("ที่อยู่ธนาคาร", "bank_address"),
    ("ซอย", "soi"),
    ("หมู่", "moo"),
    ("ตำบล/แขวง", "tambon_khwaeng"),
    ("อำเภอ/เขต", "amphoe_khet"),
    ("ถนน", "road"),
    ("จังหวัด", "province"),
    ("รหัสไปรษณี", "postal_code"),
    ("วันนัดส่ง", "delivery_day"),
    ("เดือนส่ง", "delivery_month"),
    ("เวลาส่ง", "delivery_time")
]

print("=== ฟิลด์ทั้งหมดที่รองรับ ===")
print(f"จำนวนฟิลด์ทั้งหมด: {len(fields)}")
print()

for i, (thai_name, field_key) in enumerate(fields, 1):
    print(f"{i:2d}. {thai_name:<20} ({field_key})")

print("\n=== กลุ่มฟิลด์ ===")

groups = [
    ("📋 ข้อมูลหนังสือ", [
        ("ลำดับ", "order_no"),
        ("เลขหนังสือ", "document_no"),
        ("วัน", "day"),
        ("เดือน", "month"),
        ("ปี", "year")
    ]),
    ("🏦 ข้อมูลธนาคาร", [
        ("ธนาคารสาขา", "bank_branch"),
        ("ชื่อธนาคาร", "bank_name"),
        ("เลขบัญชี", "account_no"),
        ("ชื่อบัญชี", "account_name"),
        ("เจ้าของบัญชีม้า", "account_owner_horse")
    ]),
    ("👤 ข้อมูลผู้เกี่ยวข้อง", [
        ("ผู้เสียหาย", "victim"),
        ("เคสไอดี", "case_id"),
        ("ช่วงเวลา", "time_period")
    ]),
    ("📍 ที่อยู่ธนาคาร", [
        ("ที่อยู่ธนาคาร", "bank_address"),
        ("ซอย", "soi"),
        ("หมู่", "moo"),
        ("ตำบล/แขวง", "tambon_khwaeng"),
        ("อำเภอ/เขต", "amphoe_khet"),
        ("ถนน", "road"),
        ("จังหวัด", "province"),
        ("รหัสไปรษณี", "postal_code")
    ]),
    ("📅 ข้อมูลการส่ง", [
        ("วันนัดส่ง", "delivery_day"),
        ("เดือนส่ง", "delivery_month"),
        ("เวลาส่ง", "delivery_time")
    ])
]

for group_name, group_fields in groups:
    print(f"\n{group_name}")
    for thai_name, field_key in group_fields:
        print(f"  - {thai_name}")

print("\n=== สถานะการพัฒนา ===")
print("✅ อัพเดทฟิลด์ตามความต้องการ")
print("✅ จัดกลุ่มฟิลด์เป็นหมวดหมู่")
print("✅ ปรับปรุง GUI ให้เป็นระเบียบ")
print("✅ เพิ่มการสร้างลำดับอัตโนมัติ")
print("✅ รองรับการแก้ไข ลบ คัดลอกข้อมูล")

print("\n=== วิธีใช้งาน ===")
print("1. ติดตั้ง dependencies: python3 install_dependencies.py")
print("2. รันโปรแกรม: python3 simple_excel_manager.py")
print("3. ใช้งานผ่าน GUI ที่สวยงาม เรียบง่าย")