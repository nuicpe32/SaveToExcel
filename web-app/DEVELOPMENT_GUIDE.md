# Development Guide - Criminal Case Management System

## 🎯 หลักการสำคัญ

### 1. URL หลักสำหรับการเข้าถึง
- **Frontend**: **http://localhost:3001/** ⭐ (หลัก)
- Backend API: http://localhost:8000/
- Database Admin: http://localhost:8080/

### 2. Docker Compose Configuration
- **ใช้ไฟล์เดียว**: `docker-compose.yml`
- **ไม่มี dev/production แยก** เพื่อป้องกันความสับสน
- **Port Mapping**: 3001:3000 (Frontend), 8000:8000 (Backend)

## 🚀 การเริ่มต้น Development

### 1. เริ่มต้นระบบ
```bash
cd web-app
docker-compose up -d
```

### 2. ตรวจสอบสถานะ
```bash
docker ps
```

ควรเห็น containers:
- `criminal-case-frontend` (port 3001)
- `criminal-case-backend` (port 8000)
- `criminal-case-db` (port 5432)
- `criminal-case-redis` (port 6379)

### 3. เข้าถึงระบบ
เปิดเบราว์เซอร์ไปที่: **http://localhost:3001/**

## 🛠️ การพัฒนา

### Frontend Development
- **Location**: `web-app/frontend/src/`
- **Hot Reload**: เปิดใช้งานแล้ว
- **Main Files**:
  - `src/pages/DashboardPage.tsx` - หน้าหลัก
  - `src/pages/CriminalCaseDetailPage.tsx` - รายละเอียดคดี
  - `src/components/` - Components ต่างๆ

### Backend Development
- **Location**: `web-app/backend/`
- **Hot Reload**: เปิดใช้งานแล้ว
- **Main Files**:
  - `app/main.py` - FastAPI app
  - `app/api/v1/` - API endpoints
  - `app/services/` - Business logic

### Database
- **Type**: PostgreSQL
- **Connection**: localhost:5432
- **Database**: criminal_case_db
- **Username**: user
- **Password**: password

## 📋 ฟีเจอร์สำคัญ

### 1. Dashboard
- สถิติคดี (Total, Processing, Over 6 Months, Closed)
- ตารางแสดงคดีทั้งหมด
- ฟิลเตอร์ทุกคอลัมน์

### 2. Criminal Case Management
- เพิ่ม/แก้ไข/ลบคดี
- จัดการบัญชีธนาคาร
- จัดการผู้ต้องหา

### 3. Document Generation
- หมายเรียกธนาคาร
- ซองหมายเรียกธนาคาร
- หมายเรียกผู้ต้องหา
- ซองหมายเรียกผู้ต้องหา

### 4. PDF Parser
- แกะข้อมูลจากไฟล์ PDF (ทร.14)
- Auto-fill ฟอร์มผู้ต้องหา
- Address validation

### 5. Police Station Search
- ค้นหาสถานีตำรวจตามที่อยู่
- Auto-fill ข้อมูลสถานีตำรวจ

## 🔧 การแก้ไขปัญหา

### 1. Frontend เข้าไม่ได้
```bash
# ตรวจสอบ logs
docker logs criminal-case-frontend

# Restart frontend
docker restart criminal-case-frontend

# ตรวจสอบ port
netstat -an | findstr :3001
```

### 2. Backend เข้าไม่ได้
```bash
# ตรวจสอบ logs
docker logs criminal-case-backend

# Restart backend
docker restart criminal-case-backend
```

### 3. ข้อมูลหาย
```bash
# ตรวจสอบ database
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM criminal_cases;"

# Restore จาก backup (ถ้ามี)
docker exec criminal-case-db psql -U user -d criminal_case_db < backup.sql
```

### 4. Container ไม่ start
```bash
# Clean up
docker-compose down
docker system prune -f

# Rebuild
docker-compose up -d --build
```

## 📊 การตรวจสอบข้อมูล

### 1. ตรวจสอบข้อมูลใน Database
```bash
# เข้า database
docker exec -it criminal-case-db psql -U user -d criminal_case_db

# ตรวจสอบตาราง
\dt

# ตรวจสอบข้อมูล
SELECT COUNT(*) FROM criminal_cases;
SELECT COUNT(*) FROM bank_accounts;
SELECT COUNT(*) FROM suspects;
```

### 2. ตรวจสอบ API
```bash
# ตรวจสอบ API endpoints
curl http://localhost:8000/api/v1/criminal-cases/

# ตรวจสอบ health
curl http://localhost:8000/health
```

## 🚨 ข้อควรระวัง

### 1. URL หลัก
- **ใช้ http://localhost:3001/ เสมอ**
- ไม่ใช้ http://localhost:3000/ (port ใน container)

### 2. Docker Compose
- **ใช้ไฟล์เดียว**: `docker-compose.yml`
- **ไม่สร้างไฟล์ dev/production แยก**
- **ไม่ใช้ docker-compose.dev.yml**

### 3. Data Persistence
- ข้อมูลจะไม่หายเมื่อ restart containers
- ใช้ volumes สำหรับ data persistence
- Backup ข้อมูลเป็นระยะ

### 4. Port Conflicts
- ตรวจสอบว่า ports ไม่ถูกใช้งาน
- 3001 (Frontend), 8000 (Backend), 5432 (DB), 6379 (Redis)

## 📝 การอัพเดต Code

### 1. Frontend Changes
```bash
# แก้ไขไฟล์ใน web-app/frontend/src/
# Hot reload จะทำงานอัตโนมัติ
```

### 2. Backend Changes
```bash
# แก้ไขไฟล์ใน web-app/backend/
# Hot reload จะทำงานอัตโนมัติ
```

### 3. Database Changes
```bash
# สร้าง migration
docker exec criminal-case-backend alembic revision --autogenerate -m "description"

# รัน migration
docker exec criminal-case-backend alembic upgrade head
```

## 🔄 การ Deploy

### 1. Production Build
```bash
# Build production images
docker-compose -f docker-compose.prod.yml build

# Deploy
docker-compose -f docker-compose.prod.yml up -d
```

### 2. Backup Data
```bash
# Backup database
docker exec criminal-case-db pg_dump -U user criminal_case_db > backup.sql

# Backup files
docker cp criminal-case-backend:/app/uploads ./backup-uploads
```

---

**⚠️ สำคัญ**: 
- ใช้ **http://localhost:3001/** เป็น URL หลัก
- ใช้ `docker-compose.yml` ไฟล์เดียว
- ตรวจสอบข้อมูลก่อนและหลังการเปลี่ยนแปลง
