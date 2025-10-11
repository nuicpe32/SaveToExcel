-- Migration 019: เพิ่มคอลัมน์ bank_code ในตาราง banks
-- วันที่: 11 ตุลาคม 2568

-- ========================================
-- 1. เพิ่มคอลัมน์ bank_code
-- ========================================

ALTER TABLE banks ADD COLUMN IF NOT EXISTS bank_code VARCHAR(10);

-- เพิ่ม index
CREATE INDEX IF NOT EXISTS idx_banks_bank_code ON banks(bank_code);

-- เพิ่ม comment
COMMENT ON COLUMN banks.bank_code IS 'รหัสธนาคาร 3 หลัก ตามมาตรฐาน Bank of Thailand';

-- ========================================
-- 2. อัพเดตข้อมูล bank_code
-- ========================================

-- ธนาคารกรุงเทพ
UPDATE banks SET bank_code = '002' WHERE bank_name = 'ธนาคารกรุงเทพ' OR bank_name LIKE '%กรุงเทพ%';

-- ธนาคารกสิกรไทย
UPDATE banks SET bank_code = '004' WHERE bank_name = 'ธนาคารกสิกรไทย' OR bank_name LIKE '%กสิกร%';

-- ธนาคารเดอะรอยัลแบงก์ออฟสกอตแลนด์
UPDATE banks SET bank_code = '006' WHERE bank_name LIKE '%รอยัลแบงก์%' OR bank_name LIKE '%Royal%';

-- ธนาคารกรุงไทย
UPDATE banks SET bank_code = '008' WHERE bank_name = 'ธนาคารกรุงไทย' OR bank_name LIKE '%กรุงไทย%';

-- ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร (ธ.ก.ส.)
UPDATE banks SET bank_code = '034' WHERE bank_name LIKE '%เกษตร%' OR bank_name LIKE '%ธ.ก.ส%' OR bank_name = 'ธนาคารเพื่อการเกษตรและสหกรณ์การเกษตร';

-- ธนาคารทหารไทยธนชาต (TMB)
UPDATE banks SET bank_code = '011' WHERE bank_name LIKE '%ทหารไทย%' OR bank_name LIKE '%TMB%' OR bank_name LIKE '%ธนชาต%';

-- ธนาคารไทยพาณิชย์ (SCB)
UPDATE banks SET bank_code = '014' WHERE bank_name = 'ธนาคารไทยพาณิชย์' OR bank_name LIKE '%ไทยพาณิชย์%' OR bank_name = 'SCB';

-- ธนาคารซิตี้แบงก์
UPDATE banks SET bank_code = '017' WHERE bank_name LIKE '%ซิตี้%' OR bank_name LIKE '%Citi%';

-- ธนาคารซูมิโตโม มิตซุย
UPDATE banks SET bank_code = '018' WHERE bank_name LIKE '%ซูมิโตโม%' OR bank_name LIKE '%Sumitomo%';

-- ธนาคารสแตนดาร์ดชาร์เตอร์ด
UPDATE banks SET bank_code = '020' WHERE bank_name LIKE '%สแตนดาร์ด%' OR bank_name LIKE '%Standard%';

-- ธนาคารซีไอเอ็มบี (CIMB)
UPDATE banks SET bank_code = '022' WHERE bank_name LIKE '%CIMB%' OR bank_name LIKE '%ซีไอเอ็มบี%';

-- ธนาคารยูโอบี (UOB)
UPDATE banks SET bank_code = '024' WHERE bank_name LIKE '%UOB%' OR bank_name LIKE '%ยูโอบี%';

-- ธนาคารกรุงศรีอยุธยา (BAY)
UPDATE banks SET bank_code = '025' WHERE bank_name = 'ธนาคารกรุงศรีอยุธยา' OR bank_name LIKE '%กรุงศรี%' OR bank_name = 'BAY';

-- ธนาคารเกียรตินาคินภัทร (KKP)
UPDATE banks SET bank_code = '026' WHERE bank_name LIKE '%เกียรตินาคิน%' OR bank_name LIKE '%KKP%';

-- ธนาคารแห่งอเมริกา
UPDATE banks SET bank_code = '027' WHERE bank_name LIKE '%อเมริกา%' OR bank_name LIKE '%America%';

-- ธนาคารออมสิน (GSB)
UPDATE banks SET bank_code = '030' WHERE bank_name = 'ธนาคารออมสิน' OR bank_name LIKE '%ออมสิน%' OR bank_name = 'GSB';

-- ธนาคารฮ่องกงและเซี่ยงไฮ้ (HSBC)
UPDATE banks SET bank_code = '031' WHERE bank_name LIKE '%ฮ่องกง%' OR bank_name LIKE '%HSBC%';

-- ธนาคารอาคารสงเคราะห์ (GHB)
UPDATE banks SET bank_code = '033' WHERE bank_name LIKE '%อาคารสงเคราะห์%' OR bank_name LIKE '%GHB%';

-- ธนาคารอิสลามแห่งประเทศไทย
-- หมายเหตุ: รหัส 033 ถูกใช้โดย ธนาคารอาคารสงเคราะห์ แล้ว

-- ธนาคารเพื่อการส่งออกและนำเข้าแห่งประเทศไทย (EXIM)
UPDATE banks SET bank_code = '035' WHERE bank_name LIKE '%ส่งออก%' OR bank_name LIKE '%นำเข้า%' OR bank_name LIKE '%EXIM%';

-- ธนาคารซูริไชน์
UPDATE banks SET bank_code = '039' WHERE bank_name LIKE '%ซูริไชน์%' OR bank_name LIKE '%Zuricher%';

-- ธนาคารไอซีบีซี (ICBC)
UPDATE banks SET bank_code = '070' WHERE bank_name LIKE '%ICBC%' OR bank_name LIKE '%ไอซีบีซี%';

-- ธนาคารทิสโก้ (TISCO)
UPDATE banks SET bank_code = '067' WHERE bank_name = 'ธนาคารทิสโก้' OR bank_name LIKE '%ทิสโก้%' OR bank_name LIKE '%TISCO%';

-- ธนาคารแลนด์ แอนด์ เฮ้าส์ (LH Bank)
UPDATE banks SET bank_code = '073' WHERE bank_name LIKE '%แลนด์%' OR bank_name LIKE '%เฮ้าส์%' OR bank_name LIKE '%LH%';

-- ========================================
-- 3. แสดงสรุปผลลัพธ์
-- ========================================

SELECT 
    'สรุปการอัพเดต bank_code' as summary,
    COUNT(*) as total_banks,
    COUNT(bank_code) as banks_with_code,
    COUNT(*) - COUNT(bank_code) as banks_without_code
FROM banks;

-- แสดงรายการธนาคารที่อัพเดตแล้ว
SELECT 
    bank_name,
    bank_code,
    CASE 
        WHEN bank_code IS NOT NULL THEN '✓ อัพเดตแล้ว'
        ELSE '✗ ยังไม่มีรหัส'
    END as status
FROM banks
ORDER BY bank_code NULLS LAST;

