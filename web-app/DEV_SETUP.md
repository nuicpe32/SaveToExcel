# 🛠️ Development Setup Guide

## 🎯 สำหรับการพัฒนาต่อเนื่อง (Development Mode)

### ✨ ข้อดีของ Development Mode:
- ✅ **Hot Reload** - แก้โค้ดแล้วเห็นผลทันที (ไม่ต้อง rebuild)
- ✅ **Volume Mount** - แก้ไฟล์ในเครื่องแล้ว container อัปเดตทันที
- ✅ **Fast Iteration** - ทดสอบได้เร็ว ประหยัดเวลา
- ✅ **ข้อมูลไม่หาย** - Database แยกออกมาเป็น volume
- ✅ **ปลอดภัย** - แก้อะไรผิดก็แค่ reload ไม่กระทบข้อมูล

---

## 🚀 การใช้งาน Development Mode

### 1️⃣ เริ่มต้นครั้งแรก

```bash
cd web-app

# สร้าง network และ volumes
docker network create criminal-case-network 2>/dev/null || true

# Start ทุก services
docker-compose -f docker-compose.dev.yml up -d

# ดู logs แบบ real-time
docker-compose -f docker-compose.dev.yml logs -f
```

### 2️⃣ การพัฒนาต่อเนื่อง

#### 🎨 **แก้ไข Frontend** (React/TypeScript)
```bash
# แก้ไฟล์ใน frontend/src/
# เช่น: frontend/src/pages/DashboardPage.tsx

# ✅ ไม่ต้องทำอะไร!
# Vite จะ hot reload อัตโนมัติ
# เปิดเบราว์เซอร์ที่ http://localhost:3001 จะเห็นการเปลี่ยนแปลงทันที
```

#### 🔧 **แก้ไข Backend** (FastAPI/Python)
```bash
# แก้ไฟล์ใน backend/app/
# เช่น: backend/app/api/v1/documents.py

# ✅ ไม่ต้องทำอะไร!
# Uvicorn --reload จะ restart อัตโนมัติ
# API จะพร้อมใช้ภายใน 1-2 วินาที
```

#### 🗄️ **ดูข้อมูลใน Database**
```bash
# ใช้ psql
docker-compose -f docker-compose.dev.yml exec postgres psql -U user -d criminal_case_db

# หรือ DBeaver / pgAdmin (เชื่อมต่อที่ localhost:5432)
```

### 3️⃣ การ Restart Services (เมื่อจำเป็น)

```bash
# Restart เฉพาะ frontend (เมื่อเปลี่ยน dependencies)
docker-compose -f docker-compose.dev.yml restart frontend

# Restart เฉพาะ backend (เมื่อเปลี่ยน dependencies)
docker-compose -f docker-compose.dev.yml restart backend

# Restart ทั้งหมด (ปกติไม่ต้องใช้)
docker-compose -f docker-compose.dev.yml restart
```

### 4️⃣ การ Stop และ Clean Up

```bash
# Stop ทุก services (ข้อมูลยังอยู่)
docker-compose -f docker-compose.dev.yml stop

# Start อีกครั้ง
docker-compose -f docker-compose.dev.yml start

# Remove containers (ข้อมูลยังอยู่ใน volumes)
docker-compose -f docker-compose.dev.yml down

# Remove ทั้ง containers และ volumes (⚠️ ข้อมูลหายหมด!)
docker-compose -f docker-compose.dev.yml down -v
```

---

## 🔄 Workflow การพัฒนาแบบถูกต้อง

### ✅ สำหรับการแก้ไขเล็กน้อย (90% ของเวลา)

```bash
# 1. แก้ไขโค้ด
vim frontend/src/pages/DashboardPage.tsx

# 2. บันทึกไฟล์
# → Hot reload ทำงานอัตโนมัติ ✨

# 3. Refresh browser
# → เห็นการเปลี่ยนแปลงทันที ✨

# ✅ ไม่ต้อง rebuild, ไม่ต้อง restart!
```

### 🔧 สำหรับการเปลี่ยน Dependencies

```bash
# เมื่อเพิ่ม npm package ใหม่
cd frontend
npm install <package-name>

# Rebuild เฉพาะ frontend
docker-compose -f docker-compose.dev.yml build frontend
docker-compose -f docker-compose.dev.yml restart frontend

# เมื่อเพิ่ม pip package ใหม่
# แก้ backend/requirements.txt แล้ว
docker-compose -f docker-compose.dev.yml build backend
docker-compose -f docker-compose.dev.yml restart backend
```

### 💾 สำหรับการ Commit งาน

```bash
# 1. Test ว่าทุกอย่างทำงาน
curl http://localhost:8000/api/v1/criminal-cases/
# เปิด http://localhost:3001 ดูใน browser

# 2. Commit เฉพาะไฟล์ที่เปลี่ยน
git add backend/app/api/v1/documents.py
git add frontend/src/pages/DashboardPage.tsx
git commit -m "feat: add new feature XYZ"

# 3. ✅ ฟังก์ชันเดิมยังอยู่ครบ!
```

