FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

WORKDIR /app

# Устанавливаем зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Скачиваем и устанавливаем официальную утилиту doqa
RUN curl -O https://doqa.app/downloads/doqa && chmod +x doqa && mv doqa /usr/local/bin/

# Копируем тесты
COPY . .