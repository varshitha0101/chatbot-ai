# Multi-stage build for CBT Chatbot
# Stage 1: Builder
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Stage 2: Runtime
FROM python:3.11-slim

WORKDIR /app

# Install runtime dependencies only
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy Python dependencies from builder
COPY --from=builder /root/.local /root/.local

# Add local pip to PATH
ENV PATH=/root/.local/bin:$PATH

# Copy application code
COPY backend ./backend
COPY wsgi.py .
COPY gunicorn_config.py .

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Create necessary directories for logs
RUN mkdir -p /var/log/chatbot /var/run && \
    chown -R appuser:appuser /var/log/chatbot /var/run

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/ || exit 1

# Run Gunicorn
# Run Gunicorn
CMD ["python", "-m", "gunicorn", "-c", "gunicorn_config.py", "wsgi:app"]
