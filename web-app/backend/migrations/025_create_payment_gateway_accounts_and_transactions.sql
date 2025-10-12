-- Migration: สร้างตาราง payment_gateway_accounts และ payment_gateway_transactions
-- วันที่: 12 ตุลาคม 2568
-- คำอธิบาย: สร้างตารางสำหรับจัดการบัญชี Payment Gateway และรายการโอนเงิน

-- ============================================================================
-- 1. สร้างตาราง payment_gateway_accounts
-- ============================================================================

CREATE TABLE IF NOT EXISTS payment_gateway_accounts (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    payment_gateway_id INTEGER REFERENCES payment_gateways(id) ON DELETE SET NULL,
    
    -- ข้อมูลเอกสาร
    document_number VARCHAR(100),
    document_date DATE,
    
    -- ข้อมูลบัญชี
    account_number VARCHAR(100) NOT NULL,
    account_name VARCHAR(255),
    
    -- ช่วงเวลาที่ต้องการข้อมูล
    time_period VARCHAR(255),
    
    -- การส่งหมายเรียก
    delivery_date DATE,
    
    -- สถานะ
    reply_status BOOLEAN DEFAULT FALSE,
    status VARCHAR(50) DEFAULT 'pending',
    
    -- Audit fields
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by INTEGER REFERENCES users(id) ON DELETE SET NULL
);

-- สร้าง indexes
CREATE INDEX idx_payment_gateway_accounts_criminal_case_id ON payment_gateway_accounts(criminal_case_id);
CREATE INDEX idx_payment_gateway_accounts_payment_gateway_id ON payment_gateway_accounts(payment_gateway_id);
CREATE INDEX idx_payment_gateway_accounts_reply_status ON payment_gateway_accounts(reply_status);

-- เพิ่ม comments
COMMENT ON TABLE payment_gateway_accounts IS 'ตารางเก็บข้อมูลหมายเรียกผู้ให้บริการ Payment Gateway';
COMMENT ON COLUMN payment_gateway_accounts.criminal_case_id IS 'รหัสคดี';
COMMENT ON COLUMN payment_gateway_accounts.payment_gateway_id IS 'รหัสผู้ให้บริการ Payment Gateway (FK to payment_gateways)';

-- ============================================================================
-- 2. สร้างตาราง payment_gateway_transactions
-- ============================================================================

CREATE TABLE IF NOT EXISTS payment_gateway_transactions (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Keys
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    payment_gateway_account_id INTEGER NOT NULL REFERENCES payment_gateway_accounts(id) ON DELETE CASCADE,
    
    -- บัญชีต้นทาง (Source Account)
    source_bank_id INTEGER REFERENCES banks(id) ON DELETE SET NULL,
    source_account_number VARCHAR(100),
    source_account_name VARCHAR(255),
    
    -- บัญชีปลายทาง (Destination Account)
    destination_payment_gateway_id INTEGER REFERENCES payment_gateways(id) ON DELETE SET NULL,
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
CREATE INDEX idx_payment_gateway_transactions_criminal_case_id ON payment_gateway_transactions(criminal_case_id);
CREATE INDEX idx_payment_gateway_transactions_payment_gateway_account_id ON payment_gateway_transactions(payment_gateway_account_id);
CREATE INDEX idx_payment_gateway_transactions_source_bank_id ON payment_gateway_transactions(source_bank_id);
CREATE INDEX idx_payment_gateway_transactions_destination_payment_gateway_id ON payment_gateway_transactions(destination_payment_gateway_id);
CREATE INDEX idx_payment_gateway_transactions_transfer_date ON payment_gateway_transactions(transfer_date);

-- เพิ่ม comments
COMMENT ON TABLE payment_gateway_transactions IS 'ตารางเก็บรายละเอียดการโอนเงินสำหรับ Payment Gateway Accounts';
COMMENT ON COLUMN payment_gateway_transactions.criminal_case_id IS 'รหัสคดี';
COMMENT ON COLUMN payment_gateway_transactions.payment_gateway_account_id IS 'รหัสบัญชี Payment Gateway';
COMMENT ON COLUMN payment_gateway_transactions.source_bank_id IS 'รหัสธนาคารต้นทาง (FK to banks)';
COMMENT ON COLUMN payment_gateway_transactions.destination_payment_gateway_id IS 'รหัสผู้ให้บริการปลายทาง (FK to payment_gateways)';

