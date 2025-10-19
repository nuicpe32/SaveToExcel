# CLAUDE.md - Project Context for Criminal Case Management System

## ⚠️ สำคัญมาก: โปรเจคนี้มี 2 Application

### 1. Desktop Application (Python + tkinter)
- **Path:** `/mnt/c/SaveToExcel/`
- **Main file:** `simple_excel_manager.py`
- **Version:** 2.9.0+
- **Status:** Production-ready

### 2. Web Application (FastAPI + React)
- **Path:** `/mnt/c/SaveToExcel/web-app/`
- **Version:** 3.0.1+
- **Status:** Active Development
- **⚠️ ใช้ DEV MODE เป็นหลัก**

---

## 🚀 Web Application - Quick Start (สำคัญ!)

**โปรเจค Web App ใช้ Docker Compose (Universal Mode):**

```bash
cd /mnt/c/SaveToExcel/web-app
docker-compose up -d
```

**URLs:**
- Frontend: http://localhost:3001
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Login:**
- Username: `admin`
- Password: `admin123`

**📖 อ่านเอกสารสำคัญ:**
- `/mnt/c/SaveToExcel/web-app/README.md` - ⭐ **เอกสารเดียวที่ครบถ้วนสมบูรณ์!**

---

## 📁 Project Structure

```
/mnt/c/SaveToExcel/
├── simple_excel_manager.py          # Desktop App (Python)
├── run.py                           # Alternative entry
├── Doc/                             # Word templates (9 files)
├── Xlsx/                            # Excel databases (6 files)
├── THSarabunNew/                    # Thai fonts
├── README.md                        # Desktop App docs
├── PROJECT_STATE.md                 # Desktop App state
├── CLAUDE.md                        # This file
└── web-app/                         # 🌐 Web Application
    ├── backend/                     # FastAPI Backend
    │   ├── app/
    │   │   ├── api/v1/             # API endpoints
    │   │   ├── models/             # SQLAlchemy models
    │   │   ├── schemas/            # Pydantic schemas
    │   │   └── main.py
    │   ├── requirements.txt
    │   └── Dockerfile
    ├── frontend/                    # React Frontend
    │   ├── src/
    │   │   ├── components/
    │   │   ├── pages/
    │   │   └── App.tsx
    │   ├── package.json
    │   └── Dockerfile.dev
    ├── docker-compose.yml           # ⭐ Universal Docker Compose
    └── README.md                    # ⭐ เอกสารเดียวครบถ้วน (880+ บรรทัด)
```

---

## 🎯 สำหรับ AI Assistant / New Developer

### เมื่อได้รับโปรเจคนี้:

1. **อ่านไฟล์สำคัญก่อน:**
   - `/mnt/c/SaveToExcel/web-app/README.md` ⭐ **เอกสารเดียวที่ครบถ้วนสมบูรณ์!**
   - เอกสารนี้รวมทุกอย่าง: Quick Start, Architecture, Features, Database, Email System, CFR System, Master Data, Deployment, Backup & Restore, Troubleshooting, และ Changelog

2. **ตรวจสอบว่ากำลังทำงานกับ App ไหน:**
   - Desktop App → ใช้ `simple_excel_manager.py`
   - Web App → ใช้ `docker-compose up -d`

3. **สำหรับ Web App:**
   - ใช้ `docker-compose up -d` (Universal mode รองรับทั้ง Dev และ Production)
   - Database password: `password123`
   - Container names: `criminal-case-db`, `criminal-case-backend`, `criminal-case-frontend`

4. **ตรวจสอบสถานะปัจจุบัน:**
   ```bash
   docker ps  # ดู containers
   docker volume ls | grep criminal  # ดู volumes
   ```

---

## 📦 Docker Configuration (Web App)

### ✅ คำสั่งที่ใช้:
```bash
docker-compose up -d  # เริ่มระบบ (Universal mode)
docker-compose down   # หยุดระบบ
docker-compose logs -f # ดู logs
docker-compose restart # Restart services
```

