# 🚀 Quick Start Guide - ระบบจัดการคดีอาญา Web Application

## 📋 สารบัญ
1. [ติดตั้งระบบ](#-ติดตั้งระบบ)
2. [รันด้วย Docker](#-วิธีที่-1-รันด้วย-docker-แนะนำ)
3. [รันแบบ Development](#-วิธีที่-2-รันแบบ-development)
4. [Migration ข้อมูล](#-migration-ข้อมูล)
5. [เข้าใช้งานระบบ](#-เข้าใช้งานระบบ)

---

## 📦 ติดตั้งระบบ

### ข้อกำหนดเบื้องต้น

- **Docker Desktop** (สำหรับ Windows/Mac) หรือ **Docker Engine** (สำหรับ Linux)
- **Git** (สำหรับ clone โปรเจค)
- **Node.js 18+** และ **Python 3.10+** (ถ้ารันแบบ Development)

---

## 🐳 วิธีที่ 1: รันด้วย Docker (แนะนำ)

### Step 1: เตรียมโปรเจค

```bash
# ไปที่โฟลเดอร์ web-app
cd /mnt/c/SaveToExcel/web-app

# ตรวจสอบว่ามีไฟล์ docker-compose.yml
ls docker-compose.yml
```

### Step 2: ตั้งค่า Environment Variables

```bash
cd backend
cp .env.example .env

# แก้ไขไฟล์ .env (สำคัญ!)
# เปลี่ยน SECRET_KEY ให้ปลอดภัย
nano .env  # หรือใช้ editor ที่ชอบ
```

ตัวอย่าง `.env`:
```env
DATABASE_URL=postgresql://user:password@postgres:5432/criminal_case_db
REDIS_URL=redis://redis:6379/0
SECRET_KEY=your-super-secret-key-change-this-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Step 3: สร้างและรัน Containers

```bash
cd ..  # กลับมาที่โฟลเดอร์ web-app

# Build และรัน containers ทั้งหมด
docker-compose up -d --build
```

### Step 4: ตรวจสอบสถานะ

```bash
# ดู logs
docker-compose logs -f

# ตรวจสอบว่า containers รันอยู่
docker-compose ps
```

คุณควรเห็น:
- ✅ `criminal-case-backend` - running
- ✅ `criminal-case-frontend` - running
- ✅ `criminal-case-db` - running (PostgreSQL)
- ✅ `criminal-case-redis` - running

---

## 💻 วิธีที่ 2: รันแบบ Development

### Backend Setup

```bash
cd backend

# สร้าง virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# ติดตั้ง dependencies
pip install -r requirements.txt

# ตั้งค่า environment
cp .env.example .env
nano .env  # แก้ไข DATABASE_URL, SECRET_KEY

# สร้างตารางในฐานข้อมูล (ถ้ายังไม่มี)
python init_db.py

# รัน backend server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend จะรันที่: **http://localhost:8000**

### Frontend Setup

เปิด terminal ใหม่:

```bash
cd frontend

# ติดตั้ง dependencies
npm install

# รัน development server
npm run dev
```

Frontend จะรันที่: **http://localhost:5173** (Vite) หรือ **http://localhost:3000**

---

## 📊 Migration ข้อมูล

### ย้ายข้อมูลจาก Excel → PostgreSQL

#### ใช้ Docker:

```bash
# เข้าไปใน backend container
docker-compose exec backend bash

# รัน migration script
python migrate_data.py --init --all

# หรือย้ายทีละโมดูล
python migrate_data.py --init --banks
python migrate_data.py --suspects
python migrate_data.py --cases
python migrate_data.py --arrests

# ออกจาก container
exit
```

#### ใช้ Local:

```bash
cd backend
source venv/bin/activate

# สร้างตารางก่อน
python migrate_data.py --init

# ย้ายข้อมูลทั้งหมด
python migrate_data.py --all

# หรือระบุ path ของ Excel files
python migrate_data.py --all --excel-dir /path/to/Xlsx
```

### ตัวเลือก Migration:

| Command | คำอธิบาย |
|---------|----------|
| `--init` | สร้างตารางในฐานข้อมูล |
| `--all` | ย้ายข้อมูลทั้งหมด |
| `--banks` | ย้ายข้อมูลบัญชีธนาคารเท่านั้น |
| `--suspects` | ย้ายข้อมูลหมายเรียกผู้ต้องหาเท่านั้น |
| `--cases` | ย้ายข้อมูลคดีอาญาเท่านั้น |
| `--arrests` | ย้ายข้อมูลหลังการจับกุมเท่านั้น |
| `--excel-dir PATH` | ระบุ path ของโฟลเดอร์ Xlsx |

---

## 🎯 เข้าใช้งานระบบ

### เข้าถึงแอปพลิเคชัน:

| Service | URL | คำอธิบาย |
|---------|-----|----------|
| **Frontend** | http://localhost:3000 | หน้าเว็บหลัก |
| **Backend API** | http://localhost:8000 | REST API |
| **API Docs** | http://localhost:8000/docs | Swagger UI |
| **Alternative API Docs** | http://localhost:8000/redoc | ReDoc |

### สร้าง Admin User แรก:

```bash
# ใช้ Docker
docker-compose exec backend python create_admin.py

# ใช้ Local
cd backend
python create_admin.py
```

Script จะสร้าง user:
- **Username:** `admin`
- **Password:** `admin123` (เปลี่ยนทันทีหลังเข้าระบบ!)
- **Role:** Admin

### Login เข้าระบบ:

1. เปิด http://localhost:3000
2. กรอก username: `admin`
3. กรอก password: `admin123`
4. คลิก "เข้าสู่ระบบ"

---

## 🔧 คำสั่งที่ใช้บ่อย

### Docker Commands

```bash
# ดู logs ทั้งหมด
docker-compose logs -f

# ดู logs เฉพาะ service
docker-compose logs -f backend
docker-compose logs -f frontend

# รีสตาร์ท service
docker-compose restart backend

# หยุดระบบ
docker-compose down

# หยุดและลบ volumes (ระวัง: จะลบข้อมูลในฐานข้อมูล!)
docker-compose down -v

# Build ใหม่
docker-compose up -d --build
```

### Database Commands

```bash
# เข้า PostgreSQL shell
docker-compose exec postgres psql -U user -d criminal_case_db

# Backup database
docker-compose exec postgres pg_dump -U user criminal_case_db > backup.sql

# Restore database
docker-compose exec -T postgres psql -U user criminal_case_db < backup.sql
```

---

## 🐛 Troubleshooting

### 1. Port Already in Use

**ปัญหา:** Port 3000, 8000, 5432 ถูกใช้งานอยู่

**แก้ไข:** เปลี่ยน port ใน `docker-compose.yml`

```yaml
services:
  frontend:
    ports:
      - "3001:80"  # เปลี่ยนจาก 3000 เป็น 3001

  backend:
    ports:
      - "8001:8000"  # เปลี่ยนจาก 8000 เป็น 8001
```

### 2. Database Connection Failed

**ปัญหา:** Backend ไม่สามารถเชื่อมต่อ PostgreSQL

**แก้ไข:**
```bash
# ตรวจสอบว่า PostgreSQL รันอยู่
docker-compose ps postgres

# ดู logs
docker-compose logs postgres

# รีสตาร์ท PostgreSQL
docker-compose restart postgres
```

### 3. Frontend ไม่เชื่อมต่อ Backend

**ปัญหา:** CORS error หรือ API ไม่ตอบสนอง

**แก้ไข:** ตรวจสอบ `backend/app/core/config.py`

```python
CORS_ORIGINS: List[str] = [
    "http://localhost:3000",
    "http://localhost:5173",  # เพิ่ม Vite dev server
]
```

### 4. Migration ไม่สำเร็จ

**ปัญหา:** ไม่พบไฟล์ Excel หรือ column ไม่ตรงกัน

**แก้ไข:**
```bash
# ตรวจสอบว่าไฟล์ Excel อยู่ที่ถูกต้อง
ls ../Xlsx/

# ระบุ path ชัดเจน
python migrate_data.py --all --excel-dir /absolute/path/to/Xlsx
```

### 5. Docker Build ล้มเหลว

**ปัญหา:** Dockerfile build error

**แก้ไข:**
```bash
# ลบ cache และ build ใหม่
docker-compose build --no-cache

# ลบ images เก่า
docker system prune -a
```

---

## 📚 ขั้นตอนถัดไป

หลังจากรันระบบสำเร็จแล้ว:

1. ✅ เปลี่ยนรหัสผ่าน admin
2. ✅ สร้าง users เพิ่มเติม
3. ✅ Migration ข้อมูลจาก Excel
4. ✅ ทดสอบ CRUD operations
5. ✅ ทดสอบการสร้างเอกสาร
6. ✅ Setup backup schedule

---

## 🆘 ขอความช่วยเหลือ

หากพบปัญหา:

1. ดู logs: `docker-compose logs -f`
2. ตรวจสอบ API docs: http://localhost:8000/docs
3. ตรวจสอบ README.md และ DEPLOYMENT.md
4. สร้าง issue บน GitHub

---

## 📝 ข้อมูลเพิ่มเติม

- **README.md** - รายละเอียดโปรเจคและฟีเจอร์
- **DEPLOYMENT.md** - คู่มือ deployment production
- **RUN_WITHOUT_DOCKER.md** - วิธีรันแบบไม่ใช้ Docker

---

**เวอร์ชัน:** 3.0.0
**อัปเดตล่าสุด:** September 2025
**ผู้พัฒนา:** Criminal Case Management System Team