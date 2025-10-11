-- Migration 018: สร้างตาราง cfr (Central Fraud Registry - ข้อมูลเส้นทางการเงิน)
-- วันที่: 11 ตุลาคม 2568

-- ========================================
-- สร้างตาราง cfr
-- ========================================

CREATE TABLE IF NOT EXISTS cfr (
    id SERIAL PRIMARY KEY,
    
    -- Foreign Key to Criminal Case
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,
    
    -- File Information
    filename VARCHAR(255) NOT NULL,  -- ชื่อไฟล์ CFR ที่อัพโหลด
    upload_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- CFR Response Data
    response_id BIGINT,
    bank_case_id VARCHAR(100),
    timestamp_insert VARCHAR(50),
    
    -- From Account (ต้นทาง)
    from_bank_code INTEGER,
    from_bank_short_name VARCHAR(50),
    from_account_no VARCHAR(50),
    from_account_name VARCHAR(255),
    
    -- To Account (ปลายทาง)
    to_bank_code INTEGER,
    to_bank_short_name VARCHAR(50),
    to_bank_branch VARCHAR(100),
    to_id_type VARCHAR(50),
    to_id VARCHAR(50),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    phone_number VARCHAR(50),
    
    -- PromptPay Information
    promptpay_type VARCHAR(50),
    promptpay_id VARCHAR(50),
    
    -- To Account Details
    to_account_no VARCHAR(50),
    to_account_name VARCHAR(255),
    to_account_status VARCHAR(50),
    to_open_date VARCHAR(50),
    to_close_date VARCHAR(50),
    to_balance DECIMAL(15, 2),
    
    -- Transfer Information
    transfer_date VARCHAR(50),
    transfer_channel VARCHAR(100),
    transfer_channel_detail VARCHAR(255),
    transfer_time VARCHAR(50),
    transfer_amount DECIMAL(15, 2),
    transfer_description TEXT,
    transfer_ref VARCHAR(100),
    
    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    created_by INTEGER
);

-- สร้าง indexes
CREATE INDEX idx_cfr_criminal_case_id ON cfr(criminal_case_id);
CREATE INDEX idx_cfr_filename ON cfr(filename);
CREATE INDEX idx_cfr_bank_case_id ON cfr(bank_case_id);
CREATE INDEX idx_cfr_from_account_no ON cfr(from_account_no);
CREATE INDEX idx_cfr_to_account_no ON cfr(to_account_no);
CREATE INDEX idx_cfr_transfer_date ON cfr(transfer_date);
CREATE INDEX idx_cfr_upload_date ON cfr(upload_date);

-- Composite index for case + filename (สำหรับการลบข้อมูลเดิมก่อน insert)
CREATE INDEX idx_cfr_case_filename ON cfr(criminal_case_id, filename);

-- เพิ่ม COMMENT
COMMENT ON TABLE cfr IS 'ตารางข้อมูล Central Fraud Registry (CFR) - เส้นทางการเงิน/รายการโอนเงิน';

COMMENT ON COLUMN cfr.id IS 'Primary Key';
COMMENT ON COLUMN cfr.criminal_case_id IS 'Foreign Key - เชื่อมโยงกับคดีอาญา';
COMMENT ON COLUMN cfr.filename IS 'ชื่อไฟล์ CFR ที่อัพโหลด (ใช้ตรวจสอบไฟล์ซ้ำ)';
COMMENT ON COLUMN cfr.upload_date IS 'วันเวลาที่อัพโหลดไฟล์';

-- CFR Data
COMMENT ON COLUMN cfr.response_id IS 'Response ID จาก CFR';
COMMENT ON COLUMN cfr.bank_case_id IS 'Bank Case ID';
COMMENT ON COLUMN cfr.timestamp_insert IS 'เวลาที่ insert ข้อมูลใน CFR';

-- From Account
COMMENT ON COLUMN cfr.from_bank_code IS 'รหัสธนาคารต้นทาง';
COMMENT ON COLUMN cfr.from_bank_short_name IS 'ชื่อย่อธนาคารต้นทาง';
COMMENT ON COLUMN cfr.from_account_no IS 'เลขบัญชีต้นทาง';
COMMENT ON COLUMN cfr.from_account_name IS 'ชื่อบัญชีต้นทาง';

-- To Account
COMMENT ON COLUMN cfr.to_bank_code IS 'รหัสธนาคารปลายทาง';
COMMENT ON COLUMN cfr.to_bank_short_name IS 'ชื่อย่อธนาคารปลายทาง';
COMMENT ON COLUMN cfr.to_account_no IS 'เลขบัญชีปลายทาง';
COMMENT ON COLUMN cfr.to_account_name IS 'ชื่อบัญชีปลายทาง';
COMMENT ON COLUMN cfr.to_balance IS 'ยอดเงินคงเหลือ (บาท)';

-- Transfer
COMMENT ON COLUMN cfr.transfer_date IS 'วันที่โอนเงิน';
COMMENT ON COLUMN cfr.transfer_time IS 'เวลาที่โอนเงิน';
COMMENT ON COLUMN cfr.transfer_amount IS 'จำนวนเงินที่โอน (บาท)';
COMMENT ON COLUMN cfr.transfer_channel IS 'ช่องทางการโอน เช่น EBank, Mobile Banking';

-- ========================================
-- SUMMARY
-- ========================================

SELECT 'CFR table created successfully!' as status;

