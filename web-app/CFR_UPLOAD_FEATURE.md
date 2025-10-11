# ฟีเจอร์อัพโหลดไฟล์ CFR (Central Fraud Registry)

**วันที่:** 11 ตุลาคม 2568

---

## 🎯 ภาพรวม

ระบบรองรับการอัพโหลดไฟล์ CFR (Central Fraud Registry) เพื่อเก็บข้อมูลเส้นทางการเงิน/รายการโอนเงินของคดี

### **สิ่งที่ทำได้:**
- ✅ อัพโหลดไฟล์ Excel (.xlsx) จาก CFR System
- ✅ เก็บข้อมูลเส้นทางการเงินในฐานข้อมูล
- ✅ 1 คดี สามารถอัพโหลดได้หลายไฟล์
- ✅ อัพโหลดชื่อไฟล์ซ้ำ → ลบข้อมูลเดิม + นำเข้าใหม่
- ✅ ดูรายการไฟล์ที่อัพโหลด
- ✅ ลบไฟล์ CFR และข้อมูลทั้งหมด

---

## 📊 โครงสร้างตาราง CFR

### **ตาราง: `cfr`**

```sql
CREATE TABLE cfr (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    
    -- File Information
    filename VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- CFR Response Data
    response_id BIGINT,
    bank_case_id VARCHAR(100),
    timestamp_insert VARCHAR(50),
    
    -- From Account (ต้นทาง)
    from_bank_code INTEGER,
    from_bank_short_name VARCHAR(50),
    from_account_no VARCHAR(50),
    from_account_name VARCHAR(255),
    
    -- To Account (ปลายทาง)
    to_bank_code INTEGER,
    to_bank_short_name VARCHAR(50),
    to_bank_branch VARCHAR(100),
    to_id_type VARCHAR(50),
    to_id VARCHAR(50),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(50),
    
    -- PromptPay
    promptpay_type VARCHAR(50),
    promptpay_id VARCHAR(50),
    
    -- To Account Details
    to_account_no VARCHAR(50),
    to_account_name VARCHAR(255),
    to_account_status VARCHAR(50),
    to_open_date VARCHAR(50),
    to_close_date VARCHAR(50),
    to_balance DECIMAL(15, 2),
    
    -- Transfer Information
    transfer_date VARCHAR(50),
    transfer_channel VARCHAR(100),
    transfer_channel_detail VARCHAR(255),
    transfer_time VARCHAR(50),
    transfer_amount DECIMAL(15, 2),
    transfer_description TEXT,
    transfer_ref VARCHAR(100),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by INTEGER
);
```

### **Indexes:**
- `criminal_case_id` - เร็วในการค้นหาตามคดี
- `filename` - เร็วในการค้นหาตามชื่อไฟล์
- `from_account_no`, `to_account_no` - เร็วในการค้นหาบัญชี
- `transfer_date` - เร็วในการเรียงลำดับตามวันที่
- `(criminal_case_id, filename)` - เร็วในการลบข้อมูลไฟล์เดิม

---

## 🔧 API Endpoints

### **1. Upload CFR File**
```
POST /api/v1/cfr/upload/{criminal_case_id}
Content-Type: multipart/form-data
```

**Parameters:**
- `criminal_case_id` - รหัสคดี
- `file` - ไฟล์ Excel (.xlsx)

**Response:**
```json
{
  "message": "อัพโหลดไฟล์ CFR สำเร็จ",
  "filename": "cfr_25680923KBNK00407.xlsx",
  "records_inserted": 1234,
  "records_deleted": 0
}
```

**Logic:**
1. ตรวจสอบว่าคดีมีอยู่จริง
2. ตรวจสอบว่าเป็นไฟล์ .xlsx
3. อ่านข้อมูลด้วย pandas
4. ตรวจสอบชื่อไฟล์ซ้ำ → ลบข้อมูลเดิมก่อน
5. Insert ข้อมูลใหม่ทุก row
6. Return จำนวน insert และ delete

---

### **2. Get CFR Files**
```
GET /api/v1/cfr/{criminal_case_id}/files
```

**Response:**
```json
[
  {
    "filename": "cfr_25680923KBNK00407.xlsx",
    "record_count": 1234,
    "last_upload": "2025-10-11T14:00:00+07:00"
  }
]
```

---

### **3. Get CFR Records**
```
GET /api/v1/cfr/{criminal_case_id}/records?filename=xxx&skip=0&limit=100
```

**Parameters:**
- `filename` (optional) - กรองตามชื่อไฟล์
- `skip` - pagination offset
- `limit` - pagination limit

**Response:**
```json
{
  "records": [...],
  "total": 1234
}
```

---

### **4. Delete CFR File**
```
DELETE /api/v1/cfr/{criminal_case_id}/file/{filename}
```