### Container Names (สำคัญ!):
- `criminal-case-db` - PostgreSQL (password: `password123`)
- `criminal-case-redis` - Redis
- `criminal-case-backend` - FastAPI (with hot reload)
- `criminal-case-frontend` - React (Vite dev server)
- `criminal-case-pgadmin` - pgAdmin (optional, use `--profile tools`)
- `criminal-case-adminer` - Adminer (optional, use `--profile tools`)

### Volume Names:
- `criminal-case-postgres` - Database data
- `criminal-case-uploads` - User uploads (signatures, etc.)
- `criminal-case-pgadmin` - pgAdmin data

---

## 🔐 Credentials (Web App)

### Database:
```
Host: localhost (outside) / postgres (inside Docker)
Port: 5432
User: user
Password: password123  # ⚠️ สำคัญ! ไม่ใช่ 'password'
Database: criminal_case_db
```

### Admin Login:
```
Username: admin
Password: admin123
```

---

## 🛠️ Common Commands

### Web App:

```bash
# เริ่มระบบ
cd /mnt/c/SaveToExcel/web-app
docker-compose up -d

# หยุดระบบ
docker-compose down

# ดู logs
docker logs criminal-case-backend -f
docker logs criminal-case-frontend -f

# เข้า container
docker exec -it criminal-case-backend bash
docker exec -it criminal-case-db psql -U user -d criminal_case_db

# ตรวจสอบข้อมูล
docker exec criminal-case-db psql -U user -d criminal_case_db -c "
SELECT
  (SELECT COUNT(*) FROM criminal_cases) as cases,
  (SELECT COUNT(*) FROM suspects) as suspects,
  (SELECT COUNT(*) FROM bank_accounts) as banks;
"

# Backup database
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_${TIMESTAMP}.dump
docker cp criminal-case-db:/tmp/backup_${TIMESTAMP}.dump ./backup_database_${TIMESTAMP}.dump

# เปิด pgAdmin (optional)
docker-compose --profile tools up -d pgadmin

# เปิด Adminer (optional)
docker-compose --profile tools up -d adminer
```

### Desktop App:

```bash
# รันโปรแกรม
cd /mnt/c/SaveToExcel
python3 simple_excel_manager.py

# ทดสอบ syntax
python3 -m py_compile simple_excel_manager.py

# ตรวจสอบ dependencies
python3 -c "import tkinter, pandas, openpyxl; print('All dependencies available')"
```

---

## 🚨 ปัญหาที่พบบ่อย (Web App)

### 1. Frontend ไม่เชื่อมต่อ Backend (ECONNREFUSED)

**สาเหตุ:** `vite.config.ts` ชี้ไป `localhost:8000` แทนที่จะเป็น `backend:8000`

**วิธีแก้:** (แก้ไขแล้ว)
```typescript
// frontend/vite.config.ts
proxy: {
  '/api': {
    target: 'http://backend:8000',  // ✅ ใช้ Docker service name
    changeOrigin: true,
  },
}
```

### 2. ข้อมูลหายหลัง Restart

**สาเหตุ:** ลบ volumes โดยไม่ได้ตั้งใจ (docker-compose down -v)

**วิธีแก้:**
```bash
# Restore จาก backup
docker cp backup_database_YYYYMMDD_HHMMSS.dump criminal-case-db:/tmp/restore.dump
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

### 3. Login ไม่ได้

**เช็คสิ่งเหล่านี้:**
```bash
# 1. ตรวจสอบ users table
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT * FROM users;"

