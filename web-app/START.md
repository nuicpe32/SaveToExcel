# 🚀 วิธีเริ่มต้นใช้งาน - เลือก 1 จาก 2 วิธี

## ✅ วิธีที่ 1: ใช้ Docker (แนะนำ - ง่ายที่สุด)

### ติดตั้ง Docker Desktop

1. **ดาวน์โหลดและติดตั้ง:**
   - ไปที่: https://www.docker.com/products/docker-desktop/
   - ดาวน์โหลด "Docker Desktop for Windows"
   - ติดตั้งและรีสตาร์ทเครื่อง

2. **ตรวจสอบการติดตั้ง:**
   ```powershell
   docker --version
   docker compose version
   ```

3. **รันโปรเจค:**
   ```powershell
   cd C:\SaveToExcel\web-app
   docker compose up -d --build
   ```

   **Note:** ใช้ `docker compose` (มีช่องว่าง) ไม่ใช่ `docker-compose`

4. **เข้าใช้งาน:**
   - Frontend: http://localhost:3000
   - Backend: http://localhost:8000/docs
   - Default Login: (ต้องสร้าง user ก่อน - ดูด้านล่าง)

5. **สร้าง Admin User:**
   ```powershell
   docker compose exec backend python -c "
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
   print('Admin created!')
   "
   ```

---

## 🔧 วิธีที่ 2: ไม่ใช้ Docker (รันเอง)

### ข้อกำหนด
- Python 3.11+: https://www.python.org/downloads/
- Node.js 18+: https://nodejs.org/
- PostgreSQL 14+: https://www.postgresql.org/download/windows/

### Auto Setup (ใช้ Script)

```powershell
cd C:\SaveToExcel\web-app
.\QUICK_START.ps1
```

### Manual Setup

**1. ติดตั้ง PostgreSQL**
- ดาวน์โหลดและติดตั้ง
- สร้าง database:
  ```cmd
  psql -U postgres
  CREATE DATABASE criminal_case_db;
  \q
  ```

**2. Setup Backend**
```powershell
cd C:\SaveToExcel\web-app\backend

# สร้าง virtual environment
python -m venv venv
.\venv\Scripts\Activate.ps1

# ติดตั้ง packages
pip install -r requirements.txt

# ตั้งค่า .env
copy .env.example .env
notepad .env
# แก้ไข:
# DATABASE_URL=postgresql://postgres:YOUR_PASSWORD@localhost:5432/criminal_case_db
# SECRET_KEY=your-secret-key-min-32-characters
```

**3. Setup Frontend**
```powershell
# เปิด terminal ใหม่
cd C:\SaveToExcel\web-app\frontend
npm install
```

**4. รันระบบ (ต้องใช้ 2 terminals)**

Terminal 1 - Backend:
```powershell
cd C:\SaveToExcel\web-app\backend
.\venv\Scripts\Activate.ps1
python -m uvicorn app.main:app --reload
```

Terminal 2 - Frontend:
```powershell
cd C:\SaveToExcel\web-app\frontend
npm run dev
```

**5. สร้าง Admin User**
```powershell
# Terminal 3
cd C:\SaveToExcel\web-app\backend
.\venv\Scripts\Activate.ps1
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
print("✅ Admin user created: admin / admin123")
```

กด Ctrl+Z แล้ว Enter เพื่อออก

---

## 🌐 เข้าใช้งาน

1. เปิดเบราว์เซอร์: **http://localhost:3000**
2. Login:
   - Username: **admin**
   - Password: **admin123**

---

## 📚 เอกสารเพิ่มเติม

- **README.md** - ภาพรวมโปรเจค และ features
- **RUN_WITHOUT_DOCKER.md** - คู่มือรันแบบไม่ใช้ Docker (ละเอียด)
- **DEPLOYMENT.md** - คู่มือ deploy production
- **Backend API Docs** - http://localhost:8000/docs

---

## ❓ Troubleshooting

### Docker: "docker compose" not found
ใช้เวอร์ชันใหม่: `docker compose` (มีช่องว่าง)
หรือติดตั้ง Docker Desktop ใหม่

### Backend: Database connection failed
- ตรวจสอบ PostgreSQL รันอยู่
- ตรวจสอบ DATABASE_URL ใน .env ถูกต้อง
- ตรวจสอบ password ถูกต้อง

### Frontend: Can't connect to backend
- ตรวจสอบ Backend รันที่ port 8000
- เข้าดู http://localhost:8000/health
- ตรวจสอบ vite.config.ts proxy settings

### Port already in use
```powershell
# หา process
netstat -ano | findstr :8000
netstat -ano | findstr :3000

# Kill process
taskkill /PID <PID> /F
```

---

## 🎯 Quick Commands

```powershell
# Docker - Start
docker compose up -d

# Docker - Stop
docker compose down

# Docker - View logs
docker compose logs -f backend
docker compose logs -f frontend

# Docker - Restart
docker compose restart

# Non-Docker - Check services
# Backend: http://localhost:8000/health
# Frontend: http://localhost:3000
```

---

## 💡 Tips

- แนะนำใช้ **Docker** เพราะง่ายกว่า
- ถ้าไม่มี Docker ให้ใช้วิธีที่ 2
- ใช้ **VS Code** เป็น editor แนะนำ
- ติดตั้ง Extensions: Python, ESLint, Prettier

---

## 📞 Need Help?

1. ดู logs (Docker): `docker compose logs -f`
2. ดู API docs: http://localhost:8000/docs
3. ตรวจสอบ environment variables ใน .env