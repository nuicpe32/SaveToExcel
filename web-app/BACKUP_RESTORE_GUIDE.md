# คู่มือการ Backup และ Restore ระบบ

## 📦 Backup Files ที่สร้างเมื่อ: 1 ตุลาคม 2025

### ไฟล์ Backup ที่มี:

1. **ฐานข้อมูลเต็มรูปแบบ**
   - `backup_database_20251001_221353.dump` (75 KB)
   - รูปแบบ: PostgreSQL custom format (.dump)
   - ข้อมูล: 48 คดี, 15 ผู้ต้องหา, 418 บัญชีธนาคาร

2. **โค้ดโปรแกรมทั้งหมด**
   - `/mnt/c/SaveToExcel/web-app-backup-20251001_221400.tar.gz` (682 KB)
   - รวม: frontend, backend, docker configs
   - ไม่รวม: node_modules, __pycache__ (สามารถติดตั้งใหม่ได้)

---

## 🔄 วิธีการ Restore

### วิธีที่ 1: Restore เฉพาะฐานข้อมูล (Database Only)

```bash
# 1. Copy backup file เข้า container
docker cp backup_database_20251001_221353.dump criminal-case-db-dev:/tmp/restore.dump

# 2. Restore ฐานข้อมูล
docker exec criminal-case-db-dev pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump

# 3. ตรวจสอบข้อมูล
docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM criminal_cases;"
```

### วิธีที่ 2: Restore โปรแกรมทั้งหมด (Full Restore)

```bash
# 1. หยุดระบบปัจจุบัน
cd /mnt/c/SaveToExcel/web-app
docker-compose -f docker-compose.dev.yml down

# 2. Extract backup
cd /mnt/c/SaveToExcel
tar -xzf web-app-backup-20251001_221400.tar.gz

# 3. เข้าไปที่โฟลเดอร์
cd web-app

# 4. ติดตั้ง dependencies (ถ้าจำเป็น)
cd frontend && npm install && cd ..

# 5. เริ่มระบบใหม่
docker-compose -f docker-compose.dev.yml up -d

# 6. Restore ฐานข้อมูล
docker cp backup_database_20251001_221353.dump criminal-case-db-dev:/tmp/restore.dump
docker exec criminal-case-db-dev pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

### วิธีที่ 3: Restore ไปยัง Volume ใหม่

```bash
# 1. สร้าง volume ใหม่
docker volume create criminal-case-postgres-restore

# 2. เริ่ม container ชั่วคราวด้วย volume ใหม่
docker run -d --name temp-restore-db \
  -v criminal-case-postgres-restore:/var/lib/postgresql/data \
  -e POSTGRES_USER=user \
  -e POSTGRES_PASSWORD=password123 \
  -e POSTGRES_DB=criminal_case_db \
  postgres:15-alpine

# 3. รอให้ database พร้อม
sleep 10

# 4. Copy และ restore
docker cp backup_database_20251001_221353.dump temp-restore-db:/tmp/backup.dump
docker exec temp-restore-db pg_restore -U user -d criminal_case_db -c -F c /tmp/backup.dump

# 5. หยุดและลบ container ชั่วคราว
docker stop temp-restore-db && docker rm temp-restore-db

# 6. อัพเดท docker-compose.dev.yml ให้ใช้ volume ใหม่
# แก้ volumes: จาก postgres_data_dev เป็น criminal-case-postgres-restore
```

---

## ✅ ตรวจสอบความสมบูรณ์

### ตรวจสอบข้อมูลในฐานข้อมูล:

```bash
# ตรวจนับข้อมูล
docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "
SELECT
  (SELECT COUNT(*) FROM criminal_cases) as cases,
  (SELECT COUNT(*) FROM suspects) as suspects,
  (SELECT COUNT(*) FROM bank_accounts) as bank_accounts,
  (SELECT COUNT(*) FROM users) as users;
"

# ควรได้ผลลัพธ์:
# cases: 48
# suspects: 15
# bank_accounts: 418
# users: 1
```

### ตรวจสอบการ Login:

1. เปิดเว็บ: http://localhost:3001/login
2. Username: `admin`
3. Password: `admin123`
4. ตรวจสอบว่าเข้าระบบได้และเห็นข้อมูลครบถ้วน

---

## 🚨 สำหรับกรณีฉุกเฉิน

### ถ้าระบบมีปัญหา - ใช้ไฟล์ Backup นี้:

1. **ไฟล์ฐานข้อมูล:** `backup_database_20251001_221353.dump`
2. **ไฟล์โค้ด:** `web-app-backup-20251001_221400.tar.gz`
3. **สถานที่เก็บ:** `/mnt/c/SaveToExcel/`

### ขั้นตอนกู้คืนด่วน:

```bash
# แค่ 3 คำสั่ง!
cd /mnt/c/SaveToExcel
tar -xzf web-app-backup-20251001_221400.tar.gz
cd web-app && docker-compose -f docker-compose.dev.yml up -d
docker cp backup_database_20251001_221353.dump criminal-case-db-dev:/tmp/restore.dump
docker exec criminal-case-db-dev pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

---

## 📝 หมายเหตุ

- Backup นี้ทำในโหมด Development (dev mode)
- Password database: `password123`
- Password admin: `admin123`
- Port: Frontend 3001, Backend 8000, PostgreSQL 5432
- สามารถสร้าง backup ใหม่ได้ตามขั้นตอนด้านล่าง

---

## 🔧 วิธีสร้าง Backup ใหม่

### Backup ฐานข้อมูล:
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec criminal-case-db-dev pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_${TIMESTAMP}.dump
docker cp criminal-case-db-dev:/tmp/backup_${TIMESTAMP}.dump /mnt/c/SaveToExcel/web-app/backup_database_${TIMESTAMP}.dump
```

### Backup โค้ดทั้งหมด:
```bash
cd /mnt/c/SaveToExcel
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
tar -czf web-app-backup-${TIMESTAMP}.tar.gz \
  --exclude='web-app/node_modules' \
  --exclude='web-app/frontend/node_modules' \
  --exclude='web-app/backend/__pycache__' \
  --exclude='web-app/.git' \
  web-app/
```

---

**สร้างเมื่อ:** 1 ตุลาคม 2025 22:13:53
**ข้อมูล:** 48 คดี, 15 ผู้ต้องหา, 418 บัญชีธนาคาร
**Status:** ✅ Verified & Complete
