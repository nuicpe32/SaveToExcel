# 🔄 คำแนะนำในการสลับไป Development Mode

## ⚠️ สำคัญมาก: อ่านก่อนทำ!

### 🎯 จุดประสงค์
เปลี่ยนจากการใช้ Production Mode ไปเป็น **Development Mode** ที่รองรับ:
- ✅ Hot Reload - แก้โค้ดเห็นผลทันที
- ✅ ไม่ต้อง Rebuild บ่อย
- ✅ พัฒนาเร็วขึ้น 10 เท่า

---

## 📋 ขั้นตอนการสลับ (ใช้เวลา 5 นาที)

### 1️⃣ Backup ข้อมูลปัจจุบัน (สำคัญ!)

```bash
cd /mnt/c/SaveToExcel/web-app

# Backup database
docker-compose exec postgres pg_dump -U user criminal_case_db > backup_before_dev_mode.sql

# เช็คว่า backup สำเร็จ
ls -lh backup_before_dev_mode.sql
```

### 2️⃣ Stop Production Containers (ไม่ลบ volumes)

```bash
# Stop แต่ไม่ลบ volumes (ข้อมูลยังอยู่)
docker-compose stop

# หรือถ้าต้องการลบ containers (แต่เก็บ volumes)
docker-compose down
```

### 3️⃣ Copy ข้อมูลไป Dev Volume

```bash
# สร้าง network
docker network create criminal-case-network 2>/dev/null || true

# Start เฉพาะ postgres ของ dev
docker-compose -f docker-compose.dev.yml up -d postgres

# รอให้ postgres พร้อม
sleep 10

# Restore ข้อมูล
cat backup_before_dev_mode.sql | docker-compose -f docker-compose.dev.yml exec -T postgres psql -U user -d criminal_case_db
```

### 4️⃣ Start Development Environment

```bash
# Start ทุก services
docker-compose -f docker-compose.dev.yml up -d

# ดู logs
docker-compose -f docker-compose.dev.yml logs -f
```

### 5️⃣ ทดสอบว่าทำงาน

```bash
# Test backend
curl http://localhost:8000/api/v1/criminal-cases/

# Test frontend - เปิด browser ที่
# http://localhost:3001
```

---

## 🎉 เสร็จแล้ว!

ตอนนี้คุณอยู่ใน **Development Mode** แล้ว:

### ✨ สิ่งที่เปลี่ยนไป:
- ✅ แก้โค้ด Frontend → เห็นผลทันที (ไม่ต้อง rebuild)
- ✅ แก้โค้ด Backend → reload อัตโนมัติ (ภายใน 1-2 วินาที)
- ✅ ข้อมูลปลอดภัย → อยู่ใน volume แยก
- ✅ พัฒนาเร็วขึ้น → ประหยัดเวลามหาศาล

### 📝 คำสั่งใหม่ที่ต้องใช้:
```bash
# Start dev environment
docker-compose -f docker-compose.dev.yml up -d

# Stop dev environment
docker-compose -f docker-compose.dev.yml stop

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Restart services
docker-compose -f docker-compose.dev.yml restart frontend
docker-compose -f docker-compose.dev.yml restart backend
```

---

## 🔙 ถ้าต้องการกลับไป Production Mode

```bash
# 1. Backup dev data
docker-compose -f docker-compose.dev.yml exec postgres pg_dump -U user criminal_case_db > backup_dev.sql

# 2. Stop dev
docker-compose -f docker-compose.dev.yml down

# 3. Start production
docker-compose up -d

# 4. Restore data
cat backup_dev.sql | docker-compose exec -T postgres psql -U user -d criminal_case_db
```

---

## 🚨 หากเกิดปัญหา

### Database connection failed
```bash
# เช็คว่า postgres ทำงานหรือไม่
docker-compose -f docker-compose.dev.yml ps postgres

# ดู logs
docker-compose -f docker-compose.dev.yml logs postgres

# Restart
docker-compose -f docker-compose.dev.yml restart postgres
```

### Frontend ไม่ขึ้น
```bash
# Rebuild frontend
docker-compose -f docker-compose.dev.yml build frontend
docker-compose -f docker-compose.dev.yml up -d frontend
```

### ข้อมูลหาย
```bash
# Restore จาก backup
cat backup_before_dev_mode.sql | docker-compose -f docker-compose.dev.yml exec -T postgres psql -U user -d criminal_case_db
```

---

## 💡 Pro Tips

1. **ใช้ alias** เพื่อพิมพ์ง่ายขึ้น
2. **เปิด logs ไว้เสมอ** เพื่อดูว่าเกิดอะไรขึ้น
3. **Commit บ่อยๆ** ป้องกันสูญหาย
4. **ใช้ restart แทน down/up** ปลอดภัยกว่า

---

## ✅ Checklist

- [ ] Backup database แล้ว
- [ ] Stop production containers แล้ว
- [ ] Start dev containers แล้ว
- [ ] Restore data แล้ว
- [ ] Test frontend ทำงาน
- [ ] Test backend ทำงาน
- [ ] Test hot reload ทำงาน
- [ ] อ่าน DEV_SETUP.md แล้ว
