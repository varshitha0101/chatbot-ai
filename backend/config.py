"""
Configuration Management for CBT Chatbot
Centralizes all environment variables and configuration
"""
import os
import logging
from datetime import timedelta

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class Config:
    """Base configuration"""
    
    # Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "super-secret-key-change-this")
    FLASK_ENV = os.environ.get("FLASK_ENV", "production")
    DEBUG = FLASK_ENV == "development"
    
    # API
    API_HOST = os.environ.get("API_HOST", "0.0.0.0")
    API_PORT = int(os.environ.get("API_PORT", 5000))
    API_BASE_URL = os.environ.get("API_BASE_URL", "http://localhost:5000")
    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:8080")
    
    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-secret-key-change-this")
    JWT_EXPIRATION_HOURS = int(os.environ.get("JWT_EXPIRATION_HOURS", 2))
    JWT_ALGORITHM = "HS256"
    
    # Gemini AI
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
    USE_AI = os.environ.get("USE_AI", "true").lower() == "true"
    GEMINI_MODEL = "gemini-1.5-flash"
    
    # Database
    DATABASE_TYPE = os.environ.get("DATABASE_TYPE", "sqlite")
    DATABASE_URL = os.environ.get("DATABASE_URL", "sqlite:///chatbot.db")
    
    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FILE = os.environ.get("LOG_FILE", "logs/app.log")
    
    # Security
    CORS_ORIGINS = os.environ.get(
        "CORS_ORIGINS",
        "http://localhost:3000,http://localhost:8080"
    ).split(",")
    RATE_LIMIT_ENABLED = os.environ.get("RATE_LIMIT_ENABLED", "true").lower() == "true"
    RATE_LIMIT_REQUESTS = int(os.environ.get("RATE_LIMIT_REQUESTS", 100))
    RATE_LIMIT_WINDOW = int(os.environ.get("RATE_LIMIT_WINDOW", 3600))
    
    # Monitoring
    SENTRY_DSN = os.environ.get("SENTRY_DSN", "")
    
    @staticmethod
    def validate_config():
        """Validate critical configuration on startup"""
        errors = []
        
        # Check JWT secret key
        if Config.JWT_SECRET_KEY == "jwt-secret-key-change-this":
            errors.append(
                "ERROR: JWT_SECRET_KEY not configured. Set JWT_SECRET_KEY in .env"
            )
        
        # Check Flask secret key
        if Config.SECRET_KEY == "super-secret-key-change-this":
            errors.append(
                "ERROR: SECRET_KEY not configured. Set SECRET_KEY in .env"
            )
        
        # Check Gemini API key if AI is enabled
        if Config.USE_AI and not Config.GEMINI_API_KEY:
            errors.append(
                "WARNING: USE_AI=true but GEMINI_API_KEY not set. "
                "AI responses will be disabled. Get key from https://aistudio.google.com/app/apikey"
            )
        
        if errors:
            for error in errors:
                logging.warning(error) if error.startswith("WARNING") else logging.error(error)
        
        return len([e for e in errors if e.startswith("ERROR")]) == 0


class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    FLASK_ENV = "development"
    DATABASE_URL = "sqlite:///chatbot_dev.db"


class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DATABASE_URL = "sqlite:///:memory:"
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    FLASK_ENV = "production"


def get_config():
    """Get appropriate configuration based on environment"""
    env = os.environ.get("FLASK_ENV", "production").lower()
    
    if env == "development":
        return DevelopmentConfig
    elif env == "testing":
        return TestingConfig
    else:
        return ProductionConfig
