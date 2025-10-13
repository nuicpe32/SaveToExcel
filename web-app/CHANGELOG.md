# CHANGELOG - Criminal Case Management System

## Version 3.4.0 - 13 ตุลาคม 2568

### 🎉 New Features

#### 📱 ระบบหมายเลขโทรศัพท์ (Telco Mobile)
- ✅ เพิ่ม Tab "หมายเลขโทรศัพท์" ใน Dashboard
- ✅ Modal สำหรับเพิ่ม/แก้ไข ข้อมูลหมายเลขโทรศัพท์
- ✅ Dropdown ผู้ให้บริการ (AIS, True, NT) จาก Master Data
- ✅ ตาราง `telco_mobile_accounts` พร้อม Foreign Keys
- ✅ API Endpoints: CRUD operations
- ✅ หมายเรียกข้อมูลโทรศัพท์ (HTML) - รูปแบบเฉพาะ
- ✅ ซองหมายเรียกโทรศัพท์ (HTML) - ดึงที่อยู่จาก DB

#### 🌐 ระบบ IP Address (Telco Internet)
- ✅ เพิ่ม Tab "IP Address" ใน Dashboard
- ✅ Modal สำหรับเพิ่ม/แก้ไข ข้อมูล IP Address
- ✅ Dropdown ผู้ให้บริการ (TRUE Online, AIS Fibre, 3BB, NT Broadband)
- ✅ ตาราง `telco_internet_accounts` พร้อม Foreign Keys
- ✅ API Endpoints: CRUD operations
- ✅ หมายเรียกข้อมูล IP Address (HTML) - รูปแบบเฉพาะ
- ✅ ซองหมายเรียก IP Address (HTML) - ดึงที่อยู่จาก DB
- ✅ ฟิลด์ `datetime_used` แทน `time_period` สำหรับเก็บวันเวลาที่ใช้งาน

### 🔧 Technical Improvements

#### Database
- ✅ Migration 026: สร้างตาราง `telco_mobile_accounts`
- ✅ Migration 027: สร้างตาราง `telco_internet_accounts`
- ✅ Migration 028: แก้ไข `telco_internet_accounts.time_period` → `datetime_used`
- ✅ เพิ่ม Relationships ใน `criminal_case`, `telco_mobile`, `telco_internet`

#### Backend API
- ✅ `/api/v1/telco-mobile-accounts/` - CRUD operations
- ✅ `/api/v1/telco-internet-accounts/` - CRUD operations
- ✅ `/api/v1/documents/telco-mobile-summons/{id}` - หมายเรียกโทรศัพท์
- ✅ `/api/v1/documents/telco-mobile-envelope/{id}` - ซองหมายเรียกโทรศัพท์
- ✅ `/api/v1/documents/telco-internet-summons/{id}` - หมายเรียก IP Address
- ✅ `/api/v1/documents/telco-internet-envelope/{id}` - ซองหมายเรียก IP Address

#### Frontend Components
- ✅ `TelcoMobileAccountFormModal.tsx` - Modal กรอกข้อมูลโทรศัพท์
- ✅ `TelcoInternetAccountFormModal.tsx` - Modal กรอกข้อมูล IP Address
- ✅ อัพเดต `DashboardPage.tsx` - เพิ่ม 2 Tabs ใหม่
- ✅ State Management สำหรับข้อมูลใหม่
- ✅ Handlers สำหรับ CRUD operations

#### Document Generation
- ✅ `TelcoMobileSummonsGenerator` - สร้างหมายเรียก/ซองโทรศัพท์
- ✅ `TelcoInternetSummonsGenerator` - สร้างหมายเรียก/ซอง IP Address
- ✅ Thai Date Utils - เพิ่มฟังก์ชัน `format_datetime_to_thai()`

### 🐛 Bug Fixes
- ✅ แก้ไข Vite Proxy: `criminal-case-backend` → `backend`
- ✅ แก้ไข Dropdown ผู้ให้บริการ: เพิ่ม trailing slash `/telco-mobile/`
- ✅ แก้ไข Non-Bank Summons: Indentation error
- ✅ แก้ไข ชื่อผู้ให้บริการ: ใช้ `company_name` (ชื่อเต็ม) ในเรียนและซอง

