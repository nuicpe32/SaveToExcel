# รายงานการปรับปรุงโครงสร้างฐานข้อมูล: Bank Normalization

**วันที่:** 2025-10-01
**เวอร์ชัน:** Database Schema v3.0

---

## 📋 สรุปการดำเนินการ

### ✅ สิ่งที่ทำสำเร็จ

1. **สร้างตาราง `banks`** - ตารางหลักสำหรับข้อมูลธนาคารในประเทศไทย
2. **เพิ่ม Foreign Key `bank_id`** ในตาราง `bank_accounts`
3. **Migrate ข้อมูลเดิม** - อัพเดต 406 รายการให้อ้างอิงกับตารางใหม่
4. **สร้าง Backend API** - `/api/v1/banks/` สำหรับจัดการข้อมูลธนาคาร
5. **สร้าง Models และ Schemas** สำหรับ Bank entity

---

## 🗃️ โครงสร้างฐานข้อมูลใหม่

### ตาราง `banks` (Master Data)

```sql
CREATE TABLE banks (
    id SERIAL PRIMARY KEY,
    bank_name VARCHAR(255) NOT NULL UNIQUE,
    bank_address VARCHAR(500),
    soi VARCHAR(100),
    moo VARCHAR(50),
    road VARCHAR(100),
    sub_district VARCHAR(100),
    district VARCHAR(100),
    province VARCHAR(100),
    postal_code VARCHAR(10),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### ตาราง `bank_accounts` (Updated)

เพิ่มคอลัมน์:
```sql
ALTER TABLE bank_accounts
ADD COLUMN bank_id INTEGER REFERENCES banks(id) ON DELETE SET NULL;
```

---

## 📊 ข้อมูลธนาคารทั้งหมด (13 ธนาคาร)

| ID | ชื่อธนาคาร | ที่อยู่ | อำเภอ/เขต | จังหวัด |
|----|-----------|---------|-----------|---------|
| 1 | กสิกรไทย | 400/22 พหลโยธิน | พญาไท | กรุงเทพมหานคร |
| 2 | ไทยพาณิชย์ | 9 รัชดาภิเษก | จตุจักร | กรุงเทพมหานคร |
| 3 | ทหารไทยธนชาต | 3000 พหลโยธิน | จตุจักร | กรุงเทพมหานคร |
| 4 | ยูโอบี | 690 สุขุมวิท | คลองเตย | กรุงเทพมหานคร |
| 5 | กรุงเทพ | 333 สีลม | บางรัก | กรุงเทพมหานคร |
| 6 | กรุงศรีอยุธยา | 1222 พระรามที่ 3 | ยานนาวา | กรุงเทพมหานคร |
| 7 | ออมสิน | 470 พหลโยธิน | พญาไท | กรุงเทพมหานคร |
| 8 | กรุงไทย | อาคาร 1 เลขที่ 35 สุขุมวิท | วัฒนา | กรุงเทพมหานคร |
| 9 | ซีไอเอ็มบีไทย | 44 หลังสวน | ปทุมวัน | กรุงเทพมหานคร |
| 10 | อาคารสงเคราะห์ | 63 พระราม 9 | ห้วยขวาง | กรุงเทพมหานคร |
| 11 | แลนด์แอนด์เฮ้าส์ | เลขที่ 1 อาคารคิวเฮ้าส์ ลุมพินี ชั้น 5 สาทรใต้ | สาทร | กรุงเทพมหานคร |
| 12 | เพื่อการเกษตรและสหกรณ์การเกษตร (ธ.ก.ส.) | 2346 พหลโยธิน | จตุจักร | กรุงเทพมหานคร |
| 13 | เกียรตินาคินภัทร | 209 อาคารเคเคพี ทาวเวอร์ สุขุมวิท 21 (อโศก) | วัฒนา | กรุงเทพมหานคร |

---

## 🔄 ผลการ Migrate ข้อมูล

### สถิติ

- **รายการทั้งหมดใน bank_accounts:** 417 รายการ
- **✅ Matched และ update สำเร็จ:** 406 รายการ (97.4%)
- **⚠️ NULL/NaN values (ข้อมูลว่าง):** 11 รายการ (2.6%)
- **❌ Unmatched (ไม่พบในตารางธนาคาร):** 0 รายการ

### การ Normalize ชื่อธนาคาร

ระบบได้ทำการ normalize ชื่อธนาคารที่มีช่องว่างหรือการสะกดแตกต่างกัน:

| ชื่อเดิม (ใน bank_accounts) | ชื่อที่ Normalize | สถานะ |
|----------------------------|------------------|-------|
| กสิกรไทย | กสิกรไทย | ✅ Match |
| ทหารไทยธนชาต | ทหารไทยธนชาต | ✅ Match |
| ทหารไทยธนชาต  | ทหารไทยธนชาต | ✅ Match (trim space) |
| ซีไอเอ็มบี | ซีไอเอ็มบีไทย | ✅ Match |
| ซีไอเอ็มบี ไทย | ซีไอเอ็มบีไทย | ✅ Match |
| ซีไอเอ็มบี ไทย  | ซีไอเอ็มบีไทย | ✅ Match (trim space) |
| ซีไอเอ็มบีไทย | ซีไอเอ็มบีไทย | ✅ Match |
| แลนด์ แอนด์ เฮ้าส์ | แลนด์แอนด์เฮ้าส์ | ✅ Match |
| แลนด์แอนด์เฮ้าส์ | แลนด์แอนด์เฮ้าส์ | ✅ Match |
| nan | NULL | ⚠️ Set to NULL (11 records) |

---

## 📁 ไฟล์ที่สร้าง/แก้ไข

### Backend

| ไฟล์ | สถานะ | คำอธิบาย |
|------|-------|---------|
| `backend/app/models/bank.py` | ✅ สร้างใหม่ | Bank model |
| `backend/app/models/bank_account.py` | ✅ แก้ไข | เพิ่ม bank_id FK และ relationship |
| `backend/app/models/__init__.py` | ✅ แก้ไข | Import Bank model |
| `backend/app/schemas/bank.py` | ✅ สร้างใหม่ | Bank schemas (Base, Create, Update, Response) |
| `backend/app/api/v1/endpoints/banks.py` | ✅ สร้างใหม่ | Banks API endpoints |
| `backend/app/api/v1/__init__.py` | ✅ แก้ไข | Register banks router |

### Migration Script

| ไฟล์ | สถานะ | คำอธิบาย |
|------|-------|---------|
| `migration_add_banks_table.py` | ✅ สร้างใหม่ | Migration script สำหรับสร้างตารางและ migrate ข้อมูล |

### Data Source

| ไฟล์ | คำอธิบาย |
|------|---------|
| `bank_master_data.xlsx` | Excel file ที่มีข้อมูลธนาคาร 13 แห่ง |

---

## 🔌 API Endpoints ใหม่

### Banks API

**Base URL:** `/api/v1/banks/`

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Get all banks | No |
| GET | `/{bank_id}` | Get bank by ID | No |
| POST | `/` | Create new bank | Yes (Admin) |
| PUT | `/{bank_id}` | Update bank | Yes (Admin) |
| DELETE | `/{bank_id}` | Delete bank | Yes (Admin) |

**ตัวอย่างการใช้งาน:**

```bash
# Get all banks
curl http://localhost:8000/api/v1/banks/

