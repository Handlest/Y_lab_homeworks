# Y_lab_homeworks
Первое домашнее задание: Создание API сервиса для CRUD операций с меню, подменю и блюдами. Основные технологии: FastAPI, SQLAlchemy, PostgreSQL, Docker-Compose

Второе домашнее задание: Обернуть приложение в докер контейнер, написать тесты и оптимизировать запрос к базе данных

**Оптимизированный запрос для задания 3 находится по пути routers/menu_routes.py. Функция "get_menu_by_id"**
## Запуск приложения
Для запуска приложения и базы данных в контейнере:
```
docker-compose -f docker-compose.yaml up --remove-orphans --force-recreate --build  -d
```
Для остановки контейнера с базой данных и приложением:
```
docker-compose down
```
## Запуск тестов
Для запуска CRUD тестов и тестового сценария:
```
docker-compose -f docker-compose-test.yaml up --remove-orphans --force-recreate --build
```
Для остановки базы данных и приложения: ctrl+c

## Просмотр документации
Для просмотра документации можно перейти в браузере
```
http://localhost:8000/docs#/
```
