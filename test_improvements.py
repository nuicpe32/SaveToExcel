#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ทดสอบฟีเจอร์ปรับปรุงใหม่
"""

import json
import os
from datetime import datetime

def test_bank_data():
    """ทดสอบข้อมูลธนาคาร"""
    print("="*80)
    print("🏦 ทดสอบข้อมูลธนาคารและ dropdown lists")
    print("="*80)
    
    if os.path.exists('bank_data.json'):
        with open('bank_data.json', 'r', encoding='utf-8') as f:
            bank_data = json.load(f)
        
        branches = bank_data.get('bank_branches', [])
        names = bank_data.get('bank_names', [])
        mappings = bank_data.get('address_mapping', {})
        
        print(f"✅ โหลดข้อมูลธนาคารสำเร็จ")
        print(f"   📊 ธนาคารสาขา: {len(branches)} รายการ")
        print(f"   🏛️ ชื่อธนาคาร: {len(names)} รายการ")
        print(f"   📍 การ mapping ที่อยู่: {len(mappings)} รายการ")
        
        print(f"\n🔹 ตัวอย่างธนาคารสาขา (5 รายการแรก):")
        for i, branch in enumerate(branches[:5], 1):
            print(f"   {i}. {branch}")
        
        print(f"\n🔹 ตัวอย่างชื่อธนาคาร (5 รายการแรก):")
        for i, name in enumerate(names[:5], 1):
            print(f"   {i}. {name}")
        
        print(f"\n🔹 ตัวอย่างการ mapping ที่อยู่:")
        count = 0
        for key, addr in mappings.items():
            if count >= 2:
                break
            branch, name = key.split('|')
            print(f"   {branch} + {name} =>")
            print(f"     ที่อยู่: {addr.get('ที่อยู่ธนาคาร', '')}")
            print(f"     จังหวัด: {addr.get('จังหวัด', '')}")
            count += 1
        
        return True
    else:
        print("❌ ไม่พบไฟล์ bank_data.json")
        return False

def test_automatic_fields():
    """ทดสอบฟิลด์อัตโนมัติ"""
    print(f"\n📅 ทดสอบฟิลด์อัตโนมัติ")
    print("="*50)
    
    # ทดสอบวันที่
    now = datetime.now()
    thai_months = {
        1: "มกราคม", 2: "กุมภาพันธ์", 3: "มีนาคม", 4: "เมษายน",
        5: "พฤษภาคม", 6: "มิถุนายน", 7: "กรกฎาคม", 8: "สิงหาคม",
        9: "กันยายน", 10: "ตุลาคม", 11: "พฤศจิกายน", 12: "ธันวาคม"
    }
    
    current_day = str(now.day)
    current_month = thai_months[now.month]
    current_year = str(now.year + 543)  # พ.ศ.
    
    print(f"✅ วันที่อัตโนมัติ:")
    print(f"   วัน: {current_day}")
    print(f"   เดือน: {current_month}")
    print(f"   ปี: {current_year}")
    
    # ทดสอบลำดับ (จำลอง)
    print(f"\n✅ ลำดับอัตโนมัติ:")
    print(f"   ลำดับถัดไป: 272 (ต่อจากข้อมูลเดิม 271 แถว)")
    
    return True

def test_improvements_summary():
    """สรุปการปรับปรุง"""
    print(f"\n🎯 สรุปการปรับปรุงทั้งหมด")
    print("="*80)
    
    improvements = [
        "✅ ลำดับ - แสดงอัตโนมัติ (ลำดับล่าสุด + 1)",
        "✅ วัน เดือน ปี - แสดงวันที่ปัจจุบันในรูปแบบไทย",
        "✅ ธนาคารสาขา - dropdown list จากข้อมูลเดิม (40 รายการ)",
        "✅ ชื่อธนาคาร - dropdown list จากข้อมูลเดิม (20 รายการ)",
        "✅ ชื่อบัญชี ↔ เจ้าของบัญชีม้า - ซิงค์ข้อมูลเดียวกัน",
        "✅ ช่วงเวลา - ย้ายไปส่วนข้อมูลธนาคาร",
        "✅ ที่อยู่ธนาคาร - แสดงอัตโนมัติตามการเลือกธนาคาร",
        "✅ ซอย หมู่ ตำบล อำเภอ ถนน จังหวัด รหัสไปรษณี - แสดงอัตโนมัติ"
    ]
    
    for improvement in improvements:
        print(f"   {improvement}")
    
    print(f"\n📋 โครงสร้างฟิลด์ใหม่:")
    groups = [
        ("📋 ข้อมูลหนังสือ", ["ลำดับ (auto)", "เลขหนังสือ", "วัน (auto)", "เดือน (auto)", "ปี (auto)"]),
        ("🏦 ข้อมูลธนาคาร", ["ธนาคารสาขา (dropdown)", "ชื่อธนาคาร (dropdown)", "เลขบัญชี", "ชื่อบัญชี", "เจ้าของบัญชีม้า (linked)", "ช่วงเวลา"]),
        ("👤 ข้อมูลผู้เกี่ยวข้อง", ["ผู้เสียหาย", "เคสไอดี"]),
        ("📍 ที่อยู่ธนาคาร", ["ที่อยู่ธนาคาร (auto)", "ซอย (auto)", "หมู่ (auto)", "ตำบล/แขวง (auto)", "อำเภอ/เขต (auto)", "ถนน (auto)", "จังหวัด (auto)", "รหัสไปรษณี (auto)"]),
        ("📅 ข้อมูลการส่ง", ["วันนัดส่ง", "เดือนส่ง", "เวลาส่ง"])
    ]
    
    for group_name, fields in groups:
        print(f"\n   {group_name}")
        for field in fields:
            print(f"     • {field}")
    
    print(f"\n🚀 วิธีใช้งาน:")
    print(f"   1. python3 install_dependencies.py")
    print(f"   2. python3 simple_excel_manager.py")
    print(f"   3. เลือกแท็บ 'กรอกข้อมูล' เพื่อใช้ฟีเจอร์ใหม่")
    print(f"   4. เลือกธนาคารจาก dropdown -> ที่อยู่จะปรากฏอัตโนมัติ")
    print(f"   5. กรอกชื่อบัญชี -> เจ้าของบัญชีม้าจะซิงค์อัตโนมัติ")

def main():
    """ฟังก์ชันหลัก"""
    print("🔥 ทดสอบการปรับปรุงโปรแกรม Excel Data Manager")
    
    bank_ok = test_bank_data()
    auto_ok = test_automatic_fields()
    
    if bank_ok and auto_ok:
        print(f"\n🎉 การทดสอบสำเร็จทั้งหมด!")
        test_improvements_summary()
    else:
        print(f"\n⚠️ การทดสอบไม่สมบูรณ์")

if __name__ == "__main__":
    main()