# ═══════════════════════════════════════════════════════════════════════════════
# DeployFlow — Production Dockerfile
# Multi-stage build for minimal, secure image
# ═══════════════════════════════════════════════════════════════════════════════

# ─── Stage 1: Base with dependencies ────────────────────────────────────────
FROM python:3.11-slim AS base

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PORT=5000 \
    ENVIRONMENT=production

# Create non-root user for security
RUN groupadd --gid 1001 deployflow && \
    useradd --uid 1001 --gid deployflow --shell /bin/bash --create-home deployflow

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# ─── Stage 2: Application ────────────────────────────────────────────────────
FROM base AS app

# Copy application source code
COPY --chown=deployflow:deployflow . .

# Create data directory for SQLite
RUN mkdir -p /app/data && chown deployflow:deployflow /app/data

# Switch to non-root user
USER deployflow

# Expose application port
EXPOSE 5000

# Health check — tests the real /health endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Production entrypoint: Gunicorn WSGI server
# - 2 workers (adjust for your server CPU count)
# - Bind to all interfaces on PORT
# - Timeout 120s for slow DB operations
CMD ["gunicorn", \
     "--bind", "0.0.0.0:5000", \
     "--workers", "2", \
     "--timeout", "120", \
     "--access-logfile", "-", \
     "--error-logfile", "-", \
     "--log-level", "info", \
     "app:app"]
