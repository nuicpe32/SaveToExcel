#!/bin/bash

# Script to run migration 007: Remove bank address fields from bank_accounts
# Date: 2025-10-01

echo "=============================================="
echo "Migration 007: Remove Bank Address Fields"
echo "=============================================="
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker is running
if ! docker ps > /dev/null 2>&1; then
    echo -e "${RED}❌ Docker is not running. Please start Docker first.${NC}"
    exit 1
fi

# Check if postgres container is running
if ! docker ps | grep -q criminal-case-db; then
    echo -e "${RED}❌ PostgreSQL container is not running.${NC}"
    echo "Please start the containers with: docker-compose up -d"
    exit 1
fi

echo -e "${YELLOW}⚠️  WARNING: This migration will permanently delete the following columns:${NC}"
echo "   - bank_branch"
echo "   - bank_address"
echo "   - soi, moo, road"
echo "   - sub_district, district, province, postal_code"
echo ""
echo -e "${YELLOW}This action cannot be undone unless you have a backup!${NC}"
echo ""

# Prompt for confirmation
read -p "Do you want to continue? (yes/no): " confirm
if [ "$confirm" != "yes" ]; then
    echo "Migration cancelled."
    exit 0
fi

echo ""
echo "Creating backup of bank_accounts table..."

# Create backup
docker-compose exec -T postgres psql -U user -d criminal_case_db << EOF
-- Create backup table
DROP TABLE IF EXISTS bank_accounts_backup_$(date +%Y%m%d);
CREATE TABLE bank_accounts_backup_$(date +%Y%m%d) AS 
SELECT 
    id, 
    bank_branch, 
    bank_address, 
    soi, moo, road, 
    sub_district, district, province, postal_code
FROM bank_accounts;
EOF

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backup created successfully${NC}"
else
    echo -e "${RED}❌ Backup failed. Aborting migration.${NC}"
    exit 1
fi

echo ""
echo "Running migration script..."

# Run migration
docker-compose exec -T postgres psql -U user -d criminal_case_db < backend/migrations/007_remove_bank_address_fields.sql

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Migration completed successfully${NC}"
else
    echo -e "${RED}❌ Migration failed${NC}"
    exit 1
fi

echo ""
echo "Verifying migration..."

# Verify
docker-compose exec -T postgres psql -U user -d criminal_case_db -c "\d bank_accounts" | grep -E "bank_branch|bank_address|soi|moo|road|sub_district|district|province|postal_code"

if [ $? -eq 0 ]; then
    echo -e "${RED}⚠️  Warning: Some columns might still exist${NC}"
else
    echo -e "${GREEN}✅ All columns removed successfully${NC}"
fi

echo ""
echo "Restarting backend service..."
docker-compose restart backend

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Backend restarted${NC}"
else
    echo -e "${RED}❌ Backend restart failed${NC}"
fi

echo ""
echo "=============================================="
echo -e "${GREEN}Migration 007 completed!${NC}"
echo "=============================================="
echo ""
echo "Next steps:"
echo "1. Test the API: http://localhost:8000/docs"
echo "2. Test the Frontend: http://localhost:3001/bank-accounts"
echo "3. Verify that address fields are no longer visible"
echo ""
echo "Backup location: bank_accounts_backup_$(date +%Y%m%d)"
echo ""

