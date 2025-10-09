# รายงานการตรวจสอบฟิลด์ที่ไม่ได้ใช้งานในตาราง criminal_cases

**วันที่:** 9 ตุลาคม 2568  
**ผู้ตรวจสอบ:** AI Assistant  
**ฐานข้อมูล:** PostgreSQL - `criminal_case_db`  
**ตาราง:** `criminal_cases`

---

## 📊 สรุปผลการตรวจสอบ

จากการตรวจสอบทั้ง Backend และ Frontend พบว่า:

| ฟิลด์ | สถานะ | คำอธิบาย |
|-------|--------|----------|
| `victim_name` | ✅ **จริง - ไม่ได้ใช้แล้ว** | ใช้ `complainant` แทนแล้ว |
| `suspect` | ✅ **จริง - ไม่ได้ใช้** | ใช้ตาราง `suspects` แทนแล้ว |
| `charge` | ⚠️ **ยังใช้อยู่ แต่ควรย้าย** | อยู่ในฐานข้อมูล แต่ไม่ได้แสดงใน UI |
| `case_scene` | ✅ **จริง - ไม่ได้ใช้** | ไม่มีการใช้งานเลย |
| `complaint_date_thai` | ❌ **ยังใช้อยู่** | ใช้งานอยู่ใน UI และ API |
| `incident_date_thai` | ⚠️ **ใช้เล็กน้อย** | อยู่ในโค้ดแต่ไม่ค่อยใช้ |
| `prosecutor_name` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model แต่ไม่ได้ใช้ใน UI |
| `prosecutor_file_number` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model แต่ไม่ได้ใช้ใน UI |
| `officer_in_charge` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model แต่ไม่ได้ใช้ใน UI |
| `investigating_officer` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model แต่ไม่ได้ใช้ใน UI |
| `bank_accounts_count` | ❌ **ยังใช้อยู่** | คำนวณแบบ dynamic ใน API |
| `bank_accounts_replied` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model แต่ไม่ได้ใช้งานจริง |
| `suspects_count` | ❌ **ยังใช้อยู่** | คำนวณแบบ dynamic ใน API |
| `suspects_replied` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model แต่ไม่ได้ใช้งานจริง |
| `age_in_months` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model เท่านั้น ไม่ได้ใช้งาน |
| `is_over_six_months` | ⚠️ **อยู่ในโครงสร้าง** | อยู่ใน model เท่านั้น ไม่ได้ใช้งาน |

---

## 📋 รายละเอียดแต่ละฟิลด์

### ✅ 1. **victim_name** - ไม่ได้ใช้แล้ว (จริง)

**การตรวจสอบ:**
- พบการใช้งาน: 168 ครั้งใน 29 ไฟล์
- แต่ส่วนใหญ่เป็น:
  - เอกสาร documentation (MD files)
  - Migration scripts
  - Backup files

**การใช้งานจริงใน Code:**
- ✅ Backend: ไม่ได้ใช้แล้ว (ใช้ `complainant` แทน)
- ✅ Frontend: ไม่ได้แสดงใน UI แล้ว
- ✅ Migration: มีการ sync ข้อมูลจาก `victim_name` → `complainant` แล้ว

**สรุป:** ✅ **ถูกต้อง - สามารถลบได้**

---

### ✅ 2. **suspect** - ไม่ได้ใช้ (จริง)

**การตรวจสอบ:**
- พบการใช้งาน: 8 ครั้งใน 7 ไฟล์
- เป็นเฉพาะใน:
  - Model definition (`models/criminal_case.py`)
  - Schema definition (`schemas/criminal_case.py`)
  - Migration scripts (เก่า)
  - Init scripts (ไม่ได้ใช้จริง)

**การใช้งานจริง:**
- ✅ ระบบใช้ตาราง `suspects` แทนแล้ว (แยกเป็นรายการ)
- ✅ UI ไม่มีการแสดงฟิลด์ `suspect` จากตาราง `criminal_cases`
- ✅ API ไม่ได้ส่งค่านี้ไปให้ Frontend

**สรุป:** ✅ **ถูกต้อง - สามารถลบได้**

---

### ⚠️ 3. **charge** - ยังใช้อยู่ แต่ควรย้าย (จริงบางส่วน)

**การตรวจสอบ:**
- พบการใช้งาน: 0 ครั้งในการค้นหา `.charge`
- แต่พบว่ามีในโครงสร้างฐานข้อมูล

**ตรวจสอบเพิ่มเติม:**
- อยู่ใน Model: ✅
- อยู่ใน Schema: ✅
- ใช้ใน UI: ❌ ไม่แสดง
- ใช้ใน API: ⚠️ รับส่งได้ แต่ไม่ได้ใช้งานจริง

**ตาราง suspects ปัจจุบัน:**
- ❌ **ไม่มีฟิลด์ `charge`** (ตรวจสอบแล้ว)

