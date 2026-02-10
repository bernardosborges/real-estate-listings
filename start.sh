#!/bin/bash
# start.sh - Script to run FastAPI in production on AWS (Linux)

# Define number of workers
WORKERS=4

# Define host and port
HOST=0.0.0.0
PORT=8000

# Activate virtual environment (assume venv is at /home/ubuntu/venv)
if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo "Virtual environment not found! Please create it with 'python -m venv venv'"
    exit 1
fi

# Load environment variables from .env
if [ -f ".env" ]; then
    export $(grep -v '^#' .env | xargs)
else
    echo ".env file not found! Please upload it to the server."
    exit 1
fi

# Run FastAPI backend with Uvicorn
echo "Starting FastAPI server..."
exec uvicorn app.main:app \
    --host $HOST \
    --port $PORT \
    --workers $WORKERS \
    --log-level info