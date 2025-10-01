# 📋 สรุปการปรับปรุงระบบ - Quick Reference

## ✅ สิ่งที่ทำเสร็จแล้ว

### 1. ล็อค case_id เป็น Required Field
- ✅ **Model:** `criminal_case.py` - case_id เป็น `nullable=False`
- ✅ **Schema:** `criminal_case.py` - case_id เป็น `str` (required)
- ✅ **Backend:** restart แล้ว, ทำงานปกติ

### 2. โครงสร้างฐานข้อมูล
```
criminal_cases (Parent - Master Data)
  ├── case_number (required, unique)
  ├── case_id (required) ← NEW!
  ├── complainant
  └── victim_name

bank_accounts (Child)
  └── criminal_case_id (FK, required)

suspects (Child)
  └── criminal_case_id (FK, required)
```

---

## 🎯 กฎใหม่

### สร้างคดีใหม่
**บังคับต้องมี:**
1. ✅ case_number (เช่น 1234/2568)
2. ✅ **case_id** (เช่น 68012345678) ← **ต้องใส่!**
3. ✅ complainant
4. ✅ complaint_date

### เพิ่มบัญชีธนาคาร / ผู้ต้องหา
- เลือก criminal_case_id จากคดีที่มีอยู่
- ไม่ต้องใส่ case_id, complainant ซ้ำ (ดึงจาก parent)

---

## 📁 ไฟล์ที่แก้ไข

| ไฟล์ | การเปลี่ยนแปลง |
|------|----------------|
| `backend/app/models/criminal_case.py` | ✅ case_id nullable=False |
| `backend/app/schemas/criminal_case.py` | ✅ case_id: str (required) |

---

## 🚀 ทดสอบ

### API Endpoints
```bash
# Test create case (ต้องมี case_id)
curl -X POST http://localhost:8000/api/v1/criminal-cases \
  -H "Content-Type: application/json" \
  -d '{
    "case_number": "1234/2568",
    "case_id": "68012345678",
    "complainant": "Test",
    "complaint_date": "2025-01-01",
    "status": "ระหว่างสอบสวน"
  }'

# Test without case_id (should fail)
# Error 422: field required
```

### Frontend
- เปิด: http://localhost:3001
- สร้างคดีใหม่ → ต้องกรอก case_id (บังคับ)

---

## ⚠️ Migration สำหรับข้อมูลเก่า

ข้อมูลเก่าที่มี case_id = NULL จะต้องแก้ไข:

```sql
-- ตรวจสอบ
SELECT id, case_number FROM criminal_cases WHERE case_id IS NULL;

-- แก้ไข (ตัวอย่าง)
UPDATE criminal_cases
SET case_id = '68012345678'  -- ใส่ case_id จริง
WHERE id = 123;
```

---

## 📚 เอกสารเพิ่มเติม

- **คู่มือฉบับเต็ม:** `DATABASE_STRUCTURE_IMPROVEMENTS.md`
- **ERD:** `DATABASE_ERD.md`
- **Schema:** `DATABASE_SCHEMA.md`

---

## 🔧 การ Rollback (ถ้าจำเป็น)

```python
# criminal_case.py
case_id = Column(String, index=True)  # เอา nullable=False ออก

# criminal_case schema
case_id: Optional[str] = None  # เปลี่ยนกลับเป็น Optional
```

Restart backend:
```bash
docker restart criminal-case-backend
```

---

## ✅ Checklist สำหรับ Admin

- [x] Backend models updated
- [x] Backend schemas updated
- [x] Backend restarted
- [ ] Frontend forms updated (ถ้าจำเป็น)
- [ ] User training (แจ้งให้ user รู้ว่า case_id บังคับแล้ว)
- [ ] Monitor logs สำหรับ errors

---

**Next Step:** ทดสอบสร้างคดีใหม่ผ่าน Web UI
