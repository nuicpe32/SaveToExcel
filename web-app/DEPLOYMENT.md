# คู่มือการ Deploy - ระบบจัดการคดีอาญา v3.0.0

## 🎯 ตัวเลือกการ Deploy

### 1. Docker Compose (แนะนำสำหรับ Development/Testing)
### 2. Cloud Platform (Production)
### 3. On-Premise Server (Production)

---

## 📦 1. Docker Compose Deployment

### ข้อกำหนด
- Docker 20.10+
- Docker Compose 2.0+
- RAM: 4GB+
- Disk: 20GB+

### ขั้นตอนการ Deploy

```bash
# 1. Clone repository
git clone <repository-url>
cd web-app

# 2. ตั้งค่า Environment
cd backend
cp .env.example .env
nano .env  # แก้ไข SECRET_KEY, Database credentials

# 3. Build & Run
cd ..
docker-compose up -d --build

# 4. ตรวจสอบสถานะ
docker-compose ps
docker-compose logs -f

# 5. เข้าถึงระบบ
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### การจัดการ Containers

```bash
# หยุดระบบ
docker-compose stop

# เริ่มระบบ
docker-compose start

# ลบ containers (ข้อมูลยังอยู่)
docker-compose down

# ลบทุกอย่างรวม volumes
docker-compose down -v
```

---

## ☁️ 2. Cloud Platform Deployment

### 2.1 AWS Deployment

#### Architecture
```
Internet → ELB → ECS (Frontend + Backend) → RDS (PostgreSQL) + ElastiCache (Redis)
```

#### ขั้นตอน

**A. สร้าง RDS Database**
```bash
aws rds create-db-instance \
  --db-instance-identifier criminal-case-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password yourpassword \
  --allocated-storage 20
```

**B. สร้าง ElastiCache Redis**
```bash
aws elasticache create-cache-cluster \
  --cache-cluster-id criminal-case-redis \
  --cache-node-type cache.t3.micro \
  --engine redis \
  --num-cache-nodes 1
```

**C. Push Docker Images to ECR**
```bash
# Backend
cd backend
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
docker build -t criminal-case-backend .
docker tag criminal-case-backend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/criminal-case-backend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/criminal-case-backend:latest

# Frontend
cd ../frontend
docker build -t criminal-case-frontend .
docker tag criminal-case-frontend:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/criminal-case-frontend:latest
docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/criminal-case-frontend:latest
```

**D. Deploy to ECS**
- สร้าง ECS Cluster
- สร้าง Task Definitions
- สร้าง Services
- ตั้งค่า Load Balancer

### 2.2 Google Cloud Platform (GCP)

#### Architecture
```
Internet → Cloud Load Balancer → Cloud Run → Cloud SQL + Memorystore
```

#### ขั้นตอน

```bash
# 1. สร้าง Cloud SQL
gcloud sql instances create criminal-case-db \
  --database-version=POSTGRES_14 \
  --tier=db-f1-micro \
  --region=asia-southeast1

# 2. Deploy Backend to Cloud Run
cd backend
gcloud builds submit --tag gcr.io/PROJECT_ID/criminal-case-backend
gcloud run deploy criminal-case-backend \
  --image gcr.io/PROJECT_ID/criminal-case-backend \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated

# 3. Deploy Frontend
cd ../frontend
gcloud builds submit --tag gcr.io/PROJECT_ID/criminal-case-frontend
gcloud run deploy criminal-case-frontend \
  --image gcr.io/PROJECT_ID/criminal-case-frontend \
  --platform managed \
  --region asia-southeast1 \
  --allow-unauthenticated
```

### 2.3 Azure Deployment

```bash
# สร้าง Resource Group
az group create --name criminal-case-rg --location southeastasia

# สร้าง PostgreSQL
az postgres server create \
  --resource-group criminal-case-rg \
  --name criminal-case-db \
  --location southeastasia \
  --admin-user myadmin \
  --admin-password <password> \
  --sku-name B_Gen5_1

# Deploy to App Service
az webapp up \
  --name criminal-case-app \
  --resource-group criminal-case-rg \
  --runtime "PYTHON:3.11"
