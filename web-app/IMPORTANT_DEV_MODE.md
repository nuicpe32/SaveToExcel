# ⚠️ สำคัญมาก: โปรเจคนี้ใช้ DEV MODE เป็นหลัก

## 📌 สรุปสำหรับ AI Assistant / Developer ใหม่

**วันที่อัพเดท:** 1 ตุลาคม 2025

โปรเจคนี้ได้เปลี่ยนจากการใช้ **Production Mode** มาเป็น **Development Mode เป็นหลัก** แล้ว

---

## 🚀 วิธีเริ่มต้นระบบ (เพียง 1 คำสั่ง)

```bash
cd /mnt/c/SaveToExcel/web-app
docker-compose -f docker-compose.dev.yml up -d
```

### ❌ อย่าใช้คำสั่งนี้:
```bash
docker-compose up -d  # ❌ ไม่ใช่แล้ว! จะใช้ volume ผิด
```

### ✅ ใช้คำสั่งนี้:
```bash
docker-compose -f docker-compose.dev.yml up -d  # ✅ ถูกต้อง!
```

---

## 📦 Docker Configuration

### Docker Compose Files

| File | Usage | Status |
|------|-------|--------|
| `docker-compose.yml` | Production Mode | ⚠️ **เลิกใช้แล้ว** |
| `docker-compose.dev.yml` | Development Mode | ✅ **ใช้งานหลัก** |
| `docker-compose.pgadmin.yml` | PgAdmin Tool | Optional |
| `docker-compose.adminer.yml` | Adminer Tool | Optional |

### Docker Volumes (สำคัญ!)

**⚠️ ระวัง Volume Confusion:**

โปรเจคนี้มี 2 sets ของ volumes:

#### Development Volumes (✅ ใช้งานอยู่):
```
criminal-case-postgres-dev    # ฐานข้อมูลหลัก
criminal-case-uploads-dev     # ไฟล์อัพโหลด
```

#### Production Volumes (⚠️ ไม่ใช้แล้ว):
```
web-app_postgres_data         # ฐานข้อมูลเก่า (ข้อมูลยังอยู่)
web-app_backend_uploads       # อัพโหลดเก่า
```

### Container Names

**Development Containers (ทั้งหมดลงท้ายด้วย `-dev`):**
- `criminal-case-db-dev` - PostgreSQL 15
- `criminal-case-redis-dev` - Redis 7
- `criminal-case-backend-dev` - FastAPI Backend
- `criminal-case-frontend-dev` - React Frontend (Vite)

---

## 🔌 Ports & URLs

| Service | Port | URL | Description |
|---------|------|-----|-------------|
| Frontend | 3001 | http://localhost:3001 | React App (Dev Server) |
| Backend | 8000 | http://localhost:8000 | FastAPI |
| API Docs | 8000 | http://localhost:8000/docs | Swagger UI |
| PostgreSQL | 5432 | localhost:5432 | Database |
| Redis | 6379 | localhost:6379 | Cache |

---

## 🔐 Credentials

### Database (PostgreSQL)
```
Host: localhost
Port: 5432
User: user
Password: password123  # ⚠️ DEV mode ใช้ password123 (ไม่ใช่ password)
Database: criminal_case_db
```

### Admin User (Web App)
```
Username: admin
Password: admin123
```

---

## 🛠️ คำสั่งที่ใช้บ่อย

### เริ่มระบบ
```bash
cd /mnt/c/SaveToExcel/web-app
docker-compose -f docker-compose.dev.yml up -d
```

### หยุดระบบ
```bash
docker-compose -f docker-compose.dev.yml down
```

### ดู Logs
```bash
# ทั้งหมด
docker-compose -f docker-compose.dev.yml logs -f

# เฉพาะ service
docker logs criminal-case-backend-dev -f
docker logs criminal-case-frontend-dev -f
docker logs criminal-case-db-dev -f
```

### Restart Service
```bash
docker restart criminal-case-backend-dev
docker restart criminal-case-frontend-dev
```

### เข้าไปใน Container
```bash
# Backend
docker exec -it criminal-case-backend-dev bash

# Database
docker exec -it criminal-case-db-dev psql -U user -d criminal_case_db
```

### ตรวจสอบสถานะ
```bash
docker ps  # ดู containers ที่รันอยู่
docker volume ls  # ดู volumes ทั้งหมด
docker network ls  # ดู networks
```

---

## 🗄️ Database Operations

### ตรวจสอบข้อมูล
```bash
docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "
SELECT
  (SELECT COUNT(*) FROM criminal_cases) as cases,
  (SELECT COUNT(*) FROM suspects) as suspects,
  (SELECT COUNT(*) FROM bank_accounts) as banks,
  (SELECT COUNT(*) FROM users) as users;
"
```

### Backup Database
```bash
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
docker exec criminal-case-db-dev pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_${TIMESTAMP}.dump
docker cp criminal-case-db-dev:/tmp/backup_${TIMESTAMP}.dump ./backup_database_${TIMESTAMP}.dump
```

