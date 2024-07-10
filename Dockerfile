# Достаём питон версии 3.9.9
FROM python:3.9.9-slim-buster

# Рабочая директория
WORKDIR /usr/src/TenzorQuiz

# Постановление переменных среды
# Предотвращает написание питоном pyc файлов на диск
ENV PYTHONDONTWRITEBYTECODE 1
# Предотвращает питон от буфферизации stdout и stderr
ENV PYTHONUNBUFFERED 1

# Установка зависимостей
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Копирование проекта
COPY . .