# ✅ แก้ไข Database Authentication เรียบร้อย

## ปัญหาที่พบ

**Error:**
```
FATAL: password authentication failed for user "user"
```

**สาเหตุ:**
- มีการตั้งค่า authentication method ซ้ำซ้อนใน `pg_hba.conf`:
  - `scram-sha-256` (บรรทัดแรก)
  - `md5` (บรรทัดที่สอง)
- PostgreSQL confused ว่าจะใช้ method ไหน

## การแก้ไข

### 1. แก้ไข pg_hba.conf
```conf
# เอาออก (ขัดแย้งกัน):
host all all all scram-sha-256
host all all 0.0.0.0/0 md5

# ใช้แค่บรรทัดเดียว:
host    all             all             0.0.0.0/0               md5
```

### 2. Reload Configuration
```sql
SELECT pg_reload_conf();
```

### 3. Reset Passwords
```sql
ALTER USER "user" WITH PASSWORD 'password';
ALTER USER dbuser WITH PASSWORD 'dbpass123';
```

### 4. Restart Backend
```bash
docker restart criminal-case-backend
```

---

## ✅ สถานะปัจจุบัน

### PostgreSQL Authentication
- **Method:** MD5 (สำหรับ all connections)
- **Allow from:** 0.0.0.0/0 (ทุก IP)
- **Status:** ✅ ทำงานปกติ

### Credentials ที่ใช้ได้

#### Option 1: User (Default)
```
Host:     localhost
Port:     5432
Database: criminal_case_db
Username: user
Password: password
```

#### Option 2: DBUser (Alternative)
```
Host:     localhost
Port:     5432
Database: criminal_case_db
Username: dbuser
Password: dbpass123
```

---

## 🔧 การเชื่อมต่อ

### 1. DBeaver
- Host: `localhost`
- Port: `5432`
- Database: `criminal_case_db`
- Username: `user`
- Password: `password`
- ✅ Test Connection → Should work now!

### 2. pgAdmin (Web)
- URL: http://localhost:5050
- Login: admin@admin.com / admin
- Add Server:
  - Host: `postgres` (container name)
  - Port: `5432`
  - Username: `user`
  - Password: `password`

### 3. Adminer (Web)
- URL: http://localhost:8080
- System: PostgreSQL
- Server: `postgres`
- Username: `user`
- Password: `password`
- Database: `criminal_case_db`

### 4. Backend API
- URL: http://localhost:8000
- Status: ✅ Running
- Database: ✅ Connected

---

## 📊 ตรวจสอบการเชื่อมต่อ

### Test จาก Command Line
```bash
# Test database connection
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT version();"

# Count records
docker exec criminal-case-db psql -U user -d criminal_case_db -c "
SELECT
    'criminal_cases' as table, COUNT(*) FROM criminal_cases
UNION ALL
SELECT 'bank_accounts', COUNT(*) FROM bank_accounts
UNION ALL
SELECT 'suspects', COUNT(*) FROM suspects
UNION ALL
SELECT 'post_arrests', COUNT(*) FROM post_arrests
UNION ALL
SELECT 'users', COUNT(*) FROM users;
"
```

### Test Backend
```bash
# Check API
curl http://localhost:8000

# Should return:
# {
#   "message": "Criminal Case Management System API",
#   "version": "3.0.0",
#   "docs": "/docs"
# }
```

---

## 🛡️ Security Note

### Current Setup (Development)
- ✅ MD5 authentication (better than plaintext)
- ✅ Password required
- ⚠️  Allows connections from any IP (0.0.0.0/0)

### For Production (แนะนำ)
```conf
# แทนที่ 0.0.0.0/0 ด้วย IP specific
host    all             all             10.0.0.0/8              md5
host    all             all             172.16.0.0/12           md5
host    all             all             192.168.0.0/16          md5

# หรือใช้ scram-sha-256 (ปลอดภัยกว่า)
host    all             all             0.0.0.0/0               scram-sha-256
```

---

## ✅ Checklist

- [x] แก้ไข pg_hba.conf ให้ใช้ MD5 เท่านั้น
- [x] Reload PostgreSQL configuration
- [x] Reset passwords ทั้งหมด
- [x] Restart backend
- [x] Test API connection
- [x] Verify database connections

---

## 📝 Next Steps

1. **ลองเชื่อมต่อ DBeaver อีกครั้ง:**
   - Username: `user`
   - Password: `password`
   - Should work now! ✅

2. **ถ้ายังไม่ได้:**
   - Restart DBeaver
   - Clear connection cache
   - ลองใช้ `dbuser` / `dbpass123` แทน

3. **Test Web App:**
   - URL: http://localhost:3001
   - Login: admin / admin123
   - Should work normally ✅

---

## 🔄 Backup pg_hba.conf

ไฟล์ backup เก็บไว้ที่:
```
/var/lib/postgresql/data/pg_hba.conf.backup
```

ถ้าต้องการ restore:
```bash
docker exec criminal-case-db sh -c "
cp /var/lib/postgresql/data/pg_hba.conf.backup /var/lib/postgresql/data/pg_hba.conf
"
docker exec criminal-case-db psql -U user -d postgres -c "SELECT pg_reload_conf();"
```
