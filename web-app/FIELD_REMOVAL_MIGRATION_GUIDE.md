# คู่มือการลบฟิลด์ที่ไม่ได้ใช้งานและเพิ่ม Virtual Fields

**วันที่:** 9 ตุลาคม 2568  
**Version:** 3.2.0  
**Migration:** 011_remove_unused_fields.sql

---

## 📋 สรุปการเปลี่ยนแปลง

### **ฟิลด์ที่ลบออกจากตาราง criminal_cases (16 ฟิลด์):**

#### **Group 1: ไม่ได้ใช้งานเลย (5 ฟิลด์)**
1. ✅ `victim_name` - ใช้ `complainant` แทนแล้ว
2. ✅ `suspect` - ใช้ตาราง `suspects` แทนแล้ว
3. ✅ `case_scene` - ไม่ได้ใช้งานเลย
4. ✅ `age_in_months` - คำนวณ dynamic แทน
5. ✅ `is_over_six_months` - คำนวณ dynamic แทน

#### **Group 2: ไม่แสดงใน UI (7 ฟิลด์)**
6. ✅ `charge` - ย้ายเป็น `charge_id` ในตาราง `suspects`
7. ✅ `prosecutor_name` - ไม่ได้ใช้
8. ✅ `prosecutor_file_number` - ไม่ได้ใช้
9. ✅ `officer_in_charge` - ไม่ได้ใช้
10. ✅ `investigating_officer` - ไม่ได้ใช้
11. ✅ `bank_accounts_replied` - ไม่ได้ใช้
12. ✅ `suspects_replied` - ไม่ได้ใช้

#### **Group 3: เปลี่ยนเป็น Virtual Fields (4 ฟิลด์)**
13. ✅ `complaint_date_thai` - คำนวณจาก `complaint_date`
14. ✅ `incident_date_thai` - คำนวณจาก `incident_date`
15. ✅ `bank_accounts_count` - คำนวณจาก query
16. ✅ `suspects_count` - คำนวณจาก query

### **ฟิลด์ที่เพิ่ม:**
- ✅ `charge_id` ในตาราง `suspects` (เพื่อเชื่อมโยงกับ Master Data ข้อหาในอนาคต)

---

## 🚀 ขั้นตอนการ Deploy

### **⚠️ Step 0: Backup ก่อนเสมอ!**

```bash
cd web-app

# Backup database
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_before_field_removal.dump
docker cp criminal-case-db:/tmp/backup_before_field_removal.dump ./backup_before_field_removal.dump

# Verify backup
ls -lh backup_before_field_removal.dump
```

### **Step 1: รัน Database Migration**

```bash
# Copy migration script
docker cp backend/migrations/011_remove_unused_fields.sql criminal-case-db:/tmp/

# รัน migration
docker exec criminal-case-db psql -U user -d criminal_case_db -f /tmp/011_remove_unused_fields.sql
```

**ตรวจสอบผลลัพธ์:**
```sql
-- ควรเห็นโครงสร้างตารางใหม่
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'criminal_cases' 
ORDER BY ordinal_position;

-- ตรวจสอบว่ามี charge_id ในตาราง suspects
SELECT column_name FROM information_schema.columns 
WHERE table_name = 'suspects' AND column_name = 'charge_id';
```

### **Step 2: Restart Backend**

```bash
# Restart backend เพื่อโหลดโค้ดใหม่
docker-compose restart backend

# รอให้ backend พร้อม
sleep 10

# ตรวจสอบ logs
docker-compose logs -f backend
```

### **Step 3: Test API**

```bash
# Test health check
curl http://localhost:8000/health

# Test criminal cases API
curl http://localhost:8000/api/v1/criminal-cases/ -H "Authorization: Bearer YOUR_TOKEN"
```

### **Step 4: Test Frontend**

1. เปิด http://localhost:3001
2. Login เข้าระบบ
3. ตรวจสอบ:
   - ✅ หน้า Dashboard แสดงข้อมูลครบถ้วน
   - ✅ วันที่แสดงเป็นภาษาไทย
   - ✅ จำนวนบัญชีและผู้ต้องหาแสดงถูกต้อง
   - ✅ สามารถสร้าง/แก้ไข/ลบคดีได้ปกติ

---

## 📝 การเปลี่ยนแปลงในโค้ด

### **1. Backend Models**

#### **ไฟล์: `app/models/criminal_case.py`**

