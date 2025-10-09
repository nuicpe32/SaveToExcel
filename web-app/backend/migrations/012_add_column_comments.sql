-- Migration 012: เพิ่มคำอธิบายในแต่ละคอลัมน์ของฐานข้อมูล
-- วันที่: 9 ตุลาคม 2568

-- ========================================
-- ตาราง criminal_cases
-- ========================================

COMMENT ON TABLE criminal_cases IS 'ตารางข้อมูลคดีอาญา';

-- Primary Key
COMMENT ON COLUMN criminal_cases.id IS 'Primary Key - รหัสคดีในระบบ (Auto increment)';

-- Case Identification
COMMENT ON COLUMN criminal_cases.case_number IS 'เลขที่คดี (รูปแบบ: หมายเลข/ปี เช่น 1174/2568) - ไม่ซ้ำกัน';
COMMENT ON COLUMN criminal_cases.case_id IS 'รหัสคดี (Case ID) เช่น 6809044200';
COMMENT ON COLUMN criminal_cases.status IS 'สถานะคดี เช่น "ระหว่างสอบสวน", "จำหน่าย"';

-- Parties Involved
COMMENT ON COLUMN criminal_cases.complainant IS 'ผู้เสียหาย/ผู้กล่าวหา/ผู้ร้องทุกข์ (ฟิลด์หลักสำหรับชื่อผู้เสียหาย)';

-- Case Details
COMMENT ON COLUMN criminal_cases.case_type IS 'ประเภทคดี';
COMMENT ON COLUMN criminal_cases.damage_amount IS 'มูลค่าความเสียหาย (บาท)';

-- Important Dates
COMMENT ON COLUMN criminal_cases.complaint_date IS 'วันที่ร้องทุกข์/วันที่รับแจ้ง (รูปแบบ: YYYY-MM-DD)';
COMMENT ON COLUMN criminal_cases.incident_date IS 'วันที่เกิดเหตุ (รูปแบบ: YYYY-MM-DD)';
COMMENT ON COLUMN criminal_cases.last_update_date IS 'วันที่อัพเดตข้อมูลล่าสุด';

-- Court Information
COMMENT ON COLUMN criminal_cases.court_name IS 'ศาล/เขตอำนาจศาล';

-- Metadata
COMMENT ON COLUMN criminal_cases.created_at IS 'วันเวลาที่สร้างระเบียนในระบบ (Auto timestamp)';
COMMENT ON COLUMN criminal_cases.updated_at IS 'วันเวลาที่แก้ไขระเบียนล่าสุด (Auto timestamp)';
COMMENT ON COLUMN criminal_cases.created_by IS 'ผู้สร้างคดี (User ID) - บันทึกประวัติว่าใครสร้างคดีนี้ ไม่เปลี่ยนแปลง';
COMMENT ON COLUMN criminal_cases.owner_id IS 'เจ้าของคดี/ผู้รับผิดชอบปัจจุบัน (User ID) - สามารถโอนเปลี่ยนได้';

-- ========================================
-- ตาราง suspects
-- ========================================

COMMENT ON TABLE suspects IS 'ตารางข้อมูลผู้ต้องหา/หมายเรียกผู้ต้องหา';

-- Primary Key
COMMENT ON COLUMN suspects.id IS 'Primary Key - รหัsผู้ต้องหาในระบบ (Auto increment)';

-- Foreign Key
COMMENT ON COLUMN suspects.criminal_case_id IS 'Foreign Key - เชื่อมโยงกับคดีอาญา (criminal_cases.id)';

-- Document Information
COMMENT ON COLUMN suspects.document_number IS 'เลขที่หนังสือหมายเรียก';
COMMENT ON COLUMN suspects.document_date IS 'วันที่หนังสือหมายเรียก';

-- Suspect Information
COMMENT ON COLUMN suspects.suspect_name IS 'ชื่อ-สกุล ผู้ต้องหา (Required)';
COMMENT ON COLUMN suspects.suspect_id_card IS 'เลขบัตรประชาชนผู้ต้องหา (13 หลัก)';
COMMENT ON COLUMN suspects.suspect_address IS 'ที่อยู่ผู้ต้องหา';

