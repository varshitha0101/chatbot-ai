@echo off
REM Setup script for CBT Chatbot deployment on Windows
REM This script helps initialize the deployment environment

setlocal enabledelayedexpansion

echo ================================================
echo CBT Chatbot - Deployment Setup Script (Windows)
echo ================================================
echo.

REM Check prerequisites
echo Checking prerequisites...

where docker >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Docker not found. Please install Docker Desktop: https://docs.docker.com/get-docker/
    exit /b 1
)

for /f "tokens=3" %%A in ('docker --version') do set DOCKER_VERSION=%%A
echo [OK] Docker found: %DOCKER_VERSION%

where docker-compose >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [X] Docker Compose not found. Please install Docker Compose.
    exit /b 1
)

for /f "tokens=3" %%A in ('docker-compose --version') do set COMPOSE_VERSION=%%A
echo [OK] Docker Compose found: %COMPOSE_VERSION%
echo.

REM Create .env file
echo Setting up environment configuration...

if not exist .env (
    echo Creating .env file...
    copy .env.example .env
    
    REM Note: For Windows, keys should be manually set or use PowerShell
    echo [OK] .env file created
    echo.
    echo [WARNING] IMPORTANT: Please edit .env and configure:
    echo    - SECRET_KEY (generate random value)
    echo    - JWT_SECRET_KEY (generate random value)
    echo    - API_BASE_URL (your domain)
    echo    - FRONTEND_URL (your domain)
    echo    - GEMINI_API_KEY (from https://aistudio.google.com/app/apikey)
    echo    - CORS_ORIGINS (your domain)
    echo.
    echo Then run: docker-compose up -d
) else (
    echo [OK] .env file already exists
)

REM Create directories
echo Creating necessary directories...
if not exist logs mkdir logs
if not exist data mkdir data
if not exist ssl mkdir ssl

echo [OK] Directories created
echo.

echo ================================================
echo Setup complete!
echo ================================================
echo.
echo Next steps:
echo 1. Edit .env file with your production settings
echo 2. Generate SSL certificates (if HTTPS):
echo    certbot certonly --standalone -d your-domain.com
echo    Copy certificates to ./ssl/ directory
echo 3. Start the application:
echo    docker-compose up -d
echo 4. Check health:
echo    curl http://localhost/health
echo.
echo For more information, see: DEPLOYMENT_GUIDE.md
echo.

pause
