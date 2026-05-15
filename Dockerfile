# SWARMICA Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the package
COPY swarmica/ ./swarmica/
COPY pyproject.toml .
COPY README.md .

# Install the package
RUN pip install -e .

# Default command
CMD ["python", "-c", "from swarmica import SwarmEngine; print('SWARMICA v1.0.0 ready')"]
