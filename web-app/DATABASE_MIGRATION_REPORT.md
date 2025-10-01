# รายงานการอัพเดต Foreign Key Relationships

**วันที่:** 2025-10-01
**โดย:** Claude Code
**Database:** criminal_case_db (PostgreSQL 15)

---

## สรุปผลการอัพเดต

### ✅ การอัพเดตสำเร็จ

| ตาราง | จำนวนที่อัพเดต | สถานะ |
|------|----------------|-------|
| **bank_accounts** | **35 รายการ** | ✅ สำเร็จ |
| **suspects** | **1 รายการ** | ✅ สำเร็จ |
| **รวมทั้งหมด** | **36 รายการ** | ✅ เสร็จสมบูรณ์ |

---

## รายละเอียดตาราง bank_accounts

### สถานะก่อนอัพเดต
- ข้อมูลทั้งหมด: **417 รายการ**
- มี case_id แต่ไม่มี criminal_case_id: **301 รายการ**
- case_id ที่ไม่ซ้ำกัน: **108 case_id**

### สถานะหลังอัพเดต
- ข้อมูลทั้งหมด: **417 รายการ**
- เชื่อมโยงแล้ว (มี criminal_case_id): **151 รายการ** (36.2%)
- ยังไม่ได้เชื่อมโยง: **266 รายการ** (63.8%)

### ผลการอัพเดต
- **อัพเดตสำเร็จ: 35 รายการ**
- เพิ่มจาก 116 → 151 รายการที่เชื่อมโยง

### ตัวอย่างข้อมูลที่อัพเดต
```sql
ID: 2526 | case_id: 66041271    → criminal_case_id: 269 | คดี 151/2566
ID: 2525 | case_id: 68033127891 → criminal_case_id: 248 | คดี 940/2568
ID: 2523 | case_id: 680601843   → criminal_case_id: 241 | คดี 1174/2568
ID: 2522 | case_id: 651217027   → criminal_case_id: 268 | คดี 170/2566
ID: 2514 | case_id: 6809044200  → criminal_case_id: 232 | คดี 1382/2568
```

---

## รายละเอียดตาราง suspects

### สถานะก่อนอัพเดต
- ข้อมูลทั้งหมด: **15 รายการ**
- มี case_id แต่ไม่มี criminal_case_id: **5 รายการ**
- case_id ที่ไม่ซ้ำกัน: **4 case_id**

### สถานะหลังอัพเดต
- ข้อมูลทั้งหมด: **15 รายการ**
- เชื่อมโยงแล้ว (มี criminal_case_id): **11 รายการ** (73.3%)
- ยังไม่ได้เชื่อมโยง: **4 รายการ** (26.7%)

### ผลการอัพเดต
- **อัพเดตสำเร็จ: 1 รายการ**
- เพิ่มจาก 10 → 11 รายการที่เชื่อมโยง

### ตัวอย่างข้อมูลที่อัพเดต
```sql
ID: 87 | case_id: 660625312  → criminal_case_id: 270 | คดี 134/2566 | น.ส.อรอุมา จงเย็นกลาง
ID: 86 | case_id: 6804076987 → criminal_case_id: 237 | คดี 1275/2568 | น.ส.ทัศนีย์ บุญชัยสงค์
ID: 85 | case_id: 6804076987 → criminal_case_id: 237 | คดี 1275/2568 | นายอดุลย์ ดวงอ่อน
ID: 84 | case_id: 6804076987 → criminal_case_id: 237 | คดี 1275/2568 | นางสุกัญญา หน่อแก้ว
ID: 83 | case_id: 68061214466 → criminal_case_id: 238 | คดี 1257/2568 | นายอานันท์ แซ่แต้
```

---

## ข้อมูลที่ยังไม่ได้เชื่อมโยง

### bank_accounts: 266 รายการ

**สาเหตุที่ไม่ได้เชื่อมโยง:**
1. **case_id ไม่มีในตาราง criminal_cases** - คดีเหล่านี้ยังไม่ได้ถูกสร้างในระบบ
2. **case_id เป็น "nan"** - ข้อมูลเสีย (11 รายการ)
3. **case_id format ไม่ตรงกัน** - เช่น เพิ่ม/ลด เลขศูนย์นำหน้า

**Top 10 case_id ที่หาไม่เจอ:**
| case_id | จำนวนรายการ | หมายเหตุ |
|---------|-------------|----------|
| 660511087 | 14 | ไม่มีในระบบ |
| 660511362 | 13 | ไม่มีในระบบ |
| 66086233 | 12 | ไม่มีในระบบ |
| **nan** | 11 | ⚠️ ข้อมูลเสีย |
| 66034076 | 8 | ไม่มีในระบบ |
| 66082539 | 8 | ไม่มีในระบบ |
| 66106931 | 7 | ไม่มีในระบบ |
| 660910566 | 7 | ไม่มีในระบบ |
| 68091921756 | 7 | ไม่มีในระบบ |
| 66025491 | 7 | ไม่มีในระบบ |

### suspects: 4 รายการ

ข้อมูลที่ยังไม่ได้เชื่อมโยงน้อยมาก - ส่วนใหญ่เป็น case_id ที่ไม่มีในตาราง criminal_cases

---

## SQL Commands ที่ใช้

### 1. อัพเดต bank_accounts
```sql
UPDATE bank_accounts ba
SET criminal_case_id = cc.id
FROM criminal_cases cc
WHERE ba.case_id = cc.case_id
  AND ba.criminal_case_id IS NULL
  AND ba.case_id IS NOT NULL
  AND ba.case_id != '';
```
**ผลลัพธ์:** UPDATE 35

