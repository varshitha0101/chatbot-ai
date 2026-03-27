"""
WSGI entry point for production deployment
Run with: gunicorn -c gunicorn_config.py wsgi:app
"""
import os
import sys
import logging

# Add the backend directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app import app
from backend.config import get_config, Config
from backend.logging_config import setup_logging

# Get configuration
config_class = get_config()

# Validate configuration on startup
if not config_class.validate_config():
    logging.error("Configuration validation failed. Exiting.")
    sys.exit(1)

# Set up logging
setup_logging(app, config_class)

# Configure Flask
app.config.from_object(config_class)

if __name__ == "__main__":
    app.run(
        host=config_class.API_HOST,
        port=config_class.API_PORT,
        debug=config_class.DEBUG
    )
