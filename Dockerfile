FROM python:3.11-slim

# Системные зависимости
RUN apt-get update && apt-get install -y \
    curl \
    bash \
    && rm -rf /var/lib/apt/lists/*

# Рабочая директория
WORKDIR /app

# Зависимости Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем проект
COPY . .

# Директории для артефактов
RUN mkdir -p allure-results screenshots

# Переменные окружения
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Команда по умолчанию (переопределяется в docker-compose)
CMD ["pytest", "tests/", "-v", "--alluredir=allure-results"]