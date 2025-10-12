# Criminal Case Management System - Architecture

## Project Overview

ระบบจัดการคดีอาญาได้รับการพัฒนาอย่างต่อเนื่องจนกลายเป็น **Full-Stack Application** ที่รองรับทั้ง Desktop และ Web Platform

## Dual Architecture

### 🌐 Web Application (Version 3.0.0)
```
web-app/
├── backend/                    # FastAPI Backend
│   ├── app/
│   │   ├── api/               # API Routes
│   │   │   ├── v1/
│   │   │   │   ├── auth.py           # Authentication endpoints
│   │   │   │   ├── criminal_cases.py # Criminal cases CRUD
│   │   │   │   ├── bank_accounts.py  # Bank accounts CRUD
│   │   │   │   └── suspects.py       # Suspects CRUD
│   │   ├── core/              # Core configuration
│   │   │   ├── database.py           # Database connection
│   │   │   ├── security.py           # JWT authentication
│   │   │   └── config.py             # App configuration
│   │   ├── models/            # SQLAlchemy Models
│   │   │   ├── criminal_case.py      # Criminal case model
│   │   │   ├── bank_account.py       # Bank account model
│   │   │   ├── suspect.py            # Suspect model
│   │   │   └── post_arrest.py        # Post arrest model
│   │   ├── schemas/           # Pydantic Schemas
│   │   │   ├── criminal_case.py      # Criminal case schemas
│   │   │   ├── bank_account.py       # Bank account schemas
│   │   │   ├── suspect.py            # Suspect schemas
│   │   │   └── user.py               # User schemas
│   │   ├── services/          # Business Logic
│   │   │   ├── data_migration.py     # Excel to DB migration
│   │   │   ├── auth_service.py       # Authentication service
│   │   │   └── case_service.py       # Case management service
│   │   └── utils/             # Utility functions
│   │       ├── date_utils.py         # Date formatting utilities
│   │       ├── case_styling.py       # Case styling logic
│   │       └── thai_date_utils.py    # Thai date utilities
│   ├── Dockerfile             # Backend container
│   └── requirements.txt       # Python dependencies
├── frontend/                  # React Frontend
│   ├── src/
│   │   ├── components/        # React Components
│   │   │   ├── MainLayout.tsx        # Main layout component
│   │   │   └── ProtectedRoute.tsx    # Route protection
│   │   ├── pages/             # Page Components
│   │   │   ├── LoginPage.tsx         # Login page
│   │   │   ├── DashboardPage.tsx     # Dashboard page
│   │   │   ├── AddCriminalCasePage.tsx # Add case page
│   │   │   └── EditCriminalCasePage.tsx # Edit case page
│   │   ├── services/          # API Services
│   │   │   └── api.ts               # API client
│   │   ├── stores/            # State Management
│   │   │   └── authStore.ts         # Authentication store
│   │   └── App.tsx            # Main app component
│   ├── Dockerfile             # Frontend container
│   ├── nginx.conf             # Nginx configuration
│   └── package.json           # Node dependencies
├── docker-compose.yml         # Multi-container setup
└── README.md                  # Web app documentation
```

### 🖥️ Desktop Application (Version 2.9.0)
```
SaveToExcel/
├── run.py                     # Main entry point (recommended)
├── criminal_case_manager.py   # Modular application controller
├── simple_excel_manager.py    # Original implementation (maintained for compatibility)
├── src/                       # Modular architecture
│   ├── __init__.py
│   ├── config/                # Configuration settings
│   │   ├── __init__.py
│   │   └── settings.py        # App settings, constants, feature flags
│   ├── data/                  # Data management layer
│   │   ├── __init__.py
│   │   ├── base_data_manager.py      # Base Excel operations
│   │   ├── bank_data_manager.py      # Bank account data operations
│   │   ├── criminal_data_manager.py  # Criminal cases data operations
│   │   ├── summons_data_manager.py   # Summons data operations
│   │   └── arrest_data_manager.py    # Arrest data operations
│   ├── gui/                   # GUI components
│   │   ├── __init__.py
│   │   └── base_gui.py        # Base GUI utilities and common components
│   └── utils/                 # Utility functions
│       ├── __init__.py
│       ├── date_utils.py      # Date/time related utilities
│       └── string_utils.py    # String processing utilities
├── Xlsx/                      # Excel data files
├── Doc/                       # Word document templates
├── Pdf/                       # PDF files
├── THSarabunNew/              # Thai fonts
├── logo ccib.png              # CCIB logo
└── README.md
```

