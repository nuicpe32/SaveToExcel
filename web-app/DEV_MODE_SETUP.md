# 🚀 Development Mode Setup Guide

## ปัญหาที่พบและวิธีแก้ไข

### ปัญหาเดิม
- Frontend รันแบบ Production Build (ไม่มี Hot Reload)
- ต้องรัน `docker-compose build` ทุกครั้งที่แก้ไขโค้ด
- Development workflow ช้า ไม่เหมาะกับการพัฒนา

### วิธีแก้ไข
สร้าง **Development Configuration** แยกจาก Production โดยมี:
- Frontend รันด้วย Vite Dev Server (Hot Reload)
- Backend รันด้วย Uvicorn reload mode
- Volume mounting สำหรับ live code update

---

## 📋 ข้อกำหนดเบื้องต้น

- **Docker Desktop** รันอยู่
- **Node.js 18+** ติดตั้งแล้ว
- **Git** สำหรับ pull โค้ด

---

## 🎯 Quick Start - Development Mode

### วิธีที่ 1: ใช้ Script (แนะนำ)

```powershell
# เข้าไปที่โฟลเดอร์ web-app
cd web-app

# รัน Development Mode
.\start-dev-improved.ps1
```

**สิ่งที่ script จะทำ:**
1. ✅ ตรวจสอบ Docker
2. ✅ หยุด Production containers (ถ้ามี)
3. ✅ สร้าง Backend services (PostgreSQL + Redis + Backend API)
4. ✅ รอให้ Backend พร้อม
5. ✅ ติดตั้ง Frontend dependencies
6. ✅ เปิด Vite Dev Server

### วิธีที่ 2: รันเอง (Manual)

```powershell
# 1. เข้าโฟลเดอร์
cd web-app

# 2. สร้าง Backend services
docker-compose -f docker-compose.dev.yml up -d

# 3. รอให้ Backend พร้อม (ประมาณ 10 วินาที)
Start-Sleep -Seconds 10

# 4. เปิด Terminal ใหม่ แล้วรัน Frontend
cd frontend
npm install
npm run dev
```

---

## 🌐 URLs สำหรับ Development

| Service | URL | คำอธิบาย |
|---------|-----|----------|
| **Frontend (Vite)** | http://localhost:5173 | Vite Dev Server พร้อม Hot Reload |
| **Backend API** | http://localhost:8000 | FastAPI with auto-reload |
| **API Docs (Swagger)** | http://localhost:8000/docs | Interactive API Documentation |
| **API Docs (ReDoc)** | http://localhost:8000/redoc | Alternative API Docs |
| **Database** | localhost:5432 | PostgreSQL |
| **Redis** | localhost:6379 | Redis Cache |

---

## ✨ ฟีเจอร์ Development Mode

### 🔥 Hot Reload
- **Frontend:** แก้ไขโค้ด `.tsx`, `.ts`, `.css` → เห็นผลทันที
- **Backend:** แก้ไขโค้ด `.py` → Server รีสตาร์ทอัตโนมัติ

### 🐛 Debugging
- **Frontend:** ใช้ React DevTools, Browser Console
- **Backend:** ดู Logs ได้จาก Docker: `docker-compose -f docker-compose.dev.yml logs -f backend`

### 📦 Volume Mounting
- Backend code mounted → แก้ไขเห็นผลทันที
- Frontend รันจาก local → สามารถแก้ไขได้เลย

---

## 🛠️ การใช้งาน

### เริ่มต้น Development

```powershell
# วิธีแนะนำ
.\start-dev-improved.ps1

# หรือ
docker-compose -f docker-compose.dev.yml up -d
cd frontend && npm run dev
```

### หยุด Development

```powershell
# กด Ctrl+C ที่ Terminal ของ Frontend

# จากนั้นหยุด Backend
.\stop-dev-improved.ps1

# หรือ
docker-compose -f docker-compose.dev.yml stop
```

### ดู Logs

```powershell
# Logs ทั้งหมด
docker-compose -f docker-compose.dev.yml logs -f

# Logs เฉพาะ Backend
docker-compose -f docker-compose.dev.yml logs -f backend

# Logs เฉพาะ Database
docker-compose -f docker-compose.dev.yml logs -f postgres
```

### รีสตาร์ท Service

```powershell
# รีสตาร์ท Backend
docker-compose -f docker-compose.dev.yml restart backend

# รีสตาร์ท Database
docker-compose -f docker-compose.dev.yml restart postgres
```

### ลบ Containers และ Volumes

```powershell
# หยุดและลบ containers
docker-compose -f docker-compose.dev.yml down

# ลบทั้ง containers และ volumes (ระวัง: จะลบข้อมูลในฐานข้อมูล!)
docker-compose -f docker-compose.dev.yml down -v
```

