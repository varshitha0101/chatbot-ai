# CBT Chatbot - Deployment Guide

A comprehensive guide to deploy the CBT Chatbot to production.

## Table of Contents

1. [Quick Start with Docker](#quick-start-with-docker)
2. [Prerequisites](#prerequisites)
3. [Configuration](#configuration)
4. [Deployment Options](#deployment-options)
5. [Production Checklist](#production-checklist)
6. [Troubleshooting](#troubleshooting)
7. [Monitoring & Maintenance](#monitoring--maintenance)

---

## Quick Start with Docker

### Using Docker Compose (Recommended)

```bash
# 1. Clone or navigate to the project
cd chatbot-ai

# 2. Copy and configure environment
cp .env.example .env
# Edit .env with your production values (SECRET_KEY, GEMINI_API_KEY, etc.)
nano .env

# 3. Build and start services
docker-compose up -d

# 4. Check health
docker-compose logs -f backend
curl http://localhost/health
```

**Services Started:**
- Backend API: `http://localhost:5000`
- Frontend UI: `http://localhost:80`
- Database: SQLite (or PostgreSQL if configured)

### Stopping Services

```bash
docker-compose down
```

---

## Prerequisites

### System Requirements
- **CPU:** 2+ cores
- **RAM:** 2GB minimum (4GB recommended)
- **Disk:** 10GB minimum
- **OS:** Linux (Ubuntu 20.04+), macOS, or Windows with Docker Desktop

### Required Software
- **Docker:** 20.10+
- **Docker Compose:** 1.29+
- **Git:** Latest version

### Accounts & API Keys
- **Google Gemini API Key** (free): Get it from https://aistudio.google.com/app/apikey
- **Domain & SSL Certificate** (for production): Let's Encrypt or commercial provider

### Installation

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install docker.io docker-compose git

# Start Docker
sudo systemctl start docker
sudo usermod -aG docker $USER

# macOS
brew install docker docker-compose git
# Start Docker Desktop from Applications
```

---

## Configuration

### 1. Environment Variables

Edit `.env` with your production settings:

```env
# CRITICAL - Change these for production
SECRET_KEY=generate-a-random-secure-key-here
JWT_SECRET_KEY=generate-another-random-key-here

# API Configuration
API_BASE_URL=https://your-domain.com
FRONTEND_URL=https://your-domain.com

# Google Gemini AI
GEMINI_API_KEY=your-gemini-api-key

# Database (SQLite for light load, PostgreSQL for heavy)
DATABASE_TYPE=sqlite
DATABASE_URL=sqlite:///chatbot.db

# Security
CORS_ORIGINS=https://your-domain.com,https://www.your-domain.com
RATE_LIMIT_ENABLED=true
```

### 2. Generate Secure Keys

```bash
# Generate SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate JWT_SECRET_KEY
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. SSL Certificates (HTTPS)

For Let's Encrypt (automated):

```bash
mkdir -p ssl

# Using Certbot
sudo apt-get install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d your-domain.com

# Copy certificates to ssl/ directory
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem
sudo chown $USER:$USER ssl/*
```

For self-signed (testing only):

```bash
mkdir -p ssl
openssl req -x509 -newkey rsa:4096 -nodes \
  -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

---

## Deployment Options

### Option 1: Docker Compose (Single Server)

Best for: Small-to-medium deployments, testing

```bash
docker-compose up -d
```

### Option 2: Docker with Kubernetes (Scalable)

Best for: High-traffic, multi-server deployments

```bash
# Install kubectl and deploy
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Option 3: Manual Deployment (Advanced)

Best for: Custom configurations, existing infrastructure

#### 3.1 Python Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

#### 3.2 Run with Gunicorn

```bash
gunicorn -c gunicorn_config.py wsgi:app
```

#### 3.3 Reverse Proxy with Nginx

```bash
sudo systemctl start nginx
# Nginx reads from nginx.conf
```

#### 3.4 Process Manager (Systemd)

```bash
sudo nano /etc/systemd/system/cbt-chatbot.service
```

```ini
[Unit]
Description=CBT Chatbot API
After=network.target

[Service]
Type=notify
User=appuser
WorkingDirectory=/opt/cbt-chatbot
Environment="PATH=/opt/cbt-chatbot/venv/bin"
ExecStart=/opt/cbt-chatbot/venv/bin/gunicorn -c gunicorn_config.py wsgi:app
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable cbt-chatbot
sudo systemctl start cbt-chatbot
```

---

## Production Checklist

Before going live, verify:

- [ ] **Security**
  - [ ] SECRET_KEY changed from default
  - [ ] JWT_SECRET_KEY changed from default
  - [ ] .env file NOT committed to git
  - [ ] CORS_ORIGINS restricted to your domain
  - [ ] HTTPS enabled with valid certificate
  - [ ] Rate limiting enabled

- [ ] **Database**
  - [ ] Backup strategy configured
  - [ ] Database size monitored
  - [ ] Connection limits set
  - [ ] (Recommended) Migrated to PostgreSQL

- [ ] **Performance**
  - [ ] Gunicorn workers set correctly (2 × CPU cores + 1)
  - [ ] Nginx caching enabled
  - [ ] Gzip compression enabled
  - [ ] Load testing completed (e.g., with Apache Bench)

- [ ] **Monitoring**
  - [ ] Logging configured and verified
  - [ ] Health check endpoint accessible
  - [ ] Error alerts set up
  - [ ] Uptime monitoring enabled

- [ ] **Maintenance**
  - [ ] Backup schedule configured
  - [ ] Log rotation enabled
  - [ ] SSL certificate renewal automated
  - [ ] Docker image updates tested

---

## Troubleshooting

### Container won't start

```bash
# Check logs
docker-compose logs backend

# Common issues:
# 1. Port already in use
sudo lsof -i :5000

# 2. Environment variables missing
cat .env | grep SECRET_KEY

# 3. Permission denied
docker-compose exec backend ls -la /var/log/chatbot
```

### CORS errors in frontend

**Error:** `Origin http://localhost:8080 is not allowed by Access-Control-Allow-Origin`

**Solution:**
```env
# Add to .env
CORS_ORIGINS=http://localhost:8080,http://localhost:3000
```

Then restart:
```bash
docker-compose down
docker-compose up -d
```

### Database locked (SQLite)

**Error:** `database is locked`

**Solution:** Migrate to PostgreSQL or increase SQLite timeouts

```python
# In database.py
conn = sqlite3.connect('chatbot.db', timeout=10.0)
```

### Out of memory errors

**Solution:** Increase allocated memory or reduce worker count

```bash
# Increase Docker memory limit
docker-compose down
# Edit docker-compose.yml: add "mem_limit: 4g" for backend
docker-compose up -d
```

### Certificate validation errors

```bash
# Check certificate expiry
openssl x509 -in ssl/cert.pem -noout -dates

# Renew with Let's Encrypt
certbot renew --force-renewal
```

---

## Monitoring & Maintenance

### Health Check

```bash
curl https://your-domain.com/health
```

Expected response:
```json
{
  "message": "CBT Chatbot API is running",
  "ai_powered": true,
  "ai_status": "enabled"
}
```

### View Logs

```bash
# Backend logs
docker-compose logs -f --tail=50 backend

# Nginx logs
docker-compose logs -f nginx

# All services
docker-compose logs -f
```

### Backup Database

```bash
# SQLite
docker-compose exec backend cp /app/data/chatbot.db /backup/chatbot.db

# PostgreSQL
docker-compose exec postgres pg_dump -U chatbot chatbot > backup.sql
```

### Update Application

```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose up -d --build
```

### Monitor Performance

```bash
# CPU and memory usage
docker stats

# Response times (from logs)
docker-compose logs backend | grep "rt="
```

### Scale Backend (with load balancer)

```yaml
# docker-compose.yml
services:
  backend:
    deploy:
      replicas: 3
```

---

## Support & Resources

- **Documentation:** See README.md
- **Issues:** Create GitHub issue with logs
- **API Docs:** Available at `/docs` (if Swagger enabled)
- **Google Generative AI:** https://ai.google.dev
- **Docker Docs:** https://docs.docker.com/
- **Nginx Docs:** https://nginx.org/en/docs/

---

## Security Best Practices

1. **Secrets Management**
   - Store secrets in environment variables, not code
   - Use secrets management tool (HashiCorp Vault, AWS Secrets Manager)
   - Rotate keys regularly

2. **Network Security**
   - Enable HTTPS/TLS
   - Use firewall rules
   - Restrict SSH/admin access
   - Enable fail2ban for brute-force protection

3. **Application Security**
   - Keep dependencies updated
   - Enable input validation
   - Use parameterized queries (already done)
   - Enable CORS restrictions
   - Regular security audits

4. **Operational Security**
   - Regular backups (daily)
   - Monitor error logs for attacks
   - Set up alerts for unusual activity
   - Document all deployments
   - Use GitOps for version control

---

**Last Updated:** 2026-03-27
**Version:** 1.0