### 📄 Document Content Updates

#### หมายเรียกโทรศัพท์:
- ✅ เรื่อง: "ขอให้จัดส่งข้อมูลรายละเอียดของหมายเลขโทรศัพท์ {phone_number}"
- ✅ เรียน: "กรรมการผู้จัดการ{company_name}"
- ✅ เนื้อหา: ปรับแก้ไขให้เหมาะสมกับข้อมูลโทรศัพท์
- ✅ ตาราง: ผู้ให้บริการ | หมายเลขโทรศัพท์ | ช่วงเวลาขอข้อมูล
- ✅ รายการเอกสาร: 5 ข้อเฉพาะสำหรับโทรศัพท์

#### หมายเรียก IP Address:
- ✅ เรื่อง: "ขอให้จัดส่งข้อมูลรายละเอียดของ IP Address {ip_address}"
- ✅ เรียน: "กรรมการผู้จัดการ{company_name}"
- ✅ เนื้อหา: ปรับแก้ไขให้เหมาะสมกับ IP Address
- ✅ ตาราง: ผู้ให้บริการ | IP Address | วันเวลาที่ใช้งาน
- ✅ รายการเอกสาร: 4 ข้อเฉพาะสำหรับ IP Address

#### ซองหมายเรียก:
- ✅ ใช้ `company_name` (ชื่อเต็ม) บรรทัดแรก
- ✅ ดึงที่อยู่จาก Master Data Tables
- ✅ รูปแบบเดียวกับระบบธนาคาร

### 🎯 UI/UX Enhancements
- ✅ 2 Tabs ใหม่ในลำดับที่เหมาะสม (ระหว่าง Payment Gateway และ ผู้ต้องหา)
- ✅ Form Validation และ Error Handling
- ✅ Date/DateTime Pickers พร้อมรูปแบบไทย
- ✅ สถานะตอบกลับ (เขียว/แดง) พร้อมนับวัน
- ✅ ปุ่มจัดการครบชุด (เพิ่ม/แก้ไข/ลบ/ปริ้น)

---

## 📋 ลำดับ Tabs ใน Dashboard (8 Tabs)

1. ข้อมูลทั่วไป
2. ข้อมูล CFR
3. บัญชีธนาคารที่เกี่ยวข้อง 🏦
4. Non-Bank 🏪
5. Payment Gateway 💳
6. **หมายเลขโทรศัพท์ 📱** ⭐ **ใหม่!**
7. **IP Address 🌐** ⭐ **ใหม่!**
8. ผู้ต้องหาที่เกี่ยวข้อง 👤

---

## 🗄️ Database Schema

### telco_mobile_accounts (17 columns)
- Primary Key: `id`
- Foreign Keys: `criminal_case_id`, `telco_mobile_id`
- Key Fields: `provider_name`, `phone_number`, `time_period`
- Status: `reply_status`, `days_since_sent`, `status`

### telco_internet_accounts (17 columns)
- Primary Key: `id`
- Foreign Keys: `criminal_case_id`, `telco_internet_id`
- Key Fields: `provider_name`, `ip_address`, `datetime_used`
- Status: `reply_status`, `days_since_sent`, `status`

---

## 📊 Master Data

### telco_mobile (3 providers)
1. AIS - บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)
2. True - บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)
3. NT - บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน)

### telco_internet (4 providers)
1. TRUE Online - บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)
2. AIS Fibre - บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)
3. 3BB - บริษัท ทริปเปิลที บรอดแบนด์ จำกัด (มหาชน)
4. NT Broadband - บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน)

---

## 🛡️ Backward Compatibility
- ✅ ระบบเดิมทำงานปกติ 100%
- ✅ ข้อมูลเดิมไม่กระทบ
- ✅ Non-Bank และ Payment Gateway กลับมาทำงานได้ปกติ
- ✅ เพิ่มเฉพาะฟีเจอร์ใหม่

---

## 🎯 Breaking Changes
- ❌ ไม่มี Breaking Changes
- ✅ เป็น Additive Changes เท่านั้น
