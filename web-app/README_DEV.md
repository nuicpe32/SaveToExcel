# 🚀 Development Mode - Quick Reference

## ⚡ TL;DR

```bash
cd /mnt/c/SaveToExcel/web-app

# เริ่มต้น
./dev.sh start

# แก้โค้ด → Save → Refresh → เห็นผลทันที! ✨

# เลิกงาน
./dev.sh stop
```

---

## 📚 เอกสารทั้งหมด

1. **[QUICK_START_DEV.md](QUICK_START_DEV.md)** - คำแนะนำเริ่มต้นใช้งาน
2. **[DEV_SETUP.md](DEV_SETUP.md)** - รายละเอียดการตั้งค่า Development Mode
3. **[SWITCH_TO_DEV_MODE.md](SWITCH_TO_DEV_MODE.md)** - วิธีสลับจาก Production มา Dev Mode

---

## 🎯 ตอบคำถามที่พบบ่อย

### Q: ตอนนี้อยู่ใน Mode ไหน?
```bash
# ถ้ามีไฟล์ docker-compose.yml (เดิม) = Production Mode
# ถ้าใช้ docker-compose.dev.yml = Development Mode

# เช็คได้จาก
docker ps --format "table {{.Names}}\t{{.Status}}"
# ถ้าเห็น *-dev = Development Mode
```

### Q: ควรใช้ Mode ไหน?
- **Development Mode** (แนะนำ) - เมื่อกำลังพัฒนาต่อเนื่อง
- **Production Mode** - เมื่อนำขึ้น production จริง

### Q: ฟังก์ชันจะหายไหม?
**ไม่หาย!** ถ้าใช้ Development Mode ตามคู่มือ:
- ✅ แก้โค้ด → Hot reload → ไม่ต้อง rebuild
- ✅ ข้อมูลอยู่ใน volume → ไม่หาย
- ✅ ใช้ restart แทน down/up → ปลอดภัย

### Q: แก้โค้ดแล้วไม่เห็นผล?
```bash
# 1. เช็คว่า dev mode ทำงานอยู่หรือไม่
./dev.sh ps

# 2. ดู logs
./dev.sh logs frontend

# 3. Refresh browser (Ctrl+Shift+R)

# 4. ถ้ายังไม่ได้ restart
./dev.sh restart frontend
```

### Q: ต้อง Rebuild บ่อยไหม?
**ไม่ต้อง!** ใน Development Mode:
- แก้ Frontend → Hot reload อัตโนมัติ ⚡
- แก้ Backend → Auto reload ภายใน 1-2 วินาที ⚡
- เฉพาะเมื่อเปลี่ยน dependencies ถึงต้อง rebuild

### Q: ข้อมูลหายไหมถ้าปิดเครื่อง?
**ไม่หาย!** ข้อมูลอยู่ใน Docker volumes:
```bash
# Stop แล้วข้อมูลยังอยู่
./dev.sh stop

# Start ใหม่ข้อมูลยังอยู่ครบ
./dev.sh start
```

---

## 🛡️ มาตรการป้องกันฟังก์ชันหาย

### ✅ ปฏิบัติแบบนี้
```bash
# 1. Backup บ่อยๆ
./dev.sh backup

# 2. Commit บ่อยๆ
git add .
git commit -m "feat: new feature"

# 3. ใช้ restart แทน down/up
./dev.sh restart frontend

# 4. แก้โค้ด → Save → Refresh (ไม่ต้อง rebuild)
```

### ❌ อย่าทำแบบนี้
```bash
# ❌ ใช้ docker-compose up -d (จะ recreate ทุกอย่าง)
# ✅ ใช้ ./dev.sh restart แทน

# ❌ ใช้ docker-compose down -v (จะลบข้อมูล)
# ✅ ใช้ ./dev.sh stop แทน
```

---

## 📊 เปรียบเทียบ Production vs Development Mode

| ฟีเจอร์ | Production Mode | Development Mode |
|---------|----------------|------------------|
| Hot Reload | ❌ ไม่มี | ✅ มี (ทั้ง FE & BE) |
| แก้โค้ดเห็นผลทันที | ❌ ต้อง rebuild | ✅ ทันที (1-2 วินาที) |
| เวลา rebuild | ~2-3 นาที | ไม่ต้อง rebuild |
| Volume mount | ❌ Backend อย่างเดียว | ✅ ทั้ง FE & BE |
| เหมาะสำหรับ | Production | Development |
| ความเร็วในการพัฒนา | ⭐⭐ | ⭐⭐⭐⭐⭐ |

---

## 🎨 Workflow แนะนำ

### เช้า (8:00)
```bash
cd /mnt/c/SaveToExcel/web-app
./dev.sh start
./dev.sh logs -f &  # เปิด logs ไว้ดู
```

### ตอนพัฒนา (8:00-17:00)
```bash
# แก้โค้ด
vim frontend/src/pages/DashboardPage.tsx

# Save → Refresh → เห็นผลทันที! ⚡

# Debug ถ้าเจอปัญหา
./dev.sh logs backend
```

### ก่อน Commit (17:00)
```bash
# Backup
./dev.sh backup

# Test
./dev.sh test

# Commit
git add .
git commit -m "feat: today's work"
```

### เย็น (17:30)
```bash
# หยุดหรือปล่อยทำงานต่อ
./dev.sh stop  # หรือไม่ต้องทำอะไร
```

---

## 💡 คำสั่งที่ใช้บ่อย (Top 10)

```bash
1.  ./dev.sh start          # เริ่มต้น dev environment
2.  ./dev.sh logs           # ดู logs
3.  ./dev.sh restart frontend  # Restart frontend
4.  ./dev.sh restart backend   # Restart backend
5.  ./dev.sh ps             # ดูสถานะ
6.  ./dev.sh backup         # Backup database
7.  ./dev.sh test           # ทดสอบทุก services
8.  ./dev.sh stop           # หยุดการทำงาน
9.  ./dev.sh rebuild frontend  # Rebuild frontend (เมื่อเปลี่ยน deps)
10. ./dev.sh help           # ดูความช่วยเหลือ
```

---

## 🔗 Links

- Frontend: http://localhost:3001
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Database: localhost:5432 (user: user, password: password123)

---

## 🆘 ขอความช่วยเหลือ

เจอปัญหา? ดูเอกสารเหล่านี้:

1. **[QUICK_START_DEV.md](QUICK_START_DEV.md)** - Use cases และตัวอย่างการใช้งาน
2. **[DEV_SETUP.md](DEV_SETUP.md)** - รายละเอียดการตั้งค่าและ troubleshooting
3. **[SWITCH_TO_DEV_MODE.md](SWITCH_TO_DEV_MODE.md)** - วิธีสลับมา Dev Mode

หรือรันคำสั่ง:
```bash
./dev.sh help
```

---

## ✅ Checklist สำหรับเริ่มต้น

- [ ] อ่าน [QUICK_START_DEV.md](QUICK_START_DEV.md) แล้ว
- [ ] รัน `./dev.sh start` สำเร็จ
- [ ] เปิด http://localhost:3001 ได้
- [ ] แก้โค้ดแล้วเห็น hot reload
- [ ] ทดสอบ `./dev.sh test` ผ่าน
- [ ] Backup ด้วย `./dev.sh backup` แล้ว
- [ ] เข้าใจคำสั่งพื้นฐาน (start, stop, restart, logs)

---

**🎉 พร้อมพัฒนาแล้ว! Happy Coding! 🚀**
