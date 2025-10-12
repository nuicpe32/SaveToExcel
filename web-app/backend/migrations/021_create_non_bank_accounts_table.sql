-- Migration: Create non_bank_accounts table
-- Date: 2025-10-11
-- Description: สร้างตารางสำหรับเก็บข้อมูลหมายเรียกผู้ให้บริการที่ไม่ใช่ธนาคาร (Non-Bank)

-- สร้างตาราง non_bank_accounts (คล้ายกับ bank_accounts)
CREATE TABLE IF NOT EXISTS non_bank_accounts (
    id SERIAL PRIMARY KEY,
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    non_bank_id INTEGER REFERENCES non_banks(id) ON DELETE SET NULL,
    
    -- ข้อมูลเอกสาร
    order_number INTEGER,
    document_number VARCHAR(100),
    document_date DATE,
    document_date_thai VARCHAR(100),
    
    -- ข้อมูลผู้ให้บริการและบัญชี
    provider_name VARCHAR(255) NOT NULL,  -- ชื่อผู้ให้บริการ (เช่น TrueMoney, AirPay)
    account_number VARCHAR(100) NOT NULL, -- เลขที่บัญชี/หมายเลขผู้ใช้
    account_name VARCHAR(255),            -- ชื่อบัญชี
    account_owner VARCHAR(255),           -- เจ้าของบัญชี
    
    -- ข้อมูลคดี
    complainant VARCHAR(255),             -- ผู้กล่าวหา/ผู้เสียหาย
    victim_name VARCHAR(255),             -- ชื่อผู้เสียหาย (deprecated - ใช้ complainant แทน)
    case_id VARCHAR(100),                 -- เลขคดี
    
    -- ช่วงเวลาที่ต้องการข้อมูล
    time_period VARCHAR(255),             -- ช่วงเวลาที่ทำธุรกรรม (text ภาษาไทย)
    
    -- การส่งหมายเรียก
    delivery_date DATE,                   -- กำหนดส่ง
    delivery_month VARCHAR(50),           -- เดือนที่กำหนดส่ง (สำหรับ filter)
    delivery_time VARCHAR(20),            -- เวลาที่กำหนดส่ง (09.00-16.00)
    
    -- สถานะ
    reply_status BOOLEAN DEFAULT FALSE,   -- สถานะตอบกลับ
    status VARCHAR(50) DEFAULT 'pending', -- สถานะทั่วไป (pending, sent, replied, etc.)
    
    -- การอายัด
    is_frozen BOOLEAN DEFAULT FALSE,      -- อายัดหรือไม่
    
    -- Audit fields
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL,
    
    CONSTRAINT unique_non_bank_account_per_case UNIQUE (criminal_case_id, provider_name, account_number)
);

-- สร้าง indexes
CREATE INDEX IF NOT EXISTS idx_non_bank_accounts_criminal_case_id ON non_bank_accounts(criminal_case_id);
CREATE INDEX IF NOT EXISTS idx_non_bank_accounts_non_bank_id ON non_bank_accounts(non_bank_id);
CREATE INDEX IF NOT EXISTS idx_non_bank_accounts_provider_name ON non_bank_accounts(provider_name);
CREATE INDEX IF NOT EXISTS idx_non_bank_accounts_reply_status ON non_bank_accounts(reply_status);
CREATE INDEX IF NOT EXISTS idx_non_bank_accounts_delivery_month ON non_bank_accounts(delivery_month);

-- เพิ่ม comments
COMMENT ON TABLE non_bank_accounts IS 'ตารางเก็บข้อมูลหมายเรียกผู้ให้บริการที่ไม่ใช่ธนาคาร (เช่น TrueMoney, AirPay, etc.)';
COMMENT ON COLUMN non_bank_accounts.provider_name IS 'ชื่อผู้ให้บริการ (เช่น TrueMoney Wallet, AirPay)';
COMMENT ON COLUMN non_bank_accounts.account_number IS 'เลขที่บัญชี/หมายเลขผู้ใช้/เบอร์โทรศัพท์';
COMMENT ON COLUMN non_bank_accounts.time_period IS 'ช่วงเวลาที่ทำธุรกรรม (รูปแบบภาษาไทย เช่น 1 ม.ค. 68 - 31 ม.ค. 68)';
COMMENT ON COLUMN non_bank_accounts.is_frozen IS 'ระบุว่าต้องการขอให้อายัดบัญชีหรือไม่';

-- สร้าง trigger สำหรับ updated_at
CREATE OR REPLACE FUNCTION update_non_bank_accounts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_non_bank_accounts_updated_at
    BEFORE UPDATE ON non_bank_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_non_bank_accounts_updated_at();

-- สรุป
SELECT 'non_bank_accounts table created successfully' AS status;

