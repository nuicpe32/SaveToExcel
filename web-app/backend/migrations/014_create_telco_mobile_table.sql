-- Migration 014: สร้างตาราง telco_mobile (Master Data สำหรับผู้ให้บริการเครือข่ายโทรศัพท์มือถือ)
-- วันที่: 10 ตุลาคม 2568

-- ========================================
-- สร้างตาราง telco_mobile
-- ========================================

CREATE TABLE IF NOT EXISTS telco_mobile (
    id SERIAL PRIMARY KEY,
    
    -- Company Information
    company_name VARCHAR(255) NOT NULL UNIQUE,
    company_name_short VARCHAR(100),  -- ชื่อย่อ เช่น "AIS", "True", "dtac"
    
    -- Address Information (เหมือนตาราง banks และ non_banks)
    building_name VARCHAR(255),       -- ชื่ออาคาร
    company_address VARCHAR(255),     -- เลขที่
    soi VARCHAR(100),
    moo VARCHAR(50),
    road VARCHAR(100),
    sub_district VARCHAR(100),        -- แขวง/ตำบล
    district VARCHAR(100),            -- เขต/อำเภอ
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
CREATE INDEX idx_telco_mobile_company_name ON telco_mobile(company_name);
CREATE INDEX idx_telco_mobile_company_name_short ON telco_mobile(company_name_short);
CREATE INDEX idx_telco_mobile_is_active ON telco_mobile(is_active);

-- เพิ่ม COMMENT
COMMENT ON TABLE telco_mobile IS 'ตารางข้อมูล Master Data ของผู้ให้บริการเครือข่ายโทรศัพท์มือถือ';

COMMENT ON COLUMN telco_mobile.id IS 'Primary Key - รหัสผู้ให้บริการ (Auto increment)';
COMMENT ON COLUMN telco_mobile.company_name IS 'ชื่อบริษัทเต็ม (Unique) เช่น "บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)"';
COMMENT ON COLUMN telco_mobile.company_name_short IS 'ชื่อย่อ/ชื่อแบรนด์ เช่น "AIS", "True", "dtac"';

-- Address
COMMENT ON COLUMN telco_mobile.building_name IS 'ชื่ออาคาร เช่น "อาคารเอไอเอส ทาวเวอร์ 1"';
COMMENT ON COLUMN telco_mobile.company_address IS 'เลขที่';
COMMENT ON COLUMN telco_mobile.soi IS 'ซอย';
COMMENT ON COLUMN telco_mobile.moo IS 'หมู่';
COMMENT ON COLUMN telco_mobile.road IS 'ถนน';
COMMENT ON COLUMN telco_mobile.sub_district IS 'แขวง/ตำบล';
COMMENT ON COLUMN telco_mobile.district IS 'เขต/อำเภอ';
COMMENT ON COLUMN telco_mobile.province IS 'จังหวัด';
COMMENT ON COLUMN telco_mobile.postal_code IS 'รหัสไปรษณีย์';

-- Contact
COMMENT ON COLUMN telco_mobile.phone IS 'เบอร์โทรศัพท์';
COMMENT ON COLUMN telco_mobile.email IS 'อีเมล';
COMMENT ON COLUMN telco_mobile.website IS 'เว็บไซต์';

-- Status
COMMENT ON COLUMN telco_mobile.is_active IS 'สถานะการใช้งาน (true = ใช้งานได้, false = ระงับ)';

-- Metadata
COMMENT ON COLUMN telco_mobile.created_at IS 'วันเวลาที่สร้างระเบียน (Auto timestamp)';
COMMENT ON COLUMN telco_mobile.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';

-- ========================================
-- เพิ่มข้อมูลผู้ให้บริการเครือข่ายมือถือ 3 บริษัท
-- ========================================

INSERT INTO telco_mobile (
    company_name,
    company_name_short,
    building_name,
    company_address,
    road,
    sub_district,
    district,
    province,
    postal_code
) VALUES
    -- 1. AIS
    (
        'บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)',
        'AIS',
        'อาคารเอไอเอส ทาวเวอร์ 1',
        '414',
        'พหลโยธิน',
        'สามเสนใน',
        'พญาไท',
        'กรุงเทพมหานคร',
        '10400'
    ),
    
    -- 2. True
    (
        'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)',
        'True',
        'อาคารทรู ทาวเวอร์',
        '18',
        'รัชดาภิเษก',
        'ห้วยขวาง',
        'ห้วยขวาง',
        'กรุงเทพมหานคร',
        '10310'
    ),
    
    -- 3. dtac (NT)
    (
        'บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน)',
        'dtac',
        NULL,
        '99',
        'แจ้งวัฒนะ',
        'ทุ่งสองห้อง',
        'หลักสี่',
        'กรุงเทพมหานคร',
        '10210'
    );

-- ========================================
-- ตรวจสอบผลลัพธ์
-- ========================================

SELECT 
    id,
    company_name_short,
    company_name,
    CONCAT(
        COALESCE(building_name || ' ', ''),
        'เลขที่ ', company_address, ' ',
        COALESCE('ถนน ' || road, '')
    ) as address_line1,
    CONCAT('แขวง', sub_district, ' ', 'เขต', district) as address_line2,
    CONCAT(province, ' ', postal_code) as address_line3
FROM telco_mobile
ORDER BY id;

-- ========================================
-- SUMMARY
-- ========================================

-- ✅ สร้างตาราง telco_mobile สำเร็จ
-- ✅ เพิ่มข้อมูล 3 บริษัท (AIS, True, dtac)
-- ✅ โครงสร้างเหมือน banks และ non_banks table
-- ✅ พร้อมสำหรับพัฒนาฟีเจอร์หมายเรียก Telco Mobile

SELECT 'Telco Mobile table created successfully!' as status,
       COUNT(*) as total_companies
FROM telco_mobile;

