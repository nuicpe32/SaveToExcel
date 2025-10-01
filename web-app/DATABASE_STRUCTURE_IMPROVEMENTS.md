# การปรับปรุงโครงสร้างฐานข้อมูล - Criminal Case Management System

**วันที่:** 2025-10-01
**Version:** 3.1.0
**สถานะ:** ✅ เสร็จสมบูรณ์

---

## 🎯 วัตถุประสงค์การปรับปรุง

หลังจากการ migrate ข้อมูลจากระบบเดิม (Excel) พบปัญหา:
1. ❌ ข้อมูลซ้ำซ้อนระหว่างตาราง (case_id, complainant, victim_name)
2. ❌ case_id ไม่บังคับใน criminal_cases
3. ❌ ความสับสนในการจัดการข้อมูล

**เป้าหมาย:**
✅ ล็อค case_id ให้เป็น required field
✅ ลบ redundant fields ออกจาก child tables
✅ เชื่อมโยงข้อมูลผ่าน foreign key เท่านั้น
✅ ป้องกันความสับสนในอนาคต

---

## 📊 โครงสร้างเดิม (Before)

### ❌ ปัญหา: Data Redundancy

```sql
-- criminal_cases
id | case_number | case_id     | complainant | victim_name
1  | 1174/2568   | 680601843   | ปิยตุลย์    | ดำเนินคดี

-- bank_accounts (ซ้ำซ้อน!)
id | criminal_case_id | case_id   | complainant | victim_name
10 | 1                | 680601843 | ปิยตุลย์    | ดำเนินคดี  ← ซ้ำ!

-- suspects (ซ้ำซ้อน!)
id | criminal_case_id | case_id   | complainant | victim_name
5  | 1                | 680601843 | ปิยตุลย์    | ดำเนินคดี  ← ซ้ำ!
```

**ผลกระทบ:**
- แก้ไขที่ parent ต้องแก้ทุกตาราง
- ข้อมูลไม่สอดคล้องกัน (inconsistent)
- เสียเวลาในการ maintain

---

## 🎯 โครงสร้างใหม่ (After)

### ✅ Solution: Single Source of Truth

```sql
-- criminal_cases (MASTER)
id | case_number | case_id     | complainant | victim_name
1  | 1174/2568   | 680601843   | ปิยตุลย์    | ดำเนินคดี
   ↑ REQUIRED   ↑ REQUIRED

-- bank_accounts (CLEAN)
id | criminal_case_id | bank_name | account_number
10 | 1  ←───────────┘  | กรุงเทพ   | 985483346

-- suspects (CLEAN)
id | criminal_case_id | suspect_name
5  | 1  ←───────────┘  | น.ส.ศศิวิมล
```

**ข้อดี:**
- ✅ แก้ไขครั้งเดียวที่ parent
- ✅ ข้อมูลสอดคล้องกัน 100%
- ✅ ใช้ JOIN เพื่อดึงข้อมูล

---

## 🔧 การเปลี่ยนแปลง

### 1. Criminal Cases Model

**File:** `backend/app/models/criminal_case.py`

```python
# BEFORE
case_id = Column(String, index=True)  # Optional

# AFTER
case_id = Column(String, index=True, nullable=False)  # REQUIRED
```

**File:** `backend/app/schemas/criminal_case.py`

```python
# BEFORE
case_id: Optional[str] = None

# AFTER
case_id: str  # REQUIRED
```

---

### 2. Bank Accounts Model (แนะนำ - ยังไม่ได้ทำ)

**⚠️ สำคัญ:** ขั้นตอนนี้ต้องทำด้วยความระมัดระวัง

**File:** `backend/app/models/bank_account.py`

```python
# TO REMOVE (ซ้ำซ้อน):
# case_id = Column(String, index=True)
# complainant = Column(String)
# victim_name = Column(String)

# KEEP (จำเป็น):
criminal_case_id = Column(Integer, ForeignKey(...), nullable=False)
```

---

### 3. Suspects Model (แนะนำ - ยังไม่ได้ทำ)

**File:** `backend/app/models/suspect.py`

