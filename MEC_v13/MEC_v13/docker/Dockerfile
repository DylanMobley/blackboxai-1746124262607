# Use NVIDIA base image for GPU inference support
FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

# Create non-root user (security hardening)
RUN useradd -ms /bin/bash mecuser

# Set working directory
WORKDIR /app

# Copy only requirements first (caching)
COPY ./requirements.txt /app/requirements.txt

# Install system dependencies + Python libs
RUN apt-get update && apt-get install -y \
    ffmpeg redis wget curl git build-essential && \
    apt-get clean && rm -rf /var/lib/apt/lists/* && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

# Now copy full source AFTER requirements to take advantage of Docker cache
COPY ./backend /app/backend
COPY ./ontology /app/ontology
COPY ./symbolic /app/symbolic
COPY ./emotion_core /app/emotion_core
COPY ./microservices /app/microservices
COPY ./config /app/config
COPY ./pretrained /app/pretrained

# Expose key ports
EXPOSE 5101    # Flask
EXPOSE 5105    # Clone Service
EXPOSE 6379    # Redis (optional)

# Set ownership and switch to secure user
RUN chown -R mecuser:mecuser /app
USER mecuser

# Add Docker healthcheck for orchestration
HEALTHCHECK --interval=30s --timeout=5s --start-period=20s --retries=3 \
  CMD curl -f http://localhost:5101/health || exit 1

# Default: launch Flask API (overridden by docker-compose for Celery worker)
CMD ["python3", "backend/api.py"]
