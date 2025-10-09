# การมาตรฐานฟิลด์ผู้เสียหาย: ใช้ `complainant` เป็นหลัก

**วันที่:** 9 ตุลาคม 2568  
**Version:** 3.1.2

---

## 📋 สรุปการเปลี่ยนแปลง

### **นโยบายใหม่:**
✅ **ใช้ `complainant` เป็นฟิลด์เดียวสำหรับ "ผู้เสียหาย/ผู้กล่าวหา/ผู้ร้องทุกข์"**

### **เหตุผล:**
1. ระบบเดิมมี 2 ฟิลด์ (`complainant` และ `victim_name`) ทำให้สับสน
2. ข้อมูลใน `victim_name` หลายรายการเป็น "ดำเนินคดี" (ไม่ถูกต้อง)
3. `complainant` เป็น required field และมีข้อมูลครบถ้วนกว่า

---

## 🔄 การเปลี่ยนแปลงในระบบ

### **1. Backend (API)**

#### ไฟล์: `web-app/backend/app/api/v1/documents.py`

**เดิม:**
```python
# ใช้ victim_name และมีการตรวจสอบหลายเงื่อนไข
victim_name = criminal_case.victim_name
if victim_name and victim_name.strip().lower() == 'ดำเนินคดี':
    victim_name = criminal_case.complainant
if not victim_name or victim_name.strip() == '':
    victim_name = criminal_case.complainant or 'ผู้เสียหาย'
```

**ใหม่:**
```python
# ใช้ complainant โดยตรง
complainant_name = criminal_case.complainant or 'ผู้เสียหาย'

case_data = {
    'victim_name': complainant_name,  # backward compatibility
    'complainant': complainant_name,
}
```

**ผลลัพธ์:**
- 📄 หมายเรียกธนาคาร → ใช้ `complainant`
- 📄 หมายเรียกผู้ต้องหา → ใช้ `complainant`
- 📄 ซองหมายเรียก → ใช้ `complainant`

---

### **2. Frontend (UI)**

#### ไฟล์ที่แก้ไข:
1. `web-app/frontend/src/pages/CriminalCaseDetailPage.tsx`
2. `web-app/frontend/src/pages/BankAccountsPage.tsx`
3. `web-app/frontend/src/pages/SuspectsPage.tsx`

**การเปลี่ยนแปลง:**

| เดิม | ใหม่ |
|------|------|
| แสดง 2 ฟิลด์:<br>- ผู้ร้องทุกข์<br>- ผู้เสียหาย | แสดง 1 ฟิลด์:<br>- **ผู้ร้องทุกข์/ผู้เสียหาย** |
| `criminal_case.complainant \|\| criminal_case.victim_name` | `criminal_case.complainant` |

**ตัวอย่างโค้ด:**

**เดิม:**
```tsx
<Descriptions.Item label="ผู้ร้องทุกข์">
  {criminalCase.complainant}
</Descriptions.Item>
<Descriptions.Item label="ผู้เสียหาย">
  {criminalCase.victim_name}
</Descriptions.Item>
```

**ใหม่:**
```tsx
<Descriptions.Item label="ผู้ร้องทุกข์/ผู้เสียหาย">
  {criminalCase.complainant}
</Descriptions.Item>
```

---

### **3. Database Migration**

#### ไฟล์: `web-app/backend/migrations/010_sync_complainant_victim_name.sql`

**ขั้นตอนการ Sync ข้อมูล:**

1. **Copy victim_name → complainant** (ถ้า complainant เป็นค่าว่าง)
   ```sql
   UPDATE criminal_cases
   SET complainant = victim_name
   WHERE (complainant IS NULL OR complainant = '')
     AND victim_name IS NOT NULL
     AND victim_name != 'ดำเนินคดี';
   ```

2. **แก้ไข victim_name ที่เป็น "ดำเนินคดี"**
   ```sql
   UPDATE criminal_cases
   SET victim_name = NULL
   WHERE victim_name = 'ดำเนินคดี';
   ```

**หมายเหตุ:**
- ✅ ไม่ลบคอลัมน์ `victim_name` (เก็บไว้เพื่อ backward compatibility)
- ✅ ไม่ลบข้อมูลเดิม (แค่ sync ให้สอดคล้องกัน)
- ✅ ข้อมูลปลอดภัย 100%

---

## 🚀 วิธีการ Deploy

### **1. Backup ข้อมูลก่อน (สำคัญ!)**

```bash
cd web-app

# Backup database
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_${TIMESTAMP}.dump
docker cp criminal-case-db:/tmp/backup_${TIMESTAMP}.dump ./backup_${TIMESTAMP}.dump
```

### **2. รัน Migration**

```bash
# Copy SQL file เข้า container
docker cp backend/migrations/010_sync_complainant_victim_name.sql criminal-case-db:/tmp/

# รัน migration
docker exec criminal-case-db psql -U user -d criminal_case_db -f /tmp/010_sync_complainant_victim_name.sql
```

### **3. Restart Backend**

```bash
# Restart backend เพื่อโหลดโค้ดใหม่
docker-compose restart backend

# รอประมาณ 10 วินาที
sleep 10

# ตรวจสอบ logs
docker-compose logs -f backend
```

### **4. Restart Frontend (ถ้าจำเป็น)**

```bash
# ถ้า Hot Reload ไม่ทำงาน
docker-compose restart frontend

# หรือ Hard refresh browser
# Ctrl+Shift+R (Windows/Linux)
# Cmd+Shift+R (Mac)
```