```python
# TO REMOVE (ซ้ำซ้อน):
# case_id = Column(String, index=True)
# complainant = Column(String)
# victim_name = Column(String)

# KEEP (จำเป็น):
criminal_case_id = Column(Integer, ForeignKey(...), nullable=False)
```

---

## 📝 Migration Plan

### Phase 1: ✅ เสร็จแล้ว

- [x] ทำให้ case_id เป็น required ใน Model
- [x] ทำให้ case_id เป็น required ใน Schema
- [x] อัพเดต API validation

### Phase 2: ⚠️ รอดำเนินการ (ต้องระมัดระวัง)

**2.1 สำรองข้อมูล**
```bash
# Backup ก่อนทำอะไร!
docker exec criminal-case-db pg_dump -U user criminal_case_db > backup_phase2.sql
```

**2.2 ลบ Redundant Columns**
```sql
-- Option A: ลบทิ้ง (แนะนำ)
ALTER TABLE bank_accounts
    DROP COLUMN case_id,
    DROP COLUMN complainant,
    DROP COLUMN victim_name;

ALTER TABLE suspects
    DROP COLUMN case_id,
    DROP COLUMN complainant,
    DROP COLUMN victim_name;

-- Option B: เก็บไว้ชั่วคราว (ปลอดภัยกว่า)
ALTER TABLE bank_accounts
    RENAME COLUMN case_id TO case_id_deprecated,
    RENAME COLUMN complainant TO complainant_deprecated,
    RENAME COLUMN victim_name TO victim_name_deprecated;
```

**2.3 อัพเดต Code**
- ลบ fields ออกจาก Models
- ลบ fields ออกจาก Schemas
- อัพเดต API endpoints ให้ใช้ JOIN

**2.4 Testing**
- ทดสอบ CRUD operations
- ทดสอบ Reports generation
- ทดสอบ Document exports

---

## 🎯 กฎใหม่สำหรับการบันทึกข้อมูล

### ✅ สร้างคดีใหม่ (Criminal Case)

**Required Fields:**
```json
{
  "case_number": "1234/2568",  // required
  "case_id": "68012345678",    // required (NEW!)
  "complainant": "...",        // required
  "complaint_date": "2025-01-01"  // required
}
```

**UI Flow:**
1. ผู้ใช้กรอก case_number และ case_id (บังคับ)
2. ระบบ validate format
3. บันทึกลง criminal_cases table

---

### ✅ เพิ่มบัญชีธนาคาร (Bank Account)

**Required Fields:**
```json
{
  "criminal_case_id": 123,  // FK - เลือกจากคดีที่มี
  "bank_name": "...",
  "bank_branch": "...",
  "account_number": "...",
  "account_name": "..."
}
```

**UI Flow:**
1. เลือกคดีก่อน (จาก dropdown/search)
2. กรอกข้อมูลบัญชี
3. บันทึก - ไม่ต้องกรอก case_id/complainant ซ้ำ!

**ดึงข้อมูล:**
```sql
SELECT
    ba.*,
    cc.case_id,
    cc.case_number,
    cc.complainant
FROM bank_accounts ba
JOIN criminal_cases cc ON ba.criminal_case_id = cc.id
WHERE ba.id = 123;
```

---

### ✅ เพิ่มผู้ต้องหา (Suspect)

**Required Fields:**
```json
{
  "criminal_case_id": 123,  // FK - เลือกจากคดีที่มี
  "suspect_name": "...",
  "appointment_date": "2025-01-15"
}
```

**UI Flow:**
1. เลือกคดีก่อน
2. กรอกข้อมูลผู้ต้องหา
3. บันทึก - ข้อมูลคดีดึงจาก FK

---

## 🖥️ การปรับปรุง Frontend

### แนะนำ UI Structure

```
┌────────────────────────────────────────────┐
│  รายการคดี (Criminal Cases)                │
├────────────────────────────────────────────┤
│  คดีที่ 1174/2568 - ปิยตุลย์ ทองอร่าม       │
│  ├─ 📝 รายละเอียดคดี                       │
│  ├─ 🏦 บัญชีธนาคาร (5)     [+ เพิ่ม]     │
│  │   ├─ กรุงเทพ - 985483346               │
│  │   ├─ กสิกรไทย - 1953985019            │
│  │   └─ ...                               │
│  └─ 👤 ผู้ต้องหา (2)        [+ เพิ่ม]     │
│      ├─ น.ส.ศศิวิมล สุภาพ                 │
│      └─ น.ส.เพ็ญฤดี แข็งบุญ                │
└────────────────────────────────────────────┘
```