## Architecture Overview

### 🌐 Web Application Architecture

#### 1. Full-Stack Design
- **Frontend**: React 18 + TypeScript + Ant Design
- **Backend**: FastAPI + Python 3.11 + SQLAlchemy
- **Database**: PostgreSQL with relationship mapping
- **Authentication**: JWT-based with role management
- **Containerization**: Docker + Docker Compose

#### 2. Backend Architecture
- **API Layer**: RESTful endpoints with versioning (v1)
- **Business Logic**: Service layer for complex operations
- **Data Layer**: SQLAlchemy ORM with PostgreSQL
- **Authentication**: JWT tokens with bcrypt password hashing
- **Migration**: Automated Excel to PostgreSQL data migration

#### 3. Frontend Architecture
- **Component-Based**: React functional components with hooks
- **State Management**: Zustand for global state
- **Routing**: React Router with protected routes
- **UI Framework**: Ant Design for consistent interface
- **Type Safety**: TypeScript for better development experience

#### 4. Database Design
- **Relational Model**: Proper foreign key relationships
- **Data Integrity**: Constraints and validations
- **Migration Support**: Automatic schema updates
- **Thai Date Support**: Buddhist Era date formatting

### 🖥️ Desktop Application Architecture

#### 1. Modular Design
- **Separation of Concerns**: Each module has a single responsibility
- **Data Layer**: Isolated Excel operations for better maintainability
- **Configuration Management**: Centralized settings and constants
- **Utility Functions**: Reusable helper functions

#### 2. Data Management Layer
- **BaseDataManager**: Common Excel file operations
- **Specialized Managers**: Domain-specific operations for each data type
- **Consistent Interface**: All managers follow the same patterns

#### 3. Configuration System
- **Centralized Settings**: All constants and configuration in one place
- **Feature Flags**: Easy to enable/disable features
- **Environment Detection**: Automatic detection of available libraries

#### 4. Utility Layer
- **Date Utils**: Thai date formatting and parsing
- **String Utils**: Text processing and cleaning functions
- **Modular Import**: Easy to add new utility modules

## Development Phases

### Phase 1: Desktop Application Foundation (✅ Completed)
- Create modular directory structure
- Extract utility functions
- Create configuration system
- Create data management base classes

### Phase 2: Desktop Data Layer (✅ Completed)
- Implement specialized data managers
- Extract data operations from main file
- Maintain API compatibility

### Phase 3: Web Application Development (✅ Completed)
- Create FastAPI backend with PostgreSQL
- Implement React frontend with TypeScript
- Set up Docker containerization
- Create authentication system
- Migrate Excel data to database

### Phase 4: Feature Parity (✅ Completed)
- Implement CRUD operations for criminal cases
- Add dashboard with real-time data
- Create case detail views
- Implement styling and conditional formatting
- Add bank accounts and suspects management

### Phase 5: Production Ready (✅ Completed)
- Fix all bugs and errors
- Optimize performance
- Complete testing
- Document all features

## Benefits

### 1. Maintainability
- **Clear Structure**: Easy to locate and modify specific functionality
- **Modular Components**: Changes in one module don't affect others
- **Testable Code**: Each module can be tested independently

### 2. Extensibility
- **Easy to Add Features**: New functionality can be added as new modules
- **Plugin Architecture**: Components can be easily replaced or extended
- **Configuration-Driven**: Behavior can be modified via settings

### 3. Code Quality
- **Reusable Components**: Common functionality is shared across modules
- **Consistent Patterns**: All components follow established patterns
- **Documentation**: Each module is self-documenting

## Usage

