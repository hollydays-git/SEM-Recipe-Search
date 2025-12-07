# syntax=docker/dockerfile:1
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# requirements из КОРНЯ проекта
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# копируем весь backend-код
COPY app/ app/
ENV PYTHONPATH=/app

# открываем порт
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"]


