# 📦 Export/Import Docker Containers Guide

**สำหรับ:** Criminal Case Management System  
**Version:** 3.3.2  
**Date:** October 11, 2025

---

## 🎯 ภาพรวม

คู่มือนี้จะแนะนำวิธี Export และ Import Docker Containers เพื่อให้คนอื่นนำไปพัฒนาต่อได้

---

## 📦 วิธีที่ 1: Export Docker Images (แนะนำ)

### ✅ ข้อดี:
- ใช้งานง่าย
- ขนาดเล็กกว่า
- Import ได้เร็ว
- เหมาะสำหรับการแชร์

### ขั้นตอน Export:

#### 1. Export Docker Images
```bash
# Export 3 images หลัก
docker save -o criminal-case-images.tar \
  web-app-frontend:latest \
  web-app-backend:latest \
  postgres:15-alpine

# ตรวจสอบขนาดไฟล์
dir criminal-case-images.tar
```

**ขนาดไฟล์:** ~518 MB (494 MB)

#### 2. Backup Database
```bash
# Backup PostgreSQL database
docker exec criminal-case-db pg_dump -U user criminal_case_db > database_backup.sql

# หรือ backup แบบ custom format (เล็กกว่า)
docker exec criminal-case-db pg_dump -U user -Fc criminal_case_db > database_backup.dump
```

#### 3. Backup Uploaded Files
```bash
# Backup CFR uploads และไฟล์อื่นๆ
docker cp criminal-case-backend:/app/uploads ./uploads_backup
```

#### 4. Package ทั้งหมด
```bash
# สร้างโฟลเดอร์สำหรับ export
mkdir criminal-case-export
cd criminal-case-export

# คัดลอกไฟล์ทั้งหมด
copy ..\criminal-case-images.tar .
copy ..\database_backup.sql .
copy ..\uploads_backup uploads -Recurse

# สร้าง README
# (ดูด้านล่าง)
```

---

## 📥 วิธี Import (สำหรับผู้รับ)

### ขั้นตอน Import:

#### 1. Load Docker Images
```bash
# Import images
docker load -i criminal-case-images.tar

# ตรวจสอบ
docker images | findstr "web-app"
```

#### 2. Clone Project
```bash
# Clone project จาก GitHub
git clone https://github.com/nuicpe32/SaveToExcel.git
cd SaveToExcel/web-app
```

#### 3. Setup Docker Compose
```bash
# Start containers
docker-compose up -d

# รอให้ containers พร้อม
timeout /t 10
```

#### 4. Restore Database
```bash
# Restore database
docker cp database_backup.sql criminal-case-db:/tmp/
docker exec criminal-case-db psql -U user -d criminal_case_db -f /tmp/database_backup.sql

# หรือถ้าใช้ dump format
docker cp database_backup.dump criminal-case-db:/tmp/
docker exec criminal-case-db pg_restore -U user -d criminal_case_db /tmp/database_backup.dump
```

#### 5. Restore Uploaded Files
```bash
# Restore uploads
docker cp uploads criminal-case-backend:/app/uploads
```

#### 6. Verify
```bash
# ตรวจสอบว่าระบบทำงาน
docker ps
docker logs criminal-case-backend --tail 20
docker logs criminal-case-frontend --tail 20

# เข้าใช้งาน
# http://localhost:3001
```

---

## 🗂️ วิธีที่ 2: Export Containers พร้อม Data (ขนาดใหญ่)

### ⚠️ ข้อเสีย:
- ขนาดใหญ่มาก (~2-3 GB)
- Export/Import ช้า
- ไม่แนะนำถ้าไม่จำเป็น

### ขั้นตอน Export:

```bash
# Export แต่ละ container (รวมข้อมูล)
docker export criminal-case-frontend > frontend.tar
docker export criminal-case-backend > backend.tar
docker export criminal-case-db > database.tar
```

---

## 🎁 Package สำหรับแชร์

### โครงสร้างโฟลเดอร์ที่แนะนำ:

```
criminal-case-export/
├── criminal-case-images.tar     # Docker images (518 MB)
├── database_backup.sql          # Database backup
├── uploads/                     # Uploaded files (CFR, etc.)
│   └── cfr/
├── docker-compose.yml           # จาก GitHub
├── .env.example                 # ตัวอย่าง environment
└── README.md                    # คำแนะนำการติดตั้ง
```

---

## 📝 ไฟล์ README.md สำหรับผู้รับ

ให้ผมสร้างไฟล์ README.md สำหรับผู้รับครับ:

---

ให้ผมช่วย Export ให้เลยไหมครับ? หรือต้องการให้แนะนำเพิ่มเติม?

**ตัวเลือก:**

### A. Export ทุกอย่างให้เลย (แนะนำ)
- Export Docker Images
- Backup Database
- Backup Uploads
- สร้าง Package พร้อมคำแนะนำ

### B. Export เฉพาะ Docker Images
- Export แค่ images ให้
- คนรับ clone GitHub เอง

### C. แนะนำวิธีเท่านั้น
- ให้คำแนะนำเป็นขั้นตอน
- ทำเองตามคู่มือ

**เลือกตัวเลือกไหนดีครับ?** 🤔
