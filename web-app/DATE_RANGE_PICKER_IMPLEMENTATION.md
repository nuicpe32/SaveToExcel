# ✅ เพิ่ม Date Range Picker สำหรับช่วงเวลาที่ทำธุรกรรม

**วันที่:** 1 ตุลาคม 2568  
**ฟิลด์:** ช่วงเวลาที่ทำธุรกรรม (time_period)

---

## 🎯 วัตถุประสงค์

เพิ่ม Date Range Picker เพื่อ:
1. เลือกช่วงวันที่ได้ง่าย (2 วันที่: เริ่มต้น - สิ้นสุด)
2. แสดงผลเป็นภาษาไทยแบบสั้น
3. บันทึกเป็น text ในฐานข้อมูล

---

## 📝 Format ที่ต้องการ

### ตัวอย่าง Output:
```
1 ม.ค. 68 - 5 ม.ค. 68
15 พ.ค. 68 - 20 พ.ค. 68
1 ต.ค. 68 - 31 ต.ค. 68
```

### รูปแบบ:
```
{วัน} {เดือนย่อไทย} {ปี 2 หลัก พ.ศ.} - {วัน} {เดือนย่อไทย} {ปี 2 หลัก พ.ศ.}
```

---

## 🛠️ การทำงาน

### 1. UI Component
- ใช้ **Ant Design RangePicker**
- เลือก 2 วันที่พร้อมกัน (Start Date & End Date)
- แสดง Preview: "จะบันทึกเป็น: X"

### 2. การแปลงข้อมูล
```typescript
// เลือกวันที่: 1 มกราคม 2025 - 5 มกราคม 2025
// ↓ แปลงเป็น
// "1 ม.ค. 68 - 5 ม.ค. 68"

// Logic:
1. วัน = date()
2. เดือน = formatThaiMonth(month())
3. ปี = (year() + 543).slice(-2)  // แปลง ค.ศ. เป็น พ.ศ. 2 หลัก
```

### 3. บันทึกลงฐานข้อมูล
- เก็บเป็น **VARCHAR/TEXT**
- ไม่ใช่ DATE type
- บันทึกตรงๆ เป็นข้อความไทย

---

## 🔧 Implementation Details

### ฟังก์ชัน Helper

#### 1. formatThaiMonth()
```typescript
const formatThaiMonth = (month: number): string => {
  const thaiMonths = [
    'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 
    'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 
    'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.'
  ]
  return thaiMonths[month]
}
```

#### 2. formatDateRangeToThai()
```typescript
const formatDateRangeToThai = (
  dates: [dayjs.Dayjs, dayjs.Dayjs] | null
): string => {
  if (!dates || !dates[0] || !dates[1]) return ''
  
  const [start, end] = dates
  
  // Start Date
  const startDay = start.date()
  const startMonth = formatThaiMonth(start.month())
  const startYear = (start.year() + 543).toString().slice(-2)
  
  // End Date
  const endDay = end.date()
  const endMonth = formatThaiMonth(end.month())
  const endYear = (end.year() + 543).toString().slice(-2)
  
  return `${startDay} ${startMonth} ${startYear} - ${endDay} ${endMonth} ${endYear}`
}
```

---

## 💻 Code Example

### Component
```typescript
<Form.Item label="ช่วงเวลาที่ทำธุรกรรม">
  <RangePicker
    style={{ width: '100%' }}
    format="DD/MM/YYYY"
    placeholder={['วันที่เริ่มต้น', 'วันที่สิ้นสุด']}
    onChange={(dates) => {
      setDateRange(dates)
      if (dates) {
        const formattedText = formatDateRangeToThai(dates)
        form.setFieldsValue({ time_period: formattedText })
      }
    }}
  />
  
  {/* Hidden field สำหรับเก็บค่า */}
  <Form.Item name="time_period" noStyle>
    <Input type="hidden" />
  </Form.Item>
  
  {/* Preview */}
  {dateRange && (
    <div style={{ marginTop: 8, color: '#1890ff' }}>
      จะบันทึกเป็น: {formatDateRangeToThai(dateRange)}
    </div>
  )}
</Form.Item>
```

---

## 📊 Data Flow

```
1. User เลือกวันที่ใน RangePicker
   ↓
2. onChange trigger
   ↓
3. setDateRange(dates) → update state
   ↓
4. formatDateRangeToThai(dates) → แปลงเป็น Thai text
   ↓
5. form.setFieldsValue({ time_period: text }) → เก็บใน form
   ↓
6. แสดง Preview ให้ user เห็น
   ↓
7. Submit → ส่ง text ไปบันทึกใน database
```

---

## 🎨 UI/UX

### Before (Input Text):
```
[ช่วงเวลาที่ทำธุรกรรม: _________________________]
placeholder: "เช่น ม.ค. 2568 - มี.ค. 2568"
```
**ปัญหา:** ต้องพิมพ์เอง อาจพิมพ์ผิด format ไม่ตรงกัน

### After (RangePicker):
```
[วันที่เริ่มต้น ▼] - [วันที่สิ้นสุด ▼]
📅 Calendar Picker

Preview: จะบันทึกเป็น: 1 ม.ค. 68 - 5 ม.ค. 68
```
**ข้อดี:** 
- เลือกจาก Calendar ง่าย
- Format ถูกต้องเสมอ
- มี Preview แสดงผลจริง

---

## 🔄 ตัวอย่างการใช้งาน

### Scenario 1: ธุรกรรมเดือนมกราคม
```
เลือก: 1 Jan 2025 - 31 Jan 2025
บันทึก: "1 ม.ค. 68 - 31 ม.ค. 68"
```

