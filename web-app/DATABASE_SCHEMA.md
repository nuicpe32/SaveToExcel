# Database Schema Analysis - Criminal Case Management System

## ภาพรวม Database Structure

```
criminal_cases (ตารางหลัก - คดีอาญา)
    ├── bank_accounts (บัญชีธนาคาร)
    ├── suspects (ผู้ต้องหา/หมายเรียก)
    └── post_arrests (เอกสารหลังจับกุม)

users (ผู้ใช้งานระบบ - แยกอิสระ)
```

---

## 1. criminal_cases (ตารางหลัก)

**Primary Key:** `id` (integer, auto-increment)

**Key Columns:**
- `case_number` (varchar, UNIQUE, NOT NULL) - เลขที่คดี
- `case_id` (varchar) - รหัสคดี
- `status` (varchar) - สถานะคดี
- `complainant` (varchar) - ผู้กล่าวหา/ผู้เสียหาย
- `victim_name` (varchar) - ชื่อผู้เสียหาย
- `suspect` (varchar) - ผู้ต้องหา
- `charge` (text) - ข้อกล่าวหา
- `damage_amount` (varchar) - มูลค่าความเสียหาย
- `complaint_date` (date) - วันที่รับคำกล่าวหา
- `incident_date` (date) - วันที่เกิดเหตุ

**Summary Fields (คำนวณจาก child tables):**
- `bank_accounts_count` (integer) - จำนวนบัญชีธนาคาร
- `bank_accounts_replied` (integer) - จำนวนที่ตอบกลับแล้ว
- `suspects_count` (integer) - จำนวนผู้ต้องหา
- `suspects_replied` (integer) - จำนวนที่มาแล้ว
- `age_in_months` (integer) - อายุคดี (เดือน)
- `is_over_six_months` (varchar) - เกิน 6 เดือนหรือไม่

**Indexes:**
- UNIQUE: `case_number`
- Indexed: `case_id`, `status`, `complaint_date`

**Referenced By:**
- bank_accounts (criminal_case_id → criminal_cases.id)
- suspects (criminal_case_id → criminal_cases.id)
- post_arrests (criminal_case_id → criminal_cases.id)

---

## 2. bank_accounts (บัญชีธนาคาร - หนังสือขอข้อมูล)

**Primary Key:** `id` (integer, auto-increment)

**Foreign Keys:**
- `criminal_case_id` → `criminal_cases.id` (ON DELETE CASCADE)

**Key Columns:**
- `document_number` (varchar) - เลขที่หนังสือ
- `document_date` (date) - วันที่หนังสือ
- `bank_branch` (varchar, NOT NULL) - สาขาธนาคาร
- `bank_name` (varchar, NOT NULL) - ชื่อธนาคาร
- `account_number` (varchar, NOT NULL) - เลขบัญชี
- `account_name` (varchar, NOT NULL) - ชื่อบัญชี
- `complainant` (varchar) - ผู้กล่าวหา
- `victim_name` (varchar) - ชื่อผู้เสียหาย
- `case_id` (varchar) - รหัสคดี (duplicate field)
- `reply_status` (boolean) - สถานะการตอบกลับ
- `response_date` (date) - วันที่ได้รับตอบกลับ
- `days_since_sent` (integer) - จำนวนวันตั้งแต่ส่ง

**Address Fields:**
- `bank_address`, `soi`, `moo`, `road`
- `sub_district`, `district`, `province`, `postal_code`

**Indexes:**
- Indexed: `criminal_case_id`, `complainant`, `reply_status`, `case_id`, `document_number`

**ปัญหาที่พบ:**
- มี `case_id` และ `criminal_case_id` ทั้งสองคอลัมน์ (redundant)
- `complainant`, `victim_name` ซ้ำกับ criminal_cases
- ควรใช้ relationship ผ่าน criminal_case_id แทน

---

## 3. suspects (ผู้ต้องหา/หมายเรียก)

**Primary Key:** `id` (integer, auto-increment)

**Foreign Keys:**
- `criminal_case_id` → `criminal_cases.id` (ON DELETE CASCADE)

