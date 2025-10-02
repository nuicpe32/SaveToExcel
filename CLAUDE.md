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

**โปรเจค Web App ใช้ Development Mode เป็นหลัก:**

```bash
cd /mnt/c/SaveToExcel/web-app
docker-compose -f docker-compose.dev.yml up -d
```

**URLs:**
- Frontend: http://localhost:3001
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Login:**
- Username: `admin`
- Password: `admin123`

**📖 อ่านเอกสารสำคัญ:**
- `/mnt/c/SaveToExcel/web-app/IMPORTANT_DEV_MODE.md` ⭐ **อ่านก่อนเสมอ!**
- `/mnt/c/SaveToExcel/web-app/README.md`
- `/mnt/c/SaveToExcel/web-app/BACKUP_RESTORE_GUIDE.md`

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
    ├── docker-compose.dev.yml       # ⭐ ใช้อันนี้!
    ├── docker-compose.yml           # ⚠️ เลิกใช้แล้ว
    ├── IMPORTANT_DEV_MODE.md        # ⭐ อ่านก่อนเสมอ!
    ├── BACKUP_RESTORE_GUIDE.md
    └── README.md
```

---

## 🎯 สำหรับ AI Assistant / New Developer

### เมื่อได้รับโปรเจคนี้:

1. **อ่านไฟล์สำคัญก่อน:**
   - `/mnt/c/SaveToExcel/web-app/IMPORTANT_DEV_MODE.md` ⭐⭐⭐
   - ไฟล์นี้บอกทุกอย่างที่ต้องรู้เกี่ยวกับ Docker, Volumes, Containers

2. **ตรวจสอบว่ากำลังทำงานกับ App ไหน:**
   - Desktop App → ใช้ `simple_excel_manager.py`
   - Web App → ใช้ `docker-compose -f docker-compose.dev.yml`

3. **สำหรับ Web App:**
   - **เสมอ** ใช้ `docker-compose -f docker-compose.dev.yml`
   - **อย่า** ใช้ `docker-compose up` (จะใช้ volume ผิด)
   - Container ทั้งหมดลงท้ายด้วย `-dev`
   - Database password: `password123` (ไม่ใช่ `password`)

4. **ตรวจสอบสถานะปัจจุบัน:**
   ```bash
   docker ps  # ดู containers
   docker volume ls | grep dev  # ดู volumes
   ```

---

## 📦 Docker Configuration (Web App)

### ❌ อย่าใช้:
```bash
docker-compose up -d  # ❌ ใช้ production volumes (ผิด!)
```

### ✅ ใช้อันนี้:
```bash
docker-compose -f docker-compose.dev.yml up -d  # ✅ ถูกต้อง!
```

### Container Names (สำคัญ!):
- `criminal-case-db-dev` - PostgreSQL (password: `password123`)
- `criminal-case-redis-dev` - Redis
- `criminal-case-backend-dev` - FastAPI
- `criminal-case-frontend-dev` - React (Vite)

### Volume Names:
- `criminal-case-postgres-dev` ✅ ใช้งานอยู่
- `criminal-case-uploads-dev` ✅ ใช้งานอยู่
- `web-app_postgres_data` ⚠️ เก่า (ไม่ใช้แล้ว)

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

### Web App (Development Mode):

```bash
# เริ่มระบบ
cd /mnt/c/SaveToExcel/web-app
docker-compose -f docker-compose.dev.yml up -d

# หยุดระบบ
docker-compose -f docker-compose.dev.yml down

# ดู logs
docker logs criminal-case-backend-dev -f
docker logs criminal-case-frontend-dev -f

# เข้า container
docker exec -it criminal-case-backend-dev bash
docker exec -it criminal-case-db-dev psql -U user -d criminal_case_db

# ตรวจสอบข้อมูล
docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "
SELECT
  (SELECT COUNT(*) FROM criminal_cases) as cases,
  (SELECT COUNT(*) FROM suspects) as suspects,
  (SELECT COUNT(*) FROM bank_accounts) as banks;
"

# Backup database
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec criminal-case-db-dev pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_${TIMESTAMP}.dump
docker cp criminal-case-db-dev:/tmp/backup_${TIMESTAMP}.dump ./backup_database_${TIMESTAMP}.dump
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

**สาเหตุ:** ใช้ `docker-compose.yml` แทน `docker-compose.dev.yml`

**วิธีแก้:**
```bash
# Restore จาก backup
docker cp backup_database_YYYYMMDD_HHMMSS.dump criminal-case-db-dev:/tmp/restore.dump
docker exec criminal-case-db-dev pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

### 3. Login ไม่ได้

**เช็คสิ่งเหล่านี้:**
```bash
# 1. ตรวจสอบ users table
docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "SELECT * FROM users;"

# 2. Test API โดยตรง
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# 3. ดู backend logs
docker logs criminal-case-backend-dev --tail 50
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
1. อ่าน `IMPORTANT_DEV_MODE.md` ก่อนทำงานกับ Web App
2. ใช้ `docker-compose -f docker-compose.dev.yml` สำหรับ Web App
3. ใช้ `-dev` container names
4. ใช้ `password123` สำหรับ database (DEV mode)
5. สร้าง backup ก่อนทำการเปลี่ยนแปลงสำคัญ
6. ตรวจสอบ `docker ps` และ `docker volume ls` ก่อนเริ่มงาน

### ❌ Never:
1. ใช้ `docker-compose up` โดยไม่ระบุ `-f docker-compose.dev.yml`
2. สมมติว่า production mode ใช้งานอยู่
3. ใช้ `localhost:8000` ใน Docker network (ต้องใช้ `backend:8000`)
4. ลืมตรวจสอบ volume ที่ใช้งานอยู่
5. แก้ไข `docker-compose.yml` (ใช้ `.dev.yml` แทน)

---

## 📚 Documentation Files

### Web App:
- ⭐ `web-app/IMPORTANT_DEV_MODE.md` - **อ่านก่อนเสมอ!**
- `web-app/README.md` - คู่มือหลัก
- `web-app/BACKUP_RESTORE_GUIDE.md` - Backup/Restore
- `web-app/DEV_MODE_SETUP.md` - Development setup

### Desktop App:
- `README.md` - User documentation
- `PROJECT_STATE.md` - Project state
- `ARCHITECTURE.md` - Technical architecture

### This File:
- `CLAUDE.md` - Context for AI (you are here!)

---

**Created:** 1 October 2025
**Updated:** 1 October 2025
**For:** AI Assistants & Developers
**Project:** Criminal Case Management System v3.0.1

---

## 🔗 Quick Links Summary

**Web App Quick Start:**
```bash
cd /mnt/c/SaveToExcel/web-app && docker-compose -f docker-compose.dev.yml up -d
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
docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM criminal_cases;"
```

---

**หมายเหตุสำคัญ:** ถ้ามีข้อสงสัยหรือข้อมูลไม่ตรงกัน ให้เชื่อไฟล์ `IMPORTANT_DEV_MODE.md` เป็นหลัก เพราะเป็นไฟล์ที่อัพเดทล่าสุดและมีรายละเอียดครบถ้วนที่สุด
