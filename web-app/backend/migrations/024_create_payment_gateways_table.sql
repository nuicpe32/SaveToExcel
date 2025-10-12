-- Migration: สร้างตาราง payment_gateways และย้ายข้อมูล Payment Gateway
-- วันที่: 12 ตุลาคม 2568
-- คำอธิบาย: แยก Payment Gateway ออกจาก Non-Bank เพื่อความชัดเจน

-- ============================================================================
-- 1. สร้างตาราง payment_gateways
-- ============================================================================

CREATE TABLE IF NOT EXISTS payment_gateways (
    id SERIAL PRIMARY KEY,
    
    -- Company Information
    company_name VARCHAR(255) NOT NULL UNIQUE,
    company_name_short VARCHAR(100),
    
    -- Address Information
    company_address VARCHAR(255),
    soi VARCHAR(100),
    moo VARCHAR(50),
    road VARCHAR(100),
    sub_district VARCHAR(100),
    district VARCHAR(100),
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
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- สร้าง indexes
CREATE INDEX idx_payment_gateways_company_name ON payment_gateways(company_name);
CREATE INDEX idx_payment_gateways_company_name_short ON payment_gateways(company_name_short);
CREATE INDEX idx_payment_gateways_is_active ON payment_gateways(is_active);

-- เพิ่ม comments
COMMENT ON TABLE payment_gateways IS 'ตาราง Master Data สำหรับผู้ให้บริการชำระเงิน (Payment Gateway)';
COMMENT ON COLUMN payment_gateways.company_name IS 'ชื่อบริษัทเต็ม';
COMMENT ON COLUMN payment_gateways.company_name_short IS 'ชื่อย่อ เช่น Omise, 2C2P';

-- ============================================================================
-- 2. ย้ายข้อมูล Payment Gateway จาก non_banks
-- ============================================================================

-- ย้าย Omise, GB Prime Pay, 2C2P
INSERT INTO payment_gateways (
    company_name,
    company_name_short,
    company_address,
    soi,
    moo,
    road,
    sub_district,
    district,
    province,
    postal_code,
    phone,
    email,
    website,
    is_active,
    created_at,
    updated_at
)
SELECT 
    company_name,
    company_name_short,
    company_address,
    soi,
    moo,
    road,
    sub_district,
    district,
    province,
    postal_code,
    phone,
    email,
    website,
    is_active,
    created_at,
    updated_at
FROM non_banks
WHERE company_name_short IN ('Omise', 'GB Prime Pay', '2C2P');

-- ============================================================================
-- 3. ลบข้อมูล Payment Gateway จาก non_banks
-- ============================================================================

DELETE FROM non_banks
WHERE company_name_short IN ('Omise', 'GB Prime Pay', '2C2P');

-- ============================================================================
-- 4. แสดงผลลัพธ์
-- ============================================================================

-- ตรวจสอบข้อมูลใน payment_gateways
SELECT COUNT(*) as total_payment_gateways FROM payment_gateways;

-- ตรวจสอบข้อมูลที่เหลือใน non_banks
SELECT COUNT(*) as remaining_non_banks FROM non_banks;