### Scenario 2: ธุรกรรมข้ามเดือน
```
เลือก: 25 Dec 2024 - 5 Jan 2025
บันทึก: "25 ธ.ค. 67 - 5 ม.ค. 68"
```

### Scenario 3: ธุรกรรมข้ามปี
```
เลือก: 15 Dec 2024 - 15 Jan 2025
บันทึก: "15 ธ.ค. 67 - 15 ม.ค. 68"
```

---

## 📦 Dependencies

### Packages Required:
```json
{
  "antd": "^5.12.5",     // RangePicker component
  "dayjs": "^1.11.10"    // Date manipulation
}
```

### Imports:
```typescript
import { DatePicker } from 'antd'
import dayjs from 'dayjs'
import 'dayjs/locale/th'

const { RangePicker } = DatePicker
```

---

## ✨ Features

### 1. Auto Format
- เลือกวันที่ → แปลงเป็นภาษาไทยอัตโนมัติ
- ไม่ต้องพิมพ์เอง

### 2. Preview
- แสดง Preview ก่อนบันทึก
- มั่นใจว่า format ถูกต้อง

### 3. Validation
- ไม่สามารถเลือกวันที่เริ่มต้นหลังวันที่สิ้นสุด
- RangePicker จัดการให้อัตโนมัติ

### 4. Clear Function
- สามารถลบค่าที่เลือกได้
- Reset ทั้งหมดเมื่อปิด Modal

---

## 🧪 Testing

### Test Cases:

#### 1. เลือกช่วงวันที่ปกติ
```
Input: 1 Jan 2025 - 5 Jan 2025
Expected: "1 ม.ค. 68 - 5 ม.ค. 68"
```

#### 2. เลือกช่วงวันเดียวกัน
```
Input: 1 Jan 2025 - 1 Jan 2025
Expected: "1 ม.ค. 68 - 1 ม.ค. 68"
```

#### 3. เลือกข้ามเดือน
```
Input: 25 Dec 2024 - 5 Jan 2025
Expected: "25 ธ.ค. 67 - 5 ม.ค. 68"
```

#### 4. ไม่เลือกวันที่
```
Input: null
Expected: ""
```

---

## 📝 Database Storage

### Table: bank_accounts
```sql
time_period VARCHAR(50)

-- ตัวอย่างข้อมูล:
'1 ม.ค. 68 - 5 ม.ค. 68'
'15 พ.ค. 68 - 20 พ.ค. 68'
'1 ต.ค. 68 - 31 ต.ค. 68'
```

**หมายเหตุ:** 
- เก็บเป็น text ธรรมดา
- ไม่ใช่ DATE type
- ไม่สามารถ query by date range ได้
- เหมาะสำหรับการแสดงผลเท่านั้น

---

## 🎯 Use Cases

### 1. ระบุช่วงเวลาที่บัญชีมีการทำธุรกรรม
```
"เราต้องการข้อมูลบัญชีนี้ตั้งแต่ 1 ม.ค. 68 - 31 มี.ค. 68"
```

### 2. แสดงในเอกสารหนังสือขอข้อมูล
```
ขอข้อมูลธุรกรรมในช่วงเวลา: 1 ม.ค. 68 - 31 มี.ค. 68
```

### 3. บันทึกเป็น reference
```
ข้อมูลนี้เกี่ยวข้องกับช่วงเวลา: 15 พ.ค. 68 - 20 พ.ค. 68
```

---

## 💡 Tips

### 1. ใช้ RangePicker แทน Input
```typescript
// ❌ แบบเก่า
<Input placeholder="เช่น ม.ค. 2568 - มี.ค. 2568" />

// ✅ แบบใหม่
<RangePicker onChange={handleDateChange} />
```

### 2. แสดง Preview เสมอ
```typescript
{dateRange && (
  <div>จะบันทึกเป็น: {formatDateRangeToThai(dateRange)}</div>
)}
```

### 3. Reset State เมื่อปิด Modal
```typescript
const handleCancel = () => {
  form.resetFields()
  setDateRange(null)  // ← สำคัญ!
  onClose(false)
}
```

---

## ✅ Checklist

- [x] Import RangePicker
- [x] สร้างฟังก์ชัน formatThaiMonth()
- [x] สร้างฟังก์ชัน formatDateRangeToThai()
- [x] เพิ่ม state dateRange
- [x] เปลี่ยน Input เป็น RangePicker
- [x] เพิ่ม Preview ข้อความ
- [x] Update handleSubmit()
- [x] Reset state เมื่อปิด Modal
- [x] ทดสอบการใช้งาน

---

## 🚀 ทดสอบได้เลย!

### Dev Mode (Hot Reload):
```
1. เปิด http://localhost:5173
2. เพิ่มบัญชีธนาคาร
3. เลือกช่วงเวลาที่ทำธุรกรรม
4. เห็น Preview ทันที
5. บันทึก → ดูผลในฐานข้อมูล
```

---

## 📊 สรุป

**ก่อน:**
- พิมพ์เอง: "ม.ค. 2568 - มี.ค. 2568"
- ไม่มีมาตรฐาน
- อาจผิด format

**หลัง:**
- เลือกจาก Calendar: 1 Jan - 31 Mar
- Format อัตโนมัติ: "1 ม.ค. 68 - 31 มี.ค. 68"
- ถูกต้องเสมอ ✅

---

**Status:** ✅ พร้อมใช้งาน  
**Updated:** 1 ตุลาคม 2568, 14:15:00 +07:00

