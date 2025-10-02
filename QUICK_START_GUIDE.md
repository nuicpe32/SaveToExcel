# 🚀 Quick Start Guide - SaveToExcel v3.1.1

## 📋 สิ่งที่ต้องเตรียม

### Prerequisites:
- ✅ Docker & Docker Compose
- ✅ Git
- ✅ Internet connection

## 🏃‍♂️ การเริ่มต้นใช้งาน

### 1. Clone และ Setup:
```bash
git clone https://github.com/nuicpe32/SaveToExcel.git
cd SaveToExcel
```

### 2. Start Development Environment:
```bash
cd web-app
docker-compose -f docker-compose.dev.yml up -d
```

### 3. Install Dependencies:
```bash
docker exec criminal-case-backend-dev pip install requests==2.31.0 beautifulsoup4==4.12.2
```

### 4. Restart Services:
```bash
docker restart criminal-case-backend-dev criminal-case-frontend-dev
```

### 5. Verify Everything is Running:
```bash
docker ps
```

## 🌐 URLs ที่สำคัญ

| Service | URL | Description |
|---------|-----|-------------|
| **Frontend** | http://localhost:3001 | React Web App |
| **Backend API** | http://localhost:8000 | FastAPI Backend |
| **API Docs** | http://localhost:8000/docs | Swagger Documentation |
| **pgAdmin** | http://localhost:5050 | Database Management |

## 🎯 ฟีเจอร์หลักที่ใช้งานได้

### 1. ระบบตรวจสอบที่อยู่จาก PDF:
- อัปโหลดไฟล์ PDF ทร.14
- ระบบจะตรวจสอบความถูกต้องของที่อยู่
- แสดงแจ้งเตือนหากข้อมูลไม่ถูกต้อง

### 2. ระบบค้นหาสถานีตำรวจ:
- กรอกที่อยู่ผู้ต้องหา
- คลิกปุ่ม "ค้นหาสถานีตำรวจ"
- เลือกสถานีตำรวจจากรายการ
- ข้อมูลจะถูกกรอกอัตโนมัติ

## 🔧 การแก้ไขปัญหาทั่วไป

### 1. Container ไม่ทำงาน:
```bash
# ตรวจสอบสถานะ
docker ps -a

# เริ่มใหม่
docker-compose -f docker-compose.dev.yml restart

# ดู logs
docker logs criminal-case-backend-dev
```

### 2. API ไม่ตอบสนอง:
```bash
# ตรวจสอบ backend
curl http://localhost:8000/health

# ตรวจสอบ database
docker exec criminal-case-db-dev pg_isready
```

### 3. Frontend ไม่โหลด:
```bash
# ตรวจสอบ frontend container
docker logs criminal-case-frontend-dev

# Restart frontend
docker restart criminal-case-frontend-dev
```

### 4. Dependencies ไม่ครบ:
```bash
# ติดตั้ง dependencies ใหม่
docker exec criminal-case-backend-dev pip install -r requirements.txt
```

## 📊 การทดสอบระบบ

### 1. ทดสอบ PDF Parsing:
1. ไปที่ Frontend (http://localhost:3001)
2. เข้าไปที่ "เพิ่มผู้ต้องหา"
3. อัปโหลดไฟล์ PDF ทร.14
4. ตรวจสอบว่าข้อมูลถูกกรอกอัตโนมัติ

### 2. ทดสอบ Police Station Search:
1. กรอกที่อยู่ผู้ต้องหา
2. คลิกปุ่ม "ค้นหาสถานีตำรวจ"
3. เลือกสถานีตำรวจจากรายการ
4. ตรวจสอบว่าข้อมูลถูกกรอกอัตโนมัติ

### 3. ทดสอบ API:
```bash
# ทดสอบ PDF parsing API
curl -X POST "http://localhost:8000/api/v1/parse-pdf-thor14" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@test.pdf"

# ทดสอบ Police Station Search API
curl -X POST "http://localhost:8000/api/v1/police-stations/search" \
  -H "Content-Type: application/json" \
  -d '{"address": "จังหวัดกาญจนบุรี"}'
```

## 📝 การพัฒนาเพิ่มเติม

### 1. เพิ่มข้อมูลสถานีตำรวจ:
แก้ไขไฟล์: `web-app/backend/app/services/police_station_service.py`
```python
# เพิ่มในฟังก์ชัน _get_real_police_stations
'จังหวัดใหม่': [
    {
        'name': 'สถานีตำรวจภูธรจังหวัดใหม่',
        'address': 'ที่อยู่จริง',
        'phone': 'เบอร์โทรจริง',
        'district': 'อำเภอ',
        'province': 'จังหวัด'
    }
]
```

### 2. ปรับปรุง PDF Parsing:
แก้ไขไฟล์: `web-app/backend/app/services/pdf_parser.py`
```python
# เพิ่ม regex patterns ใหม่ในฟังก์ชัน _extract_address
new_pattern = r'รูปแบบใหม่ที่ต้องการ'
```

### 3. เพิ่มฟีเจอร์ใหม่:
1. สร้าง Component ใหม่ใน `web-app/frontend/src/components/`
2. สร้าง API endpoint ใหม่ใน `web-app/backend/app/api/v1/`
3. เพิ่ม router ใน `web-app/backend/app/api/v1/__init__.py`

## 🗂️ โครงสร้างไฟล์ที่สำคัญ

```
web-app/
├── frontend/src/components/
│   ├── SuspectFormModal.tsx          # ฟอร์มผู้ต้องหา
│   └── PoliceStationSearchModal.tsx  # Modal ค้นหาสถานีตำรวจ
├── backend/app/
│   ├── services/
│   │   ├── pdf_parser.py             # ระบบแกะข้อมูล PDF
│   │   └── police_station_service.py # ระบบค้นหาสถานีตำรวจ
│   └── api/v1/
│       ├── pdf_parser.py             # API แกะข้อมูล PDF
│       └── police_stations.py        # API ค้นหาสถานีตำรวจ
└── docker-compose.dev.yml            # Docker configuration
```

## 📞 การขอความช่วยเหลือ

### 1. ตรวจสอบ Logs:
```bash
# Backend logs
docker logs criminal-case-backend-dev --tail 50

# Frontend logs  
docker logs criminal-case-frontend-dev --tail 50

# Database logs
docker logs criminal-case-db-dev --tail 50
```

### 2. ตรวจสอบ Network:
```bash
# ตรวจสอบ ports
netstat -tulpn | grep :3001
netstat -tulpn | grep :8000
netstat -tulpn | grep :5432
```

### 3. ตรวจสอบ Resources:
```bash
# ตรวจสอบ disk space
df -h

# ตรวจสอบ memory
free -h

# ตรวจสอบ docker resources
docker system df
```

## 🎯 สรุป

**SaveToExcel v3.1.1** เป็นระบบจัดการคดีอาญาที่มีฟีเจอร์:
- ✅ ระบบตรวจสอบที่อยู่จาก PDF
- ✅ ระบบค้นหาสถานีตำรวจ
- ✅ ข้อมูลสถานีตำรวจจริง
- ✅ User Experience ที่ดีขึ้น

**พร้อมใช้งานและสามารถพัฒนาต่อได้!** 🚀
