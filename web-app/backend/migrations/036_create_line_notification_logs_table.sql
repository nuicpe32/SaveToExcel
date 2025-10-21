-- 036_create_line_notification_logs_table.sql
-- สร้างตารางบันทึกประวัติการส่งการแจ้งเตือนผ่าน LINE

CREATE TABLE line_notification_logs (
    id SERIAL PRIMARY KEY,
    line_account_id INTEGER NOT NULL REFERENCES line_accounts(id) ON DELETE CASCADE,

    -- Notification Details
    notification_type VARCHAR(50) NOT NULL,
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,

    -- Related Data
    criminal_case_id INTEGER REFERENCES criminal_cases(id) ON DELETE SET NULL,

    -- Status
    status VARCHAR(20) DEFAULT 'pending',
    error_message TEXT,
    sent_at TIMESTAMPTZ,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_line_notification_logs_line_account_id ON line_notification_logs(line_account_id);
CREATE INDEX idx_line_notification_logs_status ON line_notification_logs(status);
CREATE INDEX idx_line_notification_logs_notification_type ON line_notification_logs(notification_type);
CREATE INDEX idx_line_notification_logs_criminal_case_id ON line_notification_logs(criminal_case_id);
CREATE INDEX idx_line_notification_logs_created_at ON line_notification_logs(created_at DESC);

-- Comments
COMMENT ON TABLE line_notification_logs IS 'บันทึกประวัติการส่งการแจ้งเตือนผ่าน LINE';
COMMENT ON COLUMN line_notification_logs.notification_type IS 'ประเภท: connection_test, new_case, case_update, summons_sent, email_opened';
COMMENT ON COLUMN line_notification_logs.title IS 'หัวข้อการแจ้งเตือน';
COMMENT ON COLUMN line_notification_logs.message IS 'ข้อความ';
COMMENT ON COLUMN line_notification_logs.status IS 'สถานะ: pending, sent, failed';
COMMENT ON COLUMN line_notification_logs.error_message IS 'ข้อความ error (ถ้ามี)';
COMMENT ON COLUMN line_notification_logs.sent_at IS 'เวลาที่ส่งสำเร็จ';