# Get specific bank
curl http://localhost:8000/api/v1/banks/1

# Create new bank (requires auth token)
curl -X POST http://localhost:8000/api/v1/banks/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "bank_name": "ธนาคารทดสอบ",
    "bank_address": "123 ถนนทดสอบ",
    "district": "เขตทดสอบ",
    "province": "กรุงเทพมหานคร",
    "postal_code": "10000"
  }'
```

---

## ⚠️ รายการที่ต้องดำเนินการต่อ

### 1. ข้อมูล bank_accounts ที่ยังไม่มี bank_id (11 รายการ)

รายการเหล่านี้มีค่า `bank_name = 'nan'` ซึ่งหมายความว่าไม่มีการระบุชื่อธนาคารตั้งแต่แรก

**วิธีแก้ไข:**
```sql
-- ตรวจสอบรายการ
SELECT id, document_number, account_number, account_name, bank_name
FROM bank_accounts
WHERE bank_id IS NULL
ORDER BY id;

-- แก้ไขแบบ manual (ตัวอย่าง)
UPDATE bank_accounts
SET bank_id = 1  -- ID ของธนาคารที่ถูกต้อง
WHERE id = XXX;
```

### 2. (Optional) ลบคอลัมน์ที่ซ้ำซ้อน

เมื่อตรวจสอบข้อมูลเรียบร้อยแล้ว สามารถลบคอลัมน์เหล่านี้ออกจาก `bank_accounts` ได้:

```sql
ALTER TABLE bank_accounts
DROP COLUMN bank_address,
DROP COLUMN soi,
DROP COLUMN moo,
DROP COLUMN road,
DROP COLUMN sub_district,
DROP COLUMN district,
DROP COLUMN province,
DROP COLUMN postal_code;
```

**ข้อควรระวัง:**
- ตรวจสอบให้แน่ใจว่าข้อมูลทั้งหมด migrate ถูกต้องก่อนลบคอลัมน์
- ควร backup database ก่อนดำเนินการ
- ตรวจสอบว่าไม่มี application code ที่ใช้คอลัมน์เหล่านี้แล้ว

### 3. อัพเดต Frontend

ปรับปรุง `BankAccountFormModal.tsx` ให้:
- แสดง dropdown เลือกธนาคารจาก `/api/v1/banks/`
- ลบฟิลด์ที่อยู่ธนาคารออก (เพราะดึงจาก banks table แล้ว)
- แสดงข้อมูลที่อยู่ธนาคารแบบ read-only จาก bank relation

---

## 📊 ERD ใหม่

```
┌─────────────────────────┐
│       banks             │
│─────────────────────────│
│ id (PK)                 │
│ bank_name (UNIQUE)      │
│ bank_address            │
│ soi                     │
│ moo                     │
│ road                    │
│ sub_district            │
│ district                │
│ province                │
│ postal_code             │
│ created_at              │
│ updated_at              │
└─────────────────────────┘
          │
          │ 1:N
          │
