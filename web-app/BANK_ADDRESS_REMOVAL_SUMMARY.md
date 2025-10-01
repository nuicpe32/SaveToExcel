# สรุปการลบฟิลด์ที่อยู่และสาขาออกจากตาราง bank_accounts

**วันที่:** 1 ตุลาคม 2568  
**เวอร์ชัน:** v3.0.1  
**ผู้ดำเนินการ:** System Migration

---

## 🎯 วัตถุประสงค์

ลบคอลัมน์ที่เกี่ยวกับ **ที่อยู่ธนาคาร** และ **สาขา** ออกจากตาราง `bank_accounts` เพราะ:
1. ไม่ต้องระบุสาขาในการกรอกข้อมูล
2. ส่งเอกสารไปที่ **สำนักงานใหญ่เท่านั้น**
3. ดึงที่อยู่จากตาราง `banks` (Master Data) แทน
4. ลดความซ้ำซ้อนของข้อมูล

---

## 📋 คอลัมน์ที่ลบออก (9 คอลัมน์)

| คอลัมน์ | เหตุผล |
|---------|--------|
| `bank_branch` | ไม่ต้องระบุสาขา ส่งสำนักงานใหญ่ |
| `bank_address` | ใช้จาก `banks.bank_address` |
| `soi` | ใช้จาก `banks.soi` |
| `moo` | ใช้จาก `banks.moo` |
| `road` | ใช้จาก `banks.road` |
| `sub_district` | ใช้จาก `banks.sub_district` |
| `district` | ใช้จาก `banks.district` |
| `province` | ใช้จาก `banks.province` |
| `postal_code` | ใช้จาก `banks.postal_code` |

---

## 📁 ไฟล์ที่แก้ไข

### 1. Database Migration
- ✅ `migrations/007_remove_bank_address_fields.sql`
  - ALTER TABLE DROP COLUMN สำหรับทั้ง 9 คอลัมน์
  - มี Rollback script (ถ้าต้องการย้อนกลับ)

### 2. Backend - Model
- ✅ `app/models/bank_account.py`
  - ลบฟิลด์ทั้ง 9 คอลัมน์
  - เพิ่ม comment อธิบาย

### 3. Backend - Schema
- ✅ `app/schemas/bank_account.py`
  - ลบฟิลด์จาก `BankAccountBase`
  - ลบฟิลด์จาก `BankAccountUpdate`
  - เพิ่ม comment อธิบาย

### 4. Frontend - Form
- ✅ `components/BankAccountFormModal.tsx`
  - ลบฟอร์มกรอกที่อยู่ทั้งหมด
  - แสดงข้อความแจ้งเตือน: "ที่อยู่จะดึงจากสำนักงานใหญ่โดยอัตโนมัติ"

### 5. Frontend - Display
- ✅ `pages/BankAccountsPage.tsx`
  - ลบ interface fields ที่เกี่ยวกับที่อยู่
  - ลบ Tab "ที่อยู่ธนาคาร" ออกจาก Drawer
  - แสดงข้อความแจ้งเตือนแทน

### 6. Frontend - Dashboard
- ✅ `pages/DashboardPage.tsx`
  - ลบ interface fields: `bank_branch`, `bank_address`

---

## 🔄 โครงสร้างใหม่

### Before (เก่า - ซ้ำซ้อน)
```
bank_accounts
├── bank_id (FK) ───────────┐
├── bank_name               │
├── bank_branch  ❌         │
├── bank_address ❌         │
├── soi          ❌         │
├── moo          ❌         │
├── road         ❌         │
├── sub_district ❌         │
├── district     ❌         │
├── province     ❌         │
└── postal_code  ❌         │
                            │
banks                       │
├── id ◄────────────────────┘
├── bank_name
├── bank_address  ✅
├── soi           ✅
├── moo           ✅
└── ... (ที่อยู่เต็ม)
```

### After (ใหม่ - ไม่ซ้ำซ้อน)
```
bank_accounts
├── bank_id (FK) ───────────┐
├── bank_name               │
└── ... (ข้อมูลบัญชี)        │
                            │
banks                       │
├── id ◄────────────────────┘
├── bank_name
├── bank_address  ✅ (ดึงจากตรงนี้)
└── ... (ที่อยู่สำนักงานใหญ่)
```

---

## 🚀 การใช้งานหลังจาก Migration

### การเพิ่มบัญชีธนาคาร

**ฟิลด์ที่ต้องกรอก:**
```json
{
  "criminal_case_id": 123,
  "bank_name": "ธนาคารกรุงเทพ",
  "account_number": "1234567890",
  "account_name": "นายทดสอบ",
  "time_period": "ม.ค. - มี.ค. 2568"
}
```

**ไม่ต้องกรอก:**
- ❌ สาขา (bank_branch)
- ❌ ที่อยู่ธนาคาร (bank_address, soi, moo, etc.)

**ระบบจะ:**
1. ดึง `bank_id` จากชื่อธนาคาร
2. ดึงที่อยู่สำนักงานใหญ่จาก `banks` table
3. ใช้ที่อยู่นั้นในการสร้างเอกสาร

---

## 📊 การดึงข้อมูลที่อยู่

