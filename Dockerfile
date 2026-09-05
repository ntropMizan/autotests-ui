FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

WORKDIR /app

COPY requirements.txt .
# ВАЖНО: doqa-pytest должен быть установлен явно
RUN pip install --no-cache-dir -r requirements.txt doqa-pytest

# ВАЖНО: Браузеры должны быть установлены
RUN playwright install --with-deps chromium

COPY . .