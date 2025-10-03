# Docker Compose Usage Guide

## 🚀 Single Docker Compose File

ตอนนี้ใช้ **docker-compose.yml ไฟล์เดียว** รองรับทั้ง Development และ Production

## 📋 การใช้งาน

### 🛠️ Development Mode (Default)
```bash
# Start all services
docker-compose up -d

# Access URLs:
# Frontend: http://localhost:3001
# Backend API: http://localhost:8000
# Database: localhost:5432
# Redis: localhost:6379
```

### 🔧 Production Mode
```bash
# Set environment variables
export ENVIRONMENT=production
export SECRET_KEY=your-production-secret-key

# Start services
docker-compose up -d
```

### 🛠️ With Database Tools
```bash
# Start with pgAdmin and Adminer
docker-compose --profile tools up -d

# Access URLs:
# pgAdmin: http://localhost:5050
# Adminer: http://localhost:8080
```

## 📁 Services

- **frontend**: React development server with hot reload
- **backend**: FastAPI with auto-reload
- **postgres**: PostgreSQL database
- **redis**: Redis cache
- **pgadmin**: Database admin tool (optional)
- **adminer**: Database admin tool (optional)

## 🔄 Commands

```bash
# Start services
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and start
docker-compose up -d --build

# Stop and remove volumes (⚠️ DATA LOSS)
docker-compose down -v
```

## ⚠️ Important Notes

1. **Data Persistence**: Database data is stored in Docker volume `criminal-case-postgres`
2. **Hot Reload**: Both frontend and backend support hot reload for development
3. **Ports**: 
   - Frontend: 3001
   - Backend: 8000
   - Database: 5432
   - Redis: 6379
   - pgAdmin: 5050
   - Adminer: 8080

## 🔧 Troubleshooting

### Reset Everything
```bash
docker-compose down -v
docker-compose up -d --build
```

### Check Container Status
```bash
docker-compose ps
```

### View Logs
```bash
docker-compose logs frontend
docker-compose logs backend
```