---

## 🛡️ การป้องกันฟังก์ชันหาย

### ⛔ อย่าทำ (จะทำให้ฟังก์ชันหาย)
```bash
# ❌ ใช้ docker-compose up -d ตรงๆ (จะ recreate ทุกอย่าง)
docker-compose up -d frontend

# ❌ Remove volumes โดยไม่รู้ตัว
docker-compose down -v
```

### ✅ ทำแทน
```bash
# ✅ ใช้ restart (ปลอดภัย)
docker-compose -f docker-compose.dev.yml restart frontend

# ✅ ใช้ down แบบธรรมดา (เก็บ volumes ไว้)
docker-compose -f docker-compose.dev.yml down
```

---

## 📊 ตรวจสอบสถานะ

```bash
# ดู containers ที่กำลังทำงาน
docker-compose -f docker-compose.dev.yml ps

# ดู logs แบบ real-time
docker-compose -f docker-compose.dev.yml logs -f

# ดู logs เฉพาะ backend
docker-compose -f docker-compose.dev.yml logs -f backend

# ดู logs เฉพาะ frontend
docker-compose -f docker-compose.dev.yml logs -f frontend

# เช็คว่า hot reload ทำงานหรือไม่
docker-compose -f docker-compose.dev.yml logs backend | grep "Reloading"
```

---

## 🎯 Quick Commands (บันทึกไว้ใช้บ่อยๆ)

```bash
# Start development environment
alias dev-start='cd /mnt/c/SaveToExcel/web-app && docker-compose -f docker-compose.dev.yml up -d'

# Stop development environment
alias dev-stop='cd /mnt/c/SaveToExcel/web-app && docker-compose -f docker-compose.dev.yml stop'

# View logs
alias dev-logs='cd /mnt/c/SaveToExcel/web-app && docker-compose -f docker-compose.dev.yml logs -f'

# Restart frontend only
alias dev-restart-fe='cd /mnt/c/SaveToExcel/web-app && docker-compose -f docker-compose.dev.yml restart frontend'

# Restart backend only
alias dev-restart-be='cd /mnt/c/SaveToExcel/web-app && docker-compose -f docker-compose.dev.yml restart backend'

# Check status
alias dev-ps='cd /mnt/c/SaveToExcel/web-app && docker-compose -f docker-compose.dev.yml ps'
```

---

## 🚨 Troubleshooting

### ปัญหา: Frontend ไม่ hot reload
```bash
# 1. เช็คว่า volume mount ถูกต้อง
docker-compose -f docker-compose.dev.yml exec frontend ls -la /app/src

# 2. Restart frontend
docker-compose -f docker-compose.dev.yml restart frontend

# 3. ถ้ายังไม่ได้ ลอง rebuild
docker-compose -f docker-compose.dev.yml build frontend
docker-compose -f docker-compose.dev.yml restart frontend
```

### ปัญหา: Backend ไม่ reload
```bash
# 1. เช็ค logs
docker-compose -f docker-compose.dev.yml logs backend | tail -50

# 2. เช็คว่ามี syntax error หรือไม่
docker-compose -f docker-compose.dev.yml exec backend python -m py_compile /app/app/main.py

# 3. Restart backend
docker-compose -f docker-compose.dev.yml restart backend
```

### ปัญหา: Database connection failed
```bash
# 1. เช็คว่า postgres ทำงานหรือไม่
docker-compose -f docker-compose.dev.yml ps postgres

# 2. เช็ค healthcheck
docker-compose -f docker-compose.dev.yml logs postgres | grep "ready"

# 3. ทดสอบเชื่อมต่อ
docker-compose -f docker-compose.dev.yml exec postgres psql -U user -d criminal_case_db -c "SELECT 1;"
```

---

## 📝 Best Practices

1. **ใช้ dev mode ตลอดเวลาที่พัฒนา** - ประหยัดเวลามาก
2. **Commit งานบ่อยๆ** - ป้องกันสูญหาย
3. **ใช้ restart แทน down/up** - ปลอดภัยกว่า
4. **ดู logs เป็นประจำ** - รู้ว่าเกิดอะไรขึ้น
5. **Test ก่อน commit** - ป้องกัน bug

---

## 🎉 สรุป

**Development Mode = แก้โค้ดแล้วเห็นผลทันที ไม่ต้อง rebuild!**

- Frontend: Hot reload ด้วย Vite ⚡
- Backend: Auto reload ด้วย Uvicorn --reload 🔄
- Database: ข้อมูลถาวรใน volume 💾
- ปลอดภัย: แก้อะไรผิดก็ไม่กระทบของเดิม 🛡️
