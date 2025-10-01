# 🚀 Development Environment Status

**วันที่:** 1 ตุลาคม 2568 เวลา 13:48 น.  
**โหมด:** Development Mode ✅  
**สถานะ:** พร้อมใช้งาน

---

## ✅ Services ที่กำลังรัน

| Service | Status | URL | หมายเหตุ |
|---------|--------|-----|----------|
| **Frontend Dev** | ✅ Running | http://localhost:5173 | Vite Dev Server (Hot Reload) |
| **Backend API** | ✅ Running | http://localhost:8000 | FastAPI |
| **API Docs** | ✅ Running | http://localhost:8000/docs | Swagger UI |
| **PostgreSQL** | ✅ Healthy | localhost:5432 | Database |
| **Redis** | ✅ Healthy | localhost:6379 | Cache |
| **Adminer** | ✅ Running | http://localhost:8080 | DB Admin Tool |
| **pgAdmin** | ✅ Running | http://localhost:5050 | DB Admin Tool |

---

## 🎯 ใช้งานอย่างไร?

### 1. เปิด Browser
```
http://localhost:5173
```

### 2. Login
```
Username: admin
Password: admin123
```

### 3. เริ่มพัฒนา!

**แก้ไขไฟล์:**
```
web-app/frontend/src/
├── pages/              ← แก้ไขหน้าเว็บต่างๆ
├── components/         ← แก้ไข components
├── services/           ← แก้ไข API calls
└── stores/             ← แก้ไข state management
```

**เมื่อแก้ไข:**
1. แก้ไขไฟล์ `.tsx` หรือ `.ts`
2. บันทึก (Ctrl+S)
3. ดูที่ Browser → เห็นผลทันที! ⚡

**ไม่ต้อง:**
- ❌ Rebuild
- ❌ Restart container
- ❌ Refresh browser (Hot Reload ทำให้อัตโนมัติ)

---

## 💡 Features ของ Development Mode

### ✅ Hot Module Replacement (HMR)
- แก้ไข React components → Update ทันที
- ไม่ต้อง refresh page
- State ยังคงอยู่

### ✅ Fast Refresh
- แก้ไข function/component → เห็นผลใน < 1 วินาที
- ไม่สูญเสีย component state

### ✅ Error Overlay
- เกิด error → แสดงใน browser ทันที
- บอก file และ line number
- แก้ไข error → error หายทันที

### ✅ Source Maps
- Debug ง่าย ใน browser DevTools
- เห็นโค้ดจริง ไม่ใช่โค้ดที่ถูก compile

---

## 🔧 คำสั่งที่ใช้บ่อย

### ดู Logs
```powershell
# Backend logs
docker-compose logs -f backend

# Frontend logs (ดูใน PowerShell window ที่เปิดไว้)
```

### Restart Services
```powershell
# Restart backend
docker-compose restart backend

# Restart frontend (กด Ctrl+C แล้วรันใหม่)
npm run dev
```

### หยุด Development
```powershell
# หยุด frontend (ใน PowerShell window)
Ctrl+C

# หยุด backend services
cd C:\SaveToExcel\web-app
docker-compose stop

# หรือใช้ script
.\stop-dev.ps1
```

### เริ่มใหม่
```powershell
.\start-dev.ps1
```

---

## 📁 โครงสร้าง Project

```
web-app/
├── backend/                 # FastAPI Backend (Docker)
│   └── app/
│       ├── api/v1/         # API endpoints
│       ├── models/         # Database models
│       └── schemas/        # Pydantic schemas
│
├── frontend/                # React Frontend (Local Dev)
│   ├── src/
│   │   ├── pages/          # ← แก้ไขหน้าต่างๆ ที่นี่
│   │   ├── components/     # ← แก้ไข components ที่นี่
│   │   ├── services/       # API services
│   │   └── stores/         # State management
│   │
│   ├── package.json
│   └── vite.config.ts      # Vite configuration
│
├── start-dev.ps1           # Start development
├── stop-dev.ps1            # Stop development
└── docker-compose.yml      # Backend services config
```

---

## 🎨 ตัวอย่างการแก้ไข

### Example 1: แก้ไขข้อความในหน้า Dashboard

**ไฟล์:** `frontend/src/pages/DashboardPage.tsx`

```typescript
// แก้ไขบรรทัดที่ต้องการ
<h1>Dashboard - ระบบจัดการคดีอาญา</h1>

// เปลี่ยนเป็น
<h1>แดชบอร์ด - Criminal Case Management</h1>

// บันทึก → เห็นผลทันที!
```

