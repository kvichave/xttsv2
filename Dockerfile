FROM nvidia/cuda:11.8.0-cudnn8-runtime-ubuntu22.04

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3-pip \
    python3.10-venv \
    ffmpeg \
    libsndfile1 \
    git \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set python3.10 as default
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.10 1

# Upgrade pip
RUN pip install --upgrade pip

# Copy requirements.txt
COPY requirements.txt .

# Install Python dependencies (with PyTorch + CUDA 11.8)
RUN pip install --extra-index-url https://download.pytorch.org/whl/cu118 -r requirements.txt

# Copy application files
COPY . /app
WORKDIR /app

# Expose FastAPI port
EXPOSE 8000

# Run FastAPI with correct filename (tts.py)
CMD ["uvicorn", "tts:app", "--host", "0.0.0.0", "--port", "8000"]
