# สรุปการเพิ่มคอลัมน์ bank_short_name ในตาราง banks

**วันที่:** 11 ตุลาคม 2568

---

## 🎯 ภาพรวม

เพิ่มคอลัมน์ `bank_short_name` (ชื่อย่อภาษาอังกฤษ) ในตาราง `banks` เพื่อใช้งานร่วมกับข้อมูล CFR

---

## 📊 ผลการอัพเดต

### **สรุปการอัพเดต:**
- ✅ **ธนาคารทั้งหมด:** 13 ธนาคาร
- ✅ **อัพเดต bank_short_name สำเร็จ:** 13 ธนาคาร (100%)
- ✅ **ครบทุกธนาคาร!** 🎉

---

## 📋 รายการธนาคารที่อัพเดตสำเร็จ

| ลำดับ | bank_code | bank_short_name | ชื่อธนาคาร | สถานะ |
|:---:|:---:|:---:|:---|:---:|
| 1 | 002 | BBL | กรุงเทพ | ✅ |
| 2 | 004 | KBANK | กสิกรไทย | ✅ |
| 3 | 008 | KTB | กรุงไทย | ✅ |
| 4 | 011 | TTB | ทหารไทยธนชาต | ✅ |
| 5 | 014 | SCB | ไทยพาณิชย์ | ✅ |
| 6 | 022 | CIMBT | ซีไอเอ็มบีไทย | ✅ |
| 7 | 024 | UOBT | ยูโอบี | ✅ |
| 8 | 025 | BAY | กรุงศรีอยุธยา | ✅ |
| 9 | 026 | KKP | เกียรตินาคินภัทร | ✅ |
| 10 | 030 | GSB | ออมสิน | ✅ |
| 11 | 033 | GHB | อาคารสงเคราะห์ | ✅ |
| 12 | 034 | BAAC | ธ.ก.ส. | ✅ |
| 13 | 073 | LH | แลนด์แอนด์เฮ้าส์ | ✅ |

---

## 🔄 การทำงาน

### **1. เพิ่มคอลัมน์:**
```sql
ALTER TABLE banks ADD COLUMN bank_short_name VARCHAR(20);
CREATE INDEX idx_banks_bank_short_name ON banks(bank_short_name);
```

### **2. อัพเดตข้อมูลตาม bank_code map:**
```sql
UPDATE banks SET bank_short_name = 'BBL' WHERE bank_code = '002';
UPDATE banks SET bank_short_name = 'KBANK' WHERE bank_code = '004';
UPDATE banks SET bank_short_name = 'KTB' WHERE bank_code = '008';
...
UPDATE banks SET bank_short_name = 'GHB' WHERE bank_code = '033';
...
```

---

## 📊 Bank Code Mapping

```python
bank_code_map = {
    "002": "BBL",      # ธนาคารกรุงเทพ
    "004": "KBANK",    # ธนาคารกสิกรไทย
    "006": "KTB",      # (ไม่มีในฐานข้อมูล)
    "008": "KTB",      # ธนาคารกรุงไทย (ใช้ 008 แทน 006)
    "011": "TTB",      # ธนาคารทหารไทยธนชาต
    "014": "SCB",      # ธนาคารไทยพาณิชย์
    "022": "CIMBT",    # ธนาคารซีไอเอ็มบีไทย
    "024": "UOBT",     # ธนาคารยูโอบี
    "025": "BAY",      # ธนาคารกรุงศรีอยุธยา
    "026": "KKP",      # ธนาคารเกียรตินาคินภัทร (ใช้ 026 แทน 069)
    "030": "GSB",      # ธนาคารออมสิน
    "033": "GHB",      # ธนาคารอาคารสงเคราะห์
    "034": "BAAC",     # ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร
    "067": "TISCO",    # ธนาคารทิสโก้ (ไม่มีในฐานข้อมูล)
    "070": "ICBCT",    # ธนาคารไอซีบีซี (ไม่มีในฐานข้อมูล)
    "073": "LH"        # ธนาคารแลนด์แอนด์เฮ้าส์
}
```

---

## 🎯 Use Cases

