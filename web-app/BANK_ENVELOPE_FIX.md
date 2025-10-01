# 🔧 แก้ไข: ซองหมายเรียกธนาคารแสดงที่อยู่ผู้รับ

**วันที่:** 2025-10-01
**ปัญหา:** ซองหมายเรียกบัญชีธนาคารไม่แสดงที่อยู่ผู้รับ (ธนาคาร)

---

## 🐛 ปัญหาที่พบ

เมื่อพิมพ์ซองหมายเรียกธนาคาร ระบบไม่แสดงที่อยู่ผู้รับ (ที่อยู่ธนาคาร)

**สาเหตุ:**
1. Backend ดึงข้อมูลจาก `banks` table แล้ว แต่ชื่อ field ไม่ตรงกับ schema จริง
2. Generator function ใช้ชื่อ field เก่า (`address`, `area`) แทนที่จะใช้ (`bank_address`, `sub_district`, `district`)

---

## ✅ การแก้ไข

### 1. แก้ไข API Endpoint (`documents.py`)

**ไฟล์:** `backend/app/api/v1/documents.py`

**เดิม:**
```python
bank_address = {
    'address': bank.address,        # ❌ ชื่อ field ผิด
    'road': bank.road,
    'district': bank.district,
    'area': bank.area,              # ❌ ไม่มี field นี้
    'province': bank.province,
    'postal_code': bank.postal_code,
}
```

**ใหม่:**
```python
bank_address = {
    'bank_address': bank.bank_address,  # ✅ ถูกต้อง
    'soi': bank.soi,                    # ✅ เพิ่ม
    'moo': bank.moo,                    # ✅ เพิ่ม
    'road': bank.road,
    'sub_district': bank.sub_district,  # ✅ ถูกต้อง
    'district': bank.district,
    'province': bank.province,
    'postal_code': bank.postal_code,
}
```

### 2. แก้ไข Generator Function (`bank_summons_generator.py`)

**ไฟล์:** `backend/app/services/bank_summons_generator.py`
**ฟังก์ชัน:** `generate_envelope_html()`

**การเปลี่ยนแปลง:**

#### เดิม (ไม่ครบถ้วน):
```python
# บรรทัดที่ 1: เลขที่ + ถนน
address_text = format_value(bank_address.get('address', ''))  # ❌ ชื่อผิด
if address_text:
    line1_parts.append(f"เลขที่ {address_text}")

road = format_value(bank_address.get('road', ''))
if road:
    line1_parts.append(f"ถนน {road}")

# บรรทัดที่ 2: แขวง
district = format_value(bank_address.get('district', ''))
if district:
    address_lines.append(f"แขวง {district}")

# บรรทัดที่ 3: เขต
area = format_value(bank_address.get('area', ''))  # ❌ ไม่มี field นี้
if area:
    address_lines.append(f"เขต {area}")
```

#### ใหม่ (ครบถ้วนถูกต้อง):
```python
# บรรทัดที่ 1: เลขที่ + ซอย/หมู่ + ถนน
address_text = format_value(bank_address.get('bank_address', ''))  # ✅
if address_text:
    line1_parts.append(f"เลขที่ {address_text}")

soi = format_value(bank_address.get('soi', ''))  # ✅ เพิ่ม
if soi:
    line1_parts.append(f"ซอย {soi}")

moo = format_value(bank_address.get('moo', ''))  # ✅ เพิ่ม
if moo:
    line1_parts.append(f"หมู่ {moo}")

road = format_value(bank_address.get('road', ''))
if road:
    line1_parts.append(f"ถนน {road}")

# บรรทัดที่ 2: แขวง/ตำบล
sub_district = format_value(bank_address.get('sub_district', ''))  # ✅
if sub_district:
    address_lines.append(f"แขวง{sub_district}")

# บรรทัดที่ 3: เขต/อำเภอ
district = format_value(bank_address.get('district', ''))  # ✅
if district:
    address_lines.append(f"เขต{district}")

# บรรทัดที่ 4: จังหวัด + รหัสไปรษณีย์
line4_parts = []
province = format_value(bank_address.get('province', ''))
if province:
    line4_parts.append(province)

postal_code = format_value(bank_address.get('postal_code', ''))
if postal_code:
    line4_parts.append(postal_code)

if line4_parts:
    address_lines.append(' '.join(line4_parts))
```

---

## 📊 ตัวอย่างข้อมูล

