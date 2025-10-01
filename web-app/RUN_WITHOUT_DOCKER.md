# วิธีรันโปรเจคโดยไม่ใช้ Docker

## ข้อกำหนด

1. **Python 3.11+**
2. **Node.js 18+**
3. **PostgreSQL 14+**
4. **Redis** (Optional)

---

## ขั้นตอนที่ 1: ติดตั้ง PostgreSQL

### Windows:

1. ดาวน์โหลด PostgreSQL Installer:
   https://www.postgresql.org/download/windows/

2. ติดตั้งและจดจำ:
   - Username: `postgres`
   - Password: (ที่คุณตั้ง)
   - Port: `5432`

3. สร้าง Database:
   ```cmd
   psql -U postgres
   CREATE DATABASE criminal_case_db;
   \q
   ```

---

## ขั้นตอนที่ 2: ติดตั้ง Redis (Optional)

### Windows - ใช้ WSL2:

```powershell
wsl
sudo apt update
sudo apt install redis-server -y
sudo service redis-server start
```

หรือดาวน์โหลด Redis for Windows:
https://github.com/microsoftarchive/redis/releases

---

## ขั้นตอนที่ 3: รัน Backend

```powershell
# เปิด PowerShell Terminal 1
cd C:\SaveToExcel\web-app\backend

# สร้าง Virtual Environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# ติดตั้ง Dependencies
pip install -r requirements.txt

# ตั้งค่า Environment Variables
copy .env.example .env

# แก้ไขไฟล์ .env:
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/criminal_case_db
# REDIS_URL=redis://localhost:6379/0
# SECRET_KEY=your-super-secret-key-change-this
# (ใช้ notepad .env)

# รัน Database Migration
# Note: ข้ามขั้นตอนนี้ไปก่อน database จะถูกสร้างอัตโนมัติ

# รัน Backend Server
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend จะรันที่: **http://localhost:8000**

---

## ขั้นตอนที่ 4: รัน Frontend

```powershell
# เปิด PowerShell Terminal 2 (ใหม่)
cd C:\SaveToExcel\web-app\frontend

# ติดตั้ง Node.js Dependencies
npm install

# รัน Development Server
npm run dev
```

Frontend จะรันที่: **http://localhost:3000**

---

## ขั้นตอนที่ 5: สร้าง Admin User

```powershell
# เปิด PowerShell Terminal 3 (ใหม่)
cd C:\SaveToExcel\web-app\backend
.\venv\Scripts\Activate.ps1

# รัน Python Script
python
```

```python
from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models import User, UserRole

db = SessionLocal()

admin = User(
    username='admin',
    email='admin@example.com',
    full_name='Administrator',
    hashed_password=get_password_hash('admin123'),
    role=UserRole.ADMIN,
    is_active=True
)

db.add(admin)
db.commit()
print("✅ Admin user created!")
print("Username: admin")
print("Password: admin123")
```

กด `Ctrl+Z` แล้ว `Enter` เพื่อออก

---

## การเข้าใช้งาน

1. เปิดเบราว์เซอร์: http://localhost:3000
2. Login ด้วย:
   - Username: `admin`
   - Password: `admin123`

---

## Troubleshooting

### ปัญหา: Backend ไม่เชื่อมต่อ Database

```powershell
# ตรวจสอบ PostgreSQL รันอยู่หรือไม่
psql -U postgres -c "SELECT version();"

# ตรวจสอบ connection string ในไฟล์ .env
```

### ปัญหา: Frontend ไม่เชื่อมต่อ Backend

แก้ไขไฟล์ `C:\SaveToExcel\web-app\frontend\vite.config.ts`:

```typescript
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // ตรวจสอบ URL
      changeOrigin: true,
    },
  },
}
```

### ปัญหา: Module not found

```powershell
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### ปัญหา: Port already in use

```powershell
# หา process ที่ใช้ port 8000
netstat -ano | findstr :8000

# Kill process
taskkill /PID <PID> /F
```

---

## คำสั่งที่มีประโยชน์

```powershell
# ดู Backend logs
# (จะแสดงใน Terminal ที่รัน uvicorn)

# ดู Frontend logs
# (จะแสดงใน Terminal ที่รัน npm run dev)

# หยุดโปรแกรม
# กด Ctrl+C ใน Terminal

# Restart Backend
# กด Ctrl+C แล้วรัน uvicorn อีกครั้ง

# Restart Frontend
# กด Ctrl+C แล้วรัน npm run dev อีกครั้ง
```

---

## การ Deploy แบบไม่ใช้ Docker

ดูคู่มือใน `DEPLOYMENT.md` section "On-Premise Server" แต่ข้าม Docker steps