# 💰 Damage Amount Edit Feature - เพิ่มการแก้ไขข้อมูลความเสียหาย

## 📋 ข้อกำหนดการทำงาน

ผู้ใช้ต้องการเพิ่มการแก้ไขข้อมูลความเสียหายในหน้าจอแก้ไขข้อมูลคดีอาญา เพื่อให้สามารถแก้ไขจำนวนเงินความเสียหายได้

## 🔍 การวิเคราะห์ปัญหา

### 📁 **ไฟล์ที่เกี่ยวข้อง**
- `web-app/frontend/src/pages/EditCriminalCasePage.tsx` - หน้าแก้ไขข้อมูลคดีอาญา
- `web-app/backend/app/schemas/criminal_case.py` - Schema สำหรับข้อมูลคดีอาญา
- `web-app/backend/app/api/v1/criminal_cases.py` - API endpoint สำหรับอัปเดตข้อมูล

### 🎯 **สถานะปัจจุบัน**
- ✅ **Backend Schema**: มี `damage_amount` ใน `CriminalCaseBase`, `CriminalCaseCreate`, และ `CriminalCaseUpdate`
- ✅ **Backend API**: รองรับการอัปเดต `damage_amount` ผ่าน `CriminalCaseUpdate` schema
- ❌ **Frontend**: ไม่มีฟิลด์ความเสียหายในหน้าแก้ไข

## ✨ การแก้ไขที่ทำ

### 🔧 **1. อัปเดต Interface**

#### **เพิ่ม `damage_amount` ใน CriminalCase interface**
```typescript
interface CriminalCase {
  id: number
  case_number?: string
  case_id?: string
  status: string
  complainant: string
  complaint_date: string
  case_type?: string
  court_name?: string
  damage_amount?: string  // ← เพิ่มบรรทัดนี้
}
```

#### **เพิ่ม `damage_amount` ใน CriminalCaseForm interface**
```typescript
interface CriminalCaseForm {
  case_number?: string
  case_id?: string
  status: string
  complainant: string
  complaint_date: string
  case_type?: string
  court_name?: string
  damage_amount?: string  // ← เพิ่มบรรทัดนี้
}
```

### 🔧 **2. อัปเดต Form Values**

#### **เพิ่ม `damage_amount` ใน form.setFieldsValue**
```typescript
// Set form values
form.setFieldsValue({
  case_number: response.data.case_number,
  case_id: response.data.case_id,
  status: response.data.status,
  complainant: response.data.complainant,
  case_type: response.data.case_type,
  court_name: response.data.court_name,
  damage_amount: response.data.damage_amount,  // ← เพิ่มบรรทัดนี้
  complaint_date: response.data.complaint_date ? dayjs(response.data.complaint_date) : undefined
})
```

### 🔧 **3. เพิ่มฟิลด์ความเสียหายในฟอร์ม**

#### **เปลี่ยนจาก Form.Item เดียวเป็น Row/Col layout**
```typescript
// เดิม: Form.Item เดียวสำหรับเขตอำนาจศาล
<Form.Item label="เขตอำนาจศาล" name="court_name">
  <Select placeholder="เลือกศาล" ...>
    ...
  </Select>
</Form.Item>

// ใหม่: Row/Col layout สำหรับเขตอำนาจศาลและความเสียหาย
<Row gutter={16}>
  <Col span={12}>
    <Form.Item label="เขตอำนาจศาล" name="court_name">
      <Select placeholder="เลือกศาล" ...>
        ...
      </Select>
    </Form.Item>
  </Col>
  <Col span={12}>
    <Form.Item
      label="ความเสียหาย (บาท)"
      name="damage_amount"
    >
      <Input placeholder="เช่น 500000" />
    </Form.Item>
  </Col>
</Row>
```

## 📊 **ผลลัพธ์ที่ได้**

### ✅ **ฟิลด์ใหม่ที่เพิ่ม**
- **Label**: "ความเสียหาย (บาท)"
- **Name**: "damage_amount"
- **Type**: Input field
- **Placeholder**: "เช่น 500000"
- **Layout**: อยู่ใน Column ขวาของเขตอำนาจศาล

### 🎨 **การจัดวาง**
```
┌─────────────────────────────────────────────────────────┐
│                    แก้ไขข้อมูลคดีอาญา                    │
├─────────────────────────────────────────────────────────┤
│ เลขที่คดี        │ CaseID                               │
│ สถานะคดี        │ ประเภทคดี                            │
│ ผู้ร้องทุกข์                                              │
│ วันที่/เวลา รับคำร้องทุกข์                               │
│ เขตอำนาจศาล     │ ความเสียหาย (บาท) ← ฟิลด์ใหม่        │
│ [ยกเลิก] [บันทึก]                                        │
└─────────────────────────────────────────────────────────┘
```

## 🔧 **Technical Implementation**

### 📁 **ไฟล์ที่แก้ไข**
- `web-app/frontend/src/pages/EditCriminalCasePage.tsx`

### 🛠️ **การเปลี่ยนแปลง**
1. **Interface Updates**: เพิ่ม `damage_amount` ใน interfaces
2. **Form Integration**: เพิ่มใน `form.setFieldsValue`
3. **UI Layout**: เปลี่ยนเป็น Row/Col layout
4. **Form Field**: เพิ่ม Input field สำหรับความเสียหาย

