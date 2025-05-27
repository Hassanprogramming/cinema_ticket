# Dockerfile
# Use official Python 3.12 slim image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable stdout/stderr buffering
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all project files
COPY . .

# Wait for DB and run collectstatic (optional for production)
CMD ["/bin/bash", "-c", "\
  echo 'Waiting for DB...'; \
  while ! nc -z db 5432; do sleep 1; done; \
  echo 'DB is up!'; \
  python manage.py migrate && \
  python manage.py collectstatic --noinput && \
  exec uvicorn config.asgi:application --host 0.0.0.0 --port 8000"]
