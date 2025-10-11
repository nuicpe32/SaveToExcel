-- Migration 017: สร้างโครงสร้างหน่วยงานแบบลำดับชั้น (Bureau → Division → Supervision)
-- วันที่: 11 ตุลาคม 2568

-- ========================================
-- 1. สร้างตาราง bureaus (บช.)
-- ========================================

CREATE TABLE IF NOT EXISTS bureaus (
    id SERIAL PRIMARY KEY,
    name_full VARCHAR(255) NOT NULL UNIQUE,
    name_short VARCHAR(100) NOT NULL UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_bureaus_is_active ON bureaus(is_active);

COMMENT ON TABLE bureaus IS 'ตาราง Master Data ระดับบัญชาการ (บช.)';
COMMENT ON COLUMN bureaus.id IS 'Primary Key';
COMMENT ON COLUMN bureaus.name_full IS 'ชื่อเต็ม';
COMMENT ON COLUMN bureaus.name_short IS 'ชื่อย่อ';
COMMENT ON COLUMN bureaus.is_active IS 'สถานะการใช้งาน - Admin สามารถเปิด/ปิดสิทธิ์หน่วยงาน';

-- เพิ่มข้อมูล Bureau
INSERT INTO bureaus (name_full, name_short, is_active) VALUES
('กองบัญชาการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี', 'บช.สอท.', TRUE);

-- ========================================
-- 2. สร้างตาราง divisions (บก.)
-- ========================================

CREATE TABLE IF NOT EXISTS divisions (
    id SERIAL PRIMARY KEY,
    bureau_id INTEGER NOT NULL REFERENCES bureaus(id) ON DELETE CASCADE,
    name_full VARCHAR(255) NOT NULL,
    name_short VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(bureau_id, name_short)
);

CREATE INDEX idx_divisions_bureau_id ON divisions(bureau_id);
CREATE INDEX idx_divisions_is_active ON divisions(is_active);

COMMENT ON TABLE divisions IS 'ตาราง Master Data ระดับกองบังคับการ (บก.)';
COMMENT ON COLUMN divisions.id IS 'Primary Key';
COMMENT ON COLUMN divisions.bureau_id IS 'Foreign Key - เชื่อมโยงกับ bureaus';
COMMENT ON COLUMN divisions.name_full IS 'ชื่อเต็ม';
COMMENT ON COLUMN divisions.name_short IS 'ชื่อย่อ';
COMMENT ON COLUMN divisions.is_active IS 'สถานะการใช้งาน - Admin สามารถเปิด/ปิดสิทธิ์หน่วยงาน';

-- เพิ่มข้อมูล Divisions (7 กอง)
INSERT INTO divisions (bureau_id, name_full, name_short, is_active) VALUES
(1, 'กองบังคับการอำนวยการ', 'บก.อก.บช.สอท.', TRUE),
(1, 'กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 1', 'บก.สอท.1 บช.สอท.', TRUE),
(1, 'กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 2', 'บก.สอท.2 บช.สอท.', TRUE),
(1, 'กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 3', 'บก.สอท.3 บช.สอท.', TRUE),
(1, 'กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4', 'บก.สอท.4 บช.สอท.', TRUE),
(1, 'กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 5', 'บก.สอท.5 บช.สอท.', TRUE),
(1, 'กองบังคับการตรวจสอบและวิเคราะห์อาชญากรรมทางเทคโนโลยี', 'บก.ตอท. บช.สอท.', TRUE);

-- ========================================
-- 3. สร้างตาราง supervisions (กก.)
-- ========================================

CREATE TABLE IF NOT EXISTS supervisions (
    id SERIAL PRIMARY KEY,
    division_id INTEGER NOT NULL REFERENCES divisions(id) ON DELETE CASCADE,
    name_full VARCHAR(255) NOT NULL,
    name_short VARCHAR(100) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE,
    UNIQUE(division_id, name_short)
);

CREATE INDEX idx_supervisions_division_id ON supervisions(division_id);
CREATE INDEX idx_supervisions_is_active ON supervisions(is_active);

COMMENT ON TABLE supervisions IS 'ตาราง Master Data ระดับกองกำกับการ (กก.)';
COMMENT ON COLUMN supervisions.id IS 'Primary Key';
COMMENT ON COLUMN supervisions.division_id IS 'Foreign Key - เชื่อมโยงกับ divisions';
COMMENT ON COLUMN supervisions.name_full IS 'ชื่อเต็ม';
COMMENT ON COLUMN supervisions.name_short IS 'ชื่อย่อ';
COMMENT ON COLUMN supervisions.is_active IS 'สถานะการใช้งาน - Admin สามารถเปิด/ปิดสิทธิ์หน่วยงาน';

-- เพิ่มข้อมูล Supervisions
-- บก.สอท.1 (4 กก.)
INSERT INTO supervisions (division_id, name_full, name_short, is_active) VALUES
(2, 'กองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 1', 'กก.1 บก.สอท.1 บช.สอท.', TRUE),
(2, 'กองกำกับการ 2 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 1', 'กก.2 บก.สอท.1 บช.สอท.', TRUE),
(2, 'กองกำกับการ 3 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 1', 'กก.3 บก.สอท.1 บช.สอท.', TRUE),
(2, 'กองกำกับการ 4 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 1', 'กก.4 บก.สอท.1 บช.สอท.', TRUE);

-- บก.สอท.2 (4 กก.)
INSERT INTO supervisions (division_id, name_full, name_short, is_active) VALUES
(3, 'กองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 2', 'กก.1 บก.สอท.2 บช.สอท.', TRUE),
(3, 'กองกำกับการ 2 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 2', 'กก.2 บก.สอท.2 บช.สอท.', TRUE),
(3, 'กองกำกับการ 3 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 2', 'กก.3 บก.สอท.2 บช.สอท.', TRUE),
(3, 'กองกำกับการ 4 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 2', 'กก.4 บก.สอท.2 บช.สอท.', TRUE);

-- บก.สอท.3 (4 กก.)
INSERT INTO supervisions (division_id, name_full, name_short, is_active) VALUES
(4, 'กองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 3', 'กก.1 บก.สอท.3 บช.สอท.', TRUE),
(4, 'กองกำกับการ 2 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 3', 'กก.2 บก.สอท.3 บช.สอท.', TRUE),
(4, 'กองกำกับการ 3 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 3', 'กก.3 บก.สอท.3 บช.สอท.', TRUE),
(4, 'กองกำกับการ 4 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 3', 'กก.4 บก.สอท.3 บช.สอท.', TRUE);

-- บก.สอท.4 (4 กก.)
INSERT INTO supervisions (division_id, name_full, name_short, is_active) VALUES
(5, 'กองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4', 'กก.1 บก.สอท.4 บช.สอท.', TRUE),
(5, 'กองกำกับการ 2 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4', 'กก.2 บก.สอท.4 บช.สอท.', TRUE),
(5, 'กองกำกับการ 3 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4', 'กก.3 บก.สอท.4 บช.สอท.', TRUE),
(5, 'กองกำกับการ 4 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 4', 'กก.4 บก.สอท.4 บช.สอท.', TRUE);

-- บก.สอท.5 (4 กก.)
INSERT INTO supervisions (division_id, name_full, name_short, is_active) VALUES
(6, 'กองกำกับการ 1 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 5', 'กก.1 บก.สอท.5 บช.สอท.', TRUE),
(6, 'กองกำกับการ 2 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 5', 'กก.2 บก.สอท.5 บช.สอท.', TRUE),
(6, 'กองกำกับการ 3 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 5', 'กก.3 บก.สอท.5 บช.สอท.', TRUE),
(6, 'กองกำกับการ 4 กองบังคับการตำรวจสืบสวนสอบสวนอาชญากรรมทางเทคโนโลยี 5', 'กก.4 บก.สอท.5 บช.สอท.', TRUE);

-- ========================================
-- 4. เพิ่มฟิลด์ organization ในตาราง users
-- ========================================

ALTER TABLE users
    ADD COLUMN IF NOT EXISTS bureau_id INTEGER REFERENCES bureaus(id),
    ADD COLUMN IF NOT EXISTS division_id INTEGER REFERENCES divisions(id),
    ADD COLUMN IF NOT EXISTS supervision_id INTEGER REFERENCES supervisions(id);

CREATE INDEX IF NOT EXISTS idx_users_bureau_id ON users(bureau_id);
CREATE INDEX IF NOT EXISTS idx_users_division_id ON users(division_id);
CREATE INDEX IF NOT EXISTS idx_users_supervision_id ON users(supervision_id);

COMMENT ON COLUMN users.bureau_id IS 'หน่วยงานระดับ บช. (Required)';
COMMENT ON COLUMN users.division_id IS 'หน่วยงานระดับ บก. (Required)';
COMMENT ON COLUMN users.supervision_id IS 'หน่วยงานระดับ กก. (Required)';

-- ========================================
-- 5. อัพเดต User ที่มีอยู่ให้เป็น กก.1 บก.สอท.4
-- ========================================

-- หา ID ของหน่วยงาน กก.1 บก.สอท.4
-- Bureau ID = 1 (บช.สอท.)
-- Division ID = 5 (บก.สอท.4)
-- Supervision ID = 13 (กก.1 บก.สอท.4)

UPDATE users
SET 
    bureau_id = 1,
    division_id = 5,
    supervision_id = 13
WHERE bureau_id IS NULL;

-- ========================================
-- 6. ทำให้ organization fields เป็น NOT NULL
-- ========================================

-- ตรวจสอบว่าไม่มี NULL
SELECT COUNT(*) as users_without_organization
FROM users
WHERE bureau_id IS NULL OR division_id IS NULL OR supervision_id IS NULL;

-- ถ้าไม่มี NULL แล้ว ให้ทำเป็น NOT NULL
ALTER TABLE users
    ALTER COLUMN bureau_id SET NOT NULL,
    ALTER COLUMN division_id SET NOT NULL,
    ALTER COLUMN supervision_id SET NOT NULL;

-- ========================================
-- ตรวจสอบผลลัพธ์
-- ========================================

-- แสดงโครงสร้างหน่วยงาน
SELECT 
    b.name_short as bureau,
    d.name_short as division,
    s.name_short as supervision,
    s.is_active
FROM supervisions s
JOIN divisions d ON s.division_id = d.id
JOIN bureaus b ON d.bureau_id = b.id
ORDER BY d.id, s.id;

-- แสดงข้อมูล Users พร้อมหน่วยงาน
SELECT 
    u.id,
    u.username,
    u.full_name,
    b.name_short as bureau,
    d.name_short as division,
    s.name_short as supervision
FROM users u
LEFT JOIN bureaus b ON u.bureau_id = b.id
LEFT JOIN divisions d ON u.division_id = d.id
LEFT JOIN supervisions s ON u.supervision_id = s.id
ORDER BY u.id;

-- ========================================
-- SUMMARY
-- ========================================

SELECT 
    'Organization structure created successfully!' as status,
    (SELECT COUNT(*) FROM bureaus) as total_bureaus,
    (SELECT COUNT(*) FROM divisions) as total_divisions,
    (SELECT COUNT(*) FROM supervisions) as total_supervisions,
    (SELECT COUNT(*) FROM users WHERE supervision_id IS NOT NULL) as users_with_organization;

