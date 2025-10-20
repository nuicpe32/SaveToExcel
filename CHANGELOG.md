# Changelog - ระบบจัดการคดีอาญา

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [3.7.0] - 2025-10-19

### ✨ Added - Charges Master Data System
- **📋 ระบบฐานข้อมูลข้อหาความผิด** - เพิ่มระบบจัดการข้อหาความผิดทางอาญา
  - ตาราง `charges` สำหรับข้อมูล Master Data ข้อหา
  - Model, Schema, API endpoints สำหรับ CRUD operations
  - นำเข้าข้อมูลเริ่มต้น 5 รายการจากไฟล์ Excel
- **🎨 UI Enhancement** - เพิ่ม Tab "ข้อหาความผิด" ใน Master Data Page
  - แสดงรายการข้อหาแบบ table พร้อม pagination
  - ฟอร์มเพิ่ม/แก้ไขข้อมูลครบถ้วน
  - Validation และ duplicate check
- **🔐 Admin Only** - เข้าถึงได้เฉพาะผู้ดูแลระบบเท่านั้น
- **📊 Data Structure**:
  - ชื่อข้อหา (charge_name)
  - ข้อหา/รายละเอียดเต็ม (charge_description)
  - กฎหมายที่เกี่ยวข้อง (related_laws)
  - อัตราโทษ (penalty)

### 🔧 Improved - Session Management
- **⏰ เพิ่มเวลา Session** - เปลี่ยน JWT token expiration จาก 30 นาที → 4 ชั่วโมง (240 นาที)
  - แก้ปัญหาระบบเด้งออกขณะกรอกข้อมูล
  - เหมาะกับการทำงานในออฟฟิศ
  - ป้องกันการสูญหายของข้อมูลที่กำลังกรอก

### 🔧 Technical Details
- **Database Migration**: `033_update_charges_table_structure.sql`, `034_insert_charges_data.sql`
- **Backend**: Model, Schema, Router สำหรับ Charges
- **Frontend**: Tab ใหม่ใน Master Data Page
- **API Endpoints**: `/api/v1/charges/` (GET, POST, PUT, DELETE)
- **Session Duration**: 240 minutes (4 hours)

---

## [Unreleased] - 2025-10-12

### ✨ Added - Payment Gateway Management System
- **🏢 ระบบจัดการ Payment Gateway** - เพิ่มระบบจัดการบัญชี Payment Gateway แยกต่างหาก
  - ตาราง `payment_gateways` สำหรับข้อมูล Master Data (Omise, GB Prime Pay, 2C2P)
  - ตาราง `payment_gateway_accounts` สำหรับข้อมูลบัญชี Payment Gateway
  - ตาราง `payment_gateway_transactions` สำหรับรายละเอียดการโอนเงิน
- **💰 รายละเอียดการโอนเงิน** - รองรับการบันทึกรายการโอนได้ 1-5 รายการต่อหมายเรียก
  - ข้อมูลธนาคารต้นทาง (bank_id, account_number, account_name)
  - ข้อมูลธนาคารปลายทาง (bank_id, account_number, account_name)
  - วันที่โอน, เวลา, จำนวนเงิน
- **📄 ระบบสร้างหมายเรียก Payment Gateway** - เอกสารหมายเรียกรูปแบบพิเศษ
  - หัวเรื่อง: "ขอให้จัดรายละเอียดการโอนเงิน"
  - ตารางแสดงบัญชีต้นทางและปลายทาง (รวมชื่อธนาคาร + เลขบัญชี + ชื่อบัญชี)
  - รายการเอกสารที่ขอ: รายละเอียดการชำระสินค้า/บริการ, ข้อมูล KYC
  - ไม่มีตัวเลือกอายัดบัญชี (เนื่องจาก Payment Gateway ไม่สามารถอายัดได้)
- **📧 ซองหมายเรียก Payment Gateway** - ซองหมายเรียกสำหรับ Payment Gateway
- **🎨 UI Enhancement** - เพิ่ม logo Payment Gateway และธนาคารในตาราง Dashboard

