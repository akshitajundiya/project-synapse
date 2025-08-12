FROM python:3.10-slim

# Environment settings
ENV PYTHONUNBUFFERED=1 \
    PYTHONIOENCODING=utf-8

# Set working directory
WORKDIR /app

# Install OS dependencies (add/remove as needed)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first (better caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose port if needed
EXPOSE 8080

# Default command
CMD ["python", "cli.py", "--scenario", "overloaded_restaurant"]