┌─────────▼───────────────┐
│   bank_accounts         │
│─────────────────────────│
│ id (PK)                 │
│ criminal_case_id (FK)   │
│ bank_id (FK) ← NEW!     │
│ document_number         │
│ account_number          │
│ account_name            │
│ ...                     │
└─────────────────────────┘
```

---

## ✅ ประโยชน์ที่ได้รับ

1. **ความถูกต้องของข้อมูล** - ข้อมูลธนาคารถูกจัดเก็บในที่เดียว ไม่ซ้ำซ้อน
2. **ลดข้อผิดพลาด** - ไม่มีปัญหาการพิมพ์ชื่อธนาคารผิด หรือมีช่องว่างต่างกัน
3. **ง่ายต่อการบำรุงรักษา** - แก้ไขข้อมูลธนาคารที่เดียว ส่งผลทั้งระบบ
4. **ประหยัดพื้นที่** - ลดการเก็บข้อมูลซ้ำซ้อน
5. **Scalability** - เพิ่มธนาคารใหม่ได้ง่าย ผ่าน API
6. **Data Integrity** - Foreign Key constraint รับประกันความสมบูรณ์ของข้อมูล

---

## 🔐 การรักษาความปลอดภัย

- **ON DELETE SET NULL:** เมื่อลบธนาคาร จะตั้ง `bank_id` เป็น NULL แทนการลบ bank_account ทิ้ง
- **UNIQUE Constraint:** ชื่อธนาคารต้องไม่ซ้ำกัน
- **API Authentication:** การสร้าง/แก้ไข/ลบธนาคารต้องมีสิทธิ์ Admin

---

## 📝 บันทึกเพิ่มเติม

- Excel file อยู่ที่: `/mnt/wsl/docker-desktop-bind-mounts/Ubuntu/071da0987f64b3cf84ecff23d0593b1939e5e34d3d503f509fcfa45059aae122/bank_master_data.xlsx`
- Migration script: `migration_add_banks_table.py`
- รันเมื่อ: 2025-10-01 13:00:21 (UTC+7)
- Database: PostgreSQL 15
- ผู้ดำเนินการ: System Migration

---

**สรุป:** การปรับปรุงนี้ทำให้ระบบมีประสิทธิภาพและความถูกต้องมากขึ้น โดยได้ migrate ข้อมูลเดิม 97.4% สำเร็จ มีเพียง 11 รายการที่เป็น NULL ซึ่งเป็นข้อมูลที่ไม่มีการระบุชื่อธนาคารตั้งแต่แรก