**Key Columns:**
- `document_number` (varchar) - เลขที่หนังสือ
- `document_date` (date) - วันที่หนังสือ
- `suspect_name` (varchar, NOT NULL) - ชื่อผู้ต้องหา
- `suspect_id_card` (varchar) - เลขบัตรประชาชน
- `suspect_address` (text) - ที่อยู่
- `police_station` (varchar) - สถานีตำรวจ
- `victim_name` (varchar) - ผู้เสียหาย
- `case_type` (varchar) - ประเภทคดี
- `case_id` (varchar) - รหัสคดี (duplicate)
- `complainant` (varchar) - ผู้กล่าวหา (duplicate)
- `appointment_date` (date) - วันนัดหมาย
- `reply_status` (boolean, default false) - สถานะมาตามนัด

**Indexes:**
- Indexed: `criminal_case_id`, `complainant`, `status`, `case_id`, `reply_status`

**ปัญหาที่พบ:**
- Redundant fields: `case_id`, `complainant`, `victim_name`
- ควรดึงข้อมูลเหล่านี้จาก criminal_cases แทน

---

## 4. post_arrests (เอกสารหลังจับกุม)

**Primary Key:** `id` (integer, auto-increment)

**Foreign Keys:**
- `criminal_case_id` → `criminal_cases.id`

**Key Columns:**
- `case_number` (varchar) - เลขคดี
- `suspect_name` (varchar, NOT NULL) - ชื่อผู้ต้องหา
- `arrest_date` (date) - วันที่จับกุม
- `arrest_time` (varchar) - เวลาจับกุม
- `arresting_officer` (varchar) - เจ้าหน้าที่จับกุม

**Warrant Info:**
- `warrant_court`, `warrant_number`
- `warrant_petition_date`, `warrant_issue_date`

**Prosecutor/Court Info:**
- `prosecutor_name`, `prosecutor_doc_number`
- `prosecutor_transfer_date`
- `court_name`, `court_custody_transfer_date`
- `detention_request_date`

**Process Status:**
- `interrogation_completed` (boolean)
- `bail_requested` (boolean)
- `bail_status` (varchar)

**Indexes:**
- Indexed: `criminal_case_id`, `case_number`

---

## 5. users (ผู้ใช้งานระบบ)

**Primary Key:** `id` (integer, auto-increment)

**Key Columns:**
- `username` (varchar, UNIQUE, NOT NULL)
- `email` (varchar, UNIQUE, NOT NULL)
- `hashed_password` (varchar, NOT NULL)
- `full_name` (varchar)
- `role` (enum: userrole)
- `is_active` (boolean)

**Indexes:**
- UNIQUE: `username`, `email`

**หมายเหตุ:**
- ไม่มี foreign key ไปยังตารางอื่น
- ใช้เฉพาะสำหรับ authentication/authorization

---

## Foreign Key Relationships Summary

```sql
bank_accounts.criminal_case_id → criminal_cases.id (CASCADE DELETE)
suspects.criminal_case_id → criminal_cases.id (CASCADE DELETE)
post_arrests.criminal_case_id → criminal_cases.id
```

---

## ปัญหาและข้อเสนอแนะ

### 1. **Data Redundancy**
❌ **ปัญหา:**
- `bank_accounts` และ `suspects` มี `case_id`, `complainant`, `victim_name` ซ้ำกับ `criminal_cases`
- ทำให้ข้อมูลไม่สอดคล้องกันเมื่อแก้ไข

✅ **แนะนำ:**
```sql
-- ควรลบคอลัมน์เหล่านี้ออกจาก child tables
ALTER TABLE bank_accounts DROP COLUMN case_id, DROP COLUMN complainant, DROP COLUMN victim_name;
ALTER TABLE suspects DROP COLUMN case_id, DROP COLUMN complainant, DROP COLUMN victim_name;

-- ใช้ JOIN แทน
SELECT ba.*, cc.case_id, cc.complainant, cc.victim_name
FROM bank_accounts ba
JOIN criminal_cases cc ON ba.criminal_case_id = cc.id;
```

### 2. **Missing created_by Foreign Keys**
❌ **ปัญหา:**
- ทุกตารางมี `created_by` (integer) แต่ไม่มี FK ไปยัง `users.id`

✅ **แนะนำ:**
```sql
ALTER TABLE criminal_cases
ADD CONSTRAINT fk_criminal_cases_created_by
FOREIGN KEY (created_by) REFERENCES users(id);

-- ทำซ้ำกับ bank_accounts, suspects, post_arrests
```

### 3. **case_id vs id Confusion**
❌ **ปัญหา:**
- `criminal_cases` มีทั้ง `id` (PK) และ `case_id` (user-defined)
- Child tables ใช้ `case_id` (string) แทน `criminal_case_id` (FK) ในบางที่

