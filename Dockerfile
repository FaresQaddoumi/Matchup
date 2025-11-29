# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements first (better layer caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY backend ./backend

# Expose port Flask will run on
EXPOSE 5000

# Set environment variable so Flask knows where the app is
ENV FLASK_APP=backend/app.py

# Run the app
CMD ["python", "-m", "backend.app"]
