# Criminal Case Management System v3.4.0

ระบบจัดการคดีอาญา สำหรับกองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4

## 🚀 Version 3.4.0 - New Features

### 📱 ระบบหมายเลขโทรศัพท์
- เพิ่ม/แก้ไข/ลบ ข้อมูลหมายเลขโทรศัพท์ที่เกี่ยวข้องกับคดี
- ออกหมายเรียกข้อมูลโทรศัพท์และซองหมายเรียก
- ดึงข้อมูลผู้ให้บริการจาก Master Data (AIS, True, NT)

### 🌐 ระบบ IP Address  
- เพิ่ม/แก้ไข/ลบ ข้อมูล IP Address ที่เกี่ยวข้องกับคดี
- ออกหมายเรียกข้อมูล IP Address และซองหมายเรียก
- ดึงข้อมูลผู้ให้บริการจาก Master Data (TRUE Online, AIS Fibre, 3BB, NT Broadband)
- ระบุวันเวลาที่ใช้งาน (DateTime) แทนช่วงเวลา

## 🏗️ Architecture

### Backend (FastAPI)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **API**: RESTful API with Pydantic validation
- **Document Generation**: HTML-based with Thai date formatting
- **Authentication**: JWT-based authentication

### Frontend (React + TypeScript)
- **UI Library**: Ant Design
- **State Management**: Zustand
- **Date Handling**: Day.js with Thai locale
- **Build Tool**: Vite

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Services**: PostgreSQL, Redis, FastAPI, React
- **Proxy**: Vite dev proxy for API forwarding

## 📊 Database Tables

### Core Tables
- `criminal_cases` - ข้อมูลคดีหลัก
- `users` - ผู้ใช้งานระบบ
- `police_stations` - สถานีตำรวจ

### Financial Tables
- `bank_accounts` - บัญชีธนาคาร
- `non_bank_accounts` - Non-Bank (TrueMoney, etc.)
- `payment_gateway_accounts` - Payment Gateway (Omise, etc.)

### Telecom Tables (New!)
- `telco_mobile_accounts` - หมายเลขโทรศัพท์ ⭐
- `telco_internet_accounts` - IP Address ⭐

### Master Data
- `banks` - ธนาคาร
- `non_banks` - ผู้ให้บริการ Non-Bank
- `payment_gateways` - ผู้ให้บริการ Payment Gateway
- `telco_mobile` - ผู้ให้บริการโทรศัพท์ ⭐
- `telco_internet` - ผู้ให้บริการอินเทอร์เน็ต ⭐

### Other Tables
- `suspects` - ผู้ต้องหา
- `cfr_records` - CFR Records

## 🎯 Key Features

### Dashboard
- แสดงสถิติคดี และกราฟ
- รายการคดีพร้อมการค้นหา/กรอง
- 8 Tabs สำหรับข้อมูลแต่ละประเภท

### Document Generation
- หมายเรียกพยานเอกสาร (HTML)
- ซองหมายเรียก (HTML)
- รายงานคดี (HTML)
- รองรับการพิมพ์โดยตรง

### Data Management
- CRUD operations ครบชุด
- Auto-lookup จาก Master Data
- Status tracking (ตอบกลับ/ยังไม่ตอบกลับ)
- วันที่นับจากส่งเอกสาร

## 🔐 Security
- JWT Authentication
- Role-based access control
- Database relationship constraints
- Input validation with Pydantic

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+ (for development)
- Python 3.11+ (for development)

### Quick Start
```bash
# Clone repository
git clone [repository-url]
cd SaveToExcel/web-app

# Start services
docker-compose up -d

# Access application
# Frontend: http://localhost:3001
# Backend API: http://localhost:8000
```

### Development
```bash
# Backend development
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000

# Frontend development  
cd frontend
npm install
npm run dev
```

## 📱 Usage

### 1. Login
- เข้าสู่ระบบด้วย username/password
- ระบบจะแสดง Dashboard

### 2. จัดการคดี
- ดูรายการคดีทั้งหมด
- คลิกเลขคดีเพื่อดูรายละเอียด
- เพิ่ม/แก้ไข ข้อมูลในแต่ละ Tab

### 3. เพิ่มข้อมูลโทรศัพท์
- Tab "หมายเลขโทรศัพท์"
- คลิก "เพิ่มหมายเลขโทรศัพท์"
- เลือกผู้ให้บริการ + กรอกหมายเลข
- ปริ้นหมายเรียก/ซองได้ทันที

### 4. เพิ่มข้อมูล IP Address
- Tab "IP Address"  
- คลิก "เพิ่ม IP Address"
- เลือกผู้ให้บริการ + กรอก IP
- ระบุวันเวลาที่ใช้งาน
- ปริ้นหมายเรียก/ซองได้ทันที

