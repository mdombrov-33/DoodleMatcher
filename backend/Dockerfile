# Use official Python runtime as base image
FROM python:3.12-slim-bookworm

# Set working directory inside the container
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files to container
COPY pyproject.toml poetry.lock* /app/

# Install Poetry package manager
RUN pip install --no-cache-dir poetry

# Install dependencies without creating a virtualenv (system-wide)
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy backend source code + pre-downloaded model
COPY . /app

# Expose port the app runs on
EXPOSE 8000