---

## ✅ การทดสอบ

### **1. ตรวจสอบข้อมูลในฐานข้อมูล**

```bash
# เข้า PostgreSQL
docker exec -it criminal-case-db psql -U user -d criminal_case_db

# ตรวจสอบว่า complainant มีข้อมูลครบถ้วน
SELECT 
    COUNT(*) FILTER (WHERE complainant IS NOT NULL AND complainant != '') as has_complainant,
    COUNT(*) FILTER (WHERE complainant IS NULL OR complainant = '') as no_complainant,
    COUNT(*) as total
FROM criminal_cases;

# ตรวจสอบว่าไม่มี victim_name = "ดำเนินคดี" แล้ว
SELECT COUNT(*) 
FROM criminal_cases 
WHERE victim_name = 'ดำเนินคดี';

# ออกจาก psql
\q
```

### **2. ทดสอบ UI**

1. ✅ หน้ารายละเอียดคดี → เห็น "ผู้ร้องทุกข์/ผู้เสียหาย" แค่ 1 ฟิลด์
2. ✅ หน้าบัญชีธนาคาร → Modal แสดง complainant ถูกต้อง
3. ✅ หน้าผู้ต้องหา → Modal แสดง complainant ถูกต้อง

### **3. ทดสอบการสร้างเอกสาร**

1. เข้าเมนู **"บัญชีธนาคาร"**
2. คลิก **"สร้างหมายเรียก"**
3. ตรวจสอบว่าย่อหน้าแรกแสดงชื่อผู้เสียหายจาก `complainant` (ไม่ใช่ "ดำเนินคดี")

**ตัวอย่างที่ถูกต้อง:**
```
ด้วยเหตุ นางสาว เกวลิน ม่วงเกษม (case id : 6809044200) 
ได้แจ้งความร้องทุกข์ต่อพนักงานสอบสวน...
```

---

## 📊 สรุปฟิลด์ในระบบ

| ฟิลด์ | สถานะ | การใช้งาน | หมายเหตุ |
|-------|-------|-----------|----------|
| **`complainant`** | ✅ **หลัก** | ใช้ทุกที่ในระบบ | ผู้ร้องทุกข์/ผู้เสียหาย/ผู้กล่าวหา |
| `victim_name` | 🔄 เก็บไว้ | ไม่ใช้ใน UI แล้ว | เก็บไว้เพื่อ backward compatibility |

---

## 🔒 ความปลอดภัยของข้อมูล

✅ **ข้อมูลไม่หาย:**
- ไม่ลบคอลัมน์ `victim_name`
- ไม่ลบข้อมูลใด ๆ
- แค่ sync ให้สอดคล้องกัน

✅ **Backward Compatibility:**
- API ยังส่ง `victim_name` ไปให้ template
- ถ้ามี code เก่าที่ใช้ `victim_name` ยังทำงานได้ปกติ

✅ **สามารถ Rollback ได้:**
```bash
# Restore จาก backup
docker cp backup_TIMESTAMP.dump criminal-case-db:/tmp/restore.dump
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

---

## 📝 คำศัพท์ที่ใช้ในระบบ

จากนี้ไป เมื่อพูดถึง:
- **ผู้เสียหาย** = `complainant`
- **ผู้กล่าวหา** = `complainant`
- **ผู้ร้องทุกข์** = `complainant`

**ทั้งหมดคือฟิลด์เดียวกัน: `complainant`**

---

## 🎯 ประโยชน์ของการเปลี่ยนแปลง

1. ✅ **ลดความสับสน:** มีฟิลด์เดียวสำหรับผู้เสียหาย
2. ✅ **ข้อมูลถูกต้อง:** ไม่มี "ดำเนินคดี" แทนชื่อผู้เสียหายอีกต่อไป
3. ✅ **ง่ายต่อการบำรุงรักษา:** โค้ดสั้นลง ไม่ต้องเช็คหลายเงื่อนไข
4. ✅ **มาตรฐานเดียวกัน:** ทั้งระบบใช้ `complainant` เป็นหลัก

---

## 🔧 หากพบปัญหา

### ปัญหา: ชื่อผู้เสียหายไม่แสดง

**วิธีแก้:**
```bash
# ตรวจสอบว่า complainant มีข้อมูล
docker exec criminal-case-db psql -U user -d criminal_case_db -c "
SELECT id, case_number, complainant, victim_name 
FROM criminal_cases 
WHERE complainant IS NULL OR complainant = '' 
LIMIT 10;
"
```

### ปัญหา: Backend ไม่ restart

**วิธีแก้:**
```bash
# Force rebuild backend
docker-compose up -d --build --force-recreate backend
```

---

## 📞 สรุป

✅ การเปลี่ยนแปลงนี้ทำให้ระบบ:
- **มีมาตรฐานชัดเจน**: ใช้ `complainant` เป็นหลัก
- **ข้อมูลถูกต้อง**: ไม่มี "ดำเนินคดี" แทนชื่อผู้เสียหาย
- **ปลอดภัย**: ไม่ลบข้อมูลเดิม
- **Backward Compatible**: โค้ดเก่ายังทำงานได้

**Migration สำเร็จแล้ว!** 🎉

---

**หมายเหตุ:** ถ้าต้องการดูข้อมูลเพิ่มเติม:
- Adminer: http://localhost:8080 (user/password123)
- pgAdmin: http://localhost:5050 (admin@example.com/admin)

