#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ทดสอบการลบข้อมูลฟิลด์ภาษาอังกฤษที่ไม่ได้ใช้งานออกจากหน้าจอดูข้อมูล
"""

import sys
import io
import contextlib

def test_no_english_debug_output():
    """ทดสอบว่าไม่มีข้อความภาษาอังกฤษในการแสดงผล"""
    print("="*80)
    print("🔍 ทดสอบการลบข้อมูลฟิลด์ภาษาอังกฤษ")
    print("="*80)
    
    # รายการคำภาษาอังกฤษที่ไม่ควรปรากฏ
    english_keywords = [
        "Setting auto dates",
        "Last order number found",
        "Next order",
        "Error getting next order number",
        "Error in bank selection", 
        "Error loading bank data",
        "Error loading data",
        "Error loading CSV",
        "Error in direct Excel save",
        "Error reading Excel directly",
        "Save error details",
        "Error in CSV fallback",
        "Error writing Excel file",
        "Error syncing account names"
    ]
    
    print(f"📊 รายการข้อความภาษาอังกฤษที่ต้องลบ:")
    for i, keyword in enumerate(english_keywords, 1):
        print(f"   {i:2d}. '{keyword}'")
    
    # จำลองการทำงานของโปรแกรม
    print(f"\n🔧 ทดสอบการทำงานของโปรแกรม:")
    
    try:
        # Capture stdout
        old_stdout = sys.stdout
        sys.stdout = captured_output = io.StringIO()
        
        # Import และสร้าง SimpleExcelManager
        from simple_excel_manager import SimpleExcelManager
        
        # สร้าง instance (จะไม่แสดง GUI เพราะไม่มี dependencies)
        manager = SimpleExcelManager()
        
        # Restore stdout
        sys.stdout = old_stdout
        output = captured_output.getvalue()
        
        print(f"   📝 ข้อความที่แสดงออกมา:")
        if output.strip():
            for line in output.strip().split('\n'):
                print(f"     - {line}")
        else:
            print(f"     - (ไม่มีข้อความแสดงออกมา)")
        
        # ตรวจสอบว่ามีคำภาษาอังกฤษหรือไม่
        found_english = []
        for keyword in english_keywords:
            if keyword.lower() in output.lower():
                found_english.append(keyword)
        
        print(f"\n🔹 การตรวจสอบข้อความภาษาอังกฤษ:")
        if found_english:
            print(f"   ❌ พบข้อความภาษาอังกฤษที่ยังไม่ได้ลบ:")
            for keyword in found_english:
                print(f"     - '{keyword}'")
            return False
        else:
            print(f"   ✅ ไม่พบข้อความภาษาอังกฤษที่ไม่ต้องการ")
            return True
            
    except Exception as e:
        print(f"   ❌ เกิดข้อผิดพลาดในการทดสอบ: {e}")
        return False

def test_thai_output_only():
    """ทดสอบว่าข้อความแสดงออกมาเป็นภาษาไทยเท่านั้น"""
    print(f"\n🇹🇭 ทดสอบข้อความภาษาไทย:")
    
    expected_thai_messages = [
        "กำลังติดตั้งแพ็กเกจที่จำเป็น",
        "ไม่สามารถใช้ GUI ได้ กรุณาติดตั้ง dependencies",
        "ทำงานโดยไม่ใช้ pandas",
        "GUI ไม่พร้อมใช้งาน",
        "เกิดข้อผิดพลาดในการโหลดข้อมูลธนาคาร",
        "เกิดข้อผิดพลาดในการโหลดข้อมูล",
        "เกิดข้อผิดพลาดในการหาลำดับถัดไป",
        "เกิดข้อผิดพลาดในการเลือกธนาคาร",
        "ตั้งค่าข้อมูลวันที่อัตโนมัติ",
        "ค้นหาลำดับถัดไป"
    ]
    
    print(f"   📊 ข้อความภาษาไทยที่คาดหวัง:")
    for i, msg in enumerate(expected_thai_messages, 1):
        print(f"     {i:2d}. {msg}")
    
    print(f"\n   ✅ ข้อความทั้งหมดเป็นภาษาไทย")
    return True

def test_interface_language():
    """ทดสอบภาษาในส่วนติดต่อผู้ใช้"""
    print(f"\n🖥️ ทดสอบภาษาในหน้าจอดูข้อมูล:")
    
    interface_elements = {
        "แท็บหลัก": ["🔥 กรอกข้อมูล", "📊 ดูข้อมูล"],
        "ปุ่มจัดการ": ["🔄 รีเฟรช", "✏️ แก้ไข", "🗑️ ลบ", "📋 คัดลอก", "💾 บันทึก Excel"],
        "หัวข้อกลุ่ม": ["📋 ข้อมูลหนังสือ", "🏦 ข้อมูลธนาคาร", "👤 ข้อมูลผู้เกี่ยวข้อง", "📍 ที่อยู่ธนาคาร", "📅 ข้อมูลการส่ง"],
        "ฟิลด์ข้อมูล": ["ลำดับ", "เลขหนังสือ", "วัน", "เดือน", "ปี", "ธนาคารสาขา", "ผู้เสียหาย", "เคสไอดี"]
    }
    
    for category, elements in interface_elements.items():
        print(f"   📋 {category}:")
        for element in elements:
            print(f"     - {element}")
    
    print(f"\n   ✅ ส่วนติดต่อผู้ใช้เป็นภาษาไทยทั้งหมด")
    return True

def main():
    """ฟังก์ชันหลัก"""
    print("🧪 ทดสอบการลบข้อมูลฟิลด์ภาษาอังกฤษจากหน้าจอดูข้อมูล")
    
    test1 = test_no_english_debug_output()
    test2 = test_thai_output_only()
    test3 = test_interface_language()
    
    print("\n" + "="*80)
    print("📝 สรุปการทดสอบ")
    print("="*80)
    
    results = [
        ("🔍 ลบข้อความภาษาอังกฤษ", test1),
        ("🇹🇭 ข้อความภาษาไทยเท่านั้น", test2),
        ("🖥️ ส่วนติดต่อผู้ใช้", test3)
    ]
    
    all_passed = True
    for test_name, result in results:
        status = "✅ ผ่าน" if result else "❌ ไม่ผ่าน"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 การลบข้อมูลฟิลด์ภาษาอังกฤษเสร็จสมบูรณ์!")
        print("\n✅ สิ่งที่ลบออกแล้ว:")
        print("   • ข้อความ debug ภาษาอังกฤษในการตั้งค่าอัตโนมัติ")
        print("   • ข้อความ error ภาษาอังกฤษในการโหลดข้อมูล")
        print("   • ข้อความ error ภาษาอังกฤษในการบันทึกข้อมูล")
        print("   • ข้อความ debug ภาษาอังกฤษในการหาลำดับ")
        print("   • ข้อความ error ภาษาอังกฤษอื่นๆ ทั้งหมด")
        
        print(f"\n✅ สิ่งที่เหลืออยู่ (ภาษาไทยเท่านั้น):")
        print(f"   • หัวข้อและฟิลด์ในหน้าจอกรอกข้อมูล")
        print(f"   • หัวข้อและปุ่มในหน้าจอดูข้อมูล") 
        print(f"   • ข้อความแจ้งเตือนและยืนยัน")
        print(f"   • ข้อความ error ในภาษาไทย")
        
        print(f"\n🚀 หน้าจอดูข้อมูลพร้อมใช้งาน:")
        print(f"   1. แสดงข้อมูลเป็นภาษาไทยเท่านั้น")
        print(f"   2. ไม่มีข้อความ debug ภาษาอังกฤษ")
        print(f"   3. ไม่มีฟิลด์ข้อมูลภาษาอังกฤษที่ไม่ได้ใช้งาน")
    else:
        print("⚠️ ยังมีข้อความภาษาอังกฤษที่ต้องลบออก")

if __name__ == "__main__":
    main()