**Response:**
```json
{
  "message": "ลบไฟล์ cfr_xxx.xlsx สำเร็จ",
  "records_deleted": 1234
}
```

---

## 🎨 Frontend UI

### **หน้า: Criminal Case Detail Page**

**URL:** `/case/{id}`

### **Tab: ข้อมูล CFR**

```
┌─────────────────────────────────────────────────┐
│ อัพโหลดไฟล์ CFR (Central Fraud Registry)       │
│ อัพโหลดไฟล์ข้อมูลเส้นทางการเงิน (.xlsx)       │
│ หากชื่อไฟล์ซ้ำ ระบบจะลบเดิมและนำเข้าใหม่      │
│                                                 │
│ [🔼 อัพโหลดไฟล์ CFR]                          │
│                                                 │
│ ไฟล์ที่อัพโหลดแล้ว                              │
│ ┌─────────────────────────────────────────────┐ │
│ │ 📊 cfr_25680923KBNK00407.xlsx              │ │
│ │    จำนวนรายการ: 1234 รายการ                │ │
│ │    อัพโหลดล่าสุด: 11/10/2568 14:00        │ │
│ │                              [ลบ] ────────┘ │
│ └─────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────┘
```

### **ฟีเจอร์:**
1. **ปุ่มอัพโหลด** - เลือกไฟล์ .xlsx และอัพโหลด
2. **แสดง Loading** - ระหว่างอัพโหลด
3. **แสดงรายการไฟล์** - ชื่อไฟล์, จำนวนรายการ, วันเวลา
4. **ปุ่มลบ** - ลบไฟล์และข้อมูล (มี Confirm dialog)

---

## 📝 รูปแบบไฟล์ Excel

### **ไฟล์ตัวอย่าง:**
```
C:\SaveToExcel\Xlsx\cfr_25680923KBNK00407.xlsx
```

### **Columns (30 คอลัมน์):**
1. `response_id` - Response ID
2. `bank_case_id` - Bank Case ID
3. `timestamp_insert` - Timestamp
4. `from_bank_code` - รหัสธนาคารต้นทาง
5. `from_bank_short_name` - ชื่อย่อธนาคารต้นทาง
6. `from_account_no` - เลขบัญชีต้นทาง
7. `from_account_name` - ชื่อบัญชีต้นทาง
8. `to_bank_code` - รหัสธนาคารปลายทาง
9. `to_bank_short_name` - ชื่อย่อธนาคารปลายทาง
10. `to_bank_branch` - สาขาธนาคาร
11. `to_id_type` - ประเภทบัตร
12. `to_id` - เลขบัตร
13. `first_name` - ชื่อ
14. `last_name` - นามสกุล
15. `phone_number` - เบอร์โทร
16. `promptpay_type` - ประเภท PromptPay
17. `promptpay_id` - รหัส PromptPay
18. `to_account_no` - เลขบัญชีปลายทาง
19. `to_account_name` - ชื่อบัญชีปลายทาง
20. `to_account_status` - สถานะบัญชี
21. `to_open_date` - วันเปิดบัญชี
22. `to_close_date` - วันปิดบัญชี
23. `to_balance` - ยอดเงินคงเหลือ
24. `transfer_date` - วันที่โอน
25. `transfer_channel` - ช่องทางโอน (EBank, Mobile)
26. `transfer_channel_detail` - รายละเอียดช่องทาง
27. `transfer_time` - เวลาโอน
28. `transfer_amount` - จำนวนเงิน
29. `transfer_description` - คำอธิบาย
30. `transfer_ref` - เลขอ้างอิง

---

## 🔄 Logic การอัพโหลดชื่อไฟล์ซ้ำ

### **สถานการณ์:**
1. User อัพโหลด `cfr_xxx.xlsx` ครั้งแรก → Insert 100 records
2. User อัพโหลด `cfr_xxx.xlsx` อีกครั้ง (ไฟล์ใหม่ แต่ชื่อเดิม)

### **ระบบทำงาน:**
```python
# 1. ตรวจสอบว่ามีไฟล์ชื่อนี้หรือไม่
existing_records = db.query(CFR).filter(
    CFR.criminal_case_id == case_id,
    CFR.filename == "cfr_xxx.xlsx"
).all()

# 2. ถ้ามี → ลบทั้งหมดก่อน
if existing_records:
    for record in existing_records:
        db.delete(record)
    db.commit()

# 3. Insert ข้อมูลใหม่
for row in new_data:
    cfr_record = CFR(...)
    db.add(cfr_record)
db.commit()
```

### **ผลลัพธ์:**
- ❌ ลบข้อมูลเดิม 100 records
- ✅ Insert ข้อมูลใหม่ 150 records
- 📊 Total: 150 records

---

## 🧪 การทดสอบ

### **Test Case 1: อัพโหลดไฟล์ใหม่**

