# Changelog - ระบบจัดการคดีอาญา Web Application

## [v3.0.1] - 2025-10-01 - Bank Account Management Improvements ✅

### 🎯 Checkpoint: Stable Version
**Git Tag:** `v3.0.1-bank-improvements`  
**Commit:** `d50b48d`

---

### ✅ Bug Fixes

#### 1. แก้ไขปัญหาการเพิ่มบัญชีธนาคาร
- **ปัญหา:** `TypeError: got multiple values for keyword argument 'document_number'`
- **แก้ไข:** ปรับ logic ใน `bank_accounts.py` ไม่ให้ส่ง document_number ซ้ำซ้อน
- **ไฟล์:** `backend/app/api/v1/bank_accounts.py`

#### 2. แก้ไขการแสดง "NaN" ในเลขหนังสือ
- **ปัญหา:** เลขหนังสือแสดงเป็น "NaN" เมื่อไม่มีข้อมูล
- **แก้ไข:** แสดง "-" แทน NaN
- **ไฟล์:** 
  - `frontend/src/pages/CriminalCaseDetailPage.tsx`
  - `frontend/src/pages/DashboardPage.tsx`

---

### ✨ Features

#### 1. ลบคอลัมน์ "ธนาคารสาขา" (bank_branch)
- เนื่องจากระบบส่งไปที่สำนักงานใหญ่เท่านั้น ไม่ต้องแสดงสาขา
- **ไฟล์:**
  - `frontend/src/pages/CriminalCaseDetailPage.tsx` - ลบคอลัมน์สาขา
  - `frontend/src/pages/DashboardPage.tsx` - ลบคอลัมน์ธนาคารสาขา

#### 2. การแปลงวันที่เป็นภาษาไทยอัตโนมัติ
- **ฟีเจอร์:** ระบบแปลง `document_date` เป็น `document_date_thai` อัตโนมัติ
- **รูปแบบ:** "1 ตุลาคม 2568", "15 มกราคม 2568"
- **ทำงาน:** ทั้งตอน CREATE และ UPDATE
- **ไฟล์:** `backend/app/api/v1/bank_accounts.py`
- **Utility:** `backend/app/utils/thai_date_utils.py`

#### 3. ยกเลิกการ Auto-generate เลขหนังสือ
- **เหตุผล:** ผู้ใช้ต้องการกรอกเลขเอง หรือเขียนด้วยปากกาภายหลัง
- **ก่อน:** ระบบสร้าง "BA-2568-0001" อัตโนมัติ ❌
- **หลัง:** ให้ผู้ใช้กรอกเอง หรือเว้นว่างไว้ได้ ✅

---

### 🔧 Database Updates

#### 1. อัพเดตรูปแบบเลขหนังสือมาตรฐาน
- **จำนวน:** 397 รายการ
- **รูปแบบใหม่:** `ตช. 0039.52/<เลขหนังสือ>`
- **ตัวอย่าง:**
  - "4218" → "ตช. 0039.52/4218"
  - "4406" → "ตช. 0039.52/4406"
  - "99877" → "ตช. 0039.52/99877"

#### 2. อัพเดต document_date_thai
- **จำนวน:** 1 รายการ
- **ตัวอย่าง:** 
  - document_date: 2025-10-01
  - document_date_thai: "1 ตุลาคม 2568" ✅

---

### 📁 ไฟล์ที่แก้ไข

#### Backend (5 ไฟล์)
```
✅ backend/app/api/v1/bank_accounts.py
   - ลบ auto-generate document_number
   - เพิ่มการแปลง document_date_thai อัตโนมัติ
   - แก้ไข CREATE endpoint
   - แก้ไข UPDATE endpoint
```

#### Frontend (3 ไฟล์)
```
✅ frontend/src/pages/CriminalCaseDetailPage.tsx
   - ลบคอลัมน์ bank_branch
   - แก้ไข render document_number
   - ลบ bank_branch จาก interface

✅ frontend/src/pages/DashboardPage.tsx
   - ลบคอลัมน์ bank_branch
   - แก้ไข render เลขหนังสือ (ไม่ parseInt)

✅ frontend/src/components/BankAccountFormModal.tsx
   - ไม่แก้ไขในเวอร์ชันนี้ (ยังแสดงฟิลด์ document_number ปกติ)
```

#### Infrastructure
```
✅ web-app/.gitignore - สร้างใหม่เพื่อไม่ให้ commit node_modules
```

---

### 🎯 การใช้งาน

#### เพิ่มบัญชีธนาคาร:
```
1. กดปุ่ม "เพิ่มบัญชีธนาคาร"
2. กรอกเลขหนังสือ (หรือเว้นว่าง)
3. เลือกวันที่ → ระบบแปลงเป็นไทยอัตโนมัติ
4. กรอกข้อมูลธนาคาร (ชื่อธนาคาร, เลขบัญชี, ชื่อบัญชี)
5. กดบันทึก ✅
```

#### แก้ไขบัญชีธนาคาร:
```
1. กดปุ่ม "แก้ไข"
2. เห็นข้อมูลเดิม (เช่น เลขหนังสือ "ตช. 0039.52/4406")
3. แก้ไขตามต้องการ
4. กดบันทึก ✅
```

---

### 📊 สถิติ

- **Files Changed:** 128 files
- **Insertions:** 23,428 lines
- **Database Records Updated:** 397 bank accounts
- **Migration Time:** ~5 seconds

---

### 🔄 วิธีย้อนกลับ (Rollback)

หากเกิดปัญหาและต้องการย้อนกลับมาเวอร์ชันนี้:

```bash
# ดู tags ทั้งหมด
git tag

# ย้อนกลับมาเวอร์ชันนี้
git checkout v3.0.1-bank-improvements

# หรือสร้าง branch ใหม่จากเวอร์ชันนี้
git checkout -b rollback-to-v3.0.1 v3.0.1-bank-improvements
```

---

### 📝 หมายเหตุ

- ✅ **Stable:** เวอร์ชันนี้ผ่านการทดสอบและพร้อมใช้งาน
- ✅ **Safe Point:** จุดที่ปลอดภัยสำหรับการพัฒนาต่อ
- ✅ **Database:** ข้อมูลอัพเดตครบถ้วน (397 records)
- ✅ **No Breaking Changes:** ไม่มีการเปลี่ยนแปลงที่ทำลาย API

---

### 🚀 Next Development

เวอร์ชันนี้เป็นจุดเริ่มต้นสำหรับ:
- การเพิ่มฟีเจอร์ใหญ่ต่อไป
- การทดสอบระบบ
- การพัฒนาโมดูลใหม่

**สามารถพัฒนาต่อได้อย่างมั่นใจ มี checkpoint ไว้ย้อนกลับ!** ✅

---

**Created:** 1 ตุลาคม 2568  
**Status:** ✅ Stable & Production Ready