---

## 🔧 Configuration Files

### Development Files
- `docker-compose.dev.yml` - Docker configuration สำหรับ Dev
- `start-dev-improved.ps1` - Script เริ่มต้น Development
- `stop-dev-improved.ps1` - Script หยุด Development

### Production Files (ใช้แยก)
- `docker-compose.yml` - Production configuration
- Frontend build เป็น static files

---

## 📚 Workflow แนะนำ

### 1. เริ่มวันทำงาน
```powershell
cd web-app
.\start-dev-improved.ps1
```

### 2. พัฒนาโค้ด
- แก้ไข Frontend: `frontend/src/**`
- แก้ไข Backend: `backend/app/**`
- เห็นผลทันทีโดยไม่ต้อง rebuild

### 3. ทดสอบ
- Frontend: เปิด http://localhost:5173
- Backend API: http://localhost:8000/docs

### 4. จบวันทำงาน
```powershell
# กด Ctrl+C ที่ Frontend Terminal
# จากนั้นรัน
.\stop-dev-improved.ps1
```

---

## 🐛 Troubleshooting

### ปัญหา: Port ถูกใช้งานแล้ว

**อาการ:** Error: Port 5173, 8000, 5432 already in use

**วิธีแก้:**
```powershell
# ตรวจสอบ port ที่ใช้
netstat -ano | findstr :5173
netstat -ano | findstr :8000

# หยุด production containers
docker-compose down

# รีสตาร์ท dev mode
.\start-dev-improved.ps1
```

### ปัญหา: Frontend ไม่เชื่อมต่อ Backend

**อาการ:** Network Error, CORS Error

**วิธีแก้:**
1. ตรวจสอบ Backend รันอยู่: http://localhost:8000/health
2. ตรวจสอบ CORS ใน `backend/app/core/config.py`
3. Restart Frontend: กด Ctrl+C แล้ว `npm run dev` ใหม่

### ปัญหา: Database connection failed

**วิธีแก้:**
```powershell
# ตรวจสอบ PostgreSQL
docker-compose -f docker-compose.dev.yml ps postgres

# ดู logs
docker-compose -f docker-compose.dev.yml logs postgres

# รีสตาร์ท
docker-compose -f docker-compose.dev.yml restart postgres
```

### ปัญหา: Hot Reload ไม่ทำงาน

**วิธีแก้:**
- **Frontend:** ลอง hard refresh (Ctrl+Shift+R) หรือ clear cache
- **Backend:** ตรวจสอบว่า volume mounting ถูกต้อง

---

## ⚡ Performance Tips

### 1. WSL2 สำหรับ Windows
ใช้ WSL2 แทน Hyper-V จะได้ performance ดีกว่า

### 2. Exclude node_modules จาก Antivirus
เพิ่ม `web-app/frontend/node_modules` ใน exclusion list

### 3. Docker Resource Limits
เปิด Docker Desktop → Settings → Resources
- CPU: อย่างน้อย 4 cores
- Memory: อย่างน้อย 4GB

---

## 🎓 เปรียบเทียบ Development vs Production

| Feature | Development | Production |
|---------|-------------|------------|
| **Frontend** | Vite Dev Server (5173) | Nginx Static (3001) |
| **Hot Reload** | ✅ Yes | ❌ No |
| **Build Time** | ⚡ Fast | 🐢 Slower |
| **Source Maps** | ✅ Yes | ❌ No |
| **Minification** | ❌ No | ✅ Yes |
| **Performance** | Debug Mode | Optimized |

---

## 📖 เอกสารเพิ่มเติม

- [QUICK_START_GUIDE.md](./QUICK_START_GUIDE.md) - คู่มือเริ่มต้นรวม
- [DEPLOYMENT.md](./DEPLOYMENT.md) - คู่มือ Deploy Production
- [README.md](./README.md) - ข้อมูลโปรเจคทั่วไป

---

## ✅ Checklist สำหรับ Developer

- [ ] Docker Desktop รันอยู่
- [ ] Node.js ติดตั้งแล้ว (version 18+)
- [ ] Port 5173, 8000, 5432 ว่าง
- [ ] รัน `.\start-dev-improved.ps1`
- [ ] เปิดเบราว์เซอร์ไปที่ http://localhost:5173
- [ ] Login ด้วย admin/admin123
- [ ] เริ่มพัฒนาได้เลย! 🚀

---

**เวอร์ชัน:** 1.0  
**อัปเดตล่าสุด:** October 1, 2025  
**สถานะ:** ✅ Ready for Development


