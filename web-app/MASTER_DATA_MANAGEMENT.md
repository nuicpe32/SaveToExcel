# 🗄️ Master Data Management Guide

คู่มือการใช้งานระบบจัดการฐานข้อมูล Master Data สำหรับผู้ดูแลระบบ (Admin)

**Version:** 3.5.0
**Date:** 13 ตุลาคม 2568

---

## 📋 Table of Contents
- [ภาพรวมระบบ](#ภาพรวมระบบ)
- [การเข้าถึงระบบ](#การเข้าถึงระบบ)
- [ตาราง Master Data](#ตาราง-master-data)
- [การใช้งาน](#การใช้งาน)
- [Validation Rules](#validation-rules)
- [API Reference](#api-reference)

---

## ภาพรวมระบบ

ระบบจัดการฐานข้อมูล Master Data ช่วยให้ผู้ดูแลระบบสามารถจัดการข้อมูลพื้นฐานที่ใช้ในระบบได้อย่างมีประสิทธิภาพ รวมถึง:

- ✅ เพิ่มข้อมูลใหม่
- ✅ แก้ไขข้อมูลที่มีอยู่
- ✅ ลบข้อมูลที่ไม่ใช้งาน (ภายใต้เงื่อนไข)
- ✅ ดูรายการข้อมูลทั้งหมด

### คุณสมบัติหลัก

- **Admin Only**: เฉพาะผู้ใช้ที่มีสิทธิ์ Admin เท่านั้นที่เข้าถึงได้
- **Real-time Updates**: ข้อมูลอัพเดตทันทีหลังบันทึก
- **Relationship Protection**: ป้องกันการลบข้อมูลที่ถูกใช้งานอยู่
- **User-friendly UI**: ใช้งานง่ายด้วย Tabs และ Modal Forms

---

## การเข้าถึงระบบ

### ขั้นตอนการเข้าใช้งาน

1. **Login ด้วยบัญชี Admin**
   ```
   URL: http://localhost:3001
   Username: admin
   Password: admin123
   ```

2. **เข้าเมนู Master Data Management**
   - คลิกเมนู "ระบบผู้ดูแล" (ด้านซ้าย)
   - เลือก "จัดการฐานข้อมูล" (🗄️ ไอคอน Database)

3. **เลือก Tab ที่ต้องการจัดการ**
   - ธนาคาร (🏦)
   - Non-Bank (🏪)
   - Payment Gateway (💳)
   - Telco Mobile (📱)
   - Telco Internet (🌐)
   - Crypto Exchange (🔄)

---

## ตาราง Master Data

### 1. 🏦 Banks (ธนาคาร)

**วัตถุประสงค์:** เก็บข้อมูลธนาคารสำหรับออกหมายเรียกบัญชีธนาคาร

**ฟิลด์หลัก:**
- `bank_name` *(required)* - ชื่อธนาคาร (เช่น "ธนาคารกรุงเทพ จำกัด (มหาชน)")
- `bank_code` - รหัสธนาคาร (เช่น "002")
- `bank_short_name` - ชื่อย่อ (เช่น "BBL")
- `bank_address` - ที่อยู่สำนักงานใหญ่
- `soi`, `moo`, `road` - รายละเอียดที่อยู่
- `sub_district`, `district`, `province`, `postal_code` - พื้นที่

**Relationships:**
- → `bank_accounts` (บัญชีธนาคารในคดี)

**Validation:**
- ❌ ไม่สามารถลบได้หากมีบัญชีธนาคารที่เชื่อมโยงอยู่
- ⚠️ ชื่อธนาคารต้องไม่ซ้ำ (Unique)

---

### 2. 🏪 Non-Banks (บริษัทนอกระบบธนาคาร)

**วัตถุประสงค์:** เก็บข้อมูลผู้ให้บริการ Non-Bank เช่น TrueMoney Wallet, AirPay

**ฟิลด์หลัก:**
- `company_name` *(required)* - ชื่อบริษัท
- `company_name_short` - ชื่อย่อ
- `company_address` - ที่อยู่
- `phone`, `email`, `website` - ข้อมูลติดต่อ
- `is_active` - สถานะ (ใช้งาน/ปิดใช้งาน)

**Relationships:**
- → `non_bank_accounts` (บัญชี Non-Bank ในคดี)
- → `non_bank_transactions` (รายการธุรกรรม)

**Validation:**
- ❌ ไม่สามารถลบได้หากมีบัญชี Non-Bank ที่เชื่อมโยงอยู่

---

### 3. 💳 Payment Gateways (ผู้ให้บริการชำระเงิน)

**วัตถุประสงค์:** เก็บข้อมูลผู้ให้บริการ Payment Gateway เช่น Omise, 2C2P, Stripe

**ฟิลด์หลัก:**
- `company_name` *(required)* - ชื่อบริษัท
- `company_name_short` - ชื่อย่อ
- `company_address` - ที่อยู่
- `phone`, `email`, `website` - ข้อมูลติดต่อ
- `is_active` - สถานะ

**Relationships:**
- → `payment_gateway_accounts` (บัญชี Payment Gateway ในคดี)
- → `payment_gateway_transactions` (รายการธุรกรรม)

**Validation:**
- ❌ ไม่สามารถลบได้หากมีบัญชี Payment Gateway ที่เชื่อมโยงอยู่

---

### 4. 📱 Telco Mobile (ผู้ให้บริการโทรศัพท์มือถือ)

**วัตถุประสงค์:** เก็บข้อมูลผู้ให้บริการโทรศัพท์มือถือ เช่น AIS, True, NT

**ฟิลด์หลัก:**
- `company_name` *(required)* - ชื่อบริษัท
- `company_name_short` - ชื่อย่อ (เช่น "AIS")
- `building_name` - ชื่ออาคาร
- `company_address` - ที่อยู่
- `phone`, `email`, `website` - ข้อมูลติดต่อ
- `is_active` - สถานะ

**Relationships:**
- → `telco_mobile_accounts` (หมายเลขโทรศัพท์ในคดี)

**Validation:**
- ❌ ไม่สามารถลบได้หากมีหมายเลขโทรศัพท์ที่เชื่อมโยงอยู่

**ตัวอย่างข้อมูล:**
```
AIS - บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)
True - บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)
NT - บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน)
```

---

### 5. 🌐 Telco Internet (ผู้ให้บริการอินเทอร์เน็ต)

**วัตถุประสงค์:** เก็บข้อมูลผู้ให้บริการอินเทอร์เน็ต เช่น TRUE Online, AIS Fibre, 3BB

**ฟิลด์หลัก:**
- `company_name` *(required)* - ชื่อบริษัท
- `company_name_short` - ชื่อย่อ
- `building_name` - ชื่ออาคาร
- `company_address` - ที่อยู่
- `phone`, `email`, `website` - ข้อมูลติดต่อ
- `is_active` - สถานะ

**Relationships:**
- → `telco_internet_accounts` (IP Address ในคดี)

**Validation:**
- ❌ ไม่สามารถลบได้หากมี IP Address ที่เชื่อมโยงอยู่

**ตัวอย่างข้อมูล:**
```
TRUE Online - บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)
AIS Fibre - บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)
3BB - บริษัท ทริปเปิลที บรอดแบนด์ จำกัด (มหาชน)
NT Broadband - บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน)
```

---

### 6. 🔄 Exchanges (ผู้ให้บริการซื้อขายสินทรัพย์ดิจิทัล)

**วัตถุประสงค์:** เก็บข้อมูล Crypto Exchange เช่น Bitkub, Zipmex

**ฟิลด์หลัก:**
- `company_name` *(required)* - ชื่อบริษัท
- `company_name_short` - ชื่อย่อ
- `company_name_alt` - ชื่อเดิม/ชื่อทางเลือก
- `building_name` - ชื่ออาคาร
- `company_address`, `floor`, `unit` - ที่อยู่
- `phone`, `email`, `website` - ข้อมูลติดต่อ
- `is_active` - สถานะ

**Relationships:**
- → *(ยังไม่มี exchange_accounts)*

**Validation:**
- ✅ สามารถลบได้ (ยังไม่มีตารางที่เชื่อมโยง)

**หมายเหตุ:**
- ❌ ไม่มีฟิลด์ `license_number` และ `license_date` (ไม่จำเป็น)

---

## การใช้งาน

### 🆕 เพิ่มข้อมูลใหม่

1. เลือก Tab ที่ต้องการ
2. คลิกปุ่ม "เพิ่ม..." (สีน้ำเงิน)
3. กรอกข้อมูลในฟอร์ม:
   - **ชื่อบริษัท/ธนาคาร** *(required)*
   - ชื่อย่อ
   - ที่อยู่ (แยกตามฟิลด์)
   - ข้อมูลติดต่อ
   - สถานะ (เปิด/ปิด)
4. คลิก "บันทึก"

**ตัวอย่าง: เพิ่มธนาคาร**
```
ชื่อธนาคาร: ธนาคารไทยพาณิชย์ จำกัด (มหาชน)
รหัสธนาคาร: 014
ชื่อย่อ: SCB
ที่อยู่: 9 ถนนรัชดาภิเษก
แขวง: จตุจักร
เขต: จตุจักร
จังหวัด: กรุงเทพมหานคร
รหัสไปรษณีย์: 10900
```

---

### ✏️ แก้ไขข้อมูล

1. คลิกปุ่ม "แก้ไข" (สีน้ำเงิน) ในแถวที่ต้องการ
2. ฟอร์มจะเปิดขึ้นพร้อมข้อมูลเดิม
3. แก้ไขข้อมูลที่ต้องการ
4. คลิก "บันทึก"

**⚠️ หมายเหตุ:**
- หากแก้ไขชื่อ จะมีการตรวจสอบว่าชื่อใหม่ซ้ำหรือไม่

---

### 🗑️ ลบข้อมูล

1. คลิกปุ่ม "ลบ" (สีแดง) ในแถวที่ต้องการ
2. ระบบจะแสดง Confirmation Dialog:
   - "ยืนยันการลบข้อมูล?"
   - "คุณแน่ใจหรือไม่ว่าต้องการลบข้อมูลนี้?"
3. คลิก "ยืนยัน" เพื่อลบ

**⚠️ Validation:**
- หากข้อมูลมี relationships (เช่น มีบัญชีธนาคารที่เชื่อมโยง)
- ระบบจะแสดงข้อความ:
  ```
  ไม่สามารถลบข้อมูลได้ เนื่องจากมีข้อมูลที่เชื่อมโยงอยู่
  Cannot delete. X account(s) are linked to this...
  ```

---

### 👁️ ดูรายการ

- ตารางแสดงข้อมูลทั้งหมด
- แบ่งหน้าอัตโนมัติ (10 รายการต่อหน้า)
- สถานะแสดงด้วยสี:
  - 🟢 **ใช้งาน** (สีเขียว)
  - 🔴 **ปิดใช้งาน** (สีแดง)

**คอลัมน์ที่แสดง:**

**Banks:**
- ชื่อธนาคาร, รหัส, ชื่อย่อ, ที่อยู่

**Non-Banks / Payment Gateways / Telco Mobile / Telco Internet:**
- ชื่อบริษัท, ชื่อย่อ, เบอร์โทร, อีเมล, สถานะ

**Exchanges:**
- ชื่อบริษัท, ชื่อย่อ, เบอร์โทร, อีเมล, สถานะ

---

## Validation Rules

### ✅ การตรวจสอบข้อมูล

#### 1. Unique Constraints
- **ชื่อบริษัท/ธนาคาร** ต้องไม่ซ้ำ
- ระบบจะแจ้งเตือน: "ข้อมูลซ้ำกัน" / "Name already exists"

#### 2. Required Fields
- **ชื่อบริษัท/ธนาคาร** จำเป็นต้องกรอก
- ฟิลด์อื่นๆ เป็น Optional

#### 3. Relationship Validation (Delete Protection)

| Master Data | Protected by | Error Message |
|------------|--------------|---------------|
| Banks | bank_accounts | "X bank account(s) are linked" |
| Non-Banks | non_bank_accounts | "X account(s) are linked" |
| Payment Gateways | payment_gateway_accounts | "X account(s) are linked" |
| Telco Mobile | telco_mobile_accounts | "X account(s) are linked" |
| Telco Internet | telco_internet_accounts | "X account(s) are linked" |
| Exchanges | *(ยังไม่มี)* | ลบได้ |

#### 4. HTTP Status Codes
- `200` - Success
- `400` - Bad Request (ข้อมูลซ้ำ, มี relationships)
- `403` - Forbidden (ไม่ใช่ Admin)
- `404` - Not Found

---

## API Reference

### Base URL
```
http://localhost:8000/api/v1/master-data
```

### Authentication
```http
Authorization: Bearer <jwt_token>
Role: admin
```

### Endpoints

#### 1. Banks

```http
GET    /banks/          # ดึงรายการทั้งหมด
GET    /banks/{id}      # ดึงข้อมูลตาม ID
POST   /banks/          # เพิ่มข้อมูลใหม่
PUT    /banks/{id}      # แก้ไขข้อมูล
DELETE /banks/{id}      # ลบข้อมูล
```

**Request Body (POST/PUT):**
```json
{
  "bank_name": "ธนาคารกรุงเทพ จำกัด (มหาชน)",
  "bank_code": "002",
  "bank_short_name": "BBL",
  "bank_address": "333 ถนนสีลม",
  "sub_district": "สีลม",
  "district": "บางรัก",
  "province": "กรุงเทพมหานคร",
  "postal_code": "10500"
}
```

#### 2. Non-Banks

```http
GET    /non-banks/          # ดึงรายการทั้งหมด
GET    /non-banks/{id}      # ดึงข้อมูลตาม ID
POST   /non-banks/          # เพิ่มข้อมูลใหม่
PUT    /non-banks/{id}      # แก้ไขข้อมูล
DELETE /non-banks/{id}      # ลบข้อมูล
```

**Request Body (POST/PUT):**
```json
{
  "company_name": "บริษัท แอสเซนด์ มันนี่ จำกัด",
  "company_name_short": "TrueMoney",
  "company_address": "18 อาคารทรู ทาวเวอร์",
  "phone": "02-123-4567",
  "email": "contact@truemoney.com",
  "website": "https://www.truemoney.com",
  "is_active": true
}
```

#### 3. Payment Gateways

```http
GET    /payment-gateways/          # ดึงรายการทั้งหมด
GET    /payment-gateways/{id}      # ดึงข้อมูลตาม ID
POST   /payment-gateways/          # เพิ่มข้อมูลใหม่
PUT    /payment-gateways/{id}      # แก้ไขข้อมูล
DELETE /payment-gateways/{id}      # ลบข้อมูล
```

#### 4. Telco Mobile

```http
GET    /telco-mobile/          # ดึงรายการทั้งหมด
GET    /telco-mobile/{id}      # ดึงข้อมูลตาม ID
POST   /telco-mobile/          # เพิ่มข้อมูลใหม่
PUT    /telco-mobile/{id}      # แก้ไขข้อมูล
DELETE /telco-mobile/{id}      # ลบข้อมูล
```

#### 5. Telco Internet

```http
GET    /telco-internet/          # ดึงรายการทั้งหมด
GET    /telco-internet/{id}      # ดึงข้อมูลตาม ID
POST   /telco-internet/          # เพิ่มข้อมูลใหม่
PUT    /telco-internet/{id}      # แก้ไขข้อมูล
DELETE /telco-internet/{id}      # ลบข้อมูล
```

#### 6. Exchanges

```http
GET    /exchanges/          # ดึงรายการทั้งหมด
GET    /exchanges/{id}      # ดึงข้อมูลตาม ID
POST   /exchanges/          # เพิ่มข้อมูลใหม่
PUT    /exchanges/{id}      # แก้ไขข้อมูล
DELETE /exchanges/{id}      # ลบข้อมูล
```

**Request Body (POST/PUT):**
```json
{
  "company_name": "บริษัท บิทคับ แคปปิตอล กรุ๊ป โฮลดิ้งส์ จำกัด",
  "company_name_short": "Bitkub",
  "building_name": "อาคารเอ็มไพร์ ทาวเวอร์",
  "company_address": "1 ซอย 47",
  "road": "สาทรใต้",
  "sub_district": "ยานนาวา",
  "district": "สาทร",
  "province": "กรุงเทพมหานคร",
  "postal_code": "10120",
  "phone": "02-123-4567",
  "email": "support@bitkub.com",
  "website": "https://www.bitkub.com",
  "is_active": true
}
```

---

## 🔒 Security

### Access Control
- ✅ เฉพาะ Admin เท่านั้น (`role_name = 'admin'`)
- ✅ Route Protection ทั้ง Frontend และ Backend
- ✅ JWT Authentication required

### Data Protection
- ✅ Foreign Key Constraints
- ✅ Cascade Delete Protection
- ✅ Unique Constraints

---

## 🐛 Troubleshooting

### ปัญหาที่พบบ่อย

#### 1. ไม่เห็นเมนู "จัดการฐานข้อมูล"
**สาเหตุ:** บัญชีไม่ใช่ Admin
**แก้ไข:** ติดต่อผู้ดูแลระบบเพื่อขอสิทธิ์ Admin

#### 2. ลบข้อมูลไม่ได้ แสดงข้อความ "มีข้อมูลที่เชื่อมโยงอยู่"
**สาเหตุ:** ข้อมูลถูกใช้งานอยู่
**แก้ไข:**
- ลบข้อมูลที่เชื่อมโยงก่อน (เช่น บัญชีธนาคารในคดี)
- หรือเปลี่ยนสถานะเป็น "ปิดใช้งาน" แทน

#### 3. แก้ไขชื่อไม่ได้ แสดง "ข้อมูลซ้ำกัน"
**สาเหตุ:** ชื่อใหม่ซ้ำกับข้อมูลที่มีอยู่แล้ว
**แก้ไข:** ใช้ชื่อที่ไม่ซ้ำ

#### 4. API Error 403 Forbidden
**สาเหตุ:** ไม่มีสิทธิ์ Admin
**แก้ไข:** ตรวจสอบสิทธิ์ผู้ใช้

---

## 📝 Best Practices

### การจัดการข้อมูล

1. **ตรวจสอบก่อนลบ**
   - ตรวจสอบว่ามีข้อมูลที่เชื่อมโยงหรือไม่
   - พิจารณาใช้ "ปิดใช้งาน" แทนการลบ

2. **กรอกข้อมูลให้ครบถ้วน**
   - ระบุที่อยู่ให้ละเอียด (สำหรับพิมพ์ซองหมายเรียก)
   - กรอกข้อมูลติดต่อให้ครบ

3. **ใช้ชื่อย่อที่ชัดเจน**
   - เช่น "AIS", "True", "BBL"
   - เพื่อความสะดวกในการแสดงผล

4. **ตั้งชื่อให้สื่อความหมาย**
   - ใช้ชื่อเต็มตามทะเบียนบริษัท
   - เพื่อความเป็นทางการในเอกสาร

---

## 🎯 Summary

ระบบจัดการฐานข้อมูล Master Data ใน v3.5.0 ช่วยให้:

- ✅ **ผู้ดูแลระบบ** จัดการข้อมูลพื้นฐานได้ง่าย
- ✅ **ป้องกันข้อมูล** ด้วย Validation และ Relationship Protection
- ✅ **ใช้งานสะดวก** ด้วย UI ที่ออกแบบมาเป็นพิเศษ
- ✅ **ปลอดภัย** ด้วย Admin-only Access Control

**ผลลัพธ์:** ข้อมูล Master Data ที่ถูกต้อง ครบถ้วน และพร้อมใช้งาน!

---

**📚 Related Documentation:**
- [README.md](./README.md) - คู่มือหลักของระบบ
- [CHANGELOG.md](./CHANGELOG.md) - ประวัติการอัพเดต
- API Documentation: http://localhost:8000/docs

---

**Version:** 3.5.0
**Last Updated:** 13 ตุลาคม 2568
**Maintained by:** กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4
