-- Migration 029: Create email_logs table for tracking email deliveries
-- Created: 2025-10-14
-- Version: 3.6.0

CREATE TABLE IF NOT EXISTS email_logs (
    id SERIAL PRIMARY KEY,

    -- Account reference
    account_type VARCHAR(50) NOT NULL, -- 'non_bank', 'payment_gateway', 'telco_mobile', 'telco_internet', 'bank'
    account_id INTEGER NOT NULL, -- ID of the account record
    criminal_case_id INTEGER NOT NULL REFERENCES criminal_cases(id) ON DELETE CASCADE,

    -- Email details
    recipient_email VARCHAR(255) NOT NULL,
    subject VARCHAR(500) NOT NULL,
    document_type VARCHAR(50) NOT NULL, -- 'summons', 'envelope'

    -- Sending status
    status VARCHAR(20) NOT NULL DEFAULT 'pending', -- 'pending', 'sent', 'failed', 'bounced'
    sent_at TIMESTAMP,
    error_message TEXT,

    -- Retry mechanism
    retry_count INTEGER DEFAULT 0,
    last_retry_at TIMESTAMP,

    -- Tracking
    opened_at TIMESTAMP,
    opened_count INTEGER DEFAULT 0,

    -- Metadata
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    sent_by INTEGER REFERENCES users(id) ON DELETE SET NULL,

    -- PDF file reference (if stored)
    pdf_filename VARCHAR(255),
    pdf_size_bytes INTEGER
);

-- Create indexes for performance
CREATE INDEX idx_email_logs_account ON email_logs(account_type, account_id);
CREATE INDEX idx_email_logs_case ON email_logs(criminal_case_id);
CREATE INDEX idx_email_logs_status ON email_logs(status);
CREATE INDEX idx_email_logs_recipient ON email_logs(recipient_email);
CREATE INDEX idx_email_logs_sent_at ON email_logs(sent_at);

-- Add comments
COMMENT ON TABLE email_logs IS 'ตารางบันทึกประวัติการส่งอีเมล์หมายเรียกพยานเอกสาร';
COMMENT ON COLUMN email_logs.account_type IS 'ประเภทบัญชี: non_bank, payment_gateway, telco_mobile, telco_internet, bank';
COMMENT ON COLUMN email_logs.account_id IS 'ID ของบัญชีที่ส่งหมายเรียก';
COMMENT ON COLUMN email_logs.status IS 'สถานะการส่ง: pending, sent, failed, bounced';
COMMENT ON COLUMN email_logs.retry_count IS 'จำนวนครั้งที่พยายามส่งซ้ำ';
COMMENT ON COLUMN email_logs.opened_count IS 'จำนวนครั้งที่เปิดอ่านอีเมล์';
