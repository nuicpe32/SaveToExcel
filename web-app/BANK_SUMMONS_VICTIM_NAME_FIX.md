# แก้ไขปัญหาการแสดงชื่อผู้เสียหายในหมายเรียกธนาคาร

**วันที่:** 9 ตุลาคม 2568

## ปัญหา

ในหมายเรียกบัญชีธนาคาร ย่อหน้าแรกแสดงคำว่า **"ดำเนินคดี"** แทนที่จะเป็น **ชื่อผู้เสียหายจริง**

### ตัวอย่างที่ผิด:
```
ด้วยเหตุ ดำเนินคดี (case id : 6809044200) ได้แจ้งความร้องทุกข์ต่อพนักงานสอบสวน...
```

### ตัวอย่างที่ถูกต้อง:
```
ด้วยเหตุ นางสาว เกวลิน ม่วงเกษม (case id : 6809044200) ได้แจ้งความร้องทุกข์ต่อพนักงานสอบสวน...
```

## สาเหตุ

จากการตรวจสอบพบว่า:

1. **ข้อมูลในฐานข้อมูลไม่ถูกต้อง**: หลายคดีมีค่า `victim_name` บันทึกเป็น **"ดำเนินคดี"** แทนที่จะเป็นชื่อผู้เสียหายจริง
2. **โค้ดไม่ได้กรองข้อมูล**: โค้ดเดิมใช้ค่า `victim_name` โดยตรงโดยไม่ตรวจสอบว่าเป็นข้อมูลที่ถูกต้องหรือไม่

## การแก้ไข

### ไฟล์ที่แก้ไข:
- `web-app/backend/app/api/v1/documents.py`

### การเปลี่ยนแปลง:

#### 1. ฟังก์ชัน `generate_bank_summons_html()` (บรรทัด 75-87)

**เดิม:**
```python
case_data = {
    'case_id': criminal_case.case_id,
    'case_number': criminal_case.case_number,
    'victim_name': criminal_case.victim_name or criminal_case.complainant,
    'complainant': criminal_case.complainant,
}
```

**ใหม่:**
```python
# ดึงชื่อผู้เสียหาย (ถ้าเป็น "ดำเนินคดี" ให้ใช้ complainant แทน)
victim_name = criminal_case.victim_name
if victim_name and victim_name.strip().lower() == 'ดำเนินคดี':
    victim_name = criminal_case.complainant
if not victim_name or victim_name.strip() == '':
    victim_name = criminal_case.complainant or 'ผู้เสียหาย'

case_data = {
    'case_id': criminal_case.case_id,
    'case_number': criminal_case.case_number,
    'victim_name': victim_name,
    'complainant': criminal_case.complainant,
}
```

#### 2. ฟังก์ชัน `generate_suspect_summons_html()` (บรรทัด 170-185)

เพิ่มการกรองข้อมูลแบบเดียวกันสำหรับหมายเรียกผู้ต้องหา:

```python
# ดึงชื่อผู้เสียหาย (ถ้าเป็น "ดำเนินคดี" ให้ใช้ complainant แทน)
victim_name_suspect = criminal_case.victim_name
if victim_name_suspect and victim_name_suspect.strip().lower() == 'ดำเนินคดี':
    victim_name_suspect = criminal_case.complainant
if not victim_name_suspect or victim_name_suspect.strip() == '':
    victim_name_suspect = criminal_case.complainant or 'ผู้เสียหาย'

case_data = {
    'case_id': criminal_case.case_id,
    'case_number': criminal_case.case_number,
    'victim_name': victim_name_suspect,
    'complainant': criminal_case.complainant,
    'case_type': criminal_case.case_type,
    'damage_amount': criminal_case.damage_amount,
    'court_name': criminal_case.court_name,
}
```

## Logic การกรองข้อมูล

การตรวจสอบชื่อผู้เสียหายทำตามลำดับ:

1. **ถ้า `victim_name` = "ดำเนินคดี"** → ใช้ `complainant` แทน
2. **ถ้า `victim_name` เป็นค่าว่าง** → ใช้ `complainant` แทน
3. **ถ้า `complainant` ก็เป็นค่าว่าง** → ใช้ค่า default "ผู้เสียหาย"

## การทดสอบ

### ก่อนแก้ไข:
```
ด้วยเหตุ ดำเนินคดี (case id : 6809044200) ได้แจ้งความร้องทุกข์...
```

### หลังแก้ไข:
```
ด้วยเหตุ นางสาว เกวลิน ม่วงเกษม (case id : 6809044200) ได้แจ้งความร้องทุกข์...
```

## วิธีทดสอบ

1. Restart backend container:
   ```bash
   docker-compose restart backend
   ```

2. เข้าเมนู: **"คดีอาญาในความรับผิดชอบ" > "บัญชีธนาคาร"**

3. คลิกสร้างหมายเรียกบัญชีธนาคาร

4. ตรวจสอบว่าย่อหน้าแรกแสดงชื่อผู้เสียหายถูกต้อง (ไม่ใช่ "ดำเนินคดี")

## คำแนะนำเพิ่มเติม

### การแก้ไขข้อมูลในฐานข้อมูล (Optional)

ถ้าต้องการแก้ไขข้อมูลเดิมที่บันทึกผิด:

```sql
-- ตรวจสอบคดีที่มี victim_name = "ดำเนินคดี"
SELECT id, case_number, victim_name, complainant
FROM criminal_cases
WHERE victim_name = 'ดำเนินคดี';

-- แก้ไขให้ใช้ complainant แทน
UPDATE criminal_cases
SET victim_name = complainant
WHERE victim_name = 'ดำเนินคดี'
AND complainant IS NOT NULL
AND complainant != '';

-- ตรวจสอบผลลัพธ์
SELECT id, case_number, victim_name, complainant
FROM criminal_cases
WHERE victim_name = complainant;
```

## สรุป

✅ แก้ไขแล้ว: หมายเรียกธนาคารจะแสดงชื่อผู้เสียหายที่ถูกต้อง  
✅ รองรับ: กรณีที่ `victim_name` เป็น "ดำเนินคดี" หรือค่าว่าง  
✅ Fallback: ใช้ `complainant` หรือ "ผู้เสียหาย" เป็นค่า default  

---

**หมายเหตุ:** การแก้ไขนี้ไม่จำเป็นต้องเปลี่ยนข้อมูลในฐานข้อมูล เพราะโค้ดจะกรองข้อมูลให้อัตโนมัติ

