#!/bin/bash

# Deployment automation script for MEC_v13 system

# Build and start all containers
echo "Building and starting Docker containers..."
docker-compose -f MEC_v13/docker/docker-compose.yml up --build -d

# Wait for services to be healthy
echo "Waiting for services to become healthy..."
sleep 30

# Run database migrations or setup if needed
echo "Running database migrations..."
docker exec -it mec_api alembic upgrade head

# Additional deployment automation tasks
# For example, seed initial data, clear caches, etc.
# echo "Seeding initial data..."
# docker exec -it mec_api python3 scripts/seed_data.py

# Check container statuses
echo "Checking container statuses..."
docker-compose -f MEC_v13/docker/docker-compose.yml ps

echo "Deployment completed successfully."