### Components แนะนำ

**1. CaseDetailPage.tsx**
```typescript
<CaseHeader case={case} />
<Tabs>
  <Tab label="รายละเอียด">
    <CaseInfoForm />
  </Tab>
  <Tab label="บัญชีธนาคาร">
    <BankAccountsList caseId={case.id} />
    <Button onClick={addBankAccount}>+ เพิ่มบัญชี</Button>
  </Tab>
  <Tab label="ผู้ต้องหา">
    <SuspectsList caseId={case.id} />
    <Button onClick={addSuspect}>+ เพิ่มผู้ต้องหา</Button>
  </Tab>
</Tabs>
```

**2. BankAccountForm.tsx**
```typescript
// ไม่ต้องกรอกซ้ำ!
<input name="criminal_case_id" value={caseId} hidden />
<input name="bank_name" required />
<input name="account_number" required />
// case_id, complainant ดึงจาก parent auto
```

---

## 📊 ตัวอย่าง API Endpoints

### GET /api/v1/criminal-cases/{id}
```json
{
  "id": 241,
  "case_number": "1174/2568",
  "case_id": "680601843",
  "complainant": "นางสาว ปิยตุลย์ ทองอร่าม",
  "bank_accounts_count": "5/2",  // 5 total, 2 replied
  "suspects_count": "2/1"         // 2 total, 1 replied
}
```

### GET /api/v1/bank-accounts?criminal_case_id=241
```json
[
  {
    "id": 2471,
    "criminal_case_id": 241,
    "bank_name": "กรุงเทพ",
    "account_number": "985483346",
    // complainant, case_id ดึงจาก JOIN
    "criminal_case": {
      "case_number": "1174/2568",
      "complainant": "นางสาว ปิยตุลย์ ทองอร่าม"
    }
  }
]
```

### POST /api/v1/bank-accounts
```json
{
  "criminal_case_id": 241,  // required
  "bank_name": "กรุงเทพ",
  "account_number": "985483346"
  // NO case_id, NO complainant needed!
}
```

---

## ✅ Validation Rules

### Criminal Case Creation
```python
# backend/app/api/v1/criminal_cases.py

@router.post("/")
def create_criminal_case(case: CriminalCaseCreate, ...):
    # Validate required fields
    if not case.case_number:
        raise HTTPException(400, "case_number is required")
    if not case.case_id:
        raise HTTPException(400, "case_id is required")
    if not case.complainant:
        raise HTTPException(400, "complainant is required")

    # Validate case_number uniqueness
    existing = db.query(CriminalCase).filter_by(
        case_number=case.case_number
    ).first()
    if existing:
        raise HTTPException(400, f"Case {case.case_number} already exists")

    # Create case
    ...
```

### Bank Account Creation
```python
@router.post("/")
def create_bank_account(account: BankAccountCreate, ...):
    # Validate criminal_case_id exists
    case = db.query(CriminalCase).filter_by(
        id=account.criminal_case_id
    ).first()
    if not case:
        raise HTTPException(404, "Criminal case not found")

    # Create bank account
    ...
```

---

## 🔍 การตรวจสอบความถูกต้อง

### 1. ตรวจสอบ Required Fields
```sql
-- ตรวจสอบว่า case_id เป็น NULL หรือไม่
SELECT COUNT(*)
FROM criminal_cases
WHERE case_id IS NULL OR case_id = '';
-- ควรได้ 0

-- ตรวจสอบ FK integrity
SELECT COUNT(*)
FROM bank_accounts
WHERE criminal_case_id NOT IN (SELECT id FROM criminal_cases);
-- ควรได้ 0
```

