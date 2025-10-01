-- Migration 004: Link existing bank_accounts and suspects to criminal_cases
-- This migration updates existing records to have criminal_case_id based on flexible name matching

-- Step 1: Link bank_accounts to criminal_cases using flexible matching
-- Match if criminal_case.complainant contains bank_account.complainant (removing spaces)
UPDATE bank_accounts ba
SET criminal_case_id = (
    SELECT cc.id
    FROM criminal_cases cc
    WHERE REPLACE(REPLACE(cc.complainant, ' ', ''), '.', '') LIKE '%' || REPLACE(REPLACE(ba.complainant, ' ', ''), '.', '') || '%'
    LIMIT 1
)
WHERE ba.criminal_case_id IS NULL
  AND ba.complainant IS NOT NULL
  AND ba.complainant != 'NaN'
  AND TRIM(ba.complainant) != '';

-- Step 2: Link suspects to criminal_cases using flexible matching
UPDATE suspects s
SET criminal_case_id = (
    SELECT cc.id
    FROM criminal_cases cc
    WHERE REPLACE(REPLACE(cc.complainant, ' ', ''), '.', '') LIKE '%' || REPLACE(REPLACE(s.complainant, ' ', ''), '.', '') || '%'
       OR REPLACE(REPLACE(cc.complainant, ' ', ''), '.', '') LIKE '%' || REPLACE(REPLACE(COALESCE(s.victim_name, ''), ' ', ''), '.', '') || '%'
    LIMIT 1
)
WHERE s.criminal_case_id IS NULL
  AND (s.complainant IS NOT NULL OR s.victim_name IS NOT NULL)
  AND COALESCE(s.complainant, s.victim_name, '') != '';

-- Step 3: Show statistics
SELECT 'Bank Accounts' as table_name,
       COUNT(*) as total_records,
       COUNT(criminal_case_id) as linked_records,
       COUNT(*) - COUNT(criminal_case_id) as unlinked_records
FROM bank_accounts
UNION ALL
SELECT 'Suspects' as table_name,
       COUNT(*) as total_records,
       COUNT(criminal_case_id) as linked_records,
       COUNT(*) - COUNT(criminal_case_id) as unlinked_records
FROM suspects;
