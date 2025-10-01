-- Migration 005: Update CaseID from CC format to numeric format based on report data
-- Backup old CaseID values before updating

-- Step 1: Backup current CaseID values (in case we need to rollback)
CREATE TABLE IF NOT EXISTS criminal_cases_case_id_backup AS
SELECT id, case_number, case_id, created_at, NOW() as backup_at
FROM criminal_cases
WHERE case_id IS NOT NULL AND case_id != '';

-- Step 2: Update CaseID based on case_number mapping from report
UPDATE criminal_cases SET case_id = '6809044200' WHERE case_number = '1382/2568';
UPDATE criminal_cases SET case_id = '68082125779' WHERE case_number = '1369/2568';
UPDATE criminal_cases SET case_id = '68071518486' WHERE case_number = '1303/2568';
UPDATE criminal_cases SET case_id = '6808089508' WHERE case_number = '1302/2568';
UPDATE criminal_cases SET case_id = '6807021634' WHERE case_number = '1301/2568';
UPDATE criminal_cases SET case_id = '6804076987' WHERE case_number = '1275/2568';
UPDATE criminal_cases SET case_id = '68061214466' WHERE case_number = '1257/2568';
UPDATE criminal_cases SET case_id = '68051213421' WHERE case_number = '1179/2568';
UPDATE criminal_cases SET case_id = '68063036264' WHERE case_number = '1178/2568';
UPDATE criminal_cases SET case_id = '680601843' WHERE case_number = '1174/2568';
UPDATE criminal_cases SET case_id = '6807045314' WHERE case_number = '1131/2568';
UPDATE criminal_cases SET case_id = '68051719672' WHERE case_number = '1037/2568';
UPDATE criminal_cases SET case_id = '661017313' WHERE case_number = '1036/2568';
UPDATE criminal_cases SET case_id = '66102534' WHERE case_number = '1035/2568';
UPDATE criminal_cases SET case_id = '68012222274' WHERE case_number = '947/2568';
UPDATE criminal_cases SET case_id = '68033127891' WHERE case_number = '940/2568';
UPDATE criminal_cases SET case_id = '660815663' WHERE case_number = '814/2568';
UPDATE criminal_cases SET case_id = '661113453' WHERE case_number = '813/2568';
UPDATE criminal_cases SET case_id = '661015363' WHERE case_number = '781/2568';
UPDATE criminal_cases SET case_id = '660912229' WHERE case_number = '614/2568';
UPDATE criminal_cases SET case_id = '66082037' WHERE case_number = '613/2568';
UPDATE criminal_cases SET case_id = '67018193' WHERE case_number = '612/2568';
UPDATE criminal_cases SET case_id = '67011836' WHERE case_number = '609/2568';
UPDATE criminal_cases SET case_id = '66103795' WHERE case_number = '461/2568';
UPDATE criminal_cases SET case_id = '660816156' WHERE case_number = '460/2568';
UPDATE criminal_cases SET case_id = '66084483' WHERE case_number = '458/2568';
UPDATE criminal_cases SET case_id = '66106667' WHERE case_number = '457/2568';
UPDATE criminal_cases SET case_id = '67041739' WHERE case_number = '169/2567';
UPDATE criminal_cases SET case_id = '650818501' WHERE case_number = '177/2566';
UPDATE criminal_cases SET case_id = '651217027' WHERE case_number = '170/2566';
UPDATE criminal_cases SET case_id = '66041271' WHERE case_number = '151/2566';
UPDATE criminal_cases SET case_id = '660625312' WHERE case_number = '134/2566';
UPDATE criminal_cases SET case_id = 'w660218019' WHERE case_number = '129/2566';
UPDATE criminal_cases SET case_id = '660719608' WHERE case_number = '128/2566';
UPDATE criminal_cases SET case_id = '66037061' WHERE case_number = '125/2566';
UPDATE criminal_cases SET case_id = '660627901' WHERE case_number = '98/2566';

-- Step 3: Show comparison - Before vs After
SELECT
    cc.case_number,
    backup.case_id as old_case_id,
    cc.case_id as new_case_id,
    CASE
        WHEN backup.case_id = cc.case_id THEN 'NO CHANGE'
        WHEN backup.case_id IS NULL THEN 'NEWLY SET'
        ELSE 'UPDATED'
    END as status
FROM criminal_cases cc
LEFT JOIN criminal_cases_case_id_backup backup ON cc.id = backup.id
WHERE cc.case_number IN (
    '1382/2568', '1369/2568', '1303/2568', '1302/2568', '1301/2568',
    '1275/2568', '1257/2568', '1179/2568', '1178/2568', '1174/2568'
)
ORDER BY cc.case_number DESC;

-- Step 4: Summary statistics
SELECT
    'Total cases' as metric,
    COUNT(*) as count
FROM criminal_cases
UNION ALL
SELECT
    'Cases with CaseID',
    COUNT(*)
FROM criminal_cases
WHERE case_id IS NOT NULL AND case_id != ''
UNION ALL
SELECT
    'Cases updated',
    COUNT(*)
FROM criminal_cases cc
INNER JOIN criminal_cases_case_id_backup backup ON cc.id = backup.id
WHERE cc.case_id != backup.case_id;
