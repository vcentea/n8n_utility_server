# Use Playwright's official base image which includes all browser dependencies
FROM mcr.microsoft.com/playwright/python:v1.49.0-jammy

# Install system dependencies
# - poppler-utils: PDF processing
# - ffmpeg: Required by yt-dlp for subtitle/media processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    poppler-utils \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install Playwright browsers (Chromium only to save space)
RUN playwright install chromium

# Copy application code
COPY app ./app

# Environment variables
ENV PORT=2277
ENV TEMP_PATH=/tmp/pdf_service

# Create temp directory
RUN mkdir -p /tmp/pdf_service

EXPOSE 2277

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "2277"]