### ✨ Added - Non-Bank Account Management
- **🏪 ระบบจัดการบัญชี Non-Bank** - จัดการบริการทางการเงินนอกธนาคาร (TrueMoney, Line Pay, etc.)
  - ตาราง `non_banks` สำหรับข้อมูล Master Data
  - ตาราง `non_bank_accounts` สำหรับข้อมูลบัญชี Non-Bank
  - ตาราง `non_bank_transactions` สำหรับรายละเอียดการโอนเงิน
- **💳 การเชื่อมโยง Master Data** - เชื่อมโยงกับฐานข้อมูลธนาคารและ Non-Bank
  - ธนาคารต้นทาง: ใช้ `bank_id` (FK to banks table)
  - ผู้ให้บริการปลายทาง: ใช้ `non_bank_id` (FK to non_banks table)
- **📝 ฟอร์มกรอกข้อมูล Non-Bank** - ฟอร์มสมบูรณ์พร้อม validation
  - รองรับ Multi-transfer (1-5 รายการต่อหมายเรียก)
  - ตารางแสดงรายการโอนที่เพิ่มแล้ว
  - แก้ไข/ลบรายการโอนได้
- **📄 หมายเรียก Non-Bank พร้อมตัวเลือกอายัดบัญชี**
  - Modal ถามผู้ใช้ว่าต้องการอายัดบัญชีหรือไม่
  - เอกสารปรับเนื้อหาตามการเลือก
- **🎨 Background Logo** - แสดง logo Non-Bank เป็นพื้นหลังในตาราง

### ✨ Added - CFR (Cash Flow Report) System
- **📊 ระบบ CFR - Cash Flow Report** - วิเคราะห์กระแสเงินสด
  - แท็บใหม่ "CFR" ใน Dashboard
  - อัพโหลดไฟล์ CFR จากธนาคาร (.xls, .xlsx)
  - แสดงข้อมูล Transaction ทั้งหมด
  - ตรวจจับบัญชีผู้เสียหายอัตโนมัติ
  - ตรวจจับบัญชีที่มีหมายเรียกแล้ว
  - แสดง Tag: "ผู้เสียหาย", "ส่งหมายเรียกแล้ว"
- **🔍 ระบบวิเคราะห์กระแสเงิน**
  - คำนวณจำนวนวันหลังส่งหมายเรียก
  - แสดงสถานะการตอบกลับ
  - ค้นหาธุรกรรมที่เกี่ยวข้อง
- **📈 Flow Chart Visualization** - แผนภาพแสดงกระแสเงิน
  - แสดงเส้นทางการโอนเงิน (บัญชีต้นทาง → บัญชีปลายทาง)
  - คลิกดูรายละเอียดแต่ละบัญชี
  - แสดง Transactions ที่เกี่ยวข้อง

### 🔧 Changed - Database Normalization
- **🗄️ ปรับปรุงโครงสร้างฐานข้อมูล Non-Bank**
  - ลบคอลัมน์ที่ไม่ใช้งาน: `order_number`, `document_date_thai`, `provider_name`, `account_owner`, `complainant`, `victim_name`, `case_id`, `delivery_month`, `delivery_time`, `is_frozen`
  - เปลี่ยน `source_bank_name` → `source_bank_id` (FK to banks)
  - เปลี่ยน `destination_provider_name` → `destination_non_bank_id` (FK to non_banks)
- **🔗 Relationship Mapping** - สร้างความสัมพันธ์ระหว่างตาราง
  - `non_bank_transactions.source_bank_id` → `banks.id`
  - `non_bank_transactions.destination_non_bank_id` → `non_banks.id`
  - `payment_gateway_transactions.source_bank_id` → `banks.id`
  - `payment_gateway_transactions.destination_bank_id` → `banks.id`
  - `payment_gateway_accounts.bank_id` → `banks.id`

### 🎨 Improved - UI/UX Enhancements
- **🌓 Dark Mode Support** - รองรับโหมดมืด
  - Dark mode สำหรับ Dashboard Page
  - Dark mode สำหรับ Modal dialogs
  - Dark mode สำหรับ Detail Page
  - แก้ไขปัญหา text contrast
- **📱 Sidebar Improvements** - ปรับปรุง sidebar
  - Sidebar collapse/expand
  - จำสถานะ sidebar
  - เลื่อนหน้าได้ขณะ sidebar ปิด
