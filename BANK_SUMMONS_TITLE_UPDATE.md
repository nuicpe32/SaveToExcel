# 📄 Bank Summons Title Update - อัปเดต Title หมายเรียกเอกสารธนาคาร

## 📋 ข้อกำหนดการแก้ไข

ผู้ใช้ต้องการเปลี่ยน Title ของหมายเรียกเอกสารธนาคารจาก:
- **เดิม**: "หนังสือขอข้อมูลบัญชีม้า (สอท.4)"
- **ใหม่**: "หมายเรียกพยานเอกสาร<เลขที่หนังสือ> ลงวันที่ <ลงวันที่>"

## 🔍 การวิเคราะห์ปัญหา

### 📁 **ไฟล์ที่เกี่ยวข้อง**
- `web-app/backend/app/services/bank_summons_generator.py` - ไฟล์ที่สร้าง HTML สำหรับหมายเรียกธนาคาร
- `web-app/backend/app/api/v1/documents.py` - API endpoint สำหรับสร้างเอกสาร

### 🎯 **จุดที่ต้องแก้ไข**
- บรรทัดที่ 80 ใน `bank_summons_generator.py` มี title ที่เป็น static text
- ต้องเปลี่ยนให้เป็น dynamic title ที่รวมเลขที่หนังสือและวันที่

## ✨ การแก้ไขที่ทำ

### 🔧 **แก้ไขในไฟล์ `bank_summons_generator.py`**

#### **ก่อนแก้ไข:**
```python
# สร้าง HTML
html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>หนังสือขอข้อมูลบัญชีม้า (สอท.4)</title>
```

#### **หลังแก้ไข:**
```python
# สร้าง title ตามที่ต้องการ
html_title = f"หมายเรียกพยานเอกสาร{document_no} ลงวันที่ {date_thai}"

# สร้าง HTML
html_content = f"""<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html_title}</title>
```

### 📊 **ข้อมูลที่ใช้ใน Title**
- **`document_no`**: เลขที่หนังสือ (จาก `bank_data.get('document_number')`)
- **`date_thai`**: วันที่ (จาก `bank_data.get('document_date_thai')` หรือ format จาก `document_date`)

## 🎯 **ผลลัพธ์ที่ได้**

### ✅ **Title Format ใหม่**
```
หมายเรียกพยานเอกสาร{เลขที่หนังสือ} ลงวันที่ {วันที่}
```

### 📝 **ตัวอย่าง Title**
```
หมายเรียกพยานเอกสาร12345 ลงวันที่ 15 ตุลาคม 2568
หมายเรียกพยานเอกสาร67890 ลงวันที่ 20 พฤศจิกายน 2568
```

### 🎨 **การทำงานของระบบ**
1. **ดึงข้อมูล**: ระบบดึง `document_number` และ `document_date_thai` จากฐานข้อมูล
2. **สร้าง Title**: รวมข้อมูลเป็น title ตามรูปแบบที่กำหนด
3. **แสดงผล**: Title ปรากฏใน browser tab และ PDF

## 🔧 **Technical Implementation**

### 📁 **ไฟล์ที่แก้ไข**
- `web-app/backend/app/services/bank_summons_generator.py`

### 🛠️ **การเปลี่ยนแปลง**
```python
# เพิ่มบรรทัดนี้ก่อนสร้าง HTML
html_title = f"หมายเรียกพยานเอกสาร{document_no} ลงวันที่ {date_thai}"

# เปลี่ยน title tag จาก static เป็น dynamic
<title>{html_title}</title>
```

### 🔄 **การ Restart Container**
```bash
docker restart criminal-case-backend-dev
```

## 🧪 **การทดสอบ**

### ✅ **Test Cases**
1. **Title Display**: ตรวจสอบ title ใน browser tab
2. **PDF Title**: ตรวจสอบ title เมื่อพิมพ์เป็น PDF
3. **Data Integration**: ตรวจสอบการรวมข้อมูลเลขที่หนังสือและวันที่
4. **Multiple Documents**: ทดสอบกับเอกสารหลายฉบับ

### 🔍 **Testing Steps**
1. ✅ เปิดหน้าเว็บ http://localhost:3001
2. ✅ เข้าสู่ระบบ
3. ✅ ไปที่หน้า "บัญชีธนาคาร"
4. ✅ คลิก "สร้างหมายเรียก" สำหรับบัญชีธนาคาร
5. ✅ ตรวจสอบ title ใน browser tab
6. ✅ ตรวจสอบ title เมื่อพิมพ์เป็น PDF

## 📈 **Benefits**

### 🎯 **User Experience**
- **Clear Identification**: ชื่อเอกสารชัดเจนขึ้น
- **Easy Reference**: อ้างอิงเลขที่หนังสือได้ง่าย
- **Date Tracking**: ระบุวันที่ได้ชัดเจน

### 🔧 **Technical Benefits**
- **Dynamic Content**: Title เปลี่ยนตามข้อมูลจริง
- **Consistent Format**: รูปแบบสม่ำเสมอ
- **Maintainable**: ง่ายต่อการบำรุงรักษา

## 📊 **Impact Analysis**

### ⚡ **Performance Impact**
- **Minimal**: เพิ่มเพียง 1 บรรทัด code
- **No Database Changes**: ไม่ต้องแก้ไขฐานข้อมูล
- **No API Changes**: ไม่ต้องแก้ไข API endpoints

### 🔒 **Security Impact**
- **No Security Issues**: ไม่มีผลกระทบด้านความปลอดภัย
- **Data Privacy**: ใช้ข้อมูลที่มีอยู่แล้ว

## 🚀 **Future Enhancements**

### 🔮 **Possible Improvements**
- **Custom Title Formats**: ให้ผู้ใช้เลือกรูปแบบ title
- **Multi-language Support**: รองรับหลายภาษา
- **Title Templates**: ใช้ template สำหรับ title

### 🎨 **UI Improvements**
- **Title Preview**: แสดงตัวอย่าง title ก่อนสร้าง
- **Title Validation**: ตรวจสอบความถูกต้องของ title

## 🎉 **สรุปผลการแก้ไข**

✅ **แก้ไขสำเร็จ**: Title ของหมายเรียกเอกสารธนาคารเปลี่ยนเป็น "หมายเรียกพยานเอกสาร<เลขที่หนังสือ> ลงวันที่ <ลงวันที่>"

✅ **Dynamic Title**: Title เปลี่ยนตามข้อมูลจริงของแต่ละเอกสาร

✅ **User Friendly**: ชื่อเอกสารชัดเจนและอ้างอิงได้ง่าย

✅ **Production Ready**: ผ่านการทดสอบและพร้อมใช้งาน

---

## 📋 **การใช้งาน**

### 🔗 **API Endpoint**
```
GET /api/v1/documents/bank-summons/{bank_account_id}
```

### 📄 **HTML Response**
```html
<!DOCTYPE html>
<html lang="th">
<head>
    <title>หมายเรียกพยานเอกสาร12345 ลงวันที่ 15 ตุลาคม 2568</title>
    ...
</head>
```

### 🖨️ **PDF Generation**
เมื่อพิมพ์เป็น PDF, title จะปรากฏใน:
- **PDF Properties**: Title field
- **Browser Tab**: Tab title
- **Print Preview**: Document title

---

**🎯 Title ของหมายเรียกเอกสารธนาคารอัปเดตเรียบร้อยแล้ว!**

**📄 ระบบพร้อมสร้างเอกสารที่มี title ที่ชัดเจนและอ้างอิงได้ง่าย!**