### Restore Database
```bash
docker cp backup_database_YYYYMMDD_HHMMSS.dump criminal-case-db-dev:/tmp/restore.dump
docker exec criminal-case-db-dev pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

---

## 🚨 ปัญหาที่พบบ่อย & วิธีแก้

### 1. Frontend ไม่เชื่อมต่อ Backend (ECONNREFUSED)

**สาเหตุ:** `vite.config.ts` proxy ชี้ไป `localhost` แทนที่จะเป็น `backend` (Docker service name)

**วิธีแก้:** (แก้ไขแล้วใน commit ล่าสุด)
```typescript
// vite.config.ts
server: {
  proxy: {
    '/api': {
      target: 'http://backend:8000',  // ✅ ใช้ service name
      changeOrigin: true,
    },
  },
}
```

### 2. ข้อมูลหายหลัง Restart

**สาเหตุ:** ใช้ docker-compose file ผิด หรือ volume ผิด

**วิธีแก้:**
```bash
# ตรวจสอบว่าใช้ dev volume
docker volume inspect criminal-case-postgres-dev

# Restore จาก backup (ดู BACKUP_RESTORE_GUIDE.md)
```

### 3. Login ไม่ได้

**เช็คสิ่งเหล่านี้:**
1. Database มีข้อมูล user หรือไม่
   ```bash
   docker exec criminal-case-db-dev psql -U user -d criminal_case_db -c "SELECT * FROM users;"
   ```

2. Backend logs มี error หรือไม่
   ```bash
   docker logs criminal-case-backend-dev --tail 50
   ```

3. Frontend เชื่อมต่อ Backend ได้หรือไม่
   ```bash
   curl http://localhost:8000/api/v1/auth/login \
     -X POST \
     -H "Content-Type: application/x-www-form-urlencoded" \
     -d "username=admin&password=admin123"
   ```

### 4. Port Already in Use

```bash
# หา process ที่ใช้ port
lsof -i :3001  # Frontend
lsof -i :8000  # Backend
lsof -i :5432  # PostgreSQL

# Kill process
kill -9 <PID>
```

---

## 📝 สำหรับ AI Assistant

เมื่อได้รับโปรเจคนี้ ให้จำไว้ว่า:

### ✅ Do:
1. **เสมอ** ใช้ `docker-compose -f docker-compose.dev.yml`
2. ใช้ container names ที่ลงท้ายด้วย `-dev`
3. Database password คือ `password123` (ไม่ใช่ `password`)
4. Frontend URL คือ `http://localhost:3001` (ไม่ใช่ 3000)
5. ใช้ service name `backend:8000` ใน Docker network (ไม่ใช่ `localhost:8000`)
6. สร้าง backup ก่อนทำการเปลี่ยนแปลงสำคัญ

### ❌ Don't:
1. **อย่า** ใช้ `docker-compose up` โดยไม่มี `-f docker-compose.dev.yml`
2. **อย่า** ใช้ production volumes (`web-app_postgres_data`)
3. **อย่า** แก้ไข `docker-compose.yml` (ใช้ `docker-compose.dev.yml` แทน)
4. **อย่า** ลืมระบุ `-dev` ใน container names
5. **อย่า** สมมติว่า localhost:8000 ใช้ได้ใน container (ต้องใช้ backend:8000)

### 🔍 เมื่อเริ่มงาน:
1. อ่านไฟล์นี้ทั้งหมดก่อน
2. ตรวจสอบ containers ที่รันอยู่: `docker ps`
3. ตรวจสอบ volumes: `docker volume ls | grep dev`
4. ตรวจสอบข้อมูล: รัน SQL query ด้านบน
5. Test login: http://localhost:3001/login

---

## 📚 เอกสารเพิ่มเติม

- [README.md](./README.md) - คู่มือหลัก
- [BACKUP_RESTORE_GUIDE.md](./BACKUP_RESTORE_GUIDE.md) - วิธี backup/restore
- [DEV_MODE_SETUP.md](./DEV_MODE_SETUP.md) - Setup development
- [ARCHITECTURE.md](../ARCHITECTURE.md) - สถาปัตยกรรม

---

## 📊 Current System Status (ณ วันที่ 1 ต.ค. 2025)

### ข้อมูลในระบบ:
- ✅ 48 คดีอาญา
- ✅ 15 ผู้ต้องหา
- ✅ 418 บัญชีธนาคาร
- ✅ 1 Admin user

### Backup Files:
- `backup_database_20251001_221353.dump` (75 KB)
- `web-app-backup-20251001_221400.tar.gz` (682 KB)

### Docker Status:
- ✅ criminal-case-db-dev (Running)
- ✅ criminal-case-redis-dev (Running)
- ✅ criminal-case-backend-dev (Running)
- ✅ criminal-case-frontend-dev (Running)

### Network:
- ✅ criminal-case-network (External)

---

**สร้างเมื่อ:** 1 ตุลาคม 2025
**อัพเดทล่าสุด:** 1 ตุลาคม 2025
**Status:** 🟢 Active Development Mode
