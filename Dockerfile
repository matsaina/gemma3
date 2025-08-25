FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Expose port
EXPOSE 8086

# Run Uvicorn (production mode)
# Run Uvicorn with 1 worker and 2 threads for CPU-friendly concurrency
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8086", "--workers", "1", "--threads", "2", "--loop", "uvloop", "--http", "httptools", "--timeout-keep-alive", "120"]

