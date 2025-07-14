#!/bin/bash

echo "Building Docker containers..."
docker-compose build

echo "Starting services in detached mode..."
docker-compose up -d

echo "Deployment complete!"
echo "Your application should be running at http://localhost:8000"
echo "You can check the logs with: docker-compose logs -f"