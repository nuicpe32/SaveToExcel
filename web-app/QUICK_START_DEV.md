# 🚀 Quick Start - Development Mode

## ⚡ ใช้งานง่ายด้วย Helper Script

### 📋 คำสั่งพื้นฐาน (ใช้บ่อยที่สุด)

```bash
cd /mnt/c/SaveToExcel/web-app

# เริ่มต้นใช้งาน
./dev.sh start

# ดู logs แบบ real-time
./dev.sh logs

# ดูสถานะ
./dev.sh ps

# หยุดการทำงาน
./dev.sh stop
```

---

## 🎯 Use Cases ที่พบบ่อย

### 1️⃣ เริ่มต้นวันใหม่
```bash
# Start development environment
./dev.sh start

# เปิด browser
# Frontend: http://localhost:3001
# Backend API: http://localhost:8000
```

### 2️⃣ แก้โค้ด Frontend
```bash
# แก้ไฟล์ใน frontend/src/
vim frontend/src/pages/DashboardPage.tsx

# ✅ ไม่ต้องทำอะไร! Hot reload อัตโนมัติ
# Refresh browser เห็นผลทันที
```

### 3️⃣ แก้โค้ด Backend
```bash
# แก้ไฟล์ใน backend/app/
vim backend/app/api/v1/documents.py

# ✅ ไม่ต้องทำอะไร! Auto reload ทันที
# API พร้อมใช้ภายใน 1-2 วินาที
```

### 4️⃣ เปลี่ยน Dependencies
```bash
# เมื่อเพิ่ม npm package
cd frontend
npm install <package-name>

# Rebuild เฉพาะ frontend
./dev.sh rebuild frontend

# เมื่อเพิ่ม pip package (แก้ requirements.txt แล้ว)
./dev.sh rebuild backend
```

### 5️⃣ ดู Logs เพื่อ Debug
```bash
# ดู logs ทั้งหมด
./dev.sh logs

# ดู logs เฉพาะ backend
./dev.sh logs backend

# ดู logs เฉพาะ frontend
./dev.sh logs frontend
```

### 6️⃣ Restart เมื่อมีปัญหา
```bash
# Restart เฉพาะ frontend
./dev.sh restart frontend

# Restart เฉพาะ backend
./dev.sh restart backend

# Restart ทั้งหมด
./dev.sh restart
```

### 7️⃣ Backup ข้อมูล
```bash
# Backup database
./dev.sh backup

# จะได้ไฟล์ backup_YYYYMMDD_HHMMSS.sql
```

### 8️⃣ Restore ข้อมูล
```bash
# Restore จาก backup
./dev.sh restore backup_20250101_120000.sql
```

### 9️⃣ ทดสอบว่าทุกอย่างทำงาน
```bash
# Test all services
./dev.sh test
```

### 🔟 เลิกงาน/ปิดเครื่อง
```bash
# Stop development environment (ข้อมูลยังอยู่)
./dev.sh stop

# วันรุ่งขึ้นเริ่มใหม่
./dev.sh start
```

---

## 📚 คำสั่งทั้งหมด

```bash
./dev.sh start              # เริ่มต้น dev environment
./dev.sh stop               # หยุด dev environment
./dev.sh restart [service]  # Restart ทั้งหมดหรือเฉพาะ service
./dev.sh logs [service]     # ดู logs
./dev.sh ps                 # ดูสถานะ containers
./dev.sh build [service]    # Build service
./dev.sh rebuild [service]  # Rebuild และ restart
./dev.sh clean              # ลบ containers (เก็บข้อมูล)
./dev.sh clean-all          # ลบทั้งหมด (⚠️ ข้อมูลหาย)
./dev.sh backup             # Backup database
./dev.sh restore <file>     # Restore database
./dev.sh shell <service>    # เข้า shell ใน container
./dev.sh test               # ทดสอบทุก services
./dev.sh help               # ดูความช่วยเหลือ
```

---

## 🎨 Workflow การพัฒนาแบบมืออาชีพ

### เช้า (เริ่มต้นวันใหม่)
```bash
cd /mnt/c/SaveToExcel/web-app
./dev.sh start
./dev.sh logs &  # เปิด logs ไว้ใน background
```

### ตอนพัฒนา
```bash
# แก้โค้ด → Save → Refresh browser
# ✅ เห็นผลทันที! ไม่ต้อง rebuild
```

### เมื่อเจอ Error
```bash
# ดู logs
./dev.sh logs backend

# Restart ถ้าจำเป็น
./dev.sh restart backend
```

### ก่อน Commit
```bash
# ทดสอบว่าทำงาน
./dev.sh test

# Backup ข้อมูล
./dev.sh backup

# Commit
git add .
git commit -m "feat: new feature"
```

### เย็น (เลิกงาน)
```bash
# หยุดแต่เก็บข้อมูล
./dev.sh stop

# หรือปล่อยทำงานต่อ (แนะนำ)
# ไม่ต้องทำอะไร จะ restart วันรุ่งขึ้นได้เลย
```

---

## 🛡️ การป้องกันฟังก์ชันหาย

### ✅ สิ่งที่ปลอดภัย
```bash
./dev.sh restart frontend   # ✅ ปลอดภัย
./dev.sh restart backend    # ✅ ปลอดภัย
./dev.sh stop               # ✅ ปลอดภัย (ข้อมูลยังอยู่)
./dev.sh backup             # ✅ ปลอดภัย (สร้าง backup)
```

### ⚠️ สิ่งที่ต้องระวัง
```bash
./dev.sh clean              # ⚠️ ลบ containers (แต่เก็บข้อมูล)
./dev.sh clean-all          # ❌ ลบทั้งหมดรวมข้อมูล!
```

### 🔐 Best Practice
```bash
# Backup ก่อนทำอะไรสำคัญ
./dev.sh backup

# แก้โค้ด
vim backend/app/api/v1/documents.py

# ทดสอบ
./dev.sh test

# Commit
git add .
git commit -m "fix: bug fix"
```

---

## 💡 Pro Tips

1. **เปิด logs ไว้เสมอ** - จะได้รู้ว่าเกิดอะไรขึ้น
2. **Backup บ่อยๆ** - ก่อนแก้ไขครั้งใหญ่
3. **Commit บ่อยๆ** - ป้องกันสูญหาย
4. **ใช้ restart แทน stop/start** - เร็วกว่า
5. **Test ก่อน commit** - ป้องกัน bug

---

## 🚨 Troubleshooting

### Backend ไม่ reload
```bash
./dev.sh logs backend
./dev.sh restart backend
```

### Frontend ไม่แสดงผล
```bash
./dev.sh logs frontend
./dev.sh restart frontend
```

### Database connection failed
```bash
./dev.sh logs postgres
./dev.sh restart postgres
```

### ข้อมูลหาย
```bash
./dev.sh restore backup_YYYYMMDD_HHMMSS.sql
```

---

## 🎉 สรุป

**Development Mode = แก้โค้ดเห็นผลทันที!**

```bash
# เริ่มต้น
./dev.sh start

# แก้โค้ด
vim frontend/src/pages/DashboardPage.tsx

# Save → Refresh → เห็นผลทันที! ⚡

# เลิกงาน
./dev.sh stop
```

**ง่าย เร็ว ปลอดภัย** 🚀
