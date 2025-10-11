-- Migration 016: สร้างตาราง exchanges (Master Data สำหรับผู้ให้บริการซื้อขายแลกเปลี่ยนสินทรัพย์ดิจิทัล)
-- วันที่: 10 ตุลาคม 2568

-- ========================================
-- สร้างตาราง exchanges
-- ========================================

CREATE TABLE IF NOT EXISTS exchanges (
    id SERIAL PRIMARY KEY,
    
    -- Company Information
    company_name VARCHAR(255) NOT NULL UNIQUE,
    company_name_short VARCHAR(100),  -- ชื่อย่อ เช่น "Bitkub", "Zipmex"
    company_name_alt VARCHAR(255),    -- ชื่อเดิม เช่น "Bitkub M" สำหรับ Orbix
    
    -- Address Information
    building_name VARCHAR(255),       -- ชื่ออาคาร
    company_address VARCHAR(255),     -- เลขที่
    floor VARCHAR(50),                -- ชั้น
    unit VARCHAR(100),                -- ห้อง/ยูนิต
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
    
    -- License Information
    license_number VARCHAR(100),      -- เลขที่ใบอนุญาต
    license_date DATE,                -- วันที่ออกใบอนุญาต
    
    -- Status
    is_active BOOLEAN DEFAULT TRUE,
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- สร้าง indexes
CREATE INDEX idx_exchanges_company_name ON exchanges(company_name);
CREATE INDEX idx_exchanges_company_name_short ON exchanges(company_name_short);
CREATE INDEX idx_exchanges_is_active ON exchanges(is_active);

-- เพิ่ม COMMENT
COMMENT ON TABLE exchanges IS 'ตารางข้อมูล Master Data ของผู้ให้บริการซื้อขายแลกเปลี่ยนสินทรัพย์ดิจิทัล (Crypto Exchange)';

COMMENT ON COLUMN exchanges.id IS 'Primary Key - รหัสผู้ให้บริการ (Auto increment)';
COMMENT ON COLUMN exchanges.company_name IS 'ชื่อบริษัทเต็ม (Unique)';
COMMENT ON COLUMN exchanges.company_name_short IS 'ชื่อย่อ/ชื่อแบรนด์ เช่น "Bitkub", "Zipmex"';
COMMENT ON COLUMN exchanges.company_name_alt IS 'ชื่อเดิม/ชื่อทางเลือก';

-- Address
COMMENT ON COLUMN exchanges.building_name IS 'ชื่ออาคาร';
COMMENT ON COLUMN exchanges.company_address IS 'เลขที่';
COMMENT ON COLUMN exchanges.floor IS 'ชั้น';
COMMENT ON COLUMN exchanges.unit IS 'ห้อง/ยูนิต';
COMMENT ON COLUMN exchanges.soi IS 'ซอย';
COMMENT ON COLUMN exchanges.moo IS 'หมู่';
COMMENT ON COLUMN exchanges.road IS 'ถนน';
COMMENT ON COLUMN exchanges.sub_district IS 'แขวง/ตำบล';
COMMENT ON COLUMN exchanges.district IS 'เขต/อำเภอ';
COMMENT ON COLUMN exchanges.province IS 'จังหวัด';
COMMENT ON COLUMN exchanges.postal_code IS 'รหัสไปรษณีย์';

-- Contact
COMMENT ON COLUMN exchanges.phone IS 'เบอร์โทรศัพท์';
COMMENT ON COLUMN exchanges.email IS 'อีเมล';
COMMENT ON COLUMN exchanges.website IS 'เว็บไซต์';

-- License
COMMENT ON COLUMN exchanges.license_number IS 'เลขที่ใบอนุญาตประกอบธุรกิจ';
COMMENT ON COLUMN exchanges.license_date IS 'วันที่ออกใบอนุญาต';

-- Status
COMMENT ON COLUMN exchanges.is_active IS 'สถานะการใช้งาน (true = ใช้งานได้, false = ระงับ)';

-- Metadata
COMMENT ON COLUMN exchanges.created_at IS 'วันเวลาที่สร้างระเบียน (Auto timestamp)';
COMMENT ON COLUMN exchanges.updated_at IS 'วันเวลาที่แก้ไขล่าสุด (Auto timestamp)';

-- ========================================
-- เพิ่มข้อมูลผู้ให้บริการ Crypto Exchange 7 บริษัท
-- ========================================

INSERT INTO exchanges (
    company_name,
    company_name_short,
    company_name_alt,
    building_name,
    company_address,
    floor,
    unit,
    road,
    sub_district,
    district,
    province,
    postal_code
) VALUES
    -- 1. Bitkub
    (
        'บริษัท บิทคับ ออนไลน์ จำกัด',
        'Bitkub',
        NULL,
        'อาคารเอฟวายไอ เซ็นเตอร์ ตึก 2',
        '2525',
        'ชั้น 11',
        'ยูนิต 2/1101-2/1107',
        'พระรามที่ 4',
        'คลองเตย',
        'คลองเตย',
        'กรุงเทพมหานคร',
        '10110'
    ),
    
    -- 2. Zipmex
    (
        'บริษัท ซิปเม็กซ์ จำกัด',
        'Zipmex',
        NULL,
        'อาคารเอ็มไพร์ ทาวเวอร์',
        '1',
        'ชั้น 47',
        NULL,
        'สาทรใต้',
        'ยานนาวา',
        'สาทร',
        'กรุงเทพมหานคร',
        '10120'
    ),
    
    -- 3. Satang Pro
    (
        'บริษัท สตางค์ คอร์ปอเรชั่น จำกัด',
        'Satang Pro',
        NULL,
        'อาคารแอทธินี ทาวเวอร์',
        '63',
        'ชั้น 23',
        'ห้องเลขที่ 2305-2307',
        'วิทยุ',
        'ลุมพินี',
        'ปทุมวัน',
        'กรุงเทพมหานคร',
        '10330'
    ),
    
    -- 4. Bitazza
    (
        'บริษัท บิทาซซ่า จำกัด',
        'Bitazza',
        NULL,
        'อาคารสยามพิวรรธน์ทาวเวอร์',
        '989',
        'ชั้นที่ 25',
        'ยูนิต A2 และ B2',
        'พระรามที่ 1',
        'ปทุมวัน',
        'ปทุมวัน',
        'กรุงเทพมหานคร',
        '10330'
    ),
    
    -- 5. Upbit
    (
        'บริษัท อัพบิต เอ็กซ์เชนจ์ (ประเทศไทย) จำกัด',
        'Upbit',
        NULL,
        'อาคารเอฟวายไอ เซ็นเตอร์ ตึก 1',
        '2525',
        'ชั้น 6,7 และ 8',
        NULL,
        'พระราม 4',
        'คลองเตย',
        'คลองเตย',
        'กรุงเทพมหานคร',
        '10110'
    ),
    
    -- 6. Orbix (ชื่อเดิม Bitkub M)
    (
        'บริษัท ออร์บิกซ์ เทรด จำกัด',
        'Orbix',
        'Bitkub M',
        'อาคารสีลมคอมเพล็กซ์',
        '191/2',
        'ชั้น 23',
        NULL,
        'สีลม',
        'สีลม',
        'บางรัก',
        'กรุงเทพมหานคร',
        '10500'
    ),
    
    -- 7. TDX
    (
        'บริษัท ศูนย์ซื้อขายสินทรัพย์ดิจิทัลไทย จำกัด',
        'TDX',
        NULL,
        NULL,
        '93',
        NULL,
        NULL,
        'รัชดาภิเษก',
        'ดินแดง',
        'ดินแดง',
        'กรุงเทพมหานคร',
        '10400'
    );

-- ========================================
-- ตรวจสอบผลลัพธ์
-- ========================================

SELECT 
    id,
    company_name_short,
    company_name,
    company_name_alt,
    CONCAT(
        COALESCE(building_name || ' ', ''),
        'เลขที่ ', company_address, ' ',
        COALESCE(floor || ' ', ''),
        COALESCE(unit || ' ', ''),
        COALESCE('ถนน ' || road, '')
    ) as address_line1,
    CONCAT(
        COALESCE('แขวง' || sub_district, ''), ' ',
        COALESCE('เขต' || district, '')
    ) as address_line2,
    CONCAT(province, ' ', postal_code) as address_line3
FROM exchanges
ORDER BY id;

-- ========================================
-- SUMMARY
-- ========================================

-- ✅ สร้างตาราง exchanges สำเร็จ
-- ✅ เพิ่มข้อมูล 7 บริษัท (Bitkub, Zipmex, Satang Pro, Bitazza, Upbit, Orbix, TDX)
-- ✅ รองรับข้อมูล floor และ unit สำหรับที่อยู่ที่ละเอียด
-- ✅ รองรับ company_name_alt สำหรับชื่อเดิม
-- ✅ พร้อมสำหรับพัฒนาฟีเจอร์หมายเรียก Crypto Exchange

SELECT 'Exchanges table created successfully!' as status,
       COUNT(*) as total_companies
FROM exchanges;

