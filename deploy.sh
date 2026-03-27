#!/bin/bash
# Setup script for CBT Chatbot deployment
# This script helps initialize the deployment environment

set -e  # Exit on any error

echo "================================================"
echo "CBT Chatbot - Deployment Setup Script"
echo "================================================"
echo ""

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker found: $(docker --version)"
echo "✅ Docker Compose found: $(docker-compose --version)"
echo ""

# Create .env file
echo "Setting up environment configuration..."

if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    
    # Generate secure random keys
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    JWT_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Replace in .env
    sed -i "s/your-super-secret-key-change-this-in-production/$SECRET_KEY/g" .env
    sed -i "s/your-jwt-secret-key-change-this/$JWT_SECRET_KEY/g" .env
    
    echo "✅ .env file created with secure random keys"
    echo ""
    echo "⚠️  IMPORTANT: Please edit .env and configure:"
    echo "   - API_BASE_URL (your domain)"
    echo "   - FRONTEND_URL (your domain)"
    echo "   - GEMINI_API_KEY (from https://aistudio.google.com/app/apikey)"
    echo "   - CORS_ORIGINS (your domain)"
    echo ""
    echo "Then run: docker-compose up -d"
else
    echo "✅ .env file already exists"
fi

# Create directories
echo "Creating necessary directories..."
mkdir -p logs
mkdir -p data
mkdir -p ssl

echo "✅ Directories created"
echo ""

# Check logs content
if [ -s .env ]; then
    echo "Current .env configuration (secrets hidden):"
    grep -E "^[A-Z_]+=" .env | sed 's/=.*/=/g' | head -10
    echo "..."
    echo ""
fi

echo "================================================"
echo "Setup complete!"
echo "================================================"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your production settings"
echo "2. Generate SSL certificates (if HTTPS):"
echo "   certbot certonly --standalone -d your-domain.com"
echo "   cp /etc/letsencrypt/live/your-domain.com/fullchain.pem ./ssl/cert.pem"
echo "   cp /etc/letsencrypt/live/your-domain.com/privkey.pem ./ssl/key.pem"
echo "3. Start the application:"
echo "   docker-compose up -d"
echo "4. Check health:"
echo "   curl http://localhost/health"
echo ""
echo "For more information, see: DEPLOYMENT_GUIDE.md"
