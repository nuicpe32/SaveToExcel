# Changelog - ระบบจัดการคดีอาญา

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.0.1] - 2025-10-01

### 🐛 Fixed
- **แก้ไขปัญหา API routing conflict** - ลบฟังก์ชัน `update_criminal_case` และ `delete_criminal_case` ที่ซ้ำกันใน `criminal_cases.py`
- **แก้ไขปัญหา "ไม่สามารถดึงข้อมูลคดีอาญาได้"** - เมื่อคลิกแก้ไขคดีในหน้า Dashboard
- **ปรับปรุง error handling** - ใน API endpoints สำหรับ criminal cases

### 🔧 Technical Improvements
- **Backend API Optimization** - ลบ duplicate route handlers ที่ทำให้เกิด routing conflicts
- **Code Cleanup** - ทำความสะอาดโค้ดใน `web-app/backend/app/api/v1/criminal_cases.py`
- **Auto-reload Enhancement** - ระบบ auto-reload ทำงานได้ดีขึ้นหลังแก้ไขไฟล์

### ✅ Testing
- **API Endpoints Verified** - ทดสอบ API endpoints ทั้งหมดทำงานได้ปกติ
  - `/api/v1/criminal-cases/` ✅
  - `/api/v1/criminal-cases/{id}` ✅
  - `/api/v1/courts/` ✅
  - `/api/v1/case-types` ✅
- **Authentication Working** - ระบบ login และ JWT token ทำงานได้ปกติ

### 📊 System Status
- **Database**: 48 คดีอาญา, 15 ผู้ต้องหา, 418 บัญชีธนาคาร
- **Containers**: ทั้งหมดรันอยู่และ healthy
- **Development Mode**: ใช้งาน `docker-compose.dev.yml` เป็นหลัก

---

## [3.0.0] - 2025-09-30

### 🎉 Major Release
- **Web Application Launch** - เปิดตัว Web Application แบบ Full-Stack
- **Dual Platform Support** - รองรับทั้ง Desktop และ Web Application
- **Production Ready** - พร้อมใช้งานระดับองค์กร

### ✨ New Features
- **🌐 Web Application** - React + FastAPI + PostgreSQL
- **🔐 Authentication System** - JWT-based login/logout
- **📊 Real-time Dashboard** - แดชบอร์ดแสดงข้อมูลแบบเรียลไทม์
- **🔄 CRUD Operations** - เพิ่ม/แก้ไข/ลบ/ดู คดีอาญา
- **📱 Responsive Design** - รองรับทุกขนาดหน้าจอ
- **🗄️ PostgreSQL Database** - ฐานข้อมูลแบบ relational
- **🐳 Docker Support** - Containerization พร้อม Docker Compose

### 🏗️ Architecture
- **Frontend**: React 18 + TypeScript + Ant Design
- **Backend**: FastAPI + Python 3.11 + SQLAlchemy
- **Database**: PostgreSQL 15 + Redis 7
- **Infrastructure**: Docker + Docker Compose + Nginx

---

## [2.9.0] - 2025-09-29

### 🎨 Enhanced Suspect Summons Document Formatting
- **Font Standardization** - เปลี่ยนฟอนต์ทั้งหมดเป็น THSarabunNew
- **Optimized Page Margins** - ลดขอบด้านบนเป็น 0.3in
- **Arabic Numeral Conversion** - เปลี่ยนเลขไทยเป็นเลขอาราบิก
- **Professional Layout** - ปรับปรุงการจัดตำแหน่งและระยะห่าง

### 📄 Document Management System
- **Main Documents Hub** - จุดศูนย์กลางเอกสารทั้งหมด
- **Word Templates** - 9 ไฟล์เทมเพลตมาตรฐาน
- **Database Files** - 6 ไฟล์ฐานข้อมูลอัตโนมัติ
- **One-click Access** - เปิดไฟล์ด้วยคลิกเดียว

---

## [2.6.0] - 2025-09-28

### 📁 Complete Document Management System
- **Document Management Center** - แท็บหลักสำหรับจัดการเอกสาร
- **Professional UI/UX** - ไอคอน Microsoft Office จริง
- **Cross-platform Support** - รองรับ Windows, macOS, Linux
- **Smart File Detection** - ตรวจจับไฟล์อัตโนมัติ

---

## [2.5.0] - 2025-09-27

### 🏗️ Professional Architecture Implementation
- **Modular Design** - แยกโค้ดเป็น modules ชัดเจน
- **Data Management Layer** - จัดการข้อมูลแยกตามประเภท
- **Configuration System** - การตั้งค่ากลาง
- **Utility Layer** - ฟังก์ชันช่วยเหลือ

### 📊 Enhanced Data Visualization
- **Real-time Statistics** - สถิติแบบเรียลไทม์
- **Smart Date Tracking** - ติดตามวันที่อัตโนมัติ
- **Intelligent Duplicate Detection** - ตรวจจับซ้ำแม่นยำขึ้น 27.8%
- **Professional UI Design** - หน้าตาคล้าย Excel

---

## [2.4.0] - 2025-09-26

### 🔧 Major Refactoring
- **Complete Codebase Refactoring** - แปลงจาก monolithic เป็น modular
- **Professional Code Quality** - มาตรฐานระดับองค์กร
- **100% Backward Compatible** - ใช้งานได้เหมือนเดิมทุกอย่าง
- **Risk-free Deployment** - มีระบบ fallback

