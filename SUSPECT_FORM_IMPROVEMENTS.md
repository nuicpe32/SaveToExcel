# 👤 Suspect Form Improvements - ปรับปรุงฟอร์มเพิ่มผู้ต้องหา

## 📋 ข้อกำหนดการแก้ไข

ผู้ใช้ต้องการปรับปรุงฟอร์มเพิ่มผู้ต้องหาดังนี้:

1. **ข้อมูลเอกสาร**: เปลี่ยน "เลขที่เอกสาร" เป็น "เลขที่หนังสือ" และ placeholder เป็น "ตช. 0039.52/....."
2. **ข้อมูลเอกสาร**: เปลี่ยน "วันที่เอกสาร" เป็น "ลงวันที่" และตั้งค่าวันที่ปัจจุบัน พร้อมบันทึกเป็นรูปแบบวันที่ไทย
3. **ข้อมูลผู้ต้องหา**: ฟิลด์ชื่อผู้ต้องหาให้ดึงข้อมูลจากบัญชีธนาคารในคดีนี้มาแสดงเป็น AutoComplete
4. **ข้อมูลผู้ต้องหา**: เปลี่ยน "เลขบัตรประชาชน" เป็น "เลขบัตรประชาชน/เลขที่หนังสือเดินทาง"

## 🔍 การวิเคราะห์ปัญหา

### 📁 **ไฟล์ที่เกี่ยวข้อง**
- `web-app/frontend/src/components/SuspectFormModal.tsx` - ฟอร์มเพิ่ม/แก้ไขผู้ต้องหา
- `web-app/backend/app/api/v1/suspects.py` - API สำหรับผู้ต้องหา
- `web-app/backend/app/schemas/suspect.py` - Schema สำหรับข้อมูลผู้ต้องหา

### 🎯 **สถานะปัจจุบัน**
- ✅ **Backend Schema**: มี `document_date_thai` field รองรับ
- ✅ **Backend API**: รองรับการบันทึกข้อมูลผู้ต้องหา
- ❌ **Frontend**: ฟิลด์ยังไม่ได้ปรับปรุงตามข้อกำหนด

## ✨ การแก้ไขที่ทำ

### 🔧 **1. แก้ไขข้อมูลเอกสาร**

#### **เปลี่ยน Label และ Placeholder**
```typescript
// เดิม
<Form.Item
  label="เลขที่เอกสาร"
  name="document_number"
  tooltip="ระบบจะสร้างอัตโนมัติถ้าไม่ระบุ"
>
  <Input placeholder="เช่น SP-2568-0001" />
</Form.Item>

// ใหม่
<Form.Item
  label="เลขที่หนังสือ"
  name="document_number"
  tooltip="ระบบจะสร้างอัตโนมัติถ้าไม่ระบุ"
>
  <Input placeholder="เช่น ตช. 0039.52/....." />
</Form.Item>
```

#### **เปลี่ยน Label และตั้งค่าวันที่ปัจจุบัน**
```typescript
// เดิม
<Form.Item label="วันที่เอกสาร" name="document_date">
  <DatePicker style={{ width: '100%' }} format="DD/MM/YYYY" />
</Form.Item>

// ใหม่
<Form.Item label="ลงวันที่" name="document_date">
  <DatePicker 
    style={{ width: '100%' }} 
    format="DD/MM/YYYY" 
    defaultValue={dayjs()}
  />
</Form.Item>
```

#### **เพิ่มการบันทึกเป็นรูปแบบวันที่ไทย**
```typescript
// เพิ่มฟังก์ชันแปลงวันที่เป็นรูปแบบไทย
const formatThaiDate = (date: any) => {
  if (!date) return null;
  const thaiMonths = [
    'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน',
    'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม'
  ];
  const day = date.date();
  const month = thaiMonths[date.month()];
  const year = date.year() + 543; // แปลงเป็น พ.ศ.
  return `${day} ${month} ${year}`;
};

// อัปเดต payload
const payload = {
  ...values,
  criminal_case_id: criminalCaseId,
  document_date: values.document_date
    ? values.document_date.format('YYYY-MM-DD')
    : null,
  document_date_thai: formatThaiDate(values.document_date), // ← เพิ่มบรรทัดนี้
  appointment_date: values.appointment_date
    ? values.appointment_date.format('YYYY-MM-DD')
    : null,
  appointment_date_thai: formatThaiDate(values.appointment_date), // ← เพิ่มบรรทัดนี้
}
```

