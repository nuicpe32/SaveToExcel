-- Migration 010: Sync complainant และ victim_name
-- วัตถุประสงค์: ทำให้ complainant เป็นฟิลด์หลักสำหรับผู้เสียหาย/ผู้กล่าวหา
-- หมายเหตุ: ไม่ลบข้อมูลเดิม เก็บ victim_name ไว้เพื่อ backward compatibility

-- ========================================
-- STEP 1: Copy victim_name → complainant (ถ้า complainant เป็นค่าว่าง)
-- ========================================

-- กรณีที่ complainant เป็นค่าว่าง แต่มี victim_name ที่ไม่ใช่ "ดำเนินคดี"
UPDATE criminal_cases
SET complainant = victim_name
WHERE (complainant IS NULL OR complainant = '' OR complainant = 'nan')
  AND victim_name IS NOT NULL
  AND victim_name != ''
  AND victim_name != 'nan'
  AND victim_name != 'ดำเนินคดี';

-- ========================================
-- STEP 2: แก้ไขข้อมูล victim_name ที่เป็น "ดำเนินคดี"
-- ========================================

-- ถ้า victim_name = "ดำเนินคดี" ให้เปลี่ยนเป็น NULL
UPDATE criminal_cases
SET victim_name = NULL
WHERE victim_name = 'ดำเนินคดี';

-- ========================================
-- STEP 3: ตรวจสอบผลลัพธ์
-- ========================================

-- แสดงจำนวนคดีที่มี complainant
SELECT 
    COUNT(*) FILTER (WHERE complainant IS NOT NULL AND complainant != '') as has_complainant,
    COUNT(*) FILTER (WHERE complainant IS NULL OR complainant = '') as no_complainant,
    COUNT(*) FILTER (WHERE victim_name = 'ดำเนินคดี') as victim_name_invalid,
    COUNT(*) as total
FROM criminal_cases;

-- แสดงตัวอย่างข้อมูลที่อาจมีปัญหา
SELECT 
    id,
    case_number,
    complainant,
    victim_name
FROM criminal_cases
WHERE (complainant IS NULL OR complainant = '' OR complainant = 'nan')
  OR victim_name = 'ดำเนินคดี'
ORDER BY id
LIMIT 10;

-- ========================================
-- NOTES
-- ========================================

-- 1. ไม่ลบคอลัมน์ victim_name (เก็บไว้เพื่อ backward compatibility)
-- 2. ไม่บังคับให้ complainant เป็น NOT NULL (เพื่อให้ยืดหยุ่น)
-- 3. ข้อมูลเดิมจะไม่หาย เพียงแค่ sync ให้สอดคล้องกัน
-- 4. ต่อไปนี้ใช้ complainant เป็นฟิลด์หลักในการแสดงผล

-- Migration completed successfully!

