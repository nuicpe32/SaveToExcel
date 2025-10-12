# 🚀 Criminal Case Management System - Installation Package

**Version:** 3.3.2  
**Export Date:** October 11, 2025  
**GitHub:** https://github.com/nuicpe32/SaveToExcel

---

## 📦 Package Contents

```
criminal-case-export/
├── criminal-case-images.tar      # Docker images (518 MB)
├── criminal-case-database.sql    # Database backup (1.9 MB)
├── uploads/                      # Uploaded files (CFR, etc.)
│   └── cfr/
├── docker-compose.yml            # Docker compose configuration
├── .env.example                  # Environment variables example
└── README.md                     # This file
```

---

## 🎯 Quick Start

### Prerequisites:
- Docker Desktop installed
- Git installed
- At least 4 GB free disk space

### Installation Steps:

#### 1️⃣ Load Docker Images (ใช้เวลา ~2-3 นาที)
```bash
docker load -i criminal-case-images.tar
```

**Output ที่ควรเห็น:**
```
Loaded image: web-app-frontend:latest
Loaded image: web-app-backend:latest
Loaded image: postgres:15-alpine
```

#### 2️⃣ Clone Project from GitHub
```bash
git clone https://github.com/nuicpe32/SaveToExcel.git
cd SaveToExcel/web-app
```

#### 3️⃣ Setup Environment
```bash
# Copy environment file
copy .env.example .env

# Edit .env if needed (optional)
notepad .env
```

#### 4️⃣ Start Docker Containers
```bash
# Start all containers
docker-compose up -d

# Wait for containers to be ready (30 seconds)
timeout /t 30

# Check status
docker ps
```

**ควรเห็น containers 5 ตัว:**
- criminal-case-frontend (port 3001)
- criminal-case-backend (port 8000)
- criminal-case-db (port 5432)
- criminal-case-redis (port 6379)
- criminal-case-adminer (port 8080)

#### 5️⃣ Restore Database
```bash
# Copy database backup into container
docker cp ..\criminal-case-export\criminal-case-database.sql criminal-case-db:/tmp/

# Restore database
docker exec criminal-case-db psql -U user -d criminal_case_db -f /tmp/database_backup.sql

# Verify
docker exec criminal-case-db psql -U user -d criminal_case_db -c "\dt"
```

#### 6️⃣ Restore Uploaded Files
```bash
# Copy uploads folder
docker cp ..\criminal-case-export\uploads criminal-case-backend:/app/

# Verify
docker exec criminal-case-backend ls -la /app/uploads
```

#### 7️⃣ Access System
```
Frontend:  http://localhost:3001
Backend:   http://localhost:8000
API Docs:  http://localhost:8000/docs
Adminer:   http://localhost:8080
```

**Default Admin User:**
- Username: `admin`
- Password: `admin123` (เปลี่ยนหลังเข้าใช้งานครั้งแรก)

---

## 🔧 Troubleshooting

### ปัญหา: Port ถูกใช้งานอยู่
```bash
# หา process ที่ใช้ port
netstat -ano | findstr :3001
netstat -ano | findstr :8000

# หยุด container เดิม
docker-compose down

# เริ่มใหม่
docker-compose up -d
```

### ปัญหา: Database restore ล้มเหลว
```bash
# ลบ database และสร้างใหม่
docker exec criminal-case-db psql -U user -d postgres -c "DROP DATABASE IF EXISTS criminal_case_db;"
docker exec criminal-case-db psql -U user -d postgres -c "CREATE DATABASE criminal_case_db;"

# Restore อีกครั้ง
docker exec criminal-case-db psql -U user -d criminal_case_db -f /tmp/database_backup.sql
```

### ปัญหา: Frontend ไม่เชื่อม Backend
```bash
# ตรวจสอบ backend logs
docker logs criminal-case-backend --tail 50

# Restart backend
docker restart criminal-case-backend
```

### ปัญหา: ไฟล์ไม่แสดง
```bash
# ตรวจสอบ permissions
docker exec criminal-case-backend ls -la /app/uploads

# แก้ไข permissions
docker exec criminal-case-backend chmod -R 755 /app/uploads
```

---

## 📚 Documentation

**เอกสารเพิ่มเติม:**
- [User Manual](./USER_MANUAL.md)
- [Development Guide](./DEVELOPMENT_GUIDE.md)
- [API Documentation](http://localhost:8000/docs)
- [Release Notes](./RELEASE_NOTES_CFR_AUTO_SUMMONS_v3.3.1.md)

---

## 🔄 Development

### Start Development:
```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm install
npm run dev
```

### Run Tests:
```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm test
```

---

## 📊 System Information

### Tech Stack:
- **Frontend:** React 18 + TypeScript + Vite + Ant Design
- **Backend:** FastAPI (Python 3.12) + SQLAlchemy
- **Database:** PostgreSQL 15
- **Cache:** Redis 7
- **PDF:** ReportLab
- **Flow Chart:** ReactFlow

### Features:
- ✅ Criminal case management
- ✅ Bank account summons tracking
- ✅ Suspect management
- ✅ CFR (Central Fraud Registry) integration
- ✅ Financial flow chart visualization
- ✅ Auto summons creation from CFR
- ✅ PDF document generation
- ✅ User authentication & authorization
- ✅ Organization structure (Bureau/Division/Supervision)

---

## 🔐 Security Notes

### ⚠️ สำคัญ:
1. **เปลี่ยนรหัสผ่าน admin** ทันทีหลังติดตั้ง
2. **อัพเดต .env** ให้ตรงกับ environment ของคุณ
3. **เปลี่ยน SECRET_KEY** ใน backend/.env
4. **ตั้งค่า firewall** ถ้า deploy บน production

### Database Credentials:
```
DB_HOST: localhost
DB_PORT: 5432
DB_NAME: criminal_case_db
DB_USER: user
DB_PASSWORD: password
```

**⚠️ เปลี่ยน password ก่อน deploy production!**

---

## 📞 Support

### Issues:
- GitHub Issues: https://github.com/nuicpe32/SaveToExcel/issues

### Contact:
- Developer: Ampon.Th
- GitHub Issues: https://github.com/nuicpe32/SaveToExcel/issues

---

## 📝 Version History

**v3.3.2 (Current):**
- CFR victim transfer sequence
- Bank logo watermarks
- Auto summons creation from CFR
- Improved flow chart layout

**v3.3.1:**
- CFR flow chart visualization
- CFR data upload and display

**v3.3.0:**
- Organization structure
- User management improvements

---

## 🙏 License

Copyright (c) 2025 Ampon.Th

---

## ✅ Post-Installation Checklist

After installation, verify:
- [ ] Can login with admin credentials
- [ ] Can view criminal cases
- [ ] Can create bank account summons
- [ ] Can upload CFR files
- [ ] Can view CFR flow chart
- [ ] Can create summons from CFR
- [ ] Bank logos display correctly
- [ ] PDF documents generate correctly

---

**🎉 Happy Coding!**

For detailed instructions, see EXPORT_IMPORT_GUIDE.md

