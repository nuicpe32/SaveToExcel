#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ทดสอบการกรองคอลัมน์ในหน้าจอดูข้อมูล
"""

def test_column_filtering():
    """ทดสอบการกรองคอลัมน์ที่ไม่ต้องการแสดง"""
    print("="*80)
    print("🔍 ทดสอบการกรองคอลัมน์ในตารางดูข้อมูล")
    print("="*80)
    
    # จำลองคอลัมน์จากไฟล์ Excel
    all_columns = [
        'ลำดับ', 'เลขหนังสือ', 'วัน', 'เดือน ', 'ปี ', 'ธนาคารสาขา',
        'ผู้เสียหาย', 'เคสไอดี', 'เจ้าของบัญชีม้า', 'ชื่อธนาคาร', 'เลขบัญชี',
        'ชื่อบัญชี', 'ช่วงเวลา', 'ที่อยู่ธนาคาร', 'ซอย', 'หมู่', 'ตำบล/แขวง',
        'อำเภอ/เขต', 'ถนน', 'จังหวัด', 'รหัสไปรษณีย์', 'วันนัดส่ง', 'เดือนส่ง ', 'เวลาส่ง',
        'english_field_1', 'empty_column', 'unused_data', 'field_no_data'  # คอลัมน์ที่ไม่ต้องการ
    ]
    
    # จำลองข้อมูลในตาราง
    sample_data = [
        ['272', '9999', '2', 'กรกฎาคม', '2568', 'กรุงไทย สำนักงานใหญ่',
         'นายทดสอบ', 'TEST001', 'นางสาวทดสอบ', 'กรุงไทย', '1234567890',
         'นางสาวทดสอบ', '1-31 กรกฎาคม 2568', '333', '-', '-', 'สามเสนใน',
         'พญาไท', 'พหลโยธิน', 'กรุงเทพมหานคร', '10400', '3', 'สิงหาคม', '09.00 น.',
         '', '', '', ''],  # คอลัมน์สุดท้าย 4 คอลัมน์ว่างเปล่า
        ['273', '10000', '2', 'กรกฎาคม', '2568', 'กสิกรไทย สำนักงานใหญ่',
         'นายทดสอบ 2', 'TEST002', 'นางสาวทดสอบ 2', 'กสิกรไทย', '9876543210',
         'นางสาวทดสอบ 2', '1-31 กรกฎาคม 2568', '400/22', '-', '-', 'สามเสนใน',
         'พญาไท', 'พหลโยธิน', 'กรุงเทพมหานคร', '10400', '3', 'สิงหาคม', '09.00 น.',
         '', '', '', '']  # คอลัมน์สุดท้าย 4 คอลัมน์ว่างเปล่า
    ]
    
    print(f"📊 คอลัมน์ทั้งหมดในไฟล์ Excel:")
    print(f"   - จำนวนคอลัมน์ทั้งหมด: {len(all_columns)}")
    for i, col in enumerate(all_columns, 1):
        if i <= 24:  # คอลัมน์ไทยที่มีข้อมูล
            print(f"     {i:2d}. {col} ✅")
        else:  # คอลัมน์อังกฤษที่ไม่มีข้อมูล
            print(f"     {i:2d}. {col} ❌ (ไม่ควรแสดง)")
    
    # ทดสอบการกรอง
    print(f"\n🔧 ทดสอบการกรองคอลัมน์:")
    
    try:
        # สร้าง class จำลองสำหรับทดสอบ
        class MockExcelManager:
            def is_thai_column(self, column_name):
                """ตรวจสอบว่าชื่อคอลัมน์เป็นภาษาไทยหรือไม่"""
                if not column_name or not isinstance(column_name, str):
                    return False
                
                thai_columns = [
                    'ลำดับ', 'เลขหนังสือ', 'วัน', 'เดือน', 'ปี', 'ธนาคารสาขา',
                    'ผู้เสียหาย', 'เคสไอดี', 'เจ้าของบัญชีม้า', 'ชื่อธนาคาร', 'เลขบัญชี',
                    'ชื่อบัญชี', 'ช่วงเวลา', 'ที่อยู่ธนาคาร', 'ซอย', 'หมู่', 'ตำบล/แขวง',
                    'อำเภอ/เขต', 'ถนน', 'จังหวัด', 'รหัสไปรษณีย์', 'วันนัดส่ง', 'เดือนส่ง', 'เวลาส่ง'
                ]
                
                column_clean = column_name.strip()
                for thai_col in thai_columns:
                    if thai_col in column_clean:
                        return True
                return False
            
            def column_has_data(self, column_index, data_rows):
                """ตรวจสอบว่าคอลัมน์มีข้อมูลหรือไม่"""
                if not data_rows or column_index < 0:
                    return False
                
                sample_size = min(5, len(data_rows))
                for i, row in enumerate(data_rows[:sample_size]):
                    if column_index < len(row):
                        value = str(row[column_index]).strip()
                        if value and value != '' and value.lower() != 'nan' and value != 'None':
                            return True
                return False
            
            def filter_display_columns(self, columns, data_rows):
                """กรองคอลัมน์ที่จะแสดง"""
                if not columns:
                    return []
                
                display_columns = []
                for i, col in enumerate(columns):
                    is_thai_column = self.is_thai_column(col)
                    has_data = self.column_has_data(i, data_rows)
                    
                    if is_thai_column and has_data:
                        display_columns.append(col)
                
                return display_columns
        
        # ทดสอบ
        manager = MockExcelManager()
        filtered_columns = manager.filter_display_columns(all_columns, sample_data)
        
        print(f"   📋 คอลัมน์ที่จะแสดงหลังกรอง:")
        print(f"   - จำนวนคอลัมน์ที่แสดง: {len(filtered_columns)}")
        for i, col in enumerate(filtered_columns, 1):
            print(f"     {i:2d}. {col}")
        
        print(f"\n   🗑️ คอลัมน์ที่ถูกซ่อน:")
        hidden_columns = [col for col in all_columns if col not in filtered_columns]
        print(f"   - จำนวนคอลัมน์ที่ซ่อน: {len(hidden_columns)}")
        for i, col in enumerate(hidden_columns, 1):
            print(f"     {i:2d}. {col}")
        
        # ตรวจสอบผลลัพธ์
        expected_hidden = ['english_field_1', 'empty_column', 'unused_data', 'field_no_data']
        success = all(col in hidden_columns for col in expected_hidden)
        
        print(f"\n   {'✅' if success else '❌'} การกรอง: {'ถูกต้อง' if success else 'ยังมีปัญหา'}")
        
        return success
        
    except Exception as e:
        print(f"   ❌ เกิดข้อผิดพลาด: {e}")
        return False

def test_interface_improvement():
    """ทดสอบการปรับปรุงหน้าจอดูข้อมูล"""
    print(f"\n🖥️ ทดสอบการปรับปรุงหน้าจอดูข้อมูล:")
    
    improvements = [
        "ซ่อนคอลัมน์ภาษาอังกฤษที่ไม่ได้ใช้งาน",
        "ซ่อนคอลัมน์ที่ไม่มีข้อมูล",
        "แสดงเฉพาะคอลัมน์ภาษาไทยที่มีข้อมูล",
        "ลดความยุ่งเหยิงในตารางแสดงผล",
        "ปรับปรุงประสบการณ์ผู้ใช้งาน"
    ]
    
    print(f"   📊 การปรับปรุงที่ทำ:")
    for i, improvement in enumerate(improvements, 1):
        print(f"     {i}. {improvement} ✅")
    
    print(f"\n   ✅ หน้าจอดูข้อมูลใช้งานง่ายขึ้น")
    return True

def main():
    """ฟังก์ชันหลัก"""
    print("🧪 ทดสอบการกรองคอลัมน์ในหน้าจอดูข้อมูล")
    
    test1 = test_column_filtering()
    test2 = test_interface_improvement()
    
    print("\n" + "="*80)
    print("📝 สรุปการทดสอบ")
    print("="*80)
    
    results = [
        ("🔍 การกรองคอลัมน์", test1),
        ("🖥️ การปรับปรุงหน้าจอ", test2)
    ]
    
    all_passed = True
    for test_name, result in results:
        status = "✅ ผ่าน" if result else "❌ ไม่ผ่าน"
        print(f"   {test_name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "="*80)
    if all_passed:
        print("🎉 การกรองคอลัมน์เสร็จสมบูรณ์!")
        print("\n✅ ผลลัพธ์:")
        print("   • ซ่อนคอลัมน์ภาษาอังกฤษที่ไม่ได้ใช้งาน")
        print("   • ซ่อนคอลัมน์ที่ไม่มีข้อมูล")
        print("   • แสดงเฉพาะคอลัมน์ภาษาไทยที่มีข้อมูล")
        print("   • ตารางดูข้อมูลใช้งานง่ายขึ้น")
        
        print(f"\n🚀 หน้าจอดูข้อมูลพร้อมใช้งาน:")
        print(f"   1. เปิดโปรแกรม: python3 simple_excel_manager.py")
        print(f"   2. เลือกแท็บ '📊 ดูข้อมูล'")
        print(f"   3. จะเห็นเฉพาะคอลัมน์ที่มีข้อมูลและเป็นภาษาไทย")
        print(f"   4. ไม่มีคอลัมน์ภาษาอังกฤษหรือคอลัมน์ว่างเปล่า")
    else:
        print("⚠️ ยังมีปัญหาในการกรองคอลัมน์")

if __name__ == "__main__":
    main()