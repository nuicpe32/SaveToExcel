# ระบบจัดการคดีอาญา - Web Application v3.0.1

## ⚠️ สำคัญ: โปรเจคนี้ใช้งาน DEV MODE เป็นหลัก

**🔧 Development Mode เป็นโหมดหลักในการใช้งาน** (อัพเดทเมื่อ 1 ต.ค. 2025)

เนื่องจากระบบมีการพัฒนาต่อเนื่องและต้องการความยืดหยุ่นในการแก้ไข โปรเจคนี้จึงตั้งค่าให้ **ใช้งาน Development Mode เป็นหลัก** แทน Production Mode

### 🚀 วิธีเริ่มต้นใช้งาน (Quick Start)

```bash
cd /mnt/c/SaveToExcel/web-app
docker-compose -f docker-compose.dev.yml up -d
```

**URLs:**
- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

**Login:**
- Username: `admin`
- Password: `admin123`

**หยุดระบบ:**
```bash
docker-compose -f docker-compose.dev.yml down
```

### 📦 Docker Volumes & Containers

**⚠️ สำคัญมาก:** โปรเจคนี้ใช้ Development Volumes ต่อไปนี้เป็นหลัก:

| Volume Name | Description | Status |
|------------|-------------|--------|
| `criminal-case-postgres-dev` | ฐานข้อมูลหลัก (DEV) | ✅ **ใช้งานอยู่** |
| `criminal-case-uploads-dev` | ไฟล์อัพโหลด (DEV) | ✅ **ใช้งานอยู่** |
| `web-app_postgres_data` | ฐานข้อมูลเก่า (Production) | ⚠️ ไม่ได้ใช้แล้ว |

**Container Names:**
- `criminal-case-db-dev` (PostgreSQL)
- `criminal-case-redis-dev` (Redis)
- `criminal-case-backend-dev` (FastAPI)
- `criminal-case-frontend-dev` (React)

### 🔄 กรณีข้อมูลหาย (Volume Recovery)

หากมีการใช้ volume ผิดและข้อมูลหาย ให้ใช้ backup file:
```bash
# ใช้ backup ล่าสุด (อยู่ใน /mnt/c/SaveToExcel/web-app/)
docker cp backup_database_YYYYMMDD_HHMMSS.dump criminal-case-db-dev:/tmp/restore.dump
docker exec criminal-case-db-dev pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

📖 ดูรายละเอียดใน [BACKUP_RESTORE_GUIDE.md](./BACKUP_RESTORE_GUIDE.md)

---

## 🎯 ภาพรวมโปรเจค

เวอร์ชัน Web Application ของระบบจัดการคดีอาญา พัฒนาจาก Desktop Application (v2.9.0) เป็น Full-Stack Web Application ที่รองรับการใช้งานแบบ Multi-user พร้อม Centralized Database

### เทคโนโลยีที่ใช้

**Backend:**
- FastAPI (Python Web Framework)
- PostgreSQL (Database)
- SQLAlchemy (ORM)
- Redis (Cache)
- python-docx (Document Generation)

**Frontend:**
- React 18 + TypeScript
- Ant Design (UI Framework)
- React Router (Routing)
- Zustand (State Management)
- TanStack Query (Data Fetching)

**Infrastructure:**
- Docker & Docker Compose
- Nginx (Reverse Proxy)

## 📦 โครงสร้างโปรเจค

```
web-app/
├── backend/
│   ├── app/
│   │   ├── api/v1/          # API Endpoints
│   │   ├── core/            # Core config, database, security
│   │   ├── models/          # SQLAlchemy models
│   │   ├── schemas/         # Pydantic schemas
│   │   ├── services/        # Business logic
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/      # React components
│   │   ├── pages/           # Page components
│   │   ├── services/        # API services
│   │   ├── stores/          # Zustand stores
│   │   └── App.tsx
│   ├── package.json
│   ├── Dockerfile
│   └── nginx.conf
└── docker-compose.yml
```

## 🚀 การติดตั้งและรันโปรเจค

### 🎨 โหมดการใช้งาน

โปรเจคนี้รองรับ 2 โหมด:

| โหมด | คำอธิบาย | เหมาะสำหรับ | Port |
|------|---------|-------------|------|
| **🔧 Development** | Hot Reload, Debug Mode | พัฒนา/ดีบัก | 5173 |
| **🚀 Production** | Optimized, Static Build | ใช้งานจริง | 3001 |

---

### 🔧 Development Mode (สำหรับ Developer)

**✨ แก้ไขใหม่! พร้อม Hot Reload**

```powershell
# เข้าโฟลเดอร์
cd web-app

