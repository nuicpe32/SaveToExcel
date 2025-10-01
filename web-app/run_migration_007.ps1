# PowerShell script to run migration 007: Remove bank address fields from bank_accounts
# Date: 2025-10-01

Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Migration 007: Remove Bank Address Fields" -ForegroundColor Cyan
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""

# Check if docker is running
try {
    docker ps | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker first." -ForegroundColor Red
    exit 1
}

# Check if postgres container is running
$postgresRunning = docker ps | Select-String "criminal-case-db"
if (-not $postgresRunning) {
    Write-Host "❌ PostgreSQL container is not running." -ForegroundColor Red
    Write-Host "Please start the containers with: docker-compose up -d"
    exit 1
}

Write-Host "⚠️  WARNING: This migration will permanently delete the following columns:" -ForegroundColor Yellow
Write-Host "   - bank_branch"
Write-Host "   - bank_address"
Write-Host "   - soi, moo, road"
Write-Host "   - sub_district, district, province, postal_code"
Write-Host ""
Write-Host "This action cannot be undone unless you have a backup!" -ForegroundColor Yellow
Write-Host ""

# Prompt for confirmation
$confirm = Read-Host "Do you want to continue? (yes/no)"
if ($confirm -ne "yes") {
    Write-Host "Migration cancelled."
    exit 0
}

Write-Host ""
Write-Host "Creating backup of bank_accounts table..." -ForegroundColor Yellow

# Create backup
$backupDate = Get-Date -Format "yyyyMMdd"
$backupSQL = @"
DROP TABLE IF EXISTS bank_accounts_backup_$backupDate;
CREATE TABLE bank_accounts_backup_$backupDate AS 
SELECT 
    id, 
    bank_branch, 
    bank_address, 
    soi, moo, road, 
    sub_district, district, province, postal_code
FROM bank_accounts;
"@

$backupSQL | docker-compose exec -T postgres psql -U user -d criminal_case_db

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backup created successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Backup failed. Aborting migration." -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Running migration script..." -ForegroundColor Yellow

# Run migration
Get-Content backend/migrations/007_remove_bank_address_fields.sql | docker-compose exec -T postgres psql -U user -d criminal_case_db

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Migration completed successfully" -ForegroundColor Green
} else {
    Write-Host "❌ Migration failed" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Verifying migration..." -ForegroundColor Yellow

# Verify
$verifyResult = docker-compose exec -T postgres psql -U user -d criminal_case_db -c "\d bank_accounts"
if ($verifyResult | Select-String -Pattern "bank_branch|bank_address|soi|moo|road|sub_district|district|province|postal_code") {
    Write-Host "⚠️  Warning: Some columns might still exist" -ForegroundColor Yellow
} else {
    Write-Host "✅ All columns removed successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "Restarting backend service..." -ForegroundColor Yellow
docker-compose restart backend

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Backend restarted" -ForegroundColor Green
} else {
    Write-Host "❌ Backend restart failed" -ForegroundColor Red
}

Write-Host ""
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host "Migration 007 completed!" -ForegroundColor Green
Write-Host "==============================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:"
Write-Host "1. Test the API: http://localhost:8000/docs"
Write-Host "2. Test the Frontend: http://localhost:3001/bank-accounts"
Write-Host "3. Verify that address fields are no longer visible"
Write-Host ""
Write-Host "Backup location: bank_accounts_backup_$backupDate" -ForegroundColor Cyan
Write-Host ""

