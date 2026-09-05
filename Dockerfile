FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

WORKDIR /app

# Копируем только requirements.txt для кэширования слоя зависимостей
COPY requirements.txt .

# Устанавливаем Python-зависимости + doqa-pytest
# Браузеры уже есть в базовом образе, эта команда НЕ нужна!
RUN pip install --no-cache-dir -r requirements.txt doqa-pytest

# Копируем исходный код проекта
COPY . .