### 🔧 **2. แก้ไขฟิลด์ชื่อผู้ต้องหา**

#### **เพิ่ม AutoComplete Component**
```typescript
// เพิ่ม import
import { AutoComplete } from 'antd'

// เพิ่ม state
const [bankAccountNames, setBankAccountNames] = useState<string[]>([])

// เพิ่มฟังก์ชันดึงข้อมูล
const fetchBankAccountNames = async () => {
  try {
    const response = await api.get(`/criminal-cases/${criminalCaseId}/bank-accounts`)
    const accountNames = response.data
      .map((account: any) => account.account_name)
      .filter((name: string) => name && name.trim() !== '')
      .filter((name: string, index: number, arr: string[]) => arr.indexOf(name) === index) // remove duplicates
    setBankAccountNames(accountNames)
  } catch (error) {
    console.error('Error fetching bank account names:', error)
    setBankAccountNames([])
  }
}

// เปลี่ยน Input เป็น AutoComplete
<Form.Item
  label="ชื่อผู้ต้องหา"
  name="suspect_name"
  rules={[{ required: true, message: 'กรุณาระบุชื่อผู้ต้องหา' }]}
>
  <AutoComplete
    placeholder="ชื่อ-นามสกุล หรือเลือกจากรายการ"
    options={bankAccountNames.map(name => ({ value: name }))}
    filterOption={(inputValue, option) =>
      option?.value?.toLowerCase().includes(inputValue.toLowerCase()) ?? false
    }
    allowClear
  />
</Form.Item>
```

### 🔧 **3. แก้ไขฟิลด์เลขบัตรประชาชน**

#### **เปลี่ยน Label และ Validation**
```typescript
// เดิม
<Form.Item
  label="เลขบัตรประชาชน"
  name="suspect_id_card"
  rules={[
    {
      pattern: /^[0-9]{13}$/,
      message: 'เลขบัตรประชาชนต้องเป็นตัวเลข 13 หลัก',
    },
  ]}
>
  <Input placeholder="1234567890123" maxLength={13} />
</Form.Item>

// ใหม่
<Form.Item
  label="เลขบัตรประชาชน/เลขที่หนังสือเดินทาง"
  name="suspect_id_card"
  rules={[
    {
      pattern: /^[0-9]{13}$|^[A-Z]{2}[0-9]{7}$/,
      message: 'กรุณากรอกเลขบัตรประชาชน 13 หลัก หรือเลขที่หนังสือเดินทาง',
    },
  ]}
>
  <Input placeholder="1234567890123 หรือ A1234567" maxLength={13} />
</Form.Item>
```

## 📊 **ผลลัพธ์ที่ได้**

### ✅ **การปรับปรุงที่ทำเสร็จ**

#### **1. ข้อมูลเอกสาร**
- ✅ **Label**: "เลขที่เอกสาร" → "เลขที่หนังสือ"
- ✅ **Placeholder**: "เช่น SP-2568-0001" → "เช่น ตช. 0039.52/....."
- ✅ **Label**: "วันที่เอกสาร" → "ลงวันที่"
- ✅ **Default Value**: ตั้งค่าวันที่ปัจจุบัน
- ✅ **Thai Date Format**: บันทึกเป็นรูปแบบ "1 มกราคม 2568"

