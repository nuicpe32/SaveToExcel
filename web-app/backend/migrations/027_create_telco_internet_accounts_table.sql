-- Migration 027: Create telco_internet_accounts table
-- สร้างตารางสำหรับเก็บข้อมูล IP Address ที่เกี่ยวข้องกับคดี
-- คล้ายกับ telco_mobile_accounts แต่สำหรับข้อมูล IP Address

-- Create telco_internet_accounts table
CREATE TABLE IF NOT EXISTS telco_internet_accounts (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    telco_internet_id INTEGER REFERENCES telco_internet(id) ON DELETE SET NULL,
    
    -- Document Information
    order_number INTEGER,
    document_number VARCHAR(255),
    document_date DATE,
    
    -- Telco Internet Information
    provider_name VARCHAR(255) NOT NULL,  -- ชื่อผู้ให้บริการ
    ip_address VARCHAR(100) NOT NULL,     -- IP Address
    
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
    CONSTRAINT fk_telco_internet_account_criminal_case FOREIGN KEY (criminal_case_id) 
        REFERENCES criminal_cases(id) ON DELETE CASCADE,
    CONSTRAINT fk_telco_internet_account_telco_internet FOREIGN KEY (telco_internet_id) 
        REFERENCES telco_internet(id) ON DELETE SET NULL
);

-- Create indexes for better query performance
CREATE INDEX idx_telco_internet_accounts_criminal_case_id ON telco_internet_accounts(criminal_case_id);
CREATE INDEX idx_telco_internet_accounts_telco_internet_id ON telco_internet_accounts(telco_internet_id);
CREATE INDEX idx_telco_internet_accounts_provider_name ON telco_internet_accounts(provider_name);
CREATE INDEX idx_telco_internet_accounts_ip_address ON telco_internet_accounts(ip_address);
CREATE INDEX idx_telco_internet_accounts_document_number ON telco_internet_accounts(document_number);
CREATE INDEX idx_telco_internet_accounts_reply_status ON telco_internet_accounts(reply_status);
CREATE INDEX idx_telco_internet_accounts_status ON telco_internet_accounts(status);
CREATE INDEX idx_telco_internet_accounts_order_number ON telco_internet_accounts(order_number);

-- Add comments to describe the table and columns
COMMENT ON TABLE telco_internet_accounts IS 'ตารางเก็บข้อมูล IP Address ที่เกี่ยวข้องกับคดีอาญา';
COMMENT ON COLUMN telco_internet_accounts.criminal_case_id IS 'Foreign Key ไปยัง criminal_cases - คดีที่เกี่ยวข้อง';
COMMENT ON COLUMN telco_internet_accounts.telco_internet_id IS 'Foreign Key ไปยัง telco_internet - ผู้ให้บริการ';
COMMENT ON COLUMN telco_internet_accounts.provider_name IS 'ชื่อผู้ให้บริการอินเทอร์เน็ต';
COMMENT ON COLUMN telco_internet_accounts.ip_address IS 'IP Address';
COMMENT ON COLUMN telco_internet_accounts.time_period IS 'ช่วงเวลาที่ขอข้อมูล';
COMMENT ON COLUMN telco_internet_accounts.reply_status IS 'สถานะการตอบกลับ (true = ตอบกลับแล้ว, false = ยังไม่ตอบกลับ)';
COMMENT ON COLUMN telco_internet_accounts.days_since_sent IS 'จำนวนวันนับจากวันที่ส่งเอกสาร';

