-- Migration Script: Make Foreign Keys NOT NULL
-- Created: 2025-10-01
-- Purpose: Ensure all child records have a parent criminal case

-- IMPORTANT: Run this AFTER ensuring all records have criminal_case_id

-- Step 1: Check for orphaned records in bank_accounts
DO $$
DECLARE
    orphan_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO orphan_count
    FROM bank_accounts
    WHERE criminal_case_id IS NULL;

    IF orphan_count > 0 THEN
        RAISE EXCEPTION 'Found % orphaned records in bank_accounts. Please fix before proceeding.', orphan_count;
    ELSE
        RAISE NOTICE 'No orphaned records in bank_accounts';
    END IF;
END $$;

-- Step 2: Check for orphaned records in suspects
DO $$
DECLARE
    orphan_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO orphan_count
    FROM suspects
    WHERE criminal_case_id IS NULL;

    IF orphan_count > 0 THEN
        RAISE EXCEPTION 'Found % orphaned records in suspects. Please fix before proceeding.', orphan_count;
    ELSE
        RAISE NOTICE 'No orphaned records in suspects';
    END IF;
END $$;

-- Step 3: Make criminal_case_id NOT NULL in bank_accounts
ALTER TABLE bank_accounts
ALTER COLUMN criminal_case_id SET NOT NULL;

RAISE NOTICE 'Set criminal_case_id to NOT NULL in bank_accounts';

-- Step 4: Make criminal_case_id NOT NULL in suspects
ALTER TABLE suspects
ALTER COLUMN criminal_case_id SET NOT NULL;

RAISE NOTICE 'Set criminal_case_id to NOT NULL in suspects';

-- Verify constraints
SELECT 'Column Constraints After Migration:' as status;
SELECT table_name, column_name, is_nullable
FROM information_schema.columns
WHERE table_name IN ('bank_accounts', 'suspects')
AND column_name = 'criminal_case_id';
