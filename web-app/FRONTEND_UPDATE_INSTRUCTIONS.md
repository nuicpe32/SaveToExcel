# 📝 คำแนะนำการอัปเดต Frontend หลังแก้ไข

**วันที่:** 1 ตุลาคม 2568

---

## ✅ การเปลี่ยนแปลง

### ลบฟิลด์ออกจากฟอร์มเพิ่มบัญชีธนาคาร:
- ❌ **สาขา (bank_branch)** → ลบแล้ว
- ❌ **ที่อยู่ธนาคารทั้งหมด** → ลบแล้ว

### ฟิลด์ที่เหลือ:
- ✅ ชื่อธนาคาร (dropdown)
- ✅ เลขที่บัญชี
- ✅ ชื่อบัญชี
- ✅ ช่วงเวลาที่ทำธุรกรรม
- ✅ ข้อมูลการส่ง/รับเอกสาร

---

## 🔄 วิธีอัปเดต Frontend

### **วิธีที่ 1: Rebuild Frontend Container (แนะนำ)**

```powershell
cd C:\SaveToExcel\web-app

# Rebuild frontend
docker-compose build frontend

# Restart
docker-compose restart frontend
```

### **วิธีที่ 2: รัน Frontend ใน Dev Mode (สำหรับ Development)**

```powershell
# หยุด frontend container
docker-compose stop frontend

# รัน dev mode ใน terminal ใหม่
cd frontend
npm run dev

# จะรันที่ http://localhost:5173
```

### **วิธีที่ 3: Clear Browser Cache**

ถ้า rebuild แล้วยังไม่เห็นการเปลี่ยนแปลง:

1. เปิด Chrome DevTools (F12)
2. คลิกขวาที่ปุ่ม Refresh
3. เลือก **"Empty Cache and Hard Reload"**

หรือ:
- กด **Ctrl + Shift + Delete**
- เลือก "Cached images and files"
- คลิก "Clear data"

---

## 🧪 ทดสอบการเปลี่ยนแปลง

### 1. เข้าระบบ
```
http://localhost:3001/login
```

### 2. ไปที่หน้าคดีอาญา
```
http://localhost:3001/
```

### 3. เปิดคดีใดคดีหนึ่ง
- คลิก "ดูรายละเอียด"
- ไปที่แท็บ "บัญชีธนาคาร"
- คลิก "เพิ่มบัญชีธนาคาร"

### 4. ตรวจสอบฟอร์ม

**ควรเห็น:**
- ✅ ชื่อธนาคาร (dropdown เต็มความกว้าง)
- ✅ เลขที่บัญชี
- ✅ ชื่อบัญชี
- ✅ ข้อความ: "📍 หมายเหตุ: ที่อยู่จะดึงจากข้อมูลสำนักงานใหญ่ของธนาคารโดยอัตโนมัติ"

**ไม่ควรเห็น:**
- ❌ ฟิลด์สาขา
- ❌ ฟิลด์ที่อยู่ทั้งหมด

---

## 🎯 Expected Result

### ฟอร์มเดิม (Before):
```
[ชื่อธนาคาร]  [สาขา] ❌
[เลขที่บัญชี] [ชื่อบัญชี]

=== ที่อยู่ธนาคาร === ❌
[ที่อยู่]
[ซอย] [หมู่] [ถนน] [รหัสไปรษณีย์]
[ตำบล] [อำเภอ] [จังหวัด]
```

### ฟอร์มใหม่ (After):
```
[ชื่อธนาคาร (full width)] ✅
[เลขที่บัญชี] [ชื่อบัญชี] ✅

📍 หมายเหตุ: ที่อยู่จะดึงจากข้อมูลสำนักงานใหญ่ของธนาคารโดยอัตโนมัติ
```

---

## 📊 Current Status

- ✅ Backend: Updated และ Running
- ✅ Database: Migration สำเร็จ
- ✅ Frontend Code: Updated
- ⏳ Frontend Container: ต้อง Rebuild

---

## 🐛 Troubleshooting

### ปัญหา: ยังเห็นฟิลด์สาขาอยู่

**แก้ไข:**
```powershell
# 1. Rebuild frontend
docker-compose build frontend --no-cache

# 2. Restart
docker-compose up -d frontend

# 3. Clear browser cache (Ctrl + Shift + Delete)

# 4. Refresh page (Ctrl + F5)
```

### ปัญหา: ฟอร์มไม่แสดง

**แก้ไข:**
```powershell
# ตรวจสอบ logs
docker-compose logs frontend --tail 50

# ตรวจสอบ browser console (F12)
```

---

## 📝 Notes

- การเปลี่ยนแปลงนี้เป็นไปตามการแก้ไข Database Schema
- ข้อมูลที่อยู่จะดึงจากตาราง `banks` ผ่าน `bank_id` FK
- เอกสารจะส่งไปที่สำนักงานใหญ่เท่านั้น (ไม่ใช่สาขา)

---

**Updated:** 1 ตุลาคม 2568, 13:32:18 +07:00