### **1. ค้นหาธนาคารจากชื่อย่อ:**
```sql
SELECT * FROM banks WHERE bank_short_name = 'BBL';
```

### **2. เชื่อมโยงข้อมูล CFR กับธนาคาร (ใช้ชื่อย่อ):**
```sql
SELECT 
    cfr.from_account_no,
    cfr.from_bank_short_name as cfr_bank_short,
    banks.bank_short_name as master_bank_short,
    banks.bank_name
FROM cfr
LEFT JOIN banks ON cfr.from_bank_code::text = banks.bank_code
WHERE cfr.from_bank_short_name = banks.bank_short_name;
```

### **3. วิเคราะห์เส้นทางการเงินด้วยชื่อย่อ:**
```sql
SELECT 
    b1.bank_short_name as from_bank,
    b2.bank_short_name as to_bank,
    COUNT(*) as transfer_count,
    SUM(cfr.transfer_amount) as total_amount
FROM cfr
LEFT JOIN banks b1 ON cfr.from_bank_code::text = b1.bank_code
LEFT JOIN banks b2 ON cfr.to_bank_code::text = b2.bank_code
GROUP BY b1.bank_short_name, b2.bank_short_name
ORDER BY total_amount DESC;
```

---

## 📁 ไฟล์ที่แก้ไข

### **1. Database Migration:**
- `web-app/backend/migrations/020_add_bank_short_name.sql` (NEW)

### **2. Backend Models:**
- `web-app/backend/app/models/bank.py` (เพิ่ม `bank_short_name`)

### **3. Backend Schemas:**
- `web-app/backend/app/schemas/bank.py` (เพิ่ม `bank_short_name`)

---

## 📊 ตารางข้อมูลที่อัพเดต

| bank_code | bank_short_name | bank_name |
|:---:|:---:|:---|
| 002 | BBL | กรุงเทพ |
| 004 | KBANK | กสิกรไทย |
| 008 | KTB | กรุงไทย |
| 011 | TTB | ทหารไทยธนชาต |
| 014 | SCB | ไทยพาณิชย์ |
| 022 | CIMBT | ซีไอเอ็มบีไทย |
| 024 | UOBT | ยูโอบี |
| 025 | BAY | กรุงศรีอยุธยา |
| 026 | KKP | เกียรตินาคินภัทร |
| 030 | GSB | ออมสิน |
| 033 | GHB | อาคารสงเคราะห์ |
| 034 | BAAC | ธ.ก.ส. |
| 073 | LH | แลนด์แอนด์เฮ้าส์ |

---

## ⚠️ หมายเหตุ

### **ความแตกต่างระหว่าง bank_code_map กับฐานข้อมูล:**

| ใน Map | ใช้จริง | ธนาคาร | หมายเหตุ |
|:---:|:---:|:---|:---|
| 006 | 008 | กรุงไทย (KTB) | ฐานข้อมูลใช้ 008 |
| 069 | 026 | เกียรตินาคินภัทร (KKP) | ฐานข้อมูลใช้ 026 |

**ธนาคารที่ไม่มีในฐานข้อมูล:**
- TISCO (067)
- ICBCT (070)

---

## ✅ สรุป

**การอัพเดต bank_short_name เสร็จสมบูรณ์!**

- ✅ เพิ่มคอลัมน์ `bank_short_name` ในตาราง banks
- ✅ อัพเดตชื่อย่อสำเร็จ **13 ธนาคาร ครบทั้งหมด** (100%)
- ✅ สร้าง index สำหรับ performance
- ✅ อัพเดต Model และ Schema
- ✅ พร้อมใช้งานร่วมกับข้อมูล CFR

**ตอนนี้ตาราง banks มีข้อมูลครบ:**
- ✅ `bank_name` - ชื่อเต็ม (ภาษาไทย)
- ✅ `bank_code` - รหัส 3 หลัก
- ✅ `bank_short_name` - ชื่อย่อ (ภาษาอังกฤษ)

**พร้อมใช้งานแล้ว!** 🎉

---

**หมายเหตุ:** ยังไม่ได้ commit ขึ้น Git ตามคำสั่ง

