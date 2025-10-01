# 🚀 Development Mode Guide - การพัฒนาแบบไม่ต้อง Rebuild

**สำหรับ:** การพัฒนาและแก้ไขโค้ด Frontend  
**วันที่:** 1 ตุลาคม 2568

---

## ❌ ปัญหาของ Production Mode

เมื่อรัน Frontend ใน Docker (`http://localhost:3001`):
- ต้อง **rebuild ทุกครั้ง** ที่แก้ไขโค้ด
- ใช้เวลา build ~7 วินาที/ครั้ง
- ไม่มี Hot Reload (ไม่เห็นการเปลี่ยนแปลงทันที)
- **เสียเวลา** มากในการพัฒนา

---

## ✅ วิธีแก้: ใช้ Development Mode

## วิธีที่ 1: รัน Frontend แบบ Local (แนะนำ!)

### ขั้นตอน:

#### 1. หยุด Frontend Container
```powershell
cd C:\SaveToExcel\web-app
docker-compose stop frontend
```

#### 2. รัน Frontend แบบ Dev Mode
```powershell
# เปิด Terminal/PowerShell ใหม่
cd C:\SaveToExcel\web-app\frontend

# Install dependencies (ครั้งแรกเท่านั้น)
npm install

# รัน dev server
npm run dev
```

#### 3. เปิด Browser
```
http://localhost:5173
```

### ผลลัพธ์:
- ✅ **Hot Reload**: แก้ไขโค้ด → บันทึก → เห็นผลทันที (ไม่ต้อง refresh)
- ✅ **Fast Refresh**: React components update แบบ instant
- ✅ **ไม่ต้อง rebuild**: ประหยัดเวลามหาศาล
- ✅ **Error Display**: เห็น error ชัดเจนใน browser

### โครงสร้างการรัน:
```
Backend (Docker):  http://localhost:8000  ✅
Frontend (Local):  http://localhost:5173  ✅
Database (Docker): localhost:5432         ✅
```

---

## วิธีที่ 2: Docker Compose Dev Mode

สร้าง `docker-compose.dev.yml` สำหรับ development

### ขั้นตอน:

#### 1. สร้างไฟล์ docker-compose.dev.yml
```yaml
version: '3.8'

services:
  frontend-dev:
    build:
      context: ./frontend
      dockerfile: Dockerfile.dev
    container_name: criminal-case-frontend-dev
    ports:
      - "5173:5173"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    environment:
      - CHOKIDAR_USEPOLLING=true
    command: npm run dev -- --host 0.0.0.0
    depends_on:
      - backend
```

#### 2. รัน Dev Mode
```powershell
docker-compose -f docker-compose.dev.yml up -d frontend-dev
```

---

## 📊 เปรียบเทียบ

| | Production Mode | Development Mode |
|---|---|---|
| **Port** | 3001 | 5173 |
| **Server** | Nginx | Vite Dev Server |
| **Hot Reload** | ❌ ไม่มี | ✅ มี |
| **Rebuild** | ✅ ต้อง rebuild | ❌ ไม่ต้อง |
| **เวลา/การแก้ไข** | ~10 วินาที | ~1 วินาที |
| **ใช้สำหรับ** | Testing, Production | Development |

---

## 🎯 Workflow ที่แนะนำ

### สำหรับ Development (ทำงานทุกวัน):

```powershell
# Terminal 1: Backend (Docker)
docker-compose up -d postgres redis backend

# Terminal 2: Frontend (Local)
cd frontend
npm run dev

# Browser
http://localhost:5173
```

**แก้ไขโค้ด:**
1. แก้ไฟล์ `.tsx` หรือ `.ts`
2. บันทึก (Ctrl+S)
3. เห็นผลทันที ✅ (ไม่ต้อง rebuild!)

---

### สำหรับ Testing (ทดสอบ Production):

```powershell
# Build และ Deploy Production
docker-compose build frontend
docker-compose up -d frontend

# Browser
http://localhost:3001
```

---

## 🔧 Setup แนะนำ (ครั้งแรก)

### 1. ติดตั้ง Dependencies
```powershell
cd C:\SaveToExcel\web-app\frontend
npm install
```

### 2. สร้าง Script สำหรับ Dev Mode

**สร้างไฟล์:** `start-dev.ps1`
```powershell
# Start Development Environment
Write-Host "Starting Development Environment..." -ForegroundColor Green

# Start Backend Services (Docker)
Write-Host "Starting Backend Services..." -ForegroundColor Yellow
docker-compose up -d postgres redis backend

# Wait for services
Write-Host "Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Start Frontend Dev Server (Local)
Write-Host "Starting Frontend Dev Server..." -ForegroundColor Yellow
cd frontend
npm run dev
```

### 3. รัน Dev Mode ง่ายๆ
```powershell
.\start-dev.ps1
```

---

## 🐛 Troubleshooting

### ปัญหา: Port 5173 ถูกใช้งาน

**แก้ไข:**
```powershell
# ค้นหา process ที่ใช้ port 5173
netstat -ano | findstr :5173

# Kill process (เปลี่ยน PID)
taskkill /PID <PID> /F
```

### ปัญหา: CORS Error

**แก้ไข:** ตรวจสอบ `frontend/vite.config.ts`
```typescript
export default defineConfig({
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

### ปัญหา: Hot Reload ไม่ทำงาน

**แก้ไข:**
```powershell
# ใน frontend/vite.config.ts
export default defineConfig({
  server: {
    watch: {
      usePolling: true,  // เพิ่มบรรทัดนี้
    },
  },
})
```

---

## 📝 สรุป

### สำหรับ Development (ทุกวัน):
```
✅ ใช้ npm run dev (Port 5173)
✅ Hot Reload ทำงานอัตโนมัติ
✅ ไม่ต้อง rebuild
✅ ประหยัดเวลามหาศาล
```

### สำหรับ Production/Testing:
```
✅ ใช้ docker-compose (Port 3001)
✅ ทดสอบ Production Build
✅ เหมาะกับ Deployment
```

---

## 🎓 เคล็ดลับ

1. **แก้ไข + บันทึก = เห็นผลทันที** (ไม่ต้องรอ rebuild)
2. **เปิด Dev Tools** (F12) เพื่อดู errors ชัดเจน
3. **ใช้ VS Code** + Extensions (ESLint, Prettier)
4. **Git commit บ่อยๆ** ก่อนแก้ไขใหญ่

---

**จำไว้:**
- Development Mode (5173) = พัฒนา ✅
- Production Mode (3001) = ทดสอบ & Deploy ✅

**อย่าใช้ Production Mode ในการพัฒนา!** มันเสียเวลามาก!

---

**Updated:** 1 ตุลาคม 2568

