-- 033_update_charges_table_structure.sql
-- อัพเดทโครงสร้างตาราง charges ให้ตรงกับข้อมูลจากไฟล์ Excel

-- Drop existing table if structure is completely different
DROP TABLE IF EXISTS charges CASCADE;

-- Create new charges table with proper structure
CREATE TABLE charges (
    id SERIAL PRIMARY KEY,
    charge_name VARCHAR(500) NOT NULL,  -- ชื่อข้อหา
    charge_description TEXT NOT NULL,   -- ข้อหา (รายละเอียดเต็ม)
    related_laws TEXT NOT NULL,         -- กฎหมายที่เกี่ยวข้อง
    penalty TEXT NOT NULL,              -- อัตราโทษ
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes
CREATE INDEX idx_charges_charge_name ON charges(charge_name);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION update_charges_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_charges_updated_at ON charges;
CREATE TRIGGER trigger_charges_updated_at
    BEFORE UPDATE ON charges
    FOR EACH ROW
    EXECUTE FUNCTION update_charges_updated_at();

-- Add comments
COMMENT ON TABLE charges IS 'ฐานข้อมูลความผิด (Master Data)';
COMMENT ON COLUMN charges.charge_name IS 'ชื่อข้อหา (ย่อ)';
COMMENT ON COLUMN charges.charge_description IS 'ข้อหา (รายละเอียดเต็ม)';
COMMENT ON COLUMN charges.related_laws IS 'กฎหมายที่เกี่ยวข้อง';
COMMENT ON COLUMN charges.penalty IS 'อัตราโทษ';