# 2. Test API โดยตรง
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 3. ดู backend logs
docker logs criminal-case-backend --tail 50
```

---

## 📊 Current System Status (ณ วันที่ 1 ต.ค. 2025)

### Web App Data:
- ✅ 48 คดีอาญา
- ✅ 15 ผู้ต้องหา
- ✅ 418 บัญชีธนาคาร
- ✅ 1 Admin user

### Backup Files:
- `backup_database_20251001_221353.dump` (75 KB)
- `web-app-backup-20251001_221400.tar.gz` (682 KB)
- Location: `/mnt/c/SaveToExcel/web-app/`

---

## 💡 Development Guidelines

### Code Style:
- **No comments unless requested** - Keep code clean
- **Follow existing patterns** - Maintain consistency
- **Professional naming** - Clear, descriptive names
- **Error handling** - Include try/catch blocks

### UI/UX Standards (Desktop App):
- **Thai language support** - All user-facing text in Thai
- **Professional appearance** - Clean, organized layouts
- **Responsive design** - Proper widget sizing
- **Icon consistency** - Use provided icons or fallback

### Git Commits:
```bash
git add .
git commit -m "Description of changes

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin main
```

---

## 🎯 Important Reminders for AI

### ✅ Always:
1. ใช้ `docker-compose up -d` สำหรับ Web App (Universal mode)
2. ใช้ `password123` สำหรับ database
3. Container names: `criminal-case-db`, `criminal-case-backend`, `criminal-case-frontend`
4. สร้าง backup ก่อนทำการเปลี่ยนแปลงสำคัญ
5. ตรวจสอบ `docker ps` และ `docker volume ls` ก่อนเริ่มงาน
6. ใช้ `backend:8000` ใน Docker network (ไม่ใช่ `localhost:8000`)

### ❌ Never:
1. ใช้ `docker-compose down -v` (จะลบ volumes ทั้งหมด!)
2. ใช้ `localhost:8000` ใน Docker network (ต้องใช้ `backend:8000`)
3. ลืมตรวจสอบ volume ที่ใช้งานอยู่
4. ลืม backup ข้อมูลก่อนทำการเปลี่ยนแปลงครั้งใหญ่

---

## 📚 Documentation Files

### Web App:
- ⭐ `web-app/README.md` - **เอกสารเดียวที่ครบถ้วนสมบูรณ์!** (880+ บรรทัด)
  - รวมทุกอย่าง: Architecture, Features (v3.0.0-3.6.0), Database, Development, Email System, CFR System, Master Data, Deployment, Backup & Restore, Troubleshooting, Changelog
- `web-app/docker-compose.yml` - Docker configuration (Universal mode)

### Desktop App:
- `README.md` - User documentation
- `PROJECT_STATE.md` - Project state
- `ARCHITECTURE.md` - Technical architecture

### This File:
- `CLAUDE.md` - Context for AI (you are here!)

---

**Created:** 1 October 2025
**Updated:** 19 October 2025
**For:** AI Assistants & Developers
**Project:** Criminal Case Management System v3.7.0

**⭐ การอัปเดตล่าสุด (19 ต.ค. 2025 - v3.7.0):**
- 📋 เพิ่มระบบฐานข้อมูลข้อหาความผิด (Charges Master Data)
- 🎨 เพิ่ม Tab "ข้อหาความผิด" ใน Master Data Page (Admin only)
- 📊 นำเข้าข้อมูลเริ่มต้น 5 รายการจากไฟล์ Excel
- 🔐 CRUD operations พร้อม validation และ duplicate check
- 📄 Migration SQL: 033, 034 สำหรับสร้างตารางและ import ข้อมูล

---

## 🔗 Quick Links Summary

**Web App Quick Start:**
```bash
cd /mnt/c/SaveToExcel/web-app && docker-compose up -d
```

**Web App URLs:**
- http://localhost:3001 (Frontend)
- http://localhost:8000/docs (API Docs)

**Desktop App:**
```bash
cd /mnt/c/SaveToExcel && python3 simple_excel_manager.py
```

**ตรวจสอบสถานะ:**
```bash
docker ps  # Web App containers
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM criminal_cases;"
```

---

**หมายเหตุสำคัญ:**
- โปรเจคใช้ Docker Compose แบบ Universal Mode รองรับทั้ง Development และ Production ผ่าน Environment Variables
- ⭐ **เอกสารทั้งหมดอยู่ในไฟล์เดียว:** `/mnt/c/SaveToExcel/web-app/README.md` (880+ บรรทัด)
- อ่านเอกสารนี้ก่อนเริ่มพัฒนาเสมอ เพื่อความเข้าใจที่ถูกต้องและครบถ้วน
