# Use Alpine Linux as base image
FROM python:3.11-alpine

# Install system dependencies
RUN apk add --no-cache \
    curl \
    build-base \
    libffi-dev \
    openssl-dev \
    cargo \
    git

# Install uv package manager
RUN pip install uv

# Set working directory
WORKDIR /app

RUN git clone https://github.com/quantum-craft/binance-connector-python.git

COPY pyproject.toml uv.lock ./
COPY main.py ./

# Install dependencies using uv
RUN uv sync --frozen

# Set environment variables for logging
ENV PYTHONUNBUFFERED=1
ENV PYTHONFAULTHANDLER=1

# Set the entry command
CMD ["uv", "run", "main.py"]
