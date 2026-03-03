# Use official Python slim image as base
FROM python:3.11-slim

# System dependencys
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside the container
WORKDIR /app

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all application code into the container
COPY . .

# Expose port for Uvicorn/FastAPI
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
# --host 0.0.0.0 allows access from outside the container
# --reload is optional for development
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]