✅ **แนะนำ:**
- ใช้ `criminal_case_id` (FK to id) เสมอ
- `case_id` เก็บไว้เฉพาะใน `criminal_cases` เท่านั้น

### 4. **Inconsistent Cascade Rules**
❌ **ปัญหา:**
- `bank_accounts`, `suspects` ใช้ `ON DELETE CASCADE`
- `post_arrests` ไม่มี CASCADE

✅ **แนะนำ:**
```sql
-- ควรเป็น CASCADE ทั้งหมด หรือ RESTRICT ทั้งหมด
ALTER TABLE post_arrests
DROP CONSTRAINT fk_post_arrests_criminal_case_id,
ADD CONSTRAINT fk_post_arrests_criminal_case_id
FOREIGN KEY (criminal_case_id) REFERENCES criminal_cases(id)
ON DELETE CASCADE;
```

### 5. **Missing Indexes**
✅ **ควรเพิ่ม:**
```sql
-- เพิ่ม index สำหรับ created_by
CREATE INDEX idx_criminal_cases_created_by ON criminal_cases(created_by);
CREATE INDEX idx_bank_accounts_created_by ON bank_accounts(created_by);

-- เพิ่ม index สำหรับ dates ที่ query บ่อย
CREATE INDEX idx_suspects_appointment_date ON suspects(appointment_date);
CREATE INDEX idx_post_arrests_arrest_date ON post_arrests(arrest_date);
```

---

## แนะนำ Normalized Schema

```sql
-- 1. Criminal Cases (Parent)
criminal_cases
├─ id (PK)
├─ case_number (UNIQUE)
├─ case_id
├─ complainant
├─ victim_name
├─ ... (ข้อมูลคดี)
└─ created_by (FK → users.id)

-- 2. Bank Accounts (Child)
bank_accounts
├─ id (PK)
├─ criminal_case_id (FK → criminal_cases.id) CASCADE
├─ account_number
├─ bank_name
├─ ... (ข้อมูลบัญชี - ไม่ซ้ำกับ parent)
└─ created_by (FK → users.id)

-- 3. Suspects (Child)
suspects
├─ id (PK)
├─ criminal_case_id (FK → criminal_cases.id) CASCADE
├─ suspect_name
├─ appointment_date
├─ ... (ข้อมูลผู้ต้องหา - ไม่ซ้ำกับ parent)
└─ created_by (FK → users.id)

-- 4. Post Arrests (Child)
post_arrests
├─ id (PK)
├─ criminal_case_id (FK → criminal_cases.id) CASCADE
├─ suspect_name (อาจต้อง FK → suspects.id ถ้าเป็นคนเดียวกัน)
├─ arrest_date
├─ ... (ข้อมูลหลังจับกุม)
└─ created_by (FK → users.id)

-- 5. Users (Independent)
users
├─ id (PK)
├─ username (UNIQUE)
├─ email (UNIQUE)
└─ ... (ข้อมูล auth)
```

---

## Query Examples

### ดูข้อมูลคดีพร้อม related records:

```sql
SELECT
    cc.case_number,
    cc.complainant,
    COUNT(DISTINCT ba.id) as total_bank_accounts,
    COUNT(DISTINCT s.id) as total_suspects,
    COUNT(DISTINCT pa.id) as total_arrests
FROM criminal_cases cc
LEFT JOIN bank_accounts ba ON ba.criminal_case_id = cc.id
LEFT JOIN suspects s ON s.criminal_case_id = cc.id
LEFT JOIN post_arrests pa ON pa.criminal_case_id = cc.id
GROUP BY cc.id, cc.case_number, cc.complainant
ORDER BY cc.complaint_date DESC;
```

### หา bank accounts ที่ยังไม่ได้รับตอบกลับ:

```sql
SELECT
    ba.document_number,
    ba.bank_name,
    ba.days_since_sent,
    cc.case_number,
    cc.complainant
FROM bank_accounts ba
JOIN criminal_cases cc ON ba.criminal_case_id = cc.id
WHERE ba.reply_status = false
ORDER BY ba.days_since_sent DESC;
```

### หาคดีที่เกิน 6 เดือน:

```sql
SELECT
    case_number,
    complainant,
    complaint_date,
    age_in_months,
    status
FROM criminal_cases
WHERE age_in_months > 6
ORDER BY age_in_months DESC;
```
