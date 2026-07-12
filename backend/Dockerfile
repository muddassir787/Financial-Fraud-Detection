# ----------------------------------------------------
# FastAPI Backend Dockerfile
# ----------------------------------------------------

FROM python:3.11-slim

# ----------------------------------------------------
# Environment Variables
# ----------------------------------------------------

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# ----------------------------------------------------
# Install System Packages
# ----------------------------------------------------

RUN apt-get update && \
    apt-get install -y \
        gcc \
        build-essential \
        curl && \
    rm -rf /var/lib/apt/lists/*

# ----------------------------------------------------
# Working Directory
# ----------------------------------------------------

WORKDIR /app

# ----------------------------------------------------
# Install Python Dependencies
# ----------------------------------------------------

COPY requirements.txt .

RUN pip install --upgrade pip

RUN pip install --no-cache-dir -r requirements.txt

# ----------------------------------------------------
# Copy Application
# ----------------------------------------------------

COPY . .

# ----------------------------------------------------
# Expose FastAPI Port
# ----------------------------------------------------

EXPOSE 8000

# ----------------------------------------------------
# Health Check
# ----------------------------------------------------

HEALTHCHECK --interval=30s --timeout=5s --start-period=20s \
CMD curl -f http://localhost:8000/health || exit 1

# ----------------------------------------------------
# Run FastAPI
# ----------------------------------------------------

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]