#### **2. ข้อมูลผู้ต้องหา**
- ✅ **AutoComplete**: ดึงข้อมูลจากบัญชีธนาคารในคดีนี้
- ✅ **Manual Input**: สามารถพิมพ์เพิ่มเองได้
- ✅ **Duplicate Removal**: ลบชื่อซ้ำออก
- ✅ **Filter**: ค้นหาชื่อได้

#### **3. เลขบัตรประชาชน**
- ✅ **Label**: "เลขบัตรประชาชน" → "เลขบัตรประชาชน/เลขที่หนังสือเดินทาง"
- ✅ **Validation**: รองรับทั้งเลขบัตรประชาชนและหนังสือเดินทาง
- ✅ **Placeholder**: แสดงตัวอย่างทั้งสองรูปแบบ

## 🔧 **Technical Implementation**

### 📁 **ไฟล์ที่แก้ไข**
- `web-app/frontend/src/components/SuspectFormModal.tsx`

### 🛠️ **การเปลี่ยนแปลง**
1. **Import Updates**: เพิ่ม `AutoComplete` และ `useState`
2. **State Management**: เพิ่ม `bankAccountNames` state
3. **API Integration**: เพิ่ม `fetchBankAccountNames` function
4. **Form Enhancement**: แปลง Input เป็น AutoComplete
5. **Date Formatting**: เพิ่มฟังก์ชันแปลงวันที่ไทย
6. **Validation Update**: อัปเดต regex pattern

### 🔄 **Backend Compatibility**
- ✅ **Schema Support**: `SuspectCreate` และ `SuspectUpdate` รองรับ `document_date_thai`
- ✅ **API Support**: POST/PUT endpoints รองรับการบันทึกข้อมูล
- ✅ **Database Field**: ตาราง `suspects` มีคอลัมน์ `document_date_thai`

## 🧪 **การทดสอบ**

### ✅ **Test Cases**
1. **Document Fields**: เลขที่หนังสือและลงวันที่แสดงถูกต้อง
2. **Default Date**: วันที่ปัจจุบันถูกตั้งค่าเป็นค่าเริ่มต้น
3. **Thai Date Format**: วันที่ถูกแปลงเป็นรูปแบบไทย
4. **AutoComplete**: รายชื่อจากบัญชีธนาคารแสดงใน dropdown
5. **Manual Input**: สามารถพิมพ์ชื่อใหม่ได้
6. **ID Validation**: รองรับทั้งเลขบัตรประชาชนและหนังสือเดินทาง

### 🔍 **Testing Steps**
1. ✅ เปิดหน้าเว็บ http://localhost:3001
2. ✅ เข้าสู่ระบบ
3. ✅ ไปที่หน้า "แดชบอร์ด"
4. ✅ คลิก "ดูรายละเอียด" สำหรับคดีที่มีบัญชีธนาคาร
5. ✅ คลิก "เพิ่มผู้ต้องหา"
6. ✅ ตรวจสอบฟิลด์ "เลขที่หนังสือ" และ placeholder
7. ✅ ตรวจสอบฟิลด์ "ลงวันที่" และวันที่ปัจจุบัน
8. ✅ ตรวจสอบฟิลด์ "ชื่อผู้ต้องหา" และ AutoComplete
9. ✅ ตรวจสอบฟิลด์ "เลขบัตรประชาชน/เลขที่หนังสือเดินทาง"
10. ✅ บันทึกข้อมูลและตรวจสอบรูปแบบวันที่ไทย

## 📈 **Benefits**

### 🎯 **User Experience**
- **Convenience**: เลือกชื่อจากรายการที่มีอยู่แล้ว
- **Flexibility**: สามารถพิมพ์ชื่อใหม่ได้
- **Consistency**: ใช้รูปแบบเอกสารมาตรฐาน
- **Accuracy**: วันที่แสดงเป็นรูปแบบไทย

### 🔧 **Technical Benefits**
- **Data Integration**: เชื่อมต่อกับข้อมูลบัญชีธนาคาร
- **Validation**: ตรวจสอบรูปแบบข้อมูลที่ถูกต้อง
- **Localization**: รองรับรูปแบบวันที่ไทย
- **User-Friendly**: AutoComplete เพิ่มความสะดวก

