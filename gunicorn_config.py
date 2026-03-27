"""
Gunicorn Configuration for CBT Chatbot
Production WSGI server configuration
"""
import os
import multiprocessing

# Server socket
# For Railway: use PORT env variable if available
port = os.environ.get('PORT', os.environ.get('API_PORT', 5000))
bind = f"{os.environ.get('API_HOST', '0.0.0.0')}:{port}"
backlog = 2048

# Worker processes
workers = os.environ.get('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1)
worker_class = 'sync'  # Use sync workers. For async: 'gevent', 'eventlet', 'asyncio'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = os.environ.get('ACCESS_LOG', '/var/log/chatbot/access.log')
errorlog = os.environ.get('ERROR_LOG', '/var/log/chatbot/error.log')
loglevel = os.environ.get('LOG_LEVEL', 'info').lower()
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = 'cbt-chatbot'

# Server mechanics
daemon = False
pidfile = '/var/run/gunicorn_cbt.pid'
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (if needed)
# keyfile = '/path/to/keyfile.key'
# certfile = '/path/to/certfile.crt'
# ssl_version = 'TLSv1_2'
# ciphers = 'HIGH:!aNULL:!MD5'

# Application
paste = None
virtualenv = None
pythonpath = None

# Server hooks (optional)
def on_starting(server):
    """Called just before the master process is initialized."""
    print("Gunicorn server is starting...")

def on_exit(server):
    """Called just after the master process has exited."""
    print("Gunicorn server is exiting...")

def when_ready(server):
    """Called once the wsgi app has been loaded."""
    print("Gunicorn server ready. Spawning workers...")
