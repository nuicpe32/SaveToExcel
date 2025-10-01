# 🔧 Development Workflow Guide

## 📋 สถานะปัจจุบัน

**✅ ระบบทำงานปกติ:**
- Frontend: http://localhost:3001
- Backend: http://localhost:8000
- Database: PostgreSQL (ข้อมูลครบถ้วน)
- Volume: `web-app_postgres_data` (มีข้อมูล 418 บัญชีธนาคาร, 13 ธนาคาร, 48 คดี)

---

## 🚀 การเริ่มต้น Development

### เริ่มระบบ
```bash
cd web-app
docker-compose -f docker-compose.dev.yml up -d
```

### ตรวจสอบสถานะ
```bash
docker ps --filter "name=criminal-case"
```

---

## 🔄 Development Workflow

### 1. การแก้ไขโค้ด (ไม่ต้อง Build)

**Backend (Python/FastAPI):**
- แก้ไขไฟล์ใน `backend/app/`
- เซฟไฟล์ → ระบบอัพเดททันที (Hot Reload)
- ดู logs: `docker logs criminal-case-backend-dev -f`

**Frontend (React/TypeScript):**
- แก้ไขไฟล์ใน `frontend/src/`
- เซฟไฟล์ → ระบบอัพเดททันที (Hot Reload)
- ดู logs: `docker logs criminal-case-frontend-dev -f`

### 2. การแก้ไข Dependencies (ต้อง Build)

**Backend:**
```bash
# แก้ไข requirements.txt
docker-compose -f docker-compose.dev.yml build backend
docker-compose -f docker-compose.dev.yml up -d backend
```

**Frontend:**
```bash
# แก้ไข package.json
docker-compose -f docker-compose.dev.yml build frontend
docker-compose -f docker-compose.dev.yml up -d frontend
```

### 3. การรีสตาร์ท

**รีสตาร์ทเฉพาะ service:**
```bash
docker-compose -f docker-compose.dev.yml restart backend
docker-compose -f docker-compose.dev.yml restart frontend
```

**รีสตาร์ททั้งหมด:**
```bash
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

---

## 🗂️ Volume Management

### สถานะปัจจุบัน
- **Volume เดียว**: `web-app_postgres_data`
- **ข้อมูล**: 418 บัญชีธนาคาร, 13 ธนาคาร, 48 คดี
- **ใช้ร่วมกัน**: Production และ Development

### การจัดการ Volume

**ดูข้อมูล Volume:**
```bash
docker volume ls
docker volume inspect web-app_postgres_data
```

**Backup ข้อมูล:**
```bash
docker exec criminal-case-db-dev pg_dump -U user -d criminal_case_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

**Restore ข้อมูล:**
```bash
docker exec -i criminal-case-db-dev psql -U user -d criminal_case_db < backup_file.sql
```

---

## 🧪 การทดสอบ

### ทดสอบ API
```bash
# ทดสอบ Bank Summons
curl http://localhost:8000/api/v1/documents/bank-summons/2110

# ทดสอบ Bank Envelope  
curl http://localhost:8000/api/v1/documents/bank-envelope/2110
```

### ทดสอบ Frontend
- เปิด http://localhost:3001
- Login: admin / admin123
- ทดสอบฟีเจอร์ต่างๆ

---

## 🔍 การ Debug

### ดู Logs
```bash
# Backend logs
docker logs criminal-case-backend-dev -f

# Frontend logs
docker logs criminal-case-frontend-dev -f

# Database logs
docker logs criminal-case-db-dev -f
```

### เข้า Container
```bash
# เข้า Backend container
docker exec -it criminal-case-backend-dev bash

# เข้า Database container
docker exec -it criminal-case-db-dev psql -U user -d criminal_case_db
```

---

## 📊 ฟีเจอร์สำคัญ

### ✅ ฟีเจอร์ที่ทำงานได้
- สร้าง/แก้ไข/ลบคดีอาญา
- จัดการบัญชีธนาคาร
- จัดการผู้ต้องหา
- สร้างหมายเรียกธนาคาร (HTML)
- สร้างซองหมายเรียกธนาคาร (HTML)
- Authentication & Authorization

### 🔧 API Endpoints
- `GET /api/v1/criminal-cases/` - รายการคดี
- `GET /api/v1/bank-accounts/` - รายการบัญชีธนาคาร
- `GET /api/v1/documents/bank-summons/{id}` - หมายเรียกธนาคาร
- `GET /api/v1/documents/bank-envelope/{id}` - ซองหมายเรียกธนาคาร

---

## ⚠️ ข้อควรระวัง

1. **ไม่สร้าง Volume ใหม่**: ใช้ `web-app_postgres_data` เดิม
2. **Backup ข้อมูล**: ก่อนทำการเปลี่ยนแปลงใหญ่
3. **Hot Reload**: ใช้ได้กับโค้ด แต่ไม่ใช่ dependencies
4. **Port Conflicts**: ตรวจสอบว่า port 3001, 8000, 5432 ไม่ถูกใช้

---

## 🆘 การแก้ไขปัญหา

### ระบบไม่ทำงาน
```bash
# ตรวจสอบสถานะ
docker ps
docker-compose -f docker-compose.dev.yml ps

# รีสตาร์ท
docker-compose -f docker-compose.dev.yml down
docker-compose -f docker-compose.dev.yml up -d
```

### ข้อมูลหาย
```bash
# ตรวจสอบข้อมูล
docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM bank_accounts;"

# Restore จาก backup
docker exec -i criminal-case-db-dev psql -U user -d criminal_case_db < backup_file.sql
```

### API ไม่ทำงาน
```bash
# ตรวจสอบ logs
docker logs criminal-case-backend-dev --tail 50

# รีสตาร์ท backend
docker-compose -f docker-compose.dev.yml restart backend
```

---

## 📞 การติดต่อ

หากมีปัญหา:
1. ตรวจสอบ logs ก่อน
2. ดูคู่มือนี้
3. ตรวจสอบ volume และข้อมูล
4. รีสตาร์ทระบบถ้าจำเป็น

**Happy Coding! 🚀**
