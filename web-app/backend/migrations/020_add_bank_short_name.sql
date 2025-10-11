-- Migration 020: เพิ่มคอลัมน์ bank_short_name ในตาราง banks
-- วันที่: 11 ตุลาคม 2568

-- ========================================
-- 1. เพิ่มคอลัมน์ bank_short_name
-- ========================================

ALTER TABLE banks ADD COLUMN IF NOT EXISTS bank_short_name VARCHAR(20);

-- เพิ่ม index
CREATE INDEX IF NOT EXISTS idx_banks_bank_short_name ON banks(bank_short_name);

-- เพิ่ม comment
COMMENT ON COLUMN banks.bank_short_name IS 'ชื่อย่อธนาคาร (ภาษาอังกฤษ) ตามมาตรฐาน เช่น BBL, KBANK, SCB';

-- ========================================
-- 2. อัพเดตข้อมูล bank_short_name ตาม bank_code
-- ========================================

-- BBL (002) - ธนาคารกรุงเทพ
UPDATE banks SET bank_short_name = 'BBL' WHERE bank_code = '002';

-- KBANK (004) - ธนาคารกสิกรไทย
UPDATE banks SET bank_short_name = 'KBANK' WHERE bank_code = '004';

-- KTB (008) - ธนาคารกรุงไทย (ในฐานข้อมูลใช้ 008 แต่ใน map เป็น 006)
UPDATE banks SET bank_short_name = 'KTB' WHERE bank_code = '008';

-- TTB (011) - ธนาคารทหารไทยธนชาต
UPDATE banks SET bank_short_name = 'TTB' WHERE bank_code = '011';

-- SCB (014) - ธนาคารไทยพาณิชย์
UPDATE banks SET bank_short_name = 'SCB' WHERE bank_code = '014';

-- CIMBT (022) - ธนาคารซีไอเอ็มบีไทย
UPDATE banks SET bank_short_name = 'CIMBT' WHERE bank_code = '022';

-- UOBT (024) - ธนาคารยูโอบี
UPDATE banks SET bank_short_name = 'UOBT' WHERE bank_code = '024';

-- BAY (025) - ธนาคารกรุงศรีอยุธยา
UPDATE banks SET bank_short_name = 'BAY' WHERE bank_code = '025';

-- KKP (026) - ธนาคารเกียรตินาคินภัทร (ในฐานข้อมูลใช้ 026 แต่ใน map เป็น 069)
UPDATE banks SET bank_short_name = 'KKP' WHERE bank_code = '026';

-- GSB (030) - ธนาคารออมสิน
UPDATE banks SET bank_short_name = 'GSB' WHERE bank_code = '030';

-- GHB (033) - ธนาคารอาคารสงเคราะห์
UPDATE banks SET bank_short_name = 'GHB' WHERE bank_code = '033';

-- BAAC (034) - ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร
UPDATE banks SET bank_short_name = 'BAAC' WHERE bank_code = '034';

-- TISCO (067) - ธนาคารทิสโก้
UPDATE banks SET bank_short_name = 'TISCO' WHERE bank_code = '067';

-- ICBCT (070) - ธนาคารไอซีบีซี (ถ้ามีในฐานข้อมูล)
UPDATE banks SET bank_short_name = 'ICBCT' WHERE bank_code = '070';

-- LH (073) - ธนาคารแลนด์แอนด์เฮ้าส์
UPDATE banks SET bank_short_name = 'LH' WHERE bank_code = '073';

-- ========================================
-- 3. แสดงสรุปผลลัพธ์
-- ========================================

SELECT 
    'สรุปการอัพเดต bank_short_name' as summary,
    COUNT(*) as total_banks,
    COUNT(bank_short_name) as banks_with_short_name,
    COUNT(*) - COUNT(bank_short_name) as banks_without_short_name
FROM banks;

-- แสดงรายการธนาคารที่อัพเดตแล้ว
SELECT 
    bank_code,
    bank_short_name,
    bank_name,
    CASE 
        WHEN bank_short_name IS NOT NULL THEN '✓ อัพเดตแล้ว'
        ELSE '✗ ยังไม่มีชื่อย่อ'
    END as status
FROM banks
ORDER BY bank_code::integer NULLS LAST;

