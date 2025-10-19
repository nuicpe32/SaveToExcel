-- Migration: Add signature field to users table
-- Created: 2025-10-17
-- Description: เพิ่มฟิลด์สำหรับเก็บไฟล์ลายเซ็นของ user (PNG format)

-- เพิ่ม column signature_path สำหรับเก็บ path ของไฟล์ลายเซ็น
ALTER TABLE users ADD COLUMN IF NOT EXISTS signature_path VARCHAR(500);

-- เพิ่ม comment อธิบาย column
COMMENT ON COLUMN users.signature_path IS 'Path to user signature image file (PNG format)';

-- Index สำหรับค้นหา users ที่มีลายเซ็นแล้ว
CREATE INDEX IF NOT EXISTS idx_users_signature_path ON users(signature_path) WHERE signature_path IS NOT NULL;
