# 📄 Frontend Update: Criminal Case Detail Page with Forms

## Overview
เพิ่มหน้ารายละเอียดคดีพร้อมฟอร์มสำหรับเพิ่ม/แก้ไขบัญชีธนาคารและผู้ต้องหา

**วันที่:** 2025-10-01
**เวอร์ชัน:** v2.10.0 (Frontend Enhancement)

---

## 🎯 สิ่งที่เพิ่มเข้ามา

### 1. หน้ารายละเอียดคดี (CriminalCaseDetailPage)

**ไฟล์:** `frontend/src/pages/CriminalCaseDetailPage.tsx`

**คุณสมบัติ:**
- แสดงข้อมูลคดีแบบละเอียด (Descriptions layout)
- แบ่งเป็น 2 แท็บ:
  - **บัญชีธนาคาร**: แสดงรายการบัญชีทั้งหมดที่เกี่ยวข้องกับคดี
  - **ผู้ต้องหา**: แสดงรายการผู้ต้องหาทั้งหมดที่เกี่ยวข้องกับคดี
- ปุ่ม "เพิ่ม" สำหรับเพิ่มข้อมูลใหม่
- ปุ่ม "แก้ไข" และ "ลบ" ในแต่ละแถวของตาราง
- ปุ่ม "กลับ" เพื่อกลับไปหน้า Dashboard

**การใช้งาน:**
```
URL: /cases/:id
ตัวอย่าง: /cases/1
```

**ข้อมูลที่แสดง:**
- เลขคดี, Case ID, สถานะ
- วันที่รับคำกล่าวหา
- ผู้กล่าวหา, ผู้เสียหาย, ผู้ต้องหา
- ข้อกล่าวหา, มูลค่าความเสียหาย
- เจ้าหน้าที่รับผิดชอบ
- หมายเหตุ

---

### 2. ฟอร์มบัญชีธนาคาร (BankAccountFormModal)

**ไฟล์:** `frontend/src/components/BankAccountFormModal.tsx`

**ฟิลด์ทั้งหมด (ตาม Database Schema):**

#### ข้อมูลเอกสาร
- `document_number` - เลขที่เอกสาร (Auto-generated ถ้าไม่ระบุ)
- `document_date` - วันที่เอกสาร (DatePicker)

#### ข้อมูลธนาคาร (บังคับ)
- `bank_name` - ชื่อธนาคาร (Select dropdown, **required**)
  - รองรับธนาคารไทย 36 แห่ง
  - มีฟังก์ชัน search
- `bank_branch` - สาขา (**required**)
- `account_number` - เลขที่บัญชี (**required**)
- `account_name` - ชื่อบัญชี (**required**)
- `account_owner` - เจ้าของบัญชี (เพิ่มเติม)
- `time_period` - ช่วงเวลาที่ทำธุรกรรม

#### ที่อยู่ธนาคาร
- `bank_address` - ที่อยู่
- `soi` - ซอย
- `moo` - หมู่
- `road` - ถนน
- `postal_code` - รหัสไปรษณีย์
- `sub_district` - ตำบล/แขวง
- `district` - อำเภอ/เขต
- `province` - จังหวัด

#### การส่งและรับเอกสาร
- `delivery_date` - วันที่ส่งเอกสาร (DatePicker)
- `delivery_month` - เดือนที่ส่ง
- `delivery_time` - เวลาที่ส่ง
- `reply_status` - สถานะตอบกลับ (Switch: ตอบแล้ว/รอตอบกลับ)
- `response_date` - วันที่ได้รับตอบกลับ (DatePicker)
- `status` - สถานะ (Select: pending/sent/replied/completed)

#### อื่นๆ
- `notes` - หมายเหตุ (TextArea)

**การ Validate:**
- ธนาคาร, สาขา, เลขที่บัญชี, ชื่อบัญชี = required fields

**รายชื่อธนาคาร:**
```typescript
ธนาคารกรุงเทพ, ธนาคารกสิกรไทย, ธนาคารไทยพาณิชย์, ธนาคารกรุงไทย,
ธนาคารกรุงศรีอยุธยา, ธนาคารทหารไทยธนชาต, ธนาคารเกียรตินาคินภัทร,
ธนาคารซีไอเอ็มบีไทย, ธนาคารทิสโก้, ธนาคารยูโอบี, ธนาคารธนชาต,
ธนาคารแลนด์ แอนด์ เฮ้าส์, ธนาคารไอซีบีซี (ไทย),
ธนาคารพัฒนาวิสาหกิจขนาดกลางและขนาดย่อมแห่งประเทศไทย,
ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร, ธนาคารออมสิน,
ธนาคารอาคารสงเคราะห์, ธนาคารอิสลามแห่งประเทศไทย
```

---

### 3. ฟอร์มผู้ต้องหา (SuspectFormModal)

**ไฟล์:** `frontend/src/components/SuspectFormModal.tsx`

**ฟิลด์ทั้งหมด (ตาม Database Schema):**

#### ข้อมูลเอกสาร
- `document_number` - เลขที่เอกสาร (Auto-generated ถ้าไม่ระบุ)
- `document_date` - วันที่เอกสาร (DatePicker)

