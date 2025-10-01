FROM mcr.microsoft.com/devcontainers/base:debian-12

# Install Python 3.12 via deadsnakes or the distro if available
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    wget \
    ca-certificates \
    build-essential \
    libpq-dev \
    python3.12 \
    python3.12-venv \
    python3.12-distutils \
    python3-pip \
    tesseract-ocr \
    poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Ensure 'python' refers to python3.12
RUN update-alternatives --install /usr/bin/python python /usr/bin/python3.12 1 || true

WORKDIR /workspace

CMD ["sleep", "infinity"]