### 🌐 Web Application
```bash
# Start the full-stack application
cd web-app
docker-compose up -d

# Access the application
# Frontend: http://localhost:3001
# Backend API: http://localhost:8000
# Database: localhost:5432
```

### 🖥️ Desktop Application
```bash
# New modular entry point (recommended)
python3 criminal_case_manager.py

# Original implementation (fallback)
python3 simple_excel_manager.py
```

### Development

#### Web Application Development
```bash
# Backend development
cd web-app/backend
python -m uvicorn app.main:app --reload

# Frontend development
cd web-app/frontend
npm run dev

# Database migration
docker-compose exec backend python -m app.services.data_migration
```

#### Desktop Application Development
```bash
# Import specific modules
from src.data.bank_data_manager import BankDataManager
from src.utils.date_utils import format_thai_date
from src.config.settings import APP_NAME

# Use modular components
bank_manager = BankDataManager()
bank_manager.load_data()
```

## Compatibility

- **100% Backward Compatibility**: Original functionality is preserved
- **Gradual Migration**: Both architectures work simultaneously
- **Fallback Support**: Automatic fallback to original implementation if needed
- **Data Format**: No changes to Excel file formats or data structures

## Technology Stack Summary

### 🌐 Web Application Stack
- **Frontend**: React 18, TypeScript, Ant Design, Zustand, React Router
- **Backend**: FastAPI, Python 3.11, SQLAlchemy, Pydantic
- **Database**: PostgreSQL 15
- **Authentication**: JWT, bcrypt
- **Containerization**: Docker, Docker Compose, Nginx
- **Development**: Hot reload, TypeScript checking, ESLint

### 🖥️ Desktop Application Stack
- **GUI Framework**: tkinter (Python built-in)
- **Data Processing**: pandas, openpyxl
- **Document Generation**: python-docx, reportlab
- **Configuration**: Python config files
- **File Management**: os, pathlib

## Recent Updates (v3.2.0)

### ✨ Payment Gateway System
- **Master Data**: `payment_gateways` table (Omise, GB Prime Pay, 2C2P)
- **Accounts**: `payment_gateway_accounts` with bank integration
- **Transactions**: `payment_gateway_transactions` (1-5 transfers, minimum 1 required)
- **Documents**: Specialized summons format without freeze account option
- **UI**: Logo background display, integrated dashboard tab

### ✨ Non-Bank System
- **Master Data**: `non_banks` table (TrueMoney, Line Pay, etc.)
- **Accounts**: `non_bank_accounts` linked to criminal cases
- **Transactions**: `non_bank_transactions` with multi-transfer support (1-5 transfers, optional)
- **Documents**: Modified summons format with optional freeze account
- **Normalization**: FK relationships to `banks` and `non_banks` master data

### ✨ CFR (Cash Flow Report) System
- **Upload**: Support .xls, .xlsx files from banks
- **Analysis**: Auto-detect victim accounts and summons status
- **Visualization**: Flow chart showing money transfers
- **Tags**: Visual indicators for victim accounts and summons

### ✨ UI/UX Improvements
- **Dark Mode**: Full dark mode support across all pages
- **Logo Display**: Bank/Non-Bank/Payment Gateway logos (opacity 0.05)
- **Sidebar**: Collapsible sidebar with state persistence
- **Date Handling**: Improved Thai Buddhist Era date support

## Future Enhancements

### 🌐 Web Application
1. **Advanced Reporting**: PDF generation, Excel export from database
2. **Real-time Updates**: WebSocket integration for live notifications
3. **Mobile App**: React Native version for iOS/Android
4. **Advanced Analytics**: Interactive charts and statistics dashboards
5. **API Integration**: External API integration (banks, government services)
6. **Audit Log**: Complete audit trail for all transactions
7. **Backup/Restore**: Automated backup and restore functionality

### 🖥️ Desktop Application
1. **Complete GUI Refactoring**: Extract all GUI components
2. **Plugin System**: Support for third-party extensions
3. **Database Support**: Optional database backend (SQLite/PostgreSQL)
4. **Multi-language Support**: Internationalization framework
5. **Advanced Features**: Workflow automation, bulk operations
6. **Cloud Sync**: Sync with Web Application database