#### ข้อมูลผู้ต้องหา (บังคับ)
- `suspect_name` - ชื่อผู้ต้องหา (**required**)
- `suspect_id_card` - เลขบัตรประชาชน (ต้องเป็นตัวเลข 13 หลัก)
- `suspect_address` - ที่อยู่ผู้ต้องหา (TextArea)

#### ข้อมูลสถานีตำรวจ
- `police_station` - สถานีตำรวจ
- `police_province` - จังหวัด
- `police_address` - ที่อยู่สถานีตำรวจ (TextArea)

#### ข้อมูลคดี
- `case_type` - ประเภทคดี (Select)
  - ฉ้อโกง
  - โกงรายได้
  - ยักยอกทรัพย์
  - ฟอกเงิน
  - อื่นๆ
- `damage_amount` - มูลค่าความเสียหาย

#### การนัดหมาย
- `appointment_date` - วันนัดหมาย (DatePicker)
- `appointment_time` - เวลานัดหมาย

#### สถานะ
- `reply_status` - สถานะมาตามนัด (Switch: มาแล้ว/ยังไม่มา)
- `status` - สถานะ (Select)
  - รอดำเนินการ (pending)
  - ออกหมายเรียกแล้ว (summoned)
  - มาตามนัด (appeared)
  - ไม่มาตามนัด (not_appeared)
  - เสร็จสิ้น (completed)

#### อื่นๆ
- `notes` - หมายเหตุ (TextArea)

**การ Validate:**
- ชื่อผู้ต้องหา = required
- เลขบัตรประชาชน = ต้องเป็นตัวเลข 13 หลัก (ถ้ามีการกรอก)

---

### 4. เพิ่ม Route ใน App.tsx

**ไฟล์:** `frontend/src/App.tsx`

**การเปลี่ยนแปลง:**
```typescript
// Import
import CriminalCaseDetailPage from './pages/CriminalCaseDetailPage'

// Route
<Route path="cases/:id" element={<CriminalCaseDetailPage />} />
```

---

## 🔧 API Endpoints ที่ใช้

### Criminal Cases
- `GET /api/v1/criminal-cases/:id` - ดึงข้อมูลคดี

### Bank Accounts
- `GET /api/v1/bank-accounts/?criminal_case_id=:id` - ดึงรายการบัญชี
- `POST /api/v1/bank-accounts/` - เพิ่มบัญชีใหม่
- `PUT /api/v1/bank-accounts/:id` - แก้ไขบัญชี
- `DELETE /api/v1/bank-accounts/:id` - ลบบัญชี

### Suspects
- `GET /api/v1/suspects/?criminal_case_id=:id` - ดึงรายการผู้ต้องหา
- `POST /api/v1/suspects/` - เพิ่มผู้ต้องหาใหม่
- `PUT /api/v1/suspects/:id` - แก้ไขผู้ต้องหา
- `DELETE /api/v1/suspects/:id` - ลบผู้ต้องหา

---

## 📋 การใช้งาน

### 1. เข้าสู่หน้ารายละเอียดคดี

**วิธีที่ 1: จาก Dashboard**
```typescript
// ใน DashboardPage.tsx ให้เพิ่มลิงก์
import { useNavigate } from 'react-router-dom'

const navigate = useNavigate()

<Button onClick={() => navigate(`/cases/${record.id}`)}>
  ดูรายละเอียด
</Button>
```

**วิธีที่ 2: พิมพ์ URL โดยตรง**
```
http://localhost:3001/cases/1
```

### 2. เพิ่มบัญชีธนาคาร

1. เลือกแท็บ "บัญชีธนาคาร"
2. คลิกปุ่ม "เพิ่มบัญชีธนาคาร"
3. กรอกข้อมูล (ฟิลด์บังคับ: ธนาคาร, สาขา, เลขที่บัญชี, ชื่อบัญชี)
4. คลิก "เพิ่ม"

### 3. แก้ไขบัญชีธนาคาร

1. คลิกปุ่ม "แก้ไข" ในแถวที่ต้องการ
2. แก้ไขข้อมูล
3. คลิก "บันทึก"

### 4. ลบบัญชีธนาคาร

1. คลิกปุ่ม "ลบ" ในแถวที่ต้องการ
2. ยืนยันการลบ

### 5. เพิ่ม/แก้ไข/ลบผู้ต้องหา

ทำแบบเดียวกับบัญชีธนาคาร แต่อยู่ในแท็บ "ผู้ต้องหา"

---

## 🎨 UI/UX Features

### Layout
- **Modal Width:**
  - BankAccountFormModal: 900px (กว้างกว่าเพราะมีฟิลด์มาก)
  - SuspectFormModal: 800px
