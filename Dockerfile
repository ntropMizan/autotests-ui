FROM mcr.microsoft.com/playwright/python:v1.61.0-noble

WORKDIR /app

# 1. Сначала копируем только requirements.txt (кэширование слоя)
COPY requirements.txt .

# 2. Устанавливаем зависимости + doqa-pytest
# Добавляем doqa-pytest прямо здесь, чтобы не менять requirements.txt
RUN pip install --no-cache-dir -r requirements.txt doqa-pytest

# 3. ОБЯЗАТЕЛЬНО: Устанавливаем браузеры для Playwright
# Без этого шага тесты упадут с ошибкой "Executable doesn't exist"
RUN playwright install --with-deps chromium

# 4. Копируем исходный код проекта (после установки зависимостей)
COPY . .