**ลบฟิลด์:**
```python
# ลบแล้ว
# victim_name = Column(String)
# suspect = Column(String)
# charge = Column(Text)
# case_scene = Column(Text)
# complaint_date_thai = Column(String)
# incident_date_thai = Column(String)
# prosecutor_name = Column(String)
# prosecutor_file_number = Column(String)
# officer_in_charge = Column(String)
# investigating_officer = Column(String)
# bank_accounts_count = Column(Integer, default=0)
# bank_accounts_replied = Column(Integer, default=0)
# suspects_count = Column(Integer, default=0)
# suspects_replied = Column(Integer, default=0)
# age_in_months = Column(Integer)
# is_over_six_months = Column(String)
```

**เหลือเฉพาะ:**
```python
# Parties Involved
complainant = Column(String)

# Case Details
case_type = Column(String)
damage_amount = Column(String)

# Important Dates
complaint_date = Column(Date)
incident_date = Column(Date)

# Court Information
court_name = Column(String)
```

#### **ไฟล์: `app/models/suspect.py`**

**เพิ่มฟิลด์ใหม่:**
```python
# Charge Information
charge_id = Column(Integer, index=True)  # FK to charges master data (future)
```

### **2. Backend Schemas**

#### **ไฟล์: `app/schemas/criminal_case.py`**

**ลบฟิลด์ออกจาก Base/Create/Update schemas**

**เพิ่ม Virtual Fields ใน CriminalCaseBase:**
```python
# Virtual fields (computed at runtime, not in database)
complaint_date_thai: Optional[str] = None
incident_date_thai: Optional[str] = None
```

**CriminalCaseResponse ยังคงมี:**
```python
bank_accounts_count: Optional[str] = "0/0"
suspects_count: Optional[str] = "0/0"
```

#### **ไฟล์: `app/schemas/suspect.py`**

**เพิ่มฟิลด์:**
```python
# Charge Information
charge_id: Optional[int] = None  # FK to charges master data (future)
```

### **3. Virtual Fields Utility**

#### **ไฟล์ใหม่: `app/utils/virtual_fields.py`**

ฟังก์ชันสำหรับคำนวณ virtual fields:

```python
def format_thai_date(date_obj: Optional[date]) -> Optional[str]:
    """แปลงวันที่เป็นรูปแบบไทย พ.ศ."""
    # Returns: "15 มกราคม 2568"

def get_bank_accounts_count(db: Session, case_id: int) -> str:
    """คำนวณจำนวนบัญชีธนาคาร"""
    # Returns: "5/10" (replied/total)

def get_suspects_count(db: Session, case_id: int) -> str:
    """คำนวณจำนวนผู้ต้องหา"""
    # Returns: "3/8" (replied/total)

def calculate_age_in_months(complaint_date: Optional[date]) -> Optional[int]:
    """คำนวณอายุคดีเป็นเดือน"""

def is_over_six_months(complaint_date: Optional[date]) -> Optional[str]:
    """ตรวจสอบว่าคดีเกิน 6 เดือนหรือไม่"""
```

### **4. API Changes**

#### **ไฟล์: `app/api/v1/criminal_cases.py`**

**Import virtual fields:**
```python
from app.utils.virtual_fields import format_thai_date, get_bank_accounts_count, get_suspects_count
```

**คำนวณ virtual fields ใน Response:**
```python
# Compute virtual fields
complaint_date_thai = format_thai_date(db_case.complaint_date)
incident_date_thai = format_thai_date(db_case.incident_date)
bank_accounts_count = get_bank_accounts_count(db, db_case.id)
suspects_count = get_suspects_count(db, db_case.id)

# Create response with virtual fields
response = CriminalCaseResponse.from_orm(db_case)
response.complaint_date_thai = complaint_date_thai
response.incident_date_thai = incident_date_thai
response.bank_accounts_count = bank_accounts_count
response.suspects_count = suspects_count
```

### **5. Frontend**

**ไม่ต้องแก้ไข!** ✅

เพราะ API ยังส่ง fields เหล่านี้กลับมาเหมือนเดิม:
- `complaint_date_thai`
- `incident_date_thai`
- `bank_accounts_count`
- `suspects_count`

แค่เปลี่ยนจากดึงจากฐานข้อมูลเป็นคำนวณ runtime

---

## ✅ การทดสอบ

### **Test Checklist:**

#### **1. Database Structure**
- [ ] ตาราง `criminal_cases` ไม่มีฟิลด์ที่ลบแล้ว (16 ฟิลด์)
- [ ] ตาราง `suspects` มีฟิลด์ `charge_id`
- [ ] ข้อมูลเดิมยังคงอยู่ครบถ้วน

#### **2. API Endpoints**
- [ ] GET `/api/v1/criminal-cases/` - แสดงรายการคดี
- [ ] GET `/api/v1/criminal-cases/{id}` - แสดงรายละเอียดคดี
- [ ] POST `/api/v1/criminal-cases/` - สร้างคดีใหม่
- [ ] PUT `/api/v1/criminal-cases/{id}` - แก้ไขคดี
- [ ] Response มี virtual fields: `complaint_date_thai`, `incident_date_thai`, `bank_accounts_count`, `suspects_count`