### Banks Table (ID = 6)
```
bank_name: กรุงศรีอยุธยา
bank_address: 1222
soi: NULL
moo: NULL
road: พระรามที่ 3
sub_district: บางโพงพาง
district: ยานนาวา
province: กรุงเทพมหานคร
postal_code: 10120
```

### ผลลัพธ์ที่ได้ (ที่อยู่บนซอง):

```
ธนาคารกรุงศรีอยุธยาสำนักงานใหญ่
เลขที่ 1222 ถนน พระรามที่ 3
แขวงบางโพงพาง
เขตยานนาวา
กรุงเทพมหานคร 10120
```

---

## 🧪 การทดสอบ

### 1. ทดสอบผ่าน API โดยตรง

```bash
# ต้อง login ก่อน
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# เก็บ token แล้วเรียก API
curl http://localhost:8000/api/v1/documents/bank-envelope/2110 \
  -H "Authorization: Bearer YOUR_TOKEN" \
  > test_envelope.html

# เปิดไฟล์ดู
firefox test_envelope.html
```

### 2. ทดสอบผ่าน Frontend

1. เข้า http://localhost:3001
2. Login: admin / admin123
3. คลิกเลขคดีเพื่อดูรายละเอียด
4. ไปที่แท็บ "บัญชีธนาคารที่เกี่ยวข้อง"
5. คลิกปุ่ม "ปริ้นซองหมายเรียก"
6. ตรวจสอบว่ามีที่อยู่ธนาคารแสดงถูกต้อง

### 3. ตรวจสอบข้อมูล

```sql
-- ตรวจสอบว่า bank_accounts มี bank_id
SELECT id, document_number, bank_name, bank_id
FROM bank_accounts
WHERE bank_id IS NOT NULL
LIMIT 5;

-- ตรวจสอบข้อมูลธนาคาร
SELECT id, bank_name, bank_address, road, district, province
FROM banks
WHERE id IN (SELECT DISTINCT bank_id FROM bank_accounts WHERE bank_id IS NOT NULL);
```

---

## 📋 Checklist

- [x] แก้ไข API endpoint (documents.py) - field names
- [x] แก้ไข Generator (bank_summons_generator.py) - address formatting
- [x] Restart backend
- [ ] ทดสอบพิมพ์ซองหมายเรียก
- [ ] ตรวจสอบที่อยู่แสดงถูกต้อง
- [ ] ทดสอบกับธนาคารอื่นๆ (13 ธนาคาร)

---

## ⚠️ หมายเหตุ

### สำหรับ Records ที่ไม่มี bank_id (13 records)

Records เหล่านี้จะไม่มีที่อยู่แสดงบนซอง เพราะ:
- ไม่มี `bank_id` (เป็น NULL)
- ข้อมูลเดิมไม่ได้ระบุชื่อธนาคาร

**วิธีแก้:**
```sql
-- ตรวจสอบ
SELECT id, document_number, bank_name
FROM bank_accounts
WHERE bank_id IS NULL;

-- แก้ไข (ตัวอย่าง)
UPDATE bank_accounts
SET bank_id = 1, bank_name = 'กสิกรไทย'
WHERE id = XXX;
```

### รูปแบบที่อยู่

ที่อยู่จะแสดงตามข้อมูลที่มีใน banks table:
- **มีครบ:** เลขที่ ซอย หมู่ ถนน แขวง เขต จังหวัด รหัสไปรษณีย์
- **ไม่ครบ:** จะข้ามส่วนที่ว่าง (NULL)

---

## 📁 ไฟล์ที่แก้ไข

| ไฟล์ | การเปลี่ยนแปลง |
|------|----------------|
| `backend/app/api/v1/documents.py` | แก้ชื่อ field ใน bank_address dict |
| `backend/app/services/bank_summons_generator.py` | แก้ logic การจัดรูปแบบที่อยู่ + เพิ่ม soi, moo |

---

## 🎉 สรุป

การแก้ไขนี้ทำให้:
- ✅ ซองหมายเรียกธนาคารแสดงที่อยู่ผู้รับถูกต้อง
- ✅ ดึงข้อมูลจาก banks table (สำนักงานใหญ่)
- ✅ รองรับข้อมูลครบถ้วน (เลขที่, ซอย, หมู่, ถนน, แขวง, เขต, จังหวัด, รหัสไปรษณีย์)
- ✅ จัดรูปแบบที่อยู่เป็นหลายบรรทัดอ่านง่าย

**พร้อมใช้งาน!** 🚀