### Example 2: เพิ่ม Button ใหม่

```typescript
<Button 
  type="primary" 
  onClick={() => console.log('Clicked!')}
>
  ปุ่มใหม่
</Button>

// บันทึก → ปุ่มปรากฏใน browser ทันที!
```

### Example 3: แก้ไข Style

```typescript
<div style={{ 
  backgroundColor: '#f0f0f0',  // เปลี่ยนสี
  padding: '20px'              // เพิ่ม padding
}}>
  Content here
</div>

// บันทึก → Style เปลี่ยนทันที!
```

---

## ⚡ Performance Tips

### 1. เปิด DevTools (F12)
```
- ดู Console สำหรับ errors/warnings
- ดู Network tab สำหรับ API calls
- ดู React DevTools สำหรับ component state
```

### 2. ใช้ VS Code Extensions
```
- ESLint: ตรวจสอบโค้ด
- Prettier: Format โค้ด
- TypeScript: Type checking
- React DevTools: Debug React
```

### 3. Hot Reload ช้า?
```powershell
# ใน vite.config.ts เพิ่ม:
server: {
  watch: {
    usePolling: true,  # สำหรับ Windows
  },
}
```

---

## 🐛 Troubleshooting

### Port 5173 ถูกใช้งาน?
```powershell
# หา process
netstat -ano | findstr :5173

# Kill process (เปลี่ยน PID)
taskkill /PID <PID> /F
```

### Backend ไม่ตอบสนอง?
```powershell
# Restart backend
docker-compose restart backend

# ดู logs
docker-compose logs -f backend
```

### Hot Reload ไม่ทำงาน?
```powershell
# ลอง restart Vite dev server
Ctrl+C
npm run dev
```

### เห็น CORS Error?
```
ตรวจสอบว่า Backend config ถูกต้อง
ไฟล์: backend/app/core/config.py
CORS_ORIGINS ต้องมี http://localhost:5173
```

---

## 📊 เปรียบเทียบกับ Production Mode

| | Dev Mode (5173) | Production (3001) |
|---|:---:|:---:|
| Hot Reload | ✅ | ❌ |
| Fast Refresh | ✅ | ❌ |
| Error Overlay | ✅ | ❌ |
| Source Maps | ✅ | ❌ |
| Build Time | 0 วินาที | 7 วินาที |
| Update Time | < 1 วินาที | 10-15 วินาที |
| ใช้เมื่อ | พัฒนา | ทดสอบ/Deploy |

---

## ✨ Next Steps

### ระหว่างพัฒนา:
1. ✅ แก้ไขโค้ดได้เลย ไม่ต้องกังวล
2. ✅ บันทึกบ่อยๆ เห็นผลทันที
3. ✅ Commit เป็นระยะ (Git)
4. ✅ ทดสอบทุก feature ที่แก้ไข

### เมื่อพัฒนาเสร็จ:
1. ทดสอบใน Production Mode:
   ```powershell
   docker-compose build frontend
   docker-compose up -d frontend
   http://localhost:3001
   ```

2. Deploy:
   ```powershell
   # Push to Git
   git add .
   git commit -m "Feature: ..."
   git push
   ```

---

## 📞 ช่วยเหลือ

### มีปัญหา?
1. ดู logs ใน PowerShell window (Frontend)
2. ดู `docker-compose logs backend` (Backend)
3. ดู Browser Console (F12)
4. ดู error overlay ใน browser

### ต้องการความช่วยเหลือ?
- อ่าน: `DEV_MODE_GUIDE.md`
- อ่าน: `QUICK_DEV_GUIDE.md`
- อ่าน: `README.md`

---

## 🎉 สรุป

**ตอนนี้คุณกำลังใช้:**
- ✅ Development Mode (Hot Reload)
- ✅ Frontend: http://localhost:5173
- ✅ Backend: http://localhost:8000
- ✅ พร้อมพัฒนาได้เลย!

**จำไว้:**
- แก้ไข → บันทึก → เห็นผล ⚡
- ไม่ต้อง rebuild!
- ไม่ต้อง restart!
- แค่แก้ไขและบันทึก!

---

**Happy Coding!** 🚀

*Status: Active Development Mode*  
*Updated: 1 ตุลาคม 2568, 13:48:01 +07:00*