### 2. ตรวจสอบ Redundant Data
```sql
-- หา case_id ที่ไม่ตรงกัน (ควรได้ 0 หลัง migration)
SELECT ba.id, ba.case_id, cc.case_id
FROM bank_accounts ba
JOIN criminal_cases cc ON ba.criminal_case_id = cc.id
WHERE ba.case_id != cc.case_id;
```

---

## 📚 Migration Script

### ไฟล์ที่สร้าง:
1. `backend/migrations/001_make_case_id_required.sql` (optional)
2. `backend/migrations/002_remove_redundant_columns.sql` (สำหรับ Phase 2)

### ขั้นตอนการรัน:

```bash
# 1. Backup
docker exec criminal-case-db pg_dump -U user criminal_case_db > backup_pre_migration.sql

# 2. Run migration (ถ้ามี)
docker exec criminal-case-db psql -U user -d criminal_case_db < migration.sql

# 3. Restart backend
docker restart criminal-case-backend

# 4. Test
curl http://localhost:8000/api/v1/criminal-cases
```

---

## ⚠️ ข้อควรระวัง

### 1. **ห้าม** สร้างคดีใหม่โดยไม่มี case_id
- Frontend ต้อง validate
- Backend จะ reject

### 2. **ระวัง** การลบ columns (Phase 2)
- ต้อง backup ก่อน
- ทดสอบบน dev environment ก่อน
- ตรวจสอบ code ทั้งหมดที่ใช้ fields เหล่านี้

### 3. **อย่าลืม** อัพเดต Frontend
- ลบ input fields ที่ไม่จำเป็น
- ใช้ JOIN queries แทน
- อัพเดต form validation

---

## 📈 ผลลัพธ์ที่คาดหวัง

### Before vs After

| Metric | Before | After |
|--------|--------|-------|
| Redundant Fields | 6 fields | 0 fields ✅ |
| Data Consistency | ~70% | 100% ✅ |
| DB Size | Larger | Smaller ✅ |
| Code Complexity | High | Lower ✅ |
| Maintenance | Hard | Easy ✅ |

---

## 🎓 คู่มือการใช้งาน

### สร้างคดีใหม่
1. เข้าเมนู "เพิ่มคดีใหม่"
2. กรอก **case_number** (เช่น 1234/2568) - **บังคับ**
3. กรอก **case_id** (เช่น 68012345678) - **บังคับใหม่!**
4. กรอก complainant และวันที่ - **บังคับ**
5. กรอกข้อมูลอื่นๆ (optional)
6. กด "บันทึก"

### เพิ่มบัญชีธนาคาร
1. เปิดคดีที่ต้องการ
2. ไปที่แท็บ "บัญชีธนาคาร"
3. กด "+ เพิ่มบัญชี"
4. กรอกข้อมูลธนาคาร (ไม่ต้องกรอก case_id ซ้ำ!)
5. กด "บันทึก"

### เพิ่มผู้ต้องหา
1. เปิดคดีที่ต้องการ
2. ไปที่แท็บ "ผู้ต้องหา"
3. กด "+ เพิ่มผู้ต้องหา"
4. กรอกข้อมูลผู้ต้องหา
5. กด "บันทึก"

---

## ✅ Checklist

### Phase 1: ✅ เสร็จแล้ว
- [x] แก้ไข criminal_case.py model
- [x] แก้ไข criminal_case.py schema
- [x] สร้างเอกสาร migration

### Phase 2: ⏳ รอดำเนินการ
- [ ] ทดสอบการสร้างคดีใหม่ (บังคับ case_id)
- [ ] สำรองข้อมูล
- [ ] ลบ redundant columns (ถ้าต้องการ)
- [ ] อัพเดต frontend forms
- [ ] ทดสอบ end-to-end
- [ ] Deploy to production

---

## 📞 การติดต่อและการสนับสนุน

หากมีปัญหาหรือคำถาม:
1. ตรวจสอบ logs: `docker logs criminal-case-backend`
2. ตรวจสอบ database: ใช้ pgAdmin/Adminer
3. ดู error messages ใน browser console

---

**สรุป:** การปรับปรุงนี้จะทำให้ระบบมีความเสถียรและง่ายต่อการ maintain มากขึ้น โดยป้องกันปัญหาข้อมูลซ้ำซ้อนและไม่สอดคล้องกัน
