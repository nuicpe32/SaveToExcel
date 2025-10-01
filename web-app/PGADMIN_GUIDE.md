# pgAdmin - วิธีเชื่อมต่อ Database

## ✅ pgAdmin กำลังทำงานแล้ว!

### เปิด pgAdmin:
**URL:** http://localhost:5050

### Login:
- **Email:** `admin@admin.com`
- **Password:** `admin`

---

## เพิ่ม Database Server

หลังจาก login แล้ว ทำตามขั้นตอน:

### 1. คลิกขวา Servers → Register → Server

### 2. General Tab:
- **Name:** `Criminal Case Database`

### 3. Connection Tab:
- **Host name/address:** `postgres`
- **Port:** `5432`
- **Maintenance database:** `criminal_case_db`
- **Username:** `user`
- **Password:** `password123`
- ☑ **Save password**

### 4. กด Save

---

## ถ้าเชื่อมต่อไม่ได้

ลองใช้ user อื่น:
- **Username:** `dbuser`
- **Password:** `dbpass123`

หรือใช้ host อื่น:
- **Host:** `criminal-case-db` (ชื่อ container)
- **Host:** `postgres` (service name)

---

## ดูข้อมูล

หลังเชื่อมต่อสำเร็จ:

```
Criminal Case Database
└── Databases (1)
    └── criminal_case_db
        └── Schemas
            └── public
                └── Tables (6)
                    ├── bank_accounts
                    ├── criminal_cases
                    ├── criminal_cases_case_id_backup
                    ├── post_arrests
                    ├── suspects
                    └── users
```

คลิกขวาที่ table → View/Edit Data → All Rows

---

## Alternative: Adminer (ง่ายกว่า)

**URL:** http://localhost:8080

Login:
- System: **PostgreSQL**
- Server: **postgres**
- Username: **user**
- Password: **password123**
- Database: **criminal_case_db**