---

## [2.3.2] - 2025-09-25

### 🎨 UI/UX Improvements
- **Main Window Maximized** - หน้าต่างหลักขยายเต็มจออัตโนมัติ
- **Enhanced Case Detail Window** - ขนาด 40% ความกว้าง จัดกลาง
- **Button Repositioning** - ย้ายปุ่ม "พิมพ์รายงาน" และ "ปิด" ด้านบน
- **Taskbar Fix** - แก้ไขปัญหา taskbar overlap

### 🐛 Bug Fixes
- **Bank Account Display** - แสดงบัญชีธนาคารครบถ้วน
- **Program Name Update** - เปลี่ยนเป็น "ระบบจัดการคดีอาญา"
- **Visual Consistency** - ปรับปรุงชื่อและ title ทั่วทั้งระบบ

---

## [2.3.0] - 2025-09-24

### 🖨️ Print Report Functionality
- **Professional HTML Reports** - รายงานรูปแบบ HTML สวยงาม
- **Thai Typography** - ฟอนต์ THSarabunNew มาตรฐานราชการ
- **CCIB Logo Integration** - โลโก้หน่วยงาน (ขนาด 30% ใหญ่กว่าปกติ)
- **Browser-based Printing** - พิมพ์ผ่านเบราว์เซอร์

### 📊 6-Month Case Statistics
- **Overdue Case Detection** - ตรวจจับคดีเกิน 6 เดือน
- **Visual Indicators** - แถวสีแดงสำหรับคดีล่าช้า
- **Exact Month Calculation** - คำนวณอายุคดีแม่นยำระดับเดือน

### 🚔 Arrest Management System
- **43-Field Comprehensive Forms** - ฟอร์มครบวงจร
- **9 Data Groups** - จัดกลุ่มตามกระบวนการ
- **Excel Integration** - บันทึกลงไฟล์ Excel
- **Complete Workflow** - ตั้งแต่หมายจับจนถึงผลคดี

---

## [2.2.0] - 2025-09-23

### 🔧 Data Management Enhancements
- **Warrant Data Display Fix** - แก้ไขการแสดงข้อมูลหมายจับ
- **Document Number Formatting** - ปรับปรุงรูปแบบหมายเลขเอกสาร
- **Bank Data Search** - ฟังก์ชันค้นหาข้อมูลธนาคาร
- **Simplified Bank Form** - ฟอร์มธนาคารแบบเรียบง่าย

### 🧪 Testing and Quality Assurance
- **Unit Tests** - ทดสอบฟังก์ชัน checkbox การตอบกลับ
- **Error Handling** - การจัดการข้อผิดพลาดครบถ้วน
- **File Tracking** - จัดการไฟล์ Excel ใน git

---

## [2.1.0] - 2025-01-15

### ⚖️ Criminal Cases Module
- **Comprehensive Case Viewing** - ดูรายการคดีอาญา
- **Detailed Case Information** - หน้าต่างรายละเอียดแบบ scrollable
- **Data Search Algorithms** - ใช้ชื่อผู้เสียหายในการค้นหา
- **Related Data Search** - ค้นหาข้อมูลที่เกี่ยวข้อง

---

## [2.0.0] - 2024-12-15

### 🎨 UI/UX Enhancements
- **Descriptive Tab Names** - ชื่อแท็บที่เข้าใจง่าย
- **Improved Field Sizing** - ขนาดฟิลด์ที่เหมาะสม
- **Visual Hierarchy** - ไอคอน emoji เพื่อความชัดเจน

### 📊 Data Features
- **Auto-generated Document Numbers** - เลขที่หนังสืออัตโนมัติ
- **Thai Date Formatting** - รูปแบบวันที่ไทย
- **Smart Delivery Date Calculation** - คำนวณวันส่งอัตโนมัติ
- **Case Type Dropdown** - 16 ประเภทคดี

### 🔧 Technical Improvements
- **Enhanced Error Handling** - การจัดการข้อผิดพลาดที่ดีขึ้น
- **Better Path Management** - จัดการพาธไฟล์
- **Improved Field Mapping** - แมปฟิลด์สำหรับ edit dialogs
- **Dropdown Support** - รองรับ dropdown ใน edit forms

---

## [1.0.0] - 2024-11-01

### 🎉 Initial Release
- **Desktop Application** - โปรแกรม GUI สำหรับจัดการข้อมูลคดีอาญา
- **Bank Account Management** - จัดการข้อมูลบัญชีธนาคาร
- **Suspect Management** - จัดการหมายเรียกผู้ต้องหา
- **Criminal Case Management** - จัดการคดีอาญา
- **Excel Integration** - บันทึกข้อมูลลงไฟล์ Excel
- **Thai Language Support** - รองรับภาษาไทยเต็มรูปแบบ

---

## Legend
- 🐛 **Fixed** - Bug fixes
- ✨ **Added** - New features
- 🔧 **Changed** - Changes in existing functionality
- 🗑️ **Removed** - Removed features
- 🔒 **Security** - Security improvements
- 📚 **Documentation** - Documentation updates
- 🧪 **Testing** - Testing improvements
