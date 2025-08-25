FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /app
COPY app.py /app/

EXPOSE 8086

CMD ["python", "app.py"]
# Install gunicorn
RUN pip install gunicorn

# Use gunicorn instead of flask dev server
CMD ["gunicorn", "--bind", "0.0.0.0:8086", "app:app"]
