-- Migration 028: Alter telco_internet_accounts - change time_period to datetime_used
-- เปลี่ยนจาก time_period (ช่วงเวลา) เป็น datetime_used (วันเวลาที่ใช้งาน)

-- ลบคอลัมน์เก่า
ALTER TABLE telco_internet_accounts DROP COLUMN IF EXISTS time_period;

-- เพิ่มคอลัมน์ใหม่
ALTER TABLE telco_internet_accounts ADD COLUMN datetime_used TIMESTAMP WITH TIME ZONE;

-- เพิ่ม comment
COMMENT ON COLUMN telco_internet_accounts.datetime_used IS 'วันเวลาที่ใช้งาน IP Address';

