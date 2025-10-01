-- Migration 006: Move case_type from suspects to criminal_cases

-- Step 1: Add case_type column to criminal_cases
ALTER TABLE criminal_cases
ADD COLUMN IF NOT EXISTS case_type VARCHAR;

-- Step 2: Migrate case_type data from suspects to criminal_cases
-- Use the case_type from the first suspect of each case
UPDATE criminal_cases cc
SET case_type = s.case_type
FROM (
    SELECT DISTINCT ON (criminal_case_id)
        criminal_case_id,
        case_type
    FROM suspects
    WHERE case_type IS NOT NULL
    ORDER BY criminal_case_id, id
) s
WHERE cc.id = s.criminal_case_id
  AND cc.case_type IS NULL;

-- Step 3: Show statistics
SELECT
    'Criminal Cases' as table_name,
    COUNT(*) as total_records,
    COUNT(case_type) as with_case_type
FROM criminal_cases
UNION ALL
SELECT
    'Suspects' as table_name,
    COUNT(*) as total_records,
    COUNT(case_type) as with_case_type
FROM suspects;

-- Step 4: Show sample data
SELECT
    cc.case_number,
    cc.case_type as case_type_in_cases,
    s.case_type as case_type_in_suspects,
    CASE
        WHEN cc.case_type = s.case_type THEN 'MATCH'
        WHEN cc.case_type IS NULL AND s.case_type IS NULL THEN 'BOTH NULL'
        WHEN cc.case_type IS NULL THEN 'CASE NULL'
        WHEN s.case_type IS NULL THEN 'SUSPECT NULL'
        ELSE 'MISMATCH'
    END as status
FROM criminal_cases cc
LEFT JOIN suspects s ON s.criminal_case_id = cc.id
WHERE cc.id IN (
    SELECT DISTINCT criminal_case_id
    FROM suspects
    WHERE case_type IS NOT NULL
    LIMIT 5
)
ORDER BY cc.case_number;

-- Note: We'll keep case_type in suspects for now (won't drop it yet)
-- This allows for gradual migration and rollback if needed
