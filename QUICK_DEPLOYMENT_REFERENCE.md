# Quick Deployment Reference

Quick commands and configurations for deploying CBT Chatbot.

## 🚀 Quick Start (Docker)

```bash
# 1. Setup environment
./deploy.sh  # On Linux/macOS
# or
deploy.bat   # On Windows

# 2. Configure .env
nano .env    # Edit with your settings

# 3. Start services
docker-compose up -d

# 4. Verify
curl http://localhost/health
```

## 📋 Common Commands

### Docker Management

```bash
# Start all services
docker-compose up -d

# Stop all services
docker-compose down

# View logs
docker-compose logs -f backend
docker-compose logs -f nginx

# Restart specific service
docker-compose restart backend

# View running containers
docker ps

# Execute command in container
docker-compose exec backend bash
```

### Database Operations

```bash
# SQLite backup
docker cp cbt-chatbot-backend:/app/data/chatbot.db ./backup.db

# View database
sqlite3 data/chatbot.db ".tables"

# PostgreSQL (if using)
docker-compose exec postgres psql -U chatbot -d chatbot
```

### Logs & Debugging

```bash
# All logs (last 50 lines)
docker-compose logs --tail=50

# Backend errors only
docker-compose logs backend | grep ERROR

# Real-time monitoring
watch -n 1 'docker ps --format "table {{.Names}}\t{{.Status}}"'
```

## 🔐 Security Setup

### Generate Secure Keys

```bash
python3 << 'EOF'
import secrets
print("SECRET_KEY:", secrets.token_urlsafe(32))
print("JWT_SECRET_KEY:", secrets.token_urlsafe(32))
EOF
```

### SSL Certificates

```bash
# Let's Encrypt (free, automated)
sudo certbot certonly --standalone -d your-domain.com
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem

# Self-signed (testing only)
openssl req -x509 -newkey rsa:4096 -nodes \
  -out ssl/cert.pem -keyout ssl/key.pem -days 365
```

## ⚙️ Configuration Checklist

Essential settings in `.env`:

- [ ] `SECRET_KEY` - Changed from default
- [ ] `JWT_SECRET_KEY` - Changed from default
- [ ] `API_BASE_URL` - Your domain
- [ ] `FRONTEND_URL` - Your domain
- [ ] `GEMINI_API_KEY` - From https://aistudio.google.com
- [ ] `CORS_ORIGINS` - Your domain(s)
- [ ] `FLASK_ENV` - Set to `production`
- [ ] `FLASK_DEBUG` - Set to `false`

## 🔧 Troubleshooting

### Port Already in Use

```bash
# Kill process on port 5000
lsof -i :5000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Or change port in .env
API_PORT=8000
```

### Memory Issues

```bash
# Reduce workers
GUNICORN_WORKERS=2 docker-compose up -d backend

# Or set Docker memory limit
# In docker-compose.yml:
# mem_limit: 2g
```

### Database Locked (SQLite)

Migrate to PostgreSQL or increase timeout:
```python
conn = sqlite3.connect('chatbot.db', timeout=20.0)
```

### CORS Errors

```bash
# Update .env
CORS_ORIGINS=your-domain.com,www.your-domain.com

# Rebuild
docker-compose down && docker-compose up -d
```

## 📊 Monitoring

### Health Check

```bash
curl https://your-domain.com/health

# Response should include:
# {
#   "message": "CBT Chatbot API is running",
#   "ai_powered": true,
#   "ai_status": "enabled"
# }
```

### Resource Usage

```bash
docker stats

# Output shows CPU%, Memory, and I/O for each container
```

### Check Certificate Expiry

```bash
openssl x509 -in ssl/cert.pem -noout -dates
```

## 📝 Maintenance

### Regular Backups

```bash
# SQLite
docker-compose exec backend cp /app/data/chatbot.db /backup/chatbot-$(date +%Y%m%d).db

# PostgreSQL
docker-compose exec postgres pg_dump -U chatbot chatbot > backup-$(date +%Y%m%d).sql
```

### Update Application

```bash
git pull origin main
docker-compose down
docker-compose up -d --build
```

### Renew SSL Certificate

```bash
sudo certbot renew --force-renewal
sudo cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem
sudo cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem
docker-compose exec nginx nginx -s reload
```

## 🌐 Domain & DNS

### Point Domain to Server

In your DNS provider, create:

```
A Record:
  Host: @
  Value: YOUR_SERVER_IP
  TTL: 3600

A Record:
  Host: www
  Value: YOUR_SERVER_IP
  TTL: 3600
```

## 📞 Support

- **Logs:** `docker-compose logs -f`
- **Docs:** See DEPLOYMENT_GUIDE.md
- **Configuration:** See .env.example
- **API:** Available at `/docs` (if Swagger enabled)

## 🎯 Performance Tuning

### Optimize Gunicorn Workers

```bash
# Recommended: (2 × CPU cores) + 1
# Check CPU cores
nproc

# Set in .env or docker-compose
GUNICORN_WORKERS=5  # For 2-core server
```

### Database Optimization

SQLite → PostgreSQL migration commands:

```bash
# Excellent resource
# See DEPLOYMENT_GUIDE.md for detailed migration steps
```

---

**Last Updated:** 2026-03-27
