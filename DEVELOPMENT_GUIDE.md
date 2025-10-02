# คู่มือการพัฒนา - ระบบจัดการคดีอาญา
## Development Guide - Criminal Case Management System

---

## 🎯 ภาพรวม

คู่มือนี้จัดทำขึ้นเพื่อให้ผู้พัฒนาใหม่สามารถเข้าใจและพัฒนาระบบจัดการคดีอาญาต่อได้อย่างมีประสิทธิภาพ

---

## 📋 สารบัญ

- [🏗️ โครงสร้างโปรเจค](#-โครงสร้างโปรเจค)
- [🌐 Web Application Development](#-web-application-development)
- [🖥️ Desktop Application Development](#-desktop-application-development)
- [💾 การจัดการข้อมูล](#-การจัดการข้อมูล)
- [🔧 การตั้งค่า Development Environment](#-การตั้งค่า-development-environment)
- [🧪 การทดสอบ](#-การทดสอบ)
- [📦 การ Deploy](#-การ-deploy)
- [🐛 การแก้ไขปัญหา](#-การแก้ไขปัญหา)
- [📚 แหล่งข้อมูลเพิ่มเติม](#-แหล่งข้อมูลเพิ่มเติม)

---

## 🏗️ โครงสร้างโปรเจค

### 🌐 Web Application (แนะนำ)
```
web-app/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/v1/            # API Endpoints
│   │   ├── core/              # Core Configuration
│   │   ├── models/            # Database Models
│   │   ├── schemas/           # Pydantic Schemas
│   │   ├── services/          # Business Logic
│   │   └── utils/             # Utility Functions
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/        # Reusable Components
│   │   ├── pages/             # Page Components
│   │   ├── services/          # API Services
│   │   ├── stores/            # State Management
│   │   └── App.tsx
│   ├── Dockerfile
│   └── package.json
└── docker-compose.yml
```

### 🖥️ Desktop Application (Legacy)
```
src/
├── config/                    # Configuration
├── data/                      # Data Managers
├── gui/                       # GUI Components
└── utils/                     # Utilities
```

---

## 🌐 Web Application Development

### 🚀 การเริ่มต้น

#### 1. Setup Development Environment
```bash
# Clone repository
git clone https://github.com/nuicpe32/SaveToExcel.git
cd SaveToExcel/web-app

# Start with Docker (แนะนำ)
docker-compose up -d

# หรือ Development Mode
docker-compose -f docker-compose.dev.yml up -d
```

#### 2. เข้าใช้งาน
- **Frontend**: http://localhost:3001
- **Backend API**: http://localhost:8000
- **Database**: localhost:5432

### 🔧 Backend Development (FastAPI)

#### 📁 โครงสร้าง Backend
```
backend/app/
├── api/v1/                    # API Routes
│   ├── auth.py               # Authentication endpoints
│   ├── criminal_cases.py     # Criminal cases CRUD
│   ├── bank_accounts.py      # Bank accounts CRUD
│   └── suspects.py           # Suspects CRUD
├── core/                     # Core Configuration
│   ├── database.py           # Database connection
│   ├── security.py           # JWT authentication
│   └── config.py             # App configuration
├── models/                   # SQLAlchemy Models
│   ├── criminal_case.py      # Criminal case model
│   ├── bank_account.py       # Bank account model
│   ├── suspect.py            # Suspect model
│   └── post_arrest.py        # Post arrest model
├── schemas/                  # Pydantic Schemas
├── services/                 # Business Logic
│   ├── data_migration.py     # Excel to DB migration
│   ├── auth_service.py       # Authentication service
│   └── case_service.py       # Case management service
└── utils/                    # Utility Functions
    ├── date_utils.py         # Date formatting
    ├── case_styling.py       # Case styling logic
    └── thai_date_utils.py    # Thai date utilities
```

#### 🔨 การเพิ่ม API Endpoint ใหม่

1. **สร้าง Model** (ถ้าจำเป็น)
```python
# backend/app/models/new_model.py
from sqlalchemy import Column, Integer, String, DateTime
from app.core.database import Base

class NewModel(Base):
    __tablename__ = "new_models"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

2. **สร้าง Schema**
```python
# backend/app/schemas/new_model.py
from pydantic import BaseModel
from datetime import datetime

class NewModelBase(BaseModel):
    name: str

class NewModelCreate(NewModelBase):
    pass

class NewModelResponse(NewModelBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
```

3. **สร้าง API Router**
```python
# backend/app/api/v1/new_models.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.new_model import NewModel
from app.schemas.new_model import NewModelCreate, NewModelResponse

router = APIRouter()

@router.post("/", response_model=NewModelResponse)
def create_new_model(
    new_model: NewModelCreate,
    db: Session = Depends(get_db)
):
    db_new_model = NewModel(**new_model.dict())
    db.add(db_new_model)
    db.commit()
    db.refresh(db_new_model)
    return db_new_model
```

4. **เพิ่มใน Main App**
```python
# backend/app/main.py
from app.api.v1 import new_models

app.include_router(new_models.router, prefix="/api/v1/new-models", tags=["new-models"])
```

#### 💾 การจัดการข้อมูล

##### Data Migration (Excel → PostgreSQL)
```python
# backend/app/services/data_migration.py
class DataMigration:
    def __init__(self, excel_dir: str = "/app/Xlsx"):
        self.excel_dir = Path(excel_dir)
        self.db = SessionLocal()
    
    def migrate_criminal_cases(self):
        # อ่านข้อมูลจาก Excel และบันทึกลง PostgreSQL
        pass
```

##### การรัน Migration
```bash
# รัน migration
docker-compose exec backend python -m app.services.data_migration

# หรือผ่าน API
curl -X POST http://localhost:8000/api/v1/migrate
```

### 🎨 Frontend Development (React)

#### 📁 โครงสร้าง Frontend
```
frontend/src/
├── components/                # Reusable Components
│   ├── MainLayout.tsx        # Main layout
│   └── ProtectedRoute.tsx    # Route protection
├── pages/                     # Page Components
│   ├── LoginPage.tsx         # Login page
│   ├── DashboardPage.tsx     # Dashboard
│   ├── AddCriminalCasePage.tsx # Add case
│   └── EditCriminalCasePage.tsx # Edit case
├── services/                  # API Services
│   └── api.ts               # API client
├── stores/                    # State Management
│   └── authStore.ts         # Authentication store
└── App.tsx                    # Main app component
```

#### 🔨 การเพิ่ม Page ใหม่

1. **สร้าง Page Component**
```tsx
// frontend/src/pages/NewPage.tsx
import React from 'react';
import { Layout, Card } from 'antd';

const NewPage: React.FC = () => {
  return (
    <Layout style={{ padding: '20px' }}>
      <Card title="New Page">
        <p>Content here</p>
      </Card>
    </Layout>
  );
};

export default NewPage;
```

2. **เพิ่ม Route**
```tsx
// frontend/src/App.tsx
import NewPage from './pages/NewPage';

// ใน Routes
<Route path="new-page" element={<NewPage />} />
```

3. **เพิ่ม Menu Item**
```tsx
// frontend/src/components/MainLayout.tsx
const menuItems = [
  { key: '/', icon: <DashboardOutlined />, label: 'แดชบอร์ด' },
  { key: '/new-page', icon: <NewIcon />, label: 'หน้าใหม่' },
];
```

#### 🔗 การเชื่อมต่อ API

##### API Service
```tsx
// frontend/src/services/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

// เพิ่ม endpoint ใหม่
export const newModelService = {
  getAll: () => api.get('/new-models'),
  create: (data: any) => api.post('/new-models', data),
  update: (id: number, data: any) => api.put(`/new-models/${id}`, data),
  delete: (id: number) => api.delete(`/new-models/${id}`),
};
```

##### การใช้ใน Component
```tsx
// frontend/src/pages/NewPage.tsx
import { useEffect, useState } from 'react';
import { newModelService } from '../services/api';

const NewPage: React.FC = () => {
  const [data, setData] = useState([]);
  
  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await newModelService.getAll();
        setData(response.data);
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    };
    
    fetchData();
  }, []);
  
  return (
    <div>
      {data.map(item => (
        <div key={item.id}>{item.name}</div>
      ))}
    </div>
  );
};
```

---

## 🖥️ Desktop Application Development

### 🚀 การเริ่มต้น

```bash
# รัน Desktop Application
python3 run.py

# หรือใช้ modular version
python3 criminal_case_manager.py

# หรือใช้ legacy version
python3 simple_excel_manager.py
```

### 📁 โครงสร้าง Desktop Application

```
src/
├── config/
│   └── settings.py           # การตั้งค่าทั้งหมด
├── data/                     # Data Management Layer
│   ├── base_data_manager.py  # Base Excel operations
│   ├── bank_data_manager.py  # Bank account operations
│   ├── criminal_data_manager.py # Criminal cases operations
│   ├── summons_data_manager.py  # Summons operations
│   └── arrest_data_manager.py   # Arrest operations
├── gui/                      # GUI Components
│   └── base_gui.py          # Base GUI utilities
└── utils/                    # Utility Functions
    ├── date_utils.py         # Date utilities
    └── string_utils.py       # String utilities
```

### 🔨 การเพิ่ม Data Manager ใหม่

1. **สร้าง Data Manager**
```python
# src/data/new_data_manager.py
from .base_data_manager import BaseDataManager
import pandas as pd

class NewDataManager(BaseDataManager):
    def __init__(self):
        super().__init__()
        self.file_path = "path/to/excel/file.xlsx"
    
    def load_data(self):
        """โหลดข้อมูลจากไฟล์ Excel"""
        try:
            df = pd.read_excel(self.file_path)
            return df
        except Exception as e:
            print(f"Error loading data: {e}")
            return pd.DataFrame()
    
    def save_data(self, data):
        """บันทึกข้อมูลลงไฟล์ Excel"""
        try:
            data.to_excel(self.file_path, index=False)
            return True
        except Exception as e:
            print(f"Error saving data: {e}")
            return False
```

2. **เพิ่มใน Main Application**
```python
# criminal_case_manager.py
from src.data.new_data_manager import NewDataManager

class CriminalCaseManager:
    def __init__(self):
        self.new_manager = NewDataManager()
```

### 🎨 การเพิ่ม GUI Component

1. **สร้าง GUI Component**
```python
# src/gui/new_gui.py
import tkinter as tk
from tkinter import ttk
from .base_gui import BaseGUI

class NewGUI(BaseGUI):
    def __init__(self, parent):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        # สร้าง UI components
        self.label = ttk.Label(self.parent, text="New Component")
        self.label.pack()
        
        self.button = ttk.Button(self.parent, text="Click Me", command=self.on_click)
        self.button.pack()
    
    def on_click(self):
        print("Button clicked!")
```

---

## 💾 การจัดการข้อมูล

### 🌐 Web Application Database

#### PostgreSQL Schema
```sql
-- Criminal Cases Table
CREATE TABLE criminal_cases (
    id SERIAL PRIMARY KEY,
    case_number VARCHAR(255),
    case_id VARCHAR(255),
    status VARCHAR(100) NOT NULL,
    complainant VARCHAR(255) NOT NULL,
    complaint_date DATE,
    complaint_date_thai VARCHAR(100),
    incident_date DATE,
    incident_date_thai VARCHAR(100),
    damage_amount TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Bank Accounts Table
CREATE TABLE bank_accounts (
    id SERIAL PRIMARY KEY,
    criminal_case_id INTEGER REFERENCES criminal_cases(id),
    order_number INTEGER,
    document_number VARCHAR(255),
    document_date DATE,
    document_date_thai VARCHAR(100),
    bank_branch VARCHAR(255),
    bank_name VARCHAR(255),
    account_number VARCHAR(255),
    account_name VARCHAR(255),
    complainant VARCHAR(255),
    reply_status BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Suspects Table
CREATE TABLE suspects (
    id SERIAL PRIMARY KEY,
    criminal_case_id INTEGER REFERENCES criminal_cases(id),
    document_number VARCHAR(255),
    document_date DATE,
    document_date_thai VARCHAR(100),
    suspect_name VARCHAR(255),
    suspect_id_card VARCHAR(255),
    suspect_address TEXT,
    complainant VARCHAR(255),
    reply_status BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### การเชื่อมโยงข้อมูล
```python
# การเชื่อมโยงข้อมูลระหว่าง Tables
def get_related_data(criminal_case_id: int, db: Session):
    case = db.query(CriminalCase).filter(CriminalCase.id == criminal_case_id).first()
    
    # ดึงข้อมูลที่เกี่ยวข้อง
    bank_accounts = db.query(BankAccount).filter(
        BankAccount.criminal_case_id == criminal_case_id
    ).all()
    
    suspects = db.query(Suspect).filter(
        Suspect.criminal_case_id == criminal_case_id
    ).all()
    
    return {
        "case": case,
        "bank_accounts": bank_accounts,
        "suspects": suspects
    }
```

### 🖥️ Desktop Application Data

#### Excel File Structure
```
Xlsx/
├── export_คดีอาญาในความรับผิดชอบ.xlsx    # Criminal cases data
├── หนังสือส่งธนาคารขอข้อมูลบัญชีม้า.xlsx  # Bank accounts data
├── ข้อมูลสำหรับออกหมายเรียกผู้ต้องหา.xlsx  # Suspects data
└── เอกสารหลังการจับกุม.xlsx              # Post arrest data
```

#### การอ่านข้อมูล Excel
```python
import pandas as pd

def read_excel_data(file_path: str):
    """อ่านข้อมูลจากไฟล์ Excel"""
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        print(f"Error reading Excel file: {e}")
        return pd.DataFrame()

def save_excel_data(df: pd.DataFrame, file_path: str):
    """บันทึกข้อมูลลงไฟล์ Excel"""
    try:
        df.to_excel(file_path, index=False)
        return True
    except Exception as e:
        print(f"Error saving Excel file: {e}")
        return False
```

---

## 🔧 การตั้งค่า Development Environment

### 🌐 Web Application Setup

#### 1. Prerequisites
```bash
# ติดตั้ง Docker
# Windows: Docker Desktop
# Linux: Docker Engine
# macOS: Docker Desktop
```

#### 2. Environment Variables
```bash
# backend/.env
DATABASE_URL=postgresql://user:password@postgres:5432/criminal_case_db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

#### 3. Development Commands
```bash
# Start development environment
docker-compose up -d

# View logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Rebuild containers
docker-compose build --no-cache

# Stop all services
docker-compose down

# Remove all containers and volumes
docker-compose down -v
```

#### 4. Development without Docker
```bash
# Backend
cd web-app/backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Frontend
cd web-app/frontend
npm install
npm run dev
```

### 🖥️ Desktop Application Setup

#### 1. Prerequisites
```bash
# Python 3.6+
python --version

# Install dependencies
pip install pandas openpyxl python-docx reportlab
```

#### 2. Development Commands
```bash
# Run main application
python3 run.py

# Run modular version
python3 criminal_case_manager.py

# Run legacy version
python3 simple_excel_manager.py

# Install dependencies
python3 install_dependencies.py
```

---

## 🧪 การทดสอบ

### 🌐 Web Application Testing

#### Backend Testing
```python
# backend/test_api.py
import requests

def test_criminal_cases_api():
    base_url = "http://localhost:8000"
    
    # Test login
    login_data = {
        "username": "admin",
        "password": "admin123"
    }
    
    response = requests.post(f"{base_url}/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test get criminal cases
    response = requests.get(f"{base_url}/api/v1/criminal-cases/", headers=headers)
    assert response.status_code == 200
    
    print("✅ All tests passed!")

if __name__ == "__main__":
    test_criminal_cases_api()
```

#### Frontend Testing
```bash
# Run frontend tests
cd web-app/frontend
npm test

# Run with coverage
npm run test:coverage
```

### 🖥️ Desktop Application Testing

```python
# test_desktop_app.py
import unittest
from src.data.bank_data_manager import BankDataManager

class TestBankDataManager(unittest.TestCase):
    def setUp(self):
        self.manager = BankDataManager()
    
    def test_load_data(self):
        data = self.manager.load_data()
        self.assertIsNotNone(data)
        self.assertGreater(len(data), 0)
    
    def test_save_data(self):
        # Test save functionality
        pass

if __name__ == "__main__":
    unittest.main()
```

---

## 📦 การ Deploy

### 🌐 Web Application Deployment

#### Production Docker Setup
```yaml
# docker-compose.prod.yml
version: '3.8'
services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      SECRET_KEY: ${SECRET_KEY}
    depends_on:
      - postgres
    ports:
      - "8000:8000"

  frontend:
    build: ./frontend
    depends_on:
      - backend
    ports:
      - "80:80"
```

#### Deploy Commands
```bash
# Production deployment
docker-compose -f docker-compose.prod.yml up -d

# With environment variables
export POSTGRES_USER=your_user
export POSTGRES_PASSWORD=your_password
export POSTGRES_DB=your_database
export SECRET_KEY=your_secret_key

docker-compose -f docker-compose.prod.yml up -d
```

### 🖥️ Desktop Application Deployment

#### Build Executable
```bash
# Install PyInstaller
pip install pyinstaller

# Build executable
pyinstaller --onefile --windowed --name="CriminalCaseManager" run.py

# Build with all dependencies
pyinstaller --onefile --windowed --name="CriminalCaseManager" --add-data "src;src" run.py
```

---

## 🐛 การแก้ไขปัญหา

### 🌐 Web Application Issues

#### Common Issues

1. **Database Connection Error**
```bash
# Check database status
docker-compose ps

# Check database logs
docker-compose logs postgres

# Restart database
docker-compose restart postgres
```

2. **Frontend Build Error**
```bash
# Clear node modules
cd web-app/frontend
rm -rf node_modules package-lock.json
npm install

# Rebuild frontend
docker-compose build --no-cache frontend
```

3. **API Authentication Error**
```python
# Check JWT token
import jwt
from datetime import datetime

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        return "Token expired"
    except jwt.InvalidTokenError:
        return "Invalid token"
```

### 🖥️ Desktop Application Issues

#### Common Issues

1. **Excel File Locked**
```python
# Check if file is open in Excel
import os
import psutil

def is_file_locked(file_path):
    for proc in psutil.process_iter(['pid', 'name']):
        if 'excel' in proc.info['name'].lower():
            return True
    return False
```

2. **Module Import Error**
```python
# Add to sys.path
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Or use relative imports
from .src.data.bank_data_manager import BankDataManager
```

---

## 📚 แหล่งข้อมูลเพิ่มเติม

### 🌐 Web Application Resources

#### FastAPI
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)

#### React
- [React Documentation](https://reactjs.org/docs/)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)
- [Ant Design Components](https://ant.design/components/overview/)

#### Docker
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)

### 🖥️ Desktop Application Resources

#### Python GUI
- [tkinter Documentation](https://docs.python.org/3/library/tkinter.html)
- [tkinter Tutorial](https://tkdocs.com/)

#### Data Processing
- [pandas Documentation](https://pandas.pydata.org/docs/)
- [openpyxl Documentation](https://openpyxl.readthedocs.io/)

---

## 🤝 การมีส่วนร่วม

### การรายงานปัญหา
1. สร้าง [Issue](https://github.com/nuicpe32/SaveToExcel/issues) บน GitHub
2. ระบุเวอร์ชันที่ใช้
3. อธิบายขั้นตอนที่ทำให้เกิดปัญหา
4. แนบ error logs (ถ้ามี)

### การเสนอแนะฟีเจอร์
1. สร้าง [Feature Request](https://github.com/nuicpe32/SaveToExcel/issues) บน GitHub
2. อธิบายประโยชน์ของฟีเจอร์
3. แนบ mockup หรือตัวอย่าง (ถ้ามี)

### การส่ง Pull Request
1. Fork repository
2. สร้าง branch ใหม่
3. Commit การเปลี่ยนแปลง
4. ส่ง Pull Request

---

## 📞 การติดต่อ

- **Email**: nui.cpe@gmail.com
- **GitHub**: [nuicpe32/SaveToExcel](https://github.com/nuicpe32/SaveToExcel)
- **Issues**: [GitHub Issues](https://github.com/nuicpe32/SaveToExcel/issues)

---

*📝 คู่มือการพัฒนาฉบับนี้จัดทำขึ้นเพื่อให้ผู้พัฒนาใหม่สามารถเข้าใจและพัฒนาระบบต่อได้อย่างมีประสิทธิภาพ*

*🔄 อัปเดตล่าสุด: ระบบจัดการคดีอาญา v3.0.0*
