# 🚨 สำคัญ: การพัฒนาในช่วงนี้ใช้ Development Server

## ⚠️ **ย้ำเตือน: ใช้ Development Environment เท่านั้น**

### 🎯 **สถานะปัจจุบัน:**
- ✅ **Development Server**: ใช้งานอยู่
- ❌ **Production Server**: ไม่ใช้งาน
- 🔧 **Environment**: `docker-compose.dev.yml`

## 🐳 **Docker Commands ที่ใช้:**

### 1. **Start Development Environment:**
```bash
cd web-app
docker-compose -f docker-compose.dev.yml up -d
```

### 2. **Stop Development Environment:**
```bash
cd web-app
docker-compose -f docker-compose.dev.yml down
```

### 3. **Restart Services:**
```bash
# Backend
docker restart criminal-case-backend-dev

# Frontend
docker restart criminal-case-frontend-dev

# Database
docker restart criminal-case-db-dev
```

### 4. **View Logs:**
```bash
# Backend logs
docker logs criminal-case-backend-dev --tail 50

# Frontend logs
docker logs criminal-case-frontend-dev --tail 50

# Database logs
docker logs criminal-case-db-dev --tail 50
```

## 🌐 **Development URLs:**

| Service | URL | Container |
|---------|-----|-----------|
| **Frontend** | http://localhost:3001 | criminal-case-frontend-dev |
| **Backend API** | http://localhost:8000 | criminal-case-backend-dev |
| **API Docs** | http://localhost:8000/docs | criminal-case-backend-dev |
| **Database** | localhost:5432 | criminal-case-db-dev |
| **pgAdmin** | http://localhost:5050 | pgAdmin container |

## 🔧 **Development Containers:**

### Active Containers:
```bash
docker ps
```

Expected containers:
- ✅ `criminal-case-frontend-dev` (Port: 3001)
- ✅ `criminal-case-backend-dev` (Port: 8000)
- ✅ `criminal-case-db-dev` (Port: 5432)
- ✅ `pgAdmin` (Port: 5050)

## 📝 **Development Workflow:**

### 1. **เริ่มต้นการทำงาน:**
```bash
# 1. ตรวจสอบ containers
docker ps

# 2. ถ้าไม่มี containers ให้ start
cd web-app
docker-compose -f docker-compose.dev.yml up -d

# 3. ตรวจสอบ logs
docker logs criminal-case-backend-dev --tail 10
docker logs criminal-case-frontend-dev --tail 10
```

### 2. **เมื่อมีการแก้ไขโค้ด:**
```bash
# Backend changes - restart backend
docker restart criminal-case-backend-dev

# Frontend changes - restart frontend  
docker restart criminal-case-frontend-dev

# Database changes - restart database
docker restart criminal-case-db-dev
```

### 3. **เมื่อติดตั้ง dependencies ใหม่:**
```bash
# ติดตั้ง Python packages
docker exec criminal-case-backend-dev pip install package_name

# ติดตั้ง Node packages (ถ้าจำเป็น)
docker exec criminal-case-frontend-dev npm install package_name
```

## 🚨 **สิ่งที่ต้องระวัง:**

### 1. **อย่าใช้ Production Commands:**
❌ **ห้ามใช้:**
```bash
docker-compose up -d  # Production
docker-compose -f docker-compose.yml up -d  # Production
```

✅ **ใช้แทน:**
```bash
docker-compose -f docker-compose.dev.yml up -d  # Development
```

### 2. **ตรวจสอบ Environment Variables:**
Development environment ใช้:
- `POSTGRES_DB=criminal_case_db`
- `POSTGRES_USER=user`
- `POSTGRES_PASSWORD=password123`
- `DEBUG=True`
- `ENVIRONMENT=development`

### 3. **Database Connection:**
Development database:
- **Host**: `criminal-case-db-dev` (container name)
- **Port**: `5432`
- **Database**: `criminal_case_db`
- **Username**: `user`
- **Password**: `password123`

## 🔍 **การตรวจสอบ Development Environment:**

### 1. **ตรวจสอบ Services:**
```bash
# ตรวจสอบ containers
docker ps | grep dev

# ตรวจสอบ ports
netstat -tulpn | grep :3001  # Frontend
netstat -tulpn | grep :8000  # Backend
netstat -tulpn | grep :5432  # Database
```

### 2. **ทดสอบ API:**
```bash
# Health check
curl http://localhost:8000/health

# API docs
curl http://localhost:8000/docs
```

### 3. **ทดสอบ Frontend:**
- เปิด browser: http://localhost:3001
- ตรวจสอบ console logs ใน Developer Tools

## 📊 **Development Features:**

### 1. **Hot Reload:**
- ✅ **Backend**: Auto-reload เมื่อแก้ไข Python files
- ✅ **Frontend**: Auto-reload เมื่อแก้ไข React files

### 2. **Debug Mode:**
- ✅ **Backend**: Debug logging enabled
- ✅ **Database**: Development data
- ✅ **API**: Detailed error messages

### 3. **Development Tools:**
- ✅ **pgAdmin**: Database management
- ✅ **API Docs**: Swagger documentation
- ✅ **Logs**: Detailed logging

## 🚀 **การ Deploy ไป Production:**

### เมื่อพร้อม Deploy:
1. **เปลี่ยนไปใช้ Production Environment:**
```bash
docker-compose -f docker-compose.yml up -d
```

2. **อัพเดต Environment Variables:**
- เปลี่ยน `DEBUG=False`
- เปลี่ยน `ENVIRONMENT=production`

3. **ตรวจสอบ Production URLs:**
- Frontend: Production URL
- Backend: Production API URL

## 📝 **สรุป:**

### ✅ **สิ่งที่ต้องจำ:**
1. **ใช้ `docker-compose.dev.yml` เสมอ**
2. **URLs ใช้ localhost ports**
3. **Container names มี `-dev` suffix**
4. **Debug mode เปิดอยู่**
5. **ใช้ development database**

### 🚨 **สิ่งที่ห้ามทำ:**
1. **ห้ามใช้ production docker-compose**
2. **ห้ามใช้ production database**
3. **ห้าม deploy ไป production ยัง**
4. **ห้ามเปลี่ยน environment variables**

---

**🎯 สรุป: การพัฒนาในช่วงนี้ใช้ Development Server เท่านั้น!**

**Environment**: `docker-compose.dev.yml`  
**Containers**: `*-dev` suffix  
**URLs**: `localhost` ports  
**Mode**: Development/Debug
