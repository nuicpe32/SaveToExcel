-- Migration 015: สร้างตาราง telco_internet (Master Data สำหรับผู้ให้บริการเครือข่ายอินเทอร์เน็ต)
-- วันที่: 10 ตุลาคม 2568

-- ========================================
-- สร้างตาราง telco_internet
-- ========================================

CREATE TABLE IF NOT EXISTS telco_internet (
    id SERIAL PRIMARY KEY,
    
    -- Company Information
    company_name VARCHAR(255) NOT NULL UNIQUE,
    company_name_short VARCHAR(100),  -- ชื่อย่อ เช่น "TRUE Online", "AIS Fibre", "3BB"
    
    -- Address Information
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
CREATE INDEX idx_telco_internet_company_name ON telco_internet(company_name);
CREATE INDEX idx_telco_internet_company_name_short ON telco_internet(company_name_short);
CREATE INDEX idx_telco_internet_is_active ON telco_internet(is_active);

-- เพิ่ม COMMENT
COMMENT ON TABLE telco_internet IS 'ตารางข้อมูล Master Data ของผู้ให้บริการเครือข่ายอินเทอร์เน็ต';

COMMENT ON COLUMN telco_internet.id IS 'Primary Key - รหัสผู้ให้บริการ (Auto increment)';
COMMENT ON COLUMN telco_internet.company_name IS 'ชื่อบริษัทเต็ม (Unique)';
COMMENT ON COLUMN telco_internet.company_name_short IS 'ชื่อย่อ/ชื่อแบรนด์ เช่น "TRUE Online", "AIS Fibre", "3BB"';

-- Address
COMMENT ON COLUMN telco_internet.building_name IS 'ชื่ออาคาร';
COMMENT ON COLUMN telco_internet.company_address IS 'เลขที่';
COMMENT ON COLUMN telco_internet.soi IS 'ซอย';
COMMENT ON COLUMN telco_internet.moo IS 'หมู่';
COMMENT ON COLUMN telco_internet.road IS 'ถนน';
COMMENT ON COLUMN telco_internet.sub_district IS 'แขวง/ตำบล';
COMMENT ON COLUMN telco_internet.district IS 'เขต/อำเภอ';
COMMENT ON COLUMN telco_internet.province IS 'จังหวัด';
COMMENT ON COLUMN telco_internet.postal_code IS 'รหัสไปรษณีย์';

-- Contact
COMMENT ON COLUMN telco_internet.phone IS 'เบอร์โทรศัพท์';
COMMENT ON COLUMN telco_internet.email IS 'อีเมล';
COMMENT ON COLUMN telco_internet.website IS 'เว็บไซต์';

-- Status
COMMENT ON COLUMN telco_internet.is_active IS 'สถานะการใช้งาน (true = ใช้งานได้, false = ระงับ)';

-- Metadata
COMMENT ON COLUMN telco_internet.created_at IS 'วันเวลาที่สร้างระเบียน (Auto timestamp)';
COMMENT ON COLUMN telco_internet.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';

-- ========================================
-- เพิ่มข้อมูลผู้ให้บริการอินเทอร์เน็ต 4 บริษัท
-- ========================================

INSERT INTO telco_internet (
    company_name,
    company_name_short,
    building_name,
    company_address,
    moo,
    road,
    sub_district,
    district,
    province,
    postal_code
) VALUES
    -- 1. TRUE Online
    (
        'บริษัท ทรู คอร์ปอเรชั่น จำกัด (มหาชน)',
        'TRUE Online',
        'อาคารทรู ทาวเวอร์',
        '18',
        NULL,
        'รัชดาภิเษก',
        'ห้วยขวาง',
        'ห้วยขวาง',
        'กรุงเทพมหานคร',
        '10310'
    ),
    
    -- 2. AIS Fibre
    (
        'บริษัท แอดวานซ์ อินโฟร์ เซอร์วิส จำกัด (มหาชน)',
        'AIS Fibre',
        'อาคารเอไอเอส ทาวเวอร์ 1',
        '414',
        NULL,
        'พหลโยธิน',
        'สามเสนใน',
        'พญาไท',
        'กรุงเทพมหานคร',
        '10400'
    ),
    
    -- 3. 3BB
    (
        'บริษัท ทริปเปิลที บรอดแบนด์ จำกัด (มหาชน)',
        '3BB',
        'อาคารจัสมิน อินเตอร์เนชั่นแนล ทาวเวอร์',
        '200',
        '4',
        'แจ้งวัฒนะ',
        'ปากเกร็ด',
        'ปากเกร็ด',
        'นนทบุรี',
        '11120'
    ),
    
    -- 4. NT Broadband
    (
        'บริษัท โทรคมนาคมแห่งชาติ จำกัด (มหาชน)',
        'NT Broadband',
        NULL,
        '99',
        NULL,
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
        COALESCE('หมู่ ' || moo || ' ', ''),
        COALESCE('ถนน ' || road, '')
    ) as address_line1,
    CONCAT(
        COALESCE('แขวง' || sub_district, 'ตำบล' || sub_district), ' ',
        COALESCE('เขต' || district, 'อำเภอ' || district)
    ) as address_line2,
    CONCAT(province, ' ', postal_code) as address_line3
FROM telco_internet
ORDER BY id;

-- ========================================
-- SUMMARY
-- ========================================

-- ✅ สร้างตาราง telco_internet สำเร็จ
-- ✅ เพิ่มข้อมูล 4 บริษัท (TRUE Online, AIS Fibre, 3BB, NT Broadband)
-- ✅ โครงสร้างเหมือน banks, non_banks และ telco_mobile
-- ✅ พร้อมสำหรับพัฒนาฟีเจอร์หมายเรียก Telco Internet

SELECT 'Telco Internet table created successfully!' as status,
       COUNT(*) as total_companies
FROM telco_internet;

