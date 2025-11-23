# Use Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements (if you have it)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose Flask default port
EXPOSE 5000

# Start Flask
CMD ["python", "app.py"]