```

---

## 🏢 3. On-Premise Server Deployment

### ข้อกำหนด Server
- OS: Ubuntu 22.04 LTS
- RAM: 8GB+
- CPU: 4 cores+
- Disk: 100GB+
- Network: Static IP

### ขั้นตอนการติดตั้ง

#### 3.1 ติดตั้ง Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# ติดตั้ง Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# ติดตั้ง Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.23.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# ติดตั้ง Nginx
sudo apt install nginx -y
```

#### 3.2 ตั้งค่า Nginx Reverse Proxy

```bash
sudo nano /etc/nginx/sites-available/criminal-case
```

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/criminal-case /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

#### 3.3 ตั้งค่า SSL (Let's Encrypt)

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

#### 3.4 Deploy Application

```bash
# Clone project
cd /opt
sudo git clone <repository-url> criminal-case-app
cd criminal-case-app/web-app

# ตั้งค่า environment
cd backend
sudo cp .env.example .env
sudo nano .env  # แก้ไขค่าต่างๆ

# Run with Docker Compose
cd ..
sudo docker-compose up -d --build

# ตั้งค่า auto-start on boot
sudo nano /etc/systemd/system/criminal-case.service
```

```ini
[Unit]
Description=Criminal Case Management System
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/opt/criminal-case-app/web-app
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable criminal-case.service
sudo systemctl start criminal-case.service
```

---

## 📊 4. Database Migration

```bash
# สร้าง migration
docker-compose exec backend alembic revision --autogenerate -m "Description"

# รัน migration
docker-compose exec backend alembic upgrade head

# Rollback migration
docker-compose exec backend alembic downgrade -1
```

---

## 🔐 5. Security Checklist

- [ ] เปลี่ยน SECRET_KEY ใน production
- [ ] ตั้งค่า CORS_ORIGINS ให้ถูกต้อง
- [ ] ใช้ HTTPS (SSL/TLS)
- [ ] เปลี่ยน default database credentials
- [ ] ตั้งค่า Firewall (UFW)
- [ ] Enable rate limiting
- [ ] Setup backup strategy
- [ ] Enable logging & monitoring

```bash
# ตั้งค่า UFW Firewall
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
```

---

## 📈 6. Monitoring & Logging

### Logs

```bash
# Docker logs
docker-compose logs -f backend
docker-compose logs -f frontend

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Health Checks

```bash
# Backend health
curl http://localhost:8000/health

# Database connection
docker-compose exec postgres psql -U user -d criminal_case_db -c "SELECT version();"
```

---

## 💾 7. Backup Strategy

### Database Backup

```bash
# Manual backup
docker-compose exec postgres pg_dump -U user criminal_case_db > backup_$(date +%Y%m%d_%H%M%S).sql

# Automated backup (crontab)
0 2 * * * /opt/criminal-case-app/scripts/backup.sh
```

### Restore

```bash
docker-compose exec -T postgres psql -U user criminal_case_db < backup.sql
```

---

## 🔄 8. Update & Maintenance

```bash
# Pull latest code
cd /opt/criminal-case-app/web-app
git pull origin main

# Rebuild & restart
docker-compose down
docker-compose up -d --build

# Clean old images
docker system prune -a
```

---

## 📞 Support & Troubleshooting

### Common Issues

**1. Port already in use**
```bash
sudo lsof -i :8000
sudo kill -9 <PID>
```

**2. Database connection failed**
```bash
docker-compose logs postgres
docker-compose restart postgres
```

**3. Out of memory**
```bash
# เพิ่ม swap space
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📋 Deployment Checklist

- [ ] ติดตั้ง dependencies
- [ ] Clone repository
- [ ] ตั้งค่า environment variables
- [ ] Setup database
- [ ] Build Docker images
- [ ] Run containers
- [ ] Setup Nginx reverse proxy
- [ ] Setup SSL certificate
- [ ] Run database migrations
- [ ] Create admin user
- [ ] Test all endpoints
- [ ] Setup monitoring
- [ ] Setup backup
- [ ] Document credentials