-- Charge Information
COMMENT ON COLUMN suspects.charge_id IS 'Foreign Key - เชื่อมโยงกับตารางข้อหา Master Data (ใช้ในอนาคต)';

-- Police Station Information
COMMENT ON COLUMN suspects.police_station IS 'สถานีตำรวจที่ผู้ต้องหาต้องไปรายงานตัว';
COMMENT ON COLUMN suspects.police_province IS 'จังหวัดของสถานีตำรวจ';
COMMENT ON COLUMN suspects.police_address IS 'ที่อยู่สถานีตำรวจ';

-- Appointment Information
COMMENT ON COLUMN suspects.appointment_date IS 'วันนัดหมายให้ผู้ต้องหามารายงานตัว';
COMMENT ON COLUMN suspects.appointment_date_thai IS 'วันนัดหมาย (รูปแบบไทย พ.ศ.)';

-- Status
COMMENT ON COLUMN suspects.reply_status IS 'สถานะการมาตามนัด (true = มาแล้ว, false = ยังไม่มา)';
COMMENT ON COLUMN suspects.status IS 'สถานะการดำเนินการ เช่น "pending", "completed"';

-- Additional Fields from Migration
COMMENT ON COLUMN suspects.victim_name IS '[Legacy] ชื่อผู้เสียหาย - ใช้ criminal_cases.complainant แทน';
COMMENT ON COLUMN suspects.case_type IS '[Legacy] ประเภทคดี - ใช้ criminal_cases.case_type แทน';
COMMENT ON COLUMN suspects.damage_amount IS '[Legacy] มูลค่าความเสียหาย - ใช้ criminal_cases.damage_amount แทน';
COMMENT ON COLUMN suspects.case_id IS '[Legacy] รหัสคดี - ใช้ criminal_cases.case_id แทน';
COMMENT ON COLUMN suspects.complainant IS '[Legacy] ผู้กล่าวหา - ใช้ criminal_cases.complainant แทน';

-- Metadata
COMMENT ON COLUMN suspects.created_at IS 'วันเวลาที่สร้างระเบียน (Auto timestamp)';
COMMENT ON COLUMN suspects.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';
COMMENT ON COLUMN suspects.created_by IS 'ผู้สร้างระเบียน (User ID)';

-- ========================================
-- ตาราง bank_accounts
-- ========================================

COMMENT ON TABLE bank_accounts IS 'ตารางข้อมูลบัญชีธนาคาร/หมายเรียกธนาคาร';

-- Primary Key
COMMENT ON COLUMN bank_accounts.id IS 'Primary Key - รหัสบัญชีในระบบ (Auto increment)';

-- Foreign Keys
COMMENT ON COLUMN bank_accounts.criminal_case_id IS 'Foreign Key - เชื่อมโยงกับคดีอาญา (criminal_cases.id)';
COMMENT ON COLUMN bank_accounts.bank_id IS 'Foreign Key - เชื่อมโยงกับข้อมูลธนาคาร Master Data (banks.id)';

-- Document Information
COMMENT ON COLUMN bank_accounts.order_number IS 'ลำดับที่ของหนังสือ';
COMMENT ON COLUMN bank_accounts.document_number IS 'เลขที่หนังสือหมายเรียก';
COMMENT ON COLUMN bank_accounts.document_date IS 'วันที่หนังสือหมายเรียก';

-- Bank Information
COMMENT ON COLUMN bank_accounts.bank_name IS 'ชื่อธนาคาร (Required)';
COMMENT ON COLUMN bank_accounts.account_number IS 'เลขที่บัญชี (Required)';
COMMENT ON COLUMN bank_accounts.account_name IS 'ชื่อบัญชี/ชื่อเจ้าของบัญชี (Required)';

-- Legacy Fields (from old system)
COMMENT ON COLUMN bank_accounts.victim_name IS '[Legacy] ชื่อผู้เสียหาย - ใช้ criminal_cases.complainant แทน';
COMMENT ON COLUMN bank_accounts.case_id IS '[Legacy] รหัสคดี - ใช้ criminal_cases.case_id แทน';
COMMENT ON COLUMN bank_accounts.complainant IS '[Legacy] ผู้กล่าวหา - ใช้ criminal_cases.complainant แทน';

