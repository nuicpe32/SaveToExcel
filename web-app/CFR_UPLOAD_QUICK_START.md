# คู่มือการใช้งานฟีเจอร์อัพโหลด CFR

**วันที่:** 11 ตุลาคม 2568

---

## 📋 สิ่งที่เสร็จสมบูรณ์

### ✅ **Backend**
1. **Database:**
   - สร้างตาราง `cfr` (30 columns)
   - สร้าง indexes สำหรับ performance
   - Migration: `018_create_cfr_table.sql`

2. **Models:**
   - `app/models/cfr.py` - CFR model
   - เพิ่ม relationship ใน `CriminalCase`

3. **API Endpoints:**
   - `POST /api/v1/cfr/upload/{case_id}` - อัพโหลดไฟล์
   - `GET /api/v1/cfr/{case_id}/files` - ดูรายการไฟล์
   - `GET /api/v1/cfr/{case_id}/records` - ดูข้อมูล
   - `DELETE /api/v1/cfr/{case_id}/file/{filename}` - ลบไฟล์

### ✅ **Frontend**
1. **UI Components:**
   - Tab "ข้อมูล CFR" ใน CriminalCaseDetailPage
   - Upload button (รองรับ .xlsx เท่านั้น)
   - แสดงรายการไฟล์ที่อัพโหลด
   - ปุ่มลบไฟล์ (พร้อม Confirm)

---

## 🎯 การใช้งาน

### **1. เข้าหน้ารายละเอียดคดี**
```
Dashboard → คลิก "ดูรายละเอียด" ของคดีที่ต้องการ
```

### **2. คลิก Tab "ข้อมูล CFR"**
```
Tabs: [บัญชีธนาคาร] [ผู้ต้องหา] [ข้อมูล CFR] ← คลิกที่นี่
```

### **3. อัพโหลดไฟล์**
```
1. คลิก "อัพโหลดไฟล์ CFR"
2. เลือกไฟล์ .xlsx จาก CFR System
3. รอระบบประมวลผล (3-5 วินาที)
4. แสดงข้อความ "อัพโหลดไฟล์ CFR สำเร็จ (เพิ่ม X รายการ)"
```

### **4. ดูรายการไฟล์**
```
┌─────────────────────────────────────────┐
│ 📊 cfr_25680923KBNK00407.xlsx         │
│    จำนวนรายการ: 1234 รายการ           │
│    อัพโหลดล่าสุด: 11/10/2568 14:00   │
│                              [ลบ]      │
└─────────────────────────────────────────┘
```

### **5. ลบไฟล์**
```
1. คลิกปุ่ม "ลบ" ข้างไฟล์
2. ยืนยันการลบ
3. ข้อมูลทั้งหมดจะถูกลบ
```

---

## ⚙️ ฟีเจอร์พิเศษ

### **1. Replace ไฟล์เดิม**
```
สถานการณ์:
- อัพโหลด "cfr_xxx.xlsx" ครั้งที่ 1 → เพิ่ม 100 records
- อัพโหลด "cfr_xxx.xlsx" ครั้งที่ 2 → ลบ 100 เดิม + เพิ่ม 150 ใหม่

ผลลัพธ์:
- ข้อมูลเดิมถูกลบ
- ข้อมูลใหม่ถูก insert แทน
- Total: 150 records
```

### **2. หลายไฟล์ต่อคดี**
```
1 คดี สามารถมีได้หลายไฟล์:
- cfr_file1.xlsx (1000 records)
- cfr_file2.xlsx (2000 records)
- cfr_file3.xlsx (500 records)

Total: 3500 records
```

### **3. ตรวจสอบประเภทไฟล์**
```
✅ รองรับ: .xlsx
❌ ไม่รองรับ: .xls, .csv, .pdf
```

---

## 📊 โครงสร้างไฟล์ Excel

### **ไฟล์ตัวอย่าง:**
```
C:\SaveToExcel\Xlsx\cfr_25680923KBNK00407.xlsx
```

### **Columns ที่ต้องมี:**
```
response_id, bank_case_id, timestamp_insert,
from_bank_code, from_bank_short_name, from_account_no, from_account_name,
to_bank_code, to_bank_short_name, to_bank_branch,
to_id_type, to_id, first_name, last_name, phone_number,
promptpay_type, promptpay_id,
to_account_no, to_account_name, to_account_status,
to_open_date, to_close_date, to_balance,
transfer_date, transfer_channel, transfer_channel_detail,
transfer_time, transfer_amount, transfer_description, transfer_ref
```

**หมายเหตุ:** ไฟล์ต้องมี header row และตรงกับชื่อ columns ข้างต้น

---

## 🐛 Troubleshooting

### **ปัญหา: อัพโหลดไม่สำเร็จ**