# รัน Development Mode
.\start-dev-improved.ps1
```

**ฟีเจอร์:**
- ✅ Frontend Hot Reload (Vite Dev Server)
- ✅ Backend Auto-reload (Uvicorn)
- ✅ เห็นผลการแก้ไขทันที
- ✅ Debug Mode เปิดอยู่
- ✅ Source Maps

**URLs:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

**หยุด Development:**
```powershell
# กด Ctrl+C ที่ Frontend Terminal
.\stop-dev-improved.ps1
```

📖 **เอกสารเต็ม:** [DEV_MODE_SETUP.md](./DEV_MODE_SETUP.md)

---

### 🚀 Production Mode

### 🎯 วิธีติดตั้งแบบเร็ว (Quick Setup)

**ใช้ Setup Script (แนะนำ!):**

```bash
cd /mnt/c/SaveToExcel/web-app

# รัน setup script
./setup.sh

# หรือถ้าไม่ work ให้ใช้:
bash setup.sh
```

Script จะช่วย:
- ✅ ตรวจสอบ prerequisites
- ✅ สร้าง .env files
- ✅ ติดตั้ง dependencies
- ✅ เริ่มระบบด้วย Docker
- ✅ สร้าง Admin user

---

### 📋 ข้อกำหนดเบื้องต้น

**สำหรับ Docker (แนะนำ):**
- Docker Desktop (Windows/Mac) หรือ Docker Engine (Linux)
- Docker Compose
- Git

**สำหรับ Development Mode:**
- Node.js 18+
- Python 3.10+
- PostgreSQL 15+
- Redis 7+
- Git

---

### 🐳 วิธีที่ 1: รันด้วย Docker Compose (แนะนำ)

#### 1. Clone โปรเจค
```bash
cd /mnt/c/SaveToExcel/web-app
```

#### 2. ตั้งค่า Environment Variables
```bash
cd backend
cp .env.example .env

# แก้ไขไฟล์ .env (สำคัญ!)
# เปลี่ยน SECRET_KEY เป็นค่าที่ปลอดภัย
nano .env  # หรือใช้ editor ที่ชอบ
```

#### 3. รันด้วย Docker Compose
```bash
cd ..
docker-compose up -d --build
```

#### 4. เข้าถึงระบบ
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Alternative Docs:** http://localhost:8000/redoc

#### 5. สร้าง Admin User
```bash
docker-compose exec backend python create_admin.py
```

Default credentials:
- Username: `admin`
- Password: `admin123`

#### 6. Migration ข้อมูล (Optional)
```bash
docker-compose exec backend python migrate_data.py --init --all
```

---

### 💻 วิธีที่ 2: รันแบบ Development Mode

#### Backend Setup

```bash
cd backend

# สร้าง virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# ติดตั้ง dependencies
pip install -r requirements.txt

# ตั้งค่า environment
cp .env.example .env
nano .env  # แก้ไข DATABASE_URL, SECRET_KEY, etc.

# สร้างตารางในฐานข้อมูล
python init_db.py

# สร้าง Admin user
python create_admin.py

# รัน development server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend จะรันที่: http://localhost:8000

#### Frontend Setup

เปิด terminal ใหม่:

```bash
cd frontend

# ติดตั้ง dependencies
npm install

# รัน development server
npm run dev
```

Frontend จะรันที่: http://localhost:5173 (Vite) หรือ http://localhost:3000

**หมายเหตุ:** ต้องมี PostgreSQL และ Redis รันอยู่แล้ว หรือใช้:
```bash
docker-compose up -d postgres redis
```

---

## 📊 Data Migration จาก Excel → PostgreSQL

### Migration ด้วย Docker

```bash
# เข้าไปใน backend container
docker-compose exec backend bash

# สร้างตารางก่อน
python migrate_data.py --init

# ย้ายข้อมูลทั้งหมด
python migrate_data.py --all

# หรือย้ายทีละโมดูล
python migrate_data.py --banks      # บัญชีธนาคาร
python migrate_data.py --suspects   # หมายเรียกผู้ต้องหา
python migrate_data.py --cases      # คดีอาญา
python migrate_data.py --arrests    # หลังการจับกุม

# ออกจาก container
exit
```

### Migration แบบ Local

```bash
cd backend
source venv/bin/activate

# ย้ายข้อมูลทั้งหมด
python migrate_data.py --init --all

# ระบุ path ของ Excel files (ถ้าอยู่คนละที่)
python migrate_data.py --all --excel-dir /path/to/Xlsx
```

### ตัวเลือกเพิ่มเติม

