# ==========================================
# Stop Development Environment
# ==========================================

Write-Host ""
Write-Host "=============================================" -ForegroundColor Yellow
Write-Host "  Stopping Development Environment" -ForegroundColor Yellow
Write-Host "=============================================" -ForegroundColor Yellow
Write-Host ""

Set-Location -Path $PSScriptRoot

Write-Host "Stopping all development Docker services..." -ForegroundColor Yellow
docker-compose -f docker-compose.dev.yml stop

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All development services stopped" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some services may still be running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Options:" -ForegroundColor Cyan
Write-Host "  Start dev mode again:  .\start-dev-improved.ps1" -ForegroundColor White
Write-Host "  Remove containers:     docker-compose -f docker-compose.dev.yml down" -ForegroundColor White
Write-Host "  View containers:       docker-compose -f docker-compose.dev.yml ps" -ForegroundColor White
Write-Host ""