**สาเหตุที่เป็นไปได้:**
1. ❌ ไฟล์ไม่ใช่ .xlsx
2. ❌ Columns ในไฟล์ไม่ตรง
3. ❌ ไฟล์เสียหาย
4. ❌ ขนาดไฟล์ใหญ่เกินไป (> 100 MB)

**วิธีแก้:**
1. ✅ ตรวจสอบนามสกุลไฟล์
2. ✅ ตรวจสอบ header columns
3. ✅ ลองเปิดไฟล์ใน Excel ก่อน
4. ✅ แบ่งไฟล์ใหญ่เป็นหลายไฟล์

---

### **ปัญหา: ไม่เห็นไฟล์ที่อัพโหลด**

**วิธีแก้:**
1. ✅ Refresh หน้าเว็บ (F5)
2. ✅ ตรวจสอบ Backend logs
3. ✅ ตรวจสอบฐานข้อมูล

---

### **ปัญหา: ลบไฟล์แล้วยังเห็นอยู่**

**วิธีแก้:**
1. ✅ Refresh หน้าเว็บ
2. ✅ Logout/Login ใหม่

---

## 📈 Performance

### **ความเร็วการอัพโหลด:**
| จำนวน Records | เวลา (โดยประมาณ) |
|--------------|------------------|
| 100 rows     | 1-2 วินาที       |
| 1,000 rows   | 3-5 วินาที       |
| 10,000 rows  | 30-50 วินาที     |
| 100,000 rows | 5-10 นาที        |

### **ขนาดไฟล์:**
| จำนวน Records | ขนาดไฟล์ (โดยประมาณ) |
|--------------|----------------------|
| 1,000 rows   | 200-500 KB          |
| 10,000 rows  | 2-5 MB              |
| 100,000 rows | 20-50 MB            |

---

## 🎓 Tips & Best Practices

### **1. การตั้งชื่อไฟล์**
```
✅ ดี:     cfr_25680923KBNK00407.xlsx
✅ ดี:     cfr_caseid_12345_20251011.xlsx
❌ ไม่ดี: file1.xlsx
❌ ไม่ดี: ไฟล์ใหม่.xlsx (มี Unicode)
```

### **2. การจัดการไฟล์ใหญ่**
```
ถ้าไฟล์มี > 50,000 rows:
1. แบ่งเป็นหลายไฟล์
2. ตั้งชื่อแบบ: cfr_xxx_part1.xlsx, cfr_xxx_part2.xlsx
3. อัพโหลดทีละไฟล์
```

### **3. การอัพเดตข้อมูล**
```
เมื่อได้ข้อมูลใหม่จาก CFR:
1. อัพโหลดชื่อไฟล์เดิม → ระบบจะ replace อัตโนมัติ
2. หรือลบไฟล์เดิม แล้วอัพโหลดใหม่
```

---

## 🔍 การตรวจสอบข้อมูล

### **ตรวจสอบในฐานข้อมูล:**
```sql
-- ดูจำนวนไฟล์
SELECT criminal_case_id, filename, COUNT(*) as record_count
FROM cfr
GROUP BY criminal_case_id, filename;

-- ดูข้อมูลล่าสุด
SELECT * FROM cfr
WHERE criminal_case_id = 1
ORDER BY upload_date DESC
LIMIT 10;

-- ดูข้อมูลตาม filename
SELECT * FROM cfr
WHERE criminal_case_id = 1
  AND filename = 'cfr_xxx.xlsx';
```

---

## ✅ Checklist

### **ก่อนอัพโหลด:**
- [ ] ตรวจสอบว่าไฟล์เป็น .xlsx
- [ ] เปิดไฟล์ใน Excel ได้
- [ ] มี header row
- [ ] Columns ตรงตามที่กำหนด
- [ ] ข้อมูลไม่มี error

### **หลังอัพโหลด:**
- [ ] เห็นไฟล์ในรายการ
- [ ] จำนวน records ถูกต้อง
- [ ] วันเวลาอัพโหลดถูกต้อง

---

## 📞 ติดต่อ

**มีปัญหาหรือข้อสงสัย:**
- ตรวจสอบ Backend logs
- ดู Browser console
- ตรวจสอบฐานข้อมูล

---

## 🎉 สรุป

**ฟีเจอร์อัพโหลด CFR พร้อมใช้งานแล้ว!**

✅ อัพโหลดไฟล์ Excel จาก CFR System  
✅ เก็บข้อมูลเส้นทางการเงิน  
✅ Replace ไฟล์เดิมอัตโนมัติ  
✅ ลบไฟล์และข้อมูลได้  
✅ พร้อมนำข้อมูลมาวิเคราะห์ต่อ  

**เริ่มใช้งานได้เลย!** 🚀

---

**หมายเหตุ:** ยังไม่ได้ commit ขึ้น Git ตามคำสั่ง

