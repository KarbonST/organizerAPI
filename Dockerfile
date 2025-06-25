# 1. Базовый образ с Python
FROM python:3.13

# 2. Рабочая папка внутри контейнера
WORKDIR /app

# 3. Копируем список зависимостей и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Копируем весь код приложения
COPY . .

# 5. Пробрасываем порт, на котором будет слушать Uvicorn
EXPOSE 8000

# 6. Команда запуска сервера
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]