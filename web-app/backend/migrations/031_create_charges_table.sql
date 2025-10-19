-- 031_create_charges_table.sql
-- สร้างตารางฐานข้อมูลความผิด (charges)

CREATE TABLE IF NOT EXISTS charges (
    id SERIAL PRIMARY KEY,
    title_th VARCHAR(255) NOT NULL,
    title_en VARCHAR(255),
    law_name VARCHAR(255),
    section VARCHAR(100),
    code VARCHAR(100),
    description TEXT,
    penalty TEXT,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_charges_title_th ON charges(title_th);
CREATE INDEX IF NOT EXISTS idx_charges_section ON charges(section);
CREATE INDEX IF NOT EXISTS idx_charges_code ON charges(code);
CREATE INDEX IF NOT EXISTS idx_charges_is_active ON charges(is_active);

-- Trigger to auto-update updated_at
CREATE OR REPLACE FUNCTION set_updated_at_timestamp()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_charges_updated_at ON charges;
CREATE TRIGGER trg_charges_updated_at
BEFORE UPDATE ON charges
FOR EACH ROW EXECUTE FUNCTION set_updated_at_timestamp();

