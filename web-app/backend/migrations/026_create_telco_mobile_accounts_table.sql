-- Migration 026: Create telco_mobile_accounts table
-- สร้างตารางสำหรับเก็บข้อมูลหมายเลขโทรศัพท์ที่เกี่ยวข้องกับคดี
-- คล้ายกับ bank_accounts แต่สำหรับข้อมูลโทรศัพท์

-- Create telco_mobile_accounts table
CREATE TABLE IF NOT EXISTS telco_mobile_accounts (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    telco_mobile_id INTEGER REFERENCES telco_mobile(id) ON DELETE SET NULL,
    
    -- Document Information
    order_number INTEGER,
    document_number VARCHAR(255),
    document_date DATE,
    
    -- Telco Information
    provider_name VARCHAR(255) NOT NULL,  -- ชื่อผู้ให้บริการ
    phone_number VARCHAR(50) NOT NULL,     -- หมายเลขโทรศัพท์
    
    -- Additional Information
    time_period VARCHAR(255),  -- ช่วงเวลาที่ขอข้อมูล
    
    -- Delivery Information
    delivery_date DATE,  -- กำหนดให้ส่งเอกสาร
    
    -- Status and Response
    reply_status BOOLEAN DEFAULT FALSE,
    days_since_sent INTEGER,
    
    -- Additional Information
    notes TEXT,
    status VARCHAR(100) DEFAULT 'pending',
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by INTEGER,
    
    -- Indexes
    CONSTRAINT fk_telco_mobile_account_criminal_case FOREIGN KEY (criminal_case_id) 
        REFERENCES criminal_cases(id) ON DELETE CASCADE,
    CONSTRAINT fk_telco_mobile_account_telco_mobile FOREIGN KEY (telco_mobile_id) 
        REFERENCES telco_mobile(id) ON DELETE SET NULL
);

-- Create indexes for better query performance
CREATE INDEX idx_telco_mobile_accounts_criminal_case_id ON telco_mobile_accounts(criminal_case_id);
CREATE INDEX idx_telco_mobile_accounts_telco_mobile_id ON telco_mobile_accounts(telco_mobile_id);
CREATE INDEX idx_telco_mobile_accounts_provider_name ON telco_mobile_accounts(provider_name);
CREATE INDEX idx_telco_mobile_accounts_phone_number ON telco_mobile_accounts(phone_number);
CREATE INDEX idx_telco_mobile_accounts_document_number ON telco_mobile_accounts(document_number);
CREATE INDEX idx_telco_mobile_accounts_reply_status ON telco_mobile_accounts(reply_status);
CREATE INDEX idx_telco_mobile_accounts_status ON telco_mobile_accounts(status);
CREATE INDEX idx_telco_mobile_accounts_order_number ON telco_mobile_accounts(order_number);

-- Add comments to describe the table and columns
COMMENT ON TABLE telco_mobile_accounts IS 'ตารางเก็บข้อมูลหมายเลขโทรศัพท์ที่เกี่ยวข้องกับคดีอาญา';
COMMENT ON COLUMN telco_mobile_accounts.criminal_case_id IS 'Foreign Key ไปยัง criminal_cases - คดีที่เกี่ยวข้อง';
COMMENT ON COLUMN telco_mobile_accounts.telco_mobile_id IS 'Foreign Key ไปยัง telco_mobile - ผู้ให้บริการ';
COMMENT ON COLUMN telco_mobile_accounts.provider_name IS 'ชื่อผู้ให้บริการโทรศัพท์ (AIS, True, dtac, etc.)';
COMMENT ON COLUMN telco_mobile_accounts.phone_number IS 'หมายเลขโทรศัพท์';
COMMENT ON COLUMN telco_mobile_accounts.time_period IS 'ช่วงเวลาที่ขอข้อมูล';
COMMENT ON COLUMN telco_mobile_accounts.reply_status IS 'สถานะการตอบกลับ (true = ตอบกลับแล้ว, false = ยังไม่ตอบกลับ)';
COMMENT ON COLUMN telco_mobile_accounts.days_since_sent IS 'จำนวนวันนับจากวันที่ส่งเอกสาร';

-- Grant permissions (if needed)
-- GRANT SELECT, INSERT, UPDATE, DELETE ON telco_mobile_accounts TO your_user;