-- Transaction Information
COMMENT ON COLUMN bank_accounts.time_period IS 'ช่วงเวลาที่ขอข้อมูลรายการเดินบัญชี เช่น "1 มกราคม 2568 - 31 มกราคม 2568"';

-- Delivery Information
COMMENT ON COLUMN bank_accounts.delivery_date IS 'กำหนดวันที่ธนาคารต้องส่งเอกสาร';

-- Status and Response
COMMENT ON COLUMN bank_accounts.reply_status IS 'สถานะการตอบกลับ (true = ตอบแล้ว, false = ยังไม่ตอบ)';
COMMENT ON COLUMN bank_accounts.days_since_sent IS 'จำนวนวันนับจากส่งหมาย';
COMMENT ON COLUMN bank_accounts.notes IS 'หมายเหตุเพิ่มเติม';
COMMENT ON COLUMN bank_accounts.status IS 'สถานะการดำเนินการ';

-- Metadata
COMMENT ON COLUMN bank_accounts.created_at IS 'วันเวลาที่สร้างระเบียน (Auto timestamp)';
COMMENT ON COLUMN bank_accounts.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';
COMMENT ON COLUMN bank_accounts.created_by IS 'ผู้สร้างระเบียน (User ID)';

-- ========================================
-- ตาราง banks (Master Data)
-- ========================================

COMMENT ON TABLE banks IS 'ตารางข้อมูล Master Data ของธนาคาร (สำนักงานใหญ่)';

COMMENT ON COLUMN banks.id IS 'Primary Key - รหัสธนาคาร (Auto increment)';
COMMENT ON COLUMN banks.bank_name IS 'ชื่อธนาคาร (Unique) เช่น "ธนาคารกสิกรไทย"';

-- Address
COMMENT ON COLUMN banks.bank_address IS 'เลขที่สำนักงานใหญ่';
COMMENT ON COLUMN banks.soi IS 'ซอย';
COMMENT ON COLUMN banks.moo IS 'หมู่';
COMMENT ON COLUMN banks.road IS 'ถนน';
COMMENT ON COLUMN banks.sub_district IS 'แขวง/ตำบล';
COMMENT ON COLUMN banks.district IS 'เขต/อำเภอ';
COMMENT ON COLUMN banks.province IS 'จังหวัด';
COMMENT ON COLUMN banks.postal_code IS 'รหัสไปรษณีย์';

-- Metadata
COMMENT ON COLUMN banks.created_at IS 'วันเวลาที่สร้างระเบียน (Auto timestamp)';
COMMENT ON COLUMN banks.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';

-- ========================================
-- ตาราง users
-- ========================================

COMMENT ON TABLE users IS 'ตารางข้อมูลผู้ใช้งานระบบ';

COMMENT ON COLUMN users.id IS 'Primary Key - รหัสผู้ใช้ (Auto increment)';
COMMENT ON COLUMN users.username IS 'ชื่อผู้ใช้งาน (Unique) - สำหรับ Login';
COMMENT ON COLUMN users.email IS 'อีเมล (Unique)';
COMMENT ON COLUMN users.hashed_password IS 'รหัสผ่านที่เข้ารหัสแล้ว (Hashed)';
COMMENT ON COLUMN users.full_name IS 'ชื่อ-สกุล เต็ม';
COMMENT ON COLUMN users.role IS 'บทบาท/สิทธิ์ เช่น "admin", "user"';
COMMENT ON COLUMN users.is_active IS 'สถานะการใช้งาน (true = ใช้งานได้, false = ระงับ)';
COMMENT ON COLUMN users.created_at IS 'วันเวลาที่สร้างบัญชี (Auto timestamp)';
COMMENT ON COLUMN users.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';

-- ========================================
-- สรุป
-- ========================================
-- ✅ เพิ่ม COMMENT ให้ทุกตารางและทุกคอลัมน์
-- ✅ แสดงในช่อง "หมายเหตุ" ของ Adminer และ pgAdmin
-- ✅ ช่วยให้เข้าใจโครงสร้างฐานข้อมูลได้ง่ายขึ้น

SELECT 'Column comments added successfully!' as status;

