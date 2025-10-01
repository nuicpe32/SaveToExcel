# Development Environment Startup Script
# สำหรับการพัฒนา Frontend + Backend

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "  Development Environment Startup" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

# 1. Start Backend Services (Docker)
Write-Host "[1/4] Starting Backend Services (Docker)..." -ForegroundColor Yellow
Write-Host "      - PostgreSQL" -ForegroundColor Gray
Write-Host "      - Redis" -ForegroundColor Gray
Write-Host "      - Backend API" -ForegroundColor Gray
Write-Host ""

Set-Location -Path $PSScriptRoot
docker-compose up -d postgres redis backend

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start backend services!" -ForegroundColor Red
    exit 1
}

Write-Host "Backend services started" -ForegroundColor Green
Write-Host ""

# 2. Wait for services to be ready
Write-Host "[2/4] Waiting for services to be ready..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Check Backend Health
try {
    $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 5
    Write-Host "Backend API is healthy: $($response.status)" -ForegroundColor Green
} catch {
    Write-Host "Backend API not responding yet (may need more time)" -ForegroundColor Yellow
}

Write-Host ""

# 3. Check if frontend dependencies are installed
Write-Host "[3/4] Checking Frontend dependencies..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\frontend"

if (-Not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies (first time)..." -ForegroundColor Yellow
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "Failed to install dependencies!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "Dependencies already installed" -ForegroundColor Green
}

Write-Host ""

# 4. Start Frontend Dev Server
Write-Host "[4/4] Starting Frontend Dev Server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "=====================================" -ForegroundColor Green
Write-Host "  Development Mode Ready!" -ForegroundColor Green
Write-Host "=====================================" -ForegroundColor Green
Write-Host ""
Write-Host "Frontend:  http://localhost:5173" -ForegroundColor Cyan
Write-Host "Backend:   http://localhost:8000" -ForegroundColor Cyan
Write-Host "API Docs:  http://localhost:8000/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Hot Reload is enabled - แก้ไขโค้ดแล้วเห็นผลทันที!" -ForegroundColor Green
Write-Host ""
Write-Host "กด Ctrl+C เพื่อหยุด Frontend Dev Server" -ForegroundColor Gray
Write-Host ""

# Start Vite Dev Server
npm run dev

# Cleanup on exit
Write-Host ""
Write-Host "Stopping Frontend Dev Server..." -ForegroundColor Yellow
Write-Host "Backend services are still running in Docker." -ForegroundColor Gray
Write-Host "To stop backend: docker-compose stop" -ForegroundColor Gray
