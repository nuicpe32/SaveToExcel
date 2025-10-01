-- Migration 008: Remove unused fields from bank_accounts table
-- Reason: Clean up unused fields that were removed from frontend forms
-- Date: 2025-10-01

-- Description:
-- This migration removes fields that are no longer used:
-- 1. account_owner - เจ้าของบัญชี (เพิ่มเติม) - not used
-- 2. delivery_month - เดือนที่ส่ง - removed from frontend
-- 3. delivery_time - เวลาที่ส่ง - removed from frontend
-- 4. response_date - วันที่ได้รับตอบกลับ - removed from frontend

BEGIN;

-- Remove unused columns from bank_accounts
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS account_owner;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS delivery_month;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS delivery_time;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS response_date;

COMMIT;

-- Note: The following fields are kept:
-- - status: Still used in backend logic
-- - reply_status: Still used (Switch in frontend)
-- - delivery_date: Still used (renamed to "กำหนดให้ส่งเอกสาร")

-- Rollback script (if needed):
-- ALTER TABLE bank_accounts ADD COLUMN account_owner VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN delivery_month VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN delivery_time VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN response_date DATE;