**ขั้นตอน:**
1. เข้าหน้ารายละเอียดคดี
2. คลิก Tab "ข้อมูล CFR"
3. คลิก "อัพโหลดไฟล์ CFR"
4. เลือกไฟล์ `cfr_25680923KBNK00407.xlsx`

**ผลลัพธ์:**
- ✅ แสดง "อัพโหลดไฟล์ CFR สำเร็จ (เพิ่ม 1234 รายการ)"
- ✅ ไฟล์ปรากฏในรายการ
- ✅ แสดงจำนวนรายการและวันเวลา

---

### **Test Case 2: อัพโหลดชื่อไฟล์ซ้ำ**

**ขั้นตอน:**
1. อัพโหลด `cfr_xxx.xlsx` ครั้งแรก (100 records)
2. อัพโหลด `cfr_xxx.xlsx` อีกครั้ง (150 records)

**ผลลัพธ์:**
- ✅ แสดง "อัพโหลดไฟล์ CFR สำเร็จ (เพิ่ม 150 รายการ)"
- ✅ ข้อมูลเดิม 100 records ถูกลบ
- ✅ ข้อมูลใหม่ 150 records ถูก insert
- ✅ ในฐานข้อมูลมีเพียง 150 records

---

### **Test Case 3: ลบไฟล์**

**ขั้นตอน:**
1. คลิกปุ่ม "ลบ" ข้างไฟล์
2. ยืนยันการลบ

**ผลลัพธ์:**
- ✅ แสดง Confirm dialog "จะลบข้อมูล 1234 รายการ"
- ✅ คลิก "ใช่" → ลบไฟล์และข้อมูลทั้งหมด
- ✅ แสดง "ลบไฟล์ CFR สำเร็จ"
- ✅ ไฟล์หายจากรายการ

---

### **Test Case 4: อัพโหลดไฟล์ผิดประเภท**

**ขั้นตอน:**
1. พยายามอัพโหลดไฟล์ `.pdf` หรือ `.csv`

**ผลลัพธ์:**
- ❌ ระบบแสดง error "รองรับเฉพาะไฟล์ .xlsx เท่านั้น"

---

## 📦 Database Relations

```
criminal_cases (1) ──┐
                     │
                     ├─> bank_accounts (N)
                     ├─> suspects (N)
                     └─> cfr (N)  ← NEW!
```

### **Cascade Delete:**
- ถ้าลบคดี → ลบข้อมูล CFR ทั้งหมดด้วย (`ON DELETE CASCADE`)

---

## 🎯 Use Cases

### **1. วิเคราะห์เส้นทางการเงิน**
- ดูว่าเงินไหลจากบัญชีไหน → บัญชีไหน
- หาบัญชีกลาง (hub accounts)
- วิเคราะห์รูปแบบการโอนเงิน

### **2. สืบค้นข้อมูล**
- ค้นหาบัญชีที่เกี่ยวข้องกับคดี
- ค้นหาเบอร์โทรศัพท์
- ค้นหาชื่อ-นามสกุล

### **3. Export ข้อมูล**
- ดึงข้อมูลจากฐานข้อมูลเพื่อสร้างรายงาน
- Export ไปยังเครื่องมือวิเคราะห์อื่นๆ

---

## 🚀 Next Steps

### **ฟีเจอร์ที่จะพัฒนาต่อ:**
1. ✨ แสดงข้อมูล CFR ในรูปแบบตาราง
2. ✨ ค้นหาและกรองข้อมูล CFR
3. ✨ Export ข้อมูล CFR เป็น Excel
4. ✨ Visualize เส้นทางการเงินเป็น Network Graph
5. ✨ วิเคราะห์หาบัญชีกลาง (Hub Detection)
6. ✨ แจ้งเตือนเมื่อพบบัญชีซ้ำในคดีอื่น

---

## 📊 สถิติและประสิทธิภาพ

### **Performance:**
- Upload ไฟล์ 1,000 rows ≈ 3-5 วินาที
- Upload ไฟล์ 10,000 rows ≈ 30-50 วินาที
- ค้นหาข้อมูลด้วย index ≈ < 100ms

### **Storage:**
- 1 row ≈ 1-2 KB
- 1,000 rows ≈ 1-2 MB
- 100,000 rows ≈ 100-200 MB

---

## ✅ Summary

**ระบบอัพโหลด CFR พร้อมแล้ว!**

- ✅ Database table `cfr` สร้างเรียบร้อย
- ✅ Backend API endpoints พร้อมใช้งาน
- ✅ Frontend UI พร้อมใช้งาน
- ✅ Upload, Delete, List files ทำงานได้
- ✅ รองรับการอัพโหลดไฟล์ซ้ำ (replace)

**พร้อมเก็บข้อมูลเส้นทางการเงินและนำมาประมวลผลต่อไป!** 🎉

---

**หมายเหตุ:** ยังไม่ได้ commit ขึ้น Git ตามคำสั่ง

