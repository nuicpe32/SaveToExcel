# Changelog - Version 3.2.0

**วันที่:** 9 ตุลาคม 2568  
**ชื่อเวอร์ชัน:** Database Cleanup & Feature Enhancement

---

## 🎯 สรุปการเปลี่ยนแปลงหลัก

### **1. Database Structure Optimization**
- ✅ ลบฟิลด์ที่ไม่ได้ใช้งาน 17 ฟิลด์จากตาราง `criminal_cases`
- ✅ เพิ่ม `charge_id` ในตาราง `suspects` เพื่อรองรับ Master Data ในอนาคต
- ✅ เพิ่ม COMMENT (หมายเหตุ) ให้ทุกคอลัมน์ในฐานข้อมูล

### **2. Virtual Fields Implementation**
- ✅ แปลง 4 ฟิลด์เป็น Virtual Fields (คำนวณ runtime)
- ✅ ลด database size และความซับซ้อน
- ✅ ข้อมูล realtime และถูกต้องเสมอ

### **3. Complainant Field Standardization**
- ✅ ใช้ `complainant` เป็นฟิลด์เดียวสำหรับผู้เสียหาย
- ✅ แก้ไขปัญหาข้อมูล "ดำเนินคดี" ในหมายเรียก

### **4. Bank Freeze Account Feature**
- ✅ เพิ่มฟีเจอร์เลือก "อายัดบัญชี" หรือ "ไม่อายัดบัญชี"
- ✅ Modal popup ให้เลือกก่อนพิมพ์หมายเรียก
- ✅ แบบฟอร์มแตกต่างกันตามประเภท

### **5. Case Type Addition**
- ✅ เพิ่มประเภทคดี "17.พนันออนไลน์"

### **6. UI/UX Improvements**
- ✅ แสดงจำนวนบัญชี/ผู้ต้องหา รูปแบบ "ทั้งหมด/ตอบกลับ"
- ✅ ปรับ Layout หมายเรียกให้พอดี 1 หน้ากระดาษ

---

## 📊 Database Changes

### **ตาราง criminal_cases - ฟิลด์ที่ลบออก (17 ฟิลด์):**

#### Group 1: ไม่ได้ใช้งานเลย
1. ❌ `victim_name` - ใช้ `complainant` แทน
2. ❌ `suspect` - ใช้ตาราง `suspects` แทน
3. ❌ `case_scene` - ไม่ได้ใช้
4. ❌ `age_in_months` - คำนวณ dynamic
5. ❌ `is_over_six_months` - คำนวณ dynamic

#### Group 2: ไม่แสดงใน UI
6. ❌ `charge` - ย้ายเป็น `charge_id` ในตาราง `suspects`
7. ❌ `prosecutor_name`
8. ❌ `prosecutor_file_number`
9. ❌ `officer_in_charge`
10. ❌ `investigating_officer`
11. ❌ `bank_accounts_replied`
12. ❌ `suspects_replied`

#### Group 3: Virtual Fields
13. ❌ `complaint_date_thai` - คำนวณจาก `complaint_date`
14. ❌ `incident_date_thai` - คำนวณจาก `incident_date`
15. ❌ `bank_accounts_count` - คำนวณจาก query
16. ❌ `suspects_count` - คำนวณจาก query

#### Group 4: เพิ่มเติม
17. ❌ `notes` - ไม่ได้ใช้

### **ตาราง criminal_cases - ฟิลด์ที่เหลือ (15 ฟิลด์):**
1. ✅ `id` - Primary Key
2. ✅ `case_number` - เลขที่คดี
3. ✅ `case_id` - รหัสคดี
4. ✅ `status` - สถานะ
5. ✅ `complainant` - ผู้เสียหาย/ผู้กล่าวหา
6. ✅ `case_type` - ประเภทคดี
7. ✅ `damage_amount` - มูลค่าความเสียหาย
8. ✅ `complaint_date` - วันที่ร้องทุกข์
9. ✅ `incident_date` - วันที่เกิดเหตุ
10. ✅ `last_update_date` - วันที่อัพเดต
11. ✅ `court_name` - ศาล
12. ✅ `created_at` - วันที่สร้าง
13. ✅ `updated_at` - วันที่แก้ไข
14. ✅ `created_by` - ผู้สร้าง
15. ✅ `owner_id` - เจ้าของคดี

### **ตาราง suspects - ฟิลด์ที่เพิ่ม:**
- ✅ `charge_id` - FK เชื่อมกับ Master Data ข้อหา (ใช้ในอนาคต)

---

## 🔧 Backend Changes

### **ไฟล์ใหม่:**
- ✅ `app/utils/virtual_fields.py` - Utility functions สำหรับ virtual fields
- ✅ `migrations/010_sync_complainant_victim_name.sql` - Sync complainant data
- ✅ `migrations/011_remove_unused_fields.sql` - ลบฟิลด์ที่ไม่ใช้
- ✅ `migrations/012_add_column_comments.sql` - เพิ่ม comments