### 🔄 **Backend Compatibility**
- ✅ **Schema Support**: `CriminalCaseUpdate` schema รองรับ `damage_amount`
- ✅ **API Support**: PUT endpoint รองรับการอัปเดต `damage_amount`
- ✅ **Database Field**: ตาราง `criminal_cases` มีคอลัมน์ `damage_amount`

## 🧪 **การทดสอบ**

### ✅ **Test Cases**
1. **Field Display**: ฟิลด์ความเสียหายแสดงในฟอร์ม
2. **Data Loading**: ข้อมูลความเสียหายโหลดได้ถูกต้อง
3. **Data Saving**: บันทึกข้อมูลความเสียหายได้
4. **Form Validation**: ฟิลด์ไม่บังคับกรอก (optional)

### 🔍 **Testing Steps**
1. ✅ เปิดหน้าเว็บ http://localhost:3001
2. ✅ เข้าสู่ระบบ
3. ✅ ไปที่หน้า "แดชบอร์ด"
4. ✅ คลิก "แก้ไข" สำหรับคดีอาญาใดๆ
5. ✅ ตรวจสอบฟิลด์ "ความเสียหาย (บาท)"
6. ✅ แก้ไขข้อมูลความเสียหาย
7. ✅ บันทึกการเปลี่ยนแปลง
8. ✅ ตรวจสอบว่าข้อมูลถูกบันทึก

## 📈 **Benefits**

### 🎯 **User Experience**
- **Complete Information**: สามารถแก้ไขข้อมูลความเสียหายได้
- **Consistent Layout**: ฟิลด์จัดวางอย่างสม่ำเสมอ
- **Easy Input**: Input field ที่ใช้งานง่าย

### 🔧 **Technical Benefits**
- **Data Completeness**: ข้อมูลคดีครบถ้วนมากขึ้น
- **API Consistency**: ใช้ API ที่มีอยู่แล้ว
- **Schema Alignment**: สอดคล้องกับ backend schema

## 🚀 **การใช้งาน**

### 💡 **Use Cases**
1. **Case Management**: จัดการข้อมูลความเสียหายของคดี
2. **Financial Tracking**: ติดตามจำนวนเงินความเสียหาย
3. **Reporting**: สร้างรายงานตามความเสียหาย
4. **Data Analysis**: วิเคราะห์ข้อมูลความเสียหาย

### 📊 **Data Format**
- **Input Type**: Text input
- **Expected Format**: ตัวเลข (เช่น 500000)
- **Storage**: VARCHAR ในฐานข้อมูล
- **Display**: แสดงในฟอร์มแก้ไข

## 🔮 **Future Enhancements**

### 🎨 **UI Improvements**
- **Currency Formatting**: แสดงจำนวนเงินในรูปแบบสกุลเงิน
- **Input Validation**: ตรวจสอบรูปแบบตัวเลข
- **Auto-formatting**: จัดรูปแบบตัวเลขอัตโนมัติ

### 🔧 **Functional Improvements**
- **Damage Categories**: แยกประเภทความเสียหาย
- **Currency Support**: รองรับหลายสกุลเงิน
- **Historical Tracking**: ติดตามการเปลี่ยนแปลงความเสียหาย

## 📊 **Impact Analysis**

### ⚡ **Performance Impact**
- **Minimal**: เพิ่มฟิลด์ 1 ฟิลด์เท่านั้น
- **No API Changes**: ใช้ API ที่มีอยู่แล้ว
- **No Database Changes**: ใช้คอลัมน์ที่มีอยู่แล้ว

### 🔒 **Data Integrity**
- **Optional Field**: ไม่บังคับกรอก
- **String Storage**: เก็บเป็น VARCHAR
- **No Constraints**: ไม่มี validation constraints

## 🎉 **สรุปผลการทำงาน**

✅ **เพิ่มฟิลด์สำเร็จ**: เพิ่มฟิลด์ความเสียหายในหน้าแก้ไขข้อมูลคดีอาญา

✅ **Data Integration**: เชื่อมต่อกับ backend API ได้ถูกต้อง

✅ **User Interface**: ฟิลด์จัดวางอย่างสวยงามและใช้งานง่าย

✅ **Functionality**: สามารถแก้ไขและบันทึกข้อมูลความเสียหายได้

---

## 📋 **การใช้งาน**

### 🔗 **การเข้าถึง**
1. เปิดหน้าเว็บ http://localhost:3001
2. เข้าสู่ระบบ
3. ไปที่หน้า "แดชบอร์ด"
4. คลิก "แก้ไข" สำหรับคดีอาญาที่ต้องการ

### 📝 **การแก้ไขความเสียหาย**
1. ในฟิลด์ "ความเสียหาย (บาท)"
2. กรอกจำนวนเงิน (เช่น 500000)
3. คลิก "บันทึก"
4. ระบบจะบันทึกข้อมูลและกลับไปหน้าหลัก

### 🔍 **การตรวจสอบ**
- ข้อมูลความเสียหายจะแสดงในฟิลด์เมื่อเปิดหน้าแก้ไข
- สามารถแก้ไขและบันทึกได้ตามปกติ
- ข้อมูลจะถูกส่งไปยัง backend API

---

**🎯 ฟิลด์ความเสียหายเพิ่มในหน้าแก้ไขข้อมูลคดีอาญาเรียบร้อยแล้ว!**

**💰 ระบบพร้อมสำหรับการจัดการข้อมูลความเสียหาย!**
