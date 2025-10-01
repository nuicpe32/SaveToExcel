-- Migration: Add court_name field to criminal_cases table
-- Date: 2025-10-01

ALTER TABLE criminal_cases ADD COLUMN IF NOT EXISTS court_name VARCHAR(255);

-- Create index for faster search
CREATE INDEX IF NOT EXISTS idx_criminal_cases_court_name ON criminal_cases(court_name);

-- Add comment
COMMENT ON COLUMN criminal_cases.court_name IS 'เขตอำนาจศาล - ชื่อศาลที่มีเขตอำนาจคดี';
