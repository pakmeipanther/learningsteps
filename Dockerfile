# Step 1: Use an official, lightweight Python base engine
FROM python:3.12-slim

# Step 2: Set secure environment flags for Python execution inside containers
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app:/app/api

# Step 3: Establish an isolated execution directory inside the container
WORKDIR /app

# Step 4: Install system dependencies needed for building PostgreSQL drivers
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Step 5: Copy the dependency ledger first to take advantage of Docker caching
COPY requirements.txt .

# Step 6: Install your Python application packages cleanly
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Step 7: Copy the entire api codebase into the working container layer
COPY api/ ./api/

# Step 8: Expose the network port your FastAPI application listens on
EXPOSE 8000

# ========================================================================
# DEVSECOPS STANDARD: Establish a hardened non-root container profile
# ========================================================================
RUN groupadd -g 1000 appgroup && \
    useradd -r -u 1000 -g appgroup -m -d /home/appuser -s /bin/bash appuser

# SUCCESS VALUE: Grants explicit folder permissions BEFORE dropping privileges
RUN mkdir -p /home/appuser/.vscode-server/bin && \
    chown -R appuser:appgroup /home/appuser

# Drop system execution runtime authority to your verified unprivileged user
USER appuser

# Regularly poll the application entrypoint to ensure the server is alive
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:8000/health || exit 1

# Step 9: Define the immutable operational command to spin up your Uvicorn server
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]