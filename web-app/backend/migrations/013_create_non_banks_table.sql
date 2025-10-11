-- Migration 013: สร้างตาราง non_banks (Master Data สำหรับบริษัท Non-Bank)
-- วันที่: 10 ตุลาคม 2568

-- ========================================
-- สร้างตาราง non_banks
-- ========================================

CREATE TABLE IF NOT EXISTS non_banks (
    id SERIAL PRIMARY KEY,
    
    -- Company Information
    company_name VARCHAR(255) NOT NULL UNIQUE,
    company_name_short VARCHAR(100),  -- ชื่อย่อ เช่น "Omise", "TrueMoney"
    
    -- Address Information (เหมือนตาราง banks)
    company_address VARCHAR(255),  -- เลขที่ + อาคาร + ชั้น
    soi VARCHAR(100),
    moo VARCHAR(50),
    road VARCHAR(100),
    sub_district VARCHAR(100),  -- แขวง/ตำบล
    district VARCHAR(100),      -- เขต/อำเภอ
    province VARCHAR(100),
    postal_code VARCHAR(10),
    
    -- Contact Information
    phone VARCHAR(50),
    email VARCHAR(100),
    website VARCHAR(255),
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- สร้าง indexes
CREATE INDEX idx_non_banks_company_name ON non_banks(company_name);
CREATE INDEX idx_non_banks_company_name_short ON non_banks(company_name_short);
CREATE INDEX idx_non_banks_is_active ON non_banks(is_active);

-- เพิ่ม COMMENT
COMMENT ON TABLE non_banks IS 'ตารางข้อมูล Master Data ของบริษัท Non-Bank (Payment Gateway, E-Wallet)';

COMMENT ON COLUMN non_banks.id IS 'Primary Key - รหัสบริษัท (Auto increment)';
COMMENT ON COLUMN non_banks.company_name IS 'ชื่อบริษัทเต็ม (Unique) เช่น "บริษัท โอมิเซะ จำกัด"';
COMMENT ON COLUMN non_banks.company_name_short IS 'ชื่อย่อ/ชื่อบริการ เช่น "Omise", "TrueMoney"';

-- Address
COMMENT ON COLUMN non_banks.company_address IS 'เลขที่ + อาคาร + ชั้น';
COMMENT ON COLUMN non_banks.soi IS 'ซอย';
COMMENT ON COLUMN non_banks.moo IS 'หมู่';
COMMENT ON COLUMN non_banks.road IS 'ถนน';
COMMENT ON COLUMN non_banks.sub_district IS 'แขวง/ตำบล';
COMMENT ON COLUMN non_banks.district IS 'เขต/อำเภอ';
COMMENT ON COLUMN non_banks.province IS 'จังหวัด';
COMMENT ON COLUMN non_banks.postal_code IS 'รหัสไปรษณีย์';

-- Contact
COMMENT ON COLUMN non_banks.phone IS 'เบอร์โทรศัพท์';
COMMENT ON COLUMN non_banks.email IS 'อีเมล';
COMMENT ON COLUMN non_banks.website IS 'เว็บไซต์';

-- Status
COMMENT ON COLUMN non_banks.is_active IS 'สถานะการใช้งาน (true = ใช้งานได้, false = ระงับ)';

-- Metadata
COMMENT ON COLUMN non_banks.created_at IS 'วันเวลาที่สร้างระเบียน (Auto timestamp)';
COMMENT ON COLUMN non_banks.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';

-- ========================================
-- เพิ่มข้อมูล Non-Bank บริษัททั้ง 4 บริษัท
-- ========================================

INSERT INTO non_banks (
    company_name,
    company_name_short,
    company_address,
    soi,
    road,
    sub_district,
    district,
    province,
    postal_code
) VALUES
    -- 1. Omise
    (
        'บริษัท โอมิเซะ จำกัด',
        'Omise',
        '1448/4 อาคารเจ 2',
        'ลาดพร้าว 87 (จันทราสุข)',
        'ประดิษฐ์มนูธรรม',
        'คลองจั่น',
        'บางกะปิ',
        'กรุงเทพมหานคร',
        '10240'
    ),
    
    -- 2. GB Prime Pay
    (
        'บริษัท โกลบอล ไพร์ม คอร์ปอเรชั่น จำกัด',
        'GB Prime Pay',
        '554/81-82 สกายวาย 9 เซ็นเตอร์ ชั้น 16',
        NULL,
        'ดินแดง',
        'ดินแดง',
        'ดินแดง',
        'กรุงเทพมหานคร',
        '10400'
    ),
    
    -- 3. 2C2P
    (
        'บริษัท ทูซีทูพี (ประเทศไทย) จำกัด',
        '2C2P',
        '1 อาคารเอ็มไพร์ทาวเวอร์ ชั้น 51',
        NULL,
        'สาทรใต้',
        'ยานนาวา',
        'สาทร',
        'กรุงเทพมหานคร',
        '10120'
    ),
    
    -- 4. TrueMoney
    (
        'บริษัท ทรู มันนี่ จำกัด',
        'TrueMoney',
        '101 อาคารทรู ดิจิทัล พาร์ค ตึกฟีนิกซ์ ชั้น 7-8',
        NULL,
        'สุขุมวิท',
        'บางจาก',
        'พระโขนง',
        'กรุงเทพมหานคร',
        '10260'
    );

-- ========================================
-- ตรวจสอบผลลัพธ์
-- ========================================

SELECT 
    id,
    company_name_short,
    company_name,
    CONCAT(company_address, ' ', COALESCE('ซอย ' || soi, ''), ' ', COALESCE('ถนน ' || road, '')) as address_line1,
    CONCAT(COALESCE('แขวง' || sub_district, ''), ' ', COALESCE('เขต' || district, '')) as address_line2,
    CONCAT(province, ' ', postal_code) as address_line3
FROM non_banks
ORDER BY id;

-- ========================================
-- SUMMARY
-- ========================================

-- ✅ สร้างตาราง non_banks สำเร็จ
-- ✅ เพิ่มข้อมูล 4 บริษัท
-- ✅ โครงสร้างเหมือน banks table
-- ✅ พร้อมสำหรับพัฒนาฟีเจอร์หมายเรียก Non-Bank

SELECT 'Non-Banks table created successfully!' as status,
       COUNT(*) as total_companies
FROM non_banks;

