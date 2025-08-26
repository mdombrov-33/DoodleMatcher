FROM python:3.12-slim-bookworm

WORKDIR /app

# Install system dependencies (curl)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml poetry.lock* /app/

# Install Poetry
RUN pip install --no-cache-dir poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-root --no-interaction --no-ansi

# Copy backend source code
COPY . /app

# Download ONNX model during build
RUN mkdir -p /app/models/clip && \
    curl -L https://huggingface.co/Qdrant/clip-ViT-B-32-vision/resolve/main/model.onnx \
    -o /app/models/clip/clip-vit-base-patch32.onnx

EXPOSE 8000

CMD ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
