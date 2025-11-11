# Deployment Guide

## Prerequisites

- Ubuntu Server (20.04 or later)
- Docker and Docker Compose installed
- Domain name (optional, for reverse proxy)
- Minimum 1 vCPU / 1 GB RAM

## Initial Server Setup

### 1. Update System

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Install Docker

```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

### 3. Install Docker Compose

```bash
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

## Deploy Utility Service

### 1. Clone Repository

```bash
cd /opt
sudo git clone <your-repo-url> utility-service
cd utility-service
```

### 2. Configure Environment

```bash
sudo cp .env.example .env
sudo nano .env
```

Set your configuration:
```
PORT=8080
API_KEY=your-production-api-key-here
LOG_LEVEL=info
TEMP_PATH=/tmp/pdf_service
```

### 3. Build and Start Service

```bash
sudo docker-compose up -d --build
```

### 4. Verify Service

```bash
# Check if container is running
sudo docker-compose ps

# View logs
sudo docker-compose logs -f

# Test health endpoint
curl http://localhost:8080/health
```

## Optional: Reverse Proxy with Nginx

### 1. Install Nginx

```bash
sudo apt install nginx -y
```

### 2. Create Nginx Configuration

```bash
sudo nano /etc/nginx/sites-available/utility-service
```

Add configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    client_max_body_size 10M;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 3. Enable Site

```bash
sudo ln -s /etc/nginx/sites-available/utility-service /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 4. Optional: Add SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx -y
sudo certbot --nginx -d your-domain.com
```

## Monitoring

### View Logs

```bash
# Real-time logs
sudo docker-compose logs -f utility-service

# Last 100 lines
sudo docker-compose logs --tail=100 utility-service
```

### Check Resource Usage

```bash
sudo docker stats
```

### Restart Service

```bash
sudo docker-compose restart
```

## Updates

### Update Service

```bash
cd /opt/utility-service
sudo git pull
sudo docker-compose up -d --build
```

### Rollback

```bash
sudo docker-compose down
sudo git checkout <previous-commit>
sudo docker-compose up -d --build
```

## Firewall Configuration

### Allow HTTP/HTTPS (if using Nginx)

```bash
sudo ufw allow 'Nginx Full'
```

### Allow Direct Access (if not using Nginx)

```bash
sudo ufw allow 8080/tcp
```

## Backup

### Backup Configuration

```bash
sudo cp .env /backup/.env.$(date +%Y%m%d)
```

## Troubleshooting

### Container Won't Start

```bash
# Check logs
sudo docker-compose logs

# Check if port is in use
sudo netstat -tuln | grep 8080

# Rebuild from scratch
sudo docker-compose down
sudo docker-compose up -d --build --force-recreate
```

### Permission Issues

```bash
# Fix temp directory permissions
sudo mkdir -p /tmp/pdf_service
sudo chmod 777 /tmp/pdf_service
```

### Memory Issues

```bash
# Add memory limit to docker-compose.yml
services:
  utility-service:
    mem_limit: 512m
```

## Security Hardening

### 1. Use Strong API Key

Generate a strong API key:
```bash
openssl rand -hex 32
```

### 2. Run as Non-Root User

Add to Dockerfile:
```dockerfile
RUN adduser --disabled-password --gecos '' appuser
USER appuser
```

### 3. Limit Container Resources

Add to docker-compose.yml:
```yaml
deploy:
  resources:
    limits:
      cpus: '1.0'
      memory: 1G
```

### 4. Enable Firewall

```bash
sudo ufw enable
sudo ufw status
```

## Production Checklist

- [ ] Strong API key configured
- [ ] Firewall enabled and configured
- [ ] Logs monitoring setup
- [ ] Backup strategy in place
- [ ] SSL certificate installed (if using domain)
- [ ] Resource limits configured
- [ ] Automatic restart enabled
- [ ] Health checks working
- [ ] Documentation updated

## Monitoring Services (Optional)

### Setup Uptime Monitor

Use services like:
- UptimeRobot
- Pingdom
- StatusCake

Monitor: `https://your-domain.com/health`

### Log Aggregation

Consider shipping logs to:
- Papertrail
- Loggly
- ELK Stack

## Support

For issues, check:
1. Service logs: `sudo docker-compose logs`
2. Container status: `sudo docker ps`
3. System resources: `htop` or `top`
4. Disk space: `df -h`