### **ไฟล์ที่แก้ไข:**
- ✅ `app/models/criminal_case.py` - ลบฟิลด์ที่ไม่ใช้
- ✅ `app/models/suspect.py` - เพิ่ม `charge_id`
- ✅ `app/schemas/criminal_case.py` - ปรับ schemas, เพิ่ม virtual fields
- ✅ `app/schemas/suspect.py` - เพิ่ม `charge_id`
- ✅ `app/api/v1/criminal_cases.py` - ใช้ virtual fields
- ✅ `app/api/v1/documents.py` - ใช้ `complainant`, รับ `freeze_account` parameter
- ✅ `app/api/v1/case_types.py` - เพิ่ม "17.พนันออนไลน์"
- ✅ `app/services/bank_summons_generator.py` - รองรับอายัดบัญชี, ปรับ layout

---

## 🎨 Frontend Changes

### **ไฟล์ที่แก้ไข:**
- ✅ `pages/CriminalCaseDetailPage.tsx` - เพิ่ม Modal เลือกอายัดบัญชี, ใช้ `complainant`
- ✅ `pages/DashboardPage.tsx` - เพิ่ม Modal เลือกอายัดบัญชี
- ✅ `pages/BankAccountsPage.tsx` - ใช้ `complainant`
- ✅ `pages/SuspectsPage.tsx` - ใช้ `complainant`

---

## 📋 New Features

### **1. Bank Account Freeze Option**

เมื่อกดปุ่ม "ปริ้นหมายเรียก" จะแสดง Modal ให้เลือก:

**ตัวเลือก 1: อายัดบัญชี**
- เรื่อง: ให้ทำการอายัดบัญชี,จัดส่งสำเนาคำร้องเปิดบัญชีธนาคาร,รายการเดินบัญชีและข้อมูลอื่น ๆ
- ข้อ 3: เพิ่ม "(กรณีข้อมูลจำนวนมากให้นำส่ง 10 รายการล่าสุด)"
- ข้อ 5: ให้ท่านอายัดบัญชีดังกล่าวและแจ้งผลการอายัดบัญชี พร้อมยอดเงินคงเหลือ

**ตัวเลือก 2: ไม่อายัดบัญชี**
- ใช้แบบฟอร์มเดิมทุกอย่าง

### **2. Virtual Fields**

ฟิลด์เหล่านี้คำนวณแบบ dynamic (ไม่เก็บในฐานข้อมูล):
- `complaint_date_thai` - แปลงจาก `complaint_date`
- `incident_date_thai` - แปลงจาก `incident_date`
- `bank_accounts_count` - นับจากตาราง `bank_accounts`
- `suspects_count` - นับจากตาราง `suspects`

### **3. Complainant Standardization**

- ใช้ `complainant` เป็นฟิลด์เดียวสำหรับผู้เสียหาย/ผู้กล่าวหา
- แก้ไขปัญหา "ดำเนินคดี" ในหมายเรียก

### **4. Case Type Addition**

เพิ่มประเภทคดี:
- **17.พนันออนไลน์**

---

## 🔄 Migration Files

1. `010_sync_complainant_victim_name.sql` - Sync complainant data
2. `011_remove_unused_fields.sql` - ลบฟิลด์ 17 ฟิลด์, เพิ่ม charge_id
3. `012_add_column_comments.sql` - เพิ่ม comments ทุกคอลัมน์

---

## 📦 Deployment

### **1. Backup Database**
```bash
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_v3.2.0.dump
docker cp criminal-case-db:/tmp/backup_v3.2.0.dump ./backup_v3.2.0.dump
```

### **2. Pull Latest Code**
```bash
git pull origin main
```

### **3. Restart Services**
```bash
docker-compose restart backend frontend
```

---

## ✅ Verification

- ✅ ฐานข้อมูลสะอาดขึ้น (ลบ 17 ฟิลด์)
- ✅ โปรแกรมทำงานได้เหมือนเดิม 100%
- ✅ ฟีเจอร์ใหม่: เลือกอายัดบัญชี
- ✅ หมายเรียกพอดี 1 หน้ากระดาษ
- ✅ ประเภทคดีมี 17 ประเภท

---

## 📞 Contact

**Version:** 3.2.0  
**Release Date:** 9 ตุลาคม 2568  
**Status:** ✅ Production Ready

---

## 🔐 Security Notes

- ✅ ข้อมูลไม่หาย (มี backup)
- ✅ Backward compatible
- ✅ Virtual fields คำนวณ realtime
- ✅ Database comments เพิ่มแล้ว

**Upgrade จาก v3.1.1 → v3.2.0 สำเร็จ!** 🚀

