"""
Logging Configuration for CBT Chatbot
Structured logging with file rotation and multiple handlers
"""
import logging
import logging.handlers
import os
from datetime import datetime


def setup_logging(app, config):
    """
    Configure logging for the Flask application
    
    Args:
        app: Flask application instance
        config: Configuration object
    """
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # Set up root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
    
    # Clear existing handlers
    root_logger.handlers.clear()
    
    # Log format with timestamp, level, module and message
    formatter = logging.Formatter(
        '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler (always output to console)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)
    
    # File handler with rotation (1GB per file, keep 10 backups)
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            config.LOG_FILE,
            maxBytes=1024 * 1024 * 1024,  # 1GB
            backupCount=10,
            encoding='utf-8'
        )
        file_handler.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except (IOError, OSError) as e:
        logging.warning(f"Failed to set up file logging: {e}")
    
    # Flask app logger
    app.logger.setLevel(getattr(logging, config.LOG_LEVEL, logging.INFO))
    
    # Log startup message
    app.logger.info(f"Logging initialized - Level: {config.LOG_LEVEL}, File: {config.LOG_FILE}")
    app.logger.info(f"Environment: {config.FLASK_ENV}")
    app.logger.info(f"Debug Mode: {config.DEBUG}")


def get_logger(name):
    """Get or create a logger with the given name"""
    return logging.getLogger(name)


# Context managers for logging specific operations

class log_operation:
    """Context manager for logging operation timing and errors"""
    
    def __init__(self, operation_name, logger=None):
        self.operation_name = operation_name
        self.logger = logger or logging.getLogger(__name__)
        self.start_time = None
    
    def __enter__(self):
        self.start_time = datetime.now()
        self.logger.info(f"Starting: {self.operation_name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        duration = (datetime.now() - self.start_time).total_seconds()
        
        if exc_type is None:
            self.logger.info(f"Completed: {self.operation_name} ({duration:.2f}s)")
        else:
            self.logger.error(
                f"Failed: {self.operation_name} after {duration:.2f}s - {exc_type.__name__}: {exc_val}"
            )
        
        return False  # Don't suppress exceptions
