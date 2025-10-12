-- Migration: ปรับปรุงโครงสร้างตาราง non_bank_accounts และ non_bank_transactions
-- วันที่: 12 ตุลาคม 2568
-- คำอธิบาย: ลบคอลัมน์ที่ไม่ใช้และปรับให้เป็น normalized database

-- ============================================================================
-- 1. ตาราง non_bank_accounts
-- ============================================================================

-- เพิ่ม non_bank_id (FK to non_banks) ก่อนลบ provider_name
ALTER TABLE non_bank_accounts 
ADD COLUMN IF NOT EXISTS non_bank_id INTEGER REFERENCES non_banks(id) ON DELETE SET NULL;

-- สร้าง index
CREATE INDEX IF NOT EXISTS idx_non_bank_accounts_non_bank_id ON non_bank_accounts(non_bank_id);

-- ลบคอลัมน์ที่ไม่ใช้
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS order_number;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS document_date_thai;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS provider_name;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS account_owner;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS complainant;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS victim_name;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS case_id;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS delivery_month;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS delivery_time;
ALTER TABLE non_bank_accounts DROP COLUMN IF EXISTS is_frozen;

-- เพิ่ม comment
COMMENT ON COLUMN non_bank_accounts.non_bank_id IS 'รหัสผู้ให้บริการ Non-Bank (FK to non_banks)';

-- ============================================================================
-- 2. ตาราง non_bank_transactions
-- ============================================================================

-- เพิ่ม destination_non_bank_id (FK to non_banks)
ALTER TABLE non_bank_transactions 
ADD COLUMN IF NOT EXISTS destination_non_bank_id INTEGER REFERENCES non_banks(id) ON DELETE SET NULL;

-- สร้าง index
CREATE INDEX IF NOT EXISTS idx_non_bank_transactions_destination_non_bank_id ON non_bank_transactions(destination_non_bank_id);

-- ลบคอลัมน์ที่ไม่ใช้ (ใช้ FK แทน)
ALTER TABLE non_bank_transactions DROP COLUMN IF EXISTS destination_provider_name;

-- source_bank_id มีอยู่แล้ว ไม่ต้องเพิ่ม
-- ลบ source_bank_name ไม่ได้เพราะจะใช้เก็บชื่อไว้สำหรับแสดงผล (denormalized สำหรับ performance)

-- เพิ่ม comment
COMMENT ON COLUMN non_bank_transactions.destination_non_bank_id IS 'รหัสผู้ให้บริการปลายทาง (FK to non_banks)';

