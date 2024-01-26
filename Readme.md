# Y_lab_homeworks
Первое домашнее задание: Создание API сервиса для CRUD операций с меню, подменю и блюдами. Основные технологии: FastAPI, SQLAlchemy, PostgreSQL, Docker-Compose

## Запуск базы данных в контейнере (Рекомендуется)
Для запуска чистой базы данных в контейнере
```
docker-compose up --remove-orphans --force-recreate --build  -d
```

Для остановки контейнера 
```
docker-compose down
```

Изменить настройки запуска контейнера и базы данных (Например, в случае если 5435 порт занят) можно в файле .env

## Запуск базы данных в локальном postgreSQL (Не рекомендуется)

### Для Linux
```
sudo -u postgres psql
CREATE DATABASE menu_db;
CREATE USER db_user WITH PASSWORD 'password';
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE menu_db TO db_user;
```
Меняем порт в файле .env на **5432**, остальное оставляем как есть
```
DB_USERNAME=...
DB_PASSWORD=...
DB_DATABASE=...
DB_HOST=...
DB_PORT=5432
```

### Для Windows
Если не создан суперпользователь
```
cd C:\Program Files\PostgreSQL\{Ваша_Версия_PostgreSQL}\bin
createuser –U postgres operator
psql –U postgres
ALTER ROLE operator SUPERUSER CREATEROLE CREATEDB;
\q
```
Создаём базу данных и пользователя
```
cd C:\Program Files\PostgreSQL\{Ваша_Версия_PostgreSQL}\bin
psql –U postgres
CREATE DATABASE menu_db;
CREATE USER db_user WITH PASSWORD 'password';
ALTER ROLE db_user SET client_encoding TO 'utf8';
ALTER ROLE db_user SET default_transaction_isolation TO 'read committed';
GRANT ALL PRIVILEGES ON DATABASE menu_db TO db_user;
```
Меняем порт в файле .env на **5432**, остальное оставляем как есть
```
DB_USERNAME=...
DB_PASSWORD=...
DB_DATABASE=...
DB_HOST=...
DB_PORT=5432
```

## Запуск приложения и установка зависимостей

### Для Windows
1)Создаём виртуальное окружение 
```
python -m venv venv
venv\Scripts\activate.bat
```
2)Устанавливаем зависимости
```
pip install -r requirements.txt
```

### Для Linux
1)Создаём виртуальное окружение 
```
sudo apt install -y python3-venv
python3 -m venv venv
source venv\bin\activate
```
2)Устанавливаем зависимости
```
pip install -r requirements.txt
```
После настройки базы данных и установки необходимых зависимостей, можно запускать fastAPI приложение
`python -m uvicorn main:app --reload`