```bash
# ดูวิธีใช้งาน
python migrate_data.py --help

# Migration แบบเฉพาะเจาะจง
python migrate_data.py --banks --suspects
python migrate_data.py --cases --arrests
```

---

## 🔐 Authentication & Users

### สร้าง Admin User

**ด้วย Docker:**
```bash
docker-compose exec backend python create_admin.py
```

**แบบ Local:**
```bash
cd backend
python create_admin.py
```

**Default Admin:**
- Username: `admin`
- Password: `admin123`
- Role: Administrator

⚠️ **สำคัญ:** เปลี่ยนรหัสผ่านทันทีหลังเข้าระบบครั้งแรก!

### User Management

ระบบใช้ **JWT-based authentication** พร้อม:
- Password hashing (bcrypt)
- Token expiration (30 นาที default)
- Role-based access control
- Refresh token support (planned)

## 🎨 Features

### 5 Modules หลัก

1. **แดชบอร์ด** - สถิติและภาพรวมระบบ
2. **บัญชีธนาคาร** - จัดการข้อมูลบัญชีธนาคาร + สร้างเอกสาร
3. **หมายเรียกผู้ต้องหา** - จัดการหมายเรียก + สร้างเอกสาร
4. **คดีอาญา** - ติดตามคดี + รายงาน
5. **หลังจับกุม** - กระบวนการหลังจับกุม

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /api/v1/auth/register | ลงทะเบียนผู้ใช้ |
| POST | /api/v1/auth/login | เข้าสู่ระบบ |
| GET | /api/v1/auth/me | ข้อมูลผู้ใช้ปัจจุบัน |
| GET/POST | /api/v1/bank-accounts | CRUD บัญชีธนาคาร |
| GET/POST | /api/v1/suspects | CRUD ผู้ต้องหา |
| GET/POST | /api/v1/criminal-cases | CRUD คดีอาญา |
| GET/POST | /api/v1/post-arrests | CRUD หลังจับกุม |
| GET | /api/v1/documents/* | สร้างเอกสาร Word |

## 🔧 Configuration

### Backend Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/criminal_case_db
REDIS_URL=redis://localhost:6379/0
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

### Frontend Configuration

แก้ไขใน `frontend/vite.config.ts` สำหรับ proxy settings

## 📱 Responsive Design

Frontend รองรับการใช้งานบน:
- Desktop (1920x1080+)
- Tablet (768x1024)
- Mobile (375x667+)

## 🔒 Security Features

- JWT Authentication
- Password Hashing (bcrypt)
- CORS Protection
- SQL Injection Prevention (SQLAlchemy ORM)
- XSS Protection (React built-in)

## 🚢 Deployment

### Production Deployment

1. **Update environment variables**
```bash
# เปลี่ยน SECRET_KEY
# เปลี่ยน Database credentials
# ตั้งค่า CORS_ORIGINS
```

2. **Build & Deploy**
```bash
docker-compose -f docker-compose.prod.yml up -d --build
```

3. **Setup Nginx (Reverse Proxy)**
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        proxy_pass http://localhost:3000;
    }

    location /api {
        proxy_pass http://localhost:8000;
    }
}
```

## 📖 API Documentation

เข้าถึง Swagger UI ได้ที่: http://localhost:8000/docs

## 🧪 Testing

```bash
# Backend tests
cd backend
pytest

# Frontend tests
cd frontend
npm run test
```

## 🐛 Troubleshooting

### Database Connection Failed
```bash
docker-compose logs postgres
# ตรวจสอบว่า PostgreSQL รันอยู่หรือไม่
```

### Frontend ไม่เชื่อมต่อ Backend
- ตรวจสอบ CORS settings ใน `backend/app/core/config.py`
- ตรวจสอบ proxy settings ใน `frontend/vite.config.ts`

### Port Already in Use
```bash
# เปลี่ยน port ใน docker-compose.yml
ports:
  - "3001:80"  # เปลี่ยนจาก 3000 เป็น 3001
```

## 📞 Support

หากพบปัญหาหรือต้องการความช่วยเหลือ:
- ดู logs: `docker-compose logs -f`
- ตรวจสอบ API docs: http://localhost:8000/docs

## 📝 License

โปรเจคนี้พัฒนาเพื่อใช้งานภายในองค์กร

## 🎯 Roadmap v3.1.0

- [ ] Real-time notifications (WebSocket)
- [ ] Advanced reporting (PDF/Excel export)
- [ ] Mobile application (React Native)
- [ ] Role-based dashboard customization
- [ ] Audit logging system
- [ ] Backup & restore functionality