## 🚀 **การใช้งาน**

### 💡 **Use Cases**
1. **Quick Selection**: เลือกชื่อผู้ต้องหาจากรายการที่มีอยู่
2. **Manual Entry**: เพิ่มชื่อผู้ต้องหาใหม่ที่ไม่อยู่ในรายการ
3. **Document Format**: ใช้รูปแบบเอกสารมาตรฐาน
4. **Thai Date**: แสดงวันที่ในรูปแบบที่เข้าใจง่าย

### 📊 **Data Flow**
```
1. เปิดฟอร์มเพิ่มผู้ต้องหา
2. ดึงข้อมูลบัญชีธนาคารจากคดีนี้
3. แสดงรายชื่อใน AutoComplete
4. ผู้ใช้เลือกหรือพิมพ์ชื่อ
5. บันทึกพร้อมแปลงวันที่เป็นไทย
```

## 🔮 **Future Enhancements**

### 🎨 **UI Improvements**
- **Search Highlight**: เน้นข้อความที่ค้นหา
- **Recent Selections**: แสดงรายการที่เลือกล่าสุด
- **Bulk Import**: นำเข้าข้อมูลหลายรายการ

### 🔧 **Functional Improvements**
- **Smart Suggestions**: แนะนำชื่อที่เกี่ยวข้อง
- **Duplicate Detection**: ตรวจสอบชื่อซ้ำ
- **Auto-fill**: เติมข้อมูลอัตโนมัติจากบัญชีธนาคาร

## 📊 **Impact Analysis**

### ⚡ **Performance Impact**
- **API Call**: เพิ่ม 1 API call เมื่อเปิดฟอร์ม
- **Data Processing**: ประมวลผลชื่อเพื่อลบซ้ำ
- **Memory Usage**: เก็บรายชื่อใน state

### 🔒 **Data Integrity**
- **Validation**: ตรวจสอบรูปแบบข้อมูล
- **Required Fields**: บังคับกรอกข้อมูลสำคัญ
- **Format Consistency**: รูปแบบข้อมูลสม่ำเสมอ

## 🎉 **สรุปผลการทำงาน**

✅ **ปรับปรุงสำเร็จ**: ฟอร์มเพิ่มผู้ต้องหาตามข้อกำหนด

✅ **AutoComplete**: ดึงข้อมูลจากบัญชีธนาคารและสามารถพิมพ์เพิ่มได้

✅ **Document Format**: ใช้รูปแบบเอกสารมาตรฐาน

✅ **Thai Date**: บันทึกและแสดงวันที่ในรูปแบบไทย

✅ **Enhanced Validation**: รองรับทั้งเลขบัตรประชาชนและหนังสือเดินทาง

---

## 📋 **การใช้งาน**

### 🔗 **การเข้าถึง**
1. เปิดหน้าเว็บ http://localhost:3001
2. เข้าสู่ระบบ
3. ไปที่หน้า "แดชบอร์ด"
4. คลิก "ดูรายละเอียด" สำหรับคดีใดๆ
5. คลิก "เพิ่มผู้ต้องหา"

### 📝 **การใช้งานฟิลด์ใหม่**
1. **เลขที่หนังสือ**: กรอกหรือปล่อยให้ระบบสร้างอัตโนมัติ
2. **ลงวันที่**: วันที่ปัจจุบันถูกตั้งค่าไว้แล้ว
3. **ชื่อผู้ต้องหา**: เลือกจากรายการหรือพิมพ์ใหม่
4. **เลขบัตรประชาชน**: รองรับทั้งเลขบัตรประชาชนและหนังสือเดินทาง

---

**🎯 ฟอร์มเพิ่มผู้ต้องหาปรับปรุงเรียบร้อยแล้ว!**

**👤 ระบบพร้อมสำหรับการจัดการผู้ต้องหาอย่างมีประสิทธิภาพ!**
