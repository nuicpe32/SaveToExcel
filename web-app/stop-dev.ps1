# Stop Development Environment

Write-Host ""
Write-Host "=====================================" -ForegroundColor Yellow
Write-Host "  Stopping Development Environment" -ForegroundColor Yellow
Write-Host "=====================================" -ForegroundColor Yellow
Write-Host ""

Set-Location -Path $PSScriptRoot

Write-Host "Stopping all Docker services..." -ForegroundColor Yellow
docker-compose stop

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ All services stopped" -ForegroundColor Green
} else {
    Write-Host "⚠️  Some services may still be running" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "To start development mode again, run:" -ForegroundColor Cyan
Write-Host "  .\start-dev.ps1" -ForegroundColor White
Write-Host ""

