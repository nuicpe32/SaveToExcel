# Criminal Case Management System - Complete Guide

> ระบบจัดการคดีอาญา สำหรับกองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4

**Version:** 3.7.0
**Status:** Production Ready
**Updated:** October 2025

---

## 📖 Table of Contents

1. [Quick Start](#-quick-start)
2. [Architecture](#-architecture)
3. [Features by Version](#-features-by-version)
4. [Database](#-database)
5. [Development Guide](#-development-guide)
6. [Email System](#-email-system)
7. [CFR System](#-cfr-system)
8. [Master Data](#-master-data)
9. [Deployment](#-deployment)
10. [Backup & Restore](#-backup--restore)
11. [Troubleshooting](#-troubleshooting)
12. [Changelog](#-changelog)

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Installation

```bash
# 1. Clone repository
cd /path/to/SaveToExcel/web-app

# 2. Start all services
docker-compose up -d

# 3. Access the system
# Frontend: http://localhost:3001
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### Default Credentials

```
Username: admin
Password: admin123
```

### Container Names
- `criminal-case-db` - PostgreSQL
- `criminal-case-redis` - Redis
- `criminal-case-backend` - FastAPI (with hot reload)
- `criminal-case-frontend` - React (Vite dev server)

### Common Commands

```bash
# View logs
docker logs criminal-case-backend -f
docker logs criminal-case-frontend -f

# Access database
docker exec -it criminal-case-db psql -U user -d criminal_case_db

# Restart services
docker-compose restart

# Stop all
docker-compose down

# Rebuild
docker-compose up -d --build
```

---

## 🏗️ Architecture

### Tech Stack

**Backend:**
- **Framework:** FastAPI 0.109.0
- **Database:** PostgreSQL 15 (SQLAlchemy ORM)
- **Cache:** Redis 7
- **Authentication:** JWT-based
- **Document Generation:** HTML → PDF (Playwright)
- **Email:** SMTP (Gmail)

**Frontend:**
- **Framework:** React 18 + TypeScript
- **UI Library:** Ant Design 5
- **State Management:** Zustand
- **Build Tool:** Vite 5
- **Date Handling:** Day.js (Thai locale)
- **Charts:** Recharts
- **HTTP Client:** Axios

**Infrastructure:**
- **Containerization:** Docker & Docker Compose
- **Services:** PostgreSQL, Redis, FastAPI, React
- **Hot Reload:** ✅ Backend & Frontend
- **Proxy:** Vite dev proxy for API forwarding

### Project Structure

```
web-app/
├── backend/                     # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/             # API endpoints (36 routers)
│   │   ├── models/             # SQLAlchemy models (27 models)
│   │   ├── schemas/            # Pydantic schemas
│   │   ├── services/           # Business logic
│   │   └── main.py             # Entry point
│   ├── migrations/             # 30 SQL migrations
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                    # React Frontend
│   ├── src/
│   │   ├── pages/              # 10 pages
│   │   ├── components/         # 13 components
│   │   ├── services/           # API client
│   │   └── stores/             # Zustand stores
│   ├── package.json
│   └── Dockerfile.dev
├── docker-compose.yml           # Universal Docker Compose
└── README.md                    # This file
```

---

## ✨ Features by Version

### Version 3.7.0 - Charges Master Data 📋 (Current)

**ฐานข้อมูลข้อหาความผิด:**
- Master Data สำหรับข้อหาความผิดทางอาญา
- จัดการข้อหาใน Master Data Page (Admin only)
- CRUD operations: เพิ่ม/แก้ไข/ลบข้อหา
- ข้อมูลครบถ้วน: ชื่อข้อหา, รายละเอียด, กฎหมาย, อัตราโทษ
- นำเข้าข้อมูลเริ่มต้น 5 รายการจากไฟล์ Excel

**Charges Data Structure:**
- ชื่อข้อหา (charge_name)
- ข้อหา/รายละเอียดเต็ม (charge_description)
- กฎหมายที่เกี่ยวข้อง (related_laws)
- อัตราโทษ (penalty)

### Version 3.6.0 - Email Summons Feature 📧

**ส่งหมายเรียกทางอีเมล์:**
- สร้าง PDF อัตโนมัติและส่งทางอีเมล์
- รองรับ 5 ประเภท: Non-Bank, Payment Gateway, Telco Mobile, Telco Internet, Bank
- Email templates สวยงามพร้อมข้อมูลครบถ้วน
- บันทึกประวัติการส่งใน `email_logs` table

**Email Tracking:**
- Tracking pixel (1x1 transparent GIF)
- บันทึกจำนวนครั้งที่เปิดอ่าน
- บันทึกเวลา (opened_at)
- Real-time tracking status

**ประวัติการส่งอีเมล์:**
- แสดงประวัติทั้งหมด
- สถิติ 4 การ์ด: ส่งทั้งหมด, สำเร็จ, ล้มเหลว, เปิดอ่าน
- Timeline view
- Error messages

### Version 3.5.0 - Master Data Management 🗄️

**จัดการข้อมูล Master Data 6 ประเภท (Admin Only):**
- 🏦 **Banks** - ธนาคาร
- 🏪 **Non-Banks** - บริษัทนอกระบบธนาคาร (TrueMoney, AirPay)
- 💳 **Payment Gateways** - ผู้ให้บริการชำระเงิน (Omise, 2C2P, GB Prime Pay)
- 📱 **Telco Mobile** - ผู้ให้บริการโทรศัพท์ (AIS, True, dtac, NT)
- 🌐 **Telco Internet** - ผู้ให้บริการอินเทอร์เน็ต (TRUE Online, AIS Fibre, 3BB, NT Broadband)
- 🔄 **Exchanges** - ผู้ให้บริการซื้อขายสินทรัพย์ดิจิทัล (Bitkub, Zipmex)

**Features:**
- UI แบบ Tabs พร้อม Modal forms
- Validation ป้องกันการลบข้อมูลที่มี relationships
- Real-time updates

### Version 3.4.0 - Telco Features 📱🌐

**ระบบหมายเลขโทรศัพท์:**
- เพิ่ม/แก้ไข/ลบ ข้อมูลหมายเลขโทรศัพท์
- ออกหมายเรียกข้อมูลโทรศัพท์และซองหมายเรียก
- ดึงข้อมูลผู้ให้บริการจาก Master Data

**ระบบ IP Address:**
- เพิ่ม/แก้ไข/ลบ ข้อมูล IP Address
- ออกหมายเรียกข้อมูล IP และซองหมายเรียก
- ระบุวันเวลาที่ใช้งาน (DateTime)

### Version 3.3.0 - CFR System 📊

**CFR Upload & Management:**
- อัปโหลดไฟล์ CSV CFR (Customer Financial Report)
- แสดงรายการธุรกรรมทั้งหมด
- วิเคราะห์เส้นทางการเงิน

**CFR Flow Chart:**
- แสดงเส้นทางการเงินแบบ Visual Network Graph
- Interactive (ลาก, ซูม, pan)
- บันทึกเป็นรูปภาพ PNG
- ปริ้นได้
- Victim Detection (ตรวจจับบัญชีผู้เสียหายอัตโนมัติ)

### Version 3.2.0 - Payment Gateway & Non-Bank 💳

**Payment Gateway Accounts:**
- จัดการบัญชี Payment Gateway
- ออกหมายเรียกและซองหมายเรียก
- บันทึก Transactions

**Non-Bank Accounts:**
- จัดการบัญชี Non-Bank (TrueMoney, AirPay, etc.)
- ออกหมายเรียกและซองหมายเรียก
- บันทึก Transactions

---

## 🗄️ Database

### Database Information

```
Host:     localhost (outside Docker) / postgres (inside Docker)
Port:     5432
Database: criminal_case_db
Username: user
Password: password123
```

### Core Tables

**Criminal Cases:**
- `criminal_cases` - ข้อมูลคดีหลัก
- `suspects` - ผู้ต้องหา

**Financial Accounts:**
- `bank_accounts` - บัญชีธนาคาร
- `non_bank_accounts` - Non-Bank (TrueMoney, AirPay)
- `payment_gateway_accounts` - Payment Gateway (Omise, 2C2P)
- `telco_mobile_accounts` - หมายเลขโทรศัพท์ 📱
- `telco_internet_accounts` - IP Address 🌐

**Transactions:**
- `non_bank_transactions` - ธุรกรรม Non-Bank
- `payment_gateway_transactions` - ธุรกรรม Payment Gateway

**CFR:**
- `cfr_records` - CFR Records (Customer Financial Report)

**Master Data:**
- `banks` - รายชื่อธนาคาร
- `non_banks` - ผู้ให้บริการ Non-Bank
- `payment_gateways` - ผู้ให้บริการ Payment Gateway
- `telco_mobile` - ผู้ให้บริการโทรศัพท์
- `telco_internet` - ผู้ให้บริการอินเทอร์เน็ต
- `exchanges` - ผู้ให้บริการซื้อขายสินทรัพย์ดิจิทัล
- `charges` - ฐานข้อมูลข้อหาความผิด

**Users & Organization:**
- `users` - ผู้ใช้งานระบบ
- `user_roles` - บทบาท (admin, user)
- `police_ranks` - ยศตำรวจ
- `police_stations` - สถานีตำรวจ
- `bureaus`, `divisions`, `supervisions` - โครงสร้างองค์กร

**Email:**
- `email_logs` - ประวัติการส่งอีเมล์ 📧

### Database Access Methods

**1. psql CLI (เร็วที่สุด):**
```bash
docker exec -it criminal-case-db psql -U user -d criminal_case_db
```

**2. Adminer (แนะนำ):**
```bash
docker-compose --profile tools up -d adminer
# URL: http://localhost:8080
# Server: postgres, User: user, Password: password123
```

**3. pgAdmin:**
```bash
docker-compose --profile tools up -d pgadmin
# URL: http://localhost:5050
# Email: admin@example.com, Password: admin
```

**4. DBeaver (Desktop App):**
- Download: https://dbeaver.io/
- Connection: localhost:5432, criminal_case_db, user, password123

### Common Queries

**ตรวจสอบข้อมูล:**
```sql
SELECT
  (SELECT COUNT(*) FROM criminal_cases) as cases,
  (SELECT COUNT(*) FROM suspects) as suspects,
  (SELECT COUNT(*) FROM bank_accounts) as banks,
  (SELECT COUNT(*) FROM email_logs) as emails;
```

**Export ข้อมูล:**
```bash
docker exec criminal-case-db psql -U user -d criminal_case_db \
  -c "COPY criminal_cases TO STDOUT WITH CSV HEADER" > cases.csv
```

---

## 💻 Development Guide

### Prerequisites
- Docker Desktop
- Node.js 18+ (for local frontend development)
- Python 3.11+ (for local backend development)

### Development Mode

**Start all services:**
```bash
docker-compose up -d
```

**Features:**
- ✅ Hot reload for Backend (FastAPI `--reload`)
- ✅ Hot reload for Frontend (Vite dev server)
- ✅ Volume mounting for source code
- ✅ Auto-restart on changes

### URLs
- **Frontend:** http://localhost:3001
- **Backend API:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **Adminer:** http://localhost:8080 (optional)
- **pgAdmin:** http://localhost:5050 (optional)

### Code Changes

**Frontend changes:**
- แก้ไขไฟล์ใน `frontend/src/`
- Vite จะ hot reload อัตโนมัติ
- ดูผลที่ http://localhost:3001

**Backend changes:**
- แก้ไขไฟล์ใน `backend/app/`
- FastAPI จะ reload อัตโนมัติ
- ดู logs: `docker logs criminal-case-backend -f`

**Database migration:**
```bash
# สร้าง migration ใหม่
docker exec -it criminal-case-backend alembic revision --autogenerate -m "description"

# Run migration
docker exec -it criminal-case-backend alembic upgrade head
```

### Coding Standards

**Python (Backend):**
- snake_case สำหรับ functions/variables
- PascalCase สำหรับ classes
- Type hints ทุกที่
- Docstrings สำหรับ functions สำคัญ

**TypeScript (Frontend):**
- camelCase สำหรับ variables/functions
- PascalCase สำหรับ components/interfaces
- Functional components + hooks
- Props interface สำหรับทุก component

**Database:**
- snake_case สำหรับ tables/columns
- Indexes สำหรับ foreign keys
- Constraints สำหรับ data integrity

---

## 📧 Email System

### Features

**ส่งหมายเรียกทางอีเมล์:**
- สร้าง PDF อัตโนมัติจาก HTML
- ส่งพร้อม attachment
- รองรับ 5 ประเภท: Non-Bank, Payment Gateway, Telco Mobile, Telco Internet, Bank
- Email templates สวยงาม
- CC ให้ผู้ส่งด้วย

**Email Tracking:**
- Tracking pixel (1x1 transparent GIF)
- บันทึก opened_count (จำนวนครั้งที่เปิด)
- บันทึก opened_at (เวลาที่เปิด)
- Real-time status

**ประวัติการส่ง:**
- แสดงประวัติทั้งหมด
- สถิติ: ส่งทั้งหมด, สำเร็จ, ล้มเหลว, เปิดอ่าน
- Timeline view
- Error messages

### How to Use

**1. ตั้งค่า SMTP (ครั้งแรก):**
```bash
# สร้างไฟล์ .env
cd web-app
cp .env.example .env

# แก้ไข .env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4

# Restart
docker-compose restart backend
```

**2. ส่งอีเมล์:**
- Login: http://localhost:3001
- Dashboard → คลิกเลขคดี
- เลือก Tab (Non-Bank, Payment Gateway, ฯลฯ)
- คลิก "📧 ส่งอีเมล์"
- ยืนยันการส่ง

**3. ดูประวัติ:**
- คลิก "📜 ประวัติอีเมล์" (ปุ่มสีม่วง)
- ดูสถิติ 4 การ์ด
- ตารางแสดง Timeline

### API Endpoints

```http
POST /api/v1/emails/send-summons
GET  /api/v1/emails/history/{account_type}/{account_id}
GET  /api/v1/email-tracking/track/{id}.gif
```

### Email Tracking Status

**👁️ เปิดอ่าน (0)** = ยังไม่เปิด
- รอ 1-2 วัน
- เช็คว่าส่งสำเร็จจริง

**👁️ เปิดอ่าน (1-2)** = เปิดแล้ว
- รอการตอบกลับตามกำหนด
- ถ้าผ่าน 3-5 วัน → โทรติดตาม

**👁️ เปิดอ่าน (3+)** = เปิดหลายครั้ง
- กำลังดำเนินการ
- โทรถามความคืบหน้า

---

## 📊 CFR System

### Features

**CFR Upload:**
- อัปโหลดไฟล์ CSV
- แสดงรายการธุรกรรมทั้งหมด
- วิเคราะห์เส้นทางการเงิน

**CFR Flow Chart:**
- Visual Network Graph
- Interactive (ลาก, ซูม, pan)
- บันทึกเป็นรูปภาพ PNG
- ปริ้นได้
- Victim Detection อัตโนมัติ

### Visual Indicators

- 🟦 **กรอบสีน้ำเงิน** = บัญชีธนาคารทั่วไป
- 🟩 **กรอบสีเขียว** = บัญชีผู้เสียหาย
- ➡️ **ลูกศร (animated)** = การโอนเงิน พร้อมจำนวนเงิน

### How to Use

**1. อัปโหลด CFR:**
- Dashboard → คลิกเลขคดี
- Tab "ข้อมูล CFR"
- คลิก "อัปโหลด CFR"
- เลือกไฟล์ CSV → อัปโหลด

**2. แสดงแผนผัง:**
- คลิก "แสดงแผนผังเส้นทางการเงิน"
- ลาก node เพื่อจัดตำแหน่ง
- Scroll เพื่อ zoom
- ดู MiniMap มุมขวาล่าง

**3. Export:**
- บันทึกเป็นรูปภาพ → PNG file (scale 2x)
- ปริ้นแผนผัง → พิมพ์ออกกระดาษ

### Technology

- **ReactFlow** - Node-based diagrams
- **html2canvas** - แปลง DOM เป็นรูปภาพ
- **Ant Design** - UI Components

---

## 🗂️ Master Data

### 7 ประเภทข้อมูล

1. **🏦 Banks** - ธนาคาร
2. **🏪 Non-Banks** - TrueMoney, AirPay, etc.
3. **💳 Payment Gateways** - Omise, 2C2P, GB Prime Pay, etc.
4. **📱 Telco Mobile** - AIS, True, dtac, NT
5. **🌐 Telco Internet** - TRUE Online, AIS Fibre, 3BB, NT Broadband
6. **🔄 Exchanges** - Bitkub, Zipmex, etc.
7. **📋 Charges** - ข้อหาความผิดทางอาญา

### Features

- **Admin Only Access** - เฉพาะ admin เท่านั้น
- **CRUD Operations** - เพิ่ม/แก้ไข/ลบ
- **Relationship Protection** - ป้องกันการลบข้อมูลที่ใช้งานอยู่
- **User-friendly UI** - Tabs + Modal forms
- **Real-time Updates** - อัปเดตทันที

### How to Use

1. **Login ด้วย Admin:** http://localhost:3001 (admin/admin123)
2. **เข้าเมนู:** ระบบผู้ดูแล → จัดการฐานข้อมูล
3. **เลือก Tab:** ธนาคาร, Non-Bank, Payment Gateway, ข้อหาความผิด, ฯลฯ
4. **เพิ่ม/แก้ไข/ลบ:** ใช้ปุ่มใน UI

### API Endpoints

```http
GET    /api/v1/master-data/{type}/
POST   /api/v1/master-data/{type}/
PUT    /api/v1/master-data/{type}/{id}
DELETE /api/v1/master-data/{type}/{id}

# type: banks, non-banks, payment-gateways, telco-mobile, telco-internet, exchanges

# Charges API (separate endpoints)
GET    /api/v1/charges/
POST   /api/v1/charges/
PUT    /api/v1/charges/{id}/
DELETE /api/v1/charges/{id}/
```

---

## 🚀 Deployment

### Option 1: Docker Compose (แนะนำ)

```bash
# 1. Clone repository
git clone <repository-url>
cd web-app

# 2. สร้าง .env file
cp .env.example .env
# แก้ไข .env ตามต้องการ

# 3. Start services
docker-compose up -d --build

# 4. Check status
docker-compose ps
docker logs criminal-case-backend
docker logs criminal-case-frontend
```

### Option 2: Production Server

**Prerequisites:**
- Ubuntu 20.04+
- Docker & Docker Compose
- Nginx
- SSL Certificate (Let's Encrypt)

**Steps:**
```bash
# 1. Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# 2. Install Docker Compose
sudo apt install docker-compose

# 3. Clone & Deploy
git clone <repository-url>
cd web-app
docker-compose up -d --build

# 4. Setup Nginx
sudo nano /etc/nginx/sites-available/criminal-case
# [Configure reverse proxy]

# 5. SSL with Let's Encrypt
sudo certbot --nginx -d your-domain.com
```

### Environment Variables

```bash
# Database
DATABASE_URL=postgresql://user:password123@postgres:5432/criminal_case_db
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your-secret-key-change-this
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=240

# SMTP (Email)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4

# Environment
ENVIRONMENT=production
```

---

## 💾 Backup & Restore

### Database Backup

**Manual Backup:**
```bash
# Backup to file
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c > backup_$(date +%Y%m%d_%H%M%S).dump

# Backup to plain SQL
docker exec criminal-case-db pg_dump -U user -d criminal_case_db > backup_$(date +%Y%m%d_%H%M%S).sql
```

**Automated Backup (Cron):**
```bash
# Add to crontab
0 2 * * * docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c > /backups/backup_$(date +\%Y\%m\%d).dump
```

### Database Restore

**From .dump file:**
```bash
# 1. Copy file to container
docker cp backup_20251001_221353.dump criminal-case-db:/tmp/restore.dump

# 2. Restore
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump

# 3. Verify
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT COUNT(*) FROM criminal_cases;"
```

**From .sql file:**
```bash
docker exec -i criminal-case-db psql -U user -d criminal_case_db < backup.sql
```

### Full System Backup

```bash
# Backup everything
tar -czf web-app-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
  --exclude=node_modules \
  --exclude=__pycache__ \
  --exclude=.git \
  web-app/
```

### Restore Full System

```bash
# Extract
tar -xzf web-app-backup-20251001_221400.tar.gz

# Start
cd web-app
docker-compose up -d

# Restore database
docker cp backup_database_20251001_221353.dump criminal-case-db:/tmp/restore.dump
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

---

## 🔧 Troubleshooting

### Common Issues

**1. Connection Refused (Frontend → Backend)**

**สาเหตุ:** vite.config.ts ใช้ `localhost:8000` แทน `backend:8000`

**แก้ไข:**
```typescript
// frontend/vite.config.ts
proxy: {
  '/api': {
    target: 'http://backend:8000',  // ใช้ Docker service name
    changeOrigin: true,
  },
}
```

**2. Database Connection Failed**

```bash
# Check database status
docker logs criminal-case-db

# Restart database
docker-compose restart postgres

# Check connection
docker exec criminal-case-db psql -U user -d criminal_case_db -c "SELECT 1;"
```

**3. Port Already in Use**

```bash
# Find process using port
sudo lsof -i :8000
sudo lsof -i :3001

# Kill process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
```

**4. Email Not Sending**

```bash
# Check SMTP settings in .env
cat .env | grep SMTP

# Check backend logs
docker logs criminal-case-backend | grep -i smtp

# Test SMTP connection
docker exec -it criminal-case-backend python3 -c "
import smtplib
smtp = smtplib.SMTP('smtp.gmail.com', 587)
smtp.ehlo()
smtp.starttls()
smtp.login('your-email@gmail.com', 'your-app-password')
print('SMTP connection successful!')
smtp.quit()
"
```

**5. Hot Reload Not Working**

```bash
# Restart containers
docker-compose restart

# Check volumes
docker-compose config | grep volumes

# Rebuild
docker-compose up -d --build
```

**6. Out of Memory**

```bash
# Check memory
docker stats

# Add swap (Linux)
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Performance Issues

**Slow Database Queries:**
```sql
-- Check slow queries
SELECT * FROM pg_stat_statements ORDER BY total_time DESC LIMIT 10;

-- Add index
CREATE INDEX idx_criminal_cases_case_number ON criminal_cases(case_number);
```

**Frontend Slow:**
```bash
# Build production
cd frontend
npm run build

# Check bundle size
npm run analyze
```

### Logs

```bash
# View all logs
docker-compose logs -f

# View specific service
docker logs criminal-case-backend -f
docker logs criminal-case-frontend -f
docker logs criminal-case-db -f

# Last 100 lines
docker logs criminal-case-backend --tail 100
```

---

## 📋 Changelog

### Version 3.7.0 (October 2025) - Charges Master Data
- ✨ ฐานข้อมูลข้อหาความผิด (Charges)
- ✨ Master Data Management สำหรับข้อหา
- 📋 CRUD operations ใน Master Data Page
- 🔐 Admin-only access
- 📊 นำเข้าข้อมูลเริ่มต้น 5 รายการ

### Version 3.6.0 (October 2025) - Email Summons
- ✨ ส่งหมายเรียกทางอีเมล์ (5 ประเภท)
- ✨ Email Tracking (Tracking pixel)
- ✨ ประวัติการส่งอีเมล์
- 🔧 User profile + signature upload
- 📧 Email templates สวยงาม

### Version 3.5.0 (October 2025) - Master Data
- ✨ ระบบจัดการ Master Data 6 ประเภท
- 🏦 Banks, Non-Banks, Payment Gateways
- 📱 Telco Mobile, Telco Internet
- 🔄 Crypto Exchanges
- 🔒 Admin-only access

### Version 3.4.0 (October 2025) - Telco
- ✨ ระบบหมายเลขโทรศัพท์
- ✨ ระบบ IP Address
- 📱 Telco Mobile Summons
- 🌐 Telco Internet Summons

### Version 3.3.0 (September 2025) - CFR
- ✨ CFR Upload (CSV)
- ✨ CFR Flow Chart (Visual Network)
- 📊 Interactive Graph
- 💾 Export to PNG

### Version 3.2.0 (September 2025) - Payments
- ✨ Payment Gateway Accounts
- ✨ Non-Bank Accounts
- 💳 Transaction Management
- 📄 Summons Generation

### Version 3.0.0 (August 2025) - Initial Release
- 🎯 Criminal Case Management
- 🏦 Bank Account Management
- 👤 Suspect Management
- 📄 Document Generation
- 🔐 JWT Authentication
- 📊 Dashboard & Statistics

---

## 📞 Support

**For Issues:**
- GitHub Issues: [Repository URL]
- Email: support@example.com

**Documentation:**
- README.md - This file (Complete Guide)
- /CLAUDE.md - AI Assistant Context (in root)

**Version:** 3.7.0
**Last Updated:** October 2025
**Status:** Production Ready ✅

---

**Made with ❤️ by กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4**