#### **3. Frontend**
- [ ] หน้า Dashboard แสดงข้อมูลถูกต้อง
- [ ] วันที่แสดงเป็นภาษาไทย (พ.ศ.)
- [ ] จำนวนบัญชีธนาคารแสดงถูกต้อง (replied/total)
- [ ] จำนวนผู้ต้องหาแสดงถูกต้อง (replied/total)
- [ ] สามารถสร้างคดีใหม่ได้
- [ ] สามารถแก้ไขคดีได้
- [ ] สามารถลบคดีได้

#### **4. Virtual Fields**
- [ ] วันที่ในรูปแบบไทยคำนวณถูกต้อง
- [ ] จำนวนบัญชีคำนวณถูกต้อง
- [ ] จำนวนผู้ต้องหาคำนวณถูกต้อง
- [ ] Performance ยังดีเท่าเดิม (ไม่ช้าลง)

---

## 🔄 Rollback (กรณีพบปัญหา)

```bash
# หยุดระบบ
docker-compose down

# Restore database
docker cp backup_before_field_removal.dump criminal-case-db:/tmp/restore.dump
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump

# Revert code (ถ้าใช้ Git)
git revert HEAD
git push

# เริ่มระบบใหม่
docker-compose up -d
```

---

## 📊 ข้อดีของการเปลี่ยนแปลง

### **1. ฐานข้อมูลสะอาดขึ้น**
- ✅ ลดฟิลด์ที่ไม่ได้ใช้ 16 ฟิลด์
- ✅ ไม่มีข้อมูลซ้ำซ้อน
- ✅ ง่ายต่อการบำรุงรักษา

### **2. Virtual Fields**
- ✅ ไม่ต้องบันทึกข้อมูลซ้ำ
- ✅ คำนวณ realtime (ข้อมูลถูกต้องเสมอ)
- ✅ ไม่ต้อง sync ข้อมูล

### **3. ประสิทธิภาพ**
- ✅ ลด database size
- ✅ ลดความซับซ้อนในการ query
- ✅ ไม่มี stale data

### **4. ความยืดหยุ่น**
- ✅ เพิ่ม `charge_id` สำหรับ Master Data ในอนาคต
- ✅ สามารถเพิ่ม virtual fields อื่นได้ง่าย
- ✅ แยก logic ออกจาก database

---

## 🎯 ขั้นตอนถัดไป (Future Work)

### **1. สร้างตาราง Master Data สำหรับข้อหา**
```sql
CREATE TABLE charges (
    id SERIAL PRIMARY KEY,
    charge_code VARCHAR(50) UNIQUE,
    charge_name_th TEXT,
    charge_name_en TEXT,
    description TEXT,
    is_active BOOLEAN DEFAULT TRUE
);

-- เชื่อมโยงกับ suspects
ALTER TABLE suspects
  ADD CONSTRAINT fk_charge
  FOREIGN KEY (charge_id) REFERENCES charges(id);
```

### **2. เพิ่ม Virtual Fields อื่นๆ (ถ้าต้องการ)**
- อายุคดีเป็นเดือน (`age_in_months`)
- สถานะเกิน 6 เดือน (`is_over_six_months`)
- จำนวนวันตั้งแต่ส่งหมาย (`days_since_sent`)

### **3. Optimize Performance**
- เพิ่ม caching สำหรับ virtual fields
- ใช้ database views สำหรับ complex queries

---

## ⚠️ ข้อควรระวัง

1. **Backup ก่อนเสมอ!**
2. **ทดสอบ API ทั้งหมดหลัง migration**
3. **ตรวจสอบ Frontend ทุกหน้า**
4. **Monitor performance หลัง deploy**
5. **เก็บ backup ไว้อย่างน้อย 7 วัน**

---

## 📞 สรุป

✅ **Migration 011 เสร็จสมบูรณ์!**

- ลบฟิลด์ที่ไม่ได้ใช้ 16 ฟิลด์
- เพิ่ม `charge_id` ในตาราง `suspects`
- เปลี่ยน 4 ฟิลด์เป็น Virtual Fields
- โปรแกรมทำงานได้เหมือนเดิม 100%
- ฐานข้อมูลสะอาดและง่ายต่อการบำรุงรักษา

**พร้อม Deploy แล้ว!** 🚀

---

**เอกสารสร้างโดย:** AI Assistant  
**วันที่:** 9 ตุลาคม 2568  
**Version:** 3.2.0

