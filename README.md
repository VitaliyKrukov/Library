markdown
# Python Library - Django REST API

Проект системы управления библиотекой на Django REST Framework с JWT аутентификацией.

## 🚀 Возможности

- 🔐 JWT аутентификация
- 👥 Кастомная модель пользователя с email
- 📚 Управление книгами и авторами
- 📖 Система выдачи книг
- 📱 REST API
- 📊 Документация API (Swagger/ReDoc)
- 🐳 Docker контейнеризация
- 🗄️ PostgreSQL база данных

## 🛠️ Технологии

- **Backend**: Django 5.2.8, Django REST Framework 3.16.1
- **База данных**: PostgreSQL
- **Аутентификация**: JWT (djangorestframework-simplejwt)
- **Документация**: drf-yasg
- **Контейнеризация**: Docker, Docker Compose
- **Язык**: Python 3.13

## 📦 Быстрый старт

### Клонирование и настройка
```
git clone <repository-url>
cd Python_Diplom
```
### Создаем .env
```
SECRET_KEY=django-insecure-your-secret-key-here-change-in-production
DEBUG=True
DATABASE_NAME=library_db
DATABASE_USER=postgres
DATABASE_PASSWORD=password
DATABASE_HOST=db
DATABASE_PORT=5432
```

### Сборка и запуск
```
docker-compose up --build
```
### В другом терминале - настройка БД
```
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```
### Доступ к приложению
Приложение: http://localhost:8000

Админка: http://localhost:8000/admin

Документация API: http://localhost:8000/swagger

### 🔑 API Endpoints
Аутентификация
POST /api/auth/register/ - Регистрация пользователя

POST /api/auth/token/ - Получение JWT токена

POST /api/auth/token/refresh/ - Обновление токена

Пользователи
GET/PUT /api/profile/ - Профиль пользователя

Библиотека
GET /api/library/books/ - Список книг

GET /api/library/books/{id}/ - Детали книги

POST /api/library/issuance/ - Выдача книги

GET /api/library/my-books/ - Мои книги

### 🗃️ Модели данных
Пользователь (User)
email - Email (уникальный, используется для входа)

phone - Телефон

avatar - Аватар

password - Пароль

Книга (Book)
title - Название книги

author - Автор (ForeignKey)

isbn - ISBN

description - Описание

publication_date - Дата публикации

is_available - Доступна для выдачи

Автор (Author)
name - Имя автора

bio - Биография

birth_date - Дата рождения

Выдача книги (Issuance)
user - Пользователь (ForeignKey)

book - Книга (ForeignKey)

issued_date - Дата выдачи

due_date - Срок возврата

returned_date - Дата возврата

## ⚙️ Конфигурация
Настройки Django (config/settings.py)

### Основные настройки
AUTH_USER_MODEL = 'users.User'
DEBUG = True

### База данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'library_db',
        'USER': 'postgres',
        'PASSWORD': 'password',
        'HOST': 'db',
        'PORT': '5432',
    }
}

### JWT настройки
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=60),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}


## 🔧 Разработка
Установка зависимостей
```
pip install -r requirements.txt
```
Миграции базы данных
```
python manage.py makemigrations
python manage.py migrate
```
Создание суперпользователя
```
python manage.py createsuperuser
```
Запуск сервера разработки
```
python manage.py runserver
```

## 📊 Документация API
После запуска проекта доступна автоматическая документация:

Swagger UI: http://localhost:8000/swagger/

ReDoc: http://localhost:8000/redoc/

## 🐳 Docker команды
Основные команды
### Запуск контейнеров
```
docker-compose up -d
```
### Остановка контейнеров
```
docker-compose down
```
### Просмотр логов
```
docker-compose logs -f web
```
### Выполнение команд в контейнере
```
docker-compose exec web python manage.py migrate
```
### Пересборка образов
```
docker-compose build --no-cache
```
### Запуск с пересборкой
```
docker-compose up --build
```
### Очистка Docker
```
docker system prune -a
```
## 🔐 Аутентификация
Регистрация пользователя
```
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123",
    "password_confirm": "securepassword123"
  }'
 ```
Получение JWT токена
```
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "securepassword123"
  }'
```
Использование токена
```
curl -X GET http://localhost:8000/api/profile/ \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```
## 🚀 Деплой
Продакшен настройки

Установите DEBUG=False

Настройте надежный SECRET_KEY

Настройте PostgreSQL с надежными паролями

Настройте сервер для статических файлов

Используйте Gunicorn/Uvicorn для запуска

Пример продакшен Dockerfile
dockerfile
FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]

# Конец