- **Form Layout:** Vertical layout with Row/Col grid (gutter 16)
- **Sections:** แบ่งหมวดหมู่ชัดเจนด้วย h4 สีฟ้า (#1890ff)

### Input Components
- **DatePicker:** รูปแบบ DD/MM/YYYY
- **Select:** Searchable dropdown
- **Switch:** สำหรับสถานะแบบ Boolean
- **TextArea:** สำหรับข้อมูลยาวๆ (หมายเหตุ, ที่อยู่)
- **Tooltip:** คำแนะนำสำหรับฟิลด์ document_number

### Validation
- **Required Fields:** แสดงเครื่องหมาย * สีแดง
- **Pattern Validation:** เลขบัตรประชาชน 13 หลัก
- **Error Messages:** ข้อความภาษาไทยที่ชัดเจน

### Table Features
- **Scrollable:** scroll={{ x: 1200 }}
- **Pagination:** 10 รายการต่อหน้า
- **Tags:** สีสันแสดงสถานะ (เขียว/ส้ม)
- **Fixed Columns:** คอลัมน์การดำเนินการตรึงทางขวา

---

## ✅ Testing Checklist

- [ ] เข้าหน้ารายละเอียดคดีผ่าน URL `/cases/1`
- [ ] ดูข้อมูลคดีแสดงครบถ้วน
- [ ] เปิดแท็บบัญชีธนาคาร - แสดงรายการถูกต้อง
- [ ] เปิดแท็บผู้ต้องหา - แสดงรายการถูกต้อง
- [ ] เพิ่มบัญชีธนาคารใหม่ - บันทึกสำเร็จ
- [ ] แก้ไขบัญชีธนาคาร - อัพเดตสำเร็จ
- [ ] ลบบัญชีธนาคาร - ลบสำเร็จ
- [ ] เพิ่มผู้ต้องหาใหม่ - บันทึกสำเร็จ
- [ ] แก้ไขผู้ต้องหา - อัพเดตสำเร็จ
- [ ] ลบผู้ต้องหา - ลบสำเร็จ
- [ ] Validation ทำงาน - กรอกไม่ครบแจ้ง error
- [ ] DatePicker แสดงรูปแบบไทย
- [ ] ปุ่มกลับไปหน้า Dashboard ทำงาน

---

## 🚀 Next Steps (Recommended)

### 1. เพิ่มลิงก์จาก Dashboard
ในไฟล์ `DashboardPage.tsx` เพิ่มคอลัมน์ "การดำเนินการ":

```typescript
{
  title: 'การดำเนินการ',
  key: 'action',
  render: (_, record) => (
    <Space size="small">
      <Button
        type="link"
        onClick={() => navigate(`/cases/${record.id}`)}
      >
        ดูรายละเอียด
      </Button>
      <Button
        type="link"
        onClick={() => navigate(`/edit-criminal-case/${record.id}`)}
      >
        แก้ไข
      </Button>
    </Space>
  ),
}
```

### 2. เพิ่มฟังก์ชันพิมพ์เอกสาร
- ปุ่มพิมพ์หมายเรียกผู้ต้องหา
- ปุ่มพิมพ์หนังสือขอข้อมูลบัญชี

### 3. เพิ่มสถิติในหน้ารายละเอียด
- จำนวนบัญชีที่ตอบกลับแล้ว/รอตอบกลับ
- จำนวนผู้ต้องหาที่มาตามนัด/ไม่มา

---

## 📁 ไฟล์ที่สร้าง/แก้ไข

| ไฟล์ | สถานะ | จุดประสงค์ |
|------|-------|-----------|
| `frontend/src/pages/CriminalCaseDetailPage.tsx` | ✅ สร้างใหม่ | หน้ารายละเอียดคดี |
| `frontend/src/components/BankAccountFormModal.tsx` | ✅ สร้างใหม่ | ฟอร์มบัญชีธนาคาร |
| `frontend/src/components/SuspectFormModal.tsx` | ✅ สร้างใหม่ | ฟอร์มผู้ต้องหา |
| `frontend/src/App.tsx` | ✅ แก้ไข | เพิ่ม route `/cases/:id` |

---

## 💡 Tips สำหรับ Developer

### Auto-generated Document Numbers
ทั้ง BankAccountFormModal และ SuspectFormModal มี tooltip บอกว่า:
> "ระบบจะสร้างอัตโนมัติถ้าไม่ระบุ"

Backend ควรมีตรรกะสร้างเลขที่เอกสารอัตโนมัติ (เช่น BA-2568-0001, SP-2568-0001)

### Date Formatting
DatePicker ใช้ dayjs และส่งค่าเป็น `YYYY-MM-DD` format:
```typescript
document_date: values.document_date
  ? values.document_date.format('YYYY-MM-DD')
  : null
```

### Form Reset
เมื่อปิด Modal (ทั้งกด OK และ Cancel) จะรีเซ็ตฟอร์มเสมอ:
```typescript
form.resetFields()
```

### Error Handling
แยก error type:
- `err.errorFields` - validation error จาก Ant Design
- อื่นๆ - API error

---

## 🔗 Related Documentation

- `DATABASE_STRUCTURE_IMPROVEMENTS.md` - โครงสร้างฐานข้อมูล
- `DATABASE_SCHEMA.md` - Schema details
- `QUICK_SUMMARY.md` - กฎใหม่เกี่ยวกับ case_id

---

**สร้างโดย:** Claude Code
**วันที่:** 2025-10-01
