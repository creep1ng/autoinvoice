FROM mcr.microsoft.com/devcontainers/python:3.12-trixie

# Copy UV and UVX binaries from the official UV image
COPY --from=ghcr.io/astral-sh/uv:0.8.22 /uv /uvx /bin/

# Install system dependencies for the project
# - tesseract-ocr: For OCR processing
# - poppler-utils: For PDF handling
# - build-essential & libpq-dev: For compiling Python packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    poppler-utils && \
    rm -rf /var/lib/apt/lists/*

# Set UV environment variables for better devcontainer experience
ENV UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/workspace/.venv

WORKDIR /workspace

CMD ["sleep", "infinity"]
