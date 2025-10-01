# การทดสอบ Login - Criminal Case Web App

## ✅ สถานะระบบ

### Containers ทำงานปกติ:
```
✓ criminal-case-frontend  → http://localhost:3001
✓ criminal-case-backend   → http://localhost:8000
✓ criminal-case-db        → localhost:5432
✓ criminal-case-redis     → localhost:6379
```

### API Status:
```json
{
  "message": "Criminal Case Management System API",
  "version": "3.0.0",
  "docs": "/docs"
}
```

---

## 🔐 ข้อมูล Login

### User ในระบบ:
```
Username: admin
Password: admin123
Email:    admin@example.com
Role:     ADMIN
Status:   Active ✓
```

---

## 🌐 การเข้าใช้งาน

### 1. เปิด Web Application
```
URL: http://localhost:3001
```

### 2. หน้า Login
- ใส่ Username: `admin`
- ใส่ Password: `admin123`
- กดปุ่ม Login

### 3. API Documentation (สำหรับ Debug)
```
URL: http://localhost:8000/docs
```
ใน Swagger UI จะเห็น API endpoints ทั้งหมด รวมถึง login endpoint

---

## 🔍 Troubleshooting

### ถ้า Login ไม่ได้:

#### 1. ตรวจสอบ Console ใน Browser
- กด F12 (Developer Tools)
- เปิดแท็บ Console
- ดู error messages
- เปิดแท็บ Network
- ลอง login อีกครั้ง ดูว่า API call ไปที่ไหน และ response อะไรกลับมา

#### 2. ตรวจสอบ Backend Logs
```bash
docker logs criminal-case-backend --tail 50
```

#### 3. ทดสอบ API ด้วย curl
```bash
# หา login endpoint จาก API docs
curl http://localhost:8000/docs

# ทดสอบ login (ตัวอย่าง - ต้องดู path ที่ถูกต้องจาก docs)
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

#### 4. Reset Password (ถ้าจำเป็น)
```bash
# Login เข้า database
docker exec -it criminal-case-db psql -U user -d criminal_case_db

# ดู users
SELECT username, email, is_active FROM users;

# Reset password เป็น 'admin123'
# (ต้องใช้ bcrypt hash - ทำผ่าน API หรือ script)
```

---

## 🐛 Issues พบในตอนนี้

### ❌ Database Authentication Issue (แก้ไขแล้ว)
- **ปัญหา:** Backend ไม่สามารถเชื่อมต่อ PostgreSQL
- **สาเหตุ:** การแก้ไข pg_hba.conf ทำให้ authentication ผิดพลาด
- **การแก้ไข:** Reset password และ reload config
- **สถานะ:** ✅ แก้ไขแล้ว - Backend รันปกติ

### ⚠️ Login Endpoint Unknown
- **ปัญหา:** ไม่พบ login endpoint ใน API
- **การแก้ไข:** เปิด http://localhost:8000/docs เพื่อดู API endpoints
- **แนะนำ:** ทดสอบจาก browser จริงๆ ที่ http://localhost:3001

---

## 📝 คำแนะนำ

1. **เปิด Web App:** http://localhost:3001
2. **ถ้า login ไม่ได้:** กด F12 ดู Console/Network
3. **ถ้ายังไม่ได้:** ส่ง screenshot error มา
4. **API Docs:** http://localhost:8000/docs

---

## 🔧 Quick Fixes

### Restart Services
```bash
# Restart backend
docker restart criminal-case-backend

# Restart all
docker-compose restart

# Check status
docker-compose ps
```

### Check Database Connection
```bash
# Test database
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM users;"

# Should return: 1
```

### Verify User Password Hash
```bash
docker exec criminal-case-db psql -U user -d criminal_case_db -c \
  "SELECT username, LEFT(hashed_password, 30) as hash_preview FROM users WHERE username='admin';"
```

---

## 📞 Next Steps

1. เปิด http://localhost:3001
2. ลอง login ด้วย admin/admin123
3. ถ้าไม่ได้ ส่ง screenshot มาให้ดู
