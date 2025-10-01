# ==========================================
# Development Environment Startup Script
# สำหรับการพัฒนา Frontend + Backend
# ==========================================

Write-Host ""
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host "  Criminal Case Management - Dev Mode" -ForegroundColor Cyan
Write-Host "=============================================" -ForegroundColor Cyan
Write-Host ""

Set-Location -Path $PSScriptRoot

# ตรวจสอบว่า Docker รันอยู่หรือไม่
Write-Host "[0/5] Checking Docker..." -ForegroundColor Yellow
$dockerRunning = docker info 2>&1 | Out-Null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Docker is not running!" -ForegroundColor Red
    Write-Host "Please start Docker Desktop and try again." -ForegroundColor Yellow
    exit 1
}
Write-Host "✅ Docker is running" -ForegroundColor Green
Write-Host ""

# 1. หยุด Production containers (ถ้ามี)
Write-Host "[1/5] Stopping Production containers..." -ForegroundColor Yellow
docker-compose down 2>&1 | Out-Null
Write-Host "✅ Production containers stopped" -ForegroundColor Green
Write-Host ""

# 2. Start Backend Services (Docker) - Development Mode
Write-Host "[2/5] Starting Backend Services (Dev Mode)..." -ForegroundColor Yellow
Write-Host "      - PostgreSQL" -ForegroundColor Gray
Write-Host "      - Redis" -ForegroundColor Gray
Write-Host "      - Backend API (Hot Reload)" -ForegroundColor Gray
Write-Host ""

docker-compose -f docker-compose.dev.yml up -d

if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Failed to start backend services!" -ForegroundColor Red
    exit 1
}

Write-Host "✅ Backend services started" -ForegroundColor Green
Write-Host ""

# 3. Wait for services to be ready
Write-Host "[3/5] Waiting for services to be ready..." -ForegroundColor Yellow
$maxRetries = 30
$retryCount = 0
$backendReady = $false

while (-not $backendReady -and $retryCount -lt $maxRetries) {
    Start-Sleep -Seconds 2
    $retryCount++
    
    try {
        $response = Invoke-RestMethod -Uri "http://localhost:8000/health" -Method Get -TimeoutSec 3 -ErrorAction SilentlyContinue
        if ($response.status -eq "healthy") {
            $backendReady = $true
            Write-Host "✅ Backend API is healthy!" -ForegroundColor Green
        }
    } catch {
        Write-Host "." -NoNewline -ForegroundColor Gray
    }
}

if (-not $backendReady) {
    Write-Host ""
    Write-Host "⚠️  Backend is taking longer than expected to start" -ForegroundColor Yellow
    Write-Host "    But continuing anyway..." -ForegroundColor Gray
}

Write-Host ""

# 4. Setup Frontend Dependencies
Write-Host "[4/5] Setting up Frontend..." -ForegroundColor Yellow
Set-Location -Path "$PSScriptRoot\frontend"

if (-Not (Test-Path "node_modules")) {
    Write-Host "Installing dependencies (first time setup)..." -ForegroundColor Yellow
    npm install
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Failed to install dependencies!" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "✅ Dependencies installed" -ForegroundColor Green
} else {
    Write-Host "✅ Dependencies already installed" -ForegroundColor Green
}

Write-Host ""

# 5. Start Frontend Dev Server
Write-Host "[5/5] Starting Frontend Dev Server..." -ForegroundColor Yellow
Write-Host ""

Write-Host "=============================================" -ForegroundColor Green
Write-Host "  🎉 Development Mode Ready!" -ForegroundColor Green
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Services:" -ForegroundColor Cyan
Write-Host "  Frontend (Vite):  http://localhost:5173" -ForegroundColor White
Write-Host "  Backend API:      http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs:         http://localhost:8000/docs" -ForegroundColor White
Write-Host "  Database:         localhost:5432" -ForegroundColor White
Write-Host "  Redis:            localhost:6379" -ForegroundColor White
Write-Host ""
Write-Host "Features:" -ForegroundColor Cyan
Write-Host "  ✅ Hot Reload (Frontend & Backend)" -ForegroundColor Green
Write-Host "  ✅ Auto-refresh on file changes" -ForegroundColor Green
Write-Host "  ✅ Full development environment" -ForegroundColor Green
Write-Host ""
Write-Host "Default Login:" -ForegroundColor Cyan
Write-Host "  Username: admin" -ForegroundColor White
Write-Host "  Password: admin123" -ForegroundColor White
Write-Host ""
Write-Host "=============================================" -ForegroundColor Green
Write-Host ""
Write-Host "กด Ctrl+C เพื่อหยุด Frontend Dev Server" -ForegroundColor Gray
Write-Host "(Backend services จะยังรันอยู่ใน Docker)" -ForegroundColor Gray
Write-Host ""

# Start Vite Dev Server (รันในโหมด foreground)
npm run dev

# Cleanup on exit
Write-Host ""
Write-Host "Stopping Frontend Dev Server..." -ForegroundColor Yellow
Write-Host ""
Write-Host "Backend services ยังรันอยู่ใน Docker" -ForegroundColor Gray
Write-Host "To stop backend: docker-compose -f docker-compose.dev.yml stop" -ForegroundColor Cyan
Write-Host "To stop all: docker-compose -f docker-compose.dev.yml down" -ForegroundColor Cyan
Write-Host ""


