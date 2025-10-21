-- 035_create_line_accounts_table.sql
-- สร้างตารางเก็บข้อมูลการเชื่อมต่อบัญชี LINE ของผู้ใช้

CREATE TABLE line_accounts (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    -- LINE Profile
    line_user_id VARCHAR(100) NOT NULL UNIQUE,
    line_display_name VARCHAR(255),
    line_picture_url TEXT,
    line_status_message TEXT,

    -- OAuth Tokens (encrypted)
    access_token TEXT NOT NULL,
    refresh_token TEXT,
    token_expires_at TIMESTAMPTZ,

    -- Integration Status
    is_active BOOLEAN DEFAULT TRUE,
    linked_at TIMESTAMPTZ DEFAULT NOW(),
    last_used_at TIMESTAMPTZ,

    -- Notification Preferences
    notify_new_case BOOLEAN DEFAULT TRUE,
    notify_case_update BOOLEAN DEFAULT TRUE,
    notify_summons_sent BOOLEAN DEFAULT TRUE,
    notify_email_opened BOOLEAN DEFAULT TRUE,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(user_id)
);

-- Indexes
CREATE INDEX idx_line_accounts_user_id ON line_accounts(user_id);
CREATE INDEX idx_line_accounts_line_user_id ON line_accounts(line_user_id);
CREATE INDEX idx_line_accounts_is_active ON line_accounts(is_active);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_line_accounts_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_line_accounts_updated_at ON line_accounts;
CREATE TRIGGER trigger_line_accounts_updated_at
    BEFORE UPDATE ON line_accounts
    FOR EACH ROW
    EXECUTE FUNCTION update_line_accounts_updated_at();

-- Comments
COMMENT ON TABLE line_accounts IS 'ข้อมูลการเชื่อมต่อบัญชี LINE ของผู้ใช้';
COMMENT ON COLUMN line_accounts.line_user_id IS 'LINE User ID (ไม่ซ้ำกัน)';
COMMENT ON COLUMN line_accounts.line_display_name IS 'ชื่อที่แสดงใน LINE';
COMMENT ON COLUMN line_accounts.line_picture_url IS 'รูปโปรไฟล์ LINE';
COMMENT ON COLUMN line_accounts.access_token IS 'LINE Access Token (encrypted)';
COMMENT ON COLUMN line_accounts.refresh_token IS 'LINE Refresh Token (encrypted)';
COMMENT ON COLUMN line_accounts.is_active IS 'เปิดใช้งานหรือไม่';
COMMENT ON COLUMN line_accounts.notify_new_case IS 'แจ้งเตือนคดีใหม่';
COMMENT ON COLUMN line_accounts.notify_case_update IS 'แจ้งเตือนอัปเดตคดี';
COMMENT ON COLUMN line_accounts.notify_summons_sent IS 'แจ้งเตือนส่งหมายเรียก';
COMMENT ON COLUMN line_accounts.notify_email_opened IS 'แจ้งเตือนเปิดอีเมล์';
