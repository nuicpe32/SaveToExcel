-- Migration: สร้างตาราง non_bank_transactions
-- วันที่: 12 ตุลาคม 2568
-- คำอธิบาย: เก็บรายละเอียดการโอนเงินสำหรับ Non-Bank Accounts

-- สร้างตาราง non_bank_transactions
CREATE TABLE IF NOT EXISTS non_bank_transactions (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    non_bank_account_id INTEGER NOT NULL REFERENCES non_bank_accounts(id) ON DELETE CASCADE,
    
    -- บัญชีต้นทาง (Source Account)
    source_bank_id INTEGER REFERENCES banks(id) ON DELETE SET NULL,
    source_bank_name VARCHAR(255),
    source_account_number VARCHAR(100),
    source_account_name VARCHAR(255),
    
    -- บัญชีปลายทาง (Destination Account)
    destination_provider_name VARCHAR(255),
    destination_account_number VARCHAR(100),
    destination_account_name VARCHAR(255),
    
    -- ข้อมูลการโอน
    transfer_date DATE,
    transfer_time VARCHAR(20),
    transfer_amount NUMERIC(15, 2),
    
    -- หมายเหตุ
    note VARCHAR(500),
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);

-- สร้าง indexes
CREATE INDEX idx_non_bank_transactions_criminal_case_id ON non_bank_transactions(criminal_case_id);
CREATE INDEX idx_non_bank_transactions_non_bank_account_id ON non_bank_transactions(non_bank_account_id);
CREATE INDEX idx_non_bank_transactions_source_bank_id ON non_bank_transactions(source_bank_id);
CREATE INDEX idx_non_bank_transactions_transfer_date ON non_bank_transactions(transfer_date);

-- เพิ่ม comments
COMMENT ON TABLE non_bank_transactions IS 'ตารางเก็บรายละเอียดการโอนเงินสำหรับ Non-Bank Accounts';
COMMENT ON COLUMN non_bank_transactions.criminal_case_id IS 'รหัสคดี';
COMMENT ON COLUMN non_bank_transactions.non_bank_account_id IS 'รหัสบัญชี Non-Bank';
COMMENT ON COLUMN non_bank_transactions.source_bank_id IS 'รหัสธนาคารต้นทาง (FK to banks)';
COMMENT ON COLUMN non_bank_transactions.source_bank_name IS 'ชื่อธนาคารต้นทาง';
COMMENT ON COLUMN non_bank_transactions.source_account_number IS 'เลขที่บัญชีต้นทาง';
COMMENT ON COLUMN non_bank_transactions.source_account_name IS 'ชื่อบัญชีต้นทาง';
COMMENT ON COLUMN non_bank_transactions.destination_provider_name IS 'ผู้ให้บริการปลายทาง';
COMMENT ON COLUMN non_bank_transactions.destination_account_number IS 'เลขที่บัญชีปลายทาง';
COMMENT ON COLUMN non_bank_transactions.destination_account_name IS 'ชื่อบัญชีปลายทาง';
COMMENT ON COLUMN non_bank_transactions.transfer_date IS 'วันที่โอน';
COMMENT ON COLUMN non_bank_transactions.transfer_time IS 'เวลาที่โอน';
COMMENT ON COLUMN non_bank_transactions.transfer_amount IS 'จำนวนเงินที่โอน';

