# syntax=docker/dockerfile:1
FROM python:3.11-slim

WORKDIR /app

# Копируем зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r /app/requirements.txt

# Копируем содержимое build context (твою папку embedding_service) внутрь /app/embedding_service
COPY . /app/embedding_service

ENV PYTHONPATH=/app/embedding_service

EXPOSE 8100

CMD ["uvicorn", "embedding_service.main:app", "--host", "0.0.0.0", "--port", "8100"]
