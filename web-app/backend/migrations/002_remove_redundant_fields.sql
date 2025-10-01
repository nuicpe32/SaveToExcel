-- Migration Script: Remove Redundant Fields
-- Created: 2025-10-01
-- Purpose: Remove duplicate fields from bank_accounts and suspects tables

-- IMPORTANT: Run this AFTER updating application code to use relationships

-- Backup reminder
DO $$
BEGIN
    RAISE NOTICE '=================================================';
    RAISE NOTICE 'WARNING: This migration will DROP columns!';
    RAISE NOTICE 'Make sure you have a backup before proceeding.';
    RAISE NOTICE '=================================================';
END $$;

-- Step 1: Remove redundant fields from bank_accounts
-- These fields are already in criminal_cases table
ALTER TABLE bank_accounts
DROP COLUMN IF EXISTS complainant,
DROP COLUMN IF EXISTS victim_name,
DROP COLUMN IF EXISTS case_id;

RAISE NOTICE 'Removed redundant fields from bank_accounts';

-- Step 2: Remove redundant fields from suspects
ALTER TABLE suspects
DROP COLUMN IF EXISTS complainant,
DROP COLUMN IF EXISTS victim_name,
DROP COLUMN IF EXISTS case_id,
DROP COLUMN IF EXISTS damage_amount;

RAISE NOTICE 'Removed redundant fields from suspects';

-- Step 3: Verify table structure
SELECT 'Bank Accounts Columns After Cleanup:' as status;
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'bank_accounts'
ORDER BY ordinal_position;

SELECT 'Suspects Columns After Cleanup:' as status;
SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_name = 'suspects'
ORDER BY ordinal_position;
