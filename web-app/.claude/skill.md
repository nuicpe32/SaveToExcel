# Criminal Case Management System - Development Guide

> **Version:** 3.6.0
> **Last Updated:** 19 October 2025
> **For:** AI Assistants & Developers

---

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Tech Stack](#2-tech-stack)
3. [File Structure](#3-file-structure)
4. [Naming Conventions](#4-naming-conventions)
5. [Backend Patterns](#5-backend-patterns)
6. [Frontend Patterns](#6-frontend-patterns)
7. [Database Patterns](#7-database-patterns)
8. [API Design Patterns](#8-api-design-patterns)
9. [State Management](#9-state-management)
10. [Error Handling](#10-error-handling)
11. [Development Workflow](#11-development-workflow)
12. [Code Examples](#12-code-examples)
13. [Testing Guidelines](#13-testing-guidelines)
14. [Common Pitfalls](#14-common-pitfalls)

---

## 1. Project Overview

### Purpose
ระบบจัดการคดีอาญา (Criminal Case Management System) สำหรับกองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4

### Core Features
- **Case Management** - จัดการคดีอาญา (Criminal Cases)
- **Suspect Management** - จัดการผู้ต้องหา (Suspects)
- **Financial Tracking** - ติดตามบัญชีธนาคาร, Non-Bank, Payment Gateway, Telco
- **Document Generation** - สร้างหมายจับ/หนังสือทางราชการอัตโนมัติ (Word documents)
- **Email System** - ส่งหมายจับทางอีเมลพร้อมระบบติดตาม (v3.6.0)
- **CFR System** - Customer Financial Report with Flow Chart visualization (v3.3.0)
- **Master Data Management** - จัดการข้อมูลหลัก 6 ประเภท (v3.5.0)
- **Access Control** - Role-based access control (RBAC)

### User Roles
- **Admin** - Full access to all features
- **User** - Limited to own cases only

---

## 2. Tech Stack

### Backend
- **Framework:** FastAPI 0.109.0
- **ORM:** SQLAlchemy 2.0+
- **Validation:** Pydantic 2.0+
- **Database:** PostgreSQL 15
- **Cache:** Redis
- **Authentication:** JWT (HS256)
- **Email:** SMTP (Gmail)
- **Document Generation:** python-docx

### Frontend
- **Framework:** React 18.2.0
- **Language:** TypeScript 5.2.2
- **Build Tool:** Vite 5.0.8
- **UI Library:** Ant Design 5.12.8
- **State Management:** Zustand 4.4.7 + Zustand Persist
- **HTTP Client:** Axios 1.6.5
- **Date Library:** Day.js 1.11.10
- **Routing:** React Router DOM 6.21.2

### DevOps
- **Container:** Docker + Docker Compose (Universal Mode)
- **Hot Reload:** Enabled for both backend and frontend
- **Database Tools:** pgAdmin, Adminer (optional via `--profile tools`)

---

## 3. File Structure

### Backend Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py                      # FastAPI app entry point
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py                # Settings (Pydantic BaseSettings)
│   │   ├── database.py              # Database connection & session
│   │   └── security.py              # JWT & password hashing
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py          # Router aggregation
│   │       ├── auth.py              # Authentication endpoints
│   │       ├── criminal_cases.py    # CRUD for criminal cases
│   │       ├── suspects.py          # CRUD for suspects
│   │       ├── bank_accounts.py     # CRUD for bank accounts
│   │       ├── emails.py            # Email sending (v3.6.0)
│   │       ├── email_tracking.py    # Email tracking pixel
│   │       ├── cfr_upload.py        # CFR upload & parsing
│   │       ├── documents.py         # Word document generation
│   │       └── endpoints/           # Master data endpoints
│   │           ├── banks.py
│   │           ├── non_banks.py
│   │           ├── payment_gateways.py
│   │           ├── telco_mobile.py
│   │           ├── telco_internet.py
│   │           └── exchanges.py
│   ├── models/
│   │   ├── __init__.py              # Export all models
│   │   ├── user.py                  # User, PoliceRank, UserRole
│   │   ├── criminal_case.py         # CriminalCase model
│   │   ├── suspect.py               # Suspect model
│   │   ├── bank_account.py          # BankAccount model
│   │   ├── email_log.py             # EmailLog model (v3.6.0)
│   │   └── master_data.py           # Bank, NonBank, etc.
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── criminal_case.py         # Pydantic schemas
│   │   ├── suspect.py
│   │   ├── bank_account.py
│   │   └── email.py                 # Email schemas (v3.6.0)
│   ├── services/
│   │   ├── bank_summons_generator.py          # Word doc generation
│   │   ├── non_bank_summons_generator.py
│   │   ├── payment_gateway_summons_generator.py
│   │   ├── telco_mobile_summons_generator.py
│   │   ├── telco_internet_summons_generator.py
│   │   ├── email_service.py                   # Email service (v3.6.0)
│   │   └── case_report_generator.py           # CFR processing
│   └── utils/
│       ├── string_utils.py          # String manipulation
│       ├── case_styling.py          # Row styling logic
│       ├── case_number_generator.py # Auto case number
│       └── virtual_fields.py        # Computed fields
├── migrations/                       # SQL migration files
│   ├── 001_initial_schema.sql
│   ├── 029_create_email_logs_table.sql
│   └── 030_add_signature_to_users.sql
├── requirements.txt
└── Dockerfile
```

### Frontend Structure

```
frontend/
├── src/
│   ├── main.tsx                     # React app entry point
│   ├── App.tsx                      # App component with routing
│   ├── pages/
│   │   ├── LoginPage.tsx            # Login page
│   │   ├── DashboardPage.tsx        # Main dashboard (case list)
│   │   ├── AddCriminalCasePage.tsx  # Add new case form
│   │   ├── EditCriminalCasePage.tsx # Edit case form
│   │   ├── CriminalCaseDetailPage.tsx # Case detail view
│   │   ├── SuspectsPage.tsx         # Suspects management
│   │   ├── BankAccountsPage.tsx     # Bank accounts list
│   │   ├── MasterDataPage.tsx       # Master data CRUD (v3.5.0)
│   │   ├── ProfilePage.tsx          # User profile & signature
│   │   └── AdminUsersPage.tsx       # User management (admin only)
│   ├── components/
│   │   ├── MainLayout.tsx           # Layout with sidebar
│   │   ├── BankAccountFormModal.tsx # Bank account form
│   │   ├── SuspectFormModal.tsx     # Suspect form
│   │   ├── EmailConfirmationModal.tsx # Email preview (v3.6.0)
│   │   ├── EmailHistoryModal.tsx    # Email history (v3.6.0)
│   │   ├── CfrFlowChart.tsx         # CFR flow chart (v3.3.0)
│   │   └── PoliceStationSearchModal.tsx # Police station search
│   ├── services/
│   │   └── api.ts                   # Axios instance with interceptors
│   ├── stores/
│   │   └── authStore.ts             # Zustand auth store
│   ├── contexts/
│   │   └── ThemeContext.tsx         # Theme context (unused currently)
│   └── vite-env.d.ts
├── public/
├── index.html
├── package.json
├── tsconfig.json
└── vite.config.ts                   # Vite config with proxy
```

---

## 4. Naming Conventions

### Backend (Python)

#### Files & Modules
- **Files:** `snake_case.py` (e.g., `criminal_case.py`, `bank_account.py`)
- **Folders:** `snake_case/` (e.g., `api/`, `services/`)

#### Classes
- **Models:** `PascalCase` (e.g., `CriminalCase`, `BankAccount`, `User`)
- **Schemas:** `PascalCase` with suffix (e.g., `CriminalCaseCreate`, `CriminalCaseUpdate`, `CriminalCaseResponse`)
- **Services:** `PascalCase` (rare, mostly functions)

#### Functions & Variables
- **Functions:** `snake_case` (e.g., `create_criminal_case`, `get_current_user`)
- **Variables:** `snake_case` (e.g., `db_case`, `current_user`, `access_token`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `ACCESS_TOKEN_EXPIRE_MINUTES`, `THAI_BANKS`)

#### Database
- **Tables:** `snake_case` plural (e.g., `criminal_cases`, `bank_accounts`, `users`)
- **Columns:** `snake_case` (e.g., `case_number`, `account_name`, `created_at`)
- **Relationships:** `snake_case` plural (e.g., `bank_accounts`, `suspects`)

### Frontend (TypeScript/React)

#### Files
- **Components:** `PascalCase.tsx` (e.g., `DashboardPage.tsx`, `BankAccountFormModal.tsx`)
- **Services:** `camelCase.ts` (e.g., `api.ts`)
- **Stores:** `camelCase.ts` (e.g., `authStore.ts`)
- **Contexts:** `PascalCase.tsx` (e.g., `ThemeContext.tsx`)

#### Components
- **Component Names:** `PascalCase` (e.g., `DashboardPage`, `MainLayout`)
- **Props Interfaces:** `PascalCase` + `Props` suffix (e.g., `BankAccountFormModalProps`)

#### Functions & Variables
- **Functions:** `camelCase` (e.g., `handleSubmit`, `fetchCases`)
- **Event Handlers:** `handle` + `EventName` (e.g., `handleClick`, `handleDelete`)
- **Variables:** `camelCase` (e.g., `criminalCases`, `isLoading`, `selectedRecord`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `THAI_BANKS`, `API_BASE_URL`)

#### Interfaces/Types
- **Interfaces:** `PascalCase` (e.g., `BankAccount`, `CriminalCase`, `User`)
- **Type Aliases:** `PascalCase` (e.g., `AuthState`)

---

## 5. Backend Patterns

### 5.1 API Router Pattern

**Location:** `backend/app/api/v1/*.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core import get_db
from app.models import CriminalCase, User
from app.schemas import CriminalCaseCreate, CriminalCaseResponse
from app.api.v1.auth import get_current_user

router = APIRouter()

# CREATE
@router.post("/", response_model=CriminalCaseResponse, status_code=201)
def create_criminal_case(
    criminal_case: CriminalCaseCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validation
    db_case = db.query(CriminalCase).filter(
        CriminalCase.case_number == criminal_case.case_number
    ).first()
    if db_case:
        raise HTTPException(status_code=400, detail="Case already exists")

    # Create
    db_case = CriminalCase(
        **criminal_case.dict(),
        created_by=current_user.id,
        owner_id=current_user.id
    )
    db.add(db_case)
    db.commit()
    db.refresh(db_case)

    return db_case

# READ (List)
@router.get("/", response_model=List[CriminalCaseResponse])
def read_criminal_cases(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(CriminalCase)

    # RBAC: Non-admin users see only their own cases
    if current_user.role.role_name != "admin":
        query = query.filter(CriminalCase.owner_id == current_user.id)

    return query.offset(skip).limit(limit).all()

# READ (Single)
@router.get("/{case_id}", response_model=CriminalCaseResponse)
def read_criminal_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # RBAC: Check ownership
    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return case

# UPDATE
@router.put("/{case_id}", response_model=CriminalCaseResponse)
def update_criminal_case(
    case_id: int,
    criminal_case: CriminalCaseUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # RBAC: Check ownership
    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update
    for key, value in criminal_case.dict(exclude_unset=True).items():
        setattr(case, key, value)

    db.commit()
    db.refresh(case)
    return case

# DELETE
@router.delete("/{case_id}", status_code=204)
def delete_criminal_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # RBAC: Check ownership
    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(case)
    db.commit()
    return None
```

### 5.2 Model Pattern (SQLAlchemy)

**Location:** `backend/app/models/*.py`

```python
from sqlalchemy import Column, Integer, String, DateTime, Date, ForeignKey, Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from app.core.database import Base

class CriminalCase(Base):
    __tablename__ = "criminal_cases"

    # Primary Key
    id = Column(Integer, primary_key=True, index=True)

    # Unique Fields
    case_number = Column(String, unique=True, index=True, nullable=False)
    case_id = Column(String, index=True, nullable=True)

    # Status
    status = Column(String, default="ระหว่างสอบสวน")

    # Data Fields
    complainant = Column(String)
    case_type = Column(String)
    damage_amount = Column(String)

    # Dates
    complaint_date = Column(Date)
    incident_date = Column(Date)
    last_update_date = Column(Date)

    # Metadata
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    created_by = Column(Integer)

    # Foreign Keys
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)

    # Relationships (cascade="all, delete-orphan" for auto-delete)
    bank_accounts = relationship("BankAccount", back_populates="criminal_case", cascade="all, delete-orphan")
    suspects = relationship("Suspect", back_populates="criminal_case", cascade="all, delete-orphan")
    owner = relationship("User", foreign_keys=[owner_id])
```

### 5.3 Schema Pattern (Pydantic)

**Location:** `backend/app/schemas/*.py`

```python
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, date

# Base Schema (shared fields)
class CriminalCaseBase(BaseModel):
    case_number: Optional[str] = None
    case_id: Optional[str] = None
    status: Optional[str] = "ระหว่างสอบสวน"
    complainant: Optional[str] = None
    case_type: Optional[str] = None
    damage_amount: Optional[str] = None
    complaint_date: Optional[date] = None
    incident_date: Optional[date] = None
    court_name: Optional[str] = None

# Create Schema (required fields for creation)
class CriminalCaseCreate(BaseModel):
    case_number: str  # Required
    case_id: str  # Required
    complainant: str  # Required
    complaint_date: date  # Required
    status: str
    case_type: Optional[str] = None
    damage_amount: Optional[str] = None
    incident_date: Optional[date] = None
    court_name: Optional[str] = None

# Update Schema (all fields optional)
class CriminalCaseUpdate(BaseModel):
    case_id: Optional[str] = None
    status: Optional[str] = None
    complainant: Optional[str] = None
    case_type: Optional[str] = None
    damage_amount: Optional[str] = None
    complaint_date: Optional[date] = None
    incident_date: Optional[date] = None
    court_name: Optional[str] = None

# Response Schema (all fields from DB + virtual fields)
class CriminalCaseResponse(CriminalCaseBase):
    id: int
    created_at: datetime
    last_update_date: Optional[date] = None

    # Virtual fields (computed at runtime)
    bank_accounts_count: Optional[str] = "0/0"
    suspects_count: Optional[str] = "0/0"
    complaint_date_thai: Optional[str] = None
    incident_date_thai: Optional[str] = None
    row_class: Optional[str] = ""
    row_style: Optional[dict] = {}

    # Related data
    owner_id: Optional[int] = None
    owner: Optional['CaseOwnerInfo'] = None

    class Config:
        from_attributes = True  # Pydantic v2 (was orm_mode in v1)
```

### 5.4 Authentication Pattern (JWT)

**Location:** `backend/app/api/v1/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
from datetime import datetime, timedelta
from app.core import get_db, settings
from app.core.security import verify_password, get_password_hash
from app.models import User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise credentials_exception

    if not user.is_active or not user.is_approved:
        raise HTTPException(status_code=403, detail="User is inactive or not approved")

    return user

@router.post("/login")
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == form_data.username).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Incorrect username or password")

    if not user.is_active or not user.is_approved:
        raise HTTPException(status_code=403, detail="User is inactive or not approved")

    access_token = create_access_token(data={"sub": user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "username": user.username,
            "email": user.email,
            "full_name": user.full_name,
            "role": user.role.role_name if user.role else None
        }
    }
```

---

## 6. Frontend Patterns

### 6.1 Page Component Pattern

**Location:** `frontend/src/pages/*.tsx`

```typescript
import { useState, useEffect } from 'react'
import { Table, Button, message, Space } from 'antd'
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons'
import { useNavigate } from 'react-router-dom'
import type { ColumnsType } from 'antd/es/table'
import api from '../services/api'
import { useAuthStore } from '../stores/authStore'

interface CriminalCase {
  id: number
  case_number: string
  case_id: string
  complainant: string
  complaint_date: string
  status: string
}

export default function DashboardPage() {
  const navigate = useNavigate()
  const { user } = useAuthStore()
  const [cases, setCases] = useState<CriminalCase[]>([])
  const [loading, setLoading] = useState(false)

  // Fetch data on mount
  useEffect(() => {
    fetchCases()
  }, [])

  const fetchCases = async () => {
    try {
      setLoading(true)
      const response = await api.get('/criminal-cases/')
      setCases(response.data)
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Failed to load cases')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    try {
      await api.delete(`/criminal-cases/${id}`)
      message.success('ลบคดีสำเร็จ')
      fetchCases() // Refresh list
    } catch (error: any) {
      message.error(error.response?.data?.detail || 'Failed to delete case')
    }
  }

  const columns: ColumnsType<CriminalCase> = [
    {
      title: 'หมายเลขคดี',
      dataIndex: 'case_number',
      key: 'case_number',
    },
    {
      title: 'Case ID',
      dataIndex: 'case_id',
      key: 'case_id',
    },
    {
      title: 'ผู้ร้อง',
      dataIndex: 'complainant',
      key: 'complainant',
    },
    {
      title: 'วันที่แจ้งความ',
      dataIndex: 'complaint_date',
      key: 'complaint_date',
    },
    {
      title: 'สถานะ',
      dataIndex: 'status',
      key: 'status',
    },
    {
      title: 'การดำเนินการ',
      key: 'action',
      render: (_, record) => (
        <Space size="small">
          <Button
            type="link"
            icon={<EditOutlined />}
            onClick={() => navigate(`/cases/edit/${record.id}`)}
          >
            แก้ไข
          </Button>
          <Button
            type="link"
            danger
            icon={<DeleteOutlined />}
            onClick={() => handleDelete(record.id)}
          >
            ลบ
          </Button>
        </Space>
      ),
    },
  ]

  return (
    <div>
      <div style={{ marginBottom: 16 }}>
        <Button
          type="primary"
          icon={<PlusOutlined />}
          onClick={() => navigate('/cases/add')}
        >
          เพิ่มคดีใหม่
        </Button>
      </div>

      <Table
        columns={columns}
        dataSource={cases}
        loading={loading}
        rowKey="id"
      />
    </div>
  )
}
```

### 6.2 Modal Component Pattern

**Location:** `frontend/src/components/*FormModal.tsx`

```typescript
import { useEffect } from 'react'
import { Modal, Form, Input, DatePicker, Select, message } from 'antd'
import dayjs from 'dayjs'
import api from '../services/api'

interface BankAccountFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

export default function BankAccountFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: BankAccountFormModalProps) {
  const [form] = Form.useForm()
  const isEdit = !!editingRecord

  // Populate form when editing
  useEffect(() => {
    if (editingRecord) {
      form.setFieldsValue({
        ...editingRecord,
        document_date: editingRecord.document_date ? dayjs(editingRecord.document_date) : null,
      })
    } else {
      form.resetFields()
    }
  }, [editingRecord, form])

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()

      // Transform dates to ISO format
      const payload = {
        ...values,
        document_date: values.document_date?.format('YYYY-MM-DD'),
        criminal_case_id: criminalCaseId,
      }

      if (isEdit) {
        await api.put(`/bank-accounts/${editingRecord.id}`, payload)
        message.success('แก้ไขบัญชีธนาคารสำเร็จ')
      } else {
        await api.post('/bank-accounts/', payload)
        message.success('เพิ่มบัญชีธนาคารสำเร็จ')
      }

      onClose(true) // Signal success
    } catch (error: any) {
      if (error.errorFields) {
        // Form validation error
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else {
        // API error
        message.error(error.response?.data?.detail || 'เกิดข้อผิดพลาด')
      }
    }
  }

  return (
    <Modal
      title={isEdit ? 'แก้ไขบัญชีธนาคาร' : 'เพิ่มบัญชีธนาคาร'}
      open={visible}
      onOk={handleSubmit}
      onCancel={() => onClose(false)}
      width={800}
      okText="บันทึก"
      cancelText="ยกเลิก"
    >
      <Form
        form={form}
        layout="vertical"
        initialValues={{ reply_status: false }}
      >
        <Form.Item
          label="ชื่อธนาคาร"
          name="bank_name"
          rules={[{ required: true, message: 'กรุณากรอกชื่อธนาคาร' }]}
        >
          <Select showSearch placeholder="เลือกธนาคาร">
            <Select.Option value="ธนาคารกรุงเทพ">ธนาคารกรุงเทพ</Select.Option>
            <Select.Option value="ธนาคารกสิกรไทย">ธนาคารกสิกรไทย</Select.Option>
            <Select.Option value="ธนาคารไทยพาณิชย์">ธนาคารไทยพาณิชย์</Select.Option>
          </Select>
        </Form.Item>

        <Form.Item
          label="เลขที่บัญชี"
          name="account_number"
          rules={[{ required: true, message: 'กรุณากรอกเลขที่บัญชี' }]}
        >
          <Input placeholder="เลขที่บัญชี" />
        </Form.Item>

        <Form.Item
          label="ชื่อบัญชี"
          name="account_name"
          rules={[{ required: true, message: 'กรุณากรอกชื่อบัญชี' }]}
        >
          <Input placeholder="ชื่อบัญชี" />
        </Form.Item>

        <Form.Item label="วันที่ทำหมาย" name="document_date">
          <DatePicker style={{ width: '100%' }} />
        </Form.Item>
      </Form>
    </Modal>
  )
}
```

### 6.3 API Service Pattern

**Location:** `frontend/src/services/api.ts`

```typescript
import axios from 'axios'
import { useAuthStore } from '../stores/authStore'

const api = axios.create({
  baseURL: '/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor - Add JWT token
api.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Response interceptor - Handle 401 Unauthorized
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      const message = error.response?.data?.detail || 'Session หมดอายุ กรุณา login ใหม่'

      setTimeout(() => {
        useAuthStore.getState().logout()
        window.location.href = '/login'
      }, 100)

      return Promise.reject(new Error(message))
    }
    return Promise.reject(error)
  }
)

export default api
```

---

## 7. Database Patterns

### 7.1 Relationships

```python
# One-to-Many: CriminalCase → BankAccount
class CriminalCase(Base):
    bank_accounts = relationship(
        "BankAccount",
        back_populates="criminal_case",
        cascade="all, delete-orphan"  # Auto-delete children when parent deleted
    )

class BankAccount(Base):
    criminal_case_id = Column(Integer, ForeignKey("criminal_cases.id", ondelete="CASCADE"))
    criminal_case = relationship("CriminalCase", back_populates="bank_accounts")

# Many-to-One: BankAccount → Bank (Master Data)
class BankAccount(Base):
    bank_id = Column(Integer, ForeignKey("banks.id", ondelete="SET NULL"), nullable=True)
    bank = relationship("Bank")
```

### 7.2 Virtual Fields Pattern

**Location:** `backend/app/utils/virtual_fields.py`

```python
def format_thai_date(date_obj):
    """Convert date to Thai Buddhist format"""
    if not date_obj:
        return None

    thai_year = date_obj.year + 543
    thai_months = ['ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
                   'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.']

    return f"{date_obj.day} {thai_months[date_obj.month - 1]} {thai_year}"

def get_bank_accounts_count(db: Session, case_id: int) -> str:
    """Return '2/5' format (replied/total)"""
    total = db.query(BankAccount).filter(BankAccount.criminal_case_id == case_id).count()
    replied = db.query(BankAccount).filter(
        BankAccount.criminal_case_id == case_id,
        BankAccount.reply_status == True
    ).count()
    return f"{replied}/{total}"
```

---

## 8. API Design Patterns

### 8.1 Standard CRUD Endpoints

```
GET    /api/v1/criminal-cases/          - List all (with RBAC filter)
POST   /api/v1/criminal-cases/          - Create new
GET    /api/v1/criminal-cases/{id}      - Get single
PUT    /api/v1/criminal-cases/{id}      - Update
DELETE /api/v1/criminal-cases/{id}      - Delete
```

### 8.2 Custom Action Endpoints

```
POST   /api/v1/criminal-cases/{id}/generate-case-number  - Generate case number
GET    /api/v1/bank-accounts/by-case/{case_id}          - Get by parent ID
POST   /api/v1/documents/bank-summons/{id}/generate     - Generate Word doc
POST   /api/v1/emails/send-summons                      - Send email with attachment
GET    /api/v1/email-tracking/pixel/{token}             - Tracking pixel (v3.6.0)
```

### 8.3 File Upload Endpoints

```python
from fastapi import UploadFile, File

@router.post("/upload-signature")
async def upload_signature(
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user)
):
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="Only image files allowed")

    # Save file
    file_path = f"/app/uploads/signatures/{current_user.id}_{file.filename}"
    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    return {"filename": file.filename, "path": file_path}
```

---

## 9. State Management

### 9.1 Zustand Store Pattern

**Location:** `frontend/src/stores/authStore.ts`

```typescript
import { create } from 'zustand'
import { persist } from 'zustand/middleware'

interface User {
  id: number
  username: string
  email: string
  full_name: string | null
  role?: {
    id: number
    role_name: string
    role_display: string
  }
}

interface AuthState {
  token: string | null
  user: User | null
  setAuth: (token: string, user: User) => void
  logout: () => void
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      setAuth: (token, user) => set({ token, user }),
      logout: () => set({ token: null, user: null }),
    }),
    {
      name: 'auth-storage', // localStorage key
    }
  )
)
```

**Usage in Components:**

```typescript
import { useAuthStore } from '../stores/authStore'

function MyComponent() {
  const { user, token, setAuth, logout } = useAuthStore()

  // Access state
  console.log(user?.username)

  // Update state
  setAuth(newToken, newUser)

  // Clear state
  logout()
}
```

---

## 10. Error Handling

### 10.1 Backend Error Handling

```python
from fastapi import HTTPException

# Standard errors
raise HTTPException(status_code=404, detail="Case not found")
raise HTTPException(status_code=400, detail="Invalid case number format")
raise HTTPException(status_code=401, detail="Unauthorized")
raise HTTPException(status_code=403, detail="Not authorized to access this resource")
raise HTTPException(status_code=500, detail="Internal server error")

# Try-catch pattern
try:
    db.add(db_case)
    db.commit()
    db.refresh(db_case)
except Exception as e:
    db.rollback()
    raise HTTPException(status_code=500, detail=f"Failed to create case: {str(e)}")
```

### 10.2 Frontend Error Handling

```typescript
import { message } from 'antd'

// API call pattern
const fetchData = async () => {
  try {
    setLoading(true)
    const response = await api.get('/criminal-cases/')
    setData(response.data)
  } catch (error: any) {
    // Display error message
    message.error(
      error.response?.data?.detail ||
      error.message ||
      'เกิดข้อผิดพลาด'
    )
  } finally {
    setLoading(false)
  }
}

// Form validation error
try {
  const values = await form.validateFields()
  // Submit
} catch (error: any) {
  if (error.errorFields) {
    message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
  } else {
    message.error(error.response?.data?.detail || 'เกิดข้อผิดพลาด')
  }
}
```

---

## 11. Development Workflow

### 11.1 Git Commit Convention

```bash
# Format
<type>: <subject>

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>

# Types
feat: New feature (e.g., "feat: Add email tracking system")
fix: Bug fix (e.g., "fix: Correct bank address display")
docs: Documentation (e.g., "docs: Update README with v3.6.0 features")
refactor: Code refactoring (e.g., "refactor: Extract date utils to separate file")
style: Code formatting (e.g., "style: Fix indentation in BankAccountFormModal")
test: Add tests (e.g., "test: Add unit tests for email service")
chore: Maintenance (e.g., "chore: Update dependencies")

# Example
git add .
git commit -m "feat: Add email tracking pixel for summons

Implemented email tracking system that records when recipients open emails.
Uses invisible 1x1 pixel image with unique tokens.

🤖 Generated with [Claude Code](https://claude.ai/code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 11.2 Docker Development Commands

```bash
# Start system
docker-compose up -d

# Stop system
docker-compose down

# View logs
docker logs criminal-case-backend -f
docker logs criminal-case-frontend -f

# Restart service (after code changes if hot reload fails)
docker-compose restart backend
docker-compose restart frontend

# Access database
docker exec -it criminal-case-db psql -U user -d criminal_case_db

# Backup database
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup.dump
docker cp criminal-case-db:/tmp/backup.dump ./backup.dump

# Restore database
docker cp backup.dump criminal-case-db:/tmp/restore.dump
docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump
```

### 11.3 Testing Workflow

```bash
# Backend tests (pytest)
docker exec criminal-case-backend pytest

# Frontend tests (vitest - not configured yet)
cd frontend
npm run test

# Manual testing checklist
1. Test CRUD operations
2. Test authentication (login/logout)
3. Test RBAC (admin vs user access)
4. Test file upload (signatures, CFR)
5. Test document generation (Word files)
6. Test email sending
7. Test CFR flow chart visualization
```

---

## 12. Code Examples

### 12.1 Complete API Route Example

**File:** `backend/app/api/v1/suspects.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core import get_db
from app.models import Suspect, CriminalCase, User
from app.schemas import SuspectCreate, SuspectUpdate, SuspectResponse
from app.api.v1.auth import get_current_user

router = APIRouter()

@router.post("/", response_model=SuspectResponse, status_code=201)
def create_suspect(
    suspect: SuspectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify case exists and user has access
    case = db.query(CriminalCase).filter(CriminalCase.id == suspect.criminal_case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Create suspect
    db_suspect = Suspect(**suspect.dict())
    db.add(db_suspect)
    db.commit()
    db.refresh(db_suspect)

    return db_suspect

@router.get("/by-case/{case_id}", response_model=List[SuspectResponse])
def get_suspects_by_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify case exists and user has access
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    suspects = db.query(Suspect).filter(Suspect.criminal_case_id == case_id).all()
    return suspects

@router.put("/{suspect_id}", response_model=SuspectResponse)
def update_suspect(
    suspect_id: int,
    suspect: SuspectUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not db_suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")

    # Verify user has access to case
    case = db.query(CriminalCase).filter(CriminalCase.id == db_suspect.criminal_case_id).first()
    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    # Update
    for key, value in suspect.dict(exclude_unset=True).items():
        setattr(db_suspect, key, value)

    db.commit()
    db.refresh(db_suspect)
    return db_suspect

@router.delete("/{suspect_id}", status_code=204)
def delete_suspect(
    suspect_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_suspect = db.query(Suspect).filter(Suspect.id == suspect_id).first()
    if not db_suspect:
        raise HTTPException(status_code=404, detail="Suspect not found")

    # Verify user has access to case
    case = db.query(CriminalCase).filter(CriminalCase.id == db_suspect.criminal_case_id).first()
    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    db.delete(db_suspect)
    db.commit()
    return None
```

### 12.2 Complete React Component Example

**File:** `frontend/src/components/SuspectFormModal.tsx`

```typescript
import { useEffect } from 'react'
import { Modal, Form, Input, Select, message, Row, Col } from 'antd'
import api from '../services/api'

const { Option } = Select

interface SuspectFormModalProps {
  visible: boolean
  criminalCaseId: number
  editingRecord?: any
  onClose: (success?: boolean) => void
}

export default function SuspectFormModal({
  visible,
  criminalCaseId,
  editingRecord,
  onClose,
}: SuspectFormModalProps) {
  const [form] = Form.useForm()
  const isEdit = !!editingRecord

  useEffect(() => {
    if (editingRecord) {
      form.setFieldsValue(editingRecord)
    } else {
      form.resetFields()
    }
  }, [editingRecord, form])

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields()
      const payload = { ...values, criminal_case_id: criminalCaseId }

      if (isEdit) {
        await api.put(`/suspects/${editingRecord.id}`, payload)
        message.success('แก้ไขผู้ต้องหาสำเร็จ')
      } else {
        await api.post('/suspects/', payload)
        message.success('เพิ่มผู้ต้องหาสำเร็จ')
      }

      form.resetFields()
      onClose(true)
    } catch (error: any) {
      if (error.errorFields) {
        message.error('กรุณากรอกข้อมูลให้ครบถ้วน')
      } else {
        message.error(error.response?.data?.detail || 'เกิดข้อผิดพลาด')
      }
    }
  }

  const handleCancel = () => {
    form.resetFields()
    onClose(false)
  }

  return (
    <Modal
      title={isEdit ? 'แก้ไขผู้ต้องหา' : 'เพิ่มผู้ต้องหา'}
      open={visible}
      onOk={handleSubmit}
      onCancel={handleCancel}
      width={700}
      okText="บันทึก"
      cancelText="ยกเลิก"
    >
      <Form form={form} layout="vertical">
        <Row gutter={16}>
          <Col span={8}>
            <Form.Item
              label="คำนำหน้า"
              name="prefix"
              rules={[{ required: true, message: 'กรุณาเลือกคำนำหน้า' }]}
            >
              <Select placeholder="เลือกคำนำหน้า">
                <Option value="นาย">นาย</Option>
                <Option value="นาง">นาง</Option>
                <Option value="นางสาว">นางสาว</Option>
              </Select>
            </Form.Item>
          </Col>

          <Col span={8}>
            <Form.Item
              label="ชื่อ"
              name="first_name"
              rules={[{ required: true, message: 'กรุณากรอกชื่อ' }]}
            >
              <Input placeholder="ชื่อ" />
            </Form.Item>
          </Col>

          <Col span={8}>
            <Form.Item
              label="นามสกุล"
              name="last_name"
              rules={[{ required: true, message: 'กรุณากรอกนามสกุล' }]}
            >
              <Input placeholder="นามสกุล" />
            </Form.Item>
          </Col>
        </Row>

        <Form.Item label="เลขประจำตัวประชาชน" name="id_card_number">
          <Input placeholder="เลขประจำตัวประชาชน 13 หลัก" maxLength={13} />
        </Form.Item>

        <Form.Item label="ที่อยู่" name="address">
          <Input.TextArea rows={3} placeholder="ที่อยู่" />
        </Form.Item>

        <Form.Item label="หมายเหตุ" name="notes">
          <Input.TextArea rows={2} placeholder="หมายเหตุ" />
        </Form.Item>
      </Form>
    </Modal>
  )
}
```

### 12.3 Email Service Example (v3.6.0)

**File:** `backend/app/services/email_service.py`

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from app.core.config import settings
from app.models import EmailLog
from sqlalchemy.orm import Session
import secrets

def send_email_with_attachment(
    to_email: str,
    subject: str,
    body_html: str,
    attachment_path: str,
    attachment_filename: str,
    db: Session,
    criminal_case_id: int,
    document_type: str,
    sender_name: str
):
    # Generate tracking token
    tracking_token = secrets.token_urlsafe(32)

    # Insert tracking pixel into HTML
    tracking_pixel = f'<img src="http://localhost:8000/api/v1/email-tracking/pixel/{tracking_token}" width="1" height="1" />'
    body_with_tracking = body_html + tracking_pixel

    # Create message
    msg = MIMEMultipart()
    msg['From'] = f"{settings.FROM_NAME} <{settings.FROM_EMAIL}>"
    msg['To'] = to_email
    msg['Subject'] = subject

    # Attach HTML body
    msg.attach(MIMEText(body_with_tracking, 'html', 'utf-8'))

    # Attach file
    with open(attachment_path, 'rb') as f:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename= {attachment_filename}'
        )
        msg.attach(part)

    # Send email
    with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.starttls()
        server.login(settings.SMTP_USERNAME, settings.SMTP_PASSWORD)
        server.send_message(msg)

    # Log email
    email_log = EmailLog(
        criminal_case_id=criminal_case_id,
        recipient_email=to_email,
        subject=subject,
        document_type=document_type,
        attachment_filename=attachment_filename,
        tracking_token=tracking_token,
        sender_name=sender_name,
        status='sent'
    )
    db.add(email_log)
    db.commit()

    return tracking_token
```

---

## 13. Testing Guidelines

### 13.1 Manual Testing Checklist

**Authentication**
- [ ] Login with valid credentials
- [ ] Login with invalid credentials
- [ ] Logout
- [ ] Access protected route without token (should redirect to login)
- [ ] Token expiry (after 30 minutes)

**CRUD Operations**
- [ ] Create criminal case
- [ ] View case list (admin sees all, user sees own)
- [ ] Edit case
- [ ] Delete case
- [ ] Add bank account to case
- [ ] Edit bank account
- [ ] Delete bank account
- [ ] Add suspect
- [ ] Edit suspect
- [ ] Delete suspect

**Document Generation**
- [ ] Generate bank summons (Word file downloads)
- [ ] Generate non-bank summons
- [ ] Generate payment gateway summons
- [ ] Generate telco mobile summons
- [ ] Generate telco internet summons

**Email System (v3.6.0)**
- [ ] Send bank summons via email
- [ ] Verify email received
- [ ] Open email (tracking pixel should fire)
- [ ] Check email history modal (status should show "อ่านแล้ว")

**CFR System (v3.3.0)**
- [ ] Upload CFR Excel file
- [ ] Parse and create bank accounts
- [ ] View CFR flow chart
- [ ] Detect summons from CFR data

**Master Data (v3.5.0)**
- [ ] CRUD operations on Banks
- [ ] CRUD operations on Non-Banks
- [ ] CRUD operations on Payment Gateways
- [ ] CRUD operations on Telco Mobile providers
- [ ] CRUD operations on Telco Internet providers
- [ ] CRUD operations on Exchanges

### 13.2 API Testing with cURL

```bash
# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin&password=admin123"

# Get cases (with token)
curl -X GET http://localhost:8000/api/v1/criminal-cases/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# Create case
curl -X POST http://localhost:8000/api/v1/criminal-cases/ \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "case_number": "123/2568",
    "case_id": "บต.4001/2568",
    "complainant": "นายทดสอบ ระบบ",
    "complaint_date": "2025-01-15",
    "status": "ระหว่างสอบสวน"
  }'
```

---

## 14. Common Pitfalls

### 14.1 Backend Pitfalls

**❌ Forgetting to commit database changes**
```python
db.add(db_case)
# Missing: db.commit()
# Missing: db.refresh(db_case)
return db_case  # Returns object without ID!
```

**✅ Correct:**
```python
db.add(db_case)
db.commit()
db.refresh(db_case)
return db_case
```

---

**❌ Not checking RBAC in endpoints**
```python
@router.get("/{case_id}")
def get_case(case_id: int, db: Session = Depends(get_db)):
    return db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    # Anyone can access any case!
```

**✅ Correct:**
```python
@router.get("/{case_id}")
def get_case(
    case_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    case = db.query(CriminalCase).filter(CriminalCase.id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    # Check ownership
    if current_user.role.role_name != "admin" and case.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized")

    return case
```

---

**❌ Using localhost in Docker network**
```python
# In docker-compose, services communicate via service names
DATABASE_URL = "postgresql://user:password@localhost:5432/db"  # ❌ Wrong!
```

**✅ Correct:**
```python
DATABASE_URL = "postgresql://user:password@postgres:5432/db"  # ✅ Service name
```

---

### 14.2 Frontend Pitfalls

**❌ Not handling loading states**
```typescript
const fetchData = async () => {
  const response = await api.get('/cases')
  setCases(response.data)
  // User sees stale data while loading!
}
```

**✅ Correct:**
```typescript
const fetchData = async () => {
  try {
    setLoading(true)
    const response = await api.get('/cases')
    setCases(response.data)
  } catch (error: any) {
    message.error(error.response?.data?.detail || 'Failed to load')
  } finally {
    setLoading(false)
  }
}
```

---

**❌ Forgetting to convert dates**
```typescript
const payload = {
  ...values,
  complaint_date: values.complaint_date  // Day.js object! ❌
}
await api.post('/cases', payload)
```

**✅ Correct:**
```typescript
const payload = {
  ...values,
  complaint_date: values.complaint_date?.format('YYYY-MM-DD')  // ✅ ISO string
}
await api.post('/cases', payload)
```

---

**❌ Not refreshing data after mutations**
```typescript
const handleDelete = async (id: number) => {
  await api.delete(`/cases/${id}`)
  message.success('ลบสำเร็จ')
  // Table still shows deleted item! ❌
}
```

**✅ Correct:**
```typescript
const handleDelete = async (id: number) => {
  await api.delete(`/cases/${id}`)
  message.success('ลบสำเร็จ')
  fetchCases()  // ✅ Refresh list
}
```

---

**❌ Hardcoding backend URL**
```typescript
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1'  // ❌ Won't work in Docker
})
```

**✅ Correct:**
```typescript
const api = axios.create({
  baseURL: '/api/v1'  // ✅ Proxy handles routing (vite.config.ts)
})
```

---

## Quick Reference

### Environment Variables (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password123@postgres:5432/criminal_case_db
REDIS_URL=redis://redis:6379/0

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Email (SMTP)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
FROM_EMAIL=your-email@gmail.com
FROM_NAME=กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4

# Upload
UPLOAD_DIR=/app/uploads
```

### Useful Commands

```bash
# Backend
docker exec criminal-case-backend python -m pytest
docker exec -it criminal-case-backend bash
docker logs criminal-case-backend -f

# Frontend
docker exec -it criminal-case-frontend sh
docker logs criminal-case-frontend -f

# Database
docker exec -it criminal-case-db psql -U user -d criminal_case_db
docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup.dump

# Docker
docker-compose up -d
docker-compose down
docker-compose restart backend
docker ps
docker volume ls
```

---

**End of Development Guide**

For more information, see:
- `README.md` - Complete system documentation
- `CLAUDE.md` - Project context for AI assistants
- `docker-compose.yml` - Docker configuration
