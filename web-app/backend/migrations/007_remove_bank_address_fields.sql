-- Migration 007: Remove address and branch fields from bank_accounts table
-- Reason: Use address from banks master table instead (headquarters only)
-- Date: 2025-10-01

-- Description:
-- This migration removes redundant address fields and bank_branch from bank_accounts
-- All address information will be retrieved from the banks table via bank_id FK
-- In practice, documents are sent to headquarters only, not to branches

BEGIN;

-- Remove address-related columns from bank_accounts
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS bank_branch;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS bank_address;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS soi;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS moo;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS road;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS sub_district;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS district;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS province;
ALTER TABLE bank_accounts DROP COLUMN IF EXISTS postal_code;

-- Note: bank_id FK is kept to reference banks table
-- Note: bank_name is kept for display purposes and convenience

COMMIT;

-- Rollback script (if needed):
-- ALTER TABLE bank_accounts ADD COLUMN bank_branch VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN bank_address TEXT;
-- ALTER TABLE bank_accounts ADD COLUMN soi VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN moo VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN road VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN sub_district VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN district VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN province VARCHAR;
-- ALTER TABLE bank_accounts ADD COLUMN postal_code VARCHAR;

