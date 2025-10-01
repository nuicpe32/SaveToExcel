#!/bin/bash

# Development Helper Script
# ใช้สำหรับจัดการ Development Environment ง่ายๆ

set -e

COMPOSE_FILE="docker-compose.dev.yml"
COMPOSE_CMD="docker-compose -f $COMPOSE_FILE"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_header() {
    echo -e "${BLUE}================================================${NC}"
    echo -e "${BLUE}  Criminal Case Management - Dev Helper${NC}"
    echo -e "${BLUE}================================================${NC}"
    echo
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

case "$1" in
    start)
        print_header
        print_info "Starting development environment..."

        # Create network if not exists
        docker network create criminal-case-network 2>/dev/null || true

        $COMPOSE_CMD up -d

        print_success "Development environment started!"
        print_info "Frontend: http://localhost:3001"
        print_info "Backend API: http://localhost:8000"
        print_info "Database: localhost:5432"
        echo
        print_info "Run './dev.sh logs' to view logs"
        ;;

    stop)
        print_header
        print_info "Stopping development environment..."
        $COMPOSE_CMD stop
        print_success "Development environment stopped!"
        print_info "Run './dev.sh start' to start again"
        ;;

    restart)
        print_header
        if [ -z "$2" ]; then
            print_info "Restarting all services..."
            $COMPOSE_CMD restart
            print_success "All services restarted!"
        else
            print_info "Restarting $2..."
            $COMPOSE_CMD restart $2
            print_success "$2 restarted!"
        fi
        ;;

    logs)
        if [ -z "$2" ]; then
            print_info "Showing all logs (Ctrl+C to exit)..."
            $COMPOSE_CMD logs -f
        else
            print_info "Showing logs for $2 (Ctrl+C to exit)..."
            $COMPOSE_CMD logs -f $2
        fi
        ;;

    ps|status)
        print_header
        $COMPOSE_CMD ps
        ;;

    build)
        print_header
        if [ -z "$2" ]; then
            print_info "Building all services..."
            $COMPOSE_CMD build
            print_success "All services built!"
        else
            print_info "Building $2..."
            $COMPOSE_CMD build $2
            print_success "$2 built!"
        fi
        ;;

    rebuild)
        print_header
        print_info "Rebuilding and restarting..."
        if [ -z "$2" ]; then
            $COMPOSE_CMD build
            $COMPOSE_CMD up -d
            print_success "All services rebuilt and restarted!"
        else
            $COMPOSE_CMD build $2
            $COMPOSE_CMD restart $2
            print_success "$2 rebuilt and restarted!"
        fi
        ;;

    clean)
        print_header
        print_warning "This will remove all containers (but keep volumes/data)"
        read -p "Are you sure? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            $COMPOSE_CMD down
            print_success "Containers removed! (Data preserved in volumes)"
            print_info "Run './dev.sh start' to start again"
        else
            print_info "Cancelled"
        fi
        ;;

    clean-all)
        print_header
        print_error "⚠️  WARNING: This will DELETE ALL DATA!"
        print_warning "All containers, volumes, and data will be removed"
        read -p "Are you ABSOLUTELY sure? (type 'yes'): " -r
        echo
        if [[ $REPLY == "yes" ]]; then
            $COMPOSE_CMD down -v
            print_success "Everything removed!"
            print_warning "All data has been deleted"
        else
            print_info "Cancelled"
        fi
        ;;

    backup)
        print_header
        BACKUP_FILE="backup_$(date +%Y%m%d_%H%M%S).sql"
        print_info "Backing up database to $BACKUP_FILE..."
        $COMPOSE_CMD exec -T postgres pg_dump -U user criminal_case_db > "$BACKUP_FILE"
        print_success "Database backed up to $BACKUP_FILE"
        print_info "File size: $(ls -lh $BACKUP_FILE | awk '{print $5}')"
        ;;

    restore)
        print_header
        if [ -z "$2" ]; then
            print_error "Please specify backup file"
            print_info "Usage: ./dev.sh restore <backup-file.sql>"
            exit 1
        fi

        if [ ! -f "$2" ]; then
            print_error "Backup file not found: $2"
            exit 1
        fi

        print_warning "This will restore database from $2"
        read -p "Continue? (y/N): " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            print_info "Restoring database..."
            cat "$2" | $COMPOSE_CMD exec -T postgres psql -U user -d criminal_case_db
            print_success "Database restored from $2"
        else
            print_info "Cancelled"
        fi
        ;;

    shell)
        print_header
        if [ -z "$2" ]; then
            print_error "Please specify service (backend, frontend, postgres)"
            exit 1
        fi
        print_info "Opening shell in $2..."
        $COMPOSE_CMD exec $2 sh
        ;;

    test)
        print_header
        print_info "Testing services..."
        echo

        # Test backend
        print_info "Testing Backend API..."
        if curl -f -s http://localhost:8000/api/v1/case-types > /dev/null 2>&1; then
            print_success "Backend API is working"
        else
            print_error "Backend API is not responding"
        fi

        # Test frontend
        print_info "Testing Frontend..."
        if curl -f -s http://localhost:3001 > /dev/null 2>&1; then
            print_success "Frontend is working"
        else
            print_error "Frontend is not responding"
        fi

        # Test database
        print_info "Testing Database..."
        if $COMPOSE_CMD exec -T postgres psql -U user -d criminal_case_db -c "SELECT 1;" > /dev/null 2>&1; then
            print_success "Database is working"
        else
            print_error "Database is not responding"
        fi

        echo
        print_success "Testing complete!"
        ;;

    help|*)
        print_header
        echo "Usage: ./dev.sh <command> [options]"
        echo
        echo "Commands:"
        echo "  ${GREEN}start${NC}              Start development environment"
        echo "  ${GREEN}stop${NC}               Stop development environment"
        echo "  ${GREEN}restart [service]${NC}  Restart all services or specific service"
        echo "  ${GREEN}logs [service]${NC}     Show logs (all or specific service)"
        echo "  ${GREEN}ps${NC}                 Show running containers"
        echo "  ${GREEN}build [service]${NC}    Build all services or specific service"
        echo "  ${GREEN}rebuild [service]${NC}  Rebuild and restart"
        echo "  ${GREEN}clean${NC}              Remove containers (keep data)"
        echo "  ${GREEN}clean-all${NC}          Remove everything (⚠️  deletes all data)"
        echo "  ${GREEN}backup${NC}             Backup database"
        echo "  ${GREEN}restore <file>${NC}     Restore database from backup"
        echo "  ${GREEN}shell <service>${NC}    Open shell in container"
        echo "  ${GREEN}test${NC}               Test all services"
        echo "  ${GREEN}help${NC}               Show this help"
        echo
        echo "Examples:"
        echo "  ./dev.sh start"
        echo "  ./dev.sh restart frontend"
        echo "  ./dev.sh logs backend"
        echo "  ./dev.sh backup"
        echo "  ./dev.sh restore backup_20250101_120000.sql"
        echo
        ;;
esac
