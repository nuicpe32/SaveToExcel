# Criminal Case Management System - Web Application

ระบบจัดการคดีอาญาออนไลน์ เวอร์ชัน 3.1.1

## 📋 สารบัญ

- [ภาพรวมระบบ](#ภาพรวมระบบ)
- [เทคโนโลยีที่ใช้](#เทคโนโลยีที่ใช้)
- [การติดตั้งและใช้งาน](#การติดตั้งและใช้งาน)
- [โครงสร้างโปรเจค](#โครงสร้างโปรเจค)
- [คู่มือการใช้งาน Docker](#คู่มือการใช้งาน-docker)
- [การพัฒนาต่อยอด](#การพัฒนาต่อยอด)
- [ปัญหาที่พบบ่อย](#ปัญหาที่พบบ่อย)

---

## ภาพรวมระบบ

ระบบจัดการคดีอาญาทางเทคโนโลยี สำหรับ กก.1 บก.สอท.4 ประกอบด้วย:

### ฟีเจอร์หลัก
- **จัดการคดีอาญา**: บันทึก แก้ไข ค้นหาคดี
- **จัดการผู้ต้องหา**: บันทึกข้อมูลผู้ต้องหา พิมพ์หมายเรียกผู้ต้องหา และซองหมายเรียก
- **จัดการบัญชีธนาคาร**: บันทึกบัญชีที่เกี่ยวข้อง พิมพ์หนังสือขอข้อมูลธนาคาร
- **ออกเอกสาร**:
  - หมายเรียกผู้ต้องหา (HTML)
  - ซองหมายเรียกผู้ต้องหา (HTML)
  - หนังสือขอข้อมูลธนาคาร (HTML)
- **ค้นหาข้อมูล**: ค้นหาตามหมายเลขคดี ชื่อผู้ต้องหา ชื่อผู้เสียหาย
- **Parse PDF**: แกะข้อมูลจากไฟล์ ทร.14 อัตโนมัติ
- **ค้นหาสถานีตำรวจ**: ค้นหาสถานีตำรวจตามที่อยู่

**ข้อมูลในระบบ (ณ 3 ต.ค. 2568):**
- 48 คดีอาญา
- 15 ผู้ต้องหา
- 418 บัญชีธนาคาร

---

## เทคโนโลยีที่ใช้

### Backend
- **FastAPI** - Python Web Framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Redis** - Cache & Session
- **Uvicorn** - ASGI Server
- **PyPDF2** - PDF Parser

### Frontend
- **React 18** - UI Framework
- **TypeScript** - Type Safety
- **Vite** - Build Tool
- **Ant Design 5** - UI Components
- **Axios** - HTTP Client
- **React Router** - Navigation

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Orchestration

---

## การติดตั้งและใช้งาน

### ✅ วิธีที่แนะนำ: ใช้ Docker Compose

#### 1. ติดตั้ง Docker
- Windows: [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- Linux: `sudo apt install docker.io docker-compose`

#### 2. เริ่มต้นใช้งาน

```bash
# เข้าโฟลเดอร์โปรเจค
cd /mnt/c/SaveToExcel/web-app

# เริ่มระบบ
docker-compose up -d

# รอประมาณ 30-60 วินาที เพื่อให้ทุก service พร้อม
```

#### 3. เข้าใช้งาน

- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

**ข้อมูลเข้าสู่ระบบ:**
- Username: `admin`
- Password: `admin123`

#### 4. หยุดระบบ

```bash
# หยุดระบบ (เก็บข้อมูล)
docker-compose down

# หยุดและลบข้อมูลทั้งหมด (ระวัง!)
docker-compose down -v
```

---

## โครงสร้างโปรเจค

```
web-app/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/            # API Endpoints
│   │   │   ├── auth.py        # Authentication
│   │   │   ├── criminal_cases.py
│   │   │   ├── suspects_improved.py
│   │   │   ├── bank_accounts_improved.py
│   │   │   ├── documents.py   # Document generation
│   │   │   ├── pdf_parser.py  # PDF parsing
│   │   │   └── police_stations.py
│   │   ├── models/            # Database Models (SQLAlchemy)
│   │   │   ├── criminal_case.py
│   │   │   ├── suspect.py
│   │   │   ├── bank_account.py
│   │   │   └── user.py
│   │   ├── schemas/           # Pydantic Schemas
│   │   ├── services/          # Business Logic
│   │   │   ├── bank_summons_generator.py
│   │   │   ├── suspect_summons_generator.py
│   │   │   ├── pdf_parser.py
│   │   │   └── police_station_service.py
│   │   ├── utils/             # Utilities
│   │   │   ├── date_utils.py
│   │   │   ├── thai_date_utils.py
│   │   │   └── string_utils.py
│   │   └── main.py            # FastAPI App Entry Point
│   ├── migrations/            # SQL Migration Scripts
│   ├── requirements.txt       # Python Dependencies
│   └── Dockerfile            # Backend Docker Image
│
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable Components
│   │   │   ├── BankAccountForm.tsx
│   │   │   ├── SuspectForm.tsx
│   │   │   ├── PoliceStationSearchModal.tsx
│   │   │   └── ...
│   │   ├── pages/            # Page Components
│   │   │   ├── DashboardPage.tsx          # หน้าแรก (ตาราง)
│   │   │   ├── CriminalCaseDetailPage.tsx # รายละเอียดคดี
│   │   │   ├── AddCriminalCasePage.tsx    # เพิ่มคดีใหม่
│   │   │   ├── EditCriminalCasePage.tsx   # แก้ไขคดี
│   │   │   └── LoginPage.tsx              # เข้าสู่ระบบ
│   │   ├── contexts/         # React Contexts
│   │   │   └── ThemeContext.tsx           # Dark/Light Mode
│   │   ├── api.ts            # Axios Instance & API Config
│   │   ├── App.tsx           # Main App Component
│   │   └── main.tsx          # Entry Point
│   ├── package.json          # NPM Dependencies
│   ├── vite.config.ts        # Vite Configuration
│   └── Dockerfile            # Frontend Docker Image
│
├── docker-compose.yml         # Docker Compose Configuration (Production)
├── README.md                  # This file
├── DEVELOPMENT_GUIDE.md       # Development Guide
├── DOCKER_USAGE.md           # Docker Commands Reference
└── BACKUP_RESTORE_GUIDE.md   # Backup/Restore Guide
```

---

## คู่มือการใช้งาน Docker

### ⚠️ สำคัญ: Container และ Volume Names

ระบบใช้ Docker Compose แบบ **Production Single Environment**

**Container Names:**
- `criminal-case-db` - PostgreSQL Database
- `criminal-case-redis` - Redis Cache
- `criminal-case-backend` - FastAPI Backend
- `criminal-case-frontend` - React Frontend (Vite Dev Server)

**Volume Names:**
- `web-app_postgres_data` - Database storage
- `web-app_backend_uploads` - Uploaded files

**Database Credentials:**
- Host: `postgres` (inside Docker) / `localhost:5432` (outside Docker)
- Database: `criminal_case_db`
- Username: `user`
- Password: `password123`

### คำสั่ง Docker ที่ใช้บ่อย

```bash
# ดูสถานะ containers
docker ps

# ดู logs
docker logs criminal-case-backend -f
docker logs criminal-case-frontend -f
docker logs criminal-case-db

# รีสตาร์ท service
docker-compose restart backend
docker-compose restart frontend
docker-compose restart postgres

# เข้า container
docker exec -it criminal-case-backend bash
docker exec -it criminal-case-frontend sh
docker exec -it criminal-case-db psql -U user -d criminal_case_db

# ดูข้อมูลในฐานข้อมูล
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM criminal_cases;"
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM suspects;"
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM bank_accounts;"

# ดู volumes
docker volume ls | grep web-app

# ดู networks
docker network ls | grep web-app
```

### การ Backup และ Restore

```bash
# Backup database
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_${TIMESTAMP}.dump
docker cp criminal-case-db:/tmp/backup_${TIMESTAMP}.dump ./backup_${TIMESTAMP}.dump

# Restore database
docker cp backup_20251003_163753.dump criminal-case-db:/tmp/restore.dump
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump

# Backup ทั้งระบบ (database + code)
tar -czf web-app-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
  --exclude='node_modules' \
  --exclude='__pycache__' \
  --exclude='.git' \
  .
```

### การ Rebuild Services

```bash
# Rebuild เฉพาะ backend (ใช้เมื่อแก้ Python code หรือ dependencies)
docker-compose up -d --build --no-cache backend

# Rebuild เฉพาะ frontend (ใช้เมื่อแก้ package.json)
docker-compose up -d --build --no-cache frontend

# Rebuild ทั้งหมด
docker-compose down
docker-compose up -d --build --no-cache

# ลบ images เก่าและ rebuild
docker-compose down
docker system prune -a -f
docker-compose up -d --build
```

---

## การพัฒนาต่อยอด

### การแก้ไข Backend Code

1. แก้ไขไฟล์ใน `backend/app/`
2. Backend จะ **Hot Reload อัตโนมัติ** (ไม่ต้องรีสตาร์ท)
3. ถ้า Hot Reload ไม่ทำงาน:
   ```bash
   docker-compose restart backend
   ```

### การแก้ไข Frontend Code

1. แก้ไขไฟล์ใน `frontend/src/`
2. **Vite จะ Hot Reload อัตโนมัติ** (ไม่ต้องรีสตาร์ท)
3. ถ้า Hot Reload ไม่ทำงาน:
   - รีเฟรชเบราว์เซอร์ (Ctrl+Shift+R หรือ Cmd+Shift+R)
   - หรือรีสตาร์ท frontend:
     ```bash
     docker-compose restart frontend
     ```

### การเพิ่ม Python Package

1. เพิ่มใน `backend/requirements.txt`:
   ```
   new-package==1.0.0
   ```
2. Rebuild backend:
   ```bash
   docker-compose up -d --build backend
   ```

### การเพิ่ม NPM Package

```bash
# วิธีที่ 1: เข้า container
docker exec -it criminal-case-frontend sh
npm install <package-name>
exit

# วิธีที่ 2: Rebuild
# แก้ไข frontend/package.json ก่อน
docker-compose up -d --build frontend
```

### Database Migration

1. สร้างไฟล์ migration ใหม่:
   ```sql
   -- backend/migrations/009_add_new_field.sql
   ALTER TABLE criminal_cases ADD COLUMN new_field VARCHAR(255);
   ```

2. รัน migration:
   ```bash
   docker cp backend/migrations/009_add_new_field.sql criminal-case-db:/tmp/
   docker exec criminal-case-db psql -U user -d criminal_case_db -f /tmp/009_add_new_field.sql
   ```

### การเพิ่มฟีเจอร์ใหม่

#### 1. เพิ่ม Backend API Endpoint

```python
# backend/app/api/v1/new_feature.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models.database import get_db

router = APIRouter()

@router.get("/new-feature")
async def get_new_feature(db: Session = Depends(get_db)):
    return {"message": "New feature"}
```

```python
# backend/app/main.py
from app.api.v1 import new_feature

app.include_router(new_feature.router, prefix="/api/v1", tags=["new-feature"])
```

#### 2. เพิ่ม Frontend Page

```typescript
// frontend/src/pages/NewFeaturePage.tsx
import React from 'react'
import { Card } from 'antd'

const NewFeaturePage: React.FC = () => {
  return (
    <Card title="New Feature">
      <p>Content here</p>
    </Card>
  )
}

export default NewFeaturePage
```

```typescript
// frontend/src/App.tsx
import NewFeaturePage from './pages/NewFeaturePage'

// ใน <Routes>
<Route path="/new-feature" element={<NewFeaturePage />} />
```

#### 3. เพิ่ม API Call

```typescript
// frontend/src/api.ts
export const getNewFeature = () => api.get('/api/v1/new-feature')
```

---

## ปัญหาที่พบบ่อย

### 1. Frontend ไม่เชื่อม Backend (ERR_CONNECTION_REFUSED)

**สาเหตุ:** `vite.config.ts` proxy ตั้งค่าไม่ถูกต้อง

**ตรวจสอบ:**
```typescript
// frontend/vite.config.ts
export default defineConfig({
  server: {
    host: '0.0.0.0',
    port: 3001,
    proxy: {
      '/api': {
        target: 'http://backend:8000',  // ✅ ต้องใช้ Docker service name
        changeOrigin: true,
      },
    },
  },
})
```

**แก้ไข:**
```bash
docker-compose restart frontend
```

### 2. ข้อมูลหายหลัง Restart

**สาเหตุ:** ลบ volume โดยไม่ได้ตั้งใจ (`docker-compose down -v`)

**วิธีป้องกัน:**
- ใช้ `docker-compose down` แทน `docker-compose down -v`
- สำรอง backup เป็นประจำ

**แก้ไข:**
```bash
# Restore จาก backup
docker cp backup_20251003_163753.dump criminal-case-db:/tmp/restore.dump
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

### 3. Port Already in Use

**Error:** `Bind for 0.0.0.0:3001 failed: port is already allocated`

**ตรวจสอบ:**
```bash
# Windows
netstat -ano | findstr :3001

# Linux/Mac
lsof -i :3001
```

**แก้ไข:**
- ปิด process ที่ใช้ port
- หรือเปลี่ยน port ใน `docker-compose.yml`:
  ```yaml
  frontend:
    ports:
      - "3002:3001"  # เปลี่ยนจาก 3001 เป็น 3002
  ```

### 4. Database Connection Error

**Error:** `FATAL: password authentication failed for user "user"`

**ตรวจสอบ:**
```bash
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT 1;"
```

**แก้ไข:**
- Password ที่ถูกต้อง: `password123`
- ถ้ายังไม่ได้ ให้ลบ volume และสร้างใหม่:
  ```bash
  docker-compose down -v
  docker-compose up -d
  ```

### 5. Frontend Shows Blank Page

**สาเหตุ:** JavaScript error หรือ routing ผิด

**ตรวจสอบ:**
```bash
# ดู logs
docker logs criminal-case-frontend -f

# ดู browser console (F12)
```

**แก้ไข:**
```bash
# Hard refresh browser
Ctrl+Shift+R  # Windows/Linux
Cmd+Shift+R   # Mac

# ล้าง cache
docker exec -it criminal-case-frontend sh
rm -rf node_modules/.vite
exit
docker-compose restart frontend
```

### 6. Hot Reload ไม่ทำงาน

**Backend:**
```bash
# ตรวจสอบว่า uvicorn มี --reload flag
docker exec criminal-case-backend ps aux | grep uvicorn
```

**Frontend:**
```bash
# ตรวจสอบว่า Vite running
docker logs criminal-case-frontend | grep "ready"
```

**แก้ไข:**
```bash
docker-compose restart backend
docker-compose restart frontend
```

### 7. เลขที่หนังสือแสดงเป็น NaN

**สาเหตุ:** มีการใช้ `parseInt()` กับ document_number ที่เป็น string

**แก้ไข:** ลบ `parseInt()` ออก ใช้แค่ `value || '-'`

ตรวจสอบว่าข้อมูลในฐานข้อมูลเป็นรูปแบบ "ตช.0039.52/xxxx"

---

## 📝 เอกสารเพิ่มเติม

- `DEVELOPMENT_GUIDE.md` - คู่มือสำหรับนักพัฒนา
- `DOCKER_USAGE.md` - คำสั่ง Docker ที่ใช้บ่อย
- `BACKUP_RESTORE_GUIDE.md` - วิธี Backup/Restore ฐานข้อมูล
- `CHANGELOG.md` - ประวัติการเปลี่ยนแปลง

---

## 🔒 ความปลอดภัย

**⚠️ สำคัญสำหรับ Production:**
1. เปลี่ยน database password ใน `docker-compose.yml`
2. เปลี่ยน admin password ในระบบ
3. ตั้งค่า CORS ให้ถูกต้อง
4. ใช้ HTTPS
5. ตั้งค่า SECRET_KEY ใหม่
6. สำรองข้อมูลเป็นประจำ

---

## 📞 ข้อมูลโปรเจค

- **พัฒนาโดย**: กก.1 บก.สอท.4
- **Version**: 3.1.1
- **Last Updated**: 3 ตุลาคม 2568
- **Database Backup**: `backup_20251003_163753.dump` (76 KB)

**สถิติโค้ด:**
- Backend: Python (FastAPI)
- Frontend: TypeScript + React
- Database: PostgreSQL
- Total Lines of Code: ~15,000 lines

---

## 📄 License

Internal Use Only - สำหรับใช้ภายในหน่วยงานเท่านั้น