**ข้อเสนอแนะ:**
- ✅ ควรเพิ่มฟิลด์ `charge` ในตาราง `suspects`
- ✅ แล้วลบออกจากตาราง `criminal_cases`

**สรุป:** ⚠️ **ถูกต้อง - ควรย้ายไปตาราง suspects**

---

### ✅ 4. **case_scene** - ไม่ได้ใช้ (จริง)

**การตรวจสอบ:**
- พบการใช้งาน: 11 ครั้งใน 7 ไฟล์
- เป็นเฉพาะ:
  - Model definition
  - Schema definition
  - Backup files

**การใช้งานจริง:**
- ❌ ไม่มีใน Frontend เลย
- ❌ ไม่มีใน API logic
- ❌ ไม่มีในเอกสารใดๆ

**สรุป:** ✅ **ถูกต้อง - ไม่ได้ใช้งานเลย สามารถลบได้**

---

### ❌ 5. **complaint_date_thai** - ยังใช้อยู่ (ไม่จริง!)

**การตรวจสอบ:**
- พบการใช้งาน: 27 ครั้งใน 9 ไฟล์

**การใช้งานจริง:**

**Frontend:**
```tsx
// CriminalCaseDetailPage.tsx
{criminalCase.complaint_date_thai || criminalCase.complaint_date}

// DashboardPage.tsx
complaint_date_thai?: string
{selected.complaint_date_thai || '-'}
```

**Backend:**
```python
# criminal_cases.py
complaint_date_str = db_case.complaint_date_thai or str(db_case.complaint_date)
db_case.complaint_date_thai = migration._format_thai_date(db_case.complaint_date)
```

**สรุป:** ❌ **ไม่ถูกต้อง - ยังใช้อยู่ใน UI และ API**

**หมายเหตุ:** แม้จะสามารถคำนวณ format ได้ แต่การเก็บไว้ช่วยลด overhead ในการ format ทุกครั้ง

---

### ⚠️ 6. **incident_date_thai** - ใช้เล็กน้อย

**การตรวจสอบ:**
- พบการใช้งาน: 27 ครั้งใน 9 ไฟล์ (รวมกับ complaint_date_thai)

**การใช้งานจริง:**
- อยู่ใน Model และ Schema
- อยู่ใน migration scripts
- ไม่ค่อยแสดงใน UI

**สรุป:** ⚠️ **ควรเก็บไว้เพื่อความสมบูรณ์ของข้อมูล**

---

### ⚠️ 7-10. **prosecutor_name, prosecutor_file_number, officer_in_charge, investigating_officer**

**การตรวจสอบ:**
- พบการใช้งาน: 16-27 ครั้ง
- ส่วนใหญ่ใน Model, Schema, และ backup files

**การใช้งานจริง:**
- ✅ อยู่ในโครงสร้างฐานข้อมูล
- ❌ **ไม่แสดงใน UI**
- ⚠️ อาจมีการใช้งานใน `post_arrests` table

**ตรวจสอบ post_arrests:**
```python
# พบว่ามีฟิลด์เหล่านี้ใน post_arrests table
prosecutor_name
```

**สรุป:** ⚠️ **มีในโครงสร้าง แต่ไม่ได้ใช้งานจริงในตาราง criminal_cases**

---

### ❌ 11-14. **bank_accounts_count, bank_accounts_replied, suspects_count, suspects_replied**

**การตรวจสอบ:**
- พบการใช้งาน: 60 ครั้งใน 12 ไฟล์

**การใช้งานจริง:**

**Backend API (criminal_cases.py):**
```python
# คำนวณแบบ dynamic
db_case.bank_accounts_count = get_bank_accounts_count(db, db_case.id)
db_case.suspects_count = get_suspects_count(db, db_case.id)

def get_bank_accounts_count(db: Session, case_id: int) -> str:
    # Query จากฐานข้อมูลจริง
    total = db.query(BankAccount).filter(...).count()
    replied = db.query(BankAccount).filter(..., reply_status=True).count()
    return f"{replied}/{total}"
```

**Frontend:**
```tsx
// แสดงใน UI
{criminalCase.bank_accounts_count || 0}
{criminalCase.suspects_count || 0}
```

**สรุป:** ❌ **ไม่ถูกต้อง - ยังใช้อยู่ แต่คำนวณแบบ dynamic ไม่ได้บันทึกลงฐานข้อมูล**

**หมายเหตุ:** ฟิลด์เหล่านี้อยู่ใน Model แต่ไม่ได้บันทึกค่าจริงๆ เป็นเพียง **virtual field** ที่คำนวณตอน runtime

**การตรวจสอบเพิ่มเติม:**
- `bank_accounts_replied` และ `suspects_replied` → **ไม่ได้ใช้งานจริง** (ไม่มีในโค้ด)

