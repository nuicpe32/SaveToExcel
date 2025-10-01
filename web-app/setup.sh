#!/bin/bash

# Criminal Case Management System - Setup Script
# สคริปต์ช่วยติดตั้งและ setup ระบบแบบอัตโนมัติ

set -e

echo "================================================"
echo "🚀 Criminal Case Management System - Setup"
echo "================================================"
echo ""

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ️  $1${NC}"
}

check_command() {
    if command -v $1 &> /dev/null; then
        print_success "$1 is installed"
        return 0
    else
        print_error "$1 is NOT installed"
        return 1
    fi
}

# Check prerequisites
echo "📦 Checking prerequisites..."
echo ""

DOCKER_INSTALLED=0
NODE_INSTALLED=0
PYTHON_INSTALLED=0

if check_command docker; then
    DOCKER_INSTALLED=1
fi

if check_command docker-compose || check_command docker compose; then
    print_success "docker-compose is installed"
else
    print_error "docker-compose is NOT installed"
fi

if check_command node; then
    NODE_INSTALLED=1
    NODE_VERSION=$(node --version)
    print_info "Node version: $NODE_VERSION"
fi

if check_command python3; then
    PYTHON_INSTALLED=1
    PYTHON_VERSION=$(python3 --version)
    print_info "Python version: $PYTHON_VERSION"
fi

echo ""

# Ask user for setup method
echo "🎯 เลือกวิธีการติดตั้ง:"
echo "1) Docker (แนะนำ)"
echo "2) Development Mode (Local)"
echo ""
read -p "เลือก (1 หรือ 2): " SETUP_METHOD

if [ "$SETUP_METHOD" == "1" ]; then
    if [ $DOCKER_INSTALLED -eq 0 ]; then
        print_error "กรุณาติดตั้ง Docker Desktop ก่อน: https://www.docker.com/products/docker-desktop"
        exit 1
    fi

    echo ""
    echo "🐳 Setting up with Docker..."
    echo ""

    # Setup backend .env
    if [ ! -f backend/.env ]; then
        print_info "Creating backend/.env file..."
        cp backend/.env.example backend/.env
        print_success "Created backend/.env"
        print_info "⚠️  กรุณาแก้ไข backend/.env และเปลี่ยน SECRET_KEY"
    else
        print_info "backend/.env already exists"
    fi

    echo ""
    read -p "ต้องการรัน docker-compose up ตอนนี้เลยไหม? (y/n): " RUN_DOCKER

    if [ "$RUN_DOCKER" == "y" ] || [ "$RUN_DOCKER" == "Y" ]; then
        print_info "Building and starting containers..."
        docker-compose up -d --build

        echo ""
        print_success "Containers are starting..."
        echo ""
        print_info "ตรวจสอบสถานะ: docker-compose ps"
        print_info "ดู logs: docker-compose logs -f"
        echo ""
        print_info "📊 ระบบจะพร้อมใช้งานใน 10-20 วินาที"
        echo ""
        print_success "Frontend: http://localhost:3000"
        print_success "Backend API: http://localhost:8000"
        print_success "API Docs: http://localhost:8000/docs"
        echo ""

        read -p "ต้องการสร้าง Admin user เลยไหม? (y/n): " CREATE_ADMIN

        if [ "$CREATE_ADMIN" == "y" ] || [ "$CREATE_ADMIN" == "Y" ]; then
            print_info "Waiting for backend to be ready..."
            sleep 10
            docker-compose exec backend python create_admin.py
            print_success "Admin user created!"
            print_info "Username: admin"
            print_info "Password: admin123"
        fi
    fi

elif [ "$SETUP_METHOD" == "2" ]; then
    if [ $NODE_INSTALLED -eq 0 ] || [ $PYTHON_INSTALLED -eq 0 ]; then
        print_error "กรุณาติดตั้ง Node.js และ Python 3 ก่อน"
        exit 1
    fi

    echo ""
    echo "💻 Setting up Development Environment..."
    echo ""

    # Backend setup
    echo "📦 Setting up Backend..."
    cd backend

    if [ ! -d "venv" ]; then
        print_info "Creating Python virtual environment..."
        python3 -m venv venv
        print_success "Virtual environment created"
    fi

    print_info "Activating virtual environment..."
    source venv/bin/activate || . venv/Scripts/activate

    print_info "Installing Python dependencies..."
    pip install -r requirements.txt

    if [ ! -f .env ]; then
        print_info "Creating .env file..."
        cp .env.example .env
        print_success "Created .env"
        print_info "⚠️  กรุณาแก้ไข .env และตั้งค่า DATABASE_URL, SECRET_KEY"
    fi

    cd ..

    # Frontend setup
    echo ""
    echo "📦 Setting up Frontend..."
    cd frontend

    if [ ! -d "node_modules" ]; then
        print_info "Installing Node dependencies..."
        npm install
        print_success "Node dependencies installed"
    else
        print_info "node_modules already exists"
    fi

    cd ..

    echo ""
    print_success "Development environment setup complete!"
    echo ""
    print_info "ขั้นตอนถัดไป:"
    echo "1. แก้ไข backend/.env"
    echo "2. เริ่ม PostgreSQL และ Redis (หรือใช้ Docker: docker-compose up -d postgres redis)"
    echo "3. รัน backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
    echo "4. รัน frontend (terminal ใหม่): cd frontend && npm run dev"
    echo ""

else
    print_error "Invalid choice"
    exit 1
fi

echo ""
echo "================================================"
print_success "Setup completed!"
echo "================================================"
echo ""
print_info "ดูคู่มือเพิ่มเติม: QUICK_START_GUIDE.md"
echo ""