### SQL Query (ตัวอย่าง)
```sql
-- ดึงข้อมูลบัญชีพร้อมที่อยู่ธนาคาร
SELECT 
    ba.id,
    ba.account_number,
    ba.account_name,
    ba.bank_name,
    -- ดึงที่อยู่จาก banks
    b.bank_address,
    b.soi,
    b.moo,
    b.road,
    b.sub_district,
    b.district,
    b.province,
    b.postal_code
FROM bank_accounts ba
LEFT JOIN banks b ON ba.bank_id = b.id
WHERE ba.id = ?;
```

### Backend (Python/SQLAlchemy)
```python
# ดึงข้อมูลพร้อม relationship
bank_account = db.query(BankAccount).filter(BankAccount.id == id).first()

# เข้าถึงที่อยู่จาก banks table
if bank_account.bank:
    address = bank_account.bank.bank_address
    district = bank_account.bank.district
    province = bank_account.bank.province
```

---

## ✅ ขั้นตอนการ Deploy

### 1. รัน Migration Script
```bash
# เข้าไปใน database container
docker-compose exec postgres psql -U user -d criminal_case_db

# รัน migration
\i /path/to/migrations/007_remove_bank_address_fields.sql

# ตรวจสอบ
\d bank_accounts
```

### 2. Restart Backend
```bash
docker-compose restart backend
```

### 3. Rebuild Frontend (ถ้าจำเป็น)
```bash
docker-compose restart frontend
```

### 4. ทดสอบระบบ
```bash
# Test API
curl http://localhost:8000/api/v1/bank-accounts/

# Test Frontend
# เปิด http://localhost:3001/bank-accounts
```

---

## 🧪 การทดสอบ

### Test Cases

#### ✅ Test 1: สร้างบัญชีใหม่
- กรอกข้อมูลบัญชีโดยไม่มีฟิลด์ที่อยู่
- ตรวจสอบว่าบันทึกได้สำเร็จ

#### ✅ Test 2: ดูรายละเอียดบัญชี
- ตรวจสอบว่าไม่มีฟิลด์ที่อยู่แสดง
- มีข้อความแจ้งเตือนเกี่ยวกับที่อยู่สำนักงานใหญ่

#### ✅ Test 3: แก้ไขบัญชี
- ตรวจสอบว่าไม่มีฟอร์มที่อยู่ให้กรอก
- แก้ไขฟิลด์อื่นๆ ได้ปกติ

#### ✅ Test 4: ดึงข้อมูลพร้อมที่อยู่
- Query ด้วย JOIN กับ banks table
- ได้ที่อยู่สำนักงานใหญ่ครบถ้วน

---

## 🔧 Rollback (ถ้าจำเป็น)

### ถ้าต้องการย้อนกลับ:

```sql
-- Restore columns
ALTER TABLE bank_accounts ADD COLUMN bank_branch VARCHAR;
ALTER TABLE bank_accounts ADD COLUMN bank_address TEXT;
ALTER TABLE bank_accounts ADD COLUMN soi VARCHAR;
ALTER TABLE bank_accounts ADD COLUMN moo VARCHAR;
ALTER TABLE bank_accounts ADD COLUMN road VARCHAR;
ALTER TABLE bank_accounts ADD COLUMN sub_district VARCHAR;
ALTER TABLE bank_accounts ADD COLUMN district VARCHAR;
ALTER TABLE bank_accounts ADD COLUMN province VARCHAR;
ALTER TABLE bank_accounts ADD COLUMN postal_code VARCHAR;
```

จากนั้นเรียกคืนโค้ดจาก Git:
```bash
git checkout HEAD~1 -- backend/app/models/bank_account.py
git checkout HEAD~1 -- backend/app/schemas/bank_account.py
git checkout HEAD~1 -- frontend/src/components/BankAccountFormModal.tsx
git checkout HEAD~1 -- frontend/src/pages/BankAccountsPage.tsx
```

---

## 📝 Notes

### ข้อควรระวัง
1. ⚠️ ข้อมูลเก่าที่มี `bank_branch` และที่อยู่จะหายไป (ลบถาวร)
2. ⚠️ ถ้ามีข้อมูลสำคัญใน columns เหล่านี้ ควร backup ก่อน
3. ⚠️ ต้องแน่ใจว่า `banks` table มีข้อมูลครบถ้วนก่อน

### Backup ข้อมูลเก่า (ถ้าต้องการ)
```sql
-- สำรองข้อมูลก่อน migration
CREATE TABLE bank_accounts_backup AS 
SELECT 
    id, 
    bank_branch, 
    bank_address, 
    soi, moo, road, 
    sub_district, district, province, postal_code
FROM bank_accounts;
```

---

## ✨ ประโยชน์ที่ได้รับ

1. ✅ **ลดความซ้ำซ้อน** - ที่อยู่เก็บที่เดียวในตาราง `banks`
2. ✅ **ง่ายต่อการบำรุงรักษา** - แก้ไขที่อยู่ครั้งเดียว ใช้ได้ทุกคดี
3. ✅ **ประหยัดพื้นที่** - ลดขนาดตาราง `bank_accounts`
4. ✅ **สะดวกในการใช้งาน** - ไม่ต้องกรอกที่อยู่ทุกครั้ง
5. ✅ **ถูกต้องตามการใช้งานจริง** - ส่งเอกสารไปสำนักงานใหญ่เท่านั้น

---

**Status:** ✅ Ready to Deploy  
**Estimated Migration Time:** < 5 นาที  
**Rollback Available:** ✅ Yes

