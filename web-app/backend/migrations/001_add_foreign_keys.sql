-- Migration Script: Add Foreign Key Constraints
-- Created: 2025-10-01
-- Purpose: Add proper FK constraints to bank_accounts and suspects tables

-- Step 1: Add foreign key constraint to bank_accounts
-- Check if constraint already exists before adding
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_bank_accounts_criminal_case_id'
    ) THEN
        ALTER TABLE bank_accounts
        ADD CONSTRAINT fk_bank_accounts_criminal_case_id
        FOREIGN KEY (criminal_case_id)
        REFERENCES criminal_cases(id)
        ON DELETE CASCADE;

        RAISE NOTICE 'Added FK constraint to bank_accounts';
    ELSE
        RAISE NOTICE 'FK constraint already exists on bank_accounts';
    END IF;
END $$;

-- Step 2: Add foreign key constraint to suspects
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_constraint
        WHERE conname = 'fk_suspects_criminal_case_id'
    ) THEN
        ALTER TABLE suspects
        ADD CONSTRAINT fk_suspects_criminal_case_id
        FOREIGN KEY (criminal_case_id)
        REFERENCES criminal_cases(id)
        ON DELETE CASCADE;

        RAISE NOTICE 'Added FK constraint to suspects';
    ELSE
        RAISE NOTICE 'FK constraint already exists on suspects';
    END IF;
END $$;

-- Step 3: Create indexes for better performance
CREATE INDEX IF NOT EXISTS idx_bank_accounts_criminal_case_id_v2
ON bank_accounts(criminal_case_id)
WHERE criminal_case_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_suspects_criminal_case_id_v2
ON suspects(criminal_case_id)
WHERE criminal_case_id IS NOT NULL;

-- Verify constraints
SELECT 'Foreign Key Constraints After Migration:' as status;
SELECT conname, conrelid::regclass AS table_name, confrelid::regclass AS referenced_table
FROM pg_constraint
WHERE contype = 'f'
ORDER BY conname;