---

### ⚠️ 15-16. **age_in_months, is_over_six_months**

**การตรวจสอบ:**
- พบการใช้งาน: 17 ครั้งใน 6 ไฟล์
- ส่วนใหญ่ใน Model definition และ documentation

**การใช้งานจริง:**
- อยู่ใน Model: ✅
- ใช้ใน API: ❌
- แสดงใน UI: ❌

**สรุป:** ⚠️ **ควรเป็น calculated field ไม่จำเป็นต้องเก็บในฐานข้อมูล**

---

## ✅ สรุปรายการฟิลด์ที่สามารถลบได้

### **ลบได้แน่นอน (5 ฟิลด์):**
1. ✅ `victim_name` - ใช้ `complainant` แทนแล้ว
2. ✅ `suspect` - ใช้ตาราง `suspects` แทนแล้ว
3. ✅ `case_scene` - ไม่ได้ใช้งานเลย
4. ✅ `age_in_months` - ควรคำนวณ dynamic
5. ✅ `is_over_six_months` - ควรคำนวณ dynamic

### **ควรลบ (แต่ต้องย้ายก่อน) (1 ฟิลด์):**
6. ⚠️ `charge` - **ควรย้ายไปตาราง suspects** (ตามที่คุณบอก)

### **ควรลบ (แต่ไม่ได้ใช้งานจริง) (6 ฟิลด์):**
7. ⚠️ `prosecutor_name` - ไม่แสดงใน UI
8. ⚠️ `prosecutor_file_number` - ไม่แสดงใน UI
9. ⚠️ `officer_in_charge` - ไม่แสดงใน UI
10. ⚠️ `investigating_officer` - ไม่แสดงใน UI
11. ⚠️ `bank_accounts_replied` - ไม่ได้ใช้งาน
12. ⚠️ `suspects_replied` - ไม่ได้ใช้งาน

### **ไม่ควรลบ (ยังใช้อยู่) (4 ฟิลด์):**
13. ❌ `complaint_date_thai` - **ยังใช้ใน UI และ API**
14. ❌ `incident_date_thai` - ยังใช้อยู่
15. ❌ `bank_accounts_count` - **คำนวณ dynamic แต่ใช้ใน UI**
16. ❌ `suspects_count` - **คำนวณ dynamic แต่ใช้ใน UI**

---

## 📌 ข้อเสนอแนะ

### **Phase 1: ลบฟิลด์ที่ไม่ได้ใช้เลย (ปลอดภัย)**
```sql
ALTER TABLE criminal_cases
  DROP COLUMN victim_name,
  DROP COLUMN suspect,
  DROP COLUMN case_scene,
  DROP COLUMN age_in_months,
  DROP COLUMN is_over_six_months;
```

### **Phase 2: เพิ่ม charge ในตาราง suspects แล้วย้ายข้อมูล**
```sql
-- เพิ่มคอลัมน์ใหม่
ALTER TABLE suspects
  ADD COLUMN charge TEXT;

-- ย้ายข้อมูล (ถ้ามี)
-- ต้องพิจารณาว่าจะจับคู่ข้อมูลอย่างไร

-- ลบออกจาก criminal_cases
ALTER TABLE criminal_cases
  DROP COLUMN charge;
```

### **Phase 3: ลบฟิลด์ที่ไม่ได้ใช้งานจริง**
```sql
ALTER TABLE criminal_cases
  DROP COLUMN prosecutor_name,
  DROP COLUMN prosecutor_file_number,
  DROP COLUMN officer_in_charge,
  DROP COLUMN investigating_officer,
  DROP COLUMN bank_accounts_replied,
  DROP COLUMN suspects_replied;
```

### **Phase 4: จัดการ count fields**
- เก็บ `bank_accounts_count` และ `suspects_count` ใน Model
- แต่ไม่ต้องมีในฐานข้อมูล (เป็น computed property)

---

## ⚠️ คำเตือน

**ฟิลด์ที่ไม่ควรลบ:**
1. `complaint_date_thai` - **ยังใช้งานอยู่**
2. `incident_date_thai` - **ยังใช้งานอยู่**
3. `bank_accounts_count` - เป็น virtual field แต่ยังใช้ใน response
4. `suspects_count` - เป็น virtual field แต่ยังใช้ใน response

---

## 📊 สรุปท้ายสุด

จากการตรวจสอบ **16 ฟิลด์**:
- ✅ **ถูกต้องทั้งหมด:** 5 ฟิลด์ (สามารถลบได้)
- ⚠️ **ถูกต้องบางส่วน:** 7 ฟิลด์ (ควรพิจารณาลบ)
- ❌ **ไม่ถูกต้อง:** 4 ฟิลด์ (ยังใช้อยู่ ไม่ควรลบ)

**รอคำสั่งในขั้นตอนถัดไปครับ!** 🎯

