# Use a lightweight Python base image
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && \
    apt-get install -y --no-install-recommends git curl && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir torch transformers requests flask

RUN git clone https://huggingface.co/google/gemma-3-270m /model

WORKDIR /app

COPY app.py /app/

# Expose the new port
EXPOSE 8086

CMD ["python", "app.py"]
