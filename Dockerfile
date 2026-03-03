# ----------------------------------------------------
# Builder
# ----------------------------------------------------

# Use official Python slim image as base
FROM python:3.11-slim AS builder

# Set working directory inside the container
WORKDIR /app

# System dependencys
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip

# Copy only requirements first to leverage Docker cache
COPY requirements-dev.txt requirements.txt ./

# Create pre-compiled wheels
RUN pip wheel --no-cache-dir --wheel-dir=/wheels -r requirements.txt -r requirements-dev.txt

# ----------------------------------------------------
# Runtime base
# ----------------------------------------------------
FROM python:3.11-slim AS runtime

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libpq5 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

# Copy compiled wheels
COPY --from=builder /wheels /wheels


# ----------------------------------------------------
# Development stage
# ----------------------------------------------------
FROM runtime AS dev

COPY requirements.txt requirements-dev.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements-dev.txt

# Copy all application code into the container
COPY . .

# Expose port for Uvicorn/FastAPI
EXPOSE 8000

# Command to run the FastAPI app using Uvicorn
# --host 0.0.0.0 allows access from outside the container
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]



# ----------------------------------------------------
# Production stage
# ----------------------------------------------------
FROM runtime AS prod

COPY requirements.txt ./

RUN pip install --no-cache-dir --no-index --find-links=/wheels -r requirements.txt 

COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]