- **🖼️ Logo Display** - แสดง logo สวยงาม
  - Logo ธนาคารพื้นหลัง opacity 0.05
  - Logo Non-Bank และ Payment Gateway
  - รองรับธนาคาร 15+ แห่ง

### 🐛 Fixed - Bug Fixes
- **🔒 Authentication Fixes**
  - แก้ไข JWT token expiration handling
  - แสดง error message ก่อน redirect to login
  - ปรับปรุง session timeout warning
- **📅 Date Display Fixes**
  - แก้ไขการแสดง `time_period` ใน RangePicker (Bank Account)
  - แก้ไขการแสดง `time_period` ใน RangePicker (Non-Bank Account)
  - แก้ไข parsing ของ Thai date format
- **💾 Data Persistence Fixes**
  - แก้ไขปัญหา duplicate transfers เมื่อ edit และ save ซ้ำ
  - แก้ไข API endpoint สำหรับ Payment Gateway transactions
  - แก้ไขการบันทึก `bank_id` ใน Payment Gateway form
- **📄 Document Generation Fixes**
  - แก้ไขเทมเพลต Python ใน Payment Gateway summons
  - เพิ่มคำว่า "ธนาคาร" ข้างหน้าชื่อธนาคารในตารางหมายเรียก
  - ลบคำว่า "สำนักงานใหญ่" จากบรรทัด "เรียน"
- **🗄️ Database Fixes**
  - แก้ไข PostgreSQL connection issues
  - แก้ไข pgAdmin connection problems
  - แก้ไข database migration scripts

### 📚 Documentation
- **เอกสารที่อัพเดต**
  - อัพเดต CHANGELOG.md ครอบคลุมทุก features
  - อัพเดต DEVELOPMENT_GUIDE.md รวมระบบใหม่
  - อัพเดต ARCHITECTURE.md รวมโครงสร้างใหม่
  - อัพเดต README.md รวม Payment Gateway และ Non-Bank

---

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

## [2.8.0] - 2025-09-28

### ✉️ Bank Envelope Printing System
- **🎯 Bank Envelope Printing** - ระบบพิมพ์ซองหมายเรียกธนาคารครบครัน
- **💬 User Prompt** - ถามผู้ใช้ว่าต้องการปริ้นซองหมายเรียกหรือไม่
- **📦 Batch Printing** - รองรับพิมพ์ซองหลายรายการพร้อมกัน
- **🏛️ Professional Format** - ใช้ตราครุฑและรูปแบบไปรษณีย์มาตรฐาน
- **📏 Fold Lines** - เส้นพับซองแบบ 3 ตอน

---

## [2.6.0] - 2025-09-27

### 📁 Complete Document Management System
- **Document Management Center** - แท็บหลักสำหรับจัดการเอกสาร
- **Professional UI/UX** - ไอคอน Microsoft Office จริง
- **Cross-platform Support** - รองรับ Windows, macOS, Linux
- **Smart File Detection** - ตรวจจับไฟล์อัตโนมัติ

---

## [2.5.0] - 2025-09-26

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

## [2.4.0] - 2025-09-25

### 🔧 Major Refactoring
- **Complete Codebase Refactoring** - แปลงจาก monolithic เป็น modular
- **Professional Code Quality** - มาตรฐานระดับองค์กร
- **100% Backward Compatible** - ใช้งานได้เหมือนเดิมทุกอย่าง
- **Risk-free Deployment** - มีระบบ fallback

---

## [2.3.2] - 2025-09-24

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

## [2.3.0] - 2025-09-23

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

## [2.2.0] - 2025-09-22

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

- 🎉 **Major Release** - เวอร์ชันสำคัญ
- ✨ **Added** - ฟีเจอร์ใหม่
- 🔧 **Changed** - เปลี่ยนแปลงฟังก์ชันเดิม
- 🐛 **Fixed** - แก้ไข bugs
- 🗑️ **Removed** - ลบฟีเจอร์
- 🔒 **Security** - การปรับปรุงด้านความปลอดภัย
- 📚 **Documentation** - อัพเดตเอกสาร
- 🧪 **Testing** - การทดสอบ
- 🎨 **Improved** - ปรับปรุง UI/UX
- 🏗️ **Architecture** - เปลี่ยนแปลงสถาปัตยกรรม
