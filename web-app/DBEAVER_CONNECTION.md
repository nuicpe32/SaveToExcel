# DBeaver Connection Guide

## ✅ Option 1: ใช้ User ใหม่ (แนะนำ - ทดสอบแล้วใช้ได้)

```
Host:           localhost
Port:           5432
Database:       criminal_case_db
Username:       dbuser
Password:       dbpass123
```

## Option 2: ใช้ User เดิม

```
Host:           localhost
Port:           5432
Database:       criminal_case_db
Username:       user
Password:       password
```

## วิธีตั้งค่าใน DBeaver

### 1. เปิด DBeaver
- Database → New Database Connection
- เลือก **PostgreSQL**

### 2. Main Tab
- **Host:** `localhost`
- **Port:** `5432`
- **Database:** `criminal_case_db`
- **Authentication:** Database Native
- **Username:** `dbuser`
- **Password:** `dbpass123`
- ✅ **Save password**

### 3. Driver Properties (กดแท็บ Driver properties)
เพิ่ม properties เหล่านี้:
- `ssl` = `false`
- `sslmode` = `disable`

### 4. Test Connection
- กดปุ่ม **Test Connection...**
- ครั้งแรกจะถาม download driver → กด **Download**
- ควรขึ้น: ✅ **Connected** - PostgreSQL 15.14

### 5. Finish
กด **Finish** เพื่อบันทึก connection

## ตรวจสอบข้อมูล

หลังเชื่อมต่อสำเร็จ จะเห็น:

```
criminal_case_db/
├── Schemas/
│   └── public/
│       └── Tables/
│           ├── bank_accounts (ข้อมูลบัญชีธนาคาร)
│           ├── criminal_cases (ข้อมูลคดีอาญา)
│           ├── criminal_cases_case_id_backup
│           ├── post_arrests (ข้อมูลหลังจับกุม)
│           ├── suspects (ข้อมูลผู้ต้องหา)
│           └── users (ข้อมูลผู้ใช้งาน)
```

## Troubleshooting

### ถ้ายังเชื่อมต่อไม่ได้:

**1. ตรวจสอบ Docker ทำงาน:**
```bash
docker ps | grep criminal-case-db
```

**2. ทดสอบจาก command line:**
```bash
docker exec criminal-case-db psql -U dbuser -d criminal_case_db -c "SELECT version();"
```

**3. ตรวจสอบ port 5432:**
```bash
# Windows
netstat -an | findstr 5432

# Linux/WSL
netstat -tln | grep 5432
```

**4. Restart database:**
```bash
docker restart criminal-case-db
```

**5. สร้าง user ใหม่อีกครั้ง:**
```bash
docker exec criminal-case-db psql -U user -d postgres -c "ALTER USER dbuser WITH PASSWORD 'dbpass123';"
```

## Alternative: ใช้ Adminer (Web-based)

หากยังไม่สำเร็จ ให้ใช้ Adminer แทน:

1. เปิด: http://localhost:8080
2. ใส่ข้อมูล:
   - System: PostgreSQL
   - Server: postgres
   - Username: dbuser
   - Password: dbpass123
   - Database: criminal_case_db
3. กด Login

## Connection String

สำหรับโปรแกรมอื่นๆ:

```
postgresql://dbuser:dbpass123@localhost:5432/criminal_case_db
```

JDBC URL:
```
jdbc:postgresql://localhost:5432/criminal_case_db
```