## 📄 Document Templates

### หมายเรียกโทรศัพท์
- เรื่อง: ขอข้อมูลหมายเลขโทรศัพท์
- รายการเอกสาร: 5 ข้อเฉพาะโทรศัพท์
- ตาราง: ผู้ให้บริการ | หมายเลข | ช่วงเวลา

### หมายเรียก IP Address
- เรื่อง: ขอข้อมูล IP Address
- รายการเอกสาร: 4 ข้อเฉพาะ IP Address
- ตาราง: ผู้ให้บริการ | IP Address | วันเวลาใช้งาน

### ซองหมายเรียก
- ชื่อเต็มผู้ให้บริการ (company_name)
- ที่อยู่ดึงจาก Master Data
- รูปแบบมาตรฐานราชการ

## 🔧 API Endpoints

### Authentication
- `POST /api/v1/auth/login` - เข้าสู่ระบบ
- `POST /api/v1/auth/refresh` - Refresh token

### Criminal Cases
- `GET /api/v1/criminal-cases/` - รายการคดี
- `GET /api/v1/criminal-cases/{id}` - ข้อมูลคดี
- `POST /api/v1/criminal-cases/` - สร้างคดีใหม่

### Telco Mobile (New!)
- `GET /api/v1/telco-mobile-accounts/by-case/{id}` - รายการตามคดี
- `POST /api/v1/telco-mobile-accounts/` - เพิ่มข้อมูล
- `PUT /api/v1/telco-mobile-accounts/{id}` - แก้ไข
- `DELETE /api/v1/telco-mobile-accounts/{id}` - ลบ

### Telco Internet (New!)
- `GET /api/v1/telco-internet-accounts/by-case/{id}` - รายการตามคดี
- `POST /api/v1/telco-internet-accounts/` - เพิ่มข้อมูล
- `PUT /api/v1/telco-internet-accounts/{id}` - แก้ไข
- `DELETE /api/v1/telco-internet-accounts/{id}` - ลบ

### Documents (New!)
- `GET /api/v1/documents/telco-mobile-summons/{id}` - หมายเรียกโทรศัพท์
- `GET /api/v1/documents/telco-mobile-envelope/{id}` - ซองโทรศัพท์
- `GET /api/v1/documents/telco-internet-summons/{id}` - หมายเรียก IP
- `GET /api/v1/documents/telco-internet-envelope/{id}` - ซอง IP

### Master Data
- `GET /api/v1/telco-mobile/` - ผู้ให้บริการโทรศัพท์
- `GET /api/v1/telco-internet/` - ผู้ให้บริการอินเทอร์เน็ต

## 🧪 Testing

### Manual Testing
1. **Refresh Browser**: `Ctrl + Shift + R`
2. **Open Case**: คลิกเลขคดีใดก็ได้
3. **Check New Tabs**: ดู Tab "หมายเลขโทรศัพท์" และ "IP Address"
4. **Add Data**: เพิ่มข้อมูลผ่าน Modal
5. **Print Documents**: ทดสอบปริ้นหมายเรียกและซอง

### API Testing
```bash
# Test Telco Mobile API
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/v1/telco-mobile-accounts/by-case/291

# Test Telco Internet API  
curl -H "Authorization: Bearer {token}" \
  http://localhost:8000/api/v1/telco-internet-accounts/by-case/291
```

## 📝 Migration Files

1. `026_create_telco_mobile_accounts_table.sql`
2. `027_create_telco_internet_accounts_table.sql`  
3. `028_alter_telco_internet_accounts_change_time_period.sql`

## 🎉 What's New in v3.4.0

### 🆕 New Tabs
- 📱 หมายเลขโทรศัพท์ (Phone Numbers)
- 🌐 IP Address

### 🆕 New Documents
- หมายเรียกข้อมูลโทรศัพท์
- หมายเรียกข้อมูล IP Address
- ซองหมายเรียกสำหรับทั้ง 2 ระบบ

### 🆕 New Features
- DateTime Picker สำหรับ IP Address
- Auto-lookup จาก Master Data
- Thai date/datetime formatting
- Status tracking พร้อมนับวัน

---

## 📞 Support

สำหรับข้อสงสัยหรือปัญหาการใช้งาน:
- **ระบบ**: Criminal Case Management System
- **หน่วยงาน**: กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4
- **เวอร์ชัน**: 3.4.0
- **วันที่อัพเดต**: 13 ตุลาคม 2568

---

**🎯 พร้อมใช้งานแล้ว!** 
URL: http://localhost:3001