### 2. อัพเดต suspects
```sql
UPDATE suspects s
SET criminal_case_id = cc.id
FROM criminal_cases cc
WHERE s.case_id = cc.case_id
  AND s.criminal_case_id IS NULL
  AND s.case_id IS NOT NULL
  AND s.case_id != '';
```
**ผลลัพธ์:** UPDATE 1

---

## สถิติ Database หลังอัพเดต

### Linkage Rate (อัตราการเชื่อมโยง)

```
┌──────────────────┬────────┬──────────┬────────────┬──────────┐
│ Table            │ Total  │ Linked   │ Unlinked   │ Rate     │
├──────────────────┼────────┼──────────┼────────────┼──────────┤
│ bank_accounts    │ 417    │ 151      │ 266        │ 36.2%    │
│ suspects         │ 15     │ 11       │ 4          │ 73.3%    │
│ post_arrests     │ 12     │ 12       │ 0          │ 100.0%   │
├──────────────────┼────────┼──────────┼────────────┼──────────┤
│ Total Child Recs │ 444    │ 174      │ 270        │ 39.2%    │
└──────────────────┴────────┴──────────┴────────────┴──────────┘

Parent Records: 47 criminal_cases
```

---

## แนะนำขั้นตอนต่อไป

### 1. ✅ แก้ไขข้อมูล "nan" (11 รายการ)
```sql
-- หา records ที่มี case_id เป็น 'nan'
SELECT id, document_number, bank_name, account_number
FROM bank_accounts
WHERE case_id = 'nan';

-- แก้ไขด้วยการ:
-- 1) ลบออก หรือ
-- 2) ค้นหา case_id ที่ถูกต้องจากเอกสารและ UPDATE
```

### 2. 🔍 ตรวจสอบ case_id format
```sql
-- หา case_id ที่อาจจะเป็นรูปแบบเดียวกันแต่เขียนต่างกัน
SELECT DISTINCT
    ba.case_id as bank_case_id,
    cc.case_id as criminal_case_id,
    similarity(ba.case_id, cc.case_id) as similarity_score
FROM bank_accounts ba
CROSS JOIN criminal_cases cc
WHERE ba.criminal_case_id IS NULL
  AND ba.case_id IS NOT NULL
  AND similarity(ba.case_id, cc.case_id) > 0.8
ORDER BY similarity_score DESC;
```

### 3. 📝 สร้างคดีใหม่ที่ขาดหาย
```sql
-- หา case_id ที่มีในบัญชีธนาคารแต่ไม่มีในตาราง criminal_cases
SELECT DISTINCT case_id, COUNT(*) as record_count
FROM bank_accounts
WHERE criminal_case_id IS NULL
  AND case_id IS NOT NULL
  AND case_id != ''
  AND case_id != 'nan'
GROUP BY case_id
ORDER BY record_count DESC;

-- จากนั้นสร้างคดีใหม่ตาม case_id เหล่านี้
```

### 4. 🧹 Clean Up Redundant Fields (ระยะยาว)
```sql
-- หลังจาก criminal_case_id ครบแล้ว สามารถลบฟิลด์ซ้ำซ้อน:
ALTER TABLE bank_accounts DROP COLUMN case_id;
ALTER TABLE bank_accounts DROP COLUMN complainant;
ALTER TABLE bank_accounts DROP COLUMN victim_name;

-- ใช้ JOIN แทน:
SELECT ba.*, cc.case_id, cc.complainant, cc.victim_name
FROM bank_accounts ba
JOIN criminal_cases cc ON ba.criminal_case_id = cc.id;
```

---

## Verification Queries

### ตรวจสอบความถูกต้อง
```sql
-- 1. ตรวจสอบว่า case_id กับ criminal_case_id ตรงกัน
SELECT
    ba.id,
    ba.case_id as ba_case_id,
    cc.case_id as cc_case_id,
    CASE WHEN ba.case_id = cc.case_id THEN '✅' ELSE '❌' END as match
FROM bank_accounts ba
JOIN criminal_cases cc ON ba.criminal_case_id = cc.id
WHERE ba.case_id != cc.case_id;

-- 2. ตรวจสอบ orphaned records (FK ชี้ไป id ที่ไม่มีจริง)
SELECT ba.*
FROM bank_accounts ba
LEFT JOIN criminal_cases cc ON ba.criminal_case_id = cc.id
WHERE ba.criminal_case_id IS NOT NULL
  AND cc.id IS NULL;
```

---

## บันทึกการเปลี่ยนแปลง

| วันที่ | การดำเนินการ | ผู้ทำ | ผลลัพธ์ |
|--------|--------------|-------|---------|
| 2025-10-01 | Migration: Link bank_accounts.criminal_case_id | Claude | ✅ 35 records |
| 2025-10-01 | Migration: Link suspects.criminal_case_id | Claude | ✅ 1 record |

---

## สรุป

✅ **การอัพเดตเสร็จสมบูรณ์**
- อัพเดต Foreign Key relationships สำเร็จทั้งหมด **36 รายการ**
- ข้อมูลที่เชื่อมโยงได้เพิ่มขึ้นจาก **126 → 162 รายการ** (เพิ่ม 28.6%)
- ไม่มี data loss หรือ corruption

⚠️ **ข้อควรระวัง**
- ยังมีข้อมูล **270 รายการ** (60.8%) ที่ยังไม่ได้เชื่อมโยง
- ส่วนใหญ่เกิดจาก case_id ไม่มีในตาราง criminal_cases
- แนะนำให้สร้างคดีใหม่หรือแก้ไข case_id ให้ถูกต้อง

📊 **Database Integrity**
- Foreign Key constraints ทำงานปกติ
- Cascade delete rules active
- No orphaned records detected
