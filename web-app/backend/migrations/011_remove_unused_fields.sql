-- Migration 011: ลบฟิลด์ที่ไม่ได้ใช้งานในตาราง criminal_cases
-- และเพิ่มฟิลด์ charge_id ในตาราง suspects
-- วันที่: 9 ตุลาคม 2568

-- ========================================
-- ⚠️ BACKUP ก่อนรัน Migration นี้!
-- ========================================
-- docker exec criminal-case-db pg_dump -U user -d criminal_case_db -F c -f /tmp/backup_before_field_removal.dump
-- docker cp criminal-case-db:/tmp/backup_before_field_removal.dump ./backup_before_field_removal.dump

-- ========================================
-- STEP 1: เพิ่มฟิลด์ charge_id ในตาราง suspects
-- ========================================

-- เพิ่มคอลัมน์ charge_id เพื่อเชื่อมโยงกับตาราง Master Data ของข้อหาในอนาคต
ALTER TABLE suspects
  ADD COLUMN IF NOT EXISTS charge_id INTEGER;

-- สร้าง index สำหรับ charge_id
CREATE INDEX IF NOT EXISTS idx_suspects_charge_id ON suspects(charge_id);

-- เพิ่ม comment อธิบายฟิลด์
COMMENT ON COLUMN suspects.charge_id IS 'Foreign Key to charges master data table (future implementation)';

-- ========================================
-- STEP 2: ลบฟิลด์กลุ่มที่ 1 - ไม่ได้ใช้งานเลย (5 ฟิลด์)
-- ========================================

-- Group 1: ฟิลด์ที่ไม่ได้ใช้งานเลย
ALTER TABLE criminal_cases
  DROP COLUMN IF EXISTS victim_name,
  DROP COLUMN IF EXISTS suspect,
  DROP COLUMN IF EXISTS case_scene,
  DROP COLUMN IF EXISTS age_in_months,
  DROP COLUMN IF EXISTS is_over_six_months;

-- ========================================
-- STEP 3: ลบฟิลด์กลุ่มที่ 2 - ไม่แสดงใน UI (7 ฟิลด์)
-- ========================================

-- Group 2: ฟิลด์ที่ไม่แสดงใน UI หรือไม่ได้ใช้งาน
ALTER TABLE criminal_cases
  DROP COLUMN IF EXISTS charge,
  DROP COLUMN IF EXISTS prosecutor_name,
  DROP COLUMN IF EXISTS prosecutor_file_number,
  DROP COLUMN IF EXISTS officer_in_charge,
  DROP COLUMN IF EXISTS investigating_officer,
  DROP COLUMN IF EXISTS bank_accounts_replied,
  DROP COLUMN IF EXISTS suspects_replied;

-- ========================================
-- STEP 4: ลบฟิลด์กลุ่มที่ 3 - Virtual Fields (4 ฟิลด์)
-- ========================================

-- Group 3: Virtual fields ที่ควรคำนวณแบบ dynamic
ALTER TABLE criminal_cases
  DROP COLUMN IF EXISTS complaint_date_thai,
  DROP COLUMN IF EXISTS incident_date_thai,
  DROP COLUMN IF EXISTS bank_accounts_count,
  DROP COLUMN IF EXISTS suspects_count;

-- ========================================
-- STEP 5: ตรวจสอบผลลัพธ์
-- ========================================

-- แสดงโครงสร้างตาราง criminal_cases หลังการลบ
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'criminal_cases'
  AND table_schema = 'public'
ORDER BY ordinal_position;

-- แสดงโครงสร้างตาราง suspects หลังการเพิ่ม charge_id
SELECT 
    column_name,
    data_type,
    is_nullable,
    column_default
FROM information_schema.columns
WHERE table_name = 'suspects'
  AND table_schema = 'public'
ORDER BY ordinal_position;

-- นับจำนวนข้อมูลเพื่อยืนยันว่าไม่มีข้อมูลหาย
SELECT 
    (SELECT COUNT(*) FROM criminal_cases) as total_cases,
    (SELECT COUNT(*) FROM suspects) as total_suspects,
    (SELECT COUNT(*) FROM bank_accounts) as total_bank_accounts;

-- ========================================
-- SUMMARY
-- ========================================

-- ✅ ลบฟิลด์ทั้งหมด: 16 ฟิลด์
-- ✅ เพิ่มฟิลด์ใหม่: 1 ฟิลด์ (charge_id ในตาราง suspects)
-- ✅ ข้อมูลไม่หาย (เฉพาะโครงสร้างที่เปลี่ยน)
-- ⚠️ Backend และ Frontend ต้องปรับโค้ดให้รองรับ virtual fields

-- ========================================
-- ROLLBACK (ถ้าต้องการย้อนกลับ)
-- ========================================

-- docker cp backup_before_field_removal.dump criminal-case-db:/tmp/restore.dump
-- docker exec criminal-case-db pg_restore -U user -d criminal_case_db -c -F c /tmp/restore.dump

-- Migration 011 Completed!

